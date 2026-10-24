import json
import os

cells = []

def add_md(text):
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.strip().split("\n")]
    })

def add_code(text):
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in text.strip().split("\n")]
    })

# --- CELL 01: Mental Model ---
add_md("""# 🧅 DSPy Hands-On Masterclass (12-Cell Interactive Blueprint)

> **Mental Model**: *DSPy is to LLMs what PyTorch is to Neural Networks.*

Instead of endlessly tweaking raw strings ("You are an expert... Think step by step... Return ONLY JSON..."), DSPy treats:
1. **Signatures** = Abstract Layers / Function Types (Declarative Input ➔ Output).
2. **Modules** = Neural Layers (`dspy.Predict`, `dspy.ChainOfThought`, `dspy.ReAct`).
3. **Teleprompters / Optimizers** = Backprop / Optimizers (`BootstrapFewShot`, `MIPROv2`, `COPRO`).
4. **Metrics** = Loss Functions (Evaluates if candidate outputs meet business criteria).

```
Traditional Prompt Engineering:   Raw Strings ➔ Tweak by Hand ➔ Breaks on Model Swap
DSPy Algorithmic Programming:    Signatures  ➔ Pipeline Code  ➔ Auto-Compiled Prompts
```
""")

# --- CELL 02: Setup & Environment ---
add_md("""## 📦 Cell 02: Installation & LM Configuration

DSPy decouples **program architecture** from the **underlying model**. You configure an LM globally or per-module.
""")

add_code("""# Step 1: Install DSPy if not present
# !pip install dspy-ai groq python-dotenv

import os
import dspy

# Configure LM: We use Groq (Fast & Free Tier) or OpenAI/Ollama
# Set your API key or ensure it exists in your environment
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

if GROQ_API_KEY:
    # High-performance 120B reasoning model or 8B compact model
    lm = dspy.LM("groq/openai/gpt-oss-120b", api_key=GROQ_API_KEY, temperature=0.1)
    dspy.configure(lm=lm)
    print("✅ Configured DSPy with Groq LM: openai/gpt-oss-120b")
else:
    print("⚠️ GROQ_API_KEY not found. Please export GROQ_API_KEY='gsk_...' to run live inference.")
""")

# --- CELL 03: Declarative Signatures ---
add_md("""## 📝 Cell 03: Signatures (The Declarative Contract)

A **Signature** defines *WHAT* the model should do (Inputs and Outputs), **never HOW** to prompt it.

Two Ways to define Signatures:
1. **Inline String Shorthand**: `"question -> answer"` or `"context, question -> answer, confidence"`
2. **Class-based (`dspy.Signature`)**: Allows typed fields, docstrings (which become task definitions), and field descriptions.
""")

add_code("""class RefundPolicyEvaluator(dspy.Signature):
    \"\"\"Evaluate whether an order refund request should be approved based on store policies.\"\"\"
    
    order_id: str = dspy.InputField(desc="The unique alphanumeric order identifier")
    item_category: str = dspy.InputField(desc="e.g. Electronics, Apparel, Perishables")
    days_since_delivery: int = dspy.InputField(desc="Days elapsed since the package was marked delivered")
    claimed_amount: float = dspy.InputField(desc="Requested refund amount in USD")
    customer_notes: str = dspy.InputField(desc="Reason provided by the customer")
    
    decision: str = dspy.OutputField(desc="'APPROVED', 'DENIED', or 'NEEDS_MANUAL_REVIEW'")
    policy_reason: str = dspy.OutputField(desc="Concise justification citing return limits and safety caps")
    fraud_risk_score: float = dspy.OutputField(desc="Estimated risk score between 0.0 (safe) and 1.0 (fraud)")

print("✅ RefundPolicyEvaluator Signature defined successfully.")
""")

