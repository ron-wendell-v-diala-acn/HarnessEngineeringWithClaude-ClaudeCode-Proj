# Evidence Structure Guide — Aligned with Executable Project Trees

## Overview

This guide ensures your **evidence folder mirrors the actual runnable project structure**. The strongest evidence organization directly reflects the code paths and configuration files you're analyzing.

**Core principle:** If the validator checks `.claude/skills/deploy-check/SKILL.md`, your evidence about that skill should live in `EVIDENCE/.claude/skills/deploy-check/` with clear references to that exact path.

## Test Rigor — Tests are Prerequisite, Not Evidence

**CRITICAL: Read [EVIDENCE-VS-TESTS.md](EVIDENCE-VS-TESTS.md) first to understand the distinction.**

**Tests passing ≠ Evidence.** They're different things:
- **Tests passing:** Code compiles and runs correctly (prerequisite)
- **Evidence:** Run artifacts prove architectural decisions work (actual proof)

### Test Blockers (Hard Stops)

Test failures and validator errors are **non-negotiable prerequisites**:

- **"29 passed"** → ✅ Pass blocker. Proceed to evidence collection.
- **"28 passed, 1 failed"** → ❌ **BLOCKER.** Do not proceed. Fix tests.
- **"29 passed, 1 skipped"** → ❌ **BLOCKER** (unless reason documented). Fix tests.
- **"FAIL (2 problems)"** → ❌ **BLOCKER.** Validator did not pass. Fix config.
- **Exit code 1** → ❌ **BLOCKER.** Do not proceed. Debug and fix.

### Evidence Requirements (After Tests Pass)

Once tests pass, collect **actual run artifacts** that prove architectural decisions work:

✅ **System 1:** Actual traces showing stop_reason routing claims correctly
✅ **System 2:** Actual `budget.json` proving token reduction, `eval.jsonl` proving facts block improves accuracy
✅ **System 3:** Actual config structure validated, validator output showing `OK`
✅ **System 4:** Actual `hot_state.json` under budget, actual SQL results showing filtered defects (not full history)

### Why This Matters

- Tests prove code is correct. Artifacts prove design is correct.
- "Tests pass" doesn't prove the loop routes claims. Only traces prove that.
- "Tests pass" doesn't prove budgets are met. Only actual `hot_state.json` file size proves that.
- "Tests pass" doesn't prove SQL filtering works. Only actual results prove that.
- Narrative explanations support evidence; they don't replace it.

### NOT Acceptable

❌ "All tests passed" (without run artifacts)
❌ "Validator shows OK" (without `.claude/` structure demonstrating config hierarchy)
❌ "I understand why state stays small" (without `hot_state.json` file proving budget)
❌ "Tests confirm defects are filtered" (without actual SQL results showing filtered counts)
❌ "The design is sound because..." (without proof it works in practice)

---

## Directory Layout

```
cd15315-Claude-AI-Engineer-Harness-Engineering/
├── EVIDENCE/
│   ├── system-1-claims-intake/
│   ├── system-2-retail-context/
│   ├── system-3-claude-config/
│   ├── system-4-shift-monitor/
│   └── README.md  ← this guide
├── Build a Claims Intake Agent with a stop_reason-Driven Loop/
│   └── exercises/03-dynamic-decomposition/solution/  ← System 1
├── Engineer a Long-Conversation Context Strategy.../
│   └── 04-assemble-and-locate/solution/  ← System 2
├── Configure Claude Code for a Multi-Surface Monorepo Team/
│   └── 04-plan-mode-and-explore-decision-doc/solution/  ← System 3
└── Build a Multi-Shift Quality Monitoring System.../
    └── 04-fork-scratchpad/solution/  ← System 4
```

Each `EVIDENCE/system-N-*` folder exactly parallels its corresponding solution folder structure.

---

## System 1: Claims Intake Agent

**Project path:** `Build a Claims Intake Agent with a stop_reason-Driven Loop/exercises/03-dynamic-decomposition/solution/`

### Evidence Structure

