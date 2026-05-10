#!/bin/bash
EVENT=$(cat)
CMD=$(echo "$EVENT" | python3 -c "import sys,json; e=json.load(sys.stdin); print(e.get('tool_input',{}).get('command',''))" 2>/dev/null)
if echo "$CMD" | grep -qE '(jest|playwright|npm.*test|test:unit|test:mock|test:integration|test:keyword|test:e2e)'; then
  echo 'Test execution detected: please summarize the results'
  touch /tmp/.kiro-test-ran-${PPID} 2>/dev/null || true
fi
