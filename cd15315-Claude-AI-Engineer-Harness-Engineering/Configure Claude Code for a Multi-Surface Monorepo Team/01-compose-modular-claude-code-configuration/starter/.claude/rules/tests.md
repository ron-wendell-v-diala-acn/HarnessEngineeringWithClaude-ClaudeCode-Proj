---
name: tests
paths:
  - "**/*.test.ts"
  - "**/*.test.tsx"
---

# Test file rules

When editing co-located test files (`*.test.ts` / `*.test.tsx`), these rules layer on top of the frontend or API standards:

- **Real database in integration tests:** Repository tests and multi-module integration tests hit a real PostgreSQL test instance (via Docker Compose in CI). Mocking the database layer is forbidden — we've been burned by mocked tests that hid broken migrations. If you're testing repository functions, spin up the test DB.
- **Component tests assert user behavior, not internal state:** Test rendered output and user-visible outcomes (click → dialog appears). Do not assert on hook state, internal refs, or implementation details — those are fragile and hide refactoring opportunities.
- **API handler tests call the function directly:** No HTTP fixtures needed. Call the handler with a request shape and assert on the `{ status, body }` return value. This keeps tests fast and deterministic.
