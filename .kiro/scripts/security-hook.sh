#!/bin/bash
# preToolUse: block dangerous commands
INPUT=$(cat)
CMD=$(echo "$INPUT" | python3 -c "import sys,json; e=json.load(sys.stdin); print(e.get('tool_input',{}).get('command',''))" 2>/dev/null)
if [ -z "$CMD" ]; then
  CMD=$(echo "$INPUT" | jq -r '.tool_input.command // ""' 2>/dev/null || echo "")
fi
if echo "$CMD" | grep -qE 'git push --force|git commit --no-verify|rm -rf|DROP TABLE|TRUNCATE|terraform destroy'; then
  echo 'BLOCKED: dangerous command detected' >&2; exit 2
fi
exit 0
