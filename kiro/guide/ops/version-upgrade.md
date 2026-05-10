# kiro-cli Version Upgrade Procedure

> Procedure for evaluating and updating configuration files during kiro-cli major/minor updates.
> Last updated: 2026-05-10 | kiro-cli 2.1.1
> Current version: 2.1.1

---

## When to Run

- After a kiro-cli major/minor version upgrade (e.g., 2.0 → 2.1)
- After significantly changing the agent structure
- After adding new skills or agents
- Periodic maintenance (approximately quarterly)

Usually not needed for patch versions (e.g., 2.0.0 → 2.0.1).

---

## Phase 1: Preparation (10 min)

### 1-1. Record current version

```bash
kiro-cli --version
# → Record: ___________
```

### 1-2. Update kiro-cli

```bash
wget https://desktop-release.q.us-east-1.amazonaws.com/latest/kiro-cli.deb
sudo dpkg -i kiro-cli.deb
kiro-cli --version
# → Record: ___________
```

### 1-3. Review changelog

```
https://kiro.dev/changelog/
```

Check for the following changes:

| Check Item | Impact Scope |
|-----------|-------------|
| Agent configuration schema changes | All `.kiro/agents/*.json` |
| New hook trigger additions | hooks section |
| Tool name changes/additions | tools / allowedTools |
| resources URI schema changes | file:// / skill:// |
| New settings keys | `.kiro/settings/cli.json` |
| MCP server spec changes | mcpServers |
| Skills format changes | `.kiro/skills/*/SKILL.md` |

### 1-4. Backup configuration files

```bash
cd /path/to/your-project
git stash  # if there are uncommitted changes
```

---

## Phase 2: Automated Integrity Check (5 min)

### 2-1. Run validation script

```bash
cd /path/to/your-project
python3 .kiro/scripts/validate-kiro-config.py
```

### 2-2. Review results

| Result | Action |
|--------|--------|
| ✅ No issues | Proceed to Phase 3 |
| 🔴 Errors | Fix errors before Phase 3 |
| 🟡 Warnings only | Decide on action together with Phase 3 |

### 2-3. Validate agent configurations

```bash
# Validate all agent configurations
for agent in $(ls .kiro/agents/*.json | grep -v _shared); do
  echo -n "$(basename $agent): "
  kiro-cli agent validate --path "$agent" 2>&1
done
```

---

## Phase 3: Quality Evaluation by Default Agent (30–60 min)

### 3-1. Launch kiro-cli

```bash
cd /path/to/your-project
kiro-cli
```

### 3-2. Request evaluation

Paste the following prompt as-is:

```
Assume you are an AI development specialist with expertise in kiro-cli,
and evaluate/critique the quality of the current kiro configuration files.

Steps:
1. Catch up on the latest kiro-cli information and AI development best practices
2. Review the project source code structure
3. Load all files under .kiro/ (agents, skills, prompts, scripts, settings)
4. Identify areas for improvement
5. Summarize fix points, improvement suggestions, and proposals as a professional

Current version: {new version}
Previous version: {old version}
Key changelog changes: {bullet points from Phase 1-3 review}
```

### 3-3. Record evaluation results

Review agent output and organize:

| Priority | Content | Action Needed |
|----------|---------|--------------|
| 🔴 Must fix | | |
| 🟡 Recommended | | |
| 🔵 Suggestion | | |

---

## Phase 4: Apply Fixes (time varies)

### 4-1. Decide fix approach

- 🔴 Address all
- 🟡 Decide based on cost-benefit
- 🔵 Can defer to next time

### 4-2. Request fixes from default agent

```
I'd like to address all items from high to low priority.
Please create a plan first, then apply the fixes.
Base the approach on best practices.
```

### 4-3. Notes during fixes

- Always syntax-check JSON modified by agents
- If `shared-agent-config.json` was changed, run `sync-agents.py`
- If SKILL.md was changed, verify frontmatter name/description

---

## Phase 5: Post-verification (10 min)

### 5-1. Re-run integrity check

```bash
cd /path/to/your-project
python3 .kiro/scripts/validate-kiro-config.py
```

Verify 🔴 errors = 0.

### 5-2. Verify agent behavior

Launch one representative agent and verify normal operation:

```bash
kiro-cli chat --agent backend-feature
```

Check:
- [ ] agentSpawn hook runs correctly (todo.md / lessons.md / handoff displayed)
- [ ] Skill metadata loads (verify with `/context show`)
- [ ] welcomeMessage is displayed

### 5-3. Update documentation

Reflect this session's changes in the following files:

| File | Update Content |
|------|---------------|
| `kiro/guide/ops/migration-log.md` | Add change log entry |
| `kiro/guide/onboarding.md` | Update directory structure diagram (if files added/removed) |
| `kiro/guide/agent-usage.md` | Update script table (if scripts added) |
| `kiro/guide/troubleshooting.md` | Add new troubleshooting items |

### 5-4. Update this document's version

Update the "Current version" at the top of this document to the new version.

---

## Phase 6: Team Sharing (5 min)

```bash
cd /path/to/your-project

# Review changes
git diff --stat

# Commit
git add .kiro/ kiro/ tasks/
git commit -m "kiro: v{old-version} → v{new-version} configuration update"
git push
```

---

## Completion Checklist

```
Phase 1: Preparation
  [ ] Recorded old version
  [ ] Updated kiro-cli
  [ ] Reviewed changelog
  [ ] Created backup

Phase 2: Automated Check
  [ ] Ran validate-kiro-config.py
  [ ] Ran kiro-cli agent validate for all agents

Phase 3: Quality Evaluation
  [ ] Requested evaluation from default agent
  [ ] Organized evaluation results (🔴/🟡/🔵)

Phase 4: Fixes
  [ ] Addressed all 🔴 must-fix items
  [ ] Decided on 🟡 recommended items
  [ ] Decided on 🔵 suggestion items

Phase 5: Post-verification
  [ ] validate-kiro-config.py shows 🔴 0 errors
  [ ] Verified agent behavior
  [ ] Updated documentation
  [ ] Updated this document's version

Phase 6: Team Sharing
  [ ] git commit & push done
```

---

## Version Upgrade History

| Date | Old → New | Key Changes | Author |
|------|-----------|------------|--------|
| {YYYY-MM-DD} | — → {version} | Initial configuration for this project | {author} |
