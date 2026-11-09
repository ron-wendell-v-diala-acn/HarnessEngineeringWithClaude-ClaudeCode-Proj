---
name: review
description: Codified PR review checklist for the monorepo
argument-hint: "pr reference (e.g. origin/main...origin/feature-branch)"
allowed-tools:
  - Glob
  - Grep
  - Read
---

# PR Review Checklist

This command guides a structured review of pull requests against team conventions. It operates in read-only mode — no modifications.

## Must report

The reviewer must explicitly confirm each criterion:

- **Standards compliance:** Do all changed files follow the applicable standards from `.claude/standards/` and path-scoped rules in `.claude/rules/`? (e.g., API handlers use `ApiError`, React components have exhaustive dependency arrays)
- **Schema contracts:** Any API response schema changes appear in `src/api/_schemas/responses/` in the same commit?
- **Database safety:** If migrations were added, are they forward-only? Do they avoid destructive operations without a deprecation phase?

## Skip criteria

These failures do not block review approval but must be logged:

- **Trivial test gaps:** A new component has no test file. (A new integration test should have one. A new utility function may not need a test if it's trivial.)
- **Comments:** New code lacks JSDoc comments. (Only docstrings for public APIs and non-obvious utility functions are required.)

## Code examples

### Input: PR branch with multiple files

```
git diff origin/main...origin/add-cart-feature
# Modifies:
#   src/components/Cart.tsx (adds UI for discount)
#   src/hooks/useCart.ts (adds discount state)
#   src/api/carts.ts (new endpoint for discount validation)
#   tests/Cart.test.tsx (tests discount UI interaction)
```

The review examines this diff scope across multiple files.

### Output: Structured feedback with interacting issues

```
✅ Standards compliance: All API handlers use ApiError. React components have exhaustive deps.
✅ Schema contracts: Cart response schema updated in same commit.
⚠️ Trivial gap: Discount validation tests only cover happy path. Not critical for MVP.

Summary: Standards followed. Ready to merge.
```

### Output: With discovered gaps (related checks)

```
⚠️ Standards gap #1: New endpoint src/api/carts.ts uses ApiError correctly.
⚠️ Standards gap #2: Response schema in CartItem.ts not updated — new discount field is unschemed.
❌ Schema contract: These issues are bundled — fix the schema in the same commit as the handler.
```

## Interacting vs. independent guidance

- **Interacting issues** (bundle together): Schema mismatches with response fields, error handling inconsistencies, multi-file refactors where context matters.
- **Independent issues** (check sequentially): Missing test files, missing comments, straightforward naming inconsistencies.

This command is **interacting** — it asks the author for context and uses their response to shape the review. This prevents false positives.

## Interview pattern

Before running the review, ask the author:

> Are there any known gaps in this PR or areas where the standards are intentionally bent?

Use the author's response to contextualize the review output — some deviations are acceptable if intentional and documented.
