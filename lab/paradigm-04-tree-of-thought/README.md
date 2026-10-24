# Paradigm 4: Tree-of-Thought (ToT) & Deliberative Graph Search 🧠🌳

> **Research Anchor**: *“Tree of Thoughts: Deliberate Problem Solving with Large Language Models”* (Yao et al., Princeton / Google DeepMind).

---

## 🎯 Architecture Overview
While autoregressive LLMs sample sequentially (left-to-right token generation), complex strategic reasoning (algorithmic optimization, creative writing, game playing, symbolic planning) requires:
1. **Thought Generation**: Expanding multiple candidate reasoning paths per step.
2. **State Evaluation**: Scoring intermediate thoughts via heuristic / value prompts.
3. **Graph Search**: Breadth-First Search (BFS) or Depth-First Search (DFS) with lookahead and backtracking when a thought path leads to a dead end.

```
                  [Root Problem State]
                     /      |      \
              Thought 1  Thought 2  Thought 3
               (V=0.8)    (V=0.3)    (V=0.1)
                /   \        x          x
             T 1.1  T 1.2  (Pruned)   (Pruned)
            (V=0.9) (V=0.2)
               |
         [Solved Goal]
```

---

## 🔬 Mathematical Core
Let $\mathcal{S}$ be the state space of partial thoughts, and $p_\theta$ be the language model.
- **Thought Generator**: $G(p_\theta, s, k) = \{s' \mid s' \sim p_\theta(\cdot \mid s)\}$ produces $k$ candidates.
- **Value Evaluator**: $V(p_\theta, S) = \text{softmax}(\text{ratings}) \in [0, 1]$ grades promise.
- **Search Frontier**: Explores states $\arg\max_{s} V(s)$ using priority queues with backtracking.

---

## 🚀 Status
* **Scaffolded in The Lab**: Implementation roadmap active.
* **Target Benchmark**: Multi-constraint budget allocation & combinatorial planning.
