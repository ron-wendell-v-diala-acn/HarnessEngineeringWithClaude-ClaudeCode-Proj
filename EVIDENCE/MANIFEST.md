# Evidence Manifest: Four AI Engineering Systems

**Date:** November 6, 2026
**Project:** cd15315 — Claude AI Engineer Harness
**Repository:** Build multi-shift quality monitoring + long-conversation context + claims intake + Claude Code config

---

## Executive Summary

This evidence collection documents four independent AI engineering systems, each demonstrating a distinct architectural pattern:

| System | Module | Key Pattern | Status |
|--------|--------|-------------|--------|
| **1** | Shift Monitor | Tiered state orchestration | ✅ Complete |
| **2** | Context Strategy | Long-conversation compression | ✅ Complete |
| **3** | Claims Intake | Stop-reason-driven agentic loop | ✅ Complete |
| **4** | Claude Code Config | Team configuration framework | ✅ Complete |

---

## System 1: Shift Monitor Orchestrator

### Location
`/voc/work/EVIDENCE/system-1-shift-monitor/`

### Core Files
- `README.md` — System overview and architectural highlights
- `SHIFT_MONITOR_ORCHESTRATOR_REPORT.md` — Execution report and metrics
- `hot_state.json` — In-context state snapshot (965 bytes)
- `shift_C_2026-04-30.json` — Recorded Claude response

### Quick Facts
- **Pattern:** Warm + hot tier orchestration with single Claude invocation
- **Result:** Shift C analysis (17 new defects, 3 high severity)
- **Metrics:** 965 byte state (18.8% of 5 KB budget)
- **Compression:** Hash-based tracking for large defect datasets
- **Reproducibility:** Recorded response mode (deterministic)

### Key Achievement
Demonstrates how to maintain constrained in-context state (hot tier) while analyzing historical context (warm tier), enabling scalable defect monitoring across multiple shifts.

---

## System 2: Long-Conversation Context Strategy

### Location
`/voc/work/EVIDENCE/system-2-context-strategy/`

### Core Files
- `README.md` — System overview and evaluation methodology
- `CONTEXT_STRATEGY_EXECUTION_REPORT.md` — Detailed analysis and metrics
- `test_log.txt` — System 2 pytest (30/30 passing)
- `budget.json` — Token reduction metrics (56.69%)
- `eval.jsonl` — Evaluation with full context (6/6 passing)
- `eval_control.jsonl` — Control group without context (1/6 expected)

### Quick Facts
- **Pattern:** Case fact extraction + compression + assembly
- **Result:** 56.69% token reduction (38,708 → 16,765 tokens)
- **Compression:** Refund (97.2%) + Subscription (96.4%)
- **Evaluation:** 6 questions, 100% pass with context, controlled regression in Q6
- **Quality:** Compression preserves all question-answerable facts

### Key Achievement
Demonstrates how to compress long support conversations while maintaining reasoning quality, enabling cost-effective long-running copilot conversations with controlled evaluation methodology.

---

## System 3: Claims Intake Agent

### Location
`/voc/work/EVIDENCE/system-3-claims-intake/`

### Core Files
- `README.md` — System overview and loop mechanics
- `AGENTIC_LOOP_EXECUTION_REPORT.md` — Detailed trace analysis
- `summary.md` — Run summary of 8 claims
- `claim_01_kitchen_fire.jsonl` — 2-turn simple case
- `claim_04_neighbor_injury.jsonl` — 4-turn complex case with confidence

### Quick Facts
- **Pattern:** Stop-reason-driven multi-turn loop with tool chaining
- **Result:** 8 claims processed (route or escalate)
- **Loop Control:** `stop_reason == "tool_use"` continues, `== "end_turn"` stops
- **Complexity:** Simple claims (2 turns), complex claims (4+ turns)
- **Confidence:** Models express uncertainty (0.95 for high-confidence escalations)

### Key Achievement
Demonstrates how to implement stop_reason-driven agentic loops for complex multi-step reasoning, validating tool integration, turn flow, and confidence quantification in insurance claim processing.

---

## System 4: Claude Code Configuration

### Location
`/voc/work/EVIDENCE/system-4-claude-config/`

### Core Files
- `README.md` — System overview and architecture
- `CLAUDE_CODE_CONFIG_VALIDATION_REPORT.md` — Validation and hierarchy
- `CLAUDE.md` — Project-level entry point
- **Standards (4 files):**
  - `standards_frontend.md` — React conventions
  - `standards_api.md` — Handler patterns
  - `standards_database.md` — Repository pattern
  - `standards_testing.md` — Test expectations
- **Rules (3 files with glob paths):**
  - `rules_react.md` — src/components/**, src/pages/** activation
  - `rules_api.md` — src/api/** activation
  - `rules_tests.md` — **/*.test.ts(x) activation
- **Workflows:**
  - `command_review.md` — /review (PR review checklist, 4-phase)
  - `skill_deploy_check.md` — /deploy-check (fork context, 3 checks)

### Quick Facts
- **Pattern:** Team configuration framework with path-scoped rules
- **Scope:** Project-level (git-shared) + User-level (local) + Directory-level
- **Activation:** Glob patterns (src/components/**, src/api/**, **/*.test.ts)
- **Tools:** Read-only allowlists for both /review and /deploy-check
- **Isolation:** Fork context for /deploy-check (clean main conversation)

### Key Achievement
Demonstrates how to establish team-wide conventions via version-controlled configuration, enabling automated enforcement of standards while respecting user customization and maintaining focused conversation context.

