# Client-Facing Documentation

> Flow where the `client-doc` agent references design documents and implementation code to generate client-facing documentation (current specs, improvement proposals, effort estimates) in HTML format.
> **Can only write to output/. Does not modify design documents or implementation code.**

---

## W18: Create Client-Facing Documentation

```mermaid
flowchart TD
    START([Developer: request to create client-facing documentation]) --> CD_A

    subgraph CD["client-doc — Interactive Documentation Creation"]
        CD_A[launch client-doc] --> CD_B[Requirements gathering<br>confirm document purpose, target audience, scope]
        CD_B --> CD_C[Information gathering<br>search and analyze design/ + implementation code]
        CD_C --> CD_D[Present document structure<br>chapter outline, content items, effort estimate overview]
        CD_D --> CD_E{Developer approval}
        CD_E -->|Revision requested| CD_B
        CD_E -->|Approved| CD_F[Generate HTML<br>output document to output/]
        CD_F --> CD_G[Developer review<br>request content and expression verification]
        CD_G --> CD_H{Review result}
        CD_H -->|Revision requested| CD_F
        CD_H -->|Approved| CD_I[Save final version to output/]
    end

    CD_I --> DONE([Complete])
```

---

## Notes

- **client-doc can only write to output/**: Does not modify design documents (`design/`) or implementation code at all
- **Effort estimates are AI approximations**: These are AI-generated estimates not based on actual data, and require developer review and adjustment
- **Output format**: Generated as HTML file in output/