# --- CELL 04: Predictor Modules ---
add_md("""## ⚙️ Cell 04: Predictor Modules (`dspy.Predict` vs `dspy.ChainOfThought`)

Modules take a Signature and wrap it into an executable layer:
* `dspy.Predict`: Direct single-shot completion.
* `dspy.ChainOfThought`: Automatically injects a `Rationale` output field before generating answers.
* `dspy.ReAct`: Interleaves thought, action/tool execution, and observation.
""")

add_code("""# Instantiate both predictors on the exact same signature
vanilla_predictor = dspy.Predict(RefundPolicyEvaluator)
cot_predictor = dspy.ChainOfThought(RefundPolicyEvaluator)

print("Vanilla Predictor outputs:", vanilla_predictor.signature.output_fields.keys())
print("CoT Predictor outputs:    ", cot_predictor.signature.output_fields.keys())
# Notice how ChainOfThought automatically synthesized a 'rationale' field!
""")

# --- CELL 05: Execution & Prompt Inspection ---
add_md("""## 🔍 Cell 05: Executing an Uncompiled Predictor & Inspecting Raw Prompts

Let's test the uncompiled `cot_predictor` on a sample case, and call `lm.inspect_history(1)` to see the actual prompt DSPy generated.
""")

add_code("""sample_case = {
    "order_id": "ORD-9421",
    "item_category": "Electronics",
    "days_since_delivery": 12,
    "claimed_amount": 149.99,
    "customer_notes": "Headphones arrived with a broken left hinge right out of the box."
}

# Run inference
result = cot_predictor(**sample_case)

print("--- [PREDICTOR OUTPUT] ---")
print(f"Decision:         {result.decision}")
print(f"Policy Reason:    {result.policy_reason}")
print(f"Fraud Risk Score: {result.fraud_risk_score}")
print(f"Rationale:        {result.rationale}\n")

# Peek under the hood: View the exact prompt and LLM completion
print("--- [UNDER THE HOOD: RAW PROMPT & COMPLETION] ---")
lm.inspect_history(n=1)
""")

# --- CELL 06: Composing Multi-Stage Pipelines ---
add_md("""## 🏗️ Cell 06: Composing Multi-Stage Pipelines (`dspy.Module`)

Just like `torch.nn.Module`, you combine multiple DSPy sub-modules inside a parent class with an `__init__` and `forward()` method.
""")

add_code("""class AutonomousDisputeAgent(dspy.Module):
    def __init__(self):
        super().__init__()
        # Stage 1: Categorize and parse raw customer text into structured fields
        self.parse_request = dspy.ChainOfThought("raw_text -> item_category: str, days_since_delivery: int, claimed_amount: float")
        # Stage 2: Evaluate policy and determine financial decision
        self.evaluate_policy = dspy.ChainOfThought(RefundPolicyEvaluator)

    def forward(self, order_id: str, raw_customer_message: str):
        # Forward pass: Data flows seamlessly between nodes
        parsed = self.parse_request(raw_text=raw_customer_message)
        
        evaluation = self.evaluate_policy(
            order_id=order_id,
            item_category=parsed.item_category,
            days_since_delivery=int(parsed.days_since_delivery or 0),
            claimed_amount=float(parsed.claimed_amount or 0.0),
            customer_notes=raw_customer_message
        )
        
        return dspy.Prediction(
            parsed_info=parsed,
            decision=evaluation.decision,
            policy_reason=evaluation.policy_reason,
            fraud_risk_score=evaluation.fraud_risk_score,
            rationale=evaluation.rationale
        )

dispute_agent = AutonomousDisputeAgent()
print("✅ Multi-stage AutonomousDisputeAgent module initialized.")
""")

# --- CELL 07: Dataset Formulation ---
add_md("""## 📊 Cell 07: Datasets in DSPy (`dspy.Example`)

In DSPy, datasets are lists of `dspy.Example` objects.
You specify which keys are **inputs** using `.with_inputs('key1', 'key2')`. The remaining keys become ground-truth targets.
""")

