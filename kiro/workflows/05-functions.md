# Add New Serverless Functions

> Flow for adding new functions under `functions/` for batch processing, notifications, etc.
> Does not touch Backend or Frontend.

---

## Flow Diagram

```mermaid
flowchart TD
    START([Developer: batch/notification/alert feature request]) --> SPEC_A

    subgraph SPEC["① spec-writer — Create Spec"]
        SPEC_A[launch spec-writer] --> SPEC_B[Investigate existing functions and design docs<br>reference functions/src/functions/{category}/]
        SPEC_B --> SPEC_C[Generate requirements.md / design.md / tasks.md<br>specify trigger type, schedule, function ID]
        SPEC_C --> SPEC_D{Developer review}
        SPEC_D -->|Revision requested| SPEC_C
    end

    SPEC_D -->|Approved| E{DB schema<br>changes needed?}

    E -->|Yes| DB_A[launch db-migration<br>schema change and Prisma client regeneration]
    E -->|No| FUNC_A
    DB_A --> FUNC_A

    subgraph FUNC["② functions-feature — Function Implementation"]
        FUNC_A[launch functions-feature] --> FUNC_B[Investigate spec and existing function patterns<br>read 1-2 similar functions]
        FUNC_B --> FUNC_C[Present implementation plan<br>confirm function ID, category, trigger type]
        FUNC_C --> FUNC_D{Developer approval}
        FUNC_D -->|Revision requested| FUNC_C
        FUNC_D -->|Approved| FUNC_E{Trigger type}
        FUNC_E -->|Timer<br>scheduled batch| FUNC_F[timer trigger<br>periodic execution with CRON expression]
        FUNC_E -->|Event<br>notification| FUNC_G[event trigger<br>receive and process events]
        FUNC_E -->|Storage<br>file processing| FUNC_H[storage trigger<br>blob/file trigger processing]
        FUNC_F --> FUNC_J
        FUNC_G --> FUNC_J
        FUNC_H --> FUNC_J
        FUNC_J[TDD: write test (Red) → implement (Green)] --> FUNC_K[npm run test:unit -- --testPathPattern={funcId}]
        FUNC_K --> FUNC_L{Tests green?}
        FUNC_L -->|No| FUNC_M[Identify failure cause and fix]
        FUNC_M --> FUNC_J
        FUNC_L -->|Yes| FUNC_I[Add import to src/index.ts]
    end

    FUNC_I --> NOTIF{Notification<br>sending needed?}

    NOTIF -->|Yes| OUTBOX[⚠️ Verify Outbox pattern<br>do not call event bus directly<br>insert into outbox table<br>→ send via outbox-processor]
    NOTIF -->|No| REV_A
    OUTBOX --> REV_A

    subgraph REVIEW["③ code-review — Review"]
        REV_A[launch code-review] --> REV_B[ADR compliance and security check<br>verify no secret leakage, no direct Prisma schema editing]
        REV_B --> REV_C{🔴 MUST findings?}
        REV_C -->|Yes| REV_D[Fix]
        REV_D --> REV_B
    end

    REV_C -->|No| DONE([Developer: create PR and merge])
```

---

## Notes

- **Prohibited: direct editing of `functions/prisma/schema.prisma` (ADR-002)**: Regenerate with `npm run db:generate`
- **Outbox pattern**: Directly executing notifications makes retries impossible on failure, so always use Outbox
