# todo.md Operation Guide

> Rules for handling task management files under `tasks/`.
> Last updated: 2026-05-10 | kiro-cli 2.1.1

---

## File Roles

```
.kiro/specs/{feature}/tasks.md    feature-level implementation checklist (TODO→DONE). Stays until feature complete
tasks/todo.md                     session-level work notes. Clear at session end
tasks/handoff-*.md                handoff to next session. Delete after handoff recipient reads it
tasks/lessons.md                  error patterns and improvement records (→ see lessons-guide.md)
```

### Difference Between specs/tasks.md and todo.md

| | specs/tasks.md | todo.md |
|---|---|---|
| Scope | Entire feature | What to do in this session |
| Lifespan | Until feature complete | Clear at session end |
| Updated by | Implementation agent (TODO→IN_PROGRESS→DONE) | Implementation agent (checklist format) |

---

## todo.md Lifecycle

### 1. Session Start

`session-start-hook.sh` automatically displays incomplete tasks.

### 2. Task Planning

Agent writes today's tasks in todo.md from `[TODO]` / `[IN_PROGRESS]` in specs/tasks.md.

```markdown
## Active Tasks

- [ ] Define Zod schema (specs: Phase 1 - Zod schema)
- [ ] Write Repository test → implement (specs: Phase 1 - Repository)
```

### 3. During Session

Mark completed items with `[x]` and also update specs/tasks.md to `[DONE]`.

### 4. Session End

`stop-hook.sh` displays the remaining task count.

- **All complete** → clear active tasks in todo.md to "(none)"
- **Incomplete, continue next session** → leave as is
- **Hand off to another agent** → create handoff-*.md and clear todo.md

---

## handoff-*.md (Agent-to-Agent Handoff)

### When to Create

- When switching from backend-feature → frontend-feature in full-stack development
- When handing off work to another agent due to session interruption

### Naming Convention

```
tasks/handoff-{specs-directory-name}.md
```

### Content

```markdown
# Handoff: {Feature Name}

## Completed Tasks
- Zod schema definition
- Repository test and implementation

## Remaining Tasks
- Service test and implementation
- Route implementation

## Test Status
- `cd backend && npm run test:unit` → 12 tests passing

## Notes for Next Session
- {specific notes}
```

### When to Delete

After the handoff recipient agent reads it via `session-start-hook.sh`, **delete it within that session**.
