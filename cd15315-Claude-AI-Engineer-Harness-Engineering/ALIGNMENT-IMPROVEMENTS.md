# Evidence Structure Improvements — From Generic to Aligned

## The Problem: Before

Previously, there was no structured guidance on organizing evidence. Students would create evidence folders like:

```
EVIDENCE/
├── system-4-claude-config/
│   └── skill_deploy_check.md              ❌ Generic name, doesn't mirror project
├── system-3-monitoring/
│   └── orchestration_notes.txt            ❌ Unclear what project this refers to
└── some-random-traces/
    └── trace_data.md                      ❌ No clear evidence-to-project mapping
```

**Issues:**
- Evidence paths don't mirror project structure
- Hard to trace a piece of evidence back to the actual file it analyzes
- Analyzer paths (`.claude/skills/deploy-check/SKILL.md`) don't align with evidence paths
- Reflection brief citations are vague ("See my evidence about the skill")
- Readers can't verify evidence without searching the project

---

## The Solution: After

Now there's a **complete, aligned structure** where evidence mirrors the executable project tree.

### System 3 Example: Claude Code Config

**Before (misaligned):**
```
EVIDENCE/
└── system-3-claude-config/
    └── skill_deploy_check.md        ← Where in project is this?
```

**After (aligned):**
```
EVIDENCE/
└── system-3-claude-config/
    ├── README.md                    ← Guidance for this system
    ├── CLAUDE.md                    ← Copy of project file (reference)
    ├── root-claude-overview.md      ← Analysis
    ├── validator-output.txt         ← Proof (run output)
    │
    ├── .claude/
    │   ├── standards/
    │   │   ├── README.md            ← Explain "standards" tier
    │   │   ├── frontend-analysis.md
    │   │   ├── api-analysis.md
    │   │   ├── database-analysis.md
    │   │   └── testing-analysis.md
    │   │
    │   ├── rules/
    │   │   ├── README.md            ← Explain "path-scoped rules"
    │   │   ├── api-rule-analysis.md
    │   │   ├── react-rule-analysis.md
    │   │   └── tests-rule-analysis.md
    │   │
    │   ├── commands/
    │   │   └── review-analysis.md
    │   │
    │   └── skills/
    │       └── deploy-check/
    │           ├── SKILL.md                ← Actual file copy
    │           ├── skill-overview.md       ← Analysis
    │           ├── skill-context-fork.md   ← Deep dive
    │           ├── skill-allowed-tools.md  ← Tool analysis
    │           └── skill-checks.md         ← Check descriptions
    │
    └── pytest-run-summary.md
```

✅ **Now:** Evidence paths **exactly mirror** the project structure.

---

## Why This Matters

### 1. Verifiability
**Before:** "See my evidence about the deploy-check skill"
- Reader has to guess where the project file is
- Has to search `.claude/` structure to find it
- Unclear if evidence is about SKILL.md or the command or something else

**After:** "See `EVIDENCE/system-3-claude-config/.claude/skills/deploy-check/skill-context-fork.md`"
- Reader knows exactly where to look
- Can immediately compare to project `.claude/skills/deploy-check/SKILL.md`
- Clear which aspect of the skill is analyzed

### 2. Traceability
**Before:** Analysis might reference code implicitly or vaguely
- "The skill uses fork mode"
- Reader can't easily verify or find the exact line

**After:** All analysis cites line numbers and file paths
- "From `SKILL.md` line 4: `context: fork`"
- Reader can immediately jump to the source

### 3. Alignment with Validation
**Before:** System 3's evidence structure didn't match what the validator checks
- Validator checks `.claude/skills/deploy-check/SKILL.md`
- Evidence was in `EVIDENCE/system-3-claude-config/skill_deploy_check.md`
- Mismatch = confusing

**After:** Evidence structure mirrors the validator's perspective
- Validator checks `.claude/skills/deploy-check/SKILL.md`
- Evidence is in `EVIDENCE/.claude/skills/deploy-check/skill-*.md`
- Perfect alignment