```
EVIDENCE/system-1-claims-intake/
├── README.md                          ← overview of this system's evidence
├── pytest-run.txt                     ← full output: pytest tests/ -v
├── pytest-run-summary.md              ← parsed: test count, any failures
│
├── claims_intake/                     ← mirrors project/claims_intake/
│   ├── loop.md                        ← analysis of loop.py
│   ├── tools.md                       ← analysis of tools.py
│   ├── tracer.md                      ← analysis of tracer.py
│   └── session.md                     ← analysis of session.py
│
├── fixtures/                          ← mirrors project/fixtures/
│   └── claims/
│       ├── claim-trace-example.md     ← one claim trace analyzed (jsonl)
│       └── claim-outcomes-summary.md  ← table of all 8 claims + outcomes
│
├── runs/                              ← captures from: python -m claims_intake.run --all
│   ├── run-summary.md                 ← timestamp, claim counts, exit code
│   ├── traces/
│   │   ├── claim-01-trace.md          ← one trace with stop_reason sequence
│   │   └── claim-02-trace.md
│   └── queues/
│       └── routing-summary.md         ← overview of routed claims
│
└── tests/
    ├── test-antipatterns.md           ← which antipatterns does it check?
    ├── test-loop.md                   ← loop test analysis
    └── test-tools.md                  ← tool test analysis
```

### Test Requirement (Hard Blocker)

**`pytest tests/ -v` must show exactly 29 passed with exit code 0.**

If you see:
- ❌ `X failed` (any number) → BLOCKER. Do not proceed with evidence.
- ❌ Exit code 1 → BLOCKER. Do not proceed.
- ❌ `X skipped` (without documented reason) → BLOCKER.

Fix the test failures first. The project depends on passing test suites.

### Key Evidence Files

1. **pytest-run.txt** — full terminal output (unedited)
   - Capture: `pytest tests/ -v > pytest-run.txt 2>&1`
   - Must show: `29 passed`
   - Must have exit code 0

2. **pytest-run-summary.md** — parsed summary for clarity
   - Quote the test command
   - Final test count (must be exactly 29 passed)
   - List any skipped tests with reason
   - If any failure: STOP. This is a blocker.

3. **claims_intake/loop.md** — analyze `claims_intake/loop.py`
   - Where does it call `client.messages.create()`?
   - How does it check `stop_reason`?
   - Quote the decision logic (continue vs. stop)

4. **claims_intake/tools.md** — analyze `claims_intake/tools.py`
   - List all tools and their input schemas
   - Identify tool descriptions (how do they prevent misrouting?)
   - Quote one schema with `error` field

5. **runs/traces/claim-01-trace.md** — capture one actual trace
   - Save the `.jsonl` file from your run
   - Quote the `stop_reason` sequence (show 3+ turns)
   - Note final outcome and token count

6. **runs/queues/routing-summary.md** — analyze routed claims
   - Which queues received claims?
   - Quote one routed claim from a queue JSON

---

## System 2: Retail Support Context Strategy

**Project path:** `Engineer a Long-Conversation Context Strategy for a Retail Support Copilot/04-assemble-and-locate/solution/`

### Test Requirement (Hard Blocker)

**`pytest tests/ -v` must show exactly 30 passed with exit code 0.**

If you see anything other than `30 passed`, STOP. Do not proceed with evidence. Fix the failures first.

### Evidence Structure

