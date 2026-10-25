# 📊 Benchmark Suites & Eval Datasets

Quantitative benchmarks and gold evaluation datasets used across The Lab layers to measure agent robustness against noise and model drift.

---

## 🔬 Benchmark Catalog

| Benchmark Suite | Target Layer | Metrics Measured | Dataset Path |
| :--- | :--- | :--- | :--- |
| **Model Drift & Schema Rigidity** | Onion 05 (DSPy) | Strict JSON compliance, policy accuracy, token consumption | [dataset.py](file:///c:/Desktop/new-workspace/my-cute-agents/lab/onion-05-dspy-self-tuning/agent/dataset.py) |
| **Domino Cascade Resilience** | Onion 05 (Multi-Agent) | End-to-end task completion rate across 3 chained agents | [multi_agent_pipeline.py](file:///c:/Desktop/new-workspace/my-cute-agents/lab/onion-05-dspy-self-tuning/agent/multi_agent_pipeline.py) |
| **Context Rot Mitigation** | Onion 06 (RLMs) | Chunked loop processing vs single-context degradation | [01_rlm_local.py](file:///c:/Desktop/new-workspace/my-cute-agents/lab/onion-06-recursive-language-models/01_rlm_local.py) |
| **Episodic Recall vs. BM25** | Onion 02 (Memory) | Contextual hit rate, trigger accuracy, token efficiency | [run_comparison.py](file:///c:/Desktop/new-workspace/my-cute-agents/lab/onion-02-agent-memory/run_comparison.py) |
| **Financial Security Stress Test** | Onion 01 (RefundBot) | Injection immunity, authorization check, refund ceiling enforcement | [tests/stress_test.py](file:///c:/Desktop/new-workspace/my-cute-agents/lab/onion-01-refundbot/tests/stress_test.py) |
