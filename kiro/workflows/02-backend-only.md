# New Backend API Development

> Flow for developing a Backend API standalone, without Frontend.
> For internal batch APIs, microservice communication APIs, etc.

---

## Flow Diagram

```mermaid
flowchart TD
    START([Developer: new API creation request]) --> SPEC_A

    subgraph SPEC["① spec-writer — Create Spec"]
        SPEC_A[launch spec-writer] --> SPEC_B[Investigate design docs and API specs<br>read design/api/specs/]
        SPEC_B --> SPEC_C[Generate requirements.md / design.md / tasks.md<br>specify endpoints, validation, response format]
        SPEC_C --> SPEC_D{Developer review}
        SPEC_D -->|Revision requested| SPEC_C
    end

    SPEC_D -->|Approved| E{DB schema<br>changes needed?}

    E -->|Yes| DB_A

    subgraph DBMIG["② db-migration (if needed)"]
        DB_A[launch db-migration] --> DB_B[Present change proposal and get developer approval]
        DB_B --> DB_C[Run migration<br>regenerate Prisma client]
    end

    E -->|No| BACK_A
    DB_C --> BACK_A

    subgraph BACK["③ backend-feature — API Implementation"]
        BACK_A[launch backend-feature] --> BACK_B[Investigate spec and existing patterns<br>reference similar Route / Service / Repository]
        BACK_B --> BACK_C[Present implementation plan]
        BACK_C --> BACK_D{Developer approval}
        BACK_D -->|Revision requested| BACK_C
        BACK_D -->|Approved| BACK_E[TDD: Zod → Repository → Service → Route]
        BACK_E --> BACK_F[Run tests<br>npm run test:unit<br>npm run test:mock<br>npm run test:integration]
        BACK_F --> BACK_G{All tests green?}
        BACK_G -->|No| BACK_H[Identify failure cause and fix]
        BACK_H --> BACK_F
    end

    BACK_G -->|Yes| REV_A

    subgraph REVIEW["④ code-review — Review"]
        REV_A[launch code-review] --> REV_B[ADR compliance check<br>authentication, authorization, audit log, response format]
        REV_B --> REV_C{🔴 MUST findings?}
        REV_C -->|Yes| REV_D[Fix]
        REV_D --> REV_B
    end

    REV_C -->|No| DONE([Developer: create PR and merge])
```

---

## Notes

- **ADR Checklist (required)**
  - ADR-001: `/api` prefix, no dynamic routes
  - ADR-003: List response `{ contents, totalCount, offset, limit }`
  - ADR-005: Logical delete only
  - ADR-006: Optimistic lock (version check)
  - ADR-007: Use `getCurrentDate()`
  - ADR-008: `.js` extension imports