```
EVIDENCE/system-2-retail-context/
├── README.md                          ← overview
├── pytest-run.txt                     ← full pytest output
├── pytest-run-summary.md              ← parsed: test count
│
├── retail_context/                    ← mirrors project/retail_context/
│   ├── assembler.md                   ← analysis of context assembly
│   ├── reducer.md                     ← analysis of token reduction
│   └── evaluator.md                   ← analysis of evaluation logic
│
├── data/                              ← mirrors project/data/
│   └── fixtures-summary.md            ← overview of fixture data
│
├── runs/                              ← captures from: python -m retail_context.run --all
│   ├── run-summary.md                 ← timestamp, run_id, exit code
│   │
│   ├── context/
│   │   ├── context-assembled.md       ← assembled context structure
│   │   └── context-sections.md        ← per-section analysis + token counts
│   │
│   ├── budget.json                    ← actual JSON from run
│   ├── budget-analysis.md             ← parsed budget.json
│   │   • baseline tokens
│   │   • assembled tokens
│   │   • reduction %
│   │   • per-section breakdown
│   │
│   ├── eval.jsonl                     ← actual eval results
│   ├── eval-analysis.md               ← pass count + question summaries
│   │
│   ├── eval_control.jsonl             ← control run (no facts block)
│   └── eval-control-analysis.md       ← comparison: which questions regressed?
│
└── tests/
    ├── test-assembler.md              ← what does test_assembler check?
    ├── test-reducer.md                ← token reduction test logic
    └── test-evaluator.md              ← eval test logic
```

### Key Evidence Files

1. **pytest-run-summary.md**
   - Test count (expect 30 passed)
   - Any assertion failures

2. **retail_context/reducer.md** — analyze `retail_context/` token reduction
   - Where is text summarized?
   - Where is it kept verbatim?
   - Quote the decision logic from the code

3. **runs/budget-analysis.md** — parse `budget.json`
   ```markdown
   - **Baseline tokens:** [from JSON]
   - **Assembled tokens:** [from JSON]
   - **Reduction:** [calculate %]
   - **Dominant section:** [which section is largest?]
   ```

4. **runs/eval-analysis.md** — parse `eval.jsonl`
   - How many questions passed?
   - Quote 2–3 questions and outcomes

5. **runs/eval-control-analysis.md** — compare to control
   - Run eval without facts block
   - Which questions regressed?
   - What does regression prove about the facts block?

---

## System 3: E-Commerce Team Claude Code Config

**Project path:** `Configure Claude Code for a Multi-Surface Monorepo Team/04-plan-mode-and-explore-decision-doc/solution/`

### Test & Validator Requirements (Hard Blockers)

**Both must pass, or evidence is incomplete:**

1. `pytest tests/ -v` must show exactly **35 passed** with exit code 0
   - If any fail: BLOCKER. Fix first.

2. `python -m ecommerce_team_config .` must print **OK** with exit code 0
   - If validator prints FAIL (even partial): BLOCKER. Fix first.
   - The validator is the source of truth for config correctness.

### Evidence Structure

```
EVIDENCE/system-3-claude-config/
├── README.md                          ← overview
├── pytest-run.txt                     ← full pytest output
├── pytest-run-summary.md              ← test count (expect 35 passed)
│
├── CLAUDE.md                          ← copy of project/CLAUDE.md
│
├── .claude/
│   │
│   ├── standards/
│   │   ├── README.md                  ← what are "standards"?
│   │   ├── frontend-analysis.md       ← analysis of standards/frontend.md
│   │   ├── api-analysis.md            ← analysis of standards/api.md
│   │   ├── database-analysis.md       ← analysis of standards/database.md
│   │   └── testing-analysis.md        ← analysis of standards/testing.md
│   │
│   ├── rules/
│   │   ├── README.md                  ← what are "path-scoped rules"?
│   │   ├── api-rule-analysis.md       ← analysis: path glob + enforcement
│   │   ├── react-rule-analysis.md     ← analysis: when does it apply?
│   │   └── tests-rule-analysis.md     ← analysis: path glob for test files
│   │
│   ├── commands/
│   │   └── review-analysis.md         ← analysis of /review command
│   │
│   └── skills/
│       └── deploy-check/
│           ├── SKILL.md               ← copy of project/SKILL.md
│           ├── skill-overview.md      ← what does it do?
│           ├── skill-context-fork.md  ← analysis of context: fork
│           └── skill-allowed-tools.md ← analysis of allowed-tools
│
└── validator-output.txt               ← output: python -m ecommerce_team_config .
```

### Key Evidence Files

1. **pytest-run-summary.md**
   - Test count (expect 35 passed)
   - Any failures

