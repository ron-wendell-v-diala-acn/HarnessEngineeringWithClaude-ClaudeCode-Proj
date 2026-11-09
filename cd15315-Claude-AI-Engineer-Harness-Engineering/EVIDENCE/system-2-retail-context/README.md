# System 2 Evidence: Retail Support Context Strategy

**Project:** `Engineer a Long-Conversation Context Strategy for a Retail Support Copilot/04-assemble-and-locate/solution/`

**Run commands:**
```bash
pytest tests/ -v                       # expect 30 passed
python -m retail_context.run --all     # assemble context + run 6 evals + control
```

## ⛔ Important: Tests Passing ≠ Evidence

**Before you collect evidence, understand the difference:**

- **Tests passing (30 passed)** = prerequisite. Code is correct. ✅ Required.
- **Run artifacts** = actual evidence. Proves context reduction achieves token goals, facts block improves accuracy, etc.

Read [../../EVIDENCE-VS-TESTS.md](../../EVIDENCE-VS-TESTS.md) to understand what counts as real evidence.

### Test Blocker

**`pytest tests/ -v` MUST show exactly 30 passed with exit code 0.**

If you see:
- ❌ `29 passed, 1 failed`
- ❌ `30 passed, 1 skipped` (without documented reason)
- ❌ Exit code 1

**STOP.** Fix the test failures first.

### Evidence Requirements (After Tests Pass)

Don't just collect test output. Collect **actual run artifacts** that prove the design works:

- ✅ **Actual `budget.json`** showing baseline → assembled token reduction (real numbers)
- ✅ **Actual `eval.jsonl`** showing which questions passed (actual eval results)
- ✅ **Actual `eval_control.jsonl`** (no facts block) showing regression (proves facts block is essential)
- ✅ **Per-section token breakdown** showing which section dominates and why

These artifacts prove context reduction actually achieves token budgets AND facts block improves accuracy. Test passing alone doesn't prove that.

---

## What to Capture

### 1. Test Evidence
- **`pytest-run.txt`** — Full terminal output from `pytest tests/ -v`
- **`pytest-run-summary.md`** — Parsed summary:
  - Total test count (should be 30)
  - Any assertion failures
  - Key test modules: `test_assembler.py`, `test_reducer.py`, `test_evaluator.py`

### 2. Code Analysis

#### `retail_context/assembler.md`
Analyze context assembly. Answer:
- **File:** `retail_context/assembler.py` (or equivalent)
- **Assembly process:** Quote the function that stitches sections together
- **Section types:** What sections comprise the context? (e.g., facts, policies, history)
- **Ordering:** How is the order determined?

#### `retail_context/reducer.md`
Analyze token reduction strategy. Answer:
- **File:** `retail_context/reducer.py` (or equivalent)
- **Reduction strategy:** What gets summarized vs. kept verbatim?
- **Core logic:** Quote the decision code (e.g., "if section_type == 'facts': summarize")
- **Thresholds:** Are there token limits per section?
- **Proof:** Show one summarized section vs. one verbatim section with token counts

#### `retail_context/evaluator.md`
Analyze evaluation logic. Answer:
- **File:** `retail_context/evaluator.py` (or equivalent)
- **Evaluation loop:** How are 6 questions posed to the context?
- **Pass/fail logic:** What makes a question "pass"?
- **Control design:** How does the no-facts-block control differ?

### 3. Run Evidence

#### `runs/run-summary.md`
From your `python -m retail_context.run --all` execution, capture:
- **Timestamp** of run
- **Run ID** (if applicable)
- **Exit code** (should be 0)
- **Phases executed:**
  - Context assembly: ✅
  - 6 evals: ✅
  - Control run: ✅

#### `runs/context/context-assembled.md`
From `runs/<run_id>/context.md`, extract:
- **Overall structure:** How many sections? Approximate token count before reduction?
- **Section list:** Quote or list all section names
- **Size:** Total assembled tokens

#### `runs/context/context-sections.md`
Breakdown per section (from `context.md`):

| Section | Type | Original Tokens | After Reduction | Method |
|---------|------|-----------------|-----------------|--------|
| Facts | Facts | 12,000 | 1,200 | Summarized |
| Policies | Verbatim | 5,000 | 5,000 | Kept exact |
| History | Summarized | 8,000 | 2,000 | Summarized |

- **Largest section:** Which dominates the reduced context? Why keep it?
- **Reduction rule:** Quote the code logic for section-type handling

