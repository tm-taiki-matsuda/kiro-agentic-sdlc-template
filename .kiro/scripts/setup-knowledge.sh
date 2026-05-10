#!/bin/bash
# Knowledge base initial setup script
# Target agents: spec-writer, code-review, bug-fix, design-updater, system-guide
#
# Usage:
#   cd <project-root>
#   bash .kiro/scripts/setup-knowledge.sh

set -euo pipefail

DESIGN_DIR="${DESIGN_DIR:-$(cd "$(dirname "$0")/../.." && pwd)/design}"
AGENTS=("spec-writer" "code-review" "bug-fix" "design-updater" "system-guide")

if [ ! -d "$DESIGN_DIR" ]; then
  echo "❌ design/ directory not found: $DESIGN_DIR"
  exit 1
fi

echo "=== Knowledge Base Initial Setup ==="
echo "Target agents: ${AGENTS[*]}"
echo "Index source: $DESIGN_DIR"
echo ""

for agent in "${AGENTS[@]}"; do
  echo "--- $agent ---"
  kiro-cli chat --agent "$agent" --no-interactive --trust-all-tools "/knowledge add design $DESIGN_DIR" 2>&1 | tail -5
  echo "✅ $agent done"
  echo ""
done

echo "=== All agents setup complete ==="
echo "Verify: run /knowledge show in each agent to confirm the index"
