# kiro-cli Prompting Guide

> How to give effective instructions to AI agents.
> Last updated: 2026-05-10 | kiro-cli 2.1.1

---

## 1. Core Principle: AI Agents Are "Talented New Hires"

Think of kiro-cli agents as talented new engineers who can write code quickly.

- They can read project code (can search and load files)
- They have extensive general technical knowledge (languages, frameworks, patterns)
- But they don't know project-specific context (which files are reference examples, why this design was chosen)

Telling them not just "what to do" but also "which files to reference" and "what not to do" dramatically improves output quality.

---

## 2. Four Elements of Good Instructions

### ① Target (what, where)

```
❌ "Create an API"
✅ "Create a CRUD API for user management. The endpoint is /api/v1/users"
```

### ② Reference (what to look at)

```
❌ "Implement it nicely"
✅ "Reference the existing backend/src/api/routes/v1/items.ts and implement with the same pattern"
```

### ③ Constraints (what not to do)

```
❌ (no constraints → scope expands without limit)
✅ "Limit changes to backend/src/shared/repositories/ only. Do not touch frontend/"
```

### ④ Completion criteria (when is it done)

```
❌ "Write tests too"
✅ "Done when all unit tests are green. Verify with cd backend && npm run test:unit"
```

---

## 3. Common Bad Patterns and Improvements

### Bad 1: Too vague

```
❌ "Fix the bug"
✅ "GET /api/v1/items is including logically deleted records in the list.
   Please check the WHERE clause in the Repository's findAll method"
```

### Bad 2: Scope too broad

```
❌ "Refactor everything"
✅ "Change only the findAll method in items.repository.ts from $queryRaw to findMany.
   Do not change other methods"
```

### Bad 3: Not specifying reference files

```
❌ "Write tests"
✅ "Reference backend/tests/unit/repositories/items.repository.test.ts and
   write tests with the same naming conventions and structure"
```

---

## 4. Standard Prompt When Launching with a Spec

Standard prompt when a spec exists:

```
Please implement based on the spec in .kiro/specs/{feature-name}/.
Read requirements.md and design.md first, then present the implementation plan.
```

---

## 5. What to Check at Approval Points

When an agent presents an implementation plan, verify the following before approving:

```
✅ Is the changed file list as expected?
✅ Are there any files that should not be changed?
✅ Does the test plan include 409 conflict and logical delete cases?
✅ No ADR violations (dynamic routes, new Date(), etc.)?
```

---

## 6. How to Give Correction Instructions

When agent output doesn't match intent:

```
# Tell specifically what the problem is
"The Route's single-item retrieval is /items/:id. Please change to /items?id=123 per ADR-001"

# Show a reference example
"Please implement with the same pattern as the update method in the existing items.service.ts"

# Add constraints
"Please limit this fix to items.repository.ts only. Do not change other files"
```

---

## 7. Explicitly Mention Skills

When you want the agent to follow a specific pattern, explicitly mention the skill name:

```
"Please check the adr-quick-reference skill before implementing"
"Please implement the Route following the fastify-route-pattern skill"
"Please generate tests with the 3-layer architecture from the e2e-keyword-driven-pattern skill"
```

---

## 8. Prompt for Session Handoff

When continuing from a previous session:

```
Read tasks/handoff-{feature-name}.md and resume from the remaining tasks.
```

Or resume directly from specs:

```
Check .kiro/specs/{feature-name}/tasks.md and
resume from [IN_PROGRESS] or [TODO] tasks.
```
