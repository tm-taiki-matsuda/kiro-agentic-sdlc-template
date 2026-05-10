# kiro-cli Glossary

> Explanations of terms used in kiro-cli.
> Last updated: 2026-05-10 | kiro-cli 2.1.1

---

## AI Basics

### LLM (Large Language Model)
The AI model that powers kiro-cli. This framework uses `claude-sonnet-4.6`.

### Context Window
The upper limit of information an AI can handle at once. As conversations get longer, older information gets pushed out.
In kiro-cli, you can use the `/compact` command to summarize the conversation and free up context.

### Prompt
Instructions given to AI. The `prompts/*.md` files in agents function as system prompts.

### Hallucination
The phenomenon where AI generates plausible-sounding falsehoods. It may generate non-existent file paths or APIs.
This can be prevented by verifying the changed file list at approval points.

---

## kiro-cli Core Concepts

### Agent
A specialized AI separated by role. Defined in `.kiro/agents/*.json`.
This framework has 13 agents.

### Spec
A 3-file set (requirements.md / design.md / tasks.md) that defines "what to build."
Placed in `.kiro/specs/{feature-name}/`.

### Skill
A collection of project-specific rules that agents reference. Defined in `.kiro/skills/*/SKILL.md`.
Loaded on-demand via the `skill://` protocol.

### Hook
Scripts that automatically execute in sync with agent actions.
Five trigger points: agentSpawn / userPromptSubmit / preToolUse / postToolUse / stop

### Session
One interaction from `kiro-cli chat --agent xxx` launch to `/quit`.

### Compaction
A feature that summarizes long conversations to free up the context window. Run with the `/compact` command.

### MCP Server (Model Context Protocol Server)
A standardized protocol for AI to call external tools.
This framework uses three types: postgres / playwright / design-docs.

---

## Project Mechanisms

### ADR (Architecture Decision Record)
Technical rules that must be followed across the entire project. This framework defines 8 ADRs (ADR-001 through ADR-008).
The `adr-quick-reference` skill contains violation vs. correct examples.

### allowedPaths / deniedPaths
A mechanism that physically restricts an agent's write scope.
Configured in `toolsSettings.fs_write.allowedPaths`. Cannot be bypassed by AI judgment.

### Knowledge Base
Design documents made searchable via semantic search.
Documents under `design/` are vectorized and searchable with the `knowledge` tool.

### EARS Notation
A notation for writing requirements at a testable granularity.
Written in the format `WHEN {condition} THEN the system {expected behavior}`.
See the `spec-ears-notation-guide` skill for details.

### Optimistic Lock
A mechanism to detect conflicts when multiple users update the same data simultaneously.
Implemented with the `version` field. Returns HTTP 409 on mismatch (ADR-006).

### Logical Delete (Soft Delete)
A method of not physically deleting data, but updating `is_deleted = true` (ADR-005).
`DELETE` statements are prohibited.

---

## Development Flow Terms

### TDD (Test-Driven Development)
A development method where tests are written before implementation.
Proceeds in order: Red (failing test) → Green (implementation that passes) → Refactor.

### Spec-Driven Development
A development method that starts from spec files.
`spec-writer` creates the spec, and implementation agents implement based on the spec.

### Handoff
A mechanism for passing work between agents across sessions.
Records completed tasks, remaining tasks, and test status in `tasks/handoff-{feature-name}.md`.
