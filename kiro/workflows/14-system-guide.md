# Specification Review (with Drift Detection)

> Flow where the `system-guide` agent cross-references design documents and implementation code to answer spec questions.
> **Read-only agent — does not modify code or design documents.** When drift is found, guides handoff to `design-updater`.

---

## W16: Spec/Design Questions

```mermaid
flowchart TD
    START([Developer: question about specs/design]) --> SG_A

    subgraph SG["system-guide — Spec Answer (read-only)"]
        SG_A[launch system-guide] --> SG_B[Classify question<br>screen spec / API spec / DB spec / business rule / permission]
        SG_B --> SG_C[Search design documents<br>search design/ with knowledge tool]
        SG_C --> SG_D[Verify corresponding implementation code<br>check if design doc description matches implementation]
        SG_D --> SG_E{Drift found?}
        SG_E -->|No| SG_F[Compose answer<br>cite both design doc and implementation as evidence]
        SG_E -->|Yes| SG_G[Answer based on implementation<br>⚠️ explicitly note drift]
    end

    SG_F --> DONE([Developer: review answer])
    SG_G --> DIVERGE{Handle drift}

    DIVERGE -->|"Update design docs"| DU[Guide to launch design-updater<br>present specific drift content as prompt example]
    DIVERGE -->|"No action now"| TODO[Prompt to record in tasks/todo.md]
    DIVERGE -->|"Implementation is wrong"| BF[Guide to launch bug-fix]

    DU --> DONE2([Developer: take next action])
    TODO --> DONE2
    BF --> DONE2
```

---

## W17: Spec Review → Design Doc Update

```mermaid
flowchart TD
    START([Developer: spec review for design doc modernization]) --> SG_A

    subgraph SG["① system-guide — Identify Drift"]
        SG_A[launch system-guide] --> SG_B[Read design docs for target screen/API]
        SG_B --> SG_C[Cross-reference with corresponding implementation code]
        SG_C --> SG_D[Report drift list<br>diff table: design doc vs implementation]
    end

    SG_D --> DEV{Developer decision}
    DEV -->|"Update design docs"| DU_A
    DEV -->|"No action needed"| DONE([Complete])

    subgraph DU["② design-updater — Update Design Docs"]
        DU_A[launch design-updater] --> DU_B[Present change plan based on<br>system-guide's drift report]
        DU_B --> DU_C{Developer approval}
        DU_C -->|Revision requested| DU_B
        DU_C -->|Approved| DU_D[Update design documents<br>maintain existing format]
        DU_D --> DU_E[Final consistency check]
    end

    DU_E --> DONE2([Completion report])
```

---

## Notes

- **system-guide is read-only**: Does not modify code or design documents at all. Only finds and reports drift.
- **Treat implementation as source of truth**: If design docs are outdated, the actually running code is the current spec
- **Collaboration with design-updater**: system-guide finds drift, design-updater fixes it
