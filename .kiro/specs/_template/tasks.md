# Implementation Tasks: {Feature Name}

> **Created**: YYYY-MM-DD  
> **Agent**: feature-dev  
> **Last updated**: YYYY-MM-DD

## Status Legend

- `[TODO]` — Not started
- `[IN_PROGRESS]` — In progress
- `[DONE]` — Complete

---

## Phase 0: Design & Approval

- [TODO] Read design documents (`design/features/`, `design/api/specs/`) to understand the spec
- [TODO] Present DB schema change proposal to developer and get approval
- [TODO] Confirm implementation plan with developer

---

## Phase 1: Backend Implementation (TDD order)

### Shared Type Definitions
- [TODO] Add type definitions to `shared/src/types/{type-file}.ts`
  - _Requirements: {corresponding requirement numbers}_

### Zod Schema
- [TODO] Create `backend/src/shared/schemas/{feature}Schema.ts`
  - _Requirements: {validation requirement numbers}_

### Repository (Red → Green → Refactor)
- [TODO] Create `backend/tests/unit/repositories/{feature}.repository.test.ts` (Red)
  - _Requirements: {happy path, logical delete, optimistic lock requirement numbers}_
- [TODO] Implement `backend/src/shared/repositories/{feature}.repository.ts` (Green)
- [TODO] Add export to `backend/src/shared/repositories/index.ts`

### Service (Red → Green → Refactor)
- [TODO] Create `backend/tests/unit/services/{feature}.service.test.ts` (Red)
  - _Requirements: {business rule requirement numbers}_
- [TODO] Implement `backend/src/shared/services/{feature}.service.ts` (Green)
- [TODO] Add export to `backend/src/shared/services/index.ts`

### Route
- [TODO] Create `backend/src/api/routes/v1/{feature}.ts`
  - _Requirements: {API endpoint requirement numbers}_
- [TODO] Register in `backend/src/api/routes/index.ts`
- [TODO] Create and pass `backend/tests/integration/{feature}.mock.test.ts`
  - _Requirements: {authorization, authentication error requirement numbers}_

### Backend All Tests
- [TODO] `cd backend && npm run test:unit` green
- [TODO] `cd backend && npm run test:mock` green
- [TODO] `cd backend && npm run test:integration` green

---

## Phase 2: Frontend Implementation (TDD order)

### API Hook
- [TODO] Type definitions in `frontend/src/apis/{feature}/types.ts`
  - _Requirements: {API response type requirement numbers}_
- [TODO] Implement hook in `frontend/src/apis/{feature}/use{Feature}.ts`
  - _Requirements: {data fetch/update requirement numbers}_
- [TODO] Create and pass hook unit tests
  - _Requirements: {409 error, network error requirement numbers}_

### Feature Components
- [TODO] Implement components in `frontend/src/features/{feature}/`
  - _Requirements: {screen display, validation requirement numbers}_
- [TODO] Implement page `frontend/src/app/{path}/page.tsx`
  - _Requirements: {screen navigation, authorization requirement numbers}_

### E2E TypeScript Keyword-Driven Tests
- [TODO] Create Page Object `frontend/tests/pages/{Feature}Page.ts`
  - _Requirements: {screen element selector definitions}_
- [TODO] Create Keywords `frontend/tests/keywords/{Feature}Keywords.ts`
  - _Requirements: {business operation methods}_
- [TODO] Register Keywords in `frontend/tests/keywords/index.ts`
- [TODO] Create test cases `frontend/tests/testcases/{IT-ID}-{FEATURE}-{NNN}.spec.ts`
  - _Requirements: {happy path, validation, permission error requirement numbers}_
- [TODO] `cd frontend && npm run test:keyword -- --grep "{IT-ID}"` green

---

## Phase 3: Final Verification

- [TODO] Verify change scope is minimal with `git diff --stat`
- [TODO] Verify all requirements are implemented and tested (cross-reference with requirements.md)
- [TODO] Verify all required checklist items (ADR compliance, authentication, authorization, audit log)
- [TODO] Request developer review

## Completion Criteria

- [ ] All tests green (unit / mock / integration / e2e)
- [ ] Tests exist for all requirements in requirements.md
- [ ] All ADR compliance checklist items complete
- [ ] Developer review complete
- [ ] Create `tasks/handoff-{feature}.md` if needed
