# 🧅 onion-agents
### The Multi-Layered Autonomous AI Systems Monorepo

<p align="center">
  <img src="./assets/banner.jpg" alt="Family of Cute Onion AI Agents Mascot" width="100%" />
</p>

---

**onion-agents** is a curated, production-grade monorepo organizing autonomous agent architectures into two high-visibility pillars:
1. **🔬 The Lab**: Deep mathematical and paper implementations proving fundamental agent engineering layers with interactive visual sandboxes.
2. **🚀 The Fleet**: Battle-tested, full-scale production applications graduating findings from The Lab.
3. **📚 Insights & Artifacts**: Academic paper breakdowns, production post-mortems, and reproducible eval benchmarks.

---

## 🏛️ Monorepo Architecture

```
onion-agents/
├── 🔬 lab/ (Onion Layers & Paper Implementations) ─ Proof of Knowledge & Deep Math
│   ├── onion-01-refundbot/                        # Deterministic policies, tool-calling & financial guardrails
│   ├── onion-02-agent-memory/                     # Meta AI Paper: Episodic vs. semantic proactive memory companion
│   ├── onion-03-reflection-eval/                  # Reflexion: Self-critique, verbal reinforcement & 3-tier eval loops
│   ├── onion-04-tree-of-thought/                  # Princeton/DeepMind: Deliberate problem solving via BFS/DFS tree search
│   ├── onion-05-dspy-self-tuning/                 # Stanford DSPy: Auto-compiled teleprompters & multi-agent cascade healing
│   ├── onion-06-recursive-language-models/        # RLMs: Overcoming context rot via "Code as Memory" loop decomposition
│   └── onion-07-agentify-mcp-builder/             # Agentify: Zero-code OpenAPI to TypeScript / Python MCP tool generator
│
├── 🚀 fleet/ (Flagship Production Systems) ──────── Proof of Product Execution
│   └── b-research-agent/                          # Autonomous multi-agent research & knowledge engine with voice triage
│
├── 📚 insights/ (Knowledge Base & Evidences) ───── Proof of Rigor & Evals
│   ├── papers/                                    # Academic paper breakdowns & math summaries
│   └── benchmarks/                                # Quantitative eval suites, gold datasets & stress tests
│
└── 🎨 assets/                                     # Mascot branding & UI assets
```

---

## 🔬 The Lab: Onion Layers

| Layer | Directory | Core Research / Foundation | Primary Challenge Solved | Interactive Sandbox |
|---|---|---|---|---|
| **Onion 01** | **[onion-01-refundbot](./lab/onion-01-refundbot)** | Deterministic Guardrails & Strict Tool Schema | Eliminating prompt injection and enforcing immutable financial ceilings. | CLI & FastMCP Testbench |
| **Onion 02** | **[onion-02-agent-memory](./lab/onion-02-agent-memory)** | Meta AI Proactive Memory Companion | Long-horizon context retention without quadratic token bloat. | FastAPI + Web Memory Visualizer |
| **Onion 03** | **[onion-03-reflection-eval](./lab/onion-03-reflection-eval)** | Reflexion & Test-Driven Iteration | Preventing static error persistence via verbal reinforcement and judge loops. | Regression Test Harness |
| **Onion 04** | **[onion-04-tree-of-thought](./lab/onion-04-tree-of-thought)** | Princeton / DeepMind Tree-of-Thought (ToT) | Complex combinatorial planning via state heuristic scoring and backtracking. | Graph Search Harness |
| **Onion 05** | **[onion-05-dspy-self-tuning](./lab/onion-05-dspy-self-tuning)** | Stanford DSPy Compiler (`BootstrapFewShot`) | Healing model swap degradation (15x cost reduction) & eliminating multi-agent domino cascades. | Dual Studio (Vintage Beige & Navy Blue) |
| **Onion 06** | **[onion-06-recursive-language-models](./lab/onion-06-recursive-language-models)** | Recursive Language Models (RLMs) | Defeating context rot across 10,000+ items by using Python code execution as memory. | Multi-Script Hands-On Suite |
| **Onion 07** | **[onion-07-agentify-mcp-builder](./lab/onion-07-agentify-mcp-builder)** | Model Context Protocol (MCP) Generator | Generating instant, typed TypeScript & Python MCP servers directly from OpenAPI specs. | CLI Generator (`@skyaque/agentify`) |

---

## 🚀 The Fleet: Flagship Production Applications

### **[fleet/b-research-agent](./fleet/b-research-agent)**
An autonomous, multi-agent market and technical intelligence engine:
* **Directed Acyclic Graph (DAG)**: Orchestrates Planner ➔ Researcher ➔ Synthesizer ➔ Critic agents with state persistence.
* **Voice-to-Action Capture**: Integrated voice todo and notes triage hub for hands-free workflow capture.
* **Enterprise Infrastructure**: Dockerized microservices, PostgreSQL/Qdrant vector memory, and React 18 dashboard.

---

## 📚 Insights & Artifacts

* **[Research Papers Catalog](./insights/papers)**: Reading guides, mathematical abstractions, and algorithmic comparisons.
* **[Quantitative Benchmark Suites](./insights/benchmarks)**: Gold test sets for prompt drift, memory recall accuracy, and stress tests.

---

## 🚀 Independent Deployment Guide

Each module is decoupled and can be deployed individually from this monorepo:

### 1. Render / Railway / Fly.io / Vercel
Set the **Root Directory** in your project settings:
* **Refundbot API**: `lab/onion-01-refundbot`
* **Agent Memory Visualizer**: `lab/onion-02-agent-memory`
* **DSPy Studio Server**: `lab/onion-05-dspy-self-tuning`
* **Research Assistant API**: `fleet/b-research-agent`
* **Research Assistant UI**: `fleet/b-research-agent/ui`

### 2. Docker Containers
Build images directly targeting each sub-directory:
```bash
# Build Refundbot
docker build -t onion-agents/refundbot ./lab/onion-01-refundbot

# Build DSPy Self-Tuning Studio
docker build -t onion-agents/dspy-studio ./lab/onion-05-dspy-self-tuning

# Build Flagship Research Agent API
docker build -t onion-agents/research-agent ./fleet/b-research-agent
```

---

## 📄 License
MIT © 2026 Aakash & Onion Agents Contributors.
