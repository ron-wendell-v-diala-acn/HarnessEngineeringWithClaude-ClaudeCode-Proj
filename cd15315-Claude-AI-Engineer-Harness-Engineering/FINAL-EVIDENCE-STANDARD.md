# Final Evidence Standard — Complete Specification

## The Definitive Standard

**Evidence is concrete proof that architectural decisions work. Tests are prerequisites.**

### Three Layers (All Required)

#### Layer 1: Tests Pass (Prerequisite)
```
pytest tests/ -v
→ System 1: 29 passed ✅
→ System 2: 30 passed ✅
→ System 3: 35 passed ✅ AND validator shows OK ✅
→ System 4: 33 passed ✅
```
**What this proves:** Code is correct
**What this does NOT prove:** Architecture works

**If tests fail → STOP. Fix code. Do not collect evidence.**

#### Layer 2: Run Artifacts (Actual Evidence)
```
Actual files from real execution:
→ System 1: runs/<timestamp>/traces/claim-01.jsonl
→ System 2: runs/<timestamp>/budget.json + eval.jsonl + eval_control.jsonl
→ System 3: .claude/ folder structure + validator-output.txt
→ System 4: data/hot_state.json + shift-output.txt + shift_scratchpad.jsonl
```
**What this proves:** Architectural decisions work in practice
**Status:** This is actual evidence

#### Layer 3: Analysis & Citations (Supporting Context)
```
Your interpretation of artifacts with code quotes:
→ "From budget.json: 47,832 → 18,924 tokens (60% reduction)"
→ "From trace: stop_reason = tool_use, tool_use, end_turn (routing)"
→ "From hot_state.json: 2,847 bytes (under 5KB budget)"
→ "SQL query (warm.py:34): LIMIT 100 returns filtered results"
```
**What this proves:** You understand why decisions were made
**Status:** Supports evidence, doesn't replace it

---

## System-Specific Standards

### System 1: Claims Intake Agent

❌ NOT Sufficient:
- "All 29 tests passed"
- "test_loop.py assertions verify the logic"
- "The loop should work correctly"

✅ IS Sufficient:
- **Actual trace** from `runs/<timestamp>/traces/claim-01.jsonl`
  - Shows stop_reason sequence: `tool_use` → `tool_use` → `end_turn`
  - Documents claim routed to correct queue
  - Records actual token count (not theoretical)
- **All 8 claims** successfully routed to correct destinations (proof in actual queues)
- **Table of outcomes** showing routing accuracy

**Why the difference:** Tests verify loop logic. Traces prove loop routes real claims correctly.

### System 2: Retail Support Context

❌ NOT Sufficient:
- "All 30 tests passed"
- "test_reducer.py assertions confirm token reduction"
- "Reduction algorithm is correct"

✅ IS Sufficient:
- **Actual `budget.json`** from run showing:
  - Baseline tokens: 47,832
  - Assembled tokens: 18,924
  - Reduction: 60% ← Real numbers, not theoretical
- **Actual `eval.jsonl`** showing which 6 questions passed
- **Actual `eval_control.jsonl`** (facts block removed) showing regression
  - At least 1 question failed in control
  - Proves facts block is essential
- **Per-section breakdown** showing which section dominates

**Why the difference:** Tests verify reduction logic. Artifacts prove reduction achieves goals AND facts block improves accuracy.

### System 3: E-Commerce Claude Code Config

❌ NOT Sufficient:
- "All 35 tests passed"
- "Validator shows OK"
- "Config hierarchy is valid"

✅ IS Sufficient:
- **Actual `.claude/` structure** mirrored in evidence
  - `.claude/standards/` with all files
  - `.claude/rules/` with path-scoped rules
  - `.claude/commands/` with commands
  - `.claude/skills/` with skills
- **Actual `SKILL.md`** showing:
  - `context: fork` enforcement
  - `allowed-tools:` allowlist (read-only constraints)
- **Actual path-scoped rule globs** that work
  - Example: `paths: src/api/**` (show files that match)
- **Actual validator output** printing `OK` (not just "tests pass")

