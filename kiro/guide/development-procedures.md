# kiro-cli Standard Development Procedures

> Standard procedures for kiro-cli Spec-Driven Development.
> Last updated: 2026-05-10 | kiro-cli 2.1.1

---

## Core Philosophy

```
Developer's job:    write spec → launch agent → confirm & approve
Agent's job:        read design docs → TDD implementation → run tests → suggest next steps
```

Developers don't write code. **Write specs and delegate to agents** — that's how kiro-cli works.

---

## 1. New Feature Development (Full-Stack)

### Step 1: Create Spec

```bash
kiro-cli chat --agent spec-writer
```

Example input:
```
I want to add a user management feature.
- Screens: user list, registration, edit
- API: /api/v1/users (CRUD)
- DB schema change: add department column to users table
```

Output: `.kiro/specs/user-management/` with requirements.md / design.md / tasks.md

### Step 2: DB Schema Change (if needed)

```bash
kiro-cli chat --agent db-migration
```

Example input:
```
Please change the schema based on the spec in .kiro/specs/user-management/.
Read design.md first, then present the change proposal.
```

### Step 3: Backend Implementation

```bash
kiro-cli chat --agent backend-feature
```

Example input:
```
Please implement based on the spec in .kiro/specs/user-management/.
Read requirements.md and design.md first, then present the implementation plan.
```

### Step 4: Frontend Implementation

```bash
kiro-cli chat --agent frontend-feature
```

### Step 5: E2E Tests

```bash
kiro-cli chat --agent e2e-test
```

### Step 6: Code Review

```bash
kiro-cli chat --agent code-review
```

Example input:
```
Check the change diff with git diff main and review ADR compliance, security, and test coverage.
```

---

## 2. New Backend API Only

```bash
# 1. Create spec (or write manually if small)
kiro-cli chat --agent spec-writer

# 2. Implement
kiro-cli chat --agent backend-feature

# 3. Review
kiro-cli chat --agent code-review
```

---

## 3. Bug Fix

```bash
kiro-cli chat --agent bug-fix
```

Example input:
```
GET /api/v1/items is including logically deleted records in the list.
Please check the WHERE clause in the Repository's findAll method.
```

---

## 4. Modify Existing Feature

```bash
# 1. Create change spec
kiro-cli chat --agent spec-writer

# 2. Implement (Backend or Frontend)
kiro-cli chat --agent backend-feature
# or
kiro-cli chat --agent frontend-feature

# 3. Review
kiro-cli chat --agent code-review
```

---

## 5. What to Check at Approval Points

When an agent presents an implementation plan, verify the following before approving:

| Check Item | What to Look For |
|-----------|-----------------|
| Changed file list | Are there any unexpected files? |
| Test plan | Does it include 409 conflict and logical delete tests? |
| ADR compliance | No violations like dynamic routes or `new Date()`? |
| Schema change presence | Is the "no change" judgment correct? |

---

## 6. End-of-Session Checklist

- [ ] Clear completed tasks from `tasks/todo.md`
- [ ] Add any patterns worth recording to `tasks/lessons.md`
- [ ] If handing off to another agent, create `tasks/handoff-{feature-name}.md`
- [ ] If there are differences from design documents, update with `design-updater` agent
