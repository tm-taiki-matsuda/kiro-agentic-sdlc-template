# Modify Existing Backend

> Flow for modifying existing APIs with minimal changes: adding fields, search conditions, response changes, etc.
> **The principle is to verify all existing tests pass before making changes.**

---

## Flow Diagram

```mermaid
flowchart TD
    START([Developer: existing API change/feature addition request]) --> SPEC_A

    subgraph SPEC["① spec-writer — Create Change Spec"]
        SPEC_A[launch spec-writer] --> SPEC_B[Investigate existing implementation, tests, and design docs<br>identify files to change]
        SPEC_B --> SPEC_C[Create change spec<br>✅ files to change<br>🚫 files NOT to change]
        SPEC_C --> SPEC_D{Developer review<br>verify impact scope is minimal}
        SPEC_D -->|Revision requested| SPEC_C
    end

    SPEC_D -->|Approved| E{DB schema<br>changes needed?}

    E -->|Yes| DB_A[launch db-migration<br>schema change and Prisma client regeneration]
    E -->|No| BACK_A
    DB_A --> BACK_A

    subgraph BACK["② backend-feature — Minimal Modification"]
        BACK_A[launch backend-feature] --> BACK_B[Read existing code and tests<br>check target schema, repository, service, route]
        BACK_B --> BACK_C[Verify all current tests are green<br>npm run test:unit -- --testPathPattern={feature}]
        BACK_C --> BACK_D{Current tests<br>green?}
        BACK_D -->|No| BACK_E[⚠️ Report existing defects to developer first<br>ask whether bug fix is needed first]
        BACK_D -->|Yes| BACK_G[Present change plan<br>affected file list, impact on existing tests]
        BACK_G --> BACK_H{Developer approval}
        BACK_H -->|Revision requested| BACK_G
        BACK_H -->|Approved| BACK_I[TDD: add new tests (Red) → change implementation (Green)]
        BACK_I --> BACK_J[Run all tests<br>both existing and new must be green]
        BACK_J --> BACK_K{All tests green?}
        BACK_K -->|No| BACK_L[Fix<br>verify existing tests are not broken]
        BACK_L --> BACK_J
    end

    BACK_K -->|Yes| SCOPE[Verify change scope with git diff --stat<br>check for unexpected files]

    SCOPE --> REV_A

    subgraph REVIEW["③ code-review — Review"]
        REV_A[launch code-review] --> REV_B[Verify change scope minimality<br>check for unintended changes]
        REV_B --> REV_C[ADR compliance check]
        REV_C --> REV_D{🔴 MUST findings?}
        REV_D -->|Yes| REV_E[Fix]
        REV_E --> REV_B
    end

    REV_D -->|No| DONE([Developer: create PR and merge])
```

---

## Notes

- **Verify "existing tests pass"**: Run current tests before modification and record that they are green
- **Change scope management**: Agree with developer on number of changed files using `git diff --stat`
- **Adding fields**: Adding `optional` fields to existing responses maintains backward compatibility
