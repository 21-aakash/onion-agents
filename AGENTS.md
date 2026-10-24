# 🧅 Onion Agents — Monorepo Architecture Directory

This repository organizes specialized autonomous AI agent architectures into two distinct pillars:
* **🔬 The Lab**: Algorithmic & mathematical paper implementations with interactive visual testbenches. Peeling the onion layer by layer.
* **🚀 The Fleet**: Flagship production multi-agent systems.

---

## 🏛️ System Architecture Graph

```mermaid
graph TD
    subgraph Monorepo["onion-agents"]
        subgraph TheLab["🔬 The Lab (Onion Architecture Layers)"]
            P1["<b>Onion 01: Refundbot</b><br/><i>(Deterministic Policy & Tool Guardrail)</i>"]
            P2["<b>Onion 02: Agent Memory</b><br/><i>(Meta AI Episodic Memory Sidecar)</i>"]
            P3["<b>Onion 03: Reflection & Eval</b><br/><i>(Reflexion: 3-Tier Evaluator & Verbal Reinforcement)</i>"]
            P4["<b>Onion 04: Tree-of-Thought</b><br/><i>(Princeton/DeepMind: Deliberate Graph Search)</i>"]
            P5["<b>Onion 05: DSPy Studio</b><br/><i>(Stanford DSPy: Auto-Compilation & Joint Cascade Healing)</i>"]
            P6["<b>Onion 06: Recursive LMs</b><br/><i>(Code as Memory: Mitigation of Context Rot)</i>"]
            P7["<b>Onion 07: Agentify MCP</b><br/><i>(OpenAPI to FastMCP & TypeScript Tool Generator)</i>"]
        end
        subgraph TheFleet["🚀 The Fleet (Flagship Production Systems)"]
            F1["<b>Flagship: Research Assistant</b><br/><i>(LangGraph DAG, Voice Todo Hub & Qdrant Vector DB)</i>"]
        end
        subgraph Insights["📚 Insights & Artifacts"]
            I1["<b>Papers Catalog</b>"]
            I2["<b>Engineering Blogs</b>"]
            I3["<b>Eval Benchmarks</b>"]
        end
    end
    TheLab -->|Graduated Architectures| TheFleet
```

---

## 🗂️ Onion Layer Roster

| Layer | System Name | Directory | Core Architectural Paradigm | Tech Stack | Status |
|---|---|---|---|---|---|
| **Onion 01** | **Refundbot** | [`lab/onion-01-refundbot`](./lab/onion-01-refundbot) | Deterministic Guardrails & Immutable Tool Contracts | Python, FastAPI, SQLite | Production Ready |
| **Onion 02** | **Agent Memory** | [`lab/onion-02-agent-memory`](./lab/onion-02-agent-memory) | Meta AI Episodic Memory Companion | Python, Event-Driven Sidecar | Active Lab |
| **Onion 03** | **Reflection Eval** | [`lab/onion-03-reflection-eval`](./lab/onion-03-reflection-eval) | 3-Tier Reflexion Evaluator Loop (Code ➔ LLM Judge ➔ Human) | Python, Scikit-learn, Evaluators | Production Ready |
| **Onion 04** | **Tree of Thought** | [`lab/onion-04-tree-of-thought`](./lab/onion-04-tree-of-thought) | Deliberate Problem Solving via Heuristic BFS/DFS Search | Python, Graph Search Engine | In Development |
| **Onion 05** | **DSPy Studio** | [`lab/onion-05-dspy-self-tuning`](./lab/onion-05-dspy-self-tuning) | Stanford DSPy Compilers (`BootstrapFewShot`) & Multi-Agent Joint Optimization | DSPy 3.4.1, Groq, FastAPI | Production Ready |
| **Onion 06** | **Recursive LMs** | [`lab/onion-06-recursive-language-models`](./lab/onion-06-recursive-language-models) | Solving Context Rot using Python Loops & Deterministic State Aggregators | Python, LangChain, Anthropic/Groq | Production Ready |
| **Onion 07** | **Agentify MCP** | [`lab/onion-07-agentify-mcp-builder`](./lab/onion-07-agentify-mcp-builder) | Dynamic MCP Protocol Generation from OpenAPI Specs | TypeScript, Node.js, FastMCP, Zod | Production Ready |
| **Fleet 01** | **Research Assistant** | [`fleet/b-research-agent`](./fleet/b-research-agent) | Multi-Agent Autonomous Research Engine + Voice Todo Hub | LangGraph, FastAPI, Qdrant, React 18 | Production Ready |

---

## 📐 Engineering Standards
1. **Isolated Environments**: Standalone dependency definitions (`pyproject.toml`, `requirements.txt`, `package.json`) allowing independent deployment.
2. **Deterministic Evaluation**: Every paradigm includes gold evaluation test sets and measurable metrics.
3. **Interactive Sandboxes**: Visual testbenches allowing live inspection of model behavior.
