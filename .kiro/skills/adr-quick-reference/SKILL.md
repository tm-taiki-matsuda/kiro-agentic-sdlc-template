---
name: "ADR Quick Reference"
description: "Architecture Decision Records quick reference. Violation vs. correct examples for ADR-001 through ADR-008. Referenced by code-review when detecting violations, and by all agents before implementation."
---

# ADR Quick Reference

Eight Architecture Decision Records.
Check for violations before implementation and during review.

---

## ADR-001: No Dynamic Routes (use `?id=` query parameters)

**Decision**: Do not use Next.js `[id]` dynamic routes. Use `?id=123` query parameters for single-item retrieval.

| ❌ Wrong | ✅ Correct |
|---------|-----------|
| `frontend/src/app/.../[id]/page.tsx` | `frontend/src/app/.../detail/page.tsx` |
| `const { id } = useParams()` | `const id = useSearchParams().get('id')` |
| `router.push('/path/123')` | `router.push('/path/detail?id=123')` |
| Backend: `/api/v1/items/:id` | Backend: `/api/v1/items?id=123` |

**Review check**: Verify no `[id]` directory exists under `frontend/src/app/`.

---

## ADR-002: `database/prisma/schema.prisma` is the Single Source of Truth

**Decision**: Only directly edit `database/prisma/schema.prisma`.
`backend/prisma/schema.prisma` and `functions/prisma/schema.prisma` are **generated files** (direct editing prohibited).

| ❌ Wrong | ✅ Correct |
|---------|-----------|
| Directly edit `backend/prisma/schema.prisma` | Edit `database/prisma/schema.prisma` then run `npm run db:generate` |
| Directly modify `functions/prisma/schema.prisma` | Run migrate in `database/`, then generate in each package |

---

## ADR-003: Standard Response Format

**Decision**: List APIs must always return `{ contents, totalCount, offset, limit }` format.

| ❌ Wrong | ✅ Correct |
|---------|-----------|
| `return reply.send(items)` | `return reply.send({ contents: items, totalCount: 100, offset: 0, limit: 20 })` |
| `return { data: items }` | `return { contents: items, totalCount, offset, limit }` |

**Frontend type definition**:
```typescript
interface ListResponse<T> {
  contents: T[];
  totalCount: number;
  offset: number;
  limit: number;
}
```

---

## ADR-004: Awilix DI Pattern

**Decision**: Repository = TRANSIENT scope, Service = SCOPED scope.

| Layer | Scope | Reason |
|-------|-------|--------|
| Repository | TRANSIENT | New instance per request (Prisma transaction safety) |
| Service | SCOPED | Shared within request (transaction boundary) |

**DI resolution in Route layer**:
```typescript
// Always use this pattern
const service = request.diScope.resolve<ItemService>("itemService");
// NOT: new ItemService(...)
```

---

## ADR-005: Logical Delete Only (no DELETE)

**Decision**: Physical deletion of data is prohibited. Use logical delete by updating `is_deleted = true`.

| ❌ Wrong | ✅ Correct |
|---------|-----------|
| `prisma.xxx.delete({ where: { id } })` | `prisma.xxx.updateMany({ where: { id }, data: { is_deleted: true } })` |
| `DELETE FROM table WHERE id = $1` | `UPDATE table SET is_deleted = true WHERE id = $1` |

**Required in all queries**:
```typescript
// All findMany/findFirst/$queryRaw must include is_deleted = false filter
WHERE id = ${id} AND is_deleted = FALSE
```

---

## ADR-006: Optimistic Lock Required (version field)

**Decision**: All update and delete operations must use optimistic locking. Detect conflicts with the `version` field.

| ❌ Wrong | ✅ Correct |
|---------|-----------|
| `UPDATE table SET ... WHERE id = $1` | `UPDATE table SET ..., version = version + 1 WHERE id = $1 AND version = $2` |
| Update without version check | 0 rows updated → throw `ConflictError` |
| Frontend: not sending version | Frontend: include `version: number` in update mutation body |

**Implementation pattern**:
```typescript
// Repository layer: update with optimistic lock
const result = await this.prisma.$queryRaw`
  UPDATE table SET ..., version = version + 1
  WHERE id = ${id} AND version = ${version} AND is_deleted = FALSE
  RETURNING id, version
`;
// empty result → throw ConflictError in Service layer

// Service layer
const updated = await repository.update(id, data, version, userId);
if (!updated) throw new ConflictError("Data has been updated.");

// Frontend: explicitly handle 409
if (error.response?.status === 409) {
  setError("This data has been updated by another user. Please reload the page.");
}
```

---

## ADR-007: Use `getCurrentDate()` for Date Retrieval (`new Date()` prohibited)

**Decision**: Direct use of `new Date()` is prohibited. Use `getCurrentDate()` to enable date mocking in tests.

| ❌ Wrong | ✅ Correct |
|---------|-----------|
| `const now = new Date()` | `const now = getCurrentDate()` |
| `created_at: new Date()` | `created_at: getCurrentDate()` |
| `new Date().toISOString()` | `getCurrentDate().toISOString()` |

**Import**:
```typescript
import { getCurrentDate } from "../utils/date-utils.js";
```

---

## ADR-008: ES Modules — `.js` Extension Required for Imports (Backend)

**Decision**: Backend (Node.js ESM) TypeScript file imports must always include the `.js` extension.

| ❌ Wrong | ✅ Correct |
|---------|-----------|
| `import { ItemService } from './item.service'` | `import { ItemService } from './item.service.js'` |
| `import type { ... } from '../repositories/repo'` | `import type { ... } from '../repositories/repo.js'` |

**Scope**: All imports under `backend/src/` and `functions/src/`
**Excluded**: `frontend/src/` (Next.js does not require extensions)

---

## Review Checklist

```
□ ADR-001: No [id] directory under frontend/src/app/
□ ADR-003: List response is { contents, totalCount, offset, limit } format
□ ADR-005: No prisma.xxx.delete() or DELETE FROM
           All queries have is_deleted = FALSE filter
□ ADR-006: Update operations have version check
           0-row update throws ConflictError
           Frontend update mutation includes version field
□ ADR-007: No direct use of new Date()
□ ADR-008: No backend imports missing .js extension
```
