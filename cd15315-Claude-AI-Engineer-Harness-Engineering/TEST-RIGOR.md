# Test Rigor — Passing Tests is a Prerequisite, Not Evidence

## Critical Distinction

**Tests passing ≠ Evidence**

- **Tests passing:** Code is correct (prerequisite)
- **Evidence:** Run artifacts prove architectural decisions work (actual proof)

This guide is about the prerequisite: all tests must pass before you can collect evidence.

For what actually counts as evidence, see [EVIDENCE-VS-TESTS.md](EVIDENCE-VS-TESTS.md).

## The Standard

**Tests must pass to proceed. But evidence is proof that systems work architecturally, not just that code compiles.**

Any line like these is a blocker:
- ❌ `21 passed, 9 failed`
- ❌ `30 passed, 3 failed`
- ❌ `FAIL (2 problems)`
- ❌ Exit code 1
- ❌ `expected 35 passed, got 33`

Even if your narrative report explains why a test failed, **the project depends on executable proof from the official test suites.** No amount of detailed explanation substitutes for passing tests.

---

## Critical Blockers by System

### System 1: Claims Intake Agent
```
✅ ACCEPT:  29 passed
❌ REJECT:  28 passed, 1 failed
❌ REJECT:  29 passed, 1 skipped (without documented reason)
❌ REJECT:  Exit code 1
```
**Command:** `pytest tests/ -v`

### System 2: Retail Support Context Strategy
```
✅ ACCEPT:  30 passed
❌ REJECT:  29 passed, 1 failed
❌ REJECT:  30 passed, 1 skipped (without documented reason)
❌ REJECT:  Exit code 1
```
**Command:** `pytest tests/ -v`

### System 3: E-Commerce Team Claude Code Config
```
BOTH must pass:

1. Tests:
   ✅ ACCEPT:  35 passed
   ❌ REJECT:  34 passed, 1 failed
   ❌ REJECT:  35 passed, 1 skipped (without documented reason)
   ❌ REJECT:  Exit code 1

2. Validator:
   ✅ ACCEPT:  "OK" (exit 0)
   ❌ REJECT:  "FAIL (2 problems)"
   ❌ REJECT:  "FAIL (1 problem)"
   ❌ REJECT:  Exit code 1

Commands:
- pytest tests/ -v
- python -m ecommerce_team_config .
```

### System 4: Multi-Shift Quality Monitoring
```
✅ ACCEPT:  33 passed
❌ REJECT:  32 passed, 1 failed
❌ REJECT:  33 passed, 1 skipped (without documented reason)
❌ REJECT:  Exit code 1
```
**Command:** `pytest tests/ -v`

---

## Why This Rule Exists

### Evidence is Proof, Not Explanation

**Scenario A: Test Fails**
- You write detailed analysis explaining why the test failed
- You document the bug thoroughly
- You provide narrative context

**Result:** No evidence. The system doesn't work. Explanation doesn't change that.

**Scenario B: Test Passes**
- System works
- You analyze how it works
- You cite the passing test as proof

**Result:** Evidence. Strong foundation for reflection brief.

### Test Suites Define Correctness

- Test suite specifies what "correct" means
- Passing all tests = system meets specification
- Failing any test = system doesn't meet specification
- "Almost passing" = failing

### The Project Depends on It

The capstone reflection brief asks you to defend architectural decisions. You can only defend decisions made by working code. Partial evidence from partially-working code:
- Undermines your analysis
- Makes citations weaker
- Shows the system incomplete

### Your Analysis is Only Meaningful on Working Code

When you analyze how the agentic loop controls `stop_reason`, that analysis is only meaningful if:
- The loop test suite passes
- The traced claims were routed correctly
- The end-to-end system completed successfully

Analyzing a broken loop teaches you about debugging, not about harness engineering.

---

## What To Do If Tests Fail

### Step 1: Identify the Blocker
```
pytest tests/ -v
# Output: "28 passed, 1 failed"
```

### Step 2: Read the Failure
```
FAILED tests/test_loop.py::test_continue_on_tool_use - AssertionError: ...
```

### Step 3: Debug and Fix
- Look at the test code
- Understand what it expects
- Fix the implementation
- Re-run: `pytest tests/ -v`

### Step 4: Verify Complete Pass
```
pytest tests/ -v
# Output: "29 passed"
# Exit code: 0
```

### Step 5: Collect Evidence
Now, and only now, capture the passing run output, traces, etc.

