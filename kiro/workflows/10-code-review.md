# Pre-Release Code Review

> Flow where the `code-review` agent performs multi-perspective checks for ADR compliance, security, and test coverage before PR creation.
> Read-only agent — does not modify code. Provides findings only.

---

## Flow Diagram

```mermaid
flowchart TD
    START([Developer: review request<br>prepare change diff with git diff main]) --> REV_A

    subgraph REVIEW["code-review — Multi-perspective Review (read-only)"]
        REV_A[launch code-review] --> REV_B["Get change diff with git diff main<br>understand list of changed files and change volume"]
        REV_B --> REV_C["ADR compliance check<br>reference adr-quick-reference skill"]
        REV_C --> REV_D["Security check<br>authentication, authorization, secret leakage, input validation"]
        REV_D --> REV_E["Test coverage check<br>CUD operations, error cases, boundary values, permissions"]
        REV_E --> REV_F["Code quality check<br>duplication, type safety, error handling, response format"]
        REV_F --> REV_G[Generate findings report]
    end

    REV_G --> SEVERITY{Finding severity}

    SEVERITY -->|"🔴 MUST<br>release blocker"| MUST["ADR violations / security issues<br>data integrity risk / missing tests"]
    SEVERITY -->|"🟡 SHOULD<br>recommended"| SHOULD["Code quality / response format<br>type safety / error handling improvements"]
    SEVERITY -->|"🔵 CONSIDER<br>optional"| CONSIDER["Naming improvements / refactoring proposals<br>performance improvements / documentation additions"]

    MUST --> FIX["Fix immediately with relevant agent<br>backend-feature / frontend-feature / functions-feature"]
    FIX --> RE_REVIEW[Re-review]
    RE_REVIEW --> SEVERITY

    SHOULD --> DEV_JUDGE[Developer decides and handles]
    CONSIDER --> DEFER[Consider in future sprints]

    DEV_JUDGE --> MUST_CHECK{All 🔴 MUST<br>resolved?}
    MUST_CHECK -->|No| FIX
    MUST_CHECK -->|Yes| DONE([Developer: create PR and merge])
    DEFER --> DONE
```

---

## ADR Checklist (items code-review always verifies)

| ADR | Check Content |
|-----|--------------|
| ADR-001 | No `[id]` directory under `frontend/src/app/` |
| ADR-002 | `backend/prisma/` or `functions/prisma/` not directly edited |
| ADR-003 | List API response is `{ contents, totalCount, offset, limit }` format |
| ADR-004 | Route not calling Prisma directly (via Awilix DI) |
| ADR-005 | No `DELETE` SQL or Prisma `delete()` (update to `is_deleted = true`) |
| ADR-006 | Update operations have `version` check (return 409 on mismatch) |
| ADR-007 | `new Date()` not used directly (use `getCurrentDate()`) |
| ADR-008 | Backend imports have `.js` extension |

## Notes

- **CI auto-execution**: `code-review` can run headlessly with `--no-interactive` flag. See `ops/ci-headless.md` for details.
- **🔴 MUST criteria**: Explicitly breaking team-agreed ADRs, security risks, CUD operations without tests
- **Report positive aspects**: Always report well-implemented sections, not just findings
