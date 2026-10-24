"""
03_rlm_lib.py — RLM using the alexzhang13/rlms library
=======================================================
This uses the ORIGINAL MIT CSAIL implementation of RLMs.
Paper: https://arxiv.org/abs/2512.24601

Key difference from 01 and 02:
  YOU don't write the sub-agent loop. The MODEL does.
  You just call rlm.completion("your task") and the LLM
  writes its own Python orchestration code internally.

Install:
    pip install rlms

Corporate SSL proxy fix:
    The rlms library uses openai-2.x which uses httpx.
    If you're behind a corporate proxy, the SSL patch in
    this file (patching ssl.create_default_context) is
    required. httpx uses httpcore which calls that function
    directly — patching ssl._create_default_https_context
    is NOT sufficient.

Run:
    cd /path/to/this/folder   # IMPORTANT: not from workspace root
    python 03_rlm_lib.py

    The script MUST run from this folder, not from a parent
    directory that contains an openai.py file (that file
    would shadow the openai package).
"""

# ── SSL patch — must come BEFORE any openai/rlm imports ──────────────────────
# Reason: httpcore calls ssl.create_default_context() internally when
# establishing TLS connections. Patching this function globally is the
# only reliable way to bypass corporate proxy SSL interception for httpx.
import ssl
_orig_create_default_context = ssl.create_default_context

def _no_verify_ssl_context(*args, **kwargs):
    ctx = _orig_create_default_context(*args, **kwargs)
    ctx.check_hostname = False
    ctx.verify_mode    = ssl.CERT_NONE
    return ctx

ssl.create_default_context = _no_verify_ssl_context
# ─────────────────────────────────────────────────────────────────────────────

import os
import warnings
warnings.filterwarnings("ignore")

from dotenv import load_dotenv
from rlm import RLM

load_dotenv()

api_key    = os.environ.get("OPENAI_API_KEY")
model_name = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")

# ── Create the RLM ────────────────────────────────────────────────────────────
# verbose=True shows each iteration: what code the model writes and executes.
# max_depth=1 means the model can make sub-calls but those sub-calls can't
# recursively make further sub-calls (depth 0 = orchestrator only).
rlm = RLM(
    backend="openai",
    backend_kwargs={
        "api_key":    api_key,
        "model_name": model_name,
        "base_url":   os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    },
    verbose=True,     # print each iteration's code + output
    max_depth=1,      # allow one level of recursive sub-calls
    max_iterations=20,
)

# ── Task ──────────────────────────────────────────────────────────────────────
# We give the model raw data and a task description.
# The model will:
#   1. Analyse the data size and task
#   2. Write Python code (a loop with llm_query sub-calls)
#   3. Execute that code in its REPL
#   4. Return the aggregated answer
#
# We don't write sub_agent() or for-loops. The model does.
TASK = """
You have 10 sales call notes below. Count how many times each competitor
is mentioned across ALL notes. Use programmatic sub-calls to process
notes one by one so you don't miss any.

Competitors to track: Salesforce, HubSpot, Pipedrive, Zoho, Freshsales

Sales call notes:
---
[Call 001] Customer is evaluating Salesforce as an alternative. They liked our pricing better.
[Call 002] No competitor mentioned. Customer focused on our onboarding timeline.
[Call 003] The prospect showed us a HubSpot demo. They said HubSpot's UI is cleaner.
[Call 004] Customer currently on Zoho, unhappy with support response times.
[Call 005] Competitor came up: Pipedrive. They said Pipedrive lacked reporting features.
[Call 006] No mentions. Deal progressing, proposal sent.
[Call 007] Salesforce was brought up twice — once on pricing, once on integrations.
[Call 008] HubSpot mentioned. Customer said they got a better onboarding offer from HubSpot.
[Call 009] No competitor. Technical deep-dive on our API.
[Call 010] Freshsales mentioned in passing. Customer wasn't impressed with their mobile app.
---

Return a JSON object with exact counts:
{"Salesforce": N, "HubSpot": N, "Pipedrive": N, "Zoho": N, "Freshsales": N}
"""

# Known true counts for verification
TRUE = {
    "Salesforce": 3,   # calls 001, 007 (×2)
    "HubSpot":    3,   # calls 003 (×2), 008
    "Pipedrive":  1,   # call 005
    "Zoho":       1,   # call 004
    "Freshsales": 1,   # call 010
}

# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    print(f"Model    : {model_name}")
    print(f"Endpoint : {base_url}")
    print(f"True     : {TRUE}")
    print("=" * 60)
    print("The model will now write its own orchestration loop...\n")

    result = rlm.completion(TASK)

    print("\n" + "=" * 60)
    print("Final answer from the RLM:")
    print(result.response)
    print(f"\nTrue counts for verification: {TRUE}")

    # Show metadata if available
    if hasattr(result, 'metadata') and result.metadata:
        meta = result.metadata
        print(f"\nIterations: {getattr(meta, 'num_iterations', 'N/A')}")
