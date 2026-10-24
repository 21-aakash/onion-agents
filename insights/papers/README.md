# 📑 Research Papers & Theoretical Foundations

This directory catalogs the research papers that power the architectures in **Onion Agents**.

---

## 📚 Paper Index

| Paper | Author / Institution | Focus Area | Lab Paradigm |
| :--- | :--- | :--- | :--- |
| **DSPy: Compiling Declarative Language Model Calls** | Khattab et al. (Stanford University) | Auto-optimizing prompt compilers & teleprompters | [Paradigm 05: DSPy Self-Tuning](file:///c:/Desktop/new-workspace/my-cute-agents/lab/paradigm-05-dspy-self-tuning/README.md) |
| **Recursive Language Models & Context Rot Mitigation** | MIT / Deep Research Consortium | "Code as Memory" state aggregation vs. quadratic token degradation | [Paradigm 06: Recursive Language Models](file:///c:/Desktop/new-workspace/my-cute-agents/lab/paradigm-06-recursive-language-models/README.md) |
| **Proactive Memory Agent Companion** | Meta AI Research | Episodic vs. semantic memory retrieval & proactive assistance | [Paradigm 02: Agent Memory](file:///c:/Desktop/new-workspace/my-cute-agents/lab/paradigm-02-agent-memory/readme.md) |
| **Reflexion: Language Agents with Verbal Reinforcement** | Shinn et al. (Northeastern / MIT) | Dynamic memory & self-evaluative critique loops | [Paradigm 03: Reflection Eval](file:///c:/Desktop/new-workspace/my-cute-agents/lab/paradigm-03-reflection-eval/readme.md) |
| **Tree of Thoughts: Deliberate Problem Solving** | Yao et al. (Princeton / Google DeepMind) | Heuristic state evaluation & BFS/DFS tree search | [Paradigm 04: Tree of Thought](file:///c:/Desktop/new-workspace/my-cute-agents/lab/paradigm-04-tree-of-thought/README.md) |
| **Model Context Protocol (MCP) Specification** | Anthropic Architecture Group | Standardized client-host-server protocol for tool sandboxes | [Paradigm 07: Agentify MCP Builder](file:///c:/Desktop/new-workspace/my-cute-agents/lab/paradigm-07-agentify-mcp-builder/README.md) |

---

## 🔍 How We Read & Implement Papers
1. **Extract the Mathematical Contract**: Isolate state transitions, loss/utility metrics, and memory bounds.
2. **Build the Minimum Testable Unit**: Eliminate paper bloat; verify the core algorithmic primitive against a baseline.
3. **Build an Interactive Sandbox**: Give visitors a visual test-bench to observe the phenomenon live.
