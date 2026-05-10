#!/bin/bash
# preToolUse: block fs_write to schema.prisma
# Use in agents other than db-migration
EVENT=$(cat)
FILE=$(echo "$EVENT" | python3 -c "import sys,json; e=json.load(sys.stdin); print(e.get('tool_input',{}).get('path',''))" 2>/dev/null)
if [[ "$FILE" == *schema.prisma ]]; then
  echo "BLOCKED: schema.prisma changes must be made with the db-migration agent" >&2
  exit 2
fi
exit 0
