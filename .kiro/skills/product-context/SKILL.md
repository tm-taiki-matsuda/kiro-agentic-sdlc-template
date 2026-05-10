---
name: "Product Context"
description: "System overview, key users, core business rules, security constraints, language policy, and environment list. Referenced by all agents for domain understanding."
---

# Product Context

> **This file is a template for project-specific information.**
> When starting a new project, fill in each section below with your project's actual details.

## Assumed Project Structure

This framework assumes the following directory layout at the project root.
**Customize `code-structure/SKILL.md` if your project differs.**

```
{project-root}/
├── backend/          Fastify API server
├── frontend/         Next.js frontend
├── database/         Prisma schema (source of truth) + migrations
├── shared/           Shared TypeScript package (types, constants)
├── functions/        Serverless Functions (batch / async)
├── infrastructure/   Terraform (cloud resources)
├── design/           Design documents (screen specs, API specs, DB specs)
│   ├── screen/       Screen design documents
│   ├── api/          API design documents (OpenAPI specs, etc.)
│   ├── database/     DB design documents (table definitions, etc.)
│   ├── report/       Report design documents
│   └── batch/        Batch design documents
├── tasks/            Session-level task management (todo.md, lessons.md)
└── .kiro/            kiro-cli configuration (this framework)
```

> **If `design/` does not exist**: Agents that reference design documents
> (`spec-writer`, `system-guide`, `design-updater`, `client-doc`) will still work,
> but knowledge base search will return no results. Either create the directory
> or remove the `knowledgeBase` resource entry from those agents.

> **If your directory structure differs**: Update `code-structure/SKILL.md` and
> the `allowedPaths` in each agent's JSON to match your project layout.

---

## Language Policy

> **All agents must follow this policy.** This is the single source of truth for language settings.

| Target | Language |
|--------|----------|
| Agent responses | **Japanese** |
| Business logic comments | Japanese |
| Technical implementation comments | English |
| Variable / function names | English (camelCase / snake_case) |

To change the response language for all agents, update the **Agent responses** row above.
For example, change `Japanese` to `English` to switch all agents to English responses.

## System Overview

{Describe the system's purpose, target business domain, and key features in 2–3 sentences.}

Example: An internal business management system. An enterprise web application that centralizes order, inventory, and billing management.

## Key Users

- **{Role name}**: {Description of responsibilities}
- **{Role name}**: {Description of responsibilities}
- **Administrator**: User management, master data management

## Core Business Rules

### Data Integrity Rules (Strictly Enforced)
- **Logical delete required**: All mutable tables must have `is_deleted Boolean @default(false)`. `DELETE` statements are prohibited. Always use `UPDATE SET is_deleted = true`.
- **Optimistic locking required**: All mutable tables must have `version Int @default(1)`. On update, verify version match and increment. Return HTTP 409 on mismatch.
- **Audit log required**: Output audit log on every mutation API call.

### Date Retrieval Rule
- Use `getCurrentDate()` for all date retrieval (`new Date()` is prohibited).
- This allows dates to be fixed via the `MOCK_DATE` environment variable during testing.

### {Project-specific Business Rules}
- {Rule 1}
- {Rule 2}

## Security Constraints

- **Authentication**: {Describe the auth method. Example: OAuth2 / OIDC provider → JWT}
- **Authorization**: {Describe the authz method. Example: Role-Based Access Control (RBAC)}
- **File access**: {Describe the file access method}
- **Network**: {Describe network constraints}

## Environments

| Environment | URL | Purpose |
|-------------|-----|---------|
| dev | {URL} | Development / verification |
| stg | {URL} | Staging |
| prod | {URL} | Production |

## CI/CD

{Describe the CI/CD pipeline overview. Example: CI/CD pipelines (e.g., GitHub Actions, Azure DevOps). Each package has its own CI pipeline triggered on push to main/develop branches.}
