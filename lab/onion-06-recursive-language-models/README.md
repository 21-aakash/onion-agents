# Recursive Language Models (RLMs) — Hands-On Demo

> **Plain English**: Instead of one AI trying to remember everything, write a loop that sends small chunks to fresh AI calls, and keep the running total in a Python variable.

---

## The Problem: Context Rot

Every LLM has a context window. The real issue isn't hitting the hard limit — it's that **quality degrades well before you get there**.

Ask an AI to count competitor mentions across 10,000 sales call transcripts:

```
Turn 1: read transcript 1…   (context: 500 tokens)
Turn 2: read transcript 2…   (context: 1,000 tokens)
…
Turn 500: read transcript 500…  (context: 250,000 tokens — model losing track)
Turn 2000: "I can't process all of this."
```

The model tries to hold a running count in its own head. By transcript 500, it's drifting. By transcript 2,000, it gives up.

This is **context rot** — the gradual degradation of quality as the context window fills.

---

## The Solution: Code as Memory

The RLM insight is simple:

> **Don't ask the model to remember. Ask it to write a loop.**

```
Orchestrator LLM
│  writes: for transcript in transcripts:
│              result = ask_llm(transcript)    ← fresh context, 300 tokens
│              total.update(result)            ← state in Python, not model memory
│
├──► Sub-LLM call 1  →  "Salesforce mentioned once"
├──► Sub-LLM call 2  →  "HubSpot mentioned twice"
├──► Sub-LLM call 3  →  "nothing found"
└──► Sub-LLM call N  →  "Zoho mentioned once"

total = Counter()  ← never forgets, never drifts
```

Each sub-call sees ONE transcript (~300 tokens). The aggregation lives in `Counter` — a Python variable. Python variables don't have context rot.

---

## Architecture

```
┌────────────────────────────────────────────────┐
│              YOUR PYTHON CODE                  │
│                                                │
│  chunks = split(data)   # deterministic        │
│  for chunk in chunks:                          │
│      result = sub_llm(chunk)  ──────────────┐  │
│      total.update(result)     # in code     │  │
└────────────────────────────────────────────────┘
                                             │
         Each sub_llm call is isolated:      │
         ┌───────────────────────────────────▼──┐
         │  [Fresh LLM]  context = 300 tokens   │
         │  Input: one transcript only          │
         │  Output: structured result           │
         └───────────────────────────────────────┘
```

---

## How It Differs From Other Patterns

| Pattern | Code does | State lives in | Scales to |
|---|---|---|---|
| **Plain Agent** | Acts on system (files, shell) | Model's context window | ~200k tokens |
| **Orchestrator + Subagents** | Delegates to full agents with tools | Each subagent's context | Large parallel tasks |
| **RLM** | Dispatches bare LLM calls | **Python variables** | Unlimited |

RLM workers are **stateless, cheap, and interchangeable**. Subagents are stateful and specialized. You'd use RLM for 10,000 tickets, subagents for a research pipeline.

---

## Benchmark (this repo)

30 sales call transcripts. True competitor mention counts known. Two approaches:

```
                    PLAIN agent     RLM agent
─────────────────────────────────────────────
Salesforce          off by 2        ✓
HubSpot             off by 2        ✓
Pipedrive           off by 5        ✓
Zoho                off by 3        ✓
Freshsales          off by 4        ✓

Total error             16          0

Max context/call       9,200      310 tokens
```

Plain agent sends **9,200 tokens in one shot** → model loses track.
RLM sends **310 tokens per call** → trivially easy, every call gets it right.

---

## Three Implementations

### 1. Local — `01_rlm_local.py`
Uses **qwen3:4b via Ollama** — no API key, runs fully offline.
Best for: understanding the pattern, experimenting, no network.

```bash
ollama serve   # must be running
python 01_rlm_local.py
```

### 2. LangChain — `02_rlm_langchain.py`
Uses **LangChain LCEL chains** with any OpenAI-compatible endpoint.
Best for: production apps, structured pipelines, LangChain ecosystem.

```bash
cp .env.example .env  # fill in OPENAI_API_KEY
python 02_rlm_langchain.py
```

### 3. `rlms` Library — `03_rlm_lib.py`
Uses the **original MIT CSAIL implementation** (`pip install rlms`).
The model writes the orchestration code itself — you just give it the task.
Best for: understanding the paper's exact approach, research.

```bash
pip install rlms
python 03_rlm_lib.py
```

> **Note on corporate proxy**: The `rlms` library uses `openai-2.x` which uses `httpx`. If you're behind a corporate SSL proxy, see the SSL patch in `03_rlm_lib.py`.

---

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy and fill env vars
cp .env.example .env

# 3. Make sure Ollama is running (for local script)
ollama serve

# 4. Run any script
python 01_rlm_local.py   # no API key needed
python 02_rlm_langchain.py
python 03_rlm_lib.py
```

---

## Key Concepts Glossary

| Term | What it means |
|---|---|
| **Context rot** | Quality degradation as LLM context window fills up |
| **Orchestrator** | The LLM that writes/controls the loop |
| **Sub-call / Sub-LLM** | A fresh isolated LLM call for one chunk |
| **MAP** | Split data → one sub-call per piece |
| **REDUCE** | Aggregate results in Python code, not model memory |
| **max_ctx/call** | The largest single prompt sent — key metric for scalability |

---

## When to Use RLMs

**Use RLMs when:**
- Dataset is larger than fits in context (>50k tokens)
- Task can be split into independent chunks (per-item analysis)
- You need guaranteed coverage (a `for` loop won't skip items; a model might)
- Cost matters: cheap model for sub-tasks, expensive model only for synthesis

**Don't use RLMs when:**
- Task requires holistic reasoning across ALL data simultaneously
- Dataset is small and fits comfortably in context
- You need sub-agents with tools and state (use orchestrator + subagents instead)

---

## Further Reading

- [RLM Paper (MIT CSAIL)](https://arxiv.org/abs/2512.24601)
- [Alex Zhang's original blog](https://alexzhang13.github.io/blog/2025/rlm/)
- [LangChain: How to Use RLMs in Deep Agents](https://www.langchain.com/blog/how-to-use-rlms-in-deep-agents)
- [alexzhang13/rlm on GitHub](https://github.com/alexzhang13/rlm)
