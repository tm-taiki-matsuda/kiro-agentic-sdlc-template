#!/bin/bash
# stop hook: remaining task count + changed file count warning + test not-run warning
REMAINING=$(grep -c '\[ \]' tasks/todo.md 2>/dev/null || echo 0)
echo "Remaining tasks: ${REMAINING}"

CHANGED=$(git diff --name-only 2>/dev/null | wc -l)
if [ "$CHANGED" -gt 20 ]; then
  echo "⚠️ Changed files: ${CHANGED} (too many — consider splitting commits)"
elif [ "$CHANGED" -gt 0 ]; then
  echo "Changed files: ${CHANGED}"
fi

# Warn if source files changed but tests not run
SRC_CHANGED=$(git diff --name-only 2>/dev/null | grep -E '\.(ts|tsx)$' | grep -v '\.test\.' | grep -v '\.spec\.' | wc -l)
if [ "$SRC_CHANGED" -gt 0 ]; then
  if [ -f /tmp/.kiro-test-ran-${PPID} ]; then
    rm -f /tmp/.kiro-test-ran-${PPID}
  else
    echo "⚠️ Source files changed. Did you forget to run tests?"
  fi
fi

# Prompt developer to review if new entries added to lessons.md
LESSONS_ADDED=$(git diff -- tasks/lessons.md 2>/dev/null | grep -c '^+###' || true)
if [ "$LESSONS_ADDED" -gt 0 ]; then
  echo "📝 ${LESSONS_ADDED} new entries added to lessons.md. Please review the content."
else
  echo "📝 Were there any patterns worth recording in lessons.md? (correction received, test failure, ADR violation, unexpected behavior)"
fi