2. **.claude/standards/README.md** — explain standards tier
   - What goes in standards vs. rules vs. skills?
   - Quote the scope table from project/CLAUDE.md

3. **.claude/rules/api-rule-analysis.md** — analyze one rule
   - Quote the glob frontmatter (e.g., `paths: src/api/**`)
   - When does this rule activate?
   - What guidance does it add?

4. **.claude/skills/deploy-check/skill-overview.md** — explain skill
   - Why is this a skill, not a CLAUDE.md addition?
   - Quote the `context: fork` line
   - What does fork accomplish?

5. **.claude/skills/deploy-check/skill-allowed-tools.md** — analyze tools
   - Quote the `allowed-tools:` list
   - Why are these sufficient? What's deliberately excluded?
   - Quote one `Bash(git ...)` constraint

6. **validator-output.txt** — capture validator run
   - Command: `python -m ecommerce_team_config .`
   - Full output showing OK and conformance

---

## System 4: Multi-Shift Quality Monitoring

**Project path:** `Build a Multi-Shift Quality Monitoring System with Claude Orchestration/04-fork-scratchpad/solution/`

### Test Requirement (Hard Blocker)

**`pytest tests/ -v` must show exactly 33 passed with exit code 0.**

If you see anything other than `33 passed`, STOP. Do not proceed with evidence. Fix the failures first.

### Evidence Structure

```
EVIDENCE/system-4-shift-monitor/
├── README.md                          ← overview
├── pytest-run.txt                     ← full pytest output
├── pytest-run-summary.md              ← test count (expect 33 passed)
│
├── shift_monitor/                     ← mirrors project/shift_monitor/
│   ├── orchestration.md               ← analysis of orchestration layer
│   ├── warm-store.md                  ← analysis of WarmStore (warm tier)
│   ├── hot-state.md                   ← analysis of hot state management
│   ├── recovery.md                    ← analysis of crash recovery logic
│   └── scratchpad.md                  ← analysis of scratchpad (fork state)
│
├── fixtures/                          ← mirrors project/fixtures/
│   ├── defects-summary.md             ← overview of defects.json
│   └── recorded-responses/
│       └── response-sample.md         ← one recorded API response
│
├── data/                              ← evidence of actual runs
│   ├── warm-db-schema.md              ← warm.sqlite structure
│   │
│   ├── shift-run-A/
│   │   ├── shift-output.txt           ← stdout from: python -m shift_monitor run-shift
│   │   ├── hot-state.json             ← captured hot_state.json (with byte size)
│   │   ├── hot-state-analysis.md      ← structure + size analysis
│   │   └── shift-summary.md           ← parsing shift output
│   │
│   ├── shift-run-B/
│   │   ├── shift-output.txt
│   │   ├── hot-state.json
│   │   └── hot-state-analysis.md
│   │
│   └── shift-scratchpad.jsonl          ← captured scratchpad from run
│
└── tests/
    ├── test-orchestration.md          ← what does orchestration test check?
    ├── test-recovery.md               ← crash recovery test logic
    └── test-state-bounds.md           ← state size constraints
```

### Key Evidence Files

1. **pytest-run-summary.md**
   - Test count (expect 33 passed)
   - Any failures

2. **shift_monitor/warm-store.md** — analyze WarmStore
   - Quote the indexed SQL query
   - Why does it limit returned defects?
   - What does this accomplish for the model?

3. **shift_monitor/hot-state.md** — analyze hot state management
   - What lives in hot state?
   - Why must it stay small?
   - Quote any size constraints from code

4. **shift_monitor/recovery.md** — analyze crash recovery
   - Quote the staleness threshold from `recovery.py`
   - When does it choose "fresh" vs. "resume"?
   - Why is fresh sometimes more reliable?

5. **data/shift-run-A/hot-state-analysis.md** — capture actual run
   - Actual byte size of your `hot_state.json`
   - Quote the structure (what fields?)
   - Why does byte budget matter for infinite runs?

6. **data/shift-run-A/shift-summary.md** — parse shift output
   - Shift identifier
   - Summary output
   - Defect counts
   - Exit status

