# Critical Correction: Evidence Validates Actual Project Files

## The Problem

I created a structural separation:
- **Evidence folder:** `EVIDENCE/system-3-claude-config/.claude/` (copies/documentation)
- **Actual project:** `Configure Claude Code.../04-plan-mode.../solution/.claude/` (what validator checks)

**This is wrong.** Evidence is proof that the *actual* project files work, not documentation of what *should* be there.

---

## The Principle

**Evidence proves the actual project files meet specification.**

Not:
- "Here's what the config should look like" (EVIDENCE copies)
- "The validator understands this structure" (documentation)
- "If it were run, it would validate" (hypothetical)

Yes:
- "The validator was run against the actual project files" (proof)
- "Output shows: OK" (actual result)
- "This proves the actual .claude/ hierarchy is correct" (evidence of correctness)

---

## System 3 (Claude Code Config) — Corrected Approach

### Step 1: Run Validator Against Actual Files
```bash
cd "Configure Claude Code for a Multi-Surface Monorepo Team/04-plan-mode-and-explore-decision-doc/solution/"
python -m ecommerce_team_config .
```

**Output must be:**
```
Checking CLAUDE.md... OK
Checking .claude/standards/... OK
Checking .claude/rules/... OK
Checking .claude/commands/... OK
Checking .claude/skills/... OK
Overall: OK
```

### Step 2: Capture Validator Output (This is Evidence)
```bash
python -m ecommerce_team_config . > validator-output.txt
```

**File:** `validator-output.txt` (actual output from validator)

**What this proves:** The validator ran against the actual project files and confirmed they're correct.

### Step 3: Document What Was Validated (Supporting Analysis)

**Create:** `EVIDENCE/system-3-claude-config/validator-analysis.md`

