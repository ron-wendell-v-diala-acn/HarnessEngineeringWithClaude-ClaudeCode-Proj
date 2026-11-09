# Evidence Folder — Harness Engineering Capstone

This folder holds evidence for the **Capstone: Harness Engineering** project. The goal is to build, run, and verify four systems, then write an evidence-grounded reflection brief.

## ⛔ Critical Distinction: Tests ≠ Evidence

### Read This First: [../EVIDENCE-VS-TESTS.md](../EVIDENCE-VS-TESTS.md)

**Tests passing is a prerequisite, not evidence.**

- **Tests passing:** "The code works correctly"
- **Evidence:** "The architectural decisions work in practice"

Examples:
- ❌ "29 tests passed" = NOT evidence
- ✅ "Trace shows stop_reason routing claims correctly" = evidence
- ❌ "30 tests passed" = NOT evidence
- ✅ "`budget.json` shows 60% token reduction achieved" = evidence
- ❌ "35 tests passed and validator shows OK" = NOT evidence
- ✅ "Actual deploy-check skill runs in fork and validator confirms config structure" = evidence
- ❌ "33 tests passed" = NOT evidence
- ✅ "`hot_state.json` shows 2,847 bytes (under 5KB budget)" = evidence

### Test Blockers (Non-Negotiable Prerequisites)

Before you collect ANY evidence for a system, verify:

| System | Blocker | Command |
|--------|---------|---------|
| **System 1** | 29 passed, exit 0 | `pytest tests/ -v` |
| **System 2** | 30 passed, exit 0 | `pytest tests/ -v` |
| **System 3** | 35 passed + validator OK | `pytest tests/ -v` AND `python -m ecommerce_team_config .` |
| **System 4** | 33 passed, exit 0 | `pytest tests/ -v` |

**If ANY test fails:**
- ❌ "28 passed, 1 failed" → BLOCKER
- ❌ "29 passed, 1 skipped" (undocumented) → BLOCKER
- ❌ Exit code 1 → BLOCKER
- ❌ "FAIL (2 problems)" → BLOCKER

**Action:** Fix the code. Do not collect evidence for failing runs. Narrative explanations for test failures don't substitute for working systems.

### Why This Matters

- **Evidence proves systems work.** It's not a report explaining why they don't.
- **Test suites are the source of truth.** They define correctness.
- **The project depends on passing runs.** Without them, reflection brief answers have no foundation.
- **Your detailed analysis is only meaningful when based on working code.**

### What This Doesn't Mean

- ❌ You can't learn from failures (of course you can)
- ❌ Test-driven development is bad (it's not — it's essential)
- ❌ Fixes don't require thought (they do)

What it means:
- ✅ Collect evidence only from passing runs
- ✅ Document test counts as proof of correctness
- ✅ Use passing evidence to support reflection brief answers
- ✅ If a run fails, fix it — don't explain it away

---

## Quick Start

1. **Read the structure guide:** Start with [../EVIDENCE-STRUCTURE.md](../EVIDENCE-STRUCTURE.md)
   - Explains the alignment principle: evidence mirrors project structure
   - Shows the folder layout for all four systems

2. **Pick a system:** Each has its own README with detailed guidance
   - [system-1-claims-intake/](system-1-claims-intake/) — Insurance Claims Intake Agent
   - [system-2-retail-context/](system-2-retail-context/) — Retail Support Context Strategy
   - [system-3-claude-config/](system-3-claude-config/) — E-Commerce Team Claude Code Config
   - [system-4-shift-monitor/](system-4-shift-monitor/) — Multi-Shift Quality Monitoring

3. **Build → Run → Capture evidence** for each system
   - Create venv, install, run pytest
   - Run the system end-to-end
   - Save artifacts (traces, budgets, configs, outputs)
   - Write analysis documents

4. **Fill the reflection brief** ([../Project-Harness%20Engineering%20with%20Claude%20and%20Claude%20Code/reflection-brief-template.md](../Project-Harness%20Engineering%20with%20Claude%20and%20Claude%20Code/reflection-brief-template.md))
   - Every answer cites evidence from your EVIDENCE/ folder
   - Reference format: `EVIDENCE/system-N-*/.../<file>.md`

---

## The Alignment Principle

**Strong evidence organization mirrors the executable project tree.**

### Example: System 3 (Claude Code Config)

**Project structure:**
```
Configure Claude Code for a Multi-Surface Monorepo Team/
└── 04-plan-mode-and-explore-decision-doc/solution/
    ├── CLAUDE.md                         ← Root config
    └── .claude/
        ├── standards/                    ← Always-loaded conventions
        │   ├── frontend.md
        │   ├── api.md
        │   ├── database.md
        │   └── testing.md
        ├── rules/                        ← Path-scoped rules
        │   ├── api.md
        │   ├── react.md
        │   └── tests.md
        ├── commands/                     ← On-demand commands
        │   └── review.md
        └── skills/                       ← On-demand, forked skills
            └── deploy-check/
                └── SKILL.md
```

