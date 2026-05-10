# Shared Package Changes

> Flow for adding type definitions and constants to the `shared` package.
> Breaking changes (deleting or renaming existing types) are prohibited. Additive-only is the principle.

---

## Flow Diagram

```mermaid
flowchart TD
    START([Developer: shared types/constants addition needed]) --> CHECK{Breaking change?}

    CHECK -->|"Yes (delete/rename)"| ESCALATE[⚠️ Present impact scope to developer<br>identify usage in backend/frontend/functions]
    ESCALATE --> APPROVE{Developer approval}
    APPROVE -->|Rejected| DONE_CANCEL([Cancelled])
    APPROVE -->|Approved| SHARED_A

    CHECK -->|"No (additive only)"| SHARED_A

    subgraph SHARED["shared-package — Add Types/Constants"]
        SHARED_A[launch shared-package] --> SHARED_B[Check existing types and constants<br>search for duplicates with grep]
        SHARED_B --> SHARED_C[Add type definition or constant<br>implement in shared/src/]
        SHARED_C --> SHARED_D[Add export to index.ts]
        SHARED_D --> SHARED_E[Verify build with<br>npm run build]
        SHARED_E --> SHARED_F{Build successful?}
        SHARED_F -->|No| SHARED_G[Fix type errors]
        SHARED_G --> SHARED_E
    end

    SHARED_F -->|Yes| NEXT{Next step}

    NEXT -->|"Use in Backend"| BACK([launch backend-feature])
    NEXT -->|"Use in Frontend"| FRONT([launch frontend-feature])
    NEXT -->|"Done"| DONE([Create PR and merge])
```

---

## Notes

- Complete shared package changes **before other agents** (since backend-feature / frontend-feature will import from it)
- If `npm run build` passes, type consistency is guaranteed
- For breaking changes, plan fixes for all affected packages (backend/frontend/functions) first
