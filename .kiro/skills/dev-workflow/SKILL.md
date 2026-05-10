---
name: "Development Workflow"
description: "Session start protocol, task lifecycle, change approval rules, TDD cycle, verification gates, and commit discipline. Referenced by all agents to follow proper work procedures."
---

# Development Workflow

## Session Start Protocol

1. Check `tasks/todo.md` to understand active tasks.
2. Check `tasks/lessons.md` to review past error patterns.
3. If there are handoff documents (`tasks/handoff-*.md`), read them first.
4. Read `code-structure/SKILL.md` to confirm the actual directory layout for this project.
5. Confirm "What is the task for this session?" before starting work.

## Task Lifecycle

> See `kiro/guide/todo-guide.md` for details.

1. **Plan**: Write today's tasks in `tasks/todo.md` (extracted from specs/tasks.md).
2. **Confirm**: Have the developer review the plan before starting implementation.
3. **Implement**: Mark completed items with `[x]` as you go (also update specs/tasks.md to `[DONE]`).
4. **Verify**: Prove task completion by running tests and confirming behavior.
5. **Close**: Clear todo.md when all done. Create handoff-*.md if handing off to another agent.

## Change Approval Rules

**All changes to production code require developer confirmation before execution.**

Exceptions that do not require confirmation:
- Mechanical formatting fixes (Prettier)
- Import statement cleanup
- Obviously safe type fixes

Always require confirmation:
- Schema changes affecting multiple tables
- Changes to auth/security plugins
- Changes to CI/CD pipelines
- Breaking changes to `shared/` package
- Running migrations in production environments

## TDD Cycle (Required for All Features)

```
Red (write a failing test)
  ↓
Green (make the test pass with minimal code)
  ↓
Refactor (refactor while keeping tests green)
```

Never write production code without tests.

## Verification Gate (Required Before Marking Task Complete)

```bash
# Run relevant test suites
cd backend && npm run test:unit
cd frontend && npm test

# Check change scope
git diff --stat

# Ask yourself: "Would a staff engineer approve this PR?"
```

Criteria:
- All tests pass
- Change scope is minimal relative to requirements
- No new bugs introduced
- No obvious issues that would be flagged in code review

## Commit Discipline

- **Commits are initiated by the developer** (AI does not commit autonomously)
- `git commit --no-verify` is prohibited (bypassing hooks is prohibited)
- `git push --force` is prohibited
- 1 commit = 1 concern (keep commits focused)

## Self-Improvement Loop (lessons.md Write Rules)

Record in `tasks/lessons.md` when any of the following occur:

- Received a correction from the developer
- Went through a test failure → root cause identification → fix cycle
- Self-discovered an ADR violation or pattern deviation
- Encountered unexpected behavior in existing code

```markdown
### [YYYY-MM-DD] Category: Title

**Pattern**: What happened (specific situation)
**Cause**: Why it happened
**Action**: What to do next time (specific rule)
**Apply when**: What kind of work should reference this
```

Category examples: `Backend`, `Frontend`, `Database`, `Testing`, `ADR`, `Infrastructure`, `Functions`

Not repeating the same mistake is the top priority.

## Escalation Conditions

**Always stop and confirm with the developer** in the following situations:

- A schema change affecting multiple tables becomes necessary
- Changes to auth/security-related plugins are needed
- Changes to CI/CD pipelines are needed
- Breaking changes to `shared/` package are needed
- Cannot identify the cause of test failures
- Requirements are ambiguous with multiple valid interpretations

## Pursuit of Elegance

Before making significant changes, pause and ask: "Is there a more elegant approach?"
If a fix feels like a hack, implement an elegant solution using all the information currently available.

However, skip this process for simple, obvious fixes (avoid over-engineering).

## End of Session

### Design Document Diff Check

When a task is complete, verify whether any decisions made during this session differ from the `design/` documents.
If there are differences, report to the developer and confirm how to handle them:

- **Reflect now** → Guide the developer to launch the `design-updater` agent.
- **Reflect later** → Record "update design docs with design-updater: {summary of diff}" in `tasks/todo.md`.
- **No reflection needed** → Confirm the reason and close.

### Guide to Next Agent

If the workflow requires launching another agent next, present:

1. Launch command (e.g., `kiro-cli chat --agent frontend-feature`)
2. Example prompt to pass to that agent (including spec path)

### Handoff

For tasks spanning multiple sessions, create `tasks/handoff-{feature}.md`:
- What was completed
- What remains
- Test status
- Things to watch out for in the next session