**Why the difference:** Tests verify code about config. Validator confirms config structure is correct. Together they prove configuration works.

### System 4: Multi-Shift Quality Monitoring

❌ NOT Sufficient:
- "All 33 tests passed"
- "Test assertions verify warm-tier filtering"
- "Hot state is constrained"
- "Recovery logic is sound"

✅ IS SUFFICIENT:
- **Actual `hot_state.json`** file from run
  - Real byte size: 2,847 bytes (not "small")
  - Provably under 5KB budget (quote the bytes)
  - Shows state actually stayed bounded in practice
- **Actual SQL query** showing filtering:
  - Quote: `SELECT ... WHERE filed_at > now() - interval '7 days' LIMIT 100`
  - Proves query has WHERE clause AND LIMIT clause
  - Output: actual run shows "100 defects returned" (not 50,000+)
- **Actual run output** showing:
  - Warm tier queried (LIMIT returned 100)
  - Hot state updated (file written)
  - Orchestration completed
- **Actual `shift_scratchpad.jsonl`** if fork path triggered
  - Proves fork isolation worked
- **Recovery logic quote** from code showing staleness threshold
  - Line: `if state_age > 86400: fresh_start()` (24 hour threshold)

**Why the difference:** Tests verify orchestration logic. Artifacts prove:
- SQL query actually filters (not just has a LIMIT clause in code)
- Hot state actually stays under budget (not just in theory)
- Fork actually isolates scratchpad (not just configured)
- Recovery actually chooses fresh vs. resume correctly

---

## The Pass/Fail Conditions (From User Specification)

### System 1
- ❌ Test output for the orchestration suite passes
- ✅ A run artifact shows claims routed to correct destinations
- ✅ Submitted evidence shows actual traces with stop_reason sequences
- ❌ The reflection fully explains the loop logic

### System 2
- ❌ Test output for the context suite passes
- ✅ A run artifact shows token reduction achieved (budget.json)
- ✅ Submitted evidence shows eval_control regression proving facts block necessity
- ❌ The reflection fully explains the reduction strategy

### System 3
- ❌ Test output passes AND validator shows OK
- ✅ A run artifact shows `.claude/` structure validated
- ✅ Submitted evidence shows path-scoped rules apply correctly
- ❌ The reflection fully explains the configuration hierarchy

### System 4
- ❌ Test output for the orchestration suite passes
- ✅ A run artifact shows SQL-filtered defects (not full-history loading)
- ✅ Submitted evidence shows hot_state.json under size budget
- ❌ The reflection fully explains resume vs. fresh decision

---

## What Counts as Evidence per System

### System 1 (Claims Intake)

✅ Actual Artifacts:
- `runs/<timestamp>/traces/claim-01.jsonl` (real trace file)
- `runs/<timestamp>/queues/*.jsonl` (real routed claims)
- Token counts from actual run
- All 8 claims with actual outcomes

❌ Not Evidence:
- "29 tests passed"
- "test_loop.py verifies routing"
- "The loop should route correctly"

### System 2 (Retail Context)

✅ Actual Artifacts:
- `runs/<timestamp>/budget.json` (real file with baseline/assembled/reduction)
- `runs/<timestamp>/eval.jsonl` (real eval results: pass/fail)
- `runs/<timestamp>/eval_control.jsonl` (real control: regression proof)
- Per-section token breakdown (actual numbers)

❌ Not Evidence:
- "30 tests passed"
- "test_reducer.py confirms reduction"
- "The algorithm works correctly"

### System 3 (Claude Code Config)

✅ Actual Artifacts:
- Actual `.claude/` folder structure (mirrored in evidence)
- Copy of actual `SKILL.md` with `context: fork` visible
- Actual `allowed-tools:` list showing constraints
- Actual validator output printing `OK`
- Path-scoped rule glob patterns with examples

❌ Not Evidence:
- "35 tests passed"
- "Validator shows OK"
- "Config hierarchy is correct"

### System 4 (Multi-Shift Monitoring)

