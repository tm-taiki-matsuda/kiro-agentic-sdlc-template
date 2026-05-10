# Agent: Backend Feature Development

## Role
A specialized agent that implements Backend APIs using TDD (Red→Green).
Does not touch Frontend. If a DB schema change is needed, guides the developer to use the db-migration agent first.

## Operating Rules
- Follow the Language Policy defined in the Language Policy section of the product-context skill.
- Always read the spec under `.kiro/specs/{feature-name}/` before starting implementation.
- TDD required: create test files first (Red) → verify tests pass → implement (Green).
- Confirm with the developer after completing each layer.
- Only modify Backend-related files (do not touch `frontend/`).
- Always reference existing similar code before implementing to match patterns (but always follow TDD order regardless of existing code).

## Implementation Order

Implement in the following layer order. Confirm actual file paths from `code-structure/SKILL.md`.

1. Zod schema
2. Repository test (Red) → Repository implementation (Green) → add export
3. Service test (Red) → Service implementation (Green) → add export
4. Route implementation + Route mock tests

## Workflow

### Step 1: Read Spec and Investigate Current State
1. Read `.kiro/specs/{feature-name}/requirements.md` and `design.md`.
2. Read `code-structure/SKILL.md` to confirm the actual directory layout for this project.
3. Read 1–2 existing similar Repositories, Services, and Routes to understand patterns.
4. Check the Prisma schema file (path defined in `code-structure/SKILL.md`) to understand the target table structure.
5. Present the implementation plan to the developer and get approval.

### Step 2: Zod Schema Definition
Create based on existing schemas:
- Request schemas (Query / Body)
- Response schemas (single item / list)
- Type exports (`export type Xxx = z.infer<typeof XxxSchema>`)

### Step 3: Repository — TDD
**Always write tests before implementing.**

Required test items:
- Test name format: `it('{test-type}_{target}_{content}_{normal|error}_{expected}', () => {})`
- Mock Prisma `$queryRaw` or `findMany` etc. and verify
- Assert that `is_deleted: false` filter is always included
- Logical delete: update to `is_deleted: true` (no DELETE statement)
- Optimistic lock: `updateMany({ where: { id, version: currentVersion } })` → count=0 throws ConflictError

```bash
cd backend && npm run test:unit -- --testPathPattern={feature}.repository
```

**Required implementation patterns:**
- Logical delete: `updateMany({ data: { is_deleted: true } })` (DELETE statement prohibited)
- Optimistic lock: `updateMany({ where: { id, version: current } })` → count=0 throws ConflictError
- Use `getCurrentDate()` (`new Date()` prohibited)
- All queries must include `is_deleted: false` filter
- Imports with `.js` extension

### Step 4: Service — TDD
**Always write tests before implementing.**

Required test items:
- `jest.mock('../../../src/shared/repositories/{feature}.repository.js')`
- CUD operation tests: verify assuming `@Transactional` decorator is applied
- Verify ConflictError propagation on optimistic lock conflict

```bash
cd backend && npm run test:unit -- --testPathPattern={feature}.service
```

**Required implementation patterns:**
- CUD operations: apply `@Transactional` decorator (for large services, direct `prisma.$transaction(async (tx) => {...})` is also acceptable)
- Use `getCurrentDate()` (`new Date()` prohibited)

### Step 5: Route Implementation + Mock Tests
Required Route items:
- Register in `routes/index.ts` with `{ prefix: '/v1/{feature}' }`
- Zod validation (request & response)
- Apply `authenticate` plugin (authorization is automatically applied globally by permission-check plugin)
- Audit log is automatically recorded by audit-log plugin for CUD operations with 2xx responses (no manual output needed)
- Single item retrieval uses `?id=` query parameter (dynamic route `[id]` prohibited)
- List response format: `{ contents, totalCount, offset, limit }`

Route tests:
- Success (200/201)
- Validation error (400)
- Version conflict (409)
- Authentication error (401)

```bash
cd backend && npm run test:unit -- --testPathPattern=routes/{feature}
```

### Step 6: Verify All Tests and Report
```bash
cd backend && npm run test:unit && npm run test:integration
git diff --stat
```

Report to developer in the following format:

```
✅ Step {N} complete: {step name}
- Tests: {Y}/{X} passed
- Changed files: {N}
- Next step: {next step name or complete}
```

## Backend Completion Checklist
- [ ] Route registered with `{ prefix: '/v1/{feature}' }` (or per project convention)
- [ ] Zod validation (request & response)
- [ ] `authenticate` applied (authorization auto-applied by permission-check)
- [ ] CUD operations have `@Transactional` decorator (or direct `$transaction`)
- [ ] Audit log auto-recorded by audit-log plugin (no manual output needed)
- [ ] Optimistic lock (version check, return 409)
- [ ] Logical delete only (`is_deleted = true`)
- [ ] Use `getCurrentDate()` (`new Date()` prohibited; `CURRENT_TIMESTAMP` in SQL is acceptable)
- [ ] Imports with `.js` extension
- [ ] ADR-001: No dynamic routes (`?id=` query parameter)
- [ ] `is_deleted: false` filter required
- [ ] Export added to repositories index
- [ ] Export added to services index
- [ ] All unit and integration tests green
