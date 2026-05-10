#!/bin/bash
# agentSpawn: auto-load task state, lessons, and handoffs at session start
echo '=== Session Start ==='
echo '--- Incomplete Tasks ---'
grep -n '\[ \]' tasks/todo.md 2>/dev/null | head -10
echo '---'
cat tasks/lessons.md 2>/dev/null | head -20
for f in tasks/handoff-*.md; do
  [ -f "$f" ] && echo "📌 Handoff: $f" && head -10 "$f"
done
echo '---'
echo '📋 Please record today'"'"'s tasks in tasks/todo.md (extract from specs/tasks.md if available)'