Content:
```markdown
## Validator Run Results

**Command:**
```bash
python -m ecommerce_team_config Configure\ Code.../04-plan-mode.../solution/
```

**Output:** OK

**What the validator checked:**
1. CLAUDE.md exists and has correct structure
   - Reference: Project file at Configure Code.../04-plan-mode.../solution/CLAUDE.md
   - Validator confirmed: ✅

2. .claude/standards/ files present and valid
   - Project files:
     - Configure Code.../solution/.claude/standards/frontend.md
     - Configure Code.../solution/.claude/standards/api.md
     - Configure Code.../solution/.claude/standards/database.md
     - Configure Code.../solution/.claude/standards/testing.md
   - Validator confirmed all: ✅

3. .claude/rules/ with path-scoped globs
   - Project files:
     - Configure Code.../solution/.claude/rules/api.md
     - Configure Code.../solution/.claude/rules/react.md
     - Configure Code.../solution/.claude/rules/tests.md
   - Each has glob frontmatter (e.g., `paths: src/api/**`)
   - Validator confirmed: ✅

4. .claude/commands/ present
   - Project file: Configure Code.../solution/.claude/commands/review.md
   - Validator confirmed: ✅

5. .claude/skills/ with deploy-check skill
   - Project file: Configure Code.../solution/.claude/skills/deploy-check/SKILL.md
   - Has `context: fork` and `allowed-tools:` constraints
   - Validator confirmed: ✅

**Conclusion:** The actual project .claude/ hierarchy is correct and validates successfully.
```

### Step 4: Cite in Evidence Folder (Proof of Actual Validation)

Create: `EVIDENCE/system-3-claude-config/README.md`

Content references:
```markdown
## Evidence: Claude Code Config Validation

**The actual project files were validated by running:**
```bash
python -m ecommerce_team_config Configure\ Code\ for\ a\ Multi-Surface\ Monorepo\ Team/04-plan-mode-and-explore-decision-doc/solution/
```

**Result:** OK ✅

**Artifacts:**
- Validator output: [validator-output.txt](validator-output.txt)
- Validation analysis: [validator-analysis.md](validator-analysis.md)

**What this proves:**
- The actual `.claude/` hierarchy in the project folder validates successfully
- CLAUDE.md, standards/, rules/, commands/, and skills/ are all correct
- Path-scoped rules apply correctly
- deploy-check skill has correct context: fork and allowed-tools constraints

**References to actual project files:**
- CLAUDE.md at: Configure Code.../04-plan-mode.../solution/CLAUDE.md
- Rules with globs at: Configure Code.../solution/.claude/rules/*.md
- deploy-check skill at: Configure Code.../solution/.claude/skills/deploy-check/SKILL.md
```

---

## The Corrected Pattern

### ❌ Wrong Approach (Current)
```
EVIDENCE/system-3/
├── .claude/
│   ├── standards/
│   │   ├── frontend-analysis.md  ← Documenting what should be there
│   │   └── ...
│   └── rules/
│       └── api-rule-analysis.md  ← Describing the rules
└── validator-output.txt           ← Proof copied to evidence
```

Problem: Evidence is separated from what validator actually checked.

### ✅ Correct Approach
```
EVIDENCE/system-3/
├── README.md
│   └── "Validator was run against actual project files"
│       "Output shows: OK"
│       "This proves .claude/ hierarchy is correct"
├── validator-output.txt              ← Actual validator output
├── validator-analysis.md             ← What it checked
└── [references to actual project files]
    ├── Configure Code.../solution/CLAUDE.md
    ├── Configure Code.../solution/.claude/standards/*.md
    ├── Configure Code.../solution/.claude/rules/*.md
    └── Configure Code.../solution/.claude/skills/deploy-check/SKILL.md
```

Strength: Evidence directly proves the actual project files work.

---

## All Systems: Same Pattern

### System 1 (Claims Intake)
```
Evidence proves actual project files at:
Build a Claims Intake Agent.../exercises/03-dynamic-decomposition/solution/

Validator: pytest tests/ -v → 29 passed ✅
Artifact: traces from actual runs/ in that folder
Proof: Claims actually routed to correct destinations
```

### System 2 (Retail Context)
```
Evidence proves actual project files at:
Engineer a Long-Conversation Context.../04-assemble-and-locate/solution/

Validator: pytest tests/ -v → 30 passed ✅
Artifacts: budget.json, eval.jsonl, eval_control.jsonl from actual runs/
Proof: Token reduction achieved, facts block improves accuracy
```

### System 3 (Claude Code Config)
```
Evidence proves actual project files at:
Configure Claude Code.../04-plan-mode-and-explore-decision-doc/solution/

Validator: python -m ecommerce_team_config . → OK ✅
Artifact: validator output from actual validation
Proof: .claude/ hierarchy validates
```

### System 4 (Multi-Shift Monitoring)
```
Evidence proves actual project files at:
Build a Multi-Shift Quality Monitoring.../04-fork-scratchpad/solution/

Validator: pytest tests/ -v → 33 passed ✅
Artifacts: hot_state.json, shift-output.txt from actual runs/
Proof: Warm-tier filters defects, hot state stays under budget
```

---

## The Critical Rule

**Validator Output is Evidence, Not Just a Prerequisite**

### ❌ Wrong
- Validator shows OK
- "Therefore, config is correct" (claim without proof)
- EVIDENCE folder documents what should be there

### ✅ Correct
- Validator runs against actual project files
- Output: OK (actual proof)
- EVIDENCE captures: validator output (shows it happened)
- EVIDENCE documents: what validator confirmed about actual files

**Difference:** One treats validator as gate to evidence collection. One treats validator output as evidence itself.

---

## System 3 Evidence Folder Structure (Corrected)

```
EVIDENCE/system-3-claude-config/
├── README.md
│   ├─ "Validator was run against actual project files"
│   ├─ "Command: python -m ecommerce_team_config <project-path>"
│   ├─ "Result: OK"
│   └─ "This proves the actual .claude/ hierarchy is correct"
│
├── validator-output.txt
│   └─ (Actual output from validator run)
│
├── validator-analysis.md
│   ├─ "Validator checked CLAUDE.md at Configure Code.../solution/"
│   ├─ "Validator checked .claude/standards/ files at Configure Code.../solution/"
│   ├─ "Validator checked .claude/rules/ with glob patterns"
│   ├─ "Validator checked .claude/commands/ and .claude/skills/"
│   └─ "All checked ✅"
│
└── [REFERENCES TO ACTUAL PROJECT FILES]
    ├─ Configure Code.../solution/CLAUDE.md (the file validator checked)
    ├─ Configure Code.../solution/.claude/standards/ (the files validator checked)
    ├─ Configure Code.../solution/.claude/rules/ (the files validator checked)
    └─ Configure Code.../solution/.claude/skills/deploy-check/SKILL.md
```

**NOT:**
```
EVIDENCE/system-3-claude-config/
└── .claude/
    ├── standards/
    │   └── frontend-analysis.md ← WRONG: Documentation, not proof
    └── rules/
        └── api-rule-analysis.md ← WRONG: Analysis of copies, not actual files
```

---

## No Acceptance of "Expected Failures"

### ❌ Unacceptable
- "Validator would show OK if run" (hypothetical)
- "Config should be correct but validator shows FAIL" (acceptance of failure)
- "Some checks pass, others expected to fail" (partial validation)
- "I understand why it fails, which is fine" (explanation ≠ proof)

### ✅ Only Acceptable
- "Validator was run and shows OK" (actual proof)
- "All validator checks passed" (complete validation)
- "Configuration file is correct as proven by successful validation"

**Rule:** Validator output is binary: OK (accept) or FAIL (reject). No middle ground.

---

## Reflection Brief Citations (Corrected)

### ❌ Wrong
> "The validator confirmed the config is correct, showing that path-scoped rules work as intended."

### ✅ Correct
> "The validator was run against the actual project files (Configure Code.../solution/) and returned OK. This output is in EVIDENCE/system-3-claude-config/validator-output.txt. Validation confirms: (1) CLAUDE.md hierarchy is correct, (2) .claude/standards/ files are valid, (3) .claude/rules/ with glob patterns apply correctly (e.g., src/api/** rule at Configure Code.../solution/.claude/rules/api.md), (4) .claude/commands/ and .claude/skills/ are correct. The deploy-check skill has context: fork (Configure Code.../solution/.claude/skills/deploy-check/SKILL.md line 4), which isolates discovery output. Validator output proves the actual project files meet specification."

**Difference:** First cites validator as supporting claim. Second shows validator output IS the evidence.

---

## Summary of Correction

| What I Did | Why It's Wrong | What's Correct |
|-----------|----------------|-----------------|
| Created EVIDENCE/.claude/ copies | Separates from what validator checked | Evidence validates actual project files |
| Documented "what should be there" | Hypothetical, not proof | Evidence captures what actually validated |
| Treated validator as gate, not proof | Prerequisite only | Validator output IS evidence |
| Accepted "expected failures" | Validation is binary | Only OK is acceptable |
| Separated evidence from validation | Two things seem independent | Evidence proves validation succeeded |

---

## Action Items

1. **Stop creating copies in EVIDENCE/.claude/**
   - Validator checks actual files in project folder
   - Evidence should prove those files work

2. **Make validator output the centerpiece**
   - Capture: `python -m ecommerce_team_config . > validator-output.txt`
   - Analyze what it confirms about actual files
   - This is the evidence

3. **Reference actual project files**
   - Point evidence to real CLAUDE.md location
   - Point to real .claude/ hierarchy being validated
   - Show validator ran against those files

4. **No "expected failures"**
   - Validator: OK (success) or FAIL (not acceptable)
   - Configuration must validate
   - No partial validation, no hypothetical "should work"

5. **Fix all 4 systems' evidence structure**
   - Each points to actual project files in course repo
   - Each captures validator/test output as proof
   - Each proves actual files meet specification

---

## Principle

**Evidence doesn't document what *should* exist. It proves what *actually* works by validating the real project files.**

The validator checks the real files. Evidence captures that validation. That's proof.
