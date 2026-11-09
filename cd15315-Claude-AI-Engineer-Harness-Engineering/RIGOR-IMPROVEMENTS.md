# Test Rigor Improvements — No Excuses for Failing Tests

## Problem Statement

Previously, the evidence guidance was permissive about partial results. A student could report:
- "28 passed, 1 failed, but here's my analysis of why..."
- "Validator shows FAIL (2 problems), but I understand the issues and..."
- "Exit code 1, but the output looks mostly correct..."

**The issue:** This conflates evidence (proof systems work) with explanation (why they don't). A detailed narrative about a test failure doesn't make a failing test pass.

---

## Solution: Hard Blockers

Test failures and validator errors are **non-negotiable blockers.** Evidence can only come from passing systems.

### The Rule

Any of these lines is a blocker:
- ❌ `21 passed, 9 failed`
- ❌ `29 passed, 1 failed`
- ❌ `30 passed, 3 failed`
- ❌ `FAIL (2 problems)`
- ❌ Exit code 1
- ❌ `expected 35 passed, got 33`

**Action:** STOP. Do not collect evidence. Fix the code first.

### Per-System Blockers

| System | Blocker | Command |
|--------|---------|---------|
| 1 | Exactly 29 passed | `pytest tests/ -v` |
| 2 | Exactly 30 passed | `pytest tests/ -v` |
| 3 | Exactly 35 passed + validator OK | `pytest tests/ -v` AND `python -m ecommerce_team_config .` |
| 4 | Exactly 33 passed | `pytest tests/ -v` |

If any test fails, if validator returns FAIL, if exit code is non-zero → blocker.

---

## What Changed

### 1. TEST-RIGOR.md (New File)
- Comprehensive guide on test rigor
- Clear blockers for each system
- Why this rule exists
- How to handle test failures
- Acceptable vs. unacceptable scenarios
- FAQ addressing common questions

### 2. EVIDENCE-STRUCTURE.md (Updated)
**Added:** "Test Rigor — No Excuses, All Tests Pass" section at the top
- Explains what this means (29 passed = OK, 28 passed + 1 failed = NOT OK)
- Lists acceptable and unacceptable scenarios
- Rationale: "Evidence is about proving systems work, not explaining why they don't"

**Updated:** Each system section
- System 1: Added "Test Requirement (Hard Blocker)"
- System 2: Added "Test Requirement (Hard Blocker)"
- System 3: Added "Test & Validator Requirements (Hard Blockers)" — special: both must pass
- System 4: Added "Test Requirement (Hard Blocker)"

**Updated:** Alignment Checklist
- Moved test passing to the top as "Critical Blockers"
- Marked with 🔴 to indicate non-negotiable
- Separated from "Structure Verification" (which happens after tests pass)
- Added explicit rationale

### 3. EVIDENCE/README.md (Updated)
**Added:** "Test Rigor — Critical Rule" section
- Table showing blockers for all 4 systems
- "If ANY test fails" list with examples
- Why it matters (4 key points)
- What this doesn't mean (clarifications)
- What it does mean (5 positive statements)

### 4. system-N-*/README.md (Updated)
Each system's evidence guide now has:
- **⛔ Critical Blocker** section at the top
- BEFORE any "What to Capture" guidance
- Explicit list of blockers (e.g., "28 passed, 1 failed" → STOP)
- For System 3: **TWO** blockers (tests AND validator)

Examples:
- System 1: "Before collecting any evidence: `pytest tests/ -v` MUST show exactly 29 passed with exit code 0"
- System 3: Two blockers — tests must pass AND validator must show OK

### 5. README.md (Updated)
**Added:** "⛔ Read First: Test Rigor" section under Capstone
- Links to TEST-RIGOR.md
- Emphasizes this should be read first
- Lists blocker examples
- Clarifies: narrative explanations ≠ evidence

---

## Key Principles Behind the Changes

### 1. Evidence ≠ Explanation
- **Evidence:** Proof that system works (passing tests)
- **Explanation:** Why system doesn't work (analysis of failure)
- These are different. Evidence comes from passing runs.

### 2. Test Suites Define Correctness
- Tests specify what "correct" means
- Passing all tests = system meets spec
- Failing any test = system doesn't meet spec

### 3. Project Depends on Passing Systems
- Reflection brief defends architectural decisions
- Decisions only matter if implemented correctly
- Correct implementation = passing tests

### 4. All-or-Nothing
- "Mostly passing" = failing
- "Almost done" = not done
- Either all tests pass or no evidence

### 5. No Exceptions
- No "expected failures"
- No "I understand why it fails"
- No "the rest works so..."
- Fix it or don't collect evidence

---

## How This Improves Quality

### Before
```
Evidence: "28 passed, 1 failed. The failing test is about edge case X.
Here's why it fails: [detailed explanation]. The core loop logic
works correctly despite this."

Result: Weak evidence grounded in partially-working code.
```

### After
```
Blocker: "28 passed, 1 failed"
Action: Fix the test → Run again → 29 passed
Evidence: "From pytest-run-summary.md, all 29 tests passed. This
proves the loop handles all cases including edge case X."

Result: Strong evidence grounded in fully-working code.
```

---

## Specific Blockers by System

### System 1: Claims Intake Agent
✅ `29 passed` → Proceed
❌ `28 passed, 1 failed` → BLOCKER
❌ `29 passed, 1 skipped` → BLOCKER (unless reason documented)
❌ Exit code 1 → BLOCKER

### System 2: Retail Support Context Strategy
✅ `30 passed` → Proceed
❌ `29 passed, 1 failed` → BLOCKER
❌ `30 passed, 2 failed` → BLOCKER
❌ Exit code 1 → BLOCKER

### System 3: E-Commerce Team Claude Code Config
✅ `35 passed` AND validator says `OK` → Proceed
❌ `34 passed, 1 failed` → BLOCKER
❌ `35 passed` but validator says `FAIL` → BLOCKER
❌ Any validator error → BLOCKER
❌ Exit code 1 (from either command) → BLOCKER

System 3 is special: tests verify the code, validator verifies the config. Both matter.

### System 4: Multi-Shift Quality Monitoring
✅ `33 passed` → Proceed
❌ `32 passed, 1 failed` → BLOCKER
❌ `33 passed, 1 failed` → BLOCKER
❌ Exit code 1 → BLOCKER

---

## What Students Do

### Old Approach
1. Run system
2. Some tests fail
3. Collect evidence anyway
4. Explain failures in narrative
5. Submit partial evidence

### New Approach
1. Run system
2. Check: Do all tests pass?
   - YES → Step 3
   - NO → Fix code, go to Step 1
3. Check: Does validator show OK? (System 3 only)
   - YES → Step 4
   - NO → Fix config, go to Step 1
4. Collect evidence from passing run
5. Use evidence to support reflection brief

---

## FAQ About the Changes

**Q: What if a test failure is environment-related, not code?**
A: It's still a blocker until fixed. Fix the environment. Then run tests. Then collect evidence.

**Q: What if I have a known bug I'm investigating?**
A: Great! Investigate it. Fix it. Run tests. They pass. Now collect evidence from the passing run.

**Q: What if one of the four systems genuinely can't pass?**
A: Then don't include it in your submission. Or, more likely, debug deeper—these are reference implementations that ship in the repo, so they should all pass.

**Q: Can I include analysis of a failing system?**
A: No. Evidence must come from passing runs. You can discuss the debugging process separately, but not as "evidence."

**Q: What if tests are flaky (sometimes pass, sometimes fail)?**
A: That's a test suite problem. Fix the flakiness. Run tests multiple times until stable. Then collect evidence from a passing run.

**Q: Is this too strict?**
A: No. Evidence should prove systems work. Failing tests prove they don't. Fix them.

---

## Impact on Reflection Brief

### Strong Citations (from passing evidence)
> "From EVIDENCE/system-1-claims-intake/pytest-run-summary.md, all 29 tests passed.
> The loop correctly handles stop_reason by [cite specific code line]. See test_loop.py:42
> for the specific assertion."

### Weak Citations (no longer acceptable)
> "The loop test failed, but my understanding of the code suggests [analysis]. Despite
> the failure, the logic should work correctly because [explanation]."

**Never submit the weak version.** Fix the test. Then submit the strong version.

---

## Documentation Files Changed

| File | Change | Why |
|------|--------|-----|
| TEST-RIGOR.md | NEW | Comprehensive rigor guide |
| EVIDENCE-STRUCTURE.md | "Test Rigor" section added | Upfront clarity on blockers |
| EVIDENCE/README.md | "Test Rigor" section added | Quick reference on blockers |
| system-1/README.md | "Critical Blocker" section added | No evidence without 29 passed |
| system-2/README.md | "Critical Blocker" section added | No evidence without 30 passed |
| system-3/README.md | "Critical Blockers" section added | No evidence without 35 passed + validator OK |
| system-4/README.md | "Critical Blocker" section added | No evidence without 33 passed |
| README.md | "Read First: Test Rigor" added | Emphasize importance |

---

## Summary

**The change:** Evidence must come from passing systems. Tests failing = blocker. No exceptions.

**Why:** Evidence proves systems work. Passing tests = proof. Failing tests = no proof.

**How it works:** Before collecting evidence, verify all tests pass. If not, fix them. Then collect evidence from the passing run.

**Result:** Stronger capstone submissions grounded in fully-working implementations, not partial explanations.