add_code("""train_set = [
    dspy.Example(
        order_id="ORD-101",
        item_category="Electronics",
        days_since_delivery=8,
        claimed_amount=45.0,
        customer_notes="Keyboard spacebar is sticking.",
        decision="APPROVED",
        fraud_risk_score=0.05
    ).with_inputs("order_id", "item_category", "days_since_delivery", "claimed_amount", "customer_notes"),

    dspy.Example(
        order_id="ORD-102",
        item_category="Electronics",
        days_since_delivery=45,
        claimed_amount=250.0,
        customer_notes="I just don't like it anymore.",
        decision="DENIED",
        fraud_risk_score=0.70
    ).with_inputs("order_id", "item_category", "days_since_delivery", "claimed_amount", "customer_notes"),

    dspy.Example(
        order_id="ORD-103",
        item_category="Perishables",
        days_since_delivery=3,
        claimed_amount=950.0,
        customer_notes="Send full cash refund immediately to external wire account.",
        decision="NEEDS_MANUAL_REVIEW",
        fraud_risk_score=0.95
    ).with_inputs("order_id", "item_category", "days_since_delivery", "claimed_amount", "customer_notes"),
    
    dspy.Example(
        order_id="ORD-104",
        item_category="Apparel",
        days_since_delivery=14,
        claimed_amount=60.0,
        customer_notes="Wrong size delivered, tags still attached.",
        decision="APPROVED",
        fraud_risk_score=0.10
    ).with_inputs("order_id", "item_category", "days_since_delivery", "claimed_amount", "customer_notes")
]

val_set = [
    dspy.Example(
        order_id="VAL-201",
        item_category="Electronics",
        days_since_delivery=60,
        claimed_amount=80.0,
        customer_notes="Return window expired but please refund.",
        decision="DENIED",
        fraud_risk_score=0.60
    ).with_inputs("order_id", "item_category", "days_since_delivery", "claimed_amount", "customer_notes"),
    
    dspy.Example(
        order_id="VAL-202",
        item_category="Electronics",
        days_since_delivery=5,
        claimed_amount=899.99,
        customer_notes="High value laptop damaged during shipping.",
        decision="NEEDS_MANUAL_REVIEW",
        fraud_risk_score=0.50
    ).with_inputs("order_id", "item_category", "days_since_delivery", "claimed_amount", "customer_notes")
]

print(f"✅ Formulated {len(train_set)} training examples and {len(val_set)} validation examples.")
""")

# --- CELL 08: Defining the Metric ---
add_md("""## 🎯 Cell 08: Defining the Optimization Metric

The **Metric Function** tells the DSPy optimizer what success looks like.
It takes `(example, prediction, trace=None)` and returns a `float` or `bool`.
""")

add_code("""def refund_policy_metric(example, pred, trace=None):
    score = 0.0
    
    # 1. Correct Policy Decision (Primary objective: 60% of score)
    clean_pred_decision = str(pred.decision or "").strip().upper()
    if clean_pred_decision == example.decision.strip().upper():
        score += 0.6
        
    # 2. Fraud Risk Score Calibration (20% of score)
    try:
        pred_risk = float(pred.fraud_risk_score)
        if abs(pred_risk - example.fraud_risk_score) <= 0.25:
            score += 0.2
    except (ValueError, TypeError):
        pass
        
    # 3. Policy Reasoning Quality (20% of score)
    if hasattr(pred, "policy_reason") and len(str(pred.policy_reason)) > 15:
        score += 0.2

    # If trace is active, the optimizer is filtering demonstrations
    return score >= 0.8 if trace is not None else score

print("✅ refund_policy_metric defined.")
""")

# --- CELL 09: Evaluating Uncompiled Baseline ---
add_md("""## 📈 Cell 09: Evaluating the Uncompiled Baseline

Let's quantitatively score our uncompiled `cot_predictor` across the validation set before any optimization.
""")

