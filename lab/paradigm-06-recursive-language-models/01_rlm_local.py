"""
01_rlm_local.py — RLM Demo using Local Ollama (qwen3:4b)
=========================================================
Use case : 30 sales call transcripts.
Task     : Which competitors are mentioned, and how many times?

Two approaches compared:
  Plain agent — all 30 transcripts in ONE LLM call → context rot
  RLM agent   — one transcript per sub-call → aggregate in Python Counter

No API key needed. Runs fully offline via Ollama.

Prereq:
    ollama serve          # start Ollama daemon
    ollama pull qwen3:4b  # if not already installed

Run:
    python 01_rlm_local.py
"""

import json
import re
import random
import time
from collections import Counter
from dataclasses import dataclass, field
from openai import OpenAI

# ── Client: Ollama's OpenAI-compatible endpoint ───────────────────────────────
client = OpenAI(
    api_key="ollama",                   # Ollama doesn't validate the key
    base_url="http://localhost:11434/v1",
)
MODEL = "qwen3:4b"

# ── Competitors to track ──────────────────────────────────────────────────────
COMPETITORS = ["Salesforce", "HubSpot", "Pipedrive", "Zoho", "Freshsales"]

# ── Synthetic transcript generator ───────────────────────────────────────────
# We generate fake transcripts with known ground-truth competitor mentions
# so we can measure accuracy precisely.
random.seed(7)

FILLER = [
    "The customer asked about our onboarding timeline and seemed satisfied.",
    "We discussed pricing tiers and the VP of Sales will review the proposal.",
    "Their main pain point is manual reporting — they want automation.",
    "The deal size is around $40k annually with a Q3 close target.",
    "They want a pilot with 10 seats before committing to a full rollout.",
    "Integration with their existing ticketing system is a must-have.",
    "Follow-up scheduled for next Tuesday to demo the analytics dashboard.",
    "The champion is enthusiastic but needs sign-off from procurement.",
]

COMP_SENTENCES = [
    "The prospect mentioned they're also evaluating {comp}.",
    "They said {comp} offered them a lower price but lacked key features.",
    "We had to address a concern about how we compare to {comp} on reporting.",
    "The customer showed us a {comp} demo they attended last week.",
    "Their current vendor is {comp} and they're unhappy with support.",
]


def make_transcript(idx: int) -> tuple[str, Counter]:
    """Generate one transcript. Returns (text, true_mentions_counter)."""
    lines    = random.sample(FILLER, k=random.randint(4, 6))
    mentions: Counter = Counter()

    # Inject 0-2 competitor mentions randomly
    for _ in range(random.randint(0, 2)):
        comp     = random.choice(COMPETITORS)
        sentence = random.choice(COMP_SENTENCES).format(comp=comp)
        lines.insert(random.randint(0, len(lines)), sentence)
        mentions[comp] += 1

    text = f"[Transcript {idx:03d}]\n" + " ".join(lines)
    return text, mentions


# Build 30 transcripts and record ground truth
TRANSCRIPTS: list[str] = []
TRUE_COUNTS: Counter   = Counter()

for i in range(30):
    text, mentions = make_transcript(i)
    TRANSCRIPTS.append(text)
    TRUE_COUNTS.update(mentions)


# ── Metrics ───────────────────────────────────────────────────────────────────
@dataclass
class Metrics:
    calls:          int   = 0
    prompt_tok:     int   = 0
    completion_tok: int   = 0
    max_ctx:        int   = 0    # tokens in the largest single call
    elapsed:        float = 0.0

    @property
    def total_tok(self):
        return self.prompt_tok + self.completion_tok

    def record(self, usage, fallback_chars: int):
        self.calls += 1
        pt = usage.prompt_tokens     if usage else fallback_chars // 4
        ct = usage.completion_tokens if usage else 5
        self.prompt_tok     += pt
        self.completion_tok += ct
        self.max_ctx         = max(self.max_ctx, pt)


