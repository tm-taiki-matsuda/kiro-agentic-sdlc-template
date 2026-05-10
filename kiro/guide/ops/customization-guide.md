# kiro-cli Configuration Customization Guide

> Procedures for adding and modifying agents, skills, and hooks.
> Last updated: 2026-05-10 | kiro-cli 2.1.1

---

## 1. Adding a New Agent

### 1-1. Create the JSON file

Create `.kiro/agents/{name}.json`. The safest approach is to copy an existing agent and edit it.

```bash
cp .kiro/agents/backend-feature.json .kiro/agents/new-agent.json
```

Required fields:

```json
{
  "name": "new-agent",
  "description": "Agent description (shown in agent list)",
  "prompt": "file://../prompts/new-agent.md",
  "tools": ["fs_read", "fs_write", "execute_bash", "grep", "glob", "task", "code"],
  "allowedTools": ["code", "fs_read", "glob", "grep", "task"],
  "toolsSettings": {
    "fs_write": {
      "allowedPaths": ["target-directory/**"],
      "deniedPaths": ["**/.env", "**/.env.*", "**/package-lock.json", "**/*.secrets.*"]
    },
    "execute_bash": { "autoAllowReadonly": true }
  },
  "resources": [
    "file://tasks/todo.md",
    "file://tasks/lessons.md",
    "skill://.kiro/skills/tech-stack/SKILL.md",
    "skill://.kiro/skills/dev-workflow/SKILL.md"
  ],
  "hooks": {
    "agentSpawn": [{ "command": "bash .kiro/scripts/session-start-hook.sh" }],
    "stop": [{ "command": "bash .kiro/scripts/stop-hook.sh" }],
    "preToolUse": [
      { "matcher": "shell", "command": "bash .kiro/scripts/security-hook.sh" },
      { "matcher": "write", "command": "bash .kiro/scripts/guard-schema-hook.sh" }
    ],
    "postToolUse": [
      { "matcher": "write", "command": "bash .kiro/scripts/prettier-hook.sh", "timeout_ms": 15000 },
      { "matcher": "shell", "command": "bash .kiro/scripts/test-summary-hook.sh" }
    ]
  }
}
```

### 1-2. Create the prompt file

Create `.kiro/prompts/{name}.md`.

```markdown
# Agent: {Agent Name}

## Role
{Describe the agent's role}

## Operating Rules
- Follow the Language Policy defined in the Language Policy section of the product-context skill.
- {Other rules}

## Workflow
{Step-by-step procedure}
```

### 1-3. Verify

```bash
kiro-cli agent list  # verify new agent appears
kiro-cli chat --agent new-agent
```

---

## 2. Adding a New Skill

### 2-1. Create directory and file

```bash
mkdir -p .kiro/skills/{skill-name}
cat > .kiro/skills/{skill-name}/SKILL.md << 'EOF'
---
name: "Skill Name"
description: "Skill description (describe when agents should reference this)"
---

# Skill Name

{Skill content}
EOF
```

### 2-2. Add to agent

Add to the JSON of agents that should use it:

```json
"resources": [
  ...
  "skill://.kiro/skills/{skill-name}/SKILL.md"
]
```

---

## 3. Adding a Hook Script

### 3-1. Create the script

```bash
cat > .kiro/scripts/my-hook.sh << 'EOF'
#!/bin/bash
EVENT=$(cat)
# Process event data
echo "Hook executed: $EVENT"
EOF
chmod +x .kiro/scripts/my-hook.sh
```

### 3-2. Add to agent

```json
"hooks": {
  "postToolUse": [
    {
      "matcher": "write",
      "command": "bash .kiro/scripts/my-hook.sh"
    }
  ]
}
```

---

## 4. Managing Common Configuration

Common settings for all agents can be written in `shared-agent-config.json`.
The `sync-agents.py` script can propagate them to each agent.

```bash
python3 .kiro/scripts/sync-agents.py
```

---

## 5. Adapting to Your Project Structure

This framework assumes a specific monorepo layout (see `product-context/SKILL.md`).
If your project differs, update these files:

### 5-1. Directory structure

Edit `code-structure/SKILL.md` to reflect your actual directory layout.
Agents read this skill to decide where to place files.

### 5-2. Agent write permissions

Each agent's `allowedPaths` controls where it can write. Update them in the agent JSON:

```json
"toolsSettings": {
  "fs_write": {
    "allowedPaths": [
      "your-backend-dir/src/**",
      "your-backend-dir/tests/**",
      "tasks/**"
    ]
  }
}
```

### 5-3. design/ directory

Agents that reference design documents use a `knowledgeBase` resource pointing to `./design`.
If your design docs live elsewhere, update the `source` field in each agent JSON:

```json
{
  "type": "knowledgeBase",
  "source": "file://./your-docs-directory",
  "name": "Design Documents"
}
```

If you don't use design documents at all, remove the `knowledgeBase` entry from:
`bug-fix.json`, `code-review.json`, `design-updater.json`, `spec-writer.json`, `system-guide.json`, `client-doc.json`

### 5-4. Validate after changes

```bash
python3 .kiro/scripts/validate-kiro-config.py
```

---

## 6. Validate Configuration

```bash
python3 .kiro/scripts/validate-kiro-config.py
```
