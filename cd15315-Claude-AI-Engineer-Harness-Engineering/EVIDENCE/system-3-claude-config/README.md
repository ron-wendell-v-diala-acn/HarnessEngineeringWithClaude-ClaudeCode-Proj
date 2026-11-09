# System 3 Evidence: E-Commerce Team Claude Code Config

**Project Path:**
```
Configure Claude Code for a Multi-Surface Monorepo Team/04-plan-mode-and-explore-decision-doc/solution/
```

**Actual Project Files Being Validated:**
- `Configure Code.../solution/CLAUDE.md`
- `Configure Code.../solution/.claude/standards/*.md`
- `Configure Code.../solution/.claude/rules/*.md`
- `Configure Code.../solution/.claude/commands/*.md`
- `Configure Code.../solution/.claude/skills/deploy-check/SKILL.md`

**Run commands (against actual project files):**
```bash
cd Configure\ Code.../04-plan-mode.../solution/
pytest tests/ -v                       # expect 35 passed
python -m ecommerce_team_config .      # validate ACTUAL config hierarchy in this folder
```

## ⛔ Critical: Evidence Validates ACTUAL Project Files

**Before you collect evidence, read:** [../../EVIDENCE-MUST-VALIDATE-ACTUAL-FILES.md](../../EVIDENCE-MUST-VALIDATE-ACTUAL-FILES.md)

**Key principle:** Evidence proves the *actual* project files work, not documentation of what should be there.

- **Tests passing (35 passed) + validator OK** = proof that actual project files are correct ✅
- **Don't create copies in EVIDENCE/.claude/** → Wrong. Validator checks actual files.
- **DO capture validator output** → This proves actual files validated successfully.

### Test & Validator Requirements

**Both must pass against ACTUAL project files:**

1. **Tests on actual project files:**
   ```bash
   cd Configure Code.../04-plan-mode.../solution/
   pytest tests/ -v → **35 passed** (exit code 0)
   ```
   ❌ Any failure → Fix actual code first.

2. **Validator on actual project files:**
   ```bash
   cd Configure Code.../04-plan-mode.../solution/
   python -m ecommerce_team_config . → **OK** (exit code 0)
   ```
   ❌ FAIL → Fix actual config first. No partial validation accepted.

### Evidence Requirements

After tests and validator pass against actual files:

- ✅ **Validator output** showing `OK` (captures that actual config validated)
- ✅ **Reference the actual `.claude/` files** that were validated:
  - `Configure Code.../solution/.claude/standards/frontend.md` (actual file)
  - `Configure Code.../solution/.claude/rules/api.md` (actual file, quote glob)
  - `Configure Code.../solution/.claude/skills/deploy-check/SKILL.md` (actual file, quote context: fork)
- ✅ **Proof of what validator confirmed** (analysis of what it checked)

**Do NOT:**
- ❌ Create `.claude/` copies in EVIDENCE folder
- ❌ Document "what should be there"
- ❌ Accept partial validation or "expected failures"

---

## What to Capture

**DO NOT mirror `.claude/` structure in EVIDENCE folder.**

Instead, capture and reference the actual validated project files:

### 1. Test Evidence

**Capture:** Full test output from actual project folder
```bash
cd Configure\ Code.../04-plan-mode.../solution/
pytest tests/ -v > pytest-run.txt
```

**File:** `pytest-run.txt`
- Must show: `35 passed`
- Exit code: 0

**Do NOT:** Submit just test results. This is a prerequisite, not evidence.

### 2. Validator Output (Main Evidence)

**Capture:** Validator output from actual project folder
```bash
cd Configure\ Code.../04-plan-mode.../solution/
python -m ecommerce_team_config . > validator-output.txt
```

**File:** `validator-output.txt`
- Must show: `OK` (all checks passed)
- Exit code: 0

**What this proves:** The actual `.claude/` hierarchy in that folder validates successfully.

**Do NOT accept:** `FAIL`, partial passes, or "expected failures." Validation is binary.

### 3. Analysis: What Validator Confirmed

**File:** `validator-analysis.md`

**What the validator checked:**

