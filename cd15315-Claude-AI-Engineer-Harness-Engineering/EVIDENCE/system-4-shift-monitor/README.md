# System 4 Evidence: Multi-Shift Quality Monitoring

**Project:** `Build a Multi-Shift Quality Monitoring System with Claude Orchestration/04-fork-scratchpad/solution/`

**Run commands:**
```bash
pytest tests/ -v                       # expect 33 passed
# Seed warm tier once
python -c "import json; from pathlib import Path; from shift_monitor.warm import WarmStore; \
w=WarmStore(Path('data/warm.sqlite')); w.initialize(); \
w.insert_many(json.load(open('fixtures/defects.json')))"

# Run shift offline (recorded response, no API spend)
python -m shift_monitor run-shift --shift C --warm-db data/warm.sqlite \
  --recorded-response fixtures/recorded_responses/shift_C_2026-04-30.json
```

## ⛔ Important: Tests Passing ≠ Evidence

**Before you collect evidence, understand the difference:**

- **Tests passing (33 passed)** = prerequisite. Code is correct. ✅ Required.
- **Run artifacts** = actual evidence. Proves SQL filters defects, hot state stays under budget, fork isolates scratchpad, etc.

Read [../../EVIDENCE-VS-TESTS.md](../../EVIDENCE-VS-TESTS.md) to understand what counts as real evidence.

### Test Blocker

**`pytest tests/ -v` MUST show exactly 33 passed with exit code 0.**

If you see:
- ❌ `32 passed, 1 failed`
- ❌ Any test failure
- ❌ Exit code 1

**STOP.** Fix the test failures first.

### Evidence Requirements (After Tests Pass)

Don't just collect test output. Collect **actual run artifacts** that prove the orchestration works:

- ✅ **Actual `hot_state.json`** from real shift run showing byte size under budget
- ✅ **Actual SQL query output** showing LIMIT clause returns limited defects (not full history)
- ✅ **Actual run output** showing orchestration succeeded and state was bounded
- ✅ **Actual `shift_scratchpad.jsonl`** (if fork path triggered) showing isolation
- ✅ **Proof that warm-tier filters work** (quote the indexed query with WHERE and LIMIT)

These artifacts prove warm-tier filtering and hot-state budgeting actually work. Test passing alone doesn't prove that.

**Critical Example:** "Test passes" doesn't prove the model never saw 50,000 defects. Only actual run output showing "100 defects returned" proves it.

---

## What to Capture

### 1. Test Evidence
- **`pytest-run.txt`** — Full output from `pytest tests/ -v`
- **`pytest-run-summary.md`** — Parsed summary:
  - Total test count (should be 33)
  - Any assertion failures
  - Key test modules: orchestration, warm store, hot state, recovery, scratchpad

### 2. Code Analysis

#### `shift_monitor/orchestration.md`
Analyze the orchestration layer. Answer:
- **File:** `shift_monitor/orchestration.py` (or equivalent)
- **Entry point:** Quote the function that starts a shift
- **Layer responsibilities:** What decisions does orchestration make vs. delegating?
- **State flow:** How does it move from warm → hot → scratchpad?
- **Model interaction:** Quote the call to `client.messages.create()` and what context it passes

#### `shift_monitor/warm-store.md`
Analyze the warm-tier database. Answer:
- **File:** `shift_monitor/warm.py` (or equivalent)
- **Storage:** SQLite warm.sqlite or equivalent?
- **Core query:** Quote the indexed SQL query that fetches defects
  - Look for `SELECT ... WHERE` with LIMIT, ORDER BY, or WHERE on timestamp
  - Quote the query exactly
- **Why limit results?** "The model never sees the full history because..."
  - Budget? Query returns top-N most relevant/recent?
- **Proof:** Show how query result count is limited (e.g., `LIMIT 20`)

#### `shift_monitor/hot-state.md`
Analyze the hot-state (in-memory state). Answer:
- **File:** `shift_monitor/hot.py` or location of state definition
- **State shape:** What fields track shift status? Quote the type/class
- **Size constraint:** Is there a byte budget? Quote any MAX_SIZE or memory limit
- **Purpose:** Why keep state small and in-memory?
- **Update pattern:** When and how is hot state written?

#### `shift_monitor/recovery.md`
Analyze crash recovery. Answer:
- **File:** `shift_monitor/recovery.py` (or equivalent)
- **Resume vs. fresh decision:** Quote the code that chooses
- **Staleness threshold:** How old can state be before forced fresh start? Quote the constant/logic
- **Why fresh sometimes better:** "A fresh start with injected summary is more reliable when..."
  - Example: if state is >24 hours old, more defects have been filed, old state is misleading