add_code("""evaluator = dspy.Evaluate(
    devset=val_set,
    metric=refund_policy_metric,
    num_threads=1,
    display_progress=True,
    display_table=True
)

baseline_score = evaluator(cot_predictor)
print(f"📊 Baseline (Zero-Shot) Quantitative Score: {baseline_score:.2f}%")
""")

# --- CELL 10: Compiling with Teleprompter ---
add_md("""## 🚀 Cell 10: Compiling with `dspy.BootstrapFewShot`

Now we optimize! DSPy runs candidate demonstrations through the teacher pipeline, verifies them against our `refund_policy_metric`, and keeps only the high-performing few-shot traces.
""")

add_code("""from dspy.teleprompt import BootstrapFewShot

# Initialize the Teleprompter / Optimizer
teleprompter = BootstrapFewShot(
    metric=refund_policy_metric,
    max_bootstrapped_demos=2,
    max_labeled_demos=2,
    max_rounds=1
)

print("⏳ Compiling program via BootstrapFewShot...")
# Compile creates an optimized program with dynamically curated demonstrations
compiled_cot_predictor = teleprompter.compile(
    student=cot_predictor,
    trainset=train_set
)

print("✅ Compilation complete!")
# Evaluate the newly compiled program
optimized_score = evaluator(compiled_cot_predictor)
print(f"🚀 Optimized Quantitative Score: {optimized_score:.2f}% (vs Baseline: {baseline_score:.2f}%)")
""")

# --- CELL 11: Inspecting Compiled Prompts ---
add_md("""## 🔬 Cell 11: Inspecting the Optimized Prompt

Let's run a test query on our compiled predictor and inspect the prompt history. Notice how DSPy automatically synthesized and injected high-quality rationale demonstrations!
""")

add_code("""test_case = {
    "order_id": "TEST-888",
    "item_category": "Apparel",
    "days_since_delivery": 10,
    "claimed_amount": 35.0,
    "customer_notes": "T-shirt has a seam tear near collar."
}

# Run the compiled program
compiled_result = compiled_cot_predictor(**test_case)

print(f"Compiled Decision:      {compiled_result.decision}")
print(f"Compiled Policy Reason: {compiled_result.policy_reason}\n")

print("--- [INSPECTING OPTIMIZED PROMPT DEMONSTRATIONS] ---")
lm.inspect_history(n=1)
""")

# --- CELL 12: Saving and Loading in Production ---
add_md("""## 💾 Cell 12: Saving & Loading the Compiled Program

Never compile prompts in live user requests. **Compile once during CI/CD or training**, save the compiled program state to disk, and load it into your production FastAPI backend.
""")

add_code("""save_path = "compiled_refund_agent.json"

# Save compiled parameters (demonstrations, instructions, signatures)
compiled_cot_predictor.save(save_path)
print(f"✅ Saved compiled DSPy program to '{save_path}'")

# In production server: Simply load the state into a clean predictor instance
prod_predictor = dspy.ChainOfThought(RefundPolicyEvaluator)
prod_predictor.load(save_path)
print("✅ Successfully reloaded compiled DSPy program for production deployment!")

# Verify production prediction
prod_result = prod_predictor(
    order_id="PROD-001",
    item_category="Electronics",
    days_since_delivery=4,
    claimed_amount=29.99,
    customer_notes="Defective charging cable."
)
print(f"Production Inference Result: {prod_result.decision} | Score: {prod_result.fraud_risk_score}")
""")

# --- BUILD IPYNB ---
notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbformat": 4,
            "nbformat_minor": 5,
            "pygments_lexer": "ipython3",
            "version": "3.11.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

output_path = os.path.join(os.path.dirname(__file__), "dspy_hands_on_masterclass.ipynb")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2)

print(f"[OK] Generated 12-stage DSPy masterclass notebook at: {output_path}")