# ── Single LLM call ───────────────────────────────────────────────────────────
def llm(prompt: str, m: Metrics) -> str:
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    m.record(resp.usage, len(prompt))
    text = resp.choices[0].message.content or ""
    # qwen3 wraps chain-of-thought in <think>...</think> — strip before parsing
    if "</think>" in text:
        text = text.split("</think>")[-1]
    return text.strip()


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1 — Plain Agent
#
# All 30 transcripts → one giant prompt (~9k tokens).
# Model must hold every transcript in attention at once.
# At this scale it already miscounts. At 3,000 transcripts it would fail.
# ─────────────────────────────────────────────────────────────────────────────
def plain_agent(transcripts: list[str]) -> tuple[Counter, Metrics]:
    m         = Metrics()
    comp_list = ", ".join(COMPETITORS)
    all_text  = "\n\n".join(transcripts)

    prompt = (
        f"Read ALL the sales call transcripts below and count how many times "
        f"each competitor is mentioned across ALL of them.\n"
        f"Competitors: {comp_list}\n"
        f"Reply ONLY with valid JSON: "
        f'{{"Salesforce": 3, "HubSpot": 1, "Pipedrive": 0, "Zoho": 2, "Freshsales": 1}}\n\n'
        f"Transcripts:\n{all_text}"
    )

    t0        = time.perf_counter()
    result    = llm(prompt, m)
    m.elapsed = time.perf_counter() - t0

    # Parse JSON; fall back to regex extraction if model adds commentary
    try:
        data = json.loads(result)
        return Counter({k: int(v) for k, v in data.items()}), m
    except Exception:
        match = re.search(r'\{[^{}]+\}', result)
        if match:
            try:
                data = json.loads(match.group())
                return Counter({k: int(v) for k, v in data.items()}), m
            except Exception:
                pass
    print(f"  [PLAIN] parse failed → {result[:150]}")
    return Counter(), m


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2 — RLM Agent
#
# One transcript per sub-call → each call sees ~300 tokens (trivially easy).
# Results stored in `total: Counter` — a Python variable, not model memory.
# This is the MAP → REDUCE pattern applied to LLM calls.
# ─────────────────────────────────────────────────────────────────────────────
def sub_agent(transcript: str, tid: int, m: Metrics) -> Counter:
    """Process ONE transcript. Return competitor mentions found."""
    comp_list = ", ".join(COMPETITORS)

    prompt = (
        f"Which of these competitors are mentioned in the transcript below?\n"
        f"Competitors: {comp_list}\n"
        f"List ONLY the ones mentioned, one per line. If none, write NONE.\n\n"
        f"Transcript:\n{transcript}"
    )

    result = llm(prompt, m)

    # Parse response: any line containing a competitor name counts
    found: Counter = Counter()
    for line in result.splitlines():
        for comp in COMPETITORS:
            if comp.lower() in line.lower():
                found[comp] += 1
    return found


def rlm_agent(transcripts: list[str]) -> tuple[Counter, Metrics]:
    """
    MAP:    each transcript → isolated sub-call (fresh context, ~300 tokens)
    REDUCE: update Python Counter — no LLM memory involved
    """
    m             = Metrics()
    total: Counter = Counter()

    print(f"\n  [RLM] {len(transcripts)} transcripts → {len(transcripts)} sub-calls")

    t0 = time.perf_counter()
    for i, transcript in enumerate(transcripts):
        # KEY: each call is completely isolated — zero memory of other transcripts
        found = sub_agent(transcript, i, m)
        total.update(found)          # state lives here, in Python
        if found:
            print(f"  [RLM] transcript-{i:03d}: found {dict(found)}")

    m.elapsed = time.perf_counter() - t0
    return total, m


# ── Results table ─────────────────────────────────────────────────────────────
def show_results(plain: Counter, pm: Metrics, rlm: Counter, rm: Metrics):
    print("\n" + "═" * 64)
    print(f"  {'COMPETITOR':<14} {'TRUE':>6}  {'PLAIN':>6}  {'RLM':>6}  "
          f"{'PLAIN ERR':>10}  {'RLM ERR':>8}")
    print("═" * 64)

    plain_err = rlm_err = 0
    for comp in COMPETITORS:
        true  = TRUE_COUNTS[comp]
        p     = plain.get(comp, 0)
        r     = rlm.get(comp, 0)
        pe    = abs(p - true)
        re_   = abs(r - true)
        plain_err += pe
        rlm_err   += re_
        diff = " ←" if pe != re_ else ""
        print(f"  {comp:<14} {true:>6}  {p:>6}  {r:>6}  "
              f"{'off '+str(pe) if pe else '✓':>10}  "
              f"{'off '+str(re_) if re_ else '✓':>8}{diff}")

    print("─" * 64)
    print(f"  {'TOTAL ERROR':<14} {'':>6}  {'':>6}  {'':>6}  "
          f"{plain_err:>10}  {rlm_err:>8}")
    print("═" * 64)

    print(f"\n  {'METRIC':<22} {'PLAIN':>10}   {'RLM':>10}")
    print("  " + "─" * 46)
    for label, v1, v2 in [
        ("LLM calls",      pm.calls,      rm.calls),
        ("Prompt tokens",  pm.prompt_tok, rm.prompt_tok),
        ("Total tokens",   pm.total_tok,  rm.total_tok),
        ("Max ctx/call",   pm.max_ctx,    rm.max_ctx),
        ("Time (sec)",     f"{pm.elapsed:.1f}s", f"{rm.elapsed:.1f}s"),
    ]:
        print(f"  {label:<22} {str(v1):>10}   {str(v2):>10}")

    ratio = pm.max_ctx // max(rm.max_ctx, 1)
    print(f"\n  Plain's largest call = {pm.max_ctx} tokens")
    print(f"  RLM's largest call   = {rm.max_ctx} tokens  ({ratio}x smaller)")
    print(f"  At 3,000 transcripts: plain needs ~{pm.max_ctx*100//1000}k tokens → fails")
    print(f"  RLM: still ~{rm.max_ctx} tokens/call, just 3,000 calls → still works")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Model      : {MODEL}  (local — no API key)")
    print(f"Transcripts: {len(TRANSCRIPTS)}")
    print(f"True counts: {dict(TRUE_COUNTS)}")
    print("─" * 64)

    print("\n[1/2] Plain agent — all transcripts in one call...")
    plain_counts, pm = plain_agent(TRANSCRIPTS)
    print(f"      Result: {dict(plain_counts)}")

    print("\n[2/2] RLM agent — one transcript per sub-call...")
    rlm_counts, rm = rlm_agent(TRANSCRIPTS)
    print(f"\n      Result: {dict(rlm_counts)}")

    show_results(plain_counts, pm, rlm_counts, rm)
