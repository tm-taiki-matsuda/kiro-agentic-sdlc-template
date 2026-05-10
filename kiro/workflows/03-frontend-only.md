# New Frontend Screen Development

> Flow for developing a Frontend screen only, with Backend API already implemented.

---

## Flow Diagram

```mermaid
flowchart TD
    START([Developer: new screen creation request<br>Backend API already implemented]) --> SPEC_A

    subgraph SPEC["① spec-writer — Create Spec"]
        SPEC_A[launch spec-writer] --> SPEC_B[Investigate design docs and existing components<br>read design/features/]
        SPEC_B --> SPEC_C[Generate requirements.md / design.md / tasks.md<br>specify API paths and validation rules]
        SPEC_C --> SPEC_D{Developer review}
        SPEC_D -->|Revision requested| SPEC_C
    end

    SPEC_D -->|Approved| FRONT_A

    subgraph FRONT["② frontend-feature — Screen Implementation"]
        FRONT_A[launch frontend-feature] --> FRONT_B[Investigate spec and existing patterns<br>reference similar features]
        FRONT_B --> FRONT_C[Present implementation plan<br>file list, ADR-001 check]
        FRONT_C --> FRONT_D{Developer approval}
        FRONT_D -->|Revision requested| FRONT_C
        FRONT_D -->|Approved| FRONT_E[TDD: types → API hook → Zod → custom hook → component → page]
        FRONT_E --> FRONT_F[Run tests<br>npm test (Jest + RTL)]
        FRONT_F --> FRONT_G{All tests green?}
        FRONT_G -->|No| FRONT_H[Identify failure cause and fix]
        FRONT_H --> FRONT_F
    end

    FRONT_G -->|Yes| E2E_A

    subgraph E2E["③ e2e-test — E2E Test Generation and Execution"]
        E2E_A[launch e2e-test] --> E2E_B[Design test scenarios<br>reference e2e-keyword-driven-pattern skill]
        E2E_B --> E2E_C[Generate TypeScript test cases<br>frontend/tests/testcases/{IT-ID}-{FEATURE}-{NNN}.spec.ts]
        E2E_C --> E2E_D{Test type}
        E2E_D -->|Happy path| E2E_E[Happy Path tests]
        E2E_D -->|Validation| E2E_F[Error message verification tests]
        E2E_D -->|Permission| E2E_G[Role-based access control tests]
        E2E_E --> E2E_H[npm run test:keyword -- --grep {FeatureId}]
        E2E_F --> E2E_H
        E2E_G --> E2E_H
        E2E_H --> E2E_I{E2E green?}
        E2E_I -->|No| E2E_J[Fix tests and implementation]
        E2E_J --> E2E_H
    end

    E2E_I -->|Yes| REV_A

    subgraph REVIEW["④ code-review — Pre-release Check"]
        REV_A[launch code-review] --> REV_B[ADR-001 dynamic route check<br>react-query-hook-pattern / 409 handling check]
        REV_B --> REV_C{🔴 MUST findings?}
        REV_C -->|Yes| REV_D[Fix]
        REV_D --> REV_B
    end

    REV_C -->|No| DONE([Developer: create PR and merge])
```

---

## Notes

- **ADR-001**: Page routing uses `?id=123` query parameter format. Do not use `[id]` directories
- **409 error handling**: Implement toast display on optimistic lock conflict following the `react-query-hook-pattern` skill
- **MSW mocks**: Add API mocks for development to `frontend/src/mocks/handlers/`
