---
name: "Error Handling Pattern"
description: "Backend AppError hierarchy, HTTP status mapping, Fastify error-handler plugin, Frontend getErrorMessage, and 409 conflict handling cross-cutting flow. Referenced by bug-fix and backend-feature/frontend-feature when implementing or fixing error handling."
---

# Error Handling Pattern

The full error flow spanning Backend → Frontend.

---

## Backend: AppError Hierarchy

> **`AppError` and its subclasses are examples from the default project setup.
> Replace with your project's actual error class names and HTTP mappings.**

```typescript
// example: backend/src/shared/errors/AppError.ts
AppError (base)          → HTTP 500
├── NotFoundError        → HTTP 404  "Resource not found"
├── ValidationError      → HTTP 400  "Input validation error"
├── ConflictError        → HTTP 409  "Resource conflict"
└── ForbiddenError       → HTTP 403  "Access denied"
```

### When to Use Each Error

| Error | Where | Trigger |
|-------|-------|---------|
| `ConflictError` | Service layer | Optimistic lock failure (version mismatch) |
| `NotFoundError` | Repository / Service | No result with `is_deleted=false` |
| `ForbiddenError` | Service layer | Insufficient role (fine-grained check that authorize plugin can't handle) |
| `ValidationError` | Service layer | Business rule violation that Zod can't catch |
| `AppError` | Service layer | Other business errors |

### Usage Pattern in Service Layer

```typescript
import { ConflictError, NotFoundError } from '../errors/AppError.js';

// Optimistic lock
const updated = await repository.update(id, data, version, userId);
if (!updated) throw new ConflictError();

// Existence check
const item = await repository.findById(id);
if (!item) throw new NotFoundError();
```

---

## Backend: error-handler Plugin

`backend/src/api/plugins/error-handler.ts` converts all errors to unified responses:

```typescript
// AppError → { reqId, error: "ConflictError", message: "Resource conflict" }
// ZodError → { reqId, error: "ValidationError", fields: [...], errors: [...] }
// Unknown  → { reqId, error: "InternalServerError", message: "An error occurred" }
```

**Security**: Do not include error details (stack traces, etc.) in 500 error responses.

---

## Frontend: getErrorMessage

```typescript
// frontend/src/utils/errorHandler.ts
import { getErrorMessage } from '@/utils/errorHandler';

// Usage (inside custom hook)
try {
  await mutation.mutateAsync(data);
} catch (err) {
  setError(getErrorMessage(err));
}
```

### Status-to-Message Mapping

| HTTP | Display example |
|------|----------------|
| 400 | Prefer server message |
| 401 | Authentication error |
| 403 | Permission error |
| 404 | Resource not found |
| 409 | Data has been updated |
| 500 | System error |

---

## 409 Conflict Handling (End-to-End)

```
[Frontend] PUT /api/items?id=1  body: { ..., version: 3 }
    ↓
[Route] Zod validation → Service call
    ↓
[Service] repository.update(id, data, version=3, userId)
    ↓
[Repository] UPDATE ... WHERE id=1 AND version=3 → 0 rows affected
    ↓
[Service] throw new ConflictError()
    ↓
[error-handler] → HTTP 409 { error: "ConflictError", message: "Resource conflict" }
    ↓
[Frontend] getErrorMessage(err) → "This data has been updated by another user..."
    ↓
[UI] Display error message + prompt user to reload
```

### Explicit 409 Handling on Frontend

```typescript
// inside custom hook
if (axiosErr.response?.status === 409) {
  setError('This data has been updated by another user. Please reload the page.');
  queryClient.invalidateQueries({ queryKey: ['{feature}'] });
}
```

---

## Error Verification Patterns in Tests

### Backend Mock Test

```typescript
it('returns 409 on version conflict', async () => {
  const response = await app.inject({
    method: 'PUT',
    url: '/api/items?id=1',
    headers: { 'x-api-mock': 'true', authorization: 'Bearer token' },
    payload: { ...validData, version: 999 },
  });
  expect(response.statusCode).toBe(409);
  expect(JSON.parse(response.body).error).toBe('ConflictError');
});
```

### Frontend Test

```typescript
it('displays error message on 409 error', async () => {
  server.use(
    http.put('/api/items', () => HttpResponse.json(
      { error: 'ConflictError', message: 'Resource conflict' },
      { status: 409 }
    ))
  );
  // ... run mutation → verify error message is displayed
});
```