1. **CLAUDE.md at actual location**
   - Path: `Configure Code.../04-plan-mode.../solution/CLAUDE.md`
   - Validator confirmed: ✅ (file exists, has correct structure)

2. **`.claude/standards/` files at actual location**
   - Path: `Configure Code.../solution/.claude/standards/`
   - Files validated:
     - `frontend.md` → Validator confirmed: ✅
     - `api.md` → Validator confirmed: ✅
     - `database.md` → Validator confirmed: ✅
     - `testing.md` → Validator confirmed: ✅

3. **`.claude/rules/` with glob patterns at actual location**
   - Path: `Configure Code.../solution/.claude/rules/`
   - Files validated:
     - `api.md` with glob `paths: src/api/**` → Validator confirmed: ✅
     - `react.md` with glob → Validator confirmed: ✅
     - `tests.md` with glob → Validator confirmed: ✅

4. **`.claude/commands/` at actual location**
   - Path: `Configure Code.../solution/.claude/commands/`
   - Files validated:
     - `review.md` → Validator confirmed: ✅

5. **`.claude/skills/` with deploy-check at actual location**
   - Path: `Configure Code.../solution/.claude/skills/deploy-check/`
   - Files validated:
     - `SKILL.md` with `context: fork` → Validator confirmed: ✅
     - `allowed-tools:` constraints (read-only) → Validator confirmed: ✅

**Conclusion:** The actual project `.claude/` hierarchy is correct.

---

## Citation in Reflection Brief

### Example Citation
> "From EVIDENCE/system-3-claude-config/validator-output.txt, the validator was run against the actual project files (Configure Code.../solution/) and returned OK. This proves that (1) CLAUDE.md hierarchy is correct, (2) path-scoped rules apply correctly (e.g., `paths: src/api/**` in Configure Code.../solution/.claude/rules/api.md line 3), (3) deploy-check skill has context: fork (Configure Code.../solution/.claude/skills/deploy-check/SKILL.md line 4), and (4) allowed-tools enforce read-only behavior (line 6 onward). The validator output is definitive proof the actual project configuration meets specification."

---

## Important: What NOT to Do

### ❌ Wrong Structure
```
EVIDENCE/system-3-claude-config/
├── .claude/
│   ├── standards/
│   │   ├── frontend-analysis.md      ← WRONG: Analysis of copies
│   │   └── api-analysis.md           ← WRONG: Documentation
│   └── rules/
│       └── api-rule-analysis.md      ← WRONG: Interpretation
└── validator-output.txt
```

Problems:
- Validator checked actual files, not these copies
- Analysis documents what *should* be there, not proof it works
- Separates evidence from what was validated

### ✅ Correct Structure
```
EVIDENCE/system-3-claude-config/
├── README.md (this file)
├── pytest-run.txt                    ← Actual test output
├── validator-output.txt              ← Actual validator proof
├── validator-analysis.md             ← What validator confirmed
└── [References to actual project files]
    └── Configure Code.../solution/.claude/ (the files that were validated)
```

Strength:
- Validator output directly proves actual files are correct
- No separation between evidence and validation
- Clear proof, not interpretation

---

## Alignment Checklist

✅ **Validator proves actual project files work**
- Command run: `python -m ecommerce_team_config Configure Code.../04-plan-mode.../solution/`
- Output: OK (binary result, no partial credit)

✅ **Evidence captures validator output**
- File: `validator-output.txt` (unedited)
- Shows actual validation result

✅ **Analysis references actual project files**
- Example: `Configure Code.../solution/.claude/rules/api.md` (actual file path)
- Not copies in EVIDENCE folder

✅ **Tests also pass**
- File: `pytest-run.txt` showing 35 passed
- Exit code: 0

✅ **No "expected failures" or partial validation**
- Validator is binary: OK or FAIL
- No accepting FAIL with explanation

---

## File Reference Summary

| Evidence File | What It Contains | Purpose |
|---------------|-----------------|---------|
| `pytest-run.txt` | Actual test output | Proves code is correct (prerequisite) |
| `validator-output.txt` | Actual validator output | PROVES actual .claude/ files are correct |
| `validator-analysis.md` | What validator checked | Explains what was validated |

All other files reference the *actual* project files being validated, not copies.