---

## Cross-System Analysis

### Common Themes

**1. State Management**
- System 1: Hot state (965 bytes, 18.8% utilization)
- System 2: Assembled context (56.69% reduction)
- System 3: Message history with tool results
- System 4: Configuration state (standards + rules + workflows)

**2. Compression Patterns**
- System 1: Hash-based defect tracking
- System 2: Case fact extraction
- System 3: Multi-turn reasoning chains
- System 4: Modular @-imports and path-scoped activation

**3. Determinism & Reproducibility**
- System 1: Recorded response mode
- System 2: Exact token counting via budget.json
- System 3: Complete trace capture for loop validation
- System 4: Version-controlled configuration

**4. Isolation & Boundaries**
- System 1: Warm tier (historical) vs hot tier (current)
- System 2: Active cases vs resolved (compressed) vs historical (hashed)
- System 3: Tool boundaries (classify, evaluate, score)
- System 4: Project-level (shared) vs user-level (local) vs directory-level

---

## Evidence Quality Standards

Each system includes:

### 1. Complete Specification
- Architecture and design patterns
- Configuration frontmatter (where applicable)
- Boundaries and scope
- Integration points

### 2. Execution Artifacts
- Test logs or execution reports
- Key output files
- Metrics and measurements
- Trace or audit logs

### 3. Validation Evidence
- Expected vs actual results
- Metrics matching targets
- Pass/fail criteria
- Control groups (where applicable)

### 4. Reproducibility Documentation
- Commands to reproduce
- File paths and locations
- Dependencies and prerequisites
- Known issues or workarounds

### 5. Strategic Context
- Why this pattern matters
- Trade-offs and design choices
- Real-world applicability
- Common use cases

---

## Navigating the Evidence

### For Quick Overview
1. Read this MANIFEST.md (current file)
2. Open one README.md per system of interest
3. Check execution report for key metrics

### For Detailed Analysis
1. System README.md (architecture + key findings)
2. Execution report (detailed metrics and analysis)
3. Core artifacts (JSON, logs, config files)
4. Traces or transcripts (if applicable)

### For Implementation Reference
1. Architecture section in README
2. Key patterns section
3. Example workflows or code patterns
4. Configuration frontmatter (Systems 1, 4)

### For Validation
1. Execution report (metrics section)
2. Test logs (pass/fail counts)
3. Control groups (System 2)
4. Trace analysis (System 3)

---

## File Structure

```
EVIDENCE/
├── MANIFEST.md (this file)
│
├── system-1-shift-monitor/
│   ├── README.md
│   ├── SHIFT_MONITOR_ORCHESTRATOR_REPORT.md
│   ├── hot_state.json
│   ├── shift_C_2026-04-30.json
│   └── test_log.txt
│
├── system-2-context-strategy/
│   ├── README.md
│   ├── CONTEXT_STRATEGY_EXECUTION_REPORT.md
│   ├── test_log.txt
│   ├── budget.json
│   ├── eval.jsonl
│   └── eval_control.jsonl
│
├── system-3-claims-intake/
│   ├── README.md
│   ├── AGENTIC_LOOP_EXECUTION_REPORT.md
│   ├── summary.md
│   ├── claim_01_kitchen_fire.jsonl
│   └── claim_04_neighbor_injury.jsonl
│
└── system-4-claude-config/
    ├── README.md
    ├── CLAUDE_CODE_CONFIG_VALIDATION_REPORT.md
    ├── CLAUDE.md
    ├── standards_frontend.md
    ├── standards_api.md
    ├── standards_database.md
    ├── standards_testing.md
    ├── rules_react.md
    ├── rules_api.md
    ├── rules_tests.md
    ├── command_review.md
    └── skill_deploy_check.md
```

---

## Summary Statistics

### Evidence Collection
- **Systems:** 4 independent modules
- **Total Files:** 35 (READMEs, reports, configs, artifacts, traces)
- **Total Size:** ~120 KB
- **Execution Date:** November 6, 2026

### Test Coverage
- **System 1:** Orchestrator execution (shift C validated)
- **System 2:** 30/30 pytest passing + 6/6 evaluation questions + control group
- **System 3:** 8 claims processed + trace validation
- **System 4:** Configuration validation complete (all rules, standards, commands, skills)

### Key Metrics
- **System 1:** 965 bytes hot state (18.8% utilization)
- **System 2:** 56.69% token reduction (21,943 tokens saved)
- **System 3:** 2-4 turn loops, 0.95 max confidence
- **System 4:** 3 path-scoped rules, 2 workflows, 4 standards

---

## Next Steps

### For Review
- [ ] Examine each system README for architectural overview
- [ ] Check execution reports for metrics
- [ ] Review trace files for validation

### For Replication
- [ ] Follow commands in README sections
- [ ] Use recorded responses for reproducibility
- [ ] Verify metrics match expected targets

### For Integration
- [ ] Adapt System 1 orchestration for your monitoring
- [ ] Apply System 2 compression to long conversations
- [ ] Implement System 3 loops for multi-step reasoning
- [ ] Deploy System 4 config for team standardization

---

## Document Information

- **Created:** November 6, 2026
- **Last Updated:** November 6, 2026
- **Scope:** Four AI engineering systems in cd15315 harness
- **Status:** All four systems documented and validated
- **Audience:** Engineering teams, researchers, integration teams

---

For detailed information on any system, see the corresponding README in that system's folder.
