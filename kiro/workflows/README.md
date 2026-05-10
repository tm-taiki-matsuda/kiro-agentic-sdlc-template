# kiro-cli Workflow Diagrams

Standard development workflows using kiro-cli, defined as Mermaid diagrams.
Each diagram visualizes agent launch order, decision branches, and approval points.

---

## How to Read the Diagrams

| Notation | Meaning |
|----------|---------|
| `([...])` | Start / End |
| `[...]` | Process / Action |
| `{...}` | Decision / Branch |
| `subgraph` | Agent scope |
| `⚠️` | Points requiring attention |

---

## About Session Start

All work starts automatically with the `agentSpawn` hook when an agent is launched.
Developers have session state (active specs, incomplete tasks, handoffs) restored without any special action.
See [`00-session-start.md`](./00-session-start.md) for details.

---

## Workflow List

### Regular Development

| File | Use Case | Main Agents |
|------|----------|------------|
| [00-session-start.md](./00-session-start.md) | Session start protocol (common to all flows) | agentSpawn hook |
| [01-fullstack.md](./01-fullstack.md) | New full-stack feature development | spec-writer → backend → frontend → e2e → review |
| [02-backend-only.md](./02-backend-only.md) | New Backend API only | spec-writer → backend-feature → code-review |
| [03-frontend-only.md](./03-frontend-only.md) | New Frontend screen only | spec-writer → frontend-feature → e2e-test → code-review |
| [04-db-schema.md](./04-db-schema.md) | Development with DB schema changes | spec-writer → db-migration → backend-feature |
| [05-functions.md](./05-functions.md) | Add new Serverless Functions | spec-writer → functions-feature → code-review |

### Modifications & Fixes

| File | Use Case | Main Agents |
|------|----------|------------|
| [06-backend-mod.md](./06-backend-mod.md) | Modify existing Backend | spec-writer → backend-feature → code-review |
| [07-frontend-mod.md](./07-frontend-mod.md) | Modify existing Frontend | spec-writer → frontend-feature → e2e-test → code-review |
| [08-bug-fix.md](./08-bug-fix.md) | Bug fix (normal or hotfix) | bug-fix |

### Quality & Testing

| File | Use Case | Main Agents |
|------|----------|------------|
| [09-e2e-test.md](./09-e2e-test.md) | Add E2E tests only | e2e-test |
| [10-code-review.md](./10-code-review.md) | Pre-release code review | code-review |

### Infrastructure

| File | Use Case | Main Agents |
|------|----------|------------|
| [11-infrastructure.md](./11-infrastructure.md) | Infrastructure resource changes (Terraform) | infrastructure |

### Design Document Maintenance

| File | Use Case | Main Agents |
|------|----------|------------|
| [12-design-update.md](./12-design-update.md) | Update design docs from requirements/implementation drift (W12) | design-updater |
| [12-design-update.md](./12-design-update.md) | Fix discrepancy between implementation and design docs (W13) | design-updater → code-review |
| [12-design-update.md](./12-design-update.md) | Bulk update design docs + implementation for spec changes (W14) | design-updater → spec-writer → implementation agent |

### Shared Package

| File | Use Case | Main Agents |
|------|----------|------------|
| [13-shared-package.md](./13-shared-package.md) | Add types/constants to shared package (W15) | shared-package → backend/frontend |

### Specification Review

| File | Use Case | Main Agents |
|------|----------|------------|
| [14-system-guide.md](./14-system-guide.md) | Spec/design questions (with drift detection) (W16) | system-guide |
| [14-system-guide.md](./14-system-guide.md) | Spec review → design doc update (W17) | system-guide → design-updater |

### Documentation

| File | Use Case | Main Agents |
|------|----------|------------|
| [15-client-doc.md](./15-client-doc.md) | Create client-facing documentation (W18) | client-doc |
