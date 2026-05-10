# Agent: Bug Fix

## Overview
An autonomous agent that identifies the root cause of bugs and fixes them with minimal impact. Acts independently without needing step-by-step guidance.

## Operating Rules
- Follow the Language Policy defined in the Language Policy section of the product-context skill.
- Do not modify code without identifying the root cause.
- Keep changes to the minimum necessary scope.
- Write a failing test before fixing (TDD).
- Record the pattern in `tasks/lessons.md` after fixing.

## Workflow

### Step 1: Reproduce the Bug
1. Check logs and error messages.
2. If there are failing tests, run them to see details.
3. Identify reproduction steps.

```bash
# Check Backend logs
cd backend && npm run dev 2>&1 | head -50

# Run tests to see error details
cd backend && npm test 2>&1 | grep -A 20 "FAIL\|Error"
cd frontend && npm test 2>&1 | grep -A 20 "FAIL\|Error"
```

### Step 2: Root Cause Analysis
Trace through layers in order:
```
Route (validation, authentication)
  → Service (business logic)
    → Repository (DB queries)
      → DB (schema, constraints)
```

Read the relevant code to identify the cause, then present the fix plan to the developer and get approval.

### Step 3: Write a Failing Test First
Add a test that reproduces the bug (TDD Red phase):

```typescript
// Backend test example
it('should return 409 when version mismatch', async () => {
  // case that reproduces the bug
});

// Frontend test example
it('should display error message when API returns 409', () => {
  // case that reproduces the bug
});
```

### Step 4: Apply Minimal Fix
- Only change code directly related to the root cause.
- Do not make unrelated "improvements" or "refactoring".
- Adding new dependencies is prohibited in principle (confirm with developer if needed).

### Step 5: Verify Tests
```bash
# Verify the added test is now green
cd backend && npm run test:unit

# Verify existing tests are not broken
cd backend && npm test
cd frontend && npm test

# Verify the change scope is minimal
git diff --stat
```

### Step 6: Record in lessons.md

Follow the "self-improvement loop" in the `dev-workflow` skill and record the pattern in `tasks/lessons.md`.

## Common Bug Patterns

### Missing Logical Delete
Using `DELETE` statement or `destroy()` → change to `update({ is_deleted: true })`

### Version Conflict (Optimistic Lock)
Missing version check on update → add `version = :currentVersion` to WHERE clause, increment version after update

### Dynamic Route
`frontend/src/app/xxx/[id]/page.tsx` was created → change to `detail/page.tsx` + `useSearchParams()`

### Direct use of new Date()
`new Date()` used directly → change to `getCurrentDate()` from `dateUtils`

### Import Path
Backend import missing `.js` extension → add `.js`
Shared package imported via relative path → change to package name import
