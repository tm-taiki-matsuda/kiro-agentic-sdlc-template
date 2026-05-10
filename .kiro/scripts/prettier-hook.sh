#!/bin/bash
EVENT=$(cat)
FILE=$(echo "$EVENT" | python3 -c "
import sys,json
e=json.load(sys.stdin)
ti=e.get('tool_input',{})
p=ti.get('path','')
if not p:
  ops=ti.get('operations',[])
  if ops: p=ops[0].get('path','')
print(p)
" 2>/dev/null)
SUCCESS=$(echo "$EVENT" | python3 -c "import sys,json; e=json.load(sys.stdin); print(e.get('tool_response',{}).get('success',True))" 2>/dev/null)
if [[ "$SUCCESS" == "False" ]]; then exit 0; fi
if [[ "$FILE" == *.ts || "$FILE" == *.tsx ]]; then
  if [[ "$FILE" == frontend/* ]]; then
    cd frontend && npx prettier --write "${FILE#frontend/}" 2>/dev/null || true
  elif [[ "$FILE" == backend/* ]]; then
    cd backend && npx prettier --write "${FILE#backend/}" 2>/dev/null || true
  elif [[ "$FILE" == functions/* ]]; then
    cd functions && npx prettier --write "${FILE#functions/}" 2>/dev/null || true
  elif [[ "$FILE" == shared/* ]]; then
    cd shared && npx prettier --write "${FILE#shared/}" 2>/dev/null || true
  fi
fi