**Evidence structure:**
```
EVIDENCE/system-3-claude-config/
├── README.md                             ← This system's evidence guide
├── CLAUDE.md                             ← Copy of project file (reference)
├── root-claude-overview.md               ← Analysis of CLAUDE.md
├── validator-output.txt                  ← Run output (proof)
│
├── .claude/
│   ├── standards/                        ← Mirrors project structure
│   │   ├── README.md                     ← Explain "standards" tier
│   │   ├── frontend-analysis.md          ← Analyze frontend.md
│   │   ├── api-analysis.md
│   │   ├── database-analysis.md
│   │   └── testing-analysis.md
│   │
│   ├── rules/                            ← Mirrors project structure
│   │   ├── README.md                     ← Explain "path-scoped rules"
│   │   ├── api-rule-analysis.md          ← Analyze api.md (with glob)
│   │   ├── react-rule-analysis.md
│   │   └── tests-rule-analysis.md
│   │
│   ├── commands/
│   │   └── review-analysis.md            ← Analyze /review command
│   │
│   └── skills/
│       └── deploy-check/
│           ├── SKILL.md                  ← Copy of actual file
│           ├── skill-overview.md         ← What does it do?
│           ├── skill-context-fork.md     ← Analysis of context: fork
│           ├── skill-allowed-tools.md    ← Analysis of tool allowlist
│           └── skill-checks.md           ← Analysis of the 3 checks
│
└── pytest-run-summary.md                 ← Test results
```

**Benefit:** A reader looking at evidence can immediately find the project file. E.g., "Want to verify the deploy-check skill analysis? Look at `.claude/skills/deploy-check/SKILL.md` in the project."

---

## Per-System Structure

### System 1: Claims Intake Agent
```
system-1-claims-intake/
├── README.md                    ← Detailed guidance
├── pytest-run-summary.md
├── claims_intake/               ← Mirrors project module
│   ├── loop.md
│   ├── tools.md
│   ├── tracer.md
│   └── session.md
├── fixtures/claims/
│   ├── claim-trace-example.md
│   └── claim-outcomes-summary.md
├── runs/                        ← From actual execution
│   ├── run-summary.md
│   ├── traces/
│   │   └── claim-01-trace.md
│   └── queues/
│       └── routing-summary.md
└── tests/
    ├── test-antipatterns.md
    ├── test-loop.md
    └── test-tools.md
```

### System 2: Retail Support Context
```
system-2-retail-context/
├── README.md
├── pytest-run-summary.md
├── retail_context/              ← Mirrors project module
│   ├── assembler.md
│   ├── reducer.md
│   └── evaluator.md
├── data/fixtures-summary.md
├── runs/                        ← From actual execution
│   ├── run-summary.md
│   ├── context/
│   │   ├── context-assembled.md
│   │   └── context-sections.md
│   ├── budget.json              ← Actual artifact
│   ├── budget-analysis.md       ← Analysis of JSON
│   ├── eval.jsonl               ← Actual artifact
│   ├── eval-analysis.md
│   ├── eval_control.jsonl       ← Actual artifact
│   └── eval-control-analysis.md
└── tests/
    ├── test-assembler.md
    ├── test-reducer.md
    └── test-evaluator.md
```

### System 3: Claude Code Config
See above — mirrors `.claude/` hierarchy.

### System 4: Multi-Shift Quality Monitoring
```
system-4-shift-monitor/
├── README.md
├── pytest-run-summary.md
├── shift_monitor/               ← Mirrors project module
│   ├── orchestration.md
│   ├── warm-store.md
│   ├── hot-state.md
│   ├── recovery.md
│   └── scratchpad.md
├── fixtures/
│   ├── defects-summary.md
│   └── recorded-responses/
│       └── response-sample.md
├── data/
│   ├── warm-db-schema.md
│   ├── shift-run-A/
│   │   ├── shift-output.txt     ← Captured stdout
│   │   ├── hot-state.json       ← Actual artifact
│   │   ├── hot-state-analysis.md
│   │   └── shift-summary.md
│   └── shift-run-B/             ← (optional second run)
│       └── ...
└── tests/
    ├── test-orchestration.md
    ├── test-recovery.md
    └── test-state-bounds.md
```

---

## What "Evidence" Means

Evidence files come in three types:

### 1. **Artifact Captures**
Raw outputs from running the system:
- Test run output (pytest terminal output)
- Execution traces (JSONL files from runs)
- JSON budget/state files
- Configuration file copies
- Terminal output from validators

**Pattern:** `<run-identifier>.txt`, `*.json`, `*.jsonl`

### 2. **Analysis Documents**
Markdown files that explain what the code/artifact does:
- Parse a JSON artifact and explain its fields
- Quote code with line numbers
- Show how decisions are made
- Compare two runs or a main vs. control

**Pattern:** `*-analysis.md`, `*-overview.md`

### 3. **Test Summaries**
Parsed pytest output showing what test suite verified:
- Total test count
- Which test modules ran
- Key assertions
- Any failures

**Pattern:** `pytest-run-summary.md`, `test-*.md`

---

## Citation Pattern for Reflection Brief

When answering a reflection question, cite evidence like this:

