#!/bin/bash
# Display db:generate reminder when schema.prisma is changed
EVENT=$(cat)
FILE=$(echo "$EVENT" | python3 -c "import sys,json; e=json.load(sys.stdin); print(e.get('tool_input',{}).get('path',''))" 2>/dev/null)
if [[ "$FILE" == *schema.prisma ]]; then
  echo '⚠️ schema.prisma changed (ADR-002). Run: cd database && npm run db:generate'
fi