- **Proof:** Show the comparison logic

#### `shift_monitor/scratchpad.md`
Analyze scratchpad (fork-isolated working memory). Answer:
- **File:** `shift_monitor/scratchpad.py` (or equivalent)
- **Purpose:** Why does orchestration fork and give model a scratchpad?
- **Isolation:** What stays in scratchpad vs. what returns to hot state?
- **Growth:** Can scratchpad grow unbounded? Is there a size check?
- **Proof:** Quote how fork + scratchpad works in the orchestration flow

### 3. Run Evidence

#### `fixtures/defects-summary.md`
From `fixtures/defects.json`:
- **Structure:** How many defects in test data?
- **Schema:** What fields does each defect have? (id, severity, description, timestamp, etc.)
- **Sample:** Quote one defect record
- **Purpose:** What fixtures test against?

#### `fixtures/recorded-responses/response-sample.md`
From `fixtures/recorded_responses/shift_C_2026-04-30.json`:
- **Structure:** What does a recorded API response look like?
- **Batches:** How many response batches? (If the model made multiple RPC calls)
- **Sample:** Quote one model response
- **Purpose:** Allows offline testing without API spend

#### `data/warm-db-schema.md`
Document the warm.sqlite schema:
```sql
-- From: shift_monitor/warm.py or docs
CREATE TABLE defects (
    id INTEGER PRIMARY KEY,
    severity TEXT,
    description TEXT,
    filed_at TIMESTAMP,
    ...
);
CREATE INDEX idx_filed_at ON defects(filed_at);
```
- **Tables:** What tables exist?
- **Indexes:** Which fields are indexed? Why?
- **Foreign keys:** Any relationships?

#### `data/shift-run-A/shift-output.txt`
Capture full stdout from:
```bash
python -m shift_monitor run-shift --shift C --warm-db data/warm.sqlite \
  --recorded-response fixtures/recorded_responses/shift_C_2026-04-30.json
```

#### `data/shift-run-A/hot-state.json`
Save the actual `hot_state.json` file from your run into evidence.

#### `data/shift-run-A/hot-state-analysis.md`
Analyze the captured hot_state.json:
```markdown
## Hot State Analysis

**From:** `data/shift-run-A/hot_state.json`

**Byte size:** [actual size in bytes]
**Encoded size:** [size of JSON string]

**Structure:**
```json
{
  "shift_id": "C",
  "defects_reviewed": [...],
  "high_priority_count": 42,
  "summary": "..."
}
```

**Key fields:**
- `shift_id`: Identifies which shift
- `defects_reviewed`: Count or list? Max size?
- `high_priority_count`: How many defects triggered alerts?
- `summary`: Human-readable summary or machine format?

**Size analysis:**
- Why must this stay under [some limit]?
- What breaks if it grows too large?
- Proof: Quote from code comment or README

**Infinite-run implication:**
- This shift runs once per shift, indefinitely
- What happens if hot_state grows unbounded over 6 months? 1 year?
- Quote the byte budget enforcement
```

#### `data/shift-run-A/shift-summary.md`
Parse shift output:
```markdown
## Shift Summary

**Shift ID:** C
**Timestamp:** [from output]
**Status:** [OK / ERRORS / etc.]

**Defects processed:**
- Total reviewed: [from output]
- High priority: [from output]
- Escalated: [from output]

**Model interaction:**
- Calls to model: [if logged in output]
- Tokens used: [if logged]
- Context size: [if logged]

**Hot state:**
- Size after run: [see hot-state-analysis.md]
- New fields added: [any?]
- Pruned fields: [any?]

**Exit code:** 0 (success)
```

#### (Optional) `data/shift-run-B/...`
If you run a second shift (A, B, etc.):
- Repeat structure above
- Compare hot-state sizes and recovery behavior
- Show state evolution across runs

---

## Test Analysis

#### `tests/test-orchestration.md`
Brief analysis:
- **File:** `tests/test_orchestration.py` (or part of integration tests)
- **Key assertions:** What does orchestration test verify?
  - State transitions?
  - Model interaction?
  - Fork usage?
- **Quote one:** Show a key test
- **Purpose:** Why test orchestration separately?

#### `tests/test-recovery.md`
Brief analysis:
- **File:** `tests/test_recovery.py`
- **Key scenarios:** What recovery cases does it test?
  - Fresh start behavior?
  - Resume staleness?
  - State injection?
- **Quote one:** Show a recovery test
- **Proof:** How does test guarantee reliability?

