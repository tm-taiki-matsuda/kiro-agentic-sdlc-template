# lessons.md Operation Guide

> Rules for handling `tasks/lessons.md`.
> Last updated: 2026-05-10 | kiro-cli 2.1.1

---

## Overview

lessons.md is a file where AI agents record patterns, failures, and improvements discovered during work.
It is automatically loaded at session start to prevent repeating the same mistakes.

```
Agent records → Developer reviews → Repeated patterns promoted to skills
```

---

## 1. Write Rules

### Write Triggers (4 types)

| Trigger | Example |
|---------|---------|
| Received a correction from the developer | "Use `getCurrentDate()` here" |
| Went through test failure → root cause → fix | Missing `is_deleted: false` filter caused full table scan |
| Self-discovered ADR violation or pattern deviation | Was about to create dynamic route `[id]` |
| Encountered unexpected behavior in existing code | `$queryRaw` return value was BigInt |

### Format

```markdown
### [YYYY-MM-DD] Category: Title

**Pattern**: What happened (specific situation)
**Cause**: Why it happened
**Action**: What to do next time (specific rule)
**Apply when**: What kind of work should reference this
```

---

## 2. Developer Review

Content written by agents **must always be reviewed by the developer**.

`stop-hook.sh` notifies "📝 N new entries added to lessons.md".

### Review Checklist

| Check Item | Bad Example |
|-----------|------------|
| Is the cause-effect relationship correct? | "Prisma is the problem" → actually the query was written wrong |
| Is it over-generalized? | "Add authorization check to all GETs" → not needed for public APIs |

---

## 3. Skill Promotion Flow

lessons.md is "temporary learning notes," skills are "confirmed project rules."
When the same pattern is recorded repeatedly, it's a signal to promote it to a skill.

```
Record in lessons.md (agent)
  ↓
Developer reviews content (at session end)
  ↓
Same pattern appears 3+ times (human judgment)
  ↓
Add as official rule to the relevant skill
  ↓
Add "→ promoted to skill" note to the lessons.md entry
```

### Where to Promote

| Pattern Type | Target Skill |
|-------------|-------------|
| ADR violation patterns | `adr-quick-reference` |
| Test writing failure patterns | `test-framework` |
| Security-related | `security-constraints` |
| Repository/Service implementation patterns | respective TDD pattern skills |
| Import/naming mistakes | `code-structure` |
| Business rule misunderstandings | `product-context` |
