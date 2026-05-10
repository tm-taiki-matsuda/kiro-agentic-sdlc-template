# kiro-cli Common Pitfalls

> Common mistakes new team members make in their first 1–2 weeks, and how to avoid them.
> Last updated: 2026-05-10 | kiro-cli 2.1.1

---

## 1. Using `/agent` to Switch Agents

**Symptom**: Switched from backend-feature to frontend-feature, but todo.md and lessons.md are not loaded.

**Cause**: Switching with the `/agent` command during a chat does not fire the `agentSpawn` hook (kiro-cli behavior).

**Fix**:
```bash
# ❌ Switch during chat
/agent frontend-feature

# ✅ Quit and launch as a new session
/quit
kiro-cli chat --agent frontend-feature
```

---

## 2. Asking for Implementation Without a Spec

**Symptom**: Agent implements based on guesses, generating code that doesn't match intent.

**Fix**:
```
❌ "Create a user management API"

✅ First create a spec with spec-writer, then:
   "Please implement based on the spec in .kiro/specs/user-management/.
    Read requirements.md and design.md first, then present the implementation plan."
```

---

## 3. Asking the Wrong Agent for Cross-Layer Changes

**Symptom**: Asking `backend-feature` to "fix the Frontend too," but it's blocked by `allowedPaths`.

**Fix**:
- Cross-layer fixes → use `bug-fix` agent (can write to all layers)
- Full-stack new feature development → launch `backend-feature` → `frontend-feature` in separate sessions

---

## 4. Forgetting `npm run db:generate` After DB Schema Change

**Symptom**: Changed `database/prisma/schema.prisma` but getting type errors in backend or functions.

**Cause**: `backend/prisma/schema.prisma` and `functions/prisma/schema.prisma` are generated files (ADR-002).

**Fix**:
```bash
# After schema change with db-migration agent, always run:
cd backend && npm run db:generate
cd functions && npm run db:generate
```

---

## 5. Rubber-Stamping Approval Points

**Symptom**: Didn't notice problems in the agent's implementation plan, leading to large rework later.

**Fix**: At approval points, always check at minimum:

| Check Item | What to Look For |
|-----------|-----------------|
| Changed file list | Are there any unexpected files? |
| Test plan | Does it include 409 conflict and logical delete tests? |
| Schema change presence | Is the "no change" judgment correct? |

---

## 6. Sessions Getting Too Long

**Symptom**: Response quality degrades after 30–50 turns.

**Fix**:
- 1 session = 1 layer (separate Backend / Frontend / E2E)
- Use `/compact` to summarize the conversation
- If still not improving, use `/quit` → new session with `handoff-*.md` for continuity

---

## 7. Trying to Change schema.prisma with an Agent Other Than db-migration

**Symptom**: `guard-schema-hook.sh` blocks the write and displays "BLOCKED: schema.prisma changes must be made with the db-migration agent."

**Fix**: Always use the `db-migration` agent for schema changes.

---

## 8. Agent Repeating the Same Mistakes

**Symptom**: The same ADR violations or pattern deviations occur repeatedly.

**Fix**:
1. Explicitly mention the skill name in the prompt to force rule reference:
   ```
   Please check the adr-quick-reference skill before implementing
   ```
2. Use `/compact` to reorganize context
3. If still not improving, use `/quit` → launch a new session

---

## 9. Knowledge Base Empty, Can't Search Design Documents

**Symptom**: `spec-writer` or `code-review` can't find design documents.

**Cause**: Knowledge bases are isolated per agent. Initial setup is required.

**Fix**: Run manually in each agent:
```
/knowledge add design ./design
```

Or run `setup-knowledge.sh`:
```bash
bash .kiro/scripts/setup-knowledge.sh
```

---

## 10. Asking "Skip Tests for Now, Just Implement First"

**Symptom**: Agent breaks TDD order, generating code with insufficient test coverage.

**Fix**: TDD is a required rule in this framework.

```
❌ "Skip tests for now, just implement first"
✅ "Please proceed with TDD" (this is all you need)
```

---

## References

- How to give effective instructions → [prompting-guide.md](./prompting-guide.md)
- Technical issues → [troubleshooting.md](./troubleshooting.md)
- How to use agents → [agent-usage.md](./agent-usage.md)
