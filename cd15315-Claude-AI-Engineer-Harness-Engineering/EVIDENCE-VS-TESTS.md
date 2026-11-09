# Evidence vs. Tests — The Critical Distinction

## The Problem

**Tests passing is a prerequisite, not evidence.**

Evidence is concrete proof that architectural decisions work. Tests passing proves the code *compiles and runs*. That's necessary but not sufficient.

---

## The Difference

### ❌ NOT Evidence
- `29 passed` in pytest output
- `validator shows OK`
- Exit code 0
- "All tests passed successfully"

**Why:** Tests verify code correctness. They don't prove architectural decisions work in practice.

### ✅ IS Evidence

**System 1 (Claims Intake):**
- Actual trace showing `stop_reason` sequence across 3+ turns
- Claim routed to correct queue (proof tool routing works)
- Token count showing loop efficiency

**System 2 (Retail Context):**
- Actual `budget.json` showing baseline vs. assembled tokens
- Real `eval.jsonl` with questions that passed (proof facts block works)
- Actual `eval_control.jsonl` showing regression (proof facts block is essential)

**System 3 (Claude Code Config):**
- Actual validator output showing `OK` (not just "it worked")
- Actual `.claude/` file structure in evidence matching project structure
- Proof that config hierarchy validates

**System 4 (Multi-Shift Quality Monitoring):**
- Actual `hot_state.json` file showing it stays under budget
- Actual run output showing warm-tier filtered results (not full history)
- Proof that SQL query returns limited defects
- Actual `shift_scratchpad.jsonl` showing fork isolation

---

## The Three Levels

### Level 1: Prerequisites (Tests Pass)
```
pytest tests/ -v → 29 passed
```
**What this proves:** Code is correct
**What this does NOT prove:** Architecture works as intended
**Status:** Must pass, but alone is insufficient

### Level 2: Execution Artifacts (Run Proof)
```
From actual run:
- traces/claim-01-trace.md (captured from runs/<timestamp>/traces/)
- budget.json (captured from runs/<timestamp>/budget.json)
- hot_state.json (captured from data/hot_state.json, showing size)
```
**What this proves:** System works as designed when running end-to-end
**Status:** This is actual evidence

### Level 3: Narrative Support (Understanding)
```
"The warm-tier SQL query returns only the 100 most recent high-severity
defects (query from warm.py:42), keeping the model from seeing full
history. This is necessary because [reason]."
```
**What this proves:** You understand why decisions were made
**Status:** Supports evidence, but doesn't replace it

---

## System-Specific Evidence (Not Just Tests)

### System 1: Claims Intake Agent

❌ NOT sufficient:
- "All 29 tests passed"
- "test_loop.py assertions are correct"

✅ IS sufficient:
- Actual `runs/<timestamp>/traces/claim-01-trace.jsonl` showing stop_reason sequence
- Actual claim routed to queue (from `runs/<timestamp>/queues/*.jsonl`)
- Actual token count and turns for the claim
- Table showing all 8 claims routed to correct destinations

**Why the difference:** Tests verify loop *logic*. Artifacts prove loop works end-to-end on real claims.

### System 2: Retail Support Context

❌ NOT sufficient:
- "All 30 tests passed"
- "test_reducer.py and test_evaluator.py assertions pass"

✅ IS sufficient:
- Actual `budget.json` from run showing baseline/assembled token counts
- Actual `eval.jsonl` showing which 6 questions passed
- Actual `eval_control.jsonl` (facts block removed) showing regression on at least 1 question
- Actual per-section token breakdown showing which section dominates

**Why the difference:** Tests verify reduction *logic*. Artifacts prove reduction actually achieves token goals and facts block actually improves eval accuracy.

### System 3: Claude Code Config

❌ NOT sufficient:
- "All 35 tests passed"
- "Validator shows OK"
- "Config hierarchy is correct"

✅ IS sufficient:
- Actual validator output showing `OK` (printed to validator-output.txt)
- Actual `.claude/` file structure in evidence matching project structure exactly
- Proof that path-scoped rules apply correctly (quote the glob + example file that matches)
- Proof that deploy-check skill has `context: fork` (SKILL.md copy + analysis)
- Proof that allowed-tools allowlist prevents dangerous operations (quote the restrictions)

