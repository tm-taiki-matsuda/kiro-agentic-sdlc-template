---
name: "Test Framework"
description: "E2E Keyword-Driven 3-layer tests, Backend test strategy, Frontend unit tests, test data management, and coverage goals. Referenced by test-related agents."
---

# Test Framework

## Test Philosophy

> "Express scenarios by combining Keywords written in TypeScript"

Separate into 3 layers: Page Object (selector operations) → Keywords (business language) → TestCase (scenarios).
Changes to business rules only require modifying the Keywords layer, and all test cases are automatically updated.

## Frontend E2E Tests (TypeScript Keyword-Driven + Playwright)

### Directory Structure (3-Layer Architecture)

```
frontend/tests/
├── pages/               ← Layer 1: Page Object (Playwright selector operations)
│   ├── BaseRegisterPage.ts   ← base class for all Page Objects (always extend)
│   └── {Screen}RegisterPage.ts
├── keywords/            ← Layer 2: Keywords (business-language methods)
│   ├── index.ts              ← aggregates all Keywords (always register new ones here)
│   └── {Screen}RegisterKeywords.ts
└── testcases/           ← Layer 3: TestCase (test scenarios)
    └── {IT-ID}-{FEATURE}-{NNN}.spec.ts
```

### Test Case File Format (TypeScript)

```typescript
// frontend/tests/testcases/IT-F001-ITEM-001.spec.ts
import { test } from '@playwright/test';
import { Keywords } from '../keywords';

test.describe('IT-F001: Item Registration_Happy Path', () => {

  test('happy-path_basic-info-registration_complete', async ({ page }) => {
    test.setTimeout(300000);
    const k = new Keywords(page);

    await k.login.loginAsTestUser1();
    await k.itemRegister.openItemRegistrationScreen();
    await k.itemRegister.fillBasicInfo({
      name: 'E2E_Item_' + new Date().toISOString().slice(0, 10),
      category: 'test-category',
    });
    await k.itemRegister.completeRegistration();
  });

  test('validation_name-empty_required-error-shown', async ({ page }) => {
    test.setTimeout(300000);
    const k = new Keywords(page);

    await k.login.loginAsTestUser1();
    await k.itemRegister.openItemRegistrationScreen();
    await k.itemRegister.attemptRegistrationWithEmptyFields();
    await k.itemRegister.verifyValidationError('Name is required');
  });
});
```

### Selector Priority (always follow this order)

| Priority | Selector | Use case |
|----------|---------|---------|
| 1 | `getByRole('button', { name: '...' })` | buttons, links |
| 2 | `getByLabel('...')` | text inputs, checkboxes |
| 3 | `getByRole('combobox', { name: '...' })` | select boxes |
| 4 | `getByRole('option', { name: '...' })` | select options |
| 5 | `locator('[data-testid="..."]')` | only when above cannot be used |

### Test Execution

```bash
cd frontend
npm run test:keyword                              # run all tests
npm run test:keyword -- --grep "IT-F001"         # filter by IT-ID
npm run test:e2e:ui                              # Playwright UI mode for debugging
```

### Test File Naming Convention

```
{IT-ID}-{FEATURE}-{NNN}.spec.ts

Examples:
IT-F001-ITEM-001.spec.ts   ← items feature, 1st test
IT-F002-ORDER-001.spec.ts  ← orders feature, 1st test

test.describe name: "{IT-ID}: {Screen}_{test overview}"
test name: "{happy-path/validation/error-case}_{action}_{expected result}"
```

### Test Design Criteria (per screen)

Cover the following for each screen:
1. **Happy path**: normal operation flow (list display, search, register, edit)
2. **Validation errors**: required field empty, invalid format, cross-field (date order, etc.)
3. **Authorization**: operation restrictions for unauthorized users
4. **Error cases**: user display when API returns error
5. **Boundary values**: max character count, zero-item display

## Backend Test Strategy

### Test Classification

| Type | File naming | External deps | Speed | CI |
|------|------------|--------------|-------|-----|
| Mock test | `*.mock.test.ts` | none | seconds | required |
| Unit test | `*.test.ts` | none/mocked | seconds | required |
| DB integration test | `*.db.test.ts` | PostgreSQL required | minutes | optional |

### Test File Structure

```
backend/tests/
├── unit/
│   ├── repositories/    # uses Prisma mock
│   └── services/        # uses Repository mock
└── integration/
    ├── {feature}.mock.test.ts   # uses x-api-mock: true header
    └── {feature}.db.test.ts     # real PostgreSQL
```

### Mock Test Pattern

```typescript
// use x-api-mock: true header to use mock data
const response = await app.inject({
  method: 'GET',
  url: '/api/v1/items',
  headers: { 'x-api-mock': 'true' },
});
expect(response.statusCode).toBe(200);
```

## Frontend Unit Tests (Jest + React Testing Library)

### Test File Placement

Place in the same directory as the component:
```
src/app/.../page.tsx
src/app/.../page.test.tsx
```

### Next.js Hook Mocking (required)

```typescript
// jest.mock() must be placed before import statements
const mockPush = jest.fn();
jest.mock('next/navigation', () => ({
  useRouter: () => ({ push: mockPush }),
  useSearchParams: () => new URLSearchParams(),
}));
```

### What to Test vs. Not Test

**Test ✅**
- Title and main UI element display
- Navigation triggered by button clicks
- URL parameter display verification

**Do not test ❌**
- Complex business logic (handled inside custom hooks)
- API communication (mock it, don't make real calls)
- Detailed user interactions (handled by E2E tests)

## Test Data Management

```
database/data/             # master data (CSV/Excel)
backend/src/api/mocks/     # API mock data (JSON)
backend/tests/test_data/   # test seed data
```

## Coverage Goals

- Backend unit: critical paths of business logic (services/repositories)
- Frontend unit: display and navigation of main components
- E2E: all happy path scenarios for each screen
