#!/usr/bin/env python3
"""
Kiro CLI configuration file integrity validation script.
Run before/after version upgrades or configuration changes to detect issues.

Usage:
  cd <project-root>
  python3 .kiro/scripts/validate-kiro-config.py
"""
import json, glob, os, sys, re

KIRO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
_config_dir = os.path.join(KIRO_DIR, "..")
_symlink = os.path.join(_config_dir, "..", ".kiro")
if os.path.islink(_symlink):
    PROJECT_ROOT = os.path.dirname(os.path.realpath(_symlink))
else:
    PROJECT_ROOT = _config_dir
errors = []
warnings = []


def error(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


# ─── 1. Agent JSON syntax check ───
def check_agent_json():
    for path in sorted(glob.glob(os.path.join(KIRO_DIR, "agents", "*.json"))):
        name = os.path.basename(path)
        try:
            with open(path) as f:
                json.load(f)
        except json.JSONDecodeError as e:
            error(f"[JSON] {name}: syntax error — {e}")


# ─── 2. shared-agent-config.json and agent deniedPaths sync check ───
def check_denied_paths_sync():
    shared_path = os.path.join(KIRO_DIR, "shared-agent-config.json")
    if not os.path.exists(shared_path):
        warn("[SYNC] shared-agent-config.json not found")
        return
    shared = json.load(open(shared_path))
    expected = shared.get("deniedPaths", [])

    for path in sorted(glob.glob(os.path.join(KIRO_DIR, "agents", "*.json"))):
        name = os.path.basename(path)
        if name.startswith("_"):
            continue
        agent = json.load(open(path))
        fw = agent.get("toolsSettings", {}).get("fs_write", {})
        actual = fw.get("deniedPaths")
        if actual is None:
            continue
        if actual != expected:
            warn(f"[SYNC] {name}: deniedPaths differs from shared-agent-config.json. Run: python3 .kiro/scripts/sync-agents.py")


# ─── 3. SKILL.md frontmatter check ───
def check_skill_frontmatter():
    for path in sorted(glob.glob(os.path.join(KIRO_DIR, "skills", "*", "SKILL.md"))):
        skill_name = os.path.basename(os.path.dirname(path))
        with open(path) as f:
            content = f.read()
        if not content.startswith("---"):
            error(f"[SKILL] {skill_name}/SKILL.md: missing YAML frontmatter")
            continue
        parts = content.split("---", 2)
        if len(parts) < 3:
            error(f"[SKILL] {skill_name}/SKILL.md: frontmatter not closed")
            continue
        fm = parts[1]
        if "name:" not in fm:
            error(f"[SKILL] {skill_name}/SKILL.md: frontmatter missing 'name'")
        if "description:" not in fm:
            error(f"[SKILL] {skill_name}/SKILL.md: frontmatter missing 'description'")


# ─── 4. resources reference existence check ───
def check_resource_references():
    for path in sorted(glob.glob(os.path.join(KIRO_DIR, "agents", "*.json"))):
        name = os.path.basename(path)
        if name.startswith("_"):
            continue
        agent = json.load(open(path))
        for res in agent.get("resources", []):
            if isinstance(res, dict):
                continue  # skip knowledgeBase resources
            if res.startswith("file://"):
                file_path = res[len("file://"):]
                full = os.path.join(PROJECT_ROOT, file_path)
                if "*" not in file_path and not os.path.exists(full):
                    error(f"[REF] {name}: file://{file_path} does not exist")
            elif res.startswith("skill://"):
                skill_path = res[len("skill://"):]
                if "*" not in skill_path:
                    full = os.path.join(PROJECT_ROOT, skill_path)
                    if not os.path.exists(full):
                        error(f"[REF] {name}: skill://{skill_path} does not exist")


# ─── 5. prompt field file:// reference check ───
def check_prompt_references():
    for path in sorted(glob.glob(os.path.join(KIRO_DIR, "agents", "*.json"))):
        name = os.path.basename(path)
        if name.startswith("_"):
            continue
        agent = json.load(open(path))
        prompt = agent.get("prompt", "")
        if prompt.startswith("file://"):
            file_path = prompt[len("file://"):]
            agent_dir = os.path.dirname(path)
            full = os.path.normpath(os.path.join(agent_dir, file_path))
            if not os.path.exists(full):
                error(f"[PROMPT] {name}: prompt {prompt} does not exist (resolved: {full})")
        elif prompt and not prompt.startswith("file://"):
            if len(prompt) > 200:
                warn(f"[PROMPT] {name}: inline prompt is long ({len(prompt)} chars). Consider migrating to file:// reference")


# ─── 6. scripts/ execute permission check ───
def check_script_permissions():
    for path in sorted(glob.glob(os.path.join(KIRO_DIR, "scripts", "*.sh"))):
        name = os.path.basename(path)
        if not os.access(path, os.X_OK):
            error(f"[PERM] scripts/{name}: missing execute permission. Run: chmod +x")


# ─── 7. hook script existence check ───
def check_hook_scripts():
    for path in sorted(glob.glob(os.path.join(KIRO_DIR, "agents", "*.json"))):
        name = os.path.basename(path)
        if name.startswith("_"):
            continue
        agent = json.load(open(path))
        for trigger, hooks in agent.get("hooks", {}).items():
            for hook in hooks:
                cmd = hook.get("command", "")
                match = re.search(r'bash\s+(\S+\.sh)', cmd)
                if match:
                    script = match.group(1)
                    full = os.path.join(PROJECT_ROOT, script)
                    if not os.path.exists(full):
                        error(f"[HOOK] {name}: {trigger} hook script {script} does not exist")


# ─── 8a. unnecessary write matcher hook warning ───
def check_unnecessary_hook_matchers():
    write_tools = {"fs_write", "fsWrite", "write"}
    for path in sorted(glob.glob(os.path.join(KIRO_DIR, "agents", "*.json"))):
        name = os.path.basename(path)
        if name.startswith("_"):
            continue
        agent = json.load(open(path))
        has_write = bool(write_tools & set(agent.get("tools", [])))
        for trigger in ("preToolUse", "postToolUse"):
            for hook in agent.get("hooks", {}).get(trigger, []):
                matcher = hook.get("matcher", "")
                if matcher in write_tools and not has_write:
                    warn(f"[HOOK] {name}: {trigger} has '{matcher}' matcher but tools does not include fs_write")


# ─── 8b. cross-cutting required skills check ───
REQUIRED_SKILLS_ALL = ["tech-stack", "dev-workflow"]
REQUIRED_SKILLS_IMPL = ["security-constraints"]
READ_ONLY_AGENTS = {"code-review", "system-guide"}
EXEMPT_AGENTS_ALL = set()
EXEMPT_AGENTS_WORKFLOW = {"infrastructure", "system-guide", "client-doc"}
SECURITY_EXEMPT = {"code-review"}

def check_required_skills():
    for path in sorted(glob.glob(os.path.join(KIRO_DIR, "agents", "*.json"))):
        name = os.path.basename(path).replace(".json", "")
        if name.startswith("_"):
            continue
        agent = json.load(open(path))
        skill_refs = [r for r in agent.get("resources", []) if isinstance(r, str) and r.startswith("skill://")]
        skill_names = {r.split("/")[-2] for r in skill_refs if "/skills/" in r}
        if name not in EXEMPT_AGENTS_ALL:
            for skill in REQUIRED_SKILLS_ALL:
                if skill == "dev-workflow" and name in EXEMPT_AGENTS_WORKFLOW:
                    continue
                if skill not in skill_names:
                    warn(f"[SKILL] {name}: required cross-cutting skill '{skill}' not in resources")
        if name not in READ_ONLY_AGENTS and name not in EXEMPT_AGENTS_ALL:
            for skill in REQUIRED_SKILLS_IMPL:
                if skill not in skill_names and name not in SECURITY_EXEMPT:
                    warn(f"[SKILL] {name}: required implementation skill '{skill}' not in resources")


# ─── 8. agentSpawn cache_ttl_seconds check ───
def check_agent_spawn_cache():
    for path in sorted(glob.glob(os.path.join(KIRO_DIR, "agents", "*.json"))):
        name = os.path.basename(path)
        if name.startswith("_"):
            continue
        agent = json.load(open(path))
        for hook in agent.get("hooks", {}).get("agentSpawn", []):
            if hook.get("cache_ttl_seconds"):
                warn(f"[CACHE] {name}: agentSpawn has cache_ttl_seconds but it is ignored by kiro-cli")


# ─── 8c. userPromptSubmit hook consistency check ───
PROMPT_SUBMIT_EXEMPT = set()

def check_user_prompt_submit_hooks():
    for path in sorted(glob.glob(os.path.join(KIRO_DIR, "agents", "*.json"))):
        name = os.path.basename(path).replace(".json", "")
        if name.startswith("_") or name in PROMPT_SUBMIT_EXEMPT:
            continue
        agent = json.load(open(path))
        has_bash = "execute_bash" in agent.get("tools", []) or "shell" in agent.get("tools", [])
        has_hook = bool(agent.get("hooks", {}).get("userPromptSubmit"))
        if has_bash and not has_hook:
            warn(f"[HOOK] {name}.json: has execute_bash but no userPromptSubmit hook")


# ─── 9. keyboard shortcut duplicate check ───
def check_keyboard_shortcuts():
    shortcuts = {}
    for path in sorted(glob.glob(os.path.join(KIRO_DIR, "agents", "*.json"))):
        name = os.path.basename(path)
        if name.startswith("_"):
            continue
        agent = json.load(open(path))
        ks = agent.get("keyboardShortcut")
        if ks:
            if ks in shortcuts:
                error(f"[KEY] {name} and {shortcuts[ks]} have duplicate shortcut '{ks}'")
            shortcuts[ks] = name


# ─── 10. MCP server required environment variable check ───
def check_env_vars():
    required_vars = {}
    for path in sorted(glob.glob(os.path.join(KIRO_DIR, "agents", "*.json"))):
        name = os.path.basename(path)
        if name.startswith("_"):
            continue
        agent = json.load(open(path))
        for server_name, server in agent.get("mcpServers", {}).items():
            for arg in server.get("args", []):
                if "${" in str(arg):
                    var = arg.split("${")[1].split("}")[0]
                    required_vars.setdefault(var, []).append(name)
            for val in server.get("env", {}).values():
                if "${" in str(val):
                    var = val.split("${")[1].split("}")[0]
                    required_vars.setdefault(var, []).append(name)
    for var, agents in required_vars.items():
        if not os.environ.get(var):
            warn(f"[ENV] ${var} not set (used by: {', '.join(agents)})")


# ─── Run ───
def main():
    check_agent_json()
    check_denied_paths_sync()
    check_skill_frontmatter()
    check_resource_references()
    check_prompt_references()
    check_script_permissions()
    check_hook_scripts()
    check_agent_spawn_cache()
    check_unnecessary_hook_matchers()
    check_required_skills()
    check_user_prompt_submit_hooks()
    check_keyboard_shortcuts()
    check_env_vars()

    print("=" * 60)
    print("Kiro CLI Configuration Integrity Check Results")
    print("=" * 60)

    if errors:
        print(f"\n🔴 Errors: {len(errors)}")
        for e in errors:
            print(f"  {e}")

    if warnings:
        print(f"\n🟡 Warnings: {len(warnings)}")
        for w in warnings:
            print(f"  {w}")

    if not errors and not warnings:
        print("\n✅ No issues found")

    print()
    print(f"Total: {len(errors)} error(s) / {len(warnings)} warning(s)")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