#### `runs/budget.json`
Copy the actual JSON file from run. Then create **`budget-analysis.md`**:
```markdown
## Budget Analysis

**From:** `runs/<run_id>/budget.json`

- **Baseline tokens:** [number from JSON]
- **Assembled tokens (after reduction):** [number from JSON]
- **Reduction %:** [calculate: (baseline - assembled) / baseline × 100]

**Per-section breakdown:**
```
[Quote JSON section breakdown showing tokens saved per category]
```

**Which section dominates?** [e.g., "Facts block at 8,000 tokens"]
**Why keep it verbatim?** [Quote justification from README or code]
```

#### `runs/eval/eval-analysis.md`
From `runs/<run_id>/eval.jsonl`, extract:
- **Total questions:** 6
- **Passed:** [count]
- **Question examples:** Quote 2–3 questions and results
- **Example:**
  ```json
  {
    "question": "What's our return policy for damaged items?",
    "answer_found": true,
    "context_cited": "In the Policies section..."
  }
  ```

#### `runs/eval/eval-control-analysis.md`
From `runs/<run_id>/eval_control.jsonl` (same 6 questions, no facts block):
- **Passed:** [count]
- **Regression analysis:** Which questions failed in control but passed in main eval?
- **Example regression:**
  ```
  Question: "Can you find the specific damage warranty terms?"
  Main eval: ✅ PASS (found in facts block)
  Control eval: ❌ FAIL (facts block removed, couldn't answer)
  Proof: Facts block was essential for this question
  ```
- **Insight:** Quote what the regression proves about the facts block's value

### 4. Test Analysis

#### `tests/test-assembler.md`
Brief analysis:
- **File:** `tests/test_assembler.py` (or integration tests)
- **Key assertions:** What does assembler verification check?
- **Quote one:** Show an assembly test
- **Purpose:** What would break without proper assembly?

#### `tests/test-reducer.md`
Brief analysis:
- **File:** `tests/test_reducer.py`
- **Key assertions:** Token reduction correctness? Preserve critical sections?
- **Quote one:** Show a reduction test
- **Purpose:** Why is reduction tested independently?

#### `tests/test-evaluator.md`
Brief analysis:
- **File:** `tests/test_evaluator.py`
- **Key assertions:** How are pass/fail decisions validated?
- **Quote one:** Show an evaluation test

---

## Alignment Checklist

- ✅ `retail_context/*.md` files reference actual files with line numbers
- ✅ `runs/budget-analysis.md` quotes directly from `budget.json` JSON structure
- ✅ `runs/eval/eval-analysis.md` includes actual questions from `eval.jsonl`
- ✅ `runs/eval/eval-control-analysis.md` shows specific question regressions
- ✅ Test analyses reference actual test file paths (`tests/test_*.py`)
- ✅ Per-section token counts match `budget.json` data

---

## Example Citation in Reflection Brief

When answering reflection question #5 (*The reduction. From budget.json: baseline tokens, assembled tokens, reduction %*):

> "From EVIDENCE/system-2-retail-context/runs/budget-analysis.md: baseline was 47,832 tokens, assembled is 18,924 tokens, a 60% reduction. The Facts section dominates at 8,000 tokens (post-reduction) and is kept verbatim. See runs/<run_id>/budget.json and retail_context/reducer.py line 34."

When answering question #7 (*Facts block. Compare eval.jsonl to eval_control.jsonl*):

> "From EVIDENCE/system-2-retail-context/runs/eval/eval-control-analysis.md: the control run (no facts block) failed on 'What's our damage warranty?' but the main eval passed. The facts block was critical — its removal caused regression, proving its necessity."

---

## File Reference Summary

| Evidence File | Project File | Purpose |
|---------------|--------------|---------|
| `pytest-run-summary.md` | `tests/test_*.py` | Parse test results |
| `retail_context/assembler.md` | `retail_context/assembler.py` | Context assembly logic |
| `retail_context/reducer.md` | `retail_context/reducer.py` | Token reduction strategy |
| `retail_context/evaluator.md` | `retail_context/evaluator.py` | Eval question logic |
| `runs/budget-analysis.md` | `runs/<run_id>/budget.json` | Token accounting |
| `runs/context/context-sections.md` | `runs/<run_id>/context.md` | Per-section breakdown |
| `runs/eval/eval-analysis.md` | `runs/<run_id>/eval.jsonl` | Main eval results |
| `runs/eval/eval-control-analysis.md` | `runs/<run_id>/eval_control.jsonl` | Control comparison |
| `tests/test-*.md` | `tests/test_*.py` | Test coverage analysis |

---

## Reflection Brief Citations

System 2 questions:
- **#5 (The reduction)** → `runs/budget-analysis.md` + `retail_context/reducer.md`
- **#6 (Summarize vs preserve)** → `runs/context/context-sections.md` + `retail_context/reducer.md`
- **#7 (Facts block)** → `runs/eval/eval-analysis.md` + `runs/eval/eval-control-analysis.md`
