# kiro-cli Configuration Design Philosophy

> Explains why this configuration is structured the way it is. Read before making changes.
> Last updated: 2026-05-10 | kiro-cli 2.1.1

---

## 30-Second Summary

This configuration is built on a "delegate work to a team of 13 specialists" model.

Assigning everything to one all-purpose person leads to more accidents and inconsistent quality compared to dividing work by specialty: Backend specialist, Frontend specialist, review specialist, etc. The same applies to AI agents. Furthermore, since AI carries the risk of "accidentally breaking something outside its domain," the constraint that **it physically cannot write to files outside its responsibility** is enforced at the configuration level.

---

## Design Principles

| Principle | Content | Without This |
|-----------|---------|-------------|
| Specialization | Specialized agents per layer, not one all-purpose agent | Accidents like breaking schema.prisma while fixing Frontend |
| Physical constraints | Enforce rule compliance through configuration, not "please" | AI generates ADR-violating code by ignoring prompts |
| Staged context | Load information on-demand, not all at once | 18 skills fill the context window, pushing out actual work instructions |

---

## Why Separate into 13 Agents?

### Problem: Limits of an All-Purpose Agent

Delegating everything to one all-purpose agent leads to:
- Accidentally modifying Frontend files while fixing Backend
- Directly editing DB schema and violating ADR-002
- Mixing code review and implementation, making responsibility unclear

### Solution: Specialization + Physical Constraints

Each agent's write scope is physically restricted by `allowedPaths`.
AI cannot bypass this through its own judgment.

```
backend-feature  → backend/src/**, backend/tests/**, shared/src/** only
frontend-feature → frontend/src/**, frontend/tests/** only
db-migration     → database/prisma/schema.prisma only
code-review      → no writes (read-only)
```

---

## Why Not Use steering/?

kiro-cli has a `steering/` directory feature for setting global rules, but this framework does not use it.

Reasons:
- `steering/` rules apply to all agents, making agent-specific constraints impossible
- Physical constraints via `allowedPaths` are more reliable
- On-demand loading via skills is more context-efficient

---

## Why Load Skills On-Demand?

Loading all 18 skills at startup would fill most of the context window with skills, pushing out actual work instructions.

Using the `skill://` protocol, skills are only loaded when the agent determines they're needed.
This reserves the context window for work instructions, code, and test results.

---

## Why Separate tasks/ from config/ (Framework Version)

In the source project this framework was derived from, tasks were placed in `config/tasks/`, but this framework changes it to `tasks/`.

Reasons:
- `config/` is often separated as a framework configuration repository
- Task management files (todo.md, lessons.md) are more naturally placed close to the project root
- Avoids path confusion when applying to new projects
