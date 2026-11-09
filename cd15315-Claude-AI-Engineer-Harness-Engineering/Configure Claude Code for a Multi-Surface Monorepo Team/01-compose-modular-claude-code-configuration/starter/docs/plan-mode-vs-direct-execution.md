# Plan Mode vs. Direct Execution Decision Guide

This document helps the team decide when to use Claude Code's plan mode (explore + architecture first) versus direct execution (explore inline as you code).

## Plan Mode Example

**Scenario:** Implement a new cart state-management system replacing the current context-based approach. This spans 3 core files:
- `src/components/Cart.tsx` (UI needs refactoring)
- `src/hooks/useCart.ts` (state logic needs extraction)
- `src/api/carts.ts` (endpoint integration patterns)

The team is exploring React Context vs. Zustand, with architectural implications for performance and testing.

**Why plan mode:**
- Multiple valid architectural approaches exist (Redux, Zustand, new Context with hooks).
- Changes ripple across multiple files — 3+ core files will be modified with rework risk.
- Requires understanding existing state flow before committing to a direction.
- Team feedback needed on performance trade-offs. Plan mode prevents costly rework cycles from choosing the wrong architecture.

**Workflow:**
1. Run `/plan` to enter plan mode and signal architectural exploration.
2. Explore existing state usage across components and hooks.
3. Evaluate trade-offs (API shape, performance, testing story).
4. Present the architectural choice to the team for approval.
5. Exit plan mode and execute step-by-step with full context.

**Benefit:** Team alignment before refactoring a core system; fewer rework cycles.

## Direct Execution Example

**Scenario:** Add a new field `status: string` to the cart item response schema in `src/api/_schemas/responses/CartItem.ts`. Update the handler in `src/api/carts.ts` to include this field from the database.

**Why direct execution:**
- Clear implementation target (new response field following existing patterns).
- Only touches 2 focused files (schema definition, one handler function).
- No architectural decision needed — follow the established error handling patterns.

**Workflow:**
1. Read existing cart endpoint (`src/api/carts.ts`) to understand the handler contract.
2. Update schema: add field to `CartItem` response type.
3. Update handler: project the status field from the DB query.
4. Deploy.

**Benefit:** Fast iteration for straightforward tasks; no overhead.

## Explore Example

**Scenario:** Understand why test flakiness happens in cart validation tests. Verbose investigation needed to find the root cause without cluttering main session.

**Why explore inline:**
- The task is investigative (scratchpad discovery), not architectural.
- You'll read test patterns and code to find the root cause — verbose output should stay in exploration, not main session.
- Once the cause is identified (e.g., race condition, missing await), the fix is direct.

**Workflow:**
1. Use the explore agent in a sandboxed session to investigate test patterns.
2. Isolate the flaky assertion (likely an async timing issue).
3. Summarize findings for the main session.
4. Fix the test directly in the main session.

**Benefit:** Keeps verbose discovery output out of main session context; fast root-cause analysis.

## Combined Workflow Example

**Task:** Migrate user authentication from session cookies to JWT tokens across 3 files:
- `src/api/auth.ts` (auth endpoints)
- `src/pages/login.tsx` (login UI)
- `src/hooks/useSession.ts` (session state hook)

1. **Plan mode** (~40 min):
   - Explore current auth middleware and session handling patterns.
   - Identify all files that read/validate sessions.
   - Design JWT token structure and refresh strategy.
   - Get team sign-off on the approach before rework.

2. **Direct execution** (~2 hours):
   - Implement new auth middleware (replace session reader).
   - Update login/logout endpoints to return JWT.
   - Migrate client-side handling to localStorage.
   - Test end-to-end in a branch.

3. **Plan mode again** (if needed):
   - If edge cases emerge (revocation, cross-domain tokens), re-enter plan mode to reassess.

This hybrid workflow keeps large changes intentional while staying nimble on straightforward implementation.

## Decision Rubric

| Factor | Plan Mode | Direct Execution |
|--------|-----------|------------------|
| **Scope** | Multi-file (3+), architectural | Single file, well-scoped |
| **Clarity** | Unclear approach; needs exploration | Clear target, known pattern |
| **Team input** | Needed before implementation | Not needed; follow standards |
| **Rework risk: want to avoid costly false starts** | High (want to avoid false starts) | Low (following patterns) |
| **Files affected** | 3+ core files; cascading changes | 1-2 files; isolated changes |

## Knight-Webb Curriculum Citation

This decision framework is informed by the Knight-Webb curriculum on software engineering practices, specifically "SWE Is Becoming Plan and Review," which emphasizes intentional tool choice: plan when exploring complex multi-file systems, execute directly for routine work within established patterns.

For more guidance, see `.claude/commands/review.md` for PR review patterns and `.claude/skills/deploy-check/` for pre-deployment validation.