### 4. Reflection Brief Citations
**Before:**
> "The skill uses fork to isolate output. See evidence section 3.2."

**After:**
> "From `EVIDENCE/system-3-claude-config/.claude/skills/deploy-check/skill-context-fork.md`, the skill has `context: fork` (SKILL.md line 4). This keeps discovery output (file lists, git status) isolated from the main session; only the verdict returns to the caller."

✅ Specific, verifiable, traceable.

---

## New Artifacts Created

### 1. **EVIDENCE-STRUCTURE.md** (Top-level guide)
- Comprehensive overview of alignment principle
- Directory layout for all 4 systems
- Detailed sections for each system showing exact evidence structure
- Alignment checklist
- Good vs. bad examples

### 2. **EVIDENCE/README.md** (Main evidence folder guide)
- Quick start instructions
- The alignment principle explained with System 3 example
- Per-system structure overview
- What "evidence" means (artifacts, analysis, summaries)
- Citation pattern for reflection brief
- Alignment checklist
- End-to-end example for System 1

### 3. **EVIDENCE/system-N-*/README.md** (Per-system guides)

Each system's evidence folder includes a detailed README:

#### System 1: Claims Intake Agent
- What to capture (tests, code analysis, run artifacts)
- File-by-file breakdown:
  - `claims_intake/loop.md` — agentic loop mechanics
  - `claims_intake/tools.md` — tool design + schemas
  - `claims_intake/tracer.md` — evidence capture
  - `runs/traces/claim-*.md` — actual execution traces
  - `tests/test-*.md` — test coverage analysis
- Alignment checklist
- Reflection brief citations

#### System 2: Retail Support Context
- Context assembly, reduction, evaluation analysis
- Budget analysis from actual `budget.json`
- Eval vs. control comparison
- Per-section token breakdown
- Test coverage for assembler, reducer, evaluator

#### System 3: Claude Code Config
- **Unique:** Evidence structure mirrors `.claude/` project structure
- Standards tier analysis (frontend, api, database, testing)
- Rules tier analysis (path-scoped rules with globs)
- Commands tier (e.g., `/review`)
- Skills tier (e.g., `/deploy-check` with fork analysis)
- Scope hierarchy explanation (project vs. user vs. directory)
- Validator output capture

#### System 4: Multi-Shift Quality Monitoring
- Orchestration layer analysis
- Warm-tier indexed query analysis
- Hot-state shape and byte-size analysis
- Crash recovery staleness threshold
- Scratchpad isolation analysis
- Actual run artifacts (shift output, hot_state.json with size analysis)
- Test coverage for orchestration, recovery, state bounds

### 4. **Updated main README.md**
- New "Capstone: Harness Engineering" section
- Explains evidence structure approach
- Links to guides
- Why structure matters (verifiable, traceable, aligned, reflection-ready)

### 5. **Updated main project directory**
```
cd15315-Claude-AI-Engineer-Harness-Engineering/
├── EVIDENCE/                               ← NEW: Full folder with guides
│   ├── README.md                          ← NEW: Main evidence guide
│   ├── system-1-claims-intake/            ← NEW: Template + README
│   ├── system-2-retail-context/           ← NEW: Template + README
│   ├── system-3-claude-config/            ← NEW: Template + README (with .claude/)
│   ├── system-4-shift-monitor/            ← NEW: Template + README
│   └── [nested directories for each system]
├── EVIDENCE-STRUCTURE.md                  ← NEW: Complete alignment guide
├── ALIGNMENT-IMPROVEMENTS.md              ← NEW: This document
├── README.md                              ← UPDATED: Capstone section added
└── [existing course projects...]
```

---

## Key Improvements Summary

