---
name: api
paths:
  - src/api/**/*
---

# API handler rules

When editing any file under `src/api/`, enforce these concrete patterns to keep error handling and schemas consistent across the team.

## Error handling: Use ApiError instead of raw throw

❌ **Forbidden:**
```javascript
if (!user) throw new Error("user not found");  // Generic 500; hides the real cause
```

✅ **Required:**
```javascript
if (!user) throw ApiError(404, "USER_NOT_FOUND", "User not found");
```

Rationale: Raw `Error` throws become generic 500s. Structured `ApiError` gives clients a recoverable error code so they know whether to retry, refresh auth, or show an error message.

## Response schemas: Update schema when adding fields

❌ **Forbidden:**
```javascript
// src/api/carts.ts: return new field
return { items, total: 9.99, discount: 2.00 };  // discount not in CartResponse schema
```

✅ **Required:**
```javascript
// src/api/_schemas/responses/Cart.ts: add field first
export type CartResponse = { items: Item[]; total: number; discount: number };

// src/api/carts.ts: use updated schema
return { items, total: 9.99, discount: 2.00 };
```

Rationale: Schemas are contracts. Unschemed fields cause client parsing errors in production. Schema and handler must be in sync in the same commit.

## Inputs: Validate at the boundary

All request bodies are validated using `zod` schemas in `src/api/_schemas/`. Do not re-validate inside the handler — assume the body shape is correct after boundary validation.