#### `tests/test-state-bounds.md`
Brief analysis:
- **File:** `tests/` (may be part of orchestration or warm tests)
- **Key assertions:** What byte/size limits are enforced?
  - hot_state.json max size?
  - warm query result limit?
  - scratchpad max growth?
- **Quote one:** Show a bounds test
- **Purpose:** Why does size matter?

---

## Alignment Checklist

- ✅ `shift_monitor/*.md` files reference actual code files with line numbers
- ✅ `shift_monitor/warm-store.md` quotes actual SQL from the project
- ✅ `data/shift-run-A/hot-state.json` is the actual artifact from your run (not edited)
- ✅ `data/shift-run-A/hot-state-analysis.md` analyzes JSON structure with byte sizes
- ✅ `data/shift-run-A/shift-output.txt` is captured directly from terminal
- ✅ `fixtures/` evidence mirrors project fixture structure
- ✅ Test analyses reference actual test file paths
- ✅ Recovery analysis quotes actual staleness thresholds from code

---

## Example Citation in Reflection Brief

When answering question #11 (*Push work down. Defects the SQL query returned vs warm-tier total*):

> "From EVIDENCE/system-4-shift-monitor/shift_monitor/warm-store.md, the indexed SQL query is `SELECT * FROM defects WHERE filed_at > now() - interval '7 days' ORDER BY severity DESC LIMIT 100`. The warm tier has 50,000+ defects total, but the query returns only the 100 most recent high-severity defects. The model never sees the full history because the query is limited, pushing work down to the database."

When answering question #12 (*Crash recovery*):

> "From EVIDENCE/system-4-shift-monitor/shift_monitor/recovery.md, the staleness threshold is 24 hours (see recovery.py line 34: `STALE_THRESHOLD = 86400`). If state is older than 24h, the system forces a fresh start with an injected summary rather than resuming. This is more reliable because old state becomes misleading as new defects arrive; a fresh analysis of recent defects is better than relying on stale tracking."

When answering question #13 (*Small state*):

> "From EVIDENCE/system-4-shift-monitor/data/shift-run-A/hot-state-analysis.md, the actual hot_state.json was 2,847 bytes. The budget matters because this system runs once per shift indefinitely — if hot state grew to 1 MB per shift, after 6 months of 3 shifts/day we'd have 540 MB of accumulated state. Keeping it <5KB means infinite runs are scalable."

---

## File Reference Summary

| Evidence File | Project File | Purpose |
|---------------|--------------|---------|
| `pytest-run-summary.md` | `tests/test_*.py` | Parse test results |
| `shift_monitor/orchestration.md` | `shift_monitor/orchestration.py` | Orchestration layer |
| `shift_monitor/warm-store.md` | `shift_monitor/warm.py` | Warm tier (indexed query) |
| `shift_monitor/hot-state.md` | `shift_monitor/hot.py` | Hot state shape + size |
| `shift_monitor/recovery.md` | `shift_monitor/recovery.py` | Crash recovery logic |
| `shift_monitor/scratchpad.md` | `shift_monitor/scratchpad.py` | Fork-isolated state |
| `fixtures/defects-summary.md` | `fixtures/defects.json` | Test data overview |
| `fixtures/recorded-responses/response-sample.md` | `fixtures/recorded_responses/` | Recorded API responses |
| `data/warm-db-schema.md` | `shift_monitor/warm.py` or docs | SQLite schema |
| `data/shift-run-A/shift-output.txt` | (run stdout) | Terminal output |
| `data/shift-run-A/hot-state.json` | `data/hot_state.json` | Actual run artifact |
| `data/shift-run-A/hot-state-analysis.md` | `data/shift-run-A/hot-state.json` | Size + structure analysis |
| `data/shift-run-A/shift-summary.md` | (parsed from output) | Shift results |
| `tests/test-orchestration.md` | `tests/test_*.py` | Orchestration tests |
| `tests/test-recovery.md` | `tests/test_*.py` | Recovery tests |
| `tests/test-state-bounds.md` | `tests/test_*.py` | Size constraint tests |

---

## Reflection Brief Citations

System 4 questions:
- **#11 (Push work down)** → `shift_monitor/warm-store.md` (quote SQL + LIMIT)
- **#12 (Crash recovery)** → `shift_monitor/recovery.md` (staleness threshold)
- **#13 (Small state)** → `data/shift-run-A/hot-state-analysis.md` (byte size)

And for synthesis questions that reference System 4:
- **#14 (Three layers)** → `shift_monitor/orchestration.md` (model layer)
- **#16 (Context, two faces)** → `shift_monitor/hot-state.md` (cross-session context)
