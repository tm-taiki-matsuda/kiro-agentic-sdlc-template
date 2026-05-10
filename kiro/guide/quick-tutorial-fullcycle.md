# Hands-on: Full Cycle Experience (spec → implementation → review)

> Experience the collaboration between agents, TDD, and approval points by running a small change through 3 agents.
> Estimated time: 20–30 minutes

---

## What You'll Experience

1. Create a change spec with `spec-writer`
2. Implement with TDD based on the spec using `backend-feature`
3. Review the implementation result with `code-review`

---

## Step 1: Choose a Subject

Proceed with the assumption of adding an optional `remarks` field to an existing Backend API.

```bash
ls backend/src/shared/schemas/
# Choose one of the displayed schema files (e.g., {feature}Schema.ts)
```

## Step 2: Create a Spec with spec-writer

```bash
kiro-cli chat --agent spec-writer
```

Input:
```
I want to add a remarks (notes) field to an existing API.
- Target: backend/src/shared/schemas/{feature}Schema.ts (replace with actual file)
- Change: add an optional string field
- DB schema change: none (using existing column)
```

## Step 3: Implement with backend-feature

```bash
kiro-cli chat --agent backend-feature
```

Input:
```
Please implement based on the spec in .kiro/specs/{feature-remarks}/.
Read requirements.md and design.md first, then present the implementation plan.
```

What to check at the approval point:
- Is the changed file only `{feature}Schema.ts`?
- Is a test plan included?

## Step 4: Review with code-review

```bash
kiro-cli chat --agent code-review
```

Input:
```
Check the change diff with git diff main and review ADR compliance, security, and test coverage.
```

## Step 5: Done

If there are no 🔴 MUST findings, proceed to create a PR.
