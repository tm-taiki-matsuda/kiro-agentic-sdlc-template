---
name: "Infrastructure Guide"
description: "Terraform cloud infrastructure configuration, environment list, naming conventions, deployment workflow, and safety constraints. Referenced by infrastructure agent when adding or modifying resources."
---

# Infrastructure (Terraform / Cloud)

## Environment List

| Environment | Domain | Variable File | Backend Config | Purpose |
|-------------|--------|--------------|----------------|---------|
| dev | {dev-domain} | `dev.tfvars` | `backend-dev.hcl` | Development / verification |
| stg | {stg-domain} | `stg.tfvars` | `backend-stg.hcl` | Staging |
| prod | {prod-domain} | `prod.tfvars` | `backend-prod.hcl` | Production |

## Terraform Workflow

```bash
cd infrastructure/terraform

# 1. Initialize backend (run per environment)
terraform init -backend-config=backend-{env}.hcl

# 2. Review change plan (required)
terraform plan -var-file={env}.tfvars [-var-file={env}.secrets.tfvars]

# 3. Apply only after developer review
terraform apply -var-file={env}.tfvars [-var-file={env}.secrets.tfvars]
```

**⚠️ `terraform apply` must only be run after the developer reviews the plan. Automatic apply is prohibited.**

## Terraform Directory Structure

```
terraform/
├── main.tf                  # provider configuration
├── variables.tf             # variable definitions
├── locals.tf                # local variables (naming conventions, etc.)
├── outputs.tf               # output values
├── versions.tf              # required_providers version pinning
│
├── # Resource definitions (1 file = 1 resource category)
├── resource_group.tf        # resource group / project container
├── network.tf               # VNet / VPC, subnets
├── frontend.tf              # frontend (static hosting / CDN)
├── backend.tf               # backend (application hosting)
├── functions.tf             # batch / async (serverless functions)
├── database.tf              # managed database (e.g., PostgreSQL)
├── storage.tf               # file / object storage
├── cdn_waf.tf               # CDN + WAF
├── secret_management.tf     # secret management service
├── identity_provider.tf     # identity provider configuration
├── access_control.tf        # access control role assignments
├── monitoring.tf            # monitoring / observability
└── ...
```

## Naming Convention

Resource names are centrally managed in `locals.tf`.
Pattern: `{env}-{project}-{resource-type}` (e.g., `dev-myapp-app`, `prod-myapp-db`)

## Secret Management

- Secret values are stored in `*.secrets.tfvars` (in .gitignore)
- `*.secrets.tfvars.example` exists as a sample
- `infrastructure/scripts/pre-commit-hook.sh` blocks commits of tfstate/secrets

## Commonly Used Scripts

| Script | Purpose |
|--------|---------|
| `scripts/connect-db.sh` | Connect to the database |
| `scripts/manage-group-members.sh` | Manage identity provider group members |
| `scripts/manage-resources.sh` | Start/stop resources |
| `scripts/grant-storage-permission.sh` | Grant file/object storage permissions |

## Safety Constraints

- `terraform apply` can only be run after developer confirmation
- Do not commit `*.secrets.tfvars` to git (prevented by pre-commit-hook.sh)
- Do not commit `terraform.tfstate` to git (use remote state)
- Changes to production (prod/stg) require developer review and approval
- Destructive changes (resource deletion) require explicit developer confirmation