✅ Actual Artifacts:
- Actual `hot_state.json` file (not description of its contents)
- Byte size documented (actual number, not "small")
- Actual SQL query with LIMIT clause shown
- Actual run output showing filtered results
- Actual `shift_scratchpad.jsonl` if fork triggered
- Recovery code quote showing staleness threshold

❌ Not Evidence:
- "33 tests passed"
- "Test assertions verify budgets"
- "The state should stay small"
- "SQL filtering happens"

---

## Citation Examples

### Strong Citation (Evidence-Based)
> "From EVIDENCE/system-4-shift-monitor/data/shift-run-A/hot-state-analysis.md,
> the actual `hot_state.json` file from a real shift run was 2,847 bytes.
> The budget is 5KB (5,120 bytes). This proves hot state stays under budget
> for indefinite runs at 3 shifts/day. The SQL query (warm.py:34) has:
> `LIMIT 100` proving model sees only 100 of 50,000+ defects in warm tier."

**Why strong:** Uses actual artifacts with real numbers. Cites code line. Proves constraint works.

### Weak Citation (No Longer Acceptable)
> "The tests for hot-state budgeting pass, confirming that the budget
> constraint works correctly. The reduction algorithm is sound and should
> keep state small indefinitely."

**Why weak:** Cites tests, not artifacts. Makes claim without proof. No actual numbers.

---

## The Complete Workflow

### Step 1: Pass All Tests
```bash
pytest tests/ -v                    # System 1-4
python -m ecommerce_team_config .   # System 3 only
```
✅ All must pass with exit code 0

❌ If any fail → STOP. Fix code. Do not proceed to Step 2.

### Step 2: Run Systems End-to-End
```bash
python -m claims_intake.run --all                   # System 1
python -m retail_context.run --all                  # System 2
python -m ecommerce_team_config .                   # System 3 (run again for output)
python -m shift_monitor run-shift ... --recorded-response ... # System 4
```

### Step 3: Capture Artifacts (Not Tests)
```
DO capture:
- runs/<timestamp>/traces/*.jsonl
- budget.json, eval.jsonl, eval_control.jsonl
- .claude/ folder structure
- hot_state.json, shift_scratchpad.jsonl

DO NOT capture:
- "tests passed" summaries
- Descriptions of what should happen
- Explanations of how code works
```

### Step 4: Organize in Evidence Folder
```
EVIDENCE/system-N-*/
├── [actual artifacts from Step 3]
└── [your analysis of those artifacts with code quotes]
```

### Step 5: Cite in Reflection Brief
```
Question N:
Answer: From EVIDENCE/system-X/.../filename.md, [actual data from artifact].
This proves [architectural decision] works because [metric from artifact].
Code reference: filename.py:linenum.
```

---

## The Bottom Line

| What | Is It Sufficient Evidence? | Why? |
|-----|----------------------------|-----|
| All 29 tests passed | ❌ NO | Tests verify code, not proof design works |
| Actual trace showing routing | ✅ YES | Proves loop routes claims correctly |
| "Reduction should work" | ❌ NO | No proof. Where's the actual tokens reduced? |
| `budget.json` showing 60% reduction | ✅ YES | Real numbers proving goal achieved |
| "Validator shows OK" | ❌ NO | Tests verify code. Where's config proof? |
| Actual `.claude/` structure + validator output | ✅ YES | Config hierarchy validated and demonstrated |
| "Hot state is constrained" | ❌ NO | No proof. What's the actual byte size? |
| `hot_state.json` at 2,847 bytes | ✅ YES | Real file proving budget met |
| "Tests confirm SQL filters work" | ❌ NO | Tests verify code. Did it actually filter? |
| Run output: "100 defects returned" + SQL query shown | ✅ YES | Real output proving filtering works |

---

## Key Insight

**Evidence = Concrete artifacts from real runs proving architectural decisions work.**
**Tests = Prerequisites ensuring code is correct.**
**These are different. Both are necessary. Tests alone are not evidence.**

Your reflection brief defends architectural decisions. You can only defend them with proof. That proof is run artifacts, not test suites.
