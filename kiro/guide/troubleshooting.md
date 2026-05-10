# kiro-cli Troubleshooting

> Common problems encountered during agent operation and how to resolve them.
> Last updated: 2026-05-10 | kiro-cli 2.1.1

---

## Agent Behavior Issues

### Agent starts implementing without reading the spec

**Cause**: Spec path not explicitly stated in the prompt
**Fix**:
```
Please implement based on the spec in .kiro/specs/{feature-name}/.
Read requirements.md and design.md first, then present the implementation plan.
```

### Agent generates code that violates ADRs

**Cause**: Skill not auto-loaded
**Fix**:
1. Explicitly mention skill name in prompt: `Please check the adr-quick-reference skill before implementing`
2. After generation, review with `code-review` agent

### Agent tries to write to unauthorized paths

**Cause**: Outside `toolsSettings.fs_write.allowedPaths` scope
**Fix**: Use `bug-fix` agent for cross-layer changes

### schema.prisma change is blocked

**Cause**: `guard-schema-hook.sh` blocks writes from agents other than db-migration
**Fix**: Switch to `db-migration` agent

---

## Hook-Related Issues

### prettier-hook.sh throws an error

**Cause**: prettier not installed in the target package's `node_modules`
**Fix**:
```bash
cd backend && npm install   # or frontend / functions / shared
```

### security-hook.sh blocks a legitimate command

**Cause**: `git push --force`, `rm -rf`, `DROP TABLE`, `TRUNCATE`, `terraform destroy` are pattern-matched
**Fix**: These commands are intentionally blocked. If truly needed, run manually from the terminal

---

## Knowledge Base Issues

### Can't search design documents

**Cause**: Knowledge base not initialized
**Fix**:
```bash
bash .kiro/scripts/setup-knowledge.sh
```
Or in each agent:
```
/knowledge add design ./design
```

### Knowledge base content is outdated

**Cause**: `autoUpdate: true` is set but index hasn't been updated
**Fix**:
```
/knowledge update design
```

---

## Session Management Issues

### Can't resume from previous session

**Cause**: `tasks/todo.md` is empty or `handoff-*.md` was deleted
**Fix**: Check `[IN_PROGRESS]` tasks in `.kiro/specs/{feature-name}/tasks.md` and resume manually

### Agent forgets previous instructions

**Cause**: Context window is full
**Fix**:
1. Use `/compact` to summarize the conversation
2. If still not improving, use `/quit` → launch a new session

---

## Installation & Authentication Issues

### Check kiro-cli version

```bash
kiro-cli --version
```

### When authentication expires

```bash
kiro-cli auth login
```

### Update

```bash
wget -O kiro-cli.deb https://desktop-release.q.us-east-1.amazonaws.com/latest/kiro-cli.deb
sudo dpkg -i kiro-cli.deb
```