**Format:**
```
See EVIDENCE/system-N-*/<path>/<filename>.md
```

**Examples:**

> "The `stop_reason` sequence is in `EVIDENCE/system-1-claims-intake/runs/traces/claim-01-trace.md`, showing turns 1–3 as tool_use, tool_use, end_turn. The loop code is `claims_intake/loop.py:42`."

> "From `EVIDENCE/system-2-retail-context/runs/budget-analysis.md`: baseline 47,832 tokens, assembled 18,924 tokens (60% reduction). The facts block at 8,000 tokens dominates because it's kept verbatim."

> "The deploy-check skill has `context: fork` (see `EVIDENCE/system-3-claude-config/.claude/skills/deploy-check/skill-context-fork.md` and project `.claude/skills/deploy-check/SKILL.md` line 4). This keeps discovery output isolated from the main session."

> "Actual `hot_state.json` from a shift run was 2,847 bytes (`EVIDENCE/system-4-shift-monitor/data/shift-run-A/hot-state-analysis.md`). At this rate, 3 shifts/day for 6 months = 540 MB if state grew unbounded, proving the budget matters."

**Key:** Every citation includes:
1. Path to evidence file (`EVIDENCE/system-N-*/.../file.md`)
2. Specific artifact or line number if available
3. What it proves

---

## Alignment Checklist

Before submitting evidence, verify:

- ✅ **Path mirroring:** Every evidence `.md` file corresponds to a project file or artifact
  - E.g., evidence about `project/claims_intake/loop.py` lives in `EVIDENCE/system-1/claims_intake/loop.md`

- ✅ **File references:** All evidence documents quote actual file paths and line numbers
  - Example: "`claims_intake/loop.py:42`: `if response.stop_reason == 'end_turn': break`"

- ✅ **Artifact capture:** Run outputs (traces, budgets, JSON) are saved with minimal editing
  - Save raw `.json`, `.jsonl`, `.txt` files as-is
  - Write separate `*-analysis.md` files to interpret them

- ✅ **Validator alignment (System 3 only):** Your evidence structure validates against the `.claude/` hierarchy
  - If project has `.claude/skills/deploy-check/SKILL.md`, evidence mirrors this

- ✅ **Test coverage:** Test evidence documents which test file covers which behavior
  - Example: "`tests/test_antipatterns.py` verifies that loop.py doesn't call model twice in one turn"

- ✅ **Proof citations:** Analysis files quote code or artifact data, not just summarize
  - ❌ Bad: "The tool design prevents misrouting"
  - ✅ Good: "Tools have distinct descriptions: classifier='determine type'; router='pick queue'. Quoted from `tools.py:15–20`."

---

## Example: End-to-End for One System

### Build System 1
```bash
cd "Build a Claims Intake Agent with a stop_reason-Driven Loop/exercises/03-dynamic-decomposition/solution"
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v | tee ../../../EVIDENCE/system-1-claims-intake/pytest-run.txt
python -m claims_intake.run --all
```

### Capture Evidence
1. Save `pytest-run.txt` (terminal output)
2. Copy one trace from `runs/<timestamp>/traces/` → analyze in `EVIDENCE/.../runs/traces/claim-01-trace.md`
3. Copy `runs/<timestamp>/queues/*.jsonl` → summarize in `EVIDENCE/.../runs/queues/routing-summary.md`
4. Read `claims_intake/loop.py` → write `EVIDENCE/.../claims_intake/loop.md` with quoted code
5. Read `tests/test_antipatterns.py` → write `EVIDENCE/.../tests/test-antipatterns.md`

### Write Analysis
```markdown
# claims_intake/loop.md

## Purpose
The agentic loop drives claim intake. Every claim invokes the loop to route it.

## Core Function
**File:** `claims_intake/loop.py`, **Function:** `run_session()`

The loop calls the model and checks `stop_reason`:
- `tool_use`: Execute the requested tool, loop continues
- `end_turn`: Claim is routed, exit loop, return result

**Code (line 42):**
```python
if response.stop_reason == 'end_turn':
    return session.outcome
elif response.stop_reason == 'tool_use':
    # Execute tool, continue loop
```

## Proof
From actual run: `EVIDENCE/system-1-claims-intake/runs/traces/claim-01-trace.md`
shows a trace where this decision logic routes claim 01 in 3 turns.
```

### Cite in Reflection Brief
> "Loop control: The `stop_reason` sequence from `EVIDENCE/system-1-claims-intake/runs/traces/claim-01-trace.md` shows Turn 1: `tool_use`, Turn 2: `tool_use`, Turn 3: `end_turn`, routing the claim. The decision is made in `claims_intake/loop.py:42`."

---

## Questions?

Refer to:
- [../EVIDENCE-STRUCTURE.md](../EVIDENCE-STRUCTURE.md) — Full structure guide
- `system-N-*/README.md` — Per-system details
- [../Project-Harness%20Engineering%20with%20Claude%20and%20Claude%20Code/reflection-brief-template.md](../Project-Harness%20Engineering%20with%20Claude%20and%20Claude%20Code/reflection-brief-template.md) — What to answer
