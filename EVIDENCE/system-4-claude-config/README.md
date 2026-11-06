# System 4: Claude Code Configuration Framework

**Exercise:** Configure Claude Code for a Multi-Surface Monorepo Team
**Module:** 03-author-forked-deploy-check-skill (Solution)
**Date:** November 6, 2026

## Overview

Claude Code configuration creates team-wide conventions and workflows for an e-commerce monorepo. The configuration hierarchy spans three levels:
1. **Project-level:** Shared via git (rules, standards, commands, skills)
2. **User-level:** Local only (personal preferences)
3. **Directory-level:** Narrower scope (specific subpaths)

This evidence captures the complete Exercise 3 solution with all standards, rules, commands, and skills.

## Key Artifacts

### 1. **CLAUDE_CODE_CONFIG_VALIDATION_REPORT.md**
- Complete validation of configuration structure
- Path-scoped rules documentation with glob patterns
- /review command specification (Exercise 2)
- /deploy-check skill specification (Exercise 3)
- Configuration hierarchy explanation

### 2. **CLAUDE.md**
- Project-level entry point
- Configuration scope documentation (project/user/directory)
- Modular @-imports pointing to standards
- Repository layout guide
- Team workflow references (/review, /deploy-check)

### 3. **Standards (4 files)**

#### standards_frontend.md
- React component conventions
- Hooks and state management rules
- Styling with Tailwind + CSS modules
- Scope: Applies to all frontend code

#### standards_api.md
- Node.js handler signature requirements
- Error handling with ApiError
- Input validation with zod schemas
- Output schema enforcement
- Scope: Applies to all `src/api/` handlers

#### standards_database.md
- PostgreSQL repository pattern
- Transaction management with `withTransaction()`
- Forward-only migrations
- Scope: Applies to all `src/db/` modules

#### standards_testing.md
- Where tests live (co-located, no mirror trees)
- What to test (components, handlers, repositories)
- What not to test (generated code, libraries)
- Scope: Cross-cutting expectations

### 4. **Rules (3 files with glob path activation)**

#### rules_react.md
**Frontmatter:**
```yaml
---
description: Conventions for React components and pages
paths:
  - "src/components/**/*"
  - "src/pages/**/*"
---
```
**Rules:**
- Function components only
- One default export per file
- Props via `interface` in same file
- Destructure props in signature
- Custom hooks top-level only
- Semantic HTML for accessibility
- Forbidden: `dangerouslySetInnerHTML`, `useLayoutEffect` outside hooks

#### rules_api.md
**Frontmatter:**
```yaml
---
description: Conventions for Node.js API handlers
paths:
  - "src/api/**/*"
---
```
**Rules:**
- Handler signature: `async function handle(req: ApiRequest<T>): Promise<ApiResponse<Out>>`
- Throw `ApiError` for validation, not return `{status: 400}`
- For 404: throw `ApiError(404, "NOT_FOUND", "...")`
- Wrap multi-writes in `withTransaction()`
- Validate at boundary with `bodySchema.parse()`
- Use `req.log.info()` for logging

#### rules_tests.md
**Frontmatter:**
```yaml
---
description: Conventions for test files (co-located *.test.ts and *.test.tsx)
paths:
  - "**/*.test.tsx"
  - "**/*.test.ts"
---
```
**Rules:**
- One top-level `describe` per file
- Nested `describe` max 2 levels
- Test descriptions start with verb
- Factories in `src/test/factories/` for test data
- Use `freezeTime()` helper for time-sensitive tests
- Forbidden: Snapshot tests, database mocking, setTimeout/setInterval

### 5. **Command: /review**

**File:** command_review.md

**Frontmatter:**
```yaml
---
description: Run the e-commerce team's PR review checklist against a pull request or local diff
argument-hint: <pr-number | "HEAD~1..HEAD" | path/to/file>
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(git diff:*)
  - Bash(git log:*)
  - Bash(git show:*)
  - Bash(git status:*)
  - Bash(gh pr diff:*)
  - Bash(gh pr view:*)
  - Bash(gh pr checks:*)
---
```

**Four-Phase Review Methodology:**

1. **Interview Phase:** Ask clarifying questions
   - When: dependency changes, API changes, refactors, multi-layer changes
   - Author answers in PR description

2. **Criteria Phase:** Report findings
   - **Must Report:** bugs, security issues, convention violations, breaking changes, migration safety
   - **Skip:** formatting, naming, stylistic preferences, TODO with ticket, unclear test descriptions

3. **Bundling Phase:** Group related findings
   - Interacting findings → one message
   - Independent findings → sequential messages

4. **Format Phase:** Structured output
   ```
   [severity] path/to/file.ts:line
   finding: <description>
   fix: <recommendation>

   verdict: approve | comment | request-changes
   ```

**Design:** Read-only tools only (no side effects)

### 6. **Skill: /deploy-check**

**File:** skill_deploy_check.md

**Frontmatter:**
```yaml
---
name: deploy-check
description: Run read-only pre-deployment validation in a forked sub-agent and report a single pass/fail summary back to the main session
context: fork
argument-hint: "[target-branch] (defaults to main)"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(git status:*)
  - Bash(git diff:*)
  - Bash(git log:*)
  - Bash(git rev-parse:*)
  - Bash(git ls-files:*)
  - Bash(gh pr view:*)
  - Bash(gh pr checks:*)
---
```

**Key Feature: Fork Context**

Runs in **isolated sub-agent** to:
- Execute verbose discovery (file enumeration, diff parsing)
- Keep verbose output in fork (not contaminating main session)
- Return only structured summary to parent session
- Enable "branching reality" pattern

