---
name: "E2E Keyword-Driven Pattern"
description: "Implementation template for the Keyword-Driven 3-layer E2E test architecture (PageObject → Keywords → TestCase). Selector priority, naming conventions, and Keywords/index.ts registration procedure. Referenced by e2e-test agent when adding tests for new screens."
---

# E2E Keyword-Driven Test Implementation Pattern

## 3-Layer Architecture Overview

```
frontend/tests/
├── pages/               ← Layer 1: Page Object (Playwright selector operations)
│   ├── BaseRegisterPage.ts   ← always extend this
│   └── {Screen}Page.ts
├── keywords/            ← Layer 2: Keywords (business-language methods)
│   ├── index.ts              ← aggregates all Keywords (always register new ones here)
│   └── {Screen}Keywords.ts
└── testcases/           ← Layer 3: TestCase (scenarios)
    └── {IT-ID}-{FEATURE}-{NNN}.spec.ts
```

## Required Files to Check Before Implementation

```bash
# Always read before implementing (to match existing patterns)
frontend/tests/pages/BaseRegisterPage.ts           # base class to extend
frontend/tests/pages/{ExistingScreen}Page.ts       # PageObject example
frontend/tests/keywords/{ExistingScreen}Keywords.ts # Keywords example
frontend/tests/keywords/index.ts                   # Keywords aggregation class
frontend/tests/testcases/{existing}.spec.ts        # TestCase example
```

## Layer 1: Page Object Template

```typescript
// frontend/tests/pages/{Screen}RegisterPage.ts
import { Page } from '@playwright/test';
import { BaseRegisterPage } from './BaseRegisterPage';

export class {Screen}RegisterPage extends BaseRegisterPage {
  constructor(page: Page) {
    super(page);
  }

  // ─── Navigation ───
  async open{Screen}(id?: number) {
    if (id) {
      await this.page.goto(`/{path}?id=${id}`);
    } else {
      await this.page.goto('/{path}');
    }
    await this.page.waitForLoadState('networkidle');
  }

  // ─── Input operations ───
  async fill{FieldName}(value: string) {
    await this.page.getByLabel('{label name}').fill(value);
  }

  async select{SelectName}(value: string) {
    await this.page.getByRole('combobox', { name: '{label name}' }).click();
    await this.page.getByRole('option', { name: value }).click();
  }

  async fill{DateFieldName}(value: string) {
    await this.page.getByLabel('{label name}').fill(value);
    await this.page.keyboard.press('Tab');  // close DatePicker
  }

  // ─── Button operations ───
  async clickRegisterButton() {
    await this.page.getByRole('button', { name: 'Register' }).click();
  }

  async clickUpdateButton() {
    await this.page.getByRole('button', { name: 'Update' }).click();
  }

  // ─── Result verification ───
  async verifyRegistrationComplete() {
    await this.page.waitForURL('**/{successPath}', { timeout: 30000 });
    await this.page.waitForLoadState('networkidle');
  }

  async verifyValidationError(message: string) {
    await this.page.getByText(message).waitFor({ state: 'visible', timeout: 10000 });
  }

  async verifyToastNotification(message: string) {
    await this.page.getByText(message).waitFor({ state: 'visible', timeout: 10000 });
  }
}
```

## Selector Priority (always follow this order)

| Priority | Selector | Use case |
|----------|---------|---------|
| 1 | `getByRole('button', { name: '...' })` | buttons, links |
| 2 | `getByLabel('...')` | text inputs, checkboxes |
| 3 | `getByRole('combobox', { name: '...' })` | select boxes |
| 4 | `getByRole('option', { name: '...' })` | select options |
| 5 | `locator('[data-testid="..."]')` | only when above cannot be used |

## Layer 2: Keywords Template

