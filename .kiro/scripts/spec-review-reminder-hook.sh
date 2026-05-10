#!/bin/bash
# postToolUse: display EARS notation checklist reminder when requirements.md is updated
EVENT=$(cat)
FILE=$(echo "$EVENT" | python3 -c "import sys,json; e=json.load(sys.stdin); print(e.get('tool_input',{}).get('path',''))" 2>/dev/null)
if [[ "$FILE" == *requirements.md ]]; then
  echo 'requirements.md updated: verify EARS notation (WHEN/THEN/IF/SHALL), testable granularity, error messages, 409 conflict, permission control, and boundary values'
fi
