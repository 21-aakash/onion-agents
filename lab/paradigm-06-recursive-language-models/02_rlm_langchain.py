"""
02_rlm_langchain.py — RLM Pattern using LangChain LCEL
=======================================================
Same use case as 01_rlm_local.py but using LangChain's
prompt templates, output parsers, and LCEL chains.

Why LangChain?
  - Structured output parsing built in (no manual JSON regex)
  - Prompt templates are versioned, reusable, testable
  - Easy to swap models, add memory, or wire into larger pipelines
  - LCEL (pipe operator) makes data flow explicit and readable

Run:
    cp .env.example .env   # fill in OPENAI_API_KEY
    pip install langchain langchain-openai
    python 02_rlm_langchain.py
"""

import os
import random
import time
from collections import Counter
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# ── LangChain model setup ─────────────────────────────────────────────────────
# Using ChatOpenAI pointed at an OpenAI-compatible endpoint.
# Set OPENAI_BASE_URL in .env to point to any provider.
llm = ChatOpenAI(
    model=os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"),
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    temperature=0,
)

COMPETITORS = ["Salesforce", "HubSpot", "Pipedrive", "Zoho", "Freshsales"]

# ── Synthetic data (same seed as 01_rlm_local.py for reproducibility) ────────
random.seed(42)

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
    lines    = random.sample(FILLER, k=random.randint(4, 6))
    mentions: Counter = Counter()
    for _ in range(random.randint(0, 2)):
        comp     = random.choice(COMPETITORS)
        sentence = random.choice(COMP_SENTENCES).format(comp=comp)
        lines.insert(random.randint(0, len(lines)), sentence)
        mentions[comp] += 1
    return f"[Transcript {idx:03d}]\n" + " ".join(lines), mentions


TRANSCRIPTS: list[str] = []
TRUE_COUNTS: Counter   = Counter()
for i in range(40):
    text, mentions = make_transcript(i)
    TRANSCRIPTS.append(text)
    TRUE_COUNTS.update(mentions)


# ── Metrics ───────────────────────────────────────────────────────────────────
@dataclass
class Metrics:
    calls:   int   = 0
    elapsed: float = 0.0
    max_ctx: int   = 0    # estimated from prompt character length


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1 — Plain agent (LangChain LCEL chain)
#
# Chain: prompt_template | llm | json_parser
# One call, all transcripts in context.
# ─────────────────────────────────────────────────────────────────────────────

# Prompt template makes the instruction reusable and testable
plain_prompt = ChatPromptTemplate.from_template("""
Read ALL the sales call transcripts below and count how many times
each competitor is mentioned across ALL of them.

Competitors to track: {comp_list}

Reply ONLY with valid JSON (no commentary):
{{"Salesforce": 3, "HubSpot": 1, "Pipedrive": 0, "Zoho": 2, "Freshsales": 1}}

Transcripts:
{all_transcripts}
""")

# LCEL chain: prompt → LLM → JSON parser (structured output, no manual parsing)
plain_chain = plain_prompt | llm | JsonOutputParser()


def plain_agent(transcripts: list[str]) -> tuple[Counter, Metrics]:
    m          = Metrics()
    all_text   = "\n\n".join(transcripts)
    comp_list  = ", ".join(COMPETITORS)

    t0 = time.perf_counter()
    result = plain_chain.invoke({
        "comp_list":       comp_list,
        "all_transcripts": all_text,
    })
    m.elapsed = time.perf_counter() - t0
    m.calls   = 1
    m.max_ctx = len(all_text) // 4    # rough token estimate

    return Counter({k: int(v) for k, v in result.items()}), m


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2 — RLM agent (LangChain LCEL chain per transcript)
#
# Each sub-call is its own chain invocation.
# The chain is: sub_prompt | llm | str_parser
# Results aggregated in Python Counter — NOT in any LLM's memory.
# ─────────────────────────────────────────────────────────────────────────────

sub_prompt = ChatPromptTemplate.from_template("""
Which of these competitors are mentioned in the transcript below?
Competitors: {comp_list}

List ONLY the ones mentioned, one per line. If none, write NONE.

Transcript:
{transcript}
""")

# This chain returns raw string — we parse competitor names ourselves
sub_chain = sub_prompt | llm | StrOutputParser()


def sub_agent(transcript: str, tid: int, m: Metrics) -> Counter:
    """One isolated chain invocation. Only sees this transcript."""
    comp_list = ", ".join(COMPETITORS)

    result = sub_chain.invoke({
        "comp_list":  comp_list,
        "transcript": transcript,
    })

    m.calls   += 1
    m.max_ctx  = max(m.max_ctx, len(transcript) // 4)

    # Parse lines for competitor names
    found: Counter = Counter()
    for line in result.splitlines():
        for comp in COMPETITORS:
            if comp.lower() in line.lower():
                found[comp] += 1
    return found


def rlm_agent(transcripts: list[str]) -> tuple[Counter, Metrics]:
    """
    MAP:    each transcript → sub_chain invocation (isolated context)
    REDUCE: update Counter in Python — not in any model's context window
    """
    m             = Metrics()
    total: Counter = Counter()

    print(f"\n  [RLM] {len(transcripts)} transcripts → {len(transcripts)} chain calls")

    t0 = time.perf_counter()
    for i, transcript in enumerate(transcripts):
        # Each invocation: fresh chain, no shared state with previous calls
        found = sub_agent(transcript, i, m)
        total.update(found)
        if found:
            print(f"  [RLM] transcript-{i:03d}: {dict(found)}")

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
        ("LLM calls",     pm.calls,      rm.calls),
        ("Est. max ctx",  pm.max_ctx,    rm.max_ctx),
        ("Time (sec)",    f"{pm.elapsed:.1f}s", f"{rm.elapsed:.1f}s"),
    ]:
        print(f"  {label:<22} {str(v1):>10}   {str(v2):>10}")

    print(f"\n  LangChain note:")
    print(f"  Each approach uses the same chain type (prompt | llm | parser)")
    print(f"  The only difference: plain passes ALL text, RLM passes ONE transcript")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    model_name = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")
    print(f"Model      : {model_name}  (via LangChain)")
    print(f"Transcripts: {len(TRANSCRIPTS)}")
    print(f"True counts: {dict(TRUE_COUNTS)}")
    print("─" * 64)

    print("\n[1/2] Plain agent — one chain call, all transcripts...")
    plain_counts, pm = plain_agent(TRANSCRIPTS)
    print(f"      Result: {dict(plain_counts)}")

    print("\n[2/2] RLM agent — one chain call per transcript...")
    rlm_counts, rm = rlm_agent(TRANSCRIPTS)
    print(f"\n      Result: {dict(rlm_counts)}")

    show_results(plain_counts, pm, rlm_counts, rm)
