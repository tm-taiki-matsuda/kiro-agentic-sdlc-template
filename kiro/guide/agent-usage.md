# kiro-cli Agent Usage Guide

> Last updated: 2026-05-10 | kiro-cli 2.1.1

---

## Agent List

| Agent | Shortcut | Role | Writes | Reads |
|---|---|---|---|---|
| `spec-writer` | `Ctrl+Shift+W` | Gather requirements and generate spec files | `.kiro/specs/**` only | design/, existing code, knowledge base |
| `backend-feature` | `Ctrl+Shift+B` | Implement Backend API with TDD | `backend/src/`, `backend/tests/`, `shared/src/` | spec, existing patterns |
| `frontend-feature` | `Ctrl+Shift+F` | Implement Frontend screens with TDD | `frontend/src/`, `frontend/tests/**` | spec, existing patterns |
| `functions-feature` | `Ctrl+Shift+G` | Implement Serverless Functions with TDD | `functions/src/`, `functions/tests/` only | spec, existing function patterns |
| `e2e-test` | `Ctrl+Shift+E` | Generate and run TypeScript Keyword-Driven E2E tests | `frontend/tests/` only | screen specs, implemented components |
| `code-review` | `Ctrl+Shift+R` | Review ADR compliance, security, test coverage | **none (read-only)** | change diff, implementation code, knowledge base |
| `db-migration` | `Ctrl+Shift+D` | Prisma schema changes and migration execution | `database/prisma/` only | schema design docs |
| `bug-fix` | `Ctrl+Shift+X` | Identify root cause and fix bugs with minimal changes | bug-related files only | logs, failing tests, related code, knowledge base |
| `shared-package` | `Ctrl+Shift+S` | Add type definitions and constants to shared package (no breaking changes) | `shared/src/**`, `shared/constants/**` only | tech-stack skill, existing type definitions |
| `infrastructure` | `Ctrl+Shift+I` | Manage cloud resources with Terraform | `infrastructure/**` only | tfvars, existing resource definitions |
| `design-updater` | `Ctrl+Shift+U` | Update design/ documents based on requirements or implementation drift | `design/**`, `tasks/**` | requirement memos, implementation code, existing design docs, knowledge base |
| `system-guide` | `Ctrl+Shift+H` | Answer questions about specs, design, and implementation (with drift detection) | **none (read-only)** | design docs, implementation code, DB schema, knowledge base |
| `client-doc` | `Ctrl+Shift+C` | Generate client-facing documentation (current specs, improvement proposals, effort estimates) in HTML | `output/**`, `tasks/**` | design docs, implementation code, knowledge base |

---

## Launch Commands

```bash
kiro-cli chat --agent spec-writer
kiro-cli chat --agent backend-feature
kiro-cli chat --agent frontend-feature
kiro-cli chat --agent functions-feature
kiro-cli chat --agent e2e-test
kiro-cli chat --agent code-review
kiro-cli chat --agent db-migration
kiro-cli chat --agent bug-fix
kiro-cli chat --agent shared-package
kiro-cli chat --agent infrastructure
kiro-cli chat --agent design-updater
kiro-cli chat --agent system-guide
kiro-cli chat --agent client-doc
```

> **Note**: To switch between phases, use `/quit` → `kiro-cli chat --agent xxx` to launch as a new session.
> Switching with the `/agent` command does not fire the agentSpawn hook.

---

## Use Cases

### New full-stack feature development

```
1. spec-writer      → generate .kiro/specs/{feature-name}/
2. db-migration     → only if schema changes are needed
3. backend-feature  → implement Backend API with TDD
4. frontend-feature → implement Frontend screen with TDD
5. e2e-test         → generate and run E2E tests
6. code-review      → final check before release
```

### Add Backend API only

```
1. spec-writer     → generate spec (or write manually if small)
2. backend-feature → implement
3. code-review     → review
```

### Add Frontend screen only

```
1. spec-writer      → generate spec
2. frontend-feature → implement
3. e2e-test         → E2E tests
4. code-review      → review
```

### Add or modify Serverless Functions

```
1. spec-writer       → generate spec (or write manually if small)
2. db-migration      → only if schema changes are needed
3. functions-feature → implement function (TDD)
4. code-review       → review
```

### Fix a bug

```
1. bug-fix → launch directly, no spec needed
```

### Change DB schema

```
1. db-migration → launch directly
```

### Update design documents

```
1. design-updater → launch directly
```

### Ask about specs or design

```
1. system-guide → launch directly
```

### Create client-facing documentation

```
1. client-doc → launch directly
```

---

## Skill Assignment Table

List of skills referenced by each agent.

| Skill | spec | backend | frontend | functions | e2e | review | db | bug | shared | infra | design | guide | client |
|-------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| product-context | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| tech-stack | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| code-structure | ✓ | ✓ | ✓ | | ✓ | ✓ | | ✓ | ✓ | | ✓ | ✓ | ✓ |
| security-constraints | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| dev-workflow | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | | ✓ | | |
| adr-quick-reference | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | |
| error-handling-pattern | | ✓ | ✓ | | | ✓ | | ✓ | | | | ✓ | |
| fastify-route-pattern | | ✓ | | | | | | | | | | | |
| prisma-repository-pattern | | ✓ | | ✓ | | | ✓ | | | | | | |
| service-tdd-pattern | | ✓ | | | | | | | | | | | |
| react-query-hook-pattern | | | ✓ | | | | | | | | | | |
| test-framework | | ✓ | ✓ | ✓ | ✓ | | | | | | | | |
| e2e-keyword-driven-pattern | | | | | ✓ | | | | | | | | |
| infrastructure-guide | | | | | | | | | | ✓ | | | |
| functions-guide | | | | ✓ | | | | | | | | | |
| workflow-diagrams | ✓ | | | | | ✓ | | ✓ | | | ✓ | ✓ | ✓ |
| spec-ears-notation-guide | ✓ | | | | | | | | | | | | |
