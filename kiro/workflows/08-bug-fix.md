# Bug Fix

> Has two flows: normal bug fix and hotfix (emergency response).
> Both share the same principle: start with Root Cause Analysis and make minimal fixes.

---

## Flow Diagram

```mermaid
flowchart TD
    START([Bug report / test failure / anomaly detected]) --> TRIAGE{Assess urgency}

    TRIAGE -->|"Normal bug<br>fix by next sprint"| NORMAL_A
    TRIAGE -->|"Hotfix<br>production impact, immediate response needed"| HOT_A

    %% ─────────────────────────────
    %% Normal Bug Fix Flow
    %% ─────────────────────────────
    subgraph NORMAL["Normal Bug Fix Flow"]
        NORMAL_A[launch bug-fix] --> NORMAL_B["Check logs, error messages, failing tests<br>review tasks/lessons.md for similar past patterns"]
        NORMAL_B --> NORMAL_C["Root Cause Analysis<br>trace in order: Route → Service → Repository → DB"]
        NORMAL_C --> NORMAL_D{Root cause identified?}
        NORMAL_D -->|Yes| NORMAL_E["Write failing test first (TDD: Red)<br>add test case that reproduces the bug"]
        NORMAL_D -->|No| NORMAL_X["⚠️ Request additional info from developer<br>logs, reproduction steps, environment info"]
        NORMAL_X --> NORMAL_C
        NORMAL_E --> NORMAL_F["Implement minimal fix (TDD: Green)<br>fix only root cause, refactoring goes in separate PR"]
        NORMAL_F --> NORMAL_G["Run all tests<br>npm run test:unit / test:mock / test:integration"]
        NORMAL_G --> NORMAL_H{All existing tests<br>green?}
        NORMAL_H -->|No| NORMAL_I["Investigate impact scope<br>fix unintended side effects"]
        NORMAL_I --> NORMAL_G
        NORMAL_H -->|Yes| NORMAL_J["Record bug pattern and fix in tasks/lessons.md<br>to prevent repeating the same mistake"]
        NORMAL_J --> NORMAL_K[launch code-review<br>verify fix scope and root cause resolution]
        NORMAL_K --> NORMAL_L{"🔴 MUST findings?"}
        NORMAL_L -->|Yes| NORMAL_F
        NORMAL_L -->|No| NORMAL_DONE([Create PR and merge])
    end

    %% ─────────────────────────────
    %% Hotfix Flow
    %% ─────────────────────────────
    subgraph HOTFIX["⚡ Hotfix Flow (Emergency)"]
        HOT_A["launch bug-fix<br>⚡ emergency mode"] --> HOT_B["Immediately check error logs, affected users, impact scope"]
        HOT_B --> HOT_C{Reproducible?}
        HOT_C -->|No| HOT_D["Request additional info from developer<br>logs, stack trace, reproduction conditions"]
        HOT_D --> HOT_C
        HOT_C -->|Yes| HOT_E[Identify root cause]
        HOT_E --> HOT_F{Assess fix<br>scope}
        HOT_F -->|"1-2 files<br>low risk"| HOT_G["Implement minimal fix immediately<br>absolutely no refactoring"]
        HOT_F -->|"Large scope<br>high risk"| HOT_H["⚠️ Emergency escalation to developer<br>propose partial workaround"]
        HOT_H --> HOT_I[Wait for developer decision and instructions]
        HOT_G --> HOT_J["Run tests<br>failing tests + surrounding tests must pass"]
        HOT_J --> HOT_K{Tests green?}
        HOT_K -->|No| HOT_L[Fix]
        HOT_L --> HOT_J
        HOT_K -->|Yes| HOT_M["Final check with git diff --stat<br>verify no unexpected files included"]
        HOT_M --> HOT_N{Changes minimal?}
        HOT_N -->|No| HOT_O["Narrow scope<br>move refactoring/cleanup to separate PR"]
        HOT_O --> HOT_G
        HOT_N -->|Yes| HOT_P["Record bug pattern and fix in tasks/lessons.md"]
        HOT_P --> HOT_DONE(["Developer: immediate PR, emergency approval, merge<br>deploy, share post-review plan"])
    end
```

---

## Notes

### Criteria for Normal Bug vs Hotfix

| Criteria | Normal Bug | Hotfix |
|---------|-----------|--------|
| Production impact | None or minor | Yes (data corruption, outage, security) |
| Response deadline | Next sprint | Same day to hours |
| code-review | Normal flow | Post-review acceptable |
| PR process | Normal | Use emergency approval route |

### Why recording in lessons.md matters

Recording bug patterns prevents repeating the same mistakes in the next session.
ADR violations in particular (missing logical delete, using `new Date()`, creating dynamic routes) must always be recorded.
See the "self-improvement loop" in the `dev-workflow` skill for write triggers and format.

### What NOT to do in hotfixes

- Mix in refactoring (expands scope)
- Skip hooks with `git commit --no-verify`
- Force push with `git push --force`
- Hide symptoms without investigating root cause
