# System 1 Evidence: Claims Intake Agent

**Project:** `Build a Claims Intake Agent with a stop_reason-Driven Loop/exercises/03-dynamic-decomposition/solution/`

**Run commands:**
```bash
pytest tests/ -v                       # expect 29 passed
python -m claims_intake.run --all      # processes 8 claim fixtures
```

## ⛔ Important: Tests Passing ≠ Evidence

**Before you collect evidence, understand the difference:**

- **Tests passing (29 passed)** = prerequisite. Code is correct. ✅ Required.
- **Run artifacts** = actual evidence. Proves loop routes claims correctly, tools work, etc.

Read [../../EVIDENCE-VS-TESTS.md](../../EVIDENCE-VS-TESTS.md) to understand what counts as real evidence.

### Test Blocker

**`pytest tests/ -v` MUST show exactly 29 passed with exit code 0.**

If you see:
- ❌ `28 passed, 1 failed`
- ❌ `29 passed, 1 skipped` (without documented reason)
- ❌ Exit code 1

**STOP.** Fix the test failures first.

### Evidence Requirements (After Tests Pass)

Don't just collect test output. Collect **actual run artifacts** that prove the loop works:

- ✅ **Actual trace** from `runs/<timestamp>/traces/claim-01.jsonl` showing stop_reason sequence
- ✅ **Actual claim routed** to queue from `runs/<timestamp>/queues/*.jsonl`
- ✅ **Actual token counts** from the real run (not theoretical)
- ✅ **All 8 claims** successfully routed to correct destinations

These artifacts prove the loop actually routes claims. Test passing alone doesn't prove that.

---

## What to Capture

### 1. Test Evidence
- **`pytest-run.txt`** — Full terminal output from `pytest tests/ -v`
- **`pytest-run-summary.md`** — Parsed summary:
  - Total test count (should be 29)
  - Any assertion failures
  - Key test names: `test_loop`, `test_tools`, `test_antipatterns`

### 2. Code Analysis

#### `claims_intake/loop.md`
Point to exactly where the agentic loop lives. Answer:
- **File:** `claims_intake/loop.py`
- **Core function:** Quote the function that calls `client.messages.create()`
- **Stop-reason check:** Quote the exact code that decides continue vs. stop
- **Example:** "Line 42: `if response.stop_reason == 'end_turn': break`"

#### `claims_intake/tools.md`
Analyze tool design. Answer:
- **List all tools:** Claim classifier, router, escalator, etc.
- **Overlapping tools:** Which two have similar inputs? How do descriptions differ?
- **Structured errors:** Quote one tool with an `error` field in schema
- **Proof:** Show how structured error helped agent recover

#### `claims_intake/tracer.md`
Analyze how the system captures evidence. Answer:
- **Tracer class:** Where is it in the code?
- **What it captures:** Stop reason? Token usage? Tool calls?
- **Storage:** How are traces written to disk?

#### `claims_intake/session.md`
Analyze claim sessions. Answer:
- **Session class:** `claims_intake/session.py`
- **State tracking:** What fields track claim progress?
- **Routing:** How does a claim move from intake → routed queue?

### 3. Run Evidence

#### `runs/run-summary.md`
From your `python -m claims_intake.run --all` execution, capture:
- **Timestamp** of run
- **Exit code** (should be 0)
- **Claim count** processed (should be 8)
- **Claims routed** count
- **Claims escalated** count

#### `runs/traces/claim-01-trace.md`
Pick one claim from `runs/<timestamp>/traces/`:
1. Save the raw `.jsonl` file (referenced below)
2. In `.md`, extract and quote:
   - **Claim ID and description** (kitchen fire, stolen bike, etc.)
   - **Stop-reason sequence** — show at least 3–4 turns:
     ```
     Turn 1: stop_reason = "tool_use" (called classify_claim)
     Turn 2: stop_reason = "tool_use" (called route_claim)
     Turn 3: stop_reason = "end_turn" (ended, routed to home)
     ```
   - **Final outcome** (routed to which queue? escalated?)
   - **Total tokens** used for this claim

