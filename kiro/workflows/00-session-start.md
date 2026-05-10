# Session Start Protocol

> **Common starting point for all flows.** All agents begin work from this protocol.
> The `agentSpawn` hook runs automatically — no manual action required from the developer.

---

## Flow Diagram

```mermaid
flowchart TD
    START([Agent launched<br>kiro-cli chat --agent xxx]) --> HOOK

    subgraph HOOK["🔧 agentSpawn hook (auto-run)"]
        HOOK_A[/load tasks/todo.md/] --> HOOK_B[/load tasks/lessons.md/]
        HOOK_B --> HOOK_C[/auto-detect tasks/handoff-*.md/]
    end

    HOOK_C --> A{Active spec in .kiro/specs/?<br>directory other than _template}

    A -->|Yes| B[Read tasks.md<br>identify IN_PROGRESS / TODO tasks]
    A -->|No| F["Ask developer: 'What is the task for this session?'"]

    B --> C{Handoff file<br>handoff-*.md exists?}
    C -->|Yes| E[Read handoff document<br>completed / remaining tasks / test status / notes]
    C -->|No| D[Confirm continuing tasks with developer]

    D --> G{Continue or new?}
    G -->|Continue| H[Resume implementation from last session<br>start from IN_PROGRESS tasks in tasks.md]
    G -->|New task| F

    E --> H
    F --> I[Developer: describe task/request]
    I --> DONE([Start work])
    H --> DONE
```

---

## Notes

### Why tasks/lessons.md is referenced

By reviewing mistake patterns and improvements recorded in past sessions every time,
the same errors are prevented from recurring.

### Auto-detection of active specs

If a directory other than `_template` exists in `.kiro/specs/`,
it is treated as a spec with implementation in progress, and that directory's `tasks.md` is auto-loaded.
Also, the `userPromptSubmit` hook displays the active spec path on every prompt submission.

### Multi-session handoff

For work spanning multiple sessions, `tasks/handoff-{feature}.md` is used.
The `agentSpawn` hook auto-detects `tasks/handoff-*.md`,
and if the file exists, displays the first 10 lines to inject handoff information into the agent.

### Constraint on switching with `/agent` command

When switching agents with `/agent xxx` during a chat, **the agentSpawn hook does not fire**.
Therefore, for agent switches across phases, it is recommended to use
`/quit` → `kiro-cli chat --agent xxx` to launch as a new session.

### Session end check by stop hook

When the agent's response completes, `stop-hook.sh` runs automatically and reports:
- Remaining task count (incomplete items in `tasks/todo.md`)
- Changed file count (warning if over 20)
- Test not-run warnings