```typescript
// frontend/tests/keywords/{Screen}RegisterKeywords.ts
import { Page } from '@playwright/test';
import { {Screen}RegisterPage } from '../pages/{Screen}RegisterPage';

export class {Screen}RegisterKeywords {
  private page: {Screen}RegisterPage;

  constructor(page: Page) {
    this.page = new {Screen}RegisterPage(page);
  }

  // ─── Business flows ───

  async open{Screen}(id?: number) {
    await this.page.open{Screen}(id);
  }

  async fillBasicInfo(data: {
    name: string;
    category: string;
  }) {
    await this.page.fill{Name}(data.name);
    await this.page.select{Category}(data.category);
  }

  async completeRegistration() {
    await this.page.clickRegisterButton();
    await this.page.verifyRegistrationComplete();
  }

  async attemptRegistrationWithEmptyFields() {
    await this.page.clickRegisterButton();
  }

  async verifyValidationError(message: string) {
    await this.page.verifyValidationError(message);
  }
}
```

## Layer 3: Register in keywords/index.ts

```typescript
// Add to frontend/tests/keywords/index.ts

// add import
import { {Screen}RegisterKeywords } from './{Screen}RegisterKeywords';

export class Keywords {
  // ... existing fields ...

  // add new field (camelCase, suffix with Register)
  readonly {screen}Register: {Screen}RegisterKeywords;

  constructor(page: Page) {
    // ... existing initialization ...
    this.{screen}Register = new {Screen}RegisterKeywords(page);
  }
}
```

## Layer 3: TestCase Template

```typescript
// frontend/tests/testcases/{IT-ID}-{FEATURE}-{NNN}.spec.ts
import { test } from '@playwright/test';
import { Keywords } from '../keywords';

test.describe('{IT-ID}: {Screen}_{test overview}', () => {

  test('happy-path_basic-info-registration_complete', async ({ page }) => {
    test.setTimeout(300000);  // required: 5-minute timeout
    const k = new Keywords(page);

    await k.login.loginAsTestUser1();
    await k.{screen}Register.open{Screen}();
    await k.{screen}Register.fillBasicInfo({
      name: 'E2E_{Screen}_' + new Date().toISOString().slice(0, 10),
      category: 'test-category',
    });
    await k.{screen}Register.completeRegistration();
  });

  test('validation_name-empty_required-error-shown', async ({ page }) => {
    test.setTimeout(300000);
    const k = new Keywords(page);

    await k.login.loginAsTestUser1();
    await k.{screen}Register.open{Screen}();
    await k.{screen}Register.attemptRegistrationWithEmptyFields();
    await k.{screen}Register.verifyValidationError('Name is required');
  });

  // Cross-field validation
  test('validation_end-date-before-start-date_date-error-shown', async ({ page }) => {
    test.setTimeout(300000);
    const k = new Keywords(page);

    await k.login.loginAsTestUser1();
    await k.{screen}Register.open{Screen}();
    await k.{screen}Register.fillBasicInfo({
      name: 'test',
      startDate: '2025-12-01',
      endDate: '2025-01-01',  // before start date
    });
    await k.{screen}Register.clickRegisterButton();
    await k.{screen}Register.verifyValidationError('End date must be after start date');
  });
});
```

## Test Execution Commands

```bash
cd frontend

# Run filtered by IT-ID or test name
npm run test:keyword -- --grep "IT-F001"

# UI mode (for debugging when selectors don't match)
npm run test:e2e:ui

# Run specific test file only
npm run test:keyword -- tests/testcases/IT-F001-ITEM-001.spec.ts
```

## Debugging When Selectors Cannot Be Found

1. Launch UI mode with `npm run test:e2e:ui`
2. Inspect the actual DOM to identify the correct label/role names
3. Check the `label` attribute in the implemented component
4. If `data-testid` needs to be added, request it from the frontend-feature agent

## Test Case Naming Convention

```
{IT-ID}-{FEATURE}-{NNN}.spec.ts

Examples:
IT-F001-ITEM-001.spec.ts   ← items feature, 1st test
IT-F002-ORDER-001.spec.ts  ← orders feature, 1st test

test.describe name: "{IT-ID}: {Screen}_{test overview}"
test name: "{happy-path/validation/error-case}_{action}_{expected result}"
```