---

## Acceptable Scenarios for Evidence

### ✅ All Tests Pass
```bash
$ pytest tests/ -v
================================ test session starts =================================
...
============================== 29 passed in 1.23s ================================
```
→ Proceed with evidence collection

### ✅ All Tests Pass (with documented skips)
```bash
$ pytest tests/ -v
...
============================== 29 passed, 1 skipped in 1.23s ========================

Skipped: test_deprecated_api (scheduled removal in v2.0)
```
→ Acceptable if skip reason is documented. Proceed.

### ✅ Validator Shows OK
```bash
$ python -m ecommerce_team_config .
Checking CLAUDE.md... OK
Checking .claude/standards/... OK
Checking .claude/rules/... OK
Checking .claude/commands/... OK
Checking .claude/skills/... OK
Overall: OK
```
→ Proceed with evidence collection

---

## Unacceptable Scenarios

### ❌ Test Failures
```bash
$ pytest tests/ -v
...
FAILED tests/test_antipatterns.py::test_no_double_call - AssertionError: ...
============================== 28 passed, 1 failed in 2.31s ==========================
```
**Action:** STOP. Do not collect evidence. Fix the test first.

### ❌ Partial Validator Pass
```bash
$ python -m ecommerce_team_config .
Checking CLAUDE.md... OK
Checking .claude/standards/... OK
Checking .claude/rules/... FAIL (glob pattern mismatch in react.md)
Overall: FAIL (1 problem)
```
**Action:** STOP. Do not collect evidence. Fix the config. Rerun validator.

### ❌ Narrative Explanation for Failure
```
My test is failing because X, but I understand why and here's my analysis:
[detailed explanation of root cause and why it's actually fine]
```
**Action:** STOP. No. This doesn't make it evidence. Fix the test. Then collect evidence from the passing run.

### ❌ Partial Run Claims
```
Most tests passed, but I'll skip the 1 failing test and collect evidence anyway
because the rest of the system works fine.
```
**Action:** STOP. No exceptions. Either all tests pass or no evidence. Fix them all.

---

## Citation in Reflection Brief

When citing test evidence in your reflection brief:

### ✅ Strong Citation (from passing run)
> "From EVIDENCE/system-1-claims-intake/pytest-run-summary.md, the test suite passed all 29 tests (pytest output attached in pytest-run.txt). This proves the loop correctly handles `stop_reason`: [quote specific test assertion from test_loop.py:XX]."

### ❌ Weak Citation (explaining a failure)
> "The test for `tool_use` handling actually failed, but here's why: [narrative explanation]. Despite the failure, the logic is sound and [detailed reasoning]."

**Never.** If the test fails, fix it. Then cite it only after it passes.

---

## FAQ

**Q: What if a test fails due to environmental setup, not actual code?**
A: Fix the environment. That's still a blocker until it's resolved. Once everything works, then collect evidence.

**Q: What if a test is skipped?**
A: Document the skip reason. If it's temporary (e.g., "skip: TODO implementation"), fix the code and unskip. Otherwise list the reason. Test rigor means *all* tests pass or you explain why specific skips are acceptable.

**Q: What if most tests pass but one is known broken?**
A: It's a blocker. Either fix it or document the known issue (in the repo, not in your evidence narrative). Then run again with fix in place.

**Q: What if I have partial evidence (some systems pass, others don't)?**
A: Collect evidence only from passing systems. For failing systems, either: (a) fix them and re-run, or (b) don't include their evidence in your submission.

**Q: Can I collect evidence from a run that mostly works with one known issue?**
A: No. "Mostly works" is still broken. Evidence = passing. Partial runs = not evidence.

**Q: What about flaky tests?**
A: If a test is flaky, that's a test suite problem. Fix the flakiness. Once stable, collect evidence from a passing run.

---

## Summary

| Scenario | Action |
|----------|--------|
| Tests pass, validator OK | ✅ Collect evidence |
| Any test fails | ❌ Fix code, rerun |
| Validator shows FAIL | ❌ Fix config, rerun |
| Exit code 1 | ❌ Debug, fix, rerun |
| Detailed explanation for failure | ❌ Explanation ≠ evidence. Fix code. |
| "Most tests pass" | ❌ All or nothing. Fix remaining tests. |
| Tests pass, but you know it's fragile | ✅ Collect evidence (and fix fragility in future) |

**The principle:** Evidence comes from passing runs. Passing tests = working system = valid evidence for reflection brief.
