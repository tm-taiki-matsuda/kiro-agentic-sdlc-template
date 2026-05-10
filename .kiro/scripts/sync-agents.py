#!/usr/bin/env python3
"""
Syncs deniedPaths from shared-agent-config.json to fs_write.deniedPaths in all agent JSONs.
Skips code-review since it has no fs_write.

Usage: python3 .kiro/scripts/sync-agents.py
"""
import json, glob, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AGENTS_DIR = os.path.join(SCRIPT_DIR, "..", "agents")

shared = json.load(open(os.path.join(AGENTS_DIR, "..", "shared-agent-config.json")))
denied = shared["deniedPaths"]

for path in sorted(glob.glob(os.path.join(AGENTS_DIR, "*.json"))):
    name = os.path.basename(path)
    if name.startswith("_"):
        continue

    with open(path) as f:
        agent = json.load(f)

    ts = agent.get("toolsSettings", {})
    fw = ts.get("fs_write")
    if fw is None:
        continue

    if fw.get("deniedPaths") == denied:
        continue

    fw["deniedPaths"] = denied
    with open(path, "w") as f:
        json.dump(agent, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"✅ {name}: deniedPaths updated")

print("done")
