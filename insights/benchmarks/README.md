# 📊 Benchmark Suites & Eval Datasets

Quantitative benchmarks and gold evaluation datasets used across The Lab paradigms to measure agent robustness against noise and model drift.

---

## 🔬 Benchmark Catalog

| Benchmark Suite | Target Paradigm | Metrics Measured | Dataset Path |
| :--- | :--- | :--- | :--- |
| **Model Drift & Schema Rigidity** | Paradigm 05 (DSPy) | Strict JSON compliance, policy accuracy, token consumption | [dataset.py](file:///c:/Desktop/new-workspace/my-cute-agents/lab/paradigm-05-dspy-self-tuning/agent/dataset.py) |
| **Domino Cascade Resilience** | Paradigm 05 (Multi-Agent) | End-to-end task completion rate across 3 chained agents | [multi_agent_pipeline.py](file:///c:/Desktop/new-workspace/my-cute-agents/lab/paradigm-05-dspy-self-tuning/agent/multi_agent_pipeline.py) |
| **Episodic Recall vs. BM25** | Paradigm 02 (Memory) | Contextual hit rate, trigger accuracy, token efficiency | [run_comparison.py](file:///c:/Desktop/new-workspace/my-cute-agents/lab/paradigm-02-agent-memory/run_comparison.py) |
| **Financial Security Stress Test** | Paradigm 01 (RefundBot) | Injection immunity, authorization check, refund ceiling enforcement | [tests/stress_test.py](file:///c:/Desktop/new-workspace/my-cute-agents/lab/paradigm-01-refundbot/tests/stress_test.py) |
