# Add E2E Tests Only

> Flow for adding E2E tests to already-implemented screens.
> Used to supplement test coverage without new implementation.

---

## Flow Diagram

```mermaid
flowchart TD
    START([Developer: add E2E tests to implemented screen]) --> E2E_A

    subgraph E2E["e2e-test — Test Design, Generation, and Execution"]
        E2E_A[launch e2e-test] --> E2E_B[Check target screen and screen specs<br>read design/features/]
        E2E_B --> E2E_C[Check coverage of existing test cases<br>investigate frontend/tests/testcases/]
        E2E_C --> E2E_D[Identify missing scenarios<br>happy path / validation / permission / error / boundary]
        E2E_D --> E2E_E[Reference e2e-keyword-driven-pattern skill<br>design with 3-layer architecture]
        E2E_E --> E2E_F1[Layer 1: Create/extend Page Object<br>frontend/tests/pages/{Screen}Page.ts]
        E2E_F1 --> E2E_F2[Layer 2: Create/extend Keywords<br>frontend/tests/keywords/{Screen}Keywords.ts<br>register in keywords/index.ts]
        E2E_F2 --> E2E_F3[Layer 3: Generate TypeScript TestCase<br>frontend/tests/testcases/{IT-ID}-{FEATURE}-{NNN}.spec.ts]
    end

    E2E_F3 --> SCENARIO{Test type}

    SCENARIO -->|Happy path| SC_A[Happy Path tests<br>complete normal operation flow]
    SCENARIO -->|Validation| SC_B[Error message verification tests<br>required empty, max length, cross-field]
    SCENARIO -->|Permission| SC_C[Role-based access control tests<br>hidden buttons for unauthorized users, API 403]
    SCENARIO -->|Error case| SC_D[API error display tests<br>network failure, 500 error]
    SCENARIO -->|Boundary| SC_E[0-item display, max count, pagination]

    SC_A --> RUN
    SC_B --> RUN
    SC_C --> RUN
    SC_D --> RUN
    SC_E --> RUN

    subgraph RUN["Test Execution and Verification"]
        RUN_A[npm run test:keyword -- --grep {IT-ID}] --> RUN_B{Green?}
        RUN_B -->|No| RUN_C{Failure cause}
        RUN_C -->|Selector mismatch| RUN_D[Fix Page Object selectors<br>check DOM with npm run test:e2e:ui]
        RUN_C -->|Implementation bug| RUN_E[⚠️ Report to developer<br>hand off to bug-fix agent]
        RUN_D --> RUN_A
    end

    RUN_B -->|Yes| DONE([Test addition complete])
```

---

## Notes

- **3-layer architecture**: Separate into Page Object (selector operations) → Keywords (business language) → TestCase (scenarios)
- **Selector priority**: Use in order: `getByRole` → `getByLabel` → `getByRole('combobox')` → `getByRole('option')` → `locator('[data-testid="..."]')`
- **When implementation bugs are found**: Do not modify E2E tests. Fix the bug with `bug-fix` agent, then re-run E2E tests
