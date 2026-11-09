---
name: deploy-check
description: Pre-deployment validation for e-commerce platform
context: fork
fork: true
allowed-tools:
  - Glob
  - Grep
  - Read
---

# Pre-Deployment Validation

This skill forks a sub-agent to perform read-only pre-deployment checks against the main session state. It helps catch issues before shipping.

**Rationale for forking:** The main session keeps its original context and conclusion. The fork runs checks independently and reports findings without altering the main session's understanding. This branching reality is essential for speculative validation — we check "what if we deploy this" without committing to that mental model.

## Three pre-deployment checks

1. **Schema consistency check**
   - PASS: All API response bodies in the codebase match schemas in `src/api/_schemas/responses/`.
   - FAIL: Any handler returns a field not in its schema definition.
   - Rationale: Response schema mismatches cause client-side parsing errors in production.

2. **Database migration safety**
   - PASS: All migrations in `src/db/migrations/` are forward-only (no destructive DDL).
   - FAIL: Any migration contains DROP COLUMN, DROP TABLE, or data-altering operations without deprecation phase.
   - Rationale: Irreversible migrations can corrupt data if they need to be rolled back.

3. **Handler error contract**
   - PASS: All expected failures in `src/api/` use `ApiError(status, code, message)`.
   - FAIL: Any handler contains direct `throw new Error(...)` statements (forbidden).
   - Rationale: Raw errors propagate as generic 500s, hiding the real cause from clients.

## Personal customization note

Adjust the three checks above to match your team's deployment checklist. Copy this skill to `~/.claude/skills/deploy-check/` and customize it. For example, if you use feature flags, add a check for uncommitted flag configs. If you maintain design tokens, verify sync with the codebase. Make this skill yours by forking it to your personal skills library.

## Skill vs. CLAUDE.md rubric

**Why this is a skill, not in CLAUDE.md:**
- ✅ **Forked sub-agent:** Speculative validation that branches the session state (main session untouched).
- ✅ **Read-only:** Uses only read tools (Glob, Grep, Read).
- ✅ **On-demand:** Runs when explicitly invoked (`/deploy-check`).
- ❌ **NOT always-loaded:** CLAUDE.md is for shared conventions all sessions load automatically. This is a one-off validation flow.

**CLAUDE.md is for:** Conventions, standards, path rules (always active).
**Skills are for:** Workflows, validations, forked operations (on-demand).

This distinction keeps the main session lightweight while enabling heavy-duty pre-deployment checks on request.