**Three Pre-Deployment Checks:**

1. **Uncommitted Changes**
   - Detect: `git status --porcelain`
   - Pass: Clean working tree
   - Fail: List first 10 uncommitted paths

2. **Migrations Up-to-Date**
   - Detect: Glob migration sequence, grep new repo imports
   - Check: `git diff <target>..HEAD` for `src/db/types.ts` changes
   - Pass: Every new function backed by migration
   - Fail: Code references missing column/table

3. **CI Checks Green**
   - Detect: `gh pr view --json statusCheckRollup`
   - Pass: All checks SUCCESS
   - Fail: Any FAILURE, CANCELLED, PENDING

**Output Format:**
```json
{
  "verdict": "pass | fail",
  "checks": [
    {
      "name": "uncommitted-changes",
      "status": "pass | fail",
      "detail": "<one line or empty>"
    },
    {
      "name": "migrations",
      "status": "pass | fail",
      "detail": "<one line or empty>"
    },
    {
      "name": "ci",
      "status": "pass | fail | skipped",
      "detail": "<one line or empty>"
    }
  ]
}
```

**Design:** Read-only tools, isolated execution, structured summary only

## Configuration Hierarchy

```
Project Level (git-shared)
├── CLAUDE.md (entry point)
├── .claude/standards/ (4 files: frontend, api, database, testing)
├── .claude/rules/ (3 files: react, api, tests with glob paths)
├── .claude/commands/ (review.md: PR workflow)
└── .claude/skills/ (deploy-check: pre-deploy validation)

User Level (local-only)
├── ~/.claude/CLAUDE.md
├── ~/.claude/commands/
└── ~/.claude/skills/

Directory Level (narrower scope)
└── path/CLAUDE.md (via globs in .claude/rules/)
```

## Key Design Patterns

### 1. Glob-Based Path Activation
Rules automatically fire when editing matching files:
- `src/components/**/*` → react rules apply
- `src/api/**/*` → api rules apply
- `**/*.test.ts(x)` → test rules apply

### 2. Fork-Based Output Isolation
The `/deploy-check` skill uses `context: fork` to:
- Branch execution into sub-agent
- Keep discovery output isolated
- Return only summary to main conversation
- Keep main session focused and concise

### 3. Read-Only Tool Allowlists
Both `/review` and `/deploy-check` are explicitly read-only:
- No file writes
- No git pushes
- No deployments
- No side effects
- Safe for team automation

### 4. Modular Standards via @-imports
CLAUDE.md references standards with @-syntax:
```markdown
- @.claude/standards/frontend.md
- @.claude/standards/api.md
- @.claude/standards/database.md
- @.claude/standards/testing.md
```
Enables:
- Scannable entry point
- Easy navigation
- Clear separation of concerns

## Validation Results

✅ **Exercise 1 Solution:** Base structure complete
- `.claude/standards/` (4 files)
- `.claude/rules/` (3 files with glob frontmatter)

✅ **Exercise 2 Solution:** /review command
- Captured in command_review.md
- Four-phase review methodology
- Read-only tool allowlist

✅ **Exercise 3 Solution:** /deploy-check skill
- Captured in skill_deploy_check.md
- Fork context for output isolation
- Three pre-deployment checks
- Structured pass/fail summary

## Reproducibility

Configuration is **version-controlled and shareable:**
- ✅ All files in git (CLAUDE.md, .claude/)
- ✅ Team-wide consistency
- ✅ IDE integration via Claude Code
- ✅ Automated enforcement of rules

## Notes

- **Scope:** E-commerce monorepo with React frontend + Node.js API + PostgreSQL
- **Audience:** Entire engineering team (shared via git)
- **Applicability:** Layers on top of IDE defaults, applies automatically
- **Customization:** User-level overrides in ~/.claude/ (local, not shared)

## File Structure

```
system-4-claude-config/
├── README.md (this file)
├── CLAUDE.md (project-level entry point)
├── CLAUDE_CODE_CONFIG_VALIDATION_REPORT.md
├── standards_frontend.md
├── standards_api.md
├── standards_database.md
├── standards_testing.md
├── rules_react.md (with glob paths: src/components/**, src/pages/**)
├── rules_api.md (with glob path: src/api/**)
├── rules_tests.md (with glob paths: **/*.test.ts, **/*.test.tsx)
├── command_review.md (read-only PR review)
└── skill_deploy_check.md (fork context, 3 checks)
```

## Strategic Value

This system demonstrates how to:
1. **Establish team conventions** at project level
2. **Automate rule enforcement** via path-scoped rules
3. **Create reusable workflows** (/review, /deploy-check)
4. **Isolate verbose operations** with fork context
5. **Share standards via git** for team consistency
6. **Respect user preferences** with local-only ~/.claude/

### Team Workflow Example

**Developer A:**
```bash
# Writes code in src/components/Cart.tsx
# Claude Code automatically loads:
#   - CLAUDE.md
#   - standards_frontend.md
#   - rules_react.md (glob src/components/** matches)
# Suggestions follow React conventions
```

**Developer B (PR Review):**
```bash
/review #123
# Runs four-phase checklist against PR
# Reports bugs, security, conventions, breaking changes
# Returns verdict: approve | comment | request-changes
```

**DevOps (Pre-Deploy):**
```bash
/deploy-check main
# Forks into sub-agent for verbose discovery
# Checks: uncommitted changes, migrations, CI status
# Returns only pass/fail summary to main session
```