#### `runs/queues/routing-summary.md`
From `runs/<timestamp>/queues/`:
- **Queue names** discovered (home, auto, liability, etc.)
- **Claim counts** per queue (e.g., home: 3 claims, auto: 2 claims)
- **Quote one routed claim** from a queue JSON file showing:
  - Claim ID
  - Routing decision
  - Confidence if applicable

#### `fixtures/claims/claim-outcomes-summary.md`
Build a table of all 8 claim fixtures:

| Claim | Fixture | Expected Route | Your Outcome | Match? |
|-------|---------|-----------------|--------------|--------|
| 01 | Kitchen fire | home | home | ✅ |
| 02 | Stolen bike | property | property | ✅ |
| ... | ... | ... | ... | ... |

### 4. Test Analysis

#### `tests/test-antipatterns.py`
Quote the file name and answer:
- **What antipatterns does it test?** List 3–4 examples
- **Pick one:** Quote the test code that catches it
- **Impact:** If your loop used this antipattern, what would break in `claim-01-trace.md`?

#### `tests/test-loop.md`
Brief analysis:
- **Main assertions:** What does `test_loop.py` verify?
- **Quote one:** Show a key assertion (e.g., "assert stop_reason in ['tool_use', 'end_turn']")

#### `tests/test-tools.md`
Brief analysis:
- **What does `test_tools.py` verify?** Tool schemas? Error handling?
- **Quote one:** Show a key test

---

## Alignment Checklist

- ✅ `claims_intake/loop.md` references `claims_intake/loop.py` with line numbers
- ✅ `claims_intake/tools.md` quotes actual tool schemas from `claims_intake/tools.py`
- ✅ `runs/traces/claim-01-trace.md` corresponds to actual trace in `runs/<timestamp>/traces/`
- ✅ `runs/queues/routing-summary.md` matches actual queue structure from `runs/<timestamp>/queues/`
- ✅ Test analyses reference actual test file paths (`tests/test_*.py`)
- ✅ All code quotes include file and line number (e.g., `claims_intake/loop.py:42`)

---

## Example Citation in Reflection Brief

When answering reflection question #1 (*Loop control. Quote the `stop_reason` sequence from one trace*):

> "From EVIDENCE/system-1-claims-intake/runs/traces/claim-01-trace.md, the trace shows: Turn 1: `tool_use` (classify), Turn 2: `tool_use` (route), Turn 3: `end_turn` (complete). The decision logic is in `claims_intake/loop.py:42` where the loop checks `if response.stop_reason == 'end_turn': break`."

---

## File Reference Summary

| Evidence File | Project File | Purpose |
|---------------|--------------|---------|
| `pytest-run-summary.md` | `tests/test_*.py` | Parse test run results |
| `claims_intake/loop.md` | `claims_intake/loop.py` | Agentic loop mechanics |
| `claims_intake/tools.md` | `claims_intake/tools.py` | Tool design + schemas |
| `claims_intake/tracer.md` | `claims_intake/tracer.py` | Evidence capture |
| `claims_intake/session.md` | `claims_intake/session.py` | Claim state machine |
| `runs/traces/claim-01-trace.md` | `runs/<timestamp>/traces/` | Actual execution trace |
| `runs/queues/routing-summary.md` | `runs/<timestamp>/queues/` | Routing outcomes |
| `fixtures/claims/claim-outcomes-summary.md` | `fixtures/claims/` | All 8 fixture outcomes |
| `tests/test-antipatterns.md` | `tests/test_antipatterns.py` | Antipattern detection |

---

## Reflection Brief Citations

System 1 questions:
- **#1 (Loop control)** → `runs/traces/claim-01-trace.md` + `claims_intake/loop.md`
- **#2 (Anti-pattern)** → `tests/test-antipatterns.md`
- **#3 (Tool design)** → `claims_intake/tools.md`
- **#4 (Your numbers)** → `runs/traces/claim-01-trace.md` (token count + turns)
