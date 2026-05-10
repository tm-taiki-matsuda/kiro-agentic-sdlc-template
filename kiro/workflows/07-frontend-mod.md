# Modify Existing Frontend

> Flow for modifying existing screens with minimal changes: adding fields, display changes, interaction modifications, etc.

---

## Flow Diagram

```mermaid
flowchart TD
    START([Developer: existing screen change/feature addition request]) --> SPEC_A

    subgraph SPEC["① spec-writer — Create Change Spec"]
        SPEC_A[launch spec-writer] --> SPEC_B[Investigate existing components and tests<br>read features/ and apis/]
        SPEC_B --> SPEC_C[Create change spec<br>✅ files to change<br>🚫 files NOT to change]
        SPEC_C --> SPEC_D{Developer review}
        SPEC_D -->|Revision requested| SPEC_C
    end

    SPEC_D -->|Approved| FRONT_A

    subgraph FRONT["② frontend-feature — Minimal Modification"]
        FRONT_A[launch frontend-feature] --> FRONT_B[Read existing code and tests<br>check target components and hooks]
        FRONT_B --> FRONT_C[Verify all current tests are green<br>npm test -- --testPathPattern={feature}]
        FRONT_C --> FRONT_D{Current tests<br>green?}
        FRONT_D -->|No| FRONT_E[⚠️ Report existing defects to developer first]
        FRONT_D -->|Yes| FRONT_F[Present change plan<br>affected component list, impact on existing tests]
        FRONT_F --> FRONT_G{Developer approval}
        FRONT_G -->|Revision requested| FRONT_F
        FRONT_G -->|Approved| FRONT_H[TDD: modify hooks/components<br>add new tests → change implementation]
        FRONT_H --> FRONT_I[Run all tests<br>both existing and new must be green]
        FRONT_I --> FRONT_J{All tests green?}
        FRONT_J -->|No| FRONT_K[Fix]
        FRONT_K --> FRONT_I
    end

    FRONT_J -->|Yes| E2E_Q{E2E test<br>update needed?}

    E2E_Q -->|Yes<br>field added, flow changed, etc.| E2E_A

    subgraph E2E["③ e2e-test — E2E Test Update (if needed)"]
        E2E_A[launch e2e-test] --> E2E_B{Update type}
        E2E_B -->|Fix existing tests| E2E_C[Update selectors/values in<br>existing TypeScript test cases]
        E2E_B -->|Add new tests| E2E_D[Add TypeScript test cases for new scenarios]
        E2E_C --> E2E_E[npm run test:keyword -- --grep {FeatureId}]
        E2E_D --> E2E_E
        E2E_E --> E2E_F{E2E green?}
        E2E_F -->|No| E2E_G[Fix tests and implementation]
        E2E_G --> E2E_E
    end

    E2E_F -->|Yes| REV_A
    E2E_Q -->|No| REV_A

    subgraph REVIEW["④ code-review — Review"]
        REV_A[launch code-review] --> REV_B[Verify change scope minimality<br>ADR-001 dynamic routes, type safety check]
        REV_B --> REV_C{🔴 MUST findings?}
        REV_C -->|Yes| REV_D[Fix]
        REV_D --> REV_B
    end

    REV_C -->|No| DONE([Developer: create PR and merge])
```

---

## Notes

- **When to update E2E tests**: Update needed when UI selectors, text, or flow changes. Not needed for logic-only changes
- **No changes outside `frontend/src/`**: The `frontend-feature` agent only modifies `frontend/src/`
