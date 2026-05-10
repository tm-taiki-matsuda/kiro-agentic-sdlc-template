# How kiro-cli Works

> Explains how agents, skills, prompts, hooks, and MCP work together.
> Last updated: 2026-05-10 | kiro-cli 2.1.1

---

## 1. Overall Structure

kiro-cli configuration consists of six elements:

```
┌─────────────────────────────────────────────────────────┐
│  Developer                                               │
│    └─ kiro-cli chat --agent backend-feature              │
└────────────────────────┬────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────┐
│  Agent (.kiro/agents/backend-feature.json)               │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │
│  │ Prompt   │  │ Tools    │  │ Resources             │  │
│  │ persona  │  │ read/    │  │ file:// skill:// KB   │  │
│  │ workflow │  │ write    │  │                       │  │
│  └─────┬────┘  └─────┬────┘  └──────────┬───────────┘  │
│        │             │                   │               │
│  prompts/         tools +            skills/             │
│  backend-         allowedTools +     product-context     │
│  feature.md       toolsSettings      tech-stack ...     │
│                                                          │
│  ┌──────────┐  ┌──────────────┐                         │
│  │ Hooks    │  │ MCP Servers  │                         │
│  │ auto-run │  │ external     │                         │
│  └─────┬────┘  └──────┬───────┘                         │
│        │              │                                  │
│  scripts/         postgres                               │
│  prettier-hook    playwright                             │
│  security-hook    design-docs                            │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Agent JSON Structure

Each agent is defined in `.kiro/agents/<name>.json`.

```
backend-feature.json
│
├── name: "backend-feature"
├── description: "Backend API..."
│
├── prompt ─────────────────── agent persona and workflow
│   └── "file://../prompts/backend-feature.md"
│
├── tools ──────────────────── all available tools
│   └── [fs_read, fs_write, execute_bash, grep, glob, task, code]
│
├── allowedTools ───────────── tools that run without approval
│   └── [code, fs_read, glob, grep, task]
│       ※ fs_write and execute_bash require approval
│
├── toolsSettings ──────────── per-tool detailed constraints
│   ├── fs_write:
│   │   ├── allowedPaths: [backend/src/**, backend/tests/**, ...]
│   │   └── deniedPaths:  [**/.env, **/package-lock.json, ...]
│   └── execute_bash:
│       └── autoAllowReadonly: true  ← ls, cat, etc. don't need approval
│
├── resources ──────────────── information sources loaded at startup
│   ├── "file://tasks/todo.md"              ← immediate full load
│   ├── "skill://.kiro/skills/tech-stack/..." ← on-demand load
│   └── { type: "knowledgeBase", ... }      ← semantic search
│
├── hooks ──────────────────── lifecycle hooks
│   ├── agentSpawn: [session-start-hook.sh]
│   ├── userPromptSubmit: [git branch + diff stat]
│   ├── preToolUse: [security-hook.sh, guard-schema-hook.sh]
│   ├── postToolUse: [prettier-hook.sh, test-summary-hook.sh]
│   └── stop: [stop-hook.sh]
│
├── mcpServers ─────────────── external tool connections
│   └── postgres: { command: "npx", args: [...] }
│
├── keyboardShortcut: "ctrl+shift+b"
└── welcomeMessage: "..."
```

---

## 3. Three Types of Resources

### file:// — Immediate Full Load

```json
"file://tasks/todo.md"
```

Loads the entire file into context when the agent starts.
Used for files referenced every session, like `todo.md` and `lessons.md`.

### skill:// — On-Demand Load

```json
"skill://.kiro/skills/tech-stack/SKILL.md"
```

Loaded when the agent determines it's needed.
Skill files have YAML frontmatter wrapped in `---`, indexed by `name` and `description`.

### knowledgeBase — Semantic Search

```json
{
  "type": "knowledgeBase",
  "source": "file://./design",
  "name": "Design Documents",
  "indexType": "best",
  "autoUpdate": true
}
```

References large document sets via vector search.
Design documents under `design/` can be searched with the `knowledge` tool.

---

## 4. Five Hook Triggers

| Trigger | Timing | Purpose |
|---------|--------|---------|
| `agentSpawn` | When agent starts (once) | Auto-load todo.md / lessons.md / handoff |
| `userPromptSubmit` | Every time user sends a prompt | Inject git branch + diff stat into context |
| `preToolUse` | Before tool execution | Block dangerous commands, protect schema.prisma |
| `postToolUse` | After tool execution | Auto-run Prettier, summarize test results |
| `stop` | When agent response completes | Show remaining task count, changed file count, test warnings |

---

## 5. MCP Servers

Each agent individually defines the external tools it needs.

| MCP | Purpose | Used by |
|-----|---------|---------|
| `postgres` | Direct PostgreSQL queries | backend-feature, db-migration, functions-feature |
| `playwright` | Browser operations | frontend-feature, e2e-test |
| `design-docs` | Read-only access to design/ | spec-writer, db-migration, design-updater, system-guide, client-doc |

---

## 6. Configuration File Locations

```
.kiro/
├── agents/          agent definitions (13 files)
├── prompts/         agent prompts (13 files)
├── skills/          skills (18 files)
├── settings/
│   ├── cli.json     global settings (model, feature flags, compaction)
│   └── mcp.json     global MCP (usually empty)
├── scripts/         hook scripts (11 files)
├── specs/           work-in-progress specs (working directory)
│   └── _template/   spec templates
└── shared-agent-config.json  common denied paths for all agents

kiro/
├── guide/           documentation (this file)
└── workflows/       workflow diagrams (Mermaid)

tasks/
├── todo.md          session-level task management
├── lessons.md       lessons and improvement pattern records
└── handoff-*.md     agent-to-agent handoffs (temporary files)
```
