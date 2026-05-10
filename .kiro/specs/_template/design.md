# Technical Design: {Feature Name}

> **Created**: YYYY-MM-DD

## Architecture Overview

```
[Frontend] → [Backend API] → [Service] → [Repository] → [PostgreSQL]
/{feature}    /api/v1/{feature}  {Feature}Service  {Feature}Repository
```

## DB Schema Changes

> Delete this section if no changes are needed.

| Item | Details |
|------|---------|
| Target table | `table_name` |
| Change type | Add column / New table / Add index |
| Change details | {specific changes} |
| Impact on existing data | None / {migration method} |
| **Approval status** | [ ] Requires approval |

## Shared Type Definitions

Add to `shared/src/types/{type-file}.ts`:

```typescript
export type {FeatureType} = {
  id: number;
  // field definitions
};
```

## Backend Implementation

| Layer | File Path |
|-------|-----------|
| Zod schema | `backend/src/shared/schemas/{feature}Schema.ts` |
| Repository | `backend/src/shared/repositories/{feature}.repository.ts` |
| Service | `backend/src/shared/services/{feature}.service.ts` |
| Route | `backend/src/api/routes/v1/{feature}.ts` |

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/{feature}` | List retrieval |
| GET | `/api/v1/{feature}?id={id}` | Detail retrieval (no dynamic routes) |
| POST | `/api/v1/{feature}` | Create |
| PATCH | `/api/v1/{feature}?id={id}` | Update |
| DELETE | `/api/v1/{feature}?id={id}` | Delete (logical delete) |

## Frontend Implementation

| Type | File Path |
|------|-----------|
| Type definitions | `frontend/src/apis/{feature}/types.ts` |
| API hook | `frontend/src/apis/{feature}/use{Feature}.ts` |
| Feature | `frontend/src/features/{feature}/` |
| Page | `frontend/src/app/{path}/page.tsx` |

## Test Plan

| Type | Target | File |
|------|--------|------|
| Repository unit | DB operations | `backend/tests/unit/repositories/{feature}.repository.test.ts` |
| Service unit | Business logic | `backend/tests/unit/services/{feature}.service.test.ts` |
| Route mock | API endpoints | `backend/tests/integration/{feature}.mock.test.ts` |
| Frontend E2E | Screen operations | `frontend/tests/testcases/{feature}/` |

## ADR Compliance Checklist

- [ ] **ADR-001**: No dynamic routes (`/[id]/` prohibited, use query parameters)
- [ ] **ADR-002**: `database/prisma/schema.prisma` is the single schema source
- [ ] **ADR-003**: Standard response format `{ contents, totalCount, offset, limit }`
- [ ] **ADR-004**: Awilix DI (Repository=TRANSIENT, Service=SCOPED)
- [ ] **ADR-005**: Logical delete only (`DELETE` statements prohibited)
- [ ] **ADR-006**: Optimistic lock (`version` field, check, increment)
- [ ] **ADR-007**: Use `dateUtils` (`new Date()` direct use prohibited)
- [ ] **ADR-008**: ESModules `.js` extension imports