7. **shift_monitor/scratchpad.md** — analyze fork scratchpad
   - Quote `context: fork` if it's used
   - Why isolate scratchpad in a fork?
   - How large can scratchpad grow?

---

## Alignment Checklist

### Critical Blockers (Must Pass Before Evidence Collection)

- 🔴 **System 1 tests:** `pytest tests/ -v` shows exactly **29 passed** with exit code 0
  - ANY failure → BLOCKER. Do not collect evidence. Fix the code first.
- 🔴 **System 2 tests:** `pytest tests/ -v` shows exactly **30 passed** with exit code 0
  - ANY failure → BLOCKER. Do not collect evidence. Fix the code first.
- 🔴 **System 3 tests:** `pytest tests/ -v` shows exactly **35 passed** with exit code 0
  - AND validator shows **OK**: `python -m ecommerce_team_config .` exits 0
  - ANY test failure → BLOCKER. Validator FAIL → BLOCKER. Fix first.
- 🔴 **System 4 tests:** `pytest tests/ -v` shows exactly **33 passed** with exit code 0
  - ANY failure → BLOCKER. Do not collect evidence. Fix the code first.

**Rationale:** Evidence proves systems work. If tests don't pass, the system doesn't work. No amount of narrative explanation substitutes for passing test suites.

### Structure Verification (After Tests Pass)

- ✅ **Path mirroring:** Every evidence file about `project/X/Y.py` has a corresponding `EVIDENCE/system-N/X/Y.md`
- ✅ **File references:** All evidence documents quote actual file paths and line numbers where relevant
- ✅ **Artifact capture:** Actual run artifacts (traces, budgets, outputs) are saved with minimal editing (no edits to pytest, JSON, traces)
- ✅ **Analysis precision:** Your analysis cites exact code locations, not just high-level summaries
- ✅ **Validator alignment:** For System 3, your evidence structure validates against the `.claude/` hierarchy you're analyzing
- ✅ **Test coverage:** You've documented which test file covers which behavior

---

## Quick Start: Building Your EVIDENCE Folder

1. **Create the base structure:**
   ```bash
   mkdir -p EVIDENCE/system-{1,2,3,4}-*
   cp EVIDENCE-STRUCTURE.md EVIDENCE/README.md
   ```

2. **For each system:**
   - Copy this guide to `EVIDENCE/system-N-*/README.md`
   - Build subdirectories that match project structure
   - Capture artifacts from runs
   - Write analysis documents referencing exact file paths

3. **Validate alignment:**
   - For each evidence file, confirm the corresponding project file exists
   - Use file paths consistently throughout (e.g., `claims_intake/loop.py:42`)
   - Cross-check with validator output (System 3) and test output (all systems)

---

## Example: Good vs. Bad Evidence Path Alignment

### ❌ Weak alignment
```
EVIDENCE/system-3-claude-config/
└── skill_deploy_check.md        ← Generic name, doesn't mirror project structure
```

**Problem:** Where in the project is this skill? Readers must guess or search.

### ✅ Strong alignment
```
EVIDENCE/system-3-claude-config/
└── .claude/
    └── skills/
        └── deploy-check/
            ├── SKILL.md                ← Copy of actual file for reference
            ├── skill-overview.md       ← What does it do?
            ├── skill-context-fork.md   ← Analysis of context: fork feature
            └── skill-allowed-tools.md  ← Analysis of allowed-tools
```

**Strength:** Anyone reading evidence can immediately locate project file at `.claude/skills/deploy-check/SKILL.md`.

---

## Using Evidence in the Reflection Brief

When you fill in `reflection-brief-template.md`, cite evidence like this:

> "The `stop_reason` sequence in System 1 shows [turns to routing decision]. See `EVIDENCE/system-1-claims-intake/runs/traces/claim-01-trace.md` and the trace excerpt from `claims_intake/loop.py:42`."

**Pattern:** `EVIDENCE/system-N-*/[project-subpath]/[analysis-file].md`

This keeps evidence and reflection connected and verifiable.
