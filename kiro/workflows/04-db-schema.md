# Development with DB Schema Changes

> Flow applied to all development that modifies `database/prisma/schema.prisma`.
> Schema changes are handled by the `db-migration` agent and must always be completed before other agents.

---

## Flow Diagram

```mermaid
flowchart TD
    START([Developer: schema change needed]) --> SPEC_A

    subgraph SPEC["① spec-writer — Create Spec (including schema changes)"]
        SPEC_A[launch spec-writer] --> SPEC_B[Investigate design docs and current schema<br>read database/prisma/schema.prisma]
        SPEC_B --> SPEC_C[Describe change proposal in design.md<br>specify added columns, new tables, indexes]
        SPEC_C --> SPEC_D{Developer review<br>impact scope, effect on existing data}
        SPEC_D -->|Revision requested| SPEC_C
    end

    SPEC_D -->|Approved| DB_A

    subgraph DBMIG["② db-migration — Schema Change (carefully)"]
        DB_A[launch db-migration] --> DB_B[Modify database/prisma/schema.prisma<br>⚠️ Direct editing of backend/ functions/ schema.prisma is prohibited (ADR-002)]
        DB_B --> DB_C[Present changes and impact to developer]
        DB_C --> DB_D{Developer approval}
        DB_D -->|Revision requested| DB_B
        DB_D -->|Approved| DB_E[npm run db:migrate<br>generate migration file]
        DB_E --> DB_F{Verify in dev environment}
        DB_F -->|No| DB_G[Fix migration<br>re-run with npm run db:reset]
        DB_G --> DB_E
        DB_F -->|Yes| DB_H[Regenerate Prisma clients for all services<br>npm run db:generate<br>(backend + functions)]
    end

    DB_H --> IMPL{Which services<br>need implementation?}

    IMPL -->|Backend only| BACK_A
    IMPL -->|Backend + Frontend| BACK_A
    IMPL -->|Functions only| FUNC_A
    IMPL -->|None (schema only)| REV_A

    subgraph BACK["③ backend-feature — Backend Implementation (if needed)"]
        BACK_A[launch backend-feature] --> BACK_B[Implement repository, service, route for new schema]
        BACK_B --> BACK_C{Tests green?}
        BACK_C -->|No| BACK_D[Fix]
        BACK_D --> BACK_C
    end

    subgraph FUNC["③ functions-feature — Functions Implementation (if needed)"]
        FUNC_A[launch functions-feature] --> FUNC_B[Implement function using new schema]
        FUNC_B --> FUNC_C{Tests green?}
        FUNC_C -->|No| FUNC_D[Fix]
        FUNC_D --> FUNC_C
    end

    BACK_C -->|Yes| REV_A
    FUNC_C -->|Yes| REV_A

    subgraph REVIEW["④ code-review — Review"]
        REV_A[launch code-review] --> REV_B[Verify schema change consistency<br>impact on existing tables, indexes, constraints]
        REV_B --> REV_C{🔴 MUST findings?}
        REV_C -->|Yes| REV_D[Fix]
        REV_D --> REV_B
    end

    REV_C -->|No| DONE([Developer: create PR and merge<br>⚠️ Apply to stg/prod separately with db-migration agent])
```

---

## Notes

- **No migrations outside dev**: The `db-migration` agent only runs migrations in dev. Apply to stg/prod manually as a separate step.
- **schema.prisma ownership (ADR-002)**: Only edit `database/prisma/schema.prisma`
- **Impact on existing data**: Explicitly confirm with developer when adding columns that need `DEFAULT` values or adding NOT NULL constraints
