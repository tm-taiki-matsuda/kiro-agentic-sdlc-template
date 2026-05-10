# Hands-on: Code Review with code-review

> Step-by-step tutorial for code review using kiro-cli agents.
> Prerequisite: Setup in [onboarding.md](./onboarding.md) is complete.

---

## What You'll Experience

Just tell the `code-review` agent "please review," and the AI autonomously reads the code and detects ADR violations, security issues, and missing tests.

`code-review` is a read-only agent, so no code is modified at all.

---

## Step 1: Navigate to Project Root

```bash
cd <project-root>
```

## Step 2: Launch code-review Agent

```bash
kiro-cli chat --agent code-review
```

## Step 3: Request a Review

```
Check the change diff with git diff main and review ADR compliance, security, and test coverage.
```

## Step 4: Review the Report

The agent outputs a report in the following format:

```
## Code Review Results

### Positive Aspects
- ...

### 🔴 MUST (Required Fixes)
1. {file-path}:{line} — {description of issue}
   Fix: ...

### 🟡 SHOULD (Recommended)
...

### Summary
...
```

## Step 5: Fix 🔴 MUST Findings

If there are MUST findings, fix them with the relevant agent and then request a re-review.
