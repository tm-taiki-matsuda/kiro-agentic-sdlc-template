# Hands-on: Spec Creation with spec-writer

> Experience creating spec files, the starting point of Spec-Driven Development.

---

## What You'll Experience

Tell the `spec-writer` agent a feature overview and generate a 3-file set (requirements.md / design.md / tasks.md) through dialogue.

spec-writer can only write to `.kiro/specs/`, so no project source code is modified at all.

---

## Step 1: Launch spec-writer Agent

```bash
kiro-cli chat --agent spec-writer
```

## Step 2: Request Spec Creation

```
I want to add a user management feature.
- Screens: user list, registration, edit
- API: /api/v1/users (CRUD)
- DB schema change: none
```

## Step 3: Answer the Questions

The agent will ask about unclear points. Answering specifically improves accuracy.

## Step 4: Review the Spec

Check the generated files:

```bash
cat .kiro/specs/user-management/requirements.md
cat .kiro/specs/user-management/design.md
cat .kiro/specs/user-management/tasks.md
```

## Step 5: Approve

If the content is correct, say "Please finalize this spec."

## Step 6: Launch the Implementation Agent

```bash
kiro-cli chat --agent backend-feature
```

Input:
```
Please implement based on the spec in .kiro/specs/user-management/.
Read requirements.md and design.md first, then present the implementation plan.
```
