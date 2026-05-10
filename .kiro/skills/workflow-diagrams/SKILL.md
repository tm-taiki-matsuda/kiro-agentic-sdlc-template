---
name: "Workflow Diagrams"
description: "Standard development workflow list using kiro-cli. Workflows and agent launch order for new full-stack development, Backend/Frontend standalone development, DB schema changes, bug fixes, E2E tests, code reviews, and infrastructure changes. Referenced at the start of work to determine which workflow to use."
---

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

---

## Workflow List

### Regular Development

| ID | Use Case | Agent Launch Order |
|----|----------|-------------------|
| W00 | Session start protocol (common to all flows) | agentSpawn hook (automatic) |
| W01 | New full-stack feature development | spec-writer → db-migration (if needed) → backend-feature → frontend-feature → e2e-test → code-review |
| W02 | New Backend API only | spec-writer → backend-feature → code-review |
| W03 | New Frontend screen only | spec-writer → frontend-feature → e2e-test → code-review |
| W04 | Development with DB schema changes | spec-writer → db-migration → backend-feature |
| W05 | Add new Serverless Functions | spec-writer → functions-feature → code-review |

### Modifications & Fixes

| ID | Use Case | Agent Launch Order |
|----|----------|-------------------|
| W06 | Modify existing Backend | spec-writer → backend-feature → code-review |
| W07 | Modify existing Frontend | spec-writer → frontend-feature → e2e-test → code-review |
| W08 | Bug fix (normal or hotfix) | bug-fix |

### Quality & Testing

| ID | Use Case | Agent Launch Order |
|----|----------|-------------------|
| W09 | Add E2E tests only | e2e-test |
| W10 | Pre-release code review | code-review |

### Infrastructure

| ID | Use Case | Agent Launch Order |
|----|----------|-------------------|
| W11 | Infrastructure resource changes (Terraform) | infrastructure |

### Design Document Maintenance

| ID | Use Case | Agent Launch Order |
|----|----------|-------------------|
| W12 | Update design docs from requirements/meeting notes | design-updater |
| W13 | Fix discrepancy between implementation and design docs | design-updater → code-review |
| W14 | Bulk update design docs + implementation for spec changes | design-updater → spec-writer → implementation agent |

### Shared Package

| ID | Use Case | Agent Launch Order |
|----|----------|-------------------|
| W15 | Add types/constants to shared package | shared-package → backend-feature / frontend-feature |

### Specification Review

| ID | Use Case | Agent Launch Order |
|----|----------|-------------------|
| W16 | Spec/design questions (with discrepancy detection) | system-guide |
| W17 | Spec review → design doc update | system-guide → design-updater |

### Documentation

| ID | Use Case | Agent Launch Order |
|----|----------|-------------------|
| W18 | Create client-facing documentation | client-doc |

---

## Detailed Flow Diagrams

Mermaid flow diagrams for each workflow (including approval points, branch conditions, and agent handoffs) are
stored as individual files in `kiro/workflows/`.

| Workflow | Detail Diagram File |
|----------|-------------------|
| W00 Session Start | `kiro/workflows/00-session-start.md` |
| W01 Full-stack | `kiro/workflows/01-fullstack.md` |
| W02 Backend only | `kiro/workflows/02-backend-only.md` |
| W03 Frontend only | `kiro/workflows/03-frontend-only.md` |
| W04 DB schema change | `kiro/workflows/04-db-schema.md` |
| W05 Functions | `kiro/workflows/05-functions.md` |
| W06 Backend modification | `kiro/workflows/06-backend-mod.md` |
| W07 Frontend modification | `kiro/workflows/07-frontend-mod.md` |
| W08 Bug fix | `kiro/workflows/08-bug-fix.md` |
| W09 E2E test | `kiro/workflows/09-e2e-test.md` |
| W10 Code review | `kiro/workflows/10-code-review.md` |
| W11 Infrastructure | `kiro/workflows/11-infrastructure.md` |
| W12 Design doc update | `kiro/workflows/12-design-update.md` |
| W13 Design doc + impl update | `kiro/workflows/12-design-update.md` |
| W14 Bulk design doc update | `kiro/workflows/12-design-update.md` |
| W15 Shared package | `kiro/workflows/13-shared-package.md` |
| W16 Spec review | `kiro/workflows/14-system-guide.md` |
| W17 Spec review → design update | `kiro/workflows/14-system-guide.md` |
| W18 Client documentation | `kiro/workflows/15-client-doc.md` |