**Why the difference:** Tests verify config code. Artifacts prove config is structured correctly and validators confirm it.

### System 4: Multi-Shift Quality Monitoring

❌ NOT sufficient:
- "All 33 tests passed"
- "Test assertions about warm tier and hot state are correct"

✅ IS sufficient:
- Actual `hot_state.json` from a real shift run showing byte size under budget
- Actual run output showing SQL query returned limited defects (not full history)
- Actual quote from warm.py showing the LIMIT clause
- Actual `shift_scratchpad.jsonl` showing isolated state from fork
- Proof that recovery logic chooses fresh vs. resume (actual code quote)

**Why the difference:** Tests verify orchestration *logic*. Artifacts prove orchestration works end-to-end with real state, real budgets, real filtering.

---

## The Evidence Checklist (Not Just "Tests Pass")

### System 1: Claims Intake

- ✅ 29 tests pass (prerequisite)
- ✅ Actual trace from `runs/` directory (not synthetic)
- ✅ Trace shows stop_reason sequence with 3+ turns
- ✅ Claim successfully routed to queue
- ✅ All 8 fixtures routed to correct destinations
- ✅ Token counts documented from actual run

### System 2: Retail Context

- ✅ 30 tests pass (prerequisite)
- ✅ Actual `budget.json` from run (not hypothetical)
- ✅ Token baseline, assembled, and % reduction (real numbers)
- ✅ Actual `eval.jsonl` with pass/fail results
- ✅ Actual `eval_control.jsonl` showing regression (facts block proves its necessity)
- ✅ Per-section token breakdown

### System 3: Claude Code Config

- ✅ 35 tests pass (prerequisite)
- ✅ Validator prints `OK` (not "tests pass, so likely OK")
- ✅ Actual `.claude/` structure matches project structure
- ✅ Actual `SKILL.md` with context: fork and allowed-tools
- ✅ Path-scoped rule glob patterns work (quote example files)
- ✅ Config hierarchy validated by actual validator run

### System 4: Multi-Shift Monitoring

- ✅ 33 tests pass (prerequisite)
- ✅ Actual `hot_state.json` file from run (with real byte size)
- ✅ Byte size provably under budget
- ✅ SQL query returns limited defects (LIMIT clause, timestamp filter shown)
- ✅ Actual run output showing filtered results
- ✅ Recovery staleness threshold documented with code quote
- ✅ Actual `shift_scratchpad.jsonl` showing fork isolation

---

## What Counts as Evidence

### ✅ Artifacts (Use These)

Real files from actual runs:
- `runs/<timestamp>/traces/claim-01.jsonl` ← actual trace
- `budget.json` ← actual JSON from run
- `eval.jsonl` ← actual results
- `hot_state.json` ← actual state file
- `validator-output.txt` ← actual validator output
- `shift_scratchpad.jsonl` ← actual scratchpad from fork
- `pytest-run.txt` ← full test output

### ✅ Parsed Analysis (Use These)

Your interpretation of artifacts:
- "From budget.json: baseline 47,832 → assembled 18,924 (60% reduction)"
- "From eval.jsonl: 6/6 questions passed (see attached)"
- "From hot_state.json: 2,847 bytes (well under 5KB budget)"
- "From trace: stop_reason sequence shows tool_use, tool_use, end_turn"

### ❌ Generic Claims (Don't Use These)

Statements without artifacts:
- "The loop works correctly"
- "Context reduction is efficient"
- "Config hierarchy is valid"
- "State stays small"

These need proof. Show the artifact.

### ❌ Test Outputs Alone (Don't Use These)

Tests as evidence:
- "All tests passed"
- "Test assertions are correct"
- "Validator shows tests pass"

Tests are prerequisites. Show the real output.

---

## Citation Pattern: Strong vs. Weak

### ❌ WEAK (Based on Test Passing)
> "From pytest-run.txt, the test suite passed, confirming that the loop correctly
> handles stop_reason. The test assertions verify the logic is correct."

**Problem:** You're describing tests, not evidence. Tests verify code. Where's proof it works?

