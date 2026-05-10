# New Full-Stack Feature Development

> End-to-end development flow for Backend API + Frontend screen.
> If DB schema changes are needed, run db-migration before backend-feature.

---

## Flow Diagram

```mermaid
flowchart TD
    START([Developer: new feature request]) --> SPEC_A

    subgraph SPEC["① spec-writer — Create Spec"]
        SPEC_A[launch spec-writer] --> SPEC_B[Investigate design docs and existing code<br>read design/]
        SPEC_B --> SPEC_C[Generate requirements.md / design.md / tasks.md]
        SPEC_C --> SPEC_D{Developer review}
        SPEC_D -->|Revision requested| SPEC_C
    end

    SPEC_D -->|Approved| E{DB schema<br>changes needed?}

    E -->|Yes| DB_A

    subgraph DBMIG["② db-migration — Migration (conditional)"]
        DB_A[launch db-migration] --> DB_B[Present schema change proposal]
        DB_B --> DB_C{Developer approval}
        DB_C -->|Revision requested| DB_B
        DB_C -->|Approved| DB_D[Run migration<br>verify in dev environment]
        DB_D --> DB_E[Regenerate Prisma clients<br>for backend / functions]
    end

    E -->|No| BACK_A
    DB_E --> BACK_A

    subgraph BACK["③ backend-feature — Backend Implementation"]
        BACK_A[launch backend-feature] --> BACK_B[Investigate spec, design docs, existing patterns]
        BACK_B --> BACK_C[Present implementation plan]
        BACK_C --> BACK_D{Developer approval}
        BACK_D -->|Revision requested| BACK_C
        BACK_D -->|Approved| BACK_E[TDD: Zod → Repository → Service → Route]
        BACK_E --> BACK_F{All tests green?<br>unit / mock / integration}
        BACK_F -->|No| BACK_G[Identify failure cause and fix]
        BACK_G --> BACK_F
    end

    BACK_F -->|Yes| BACK_HANDOFF[Create handoff-*.md<br>(for multi-session)]
    BACK_HANDOFF --> FRONT_A

    subgraph FRONT["④ frontend-feature — Frontend Implementation"]
        FRONT_A[launch frontend-feature] --> FRONT_B[Investigate spec and existing patterns]
        FRONT_B --> FRONT_C[Present implementation plan]
        FRONT_C --> FRONT_D{Developer approval}
        FRONT_D -->|Revision requested| FRONT_C
        FRONT_D -->|Approved| FRONT_E[TDD: types → hooks → Zod → components → pages]
        FRONT_E --> FRONT_F{All tests green?}
        FRONT_F -->|No| FRONT_G[Identify failure cause and fix]
        FRONT_G --> FRONT_F
    end

    FRONT_F -->|Yes| FRONT_HANDOFF[Create handoff-*.md<br>(for multi-session)]
    FRONT_HANDOFF --> E2E_A

    subgraph E2E["⑤ e2e-test — E2E Test Generation"]
        E2E_A[launch e2e-test] --> E2E_B[Generate TypeScript test cases<br>happy path / validation / permission errors]
        E2E_B --> E2E_C{E2E green?}
        E2E_C -->|No| E2E_D[Fix tests and implementation]
        E2E_D --> E2E_C
    end

    E2E_C -->|Yes| REV_A

    subgraph REVIEW["⑥ code-review — Pre-release Check"]
        REV_A[launch code-review] --> REV_B[ADR compliance check<br>reference adr-quick-reference skill]
        REV_B --> REV_C[Security and missing test check]
        REV_C --> REV_D{🔴 MUST findings?}
        REV_D -->|Yes| REV_E[Fix with relevant agent]
        REV_E --> REV_B
    end

    REV_D -->|No| DONE([Developer: create PR and merge])
```

---

## Notes

### Switch agents with new sessions

For each phase switch, use `/quit` → `kiro-cli chat --agent xxx` to launch as a new session.

```bash
# After ① spec-writer completes
/quit
# Launch next agent as new session
kiro-cli chat --agent backend-feature
```

### Other notes

- **Large specs**: Use `spec-writer` to generate split specs for Backend / Frontend, then launch agents in order
- **DB schema changes**: Always complete `db-migration` first and regenerate all service clients with `npm run db:generate` before proceeding
