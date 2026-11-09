# E-Commerce Platform — Shared Claude Code Conventions

This file is the **project-level** entry point for the e-commerce monorepo. Every teammate's Claude session loads it automatically.

## Scope: what belongs here vs. elsewhere

| Scope | Purpose | Shared? | Example |
|-------|---------|---------|---------|
| **Project-level** (`./CLAUDE.md`, `.claude/`) | Team conventions, shared standards, path-scoped rules | ✅ Via version control | Language choice, async patterns, import rules |
| **User-level** (`~/.claude/`) | Personal preferences, local development setup | ❌ NOT shared | Preferred commit message template, local path aliases |
| **Directory-level** (subdir `CLAUDE.md`) | Overrides for specific subdirectories | ✅ Via version control | Special rules for monorepo workspace |

This layered approach keeps team conventions visible and version-controlled while allowing individuals to customize their own working environment without affecting teammates.

## Shared standards (modular via @-imports)

The actual conventions live in focused files so this entry point stays scannable:

@.claude/standards/frontend.md
@.claude/standards/api.md
@.claude/standards/database.md
@.claude/standards/testing.md

Path-scoped rules in [.claude/rules/](.claude/rules/) layer on top of these standards and activate only when Claude is editing matching files (React components, API handlers, test files).

## Repository layout

```
src/components/   React components (functional + hooks)
src/pages/        Top-level routes
src/api/          Node.js API handlers
src/db/           PostgreSQL repository-pattern modules
```

Tests are co-located: `Foo.tsx` lives next to `Foo.test.tsx`.

## Troubleshooting

If a CLAUDE.md instruction isn't being followed, run `/memory` to see exactly which configuration files loaded for the current session.

## Team workflows

- `/review <pr-ref>` — codified PR review checklist. (You will author this in Exercise 2.)
- `/deploy-check` — read-only pre-deployment validation. (You will author this in Exercise 3.)

For decisions about when to use plan mode vs. direct execution on this codebase, you will produce a team decision doc in Exercise 4.
