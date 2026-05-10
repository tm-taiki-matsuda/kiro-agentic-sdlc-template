# kiro-cli Architecture Diagrams

> Visualizes the overall structure of kiro-cli configuration with Mermaid diagrams.
> Last updated: 2026-05-10 | kiro-cli 2.1.1

---

## 1. Overall Structure

```mermaid
graph TB
    DEV[👤 Developer] -->|"kiro-cli chat --agent xxx"| AGENT

    subgraph AGENT["Agent (.kiro/agents/*.json)"]
        PROMPT["📝 Prompt<br>persona, workflow, decision criteria<br>prompts/*.md"]
        TOOLS["🔧 Tools<br>fs_read / fs_write / execute_bash<br>grep / glob / code / task"]
        RESOURCES["📚 Resources<br>file:// → immediate load<br>skill:// → on-demand<br>knowledgeBase → semantic search"]
        HOOKS["⚡ Hooks<br>scripts/*.sh<br>5 trigger points"]
        MCP["🔌 MCP Servers<br>postgres / playwright / design-docs"]
    end

    RESOURCES -->|"skill://"| SKILLS["📖 Skills × 18<br>.kiro/skills/*/SKILL.md"]
    RESOURCES -->|"file://"| FILES["📄 Task Management<br>tasks/todo.md / lessons.md"]
    RESOURCES -->|"knowledgeBase"| KB["🔍 Knowledge Base<br>design/ semantic search"]
    HOOKS -->|"execute"| SCRIPTS["📜 Common Scripts<br>.kiro/scripts/"]
    TOOLS -->|"constrained by"| SETTINGS["⚙️ toolsSettings<br>allowedPaths / deniedPaths"]

    AGENT -->|"generate/modify"| CODE["💻 Project Code<br>backend / frontend / functions / shared"]
    AGENT -->|"reference"| SPECS["📋 Specs<br>.kiro/specs/{feature}/"]
    AGENT -->|"reference"| DESIGN["📐 Design Docs<br>design/"]
```

---

## 2. Agent Structure — 13 Agents and Write Scopes

```mermaid
graph LR
    subgraph "Implementation"
        BE["backend-feature<br>Ctrl+Shift+B"]
        FE["frontend-feature<br>Ctrl+Shift+F"]
        FN["functions-feature<br>Ctrl+Shift+G"]
        E2E["e2e-test<br>Ctrl+Shift+E"]
        DB["db-migration<br>Ctrl+Shift+D"]
        SP["shared-package<br>Ctrl+Shift+S"]
        IF["infrastructure<br>Ctrl+Shift+I"]
    end

    subgraph "Cross-cutting"
        BF["bug-fix<br>Ctrl+Shift+X"]
        CR["code-review<br>Ctrl+Shift+R (read-only)"]
    end

    subgraph "Design & Spec"
        SW["spec-writer<br>Ctrl+Shift+W"]
        DU["design-updater<br>Ctrl+Shift+U"]
        SG["system-guide<br>Ctrl+Shift+H (read-only)"]
        CD["client-doc<br>Ctrl+Shift+C"]
    end

    BE -->|"writes"| BACK["backend/src/**<br>backend/tests/**<br>shared/src/**"]
    FE -->|"writes"| FRONT["frontend/src/**<br>frontend/tests/**"]
    FN -->|"writes"| FUNC["functions/src/**<br>functions/tests/**"]
    E2E -->|"writes"| E2EDIR["frontend/tests/pages/**<br>frontend/tests/keywords/**<br>frontend/tests/testcases/**"]
    DB -->|"writes"| SCHEMA["database/prisma/schema.prisma"]
    SP -->|"writes"| SHARED["shared/src/**<br>shared/constants/**"]
    IF -->|"writes"| INFRA["infrastructure/**"]
    BF -->|"writes"| ALL["all layers"]
    SW -->|"writes"| SPECS[".kiro/specs/**"]
    DU -->|"writes"| DESIGNDIR["design/**"]
    CD -->|"writes"| OUTPUT["output/**"]
```

---

## 3. Hook Lifecycle

```mermaid
sequenceDiagram
    participant DEV as Developer
    participant KIRO as kiro-cli
    participant HOOK as Hook Scripts
    participant AGENT as Agent

    DEV->>KIRO: kiro-cli chat --agent xxx
    KIRO->>HOOK: agentSpawn hook
    HOOK->>AGENT: inject todo.md / lessons.md / handoff-*.md

    loop During conversation
        DEV->>AGENT: send prompt
        KIRO->>HOOK: userPromptSubmit hook
        HOOK->>AGENT: inject git branch + diff stat

        AGENT->>KIRO: request tool execution (fs_write)
        KIRO->>HOOK: preToolUse hook (security-hook / guard-schema-hook)
        HOOK-->>KIRO: OK or BLOCKED

        KIRO->>AGENT: execute tool
        KIRO->>HOOK: postToolUse hook (prettier-hook / test-summary-hook)
    end

    AGENT->>KIRO: response complete
    KIRO->>HOOK: stop hook
    HOOK->>DEV: remaining task count, changed file count, test warnings
```

---

## 4. Skill Reference Mechanism

```mermaid
graph LR
    AGENT["Agent"] -->|"skill:// protocol"| INDEX["Skill Index<br>(name + description)"]
    INDEX -->|"when determined needed"| SKILL["Full Skill File<br>SKILL.md"]
    SKILL -->|"added to context"| AGENT

    NOTE["18 skills not loaded at startup<br>→ saves context window"]
```