### ✅ STRONG (Based on Run Artifacts)
> "From EVIDENCE/system-1-claims-intake/runs/traces/claim-01-trace.md, the actual
> trace shows: Turn 1: stop_reason='tool_use' (classify_claim), Turn 2: stop_reason=
> 'tool_use' (route_claim), Turn 3: stop_reason='end_turn' (complete). Claim routed
> to home queue. This proves the loop (claims_intake/loop.py:42) correctly dispatches
> on stop_reason to achieve routing. Total: 3 turns, 1,842 tokens."

**Strength:** You show actual output proving the decision works. You cite the code. You show the result.

---

## Reflection Brief Citations

### ❌ Weak (Test-Based)
> "Question #11: The tests for warm-tier query filtering verify that the implementation
> correctly limits defect results. The test assertions show this works."

### ✅ Strong (Artifact-Based)
> "Question #11: From EVIDENCE/system-4-shift-monitor/shift_monitor/warm-store.md,
> the SQL query (warm.py:34) is:
> ```sql
> SELECT * FROM defects WHERE filed_at > now() - interval '7 days'
> ORDER BY severity DESC LIMIT 100
> ```
> From actual run output (shift-output.txt), the model received exactly 100 defects
> (the LIMIT), not the full 50,000+ in the warm tier. This proves the query
> successfully 'pushes work down' to the database, preventing the model from
> seeing full history. Without LIMIT, token budget would exceed available context."

**Why stronger:** You show the query, the result, the constraint, and why it matters.

---

## The Evidence Standard

**Mandatory:**
1. Tests pass (prerequisite — must be first)
2. Run artifacts exist (traces, JSON, output files)
3. Artifacts show architectural decisions actually work
4. You cite the artifacts in reflection brief

**Optional but helpful:**
1. Code quotes explaining why decisions were made
2. Comparative data (before/after, with/without)
3. Analysis of how artifacts prove claims

**Not acceptable:**
1. "Tests pass, so the architecture is correct"
2. "Code looks right, so it should work"
3. "I verified this manually, trust me"
4. Explanation without proof

---

## Summary

| What | Is It Evidence? | Why |
|-----|-----------------|-----|
| Tests pass | ❌ Prerequisite only | Proves code compiles, not that design works |
| Actual trace showing stop_reason | ✅ YES | Proves loop routes claims correctly |
| "Loop logic is correct" | ❌ No | That's an explanation, not proof |
| `budget.json` showing 60% reduction | ✅ YES | Proves context strategy achieves goals |
| `eval.jsonl` with passing questions | ✅ YES | Proves facts block improves accuracy |
| "Tests confirm reduction works" | ❌ No | Show the actual budget numbers |
| `hot_state.json` at 2,847 bytes | ✅ YES | Proves state stays under budget |
| "Hot state is constrained" | ❌ No | Show the actual file size |
| Validator shows `OK` | ✅ YES | Proves config hierarchy is valid |
| "Config is correct" | ❌ No | Show validator output |

---

## Action Items for Evidence Collection

### Before Collection (Tests Pass)
```bash
pytest tests/ -v                    # Must show all tests passing
python -m ecommerce_team_config .   # System 3 only: must show OK
```

### During Collection (Capture Artifacts)
```bash
# Save actual files, not summaries
cp runs/<timestamp>/traces/*.jsonl EVIDENCE/system-1/.../
cp runs/<timestamp>/budget.json EVIDENCE/system-2/runs/
cp data/hot_state.json EVIDENCE/system-4/data/
cp validator-output.txt EVIDENCE/system-3/
```

### During Analysis (Cite Artifacts)
```
"From [actual file], [actual data] proves [architectural decision works].
Quote the relevant code line. Show the supporting metric."
```

### In Reflection Brief (Use Artifacts)
```
"Answer: [Quote from artifact]. This is proof that [design decision] works
because [metric from artifact]. Code reference: [file:line]."
```

---

## Key Insight

**Tests passing = "The code works correctly"**
**Run artifacts = "The architecture achieves its goals"**
**These are different things. Both are necessary. Tests alone are not evidence.**

Your reflection brief is defending architectural decisions (layer 3 orchestration, forked contexts, token budgets, path-scoped rules). You can only defend them with proof they work. That proof is artifacts from real runs, not test suites.
