# Infrastructure Resource Changes (Terraform)

> Flow for adding, modifying, or deleting cloud resources with Terraform.
> **`terraform apply` must only be run after the developer reviews the plan. Automatic apply is prohibited.**

---

## Flow Diagram

```mermaid
flowchart TD
    START([Developer: cloud resource addition/change request]) --> INFRA_A

    subgraph PLAN_PHASE["① infrastructure — Investigation, Design, Code Changes"]
        INFRA_A[launch infrastructure] --> INFRA_B[Read existing Terraform definitions<br>infrastructure/terraform/*.tf]
        INFRA_B --> INFRA_C[Check target environment variable files<br>{env}.tfvars / {env}.secrets.tfvars]
        INFRA_C --> INFRA_D[Present change plan<br>list of resources to add/modify/delete]
        INFRA_D --> INFRA_E{Developer approval}
        INFRA_E -->|Revision requested| INFRA_D
        INFRA_E -->|Approved| INFRA_F[Edit *.tf files<br>1 file = 1 resource category]
        INFRA_F --> INFRA_G[Add variables to variables.tf<br>naming: {env}-{project}-{resource-type}]
    end

    INFRA_G --> TF_INIT

    subgraph TF_PLAN["② terraform plan — Visualize Changes (required)"]
        TF_INIT[terraform init -backend-config=backend-{env}.hcl] --> TF_PLAN_CMD[terraform plan -var-file={env}.tfvars]
        TF_PLAN_CMD --> TF_SHOW[Present plan results to developer<br>breakdown of + add / ~ modify / - delete]
        TF_SHOW --> TF_DESTROY_Q{Resources<br>being deleted?}
        TF_DESTROY_Q -->|Yes| TF_WARN[⚠️ Explicitly state impact of deletions<br>verify impact on production data and dependent resources]
        TF_DESTROY_Q -->|No| TF_DEV_OK
        TF_WARN --> TF_DEV_OK
        TF_DEV_OK{Developer approval}
        TF_DEV_OK -->|Revision requested| INFRA_F
    end

    TF_DEV_OK -->|Approved| TF_APPLY

    subgraph TF_APPLY_PHASE["③ terraform apply — Only after explicit developer instruction"]
        TF_APPLY[Confirm developer's explicit instruction to apply] --> TF_APPLY_CMD[terraform apply -var-file={env}.tfvars]
        TF_APPLY_CMD --> TF_RESULT{Apply successful?}
        TF_RESULT -->|No| TF_ERROR[⚠️ Report error details to developer]
        TF_RESULT -->|Yes| TF_VERIFY[Verify post-apply state<br>terraform show / terraform state list]
    end

    TF_VERIFY --> MULTI_ENV{Apply to<br>other environments?}
    MULTI_ENV -->|Yes| TF_NEXT[Repeat same flow for next environment<br>dev → stg → prod order]
    MULTI_ENV -->|No| DONE([Completion report])
    TF_NEXT --> DONE
    TF_ERROR --> DONE_ERR([Developer: manual investigation and fix])
```

---

## Notes

### Environment Application Order

```
dev → stg → prod
```

Always verify in stg before applying to production (prod).

### Secret Management

- Do not commit `*.secrets.tfvars` to git (in `.gitignore`)
- Use remote backend for `terraform.tfstate`. Do not store locally