| Aspect | Before | After |
|--------|--------|-------|
| **Structure** | Ad-hoc, no template | Mirrors project tree for all 4 systems |
| **System 3 alignment** | Mismatched (evidence ≠ project) | Perfect mirror of `.claude/` hierarchy |
| **Citation precision** | Vague ("my evidence") | Exact file paths (`EVIDENCE/system-N-*/...`) |
| **Traceability** | Hard to map evidence → code | Direct path correspondence |
| **Validator alignment** | Not aligned to validator paths | Evidence validates same structure as validator checks |
| **Guidance** | None | 4 detailed per-system READMEs + 2 main guides |
| **Artifact capture** | Unclear what to save | Explicit checklist per system |
| **Reflection brief citations** | Vague references | Specific, verifiable citations |

---

## How Students Use This

### For Each System:
1. **Read the per-system guide:** `EVIDENCE/system-N-*/README.md`
2. **Build and run the system** following capstone instructions
3. **Capture evidence** following the "What to Capture" section
4. **Organize in the aligned structure** (directories already created)
5. **Write analysis documents** in corresponding places
6. **Cite in reflection brief** using the `EVIDENCE/system-N-*/.../file.md` pattern

### Example: System 3 Evidence Flow
```
1. Run: python -m ecommerce_team_config . → save output to EVIDENCE/validator-output.txt
2. Analyze: Copy .claude/standards/frontend.md → write EVIDENCE/.claude/standards/frontend-analysis.md
3. Reference: Quote "lines 8–12" in analysis
4. Cite: "From EVIDENCE/system-3-claude-config/.claude/standards/frontend-analysis.md, the rule is 'Function components only' (standards/frontend.md line 8)"
```

---

## Validation: Does It Work?

### System 3 Validator Alignment Test

**Project file:** `.claude/skills/deploy-check/SKILL.md`

**Evidence structure:**
```
EVIDENCE/system-3-claude-config/
└── .claude/
    └── skills/
        └── deploy-check/
            ├── SKILL.md              ← Copy for reference
            ├── skill-overview.md     ← Analysis of purpose
            ├── skill-context-fork.md ← Analysis of context: fork
            └── ...
```

**Validator checks:** ✅ (same path structure)
**Evidence reflects:** ✅ (analysis documents alongside artifact)
**Citation in brief:** ✅ (direct path mapping)

---

## Next Steps for Students

1. Create your EVIDENCE folder structure (templates provided)
2. Follow EVIDENCE-STRUCTURE.md and per-system README guides
3. Run each system and capture artifacts
4. Write analysis documents with exact citations
5. Fill reflection brief with specific evidence paths
6. Verify alignment checklist before submitting

---

## Design Principles

The improved structure follows these principles:

1. **Mirror, don't invent** — Evidence paths match project paths
2. **Cite precisely** — Every analysis quotes file names and line numbers
3. **Capture artifacts raw** — Actual traces, budgets, outputs stay unedited
4. **Analyze separately** — Create `*-analysis.md` files alongside artifacts
5. **Validate alignment** — For System 3, evidence structure itself validates the config hierarchy
6. **Enable tracing** — Any citation should be immediately verifiable against the project

---

## Files to Start With

1. **First read:** [../EVIDENCE-STRUCTURE.md](../EVIDENCE-STRUCTURE.md) (15 min)
   - Understand alignment principle
   - See folder layouts for all 4 systems

2. **Then pick a system:** [system-N-*/README.md](system-1-claims-intake/) (5–10 min each)
   - Get specific guidance on what to capture
   - See exact file organization

3. **As you run systems:** Refer to guides
   - Capture artifacts where indicated
   - Create analysis documents in right folders
   - Cite using `EVIDENCE/system-N-*/.../file.md` pattern

---

## Questions or Issues?

- Check [EVIDENCE-STRUCTURE.md](../EVIDENCE-STRUCTURE.md) for the comprehensive guide
- See `EVIDENCE/system-N-*/README.md` for per-system details
- Look at citation examples in each guide
- Verify structure against alignment checklist before submitting
