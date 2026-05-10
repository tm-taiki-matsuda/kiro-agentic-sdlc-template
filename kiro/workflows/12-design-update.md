# Design Document Update

> Flow for updating design documents under `design/` based on requirement memos or implementation drift.
> **All changes are presented as drafts to the developer and confirmed before finalizing.**

---

## Flow Diagram

```mermaid
flowchart TD
    START([Requirement memo / implementation drift report / spec change instruction]) --> TRIAGE{Determine update type}

    TRIAGE -->|"Design docs only<br>no implementation changes"| DOC_ONLY_A
    TRIAGE -->|"Both design docs and<br>implementation need updating"| FULL_A

    subgraph DOC_ONLY["Design Docs Only Update (W12)"]
        DOC_ONLY_A[launch design-updater] --> DOC_ONLY_B[Understand change requirements<br>review requirement memo or drift report]
        DOC_ONLY_B --> DOC_ONLY_C[Read target design documents<br>also check related docs (screen ↔ API ↔ DB)]
        DOC_ONLY_C --> DOC_ONLY_D[Present change plan<br>target files, impact scope, change summary]
        DOC_ONLY_D --> DOC_ONLY_E{Developer approval}
        DOC_ONLY_E -->|Revision requested| DOC_ONLY_D
        DOC_ONLY_E -->|Approved| DOC_ONLY_F[Update design documents<br>maintain existing format, present diff]
        DOC_ONLY_F --> DOC_ONLY_G[Final consistency check<br>verify screen ↔ API ↔ DB alignment]
        DOC_ONLY_G --> DOC_ONLY_H{Consistency OK?}
        DOC_ONLY_H -->|No| DOC_ONLY_I[Fix inconsistencies]
        DOC_ONLY_I --> DOC_ONLY_G
        DOC_ONLY_H -->|Yes| DOC_ONLY_DONE([Completion report<br>updated file list, guide on implementation impact])
    end

    subgraph FULL["Design Docs + Implementation Bulk Update (W14)"]
        FULL_A[launch design-updater] --> FULL_B[Understand change requirements<br>organize changes affecting both design docs and implementation]
        FULL_B --> FULL_C[Read target design docs + check current implementation<br>identify gaps between design docs and implementation]
        FULL_C --> FULL_D[Present change plan<br>design doc changes + implementation impact scope]
        FULL_D --> FULL_E{Developer approval}
        FULL_E -->|Revision requested| FULL_D
        FULL_E -->|Approved| FULL_F[Update design docs first<br>finalize design before implementation]
        FULL_F --> FULL_G[Guide to launch spec-writer<br>create spec based on updated design docs]
        FULL_G --> FULL_H[Guide to launch implementation agent<br>backend-feature / frontend-feature / etc.]
        FULL_H --> FULL_I[Guide to launch code-review<br>final consistency check between design docs and implementation]
        FULL_I --> FULL_DONE([Complete])
    end
```

---

## Notes

### Design Document Categories

| Category | Path |
|---------|------|
| Screen design | `design/screen/specs/` |
| API design | `design/api/specs/` |
| DB design | `design/database/` |
| Report design | `design/report/specs/` |
| Batch design | `design/batch/specs/` |

### What design-updater does NOT do

- Modify implementation code (`backend/`, `frontend/`, `functions/`, etc.)
- Delete design documents
- Finalize changes without developer approval
