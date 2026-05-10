# kiro-cli Getting Started Guide

> An overview of development with kiro-cli.
> For setup instructions, see [onboarding.md](./onboarding.md).
> For terminology, see [glossary.md](./glossary.md).
> Last updated: 2026-05-10 | kiro-cli 2.1.1

---

## 1. What is kiro-cli?

An AI development tool that runs in the terminal. Instead of writing code themselves, developers delegate tasks to specialized AI agents.

While traditional AI assistance tools (like GitHub Copilot) "assist developers as they write code," kiro-cli inverts this: "AI agents write the code, and developers focus on planning, approving, and reviewing."

| | Traditional AI Assistance | kiro-cli |
|---|---|---|
| Who writes code | **Developer** (AI assists) | **AI agent** (developer directs) |
| Unit of work | Lines, functions, files | Features, tasks |
| AI's knowledge scope | Primarily open files | Entire project including design docs, ADRs, past lessons |
| Quality assurance | Depends on developer skill | Rules and constraints configurable per project |

### Is it safe to have AI write code?

kiro-cli itself is a general-purpose AI development tool — TDD and ADR checks are not built in. However, the agent definition, skills, and hooks mechanism allows you to configure safety mechanisms per project. This framework configures them as follows:

| Safety Mechanism | How It Works | Configuration |
|-----------------|-------------|---------------|
| Physical write scope restriction | Backend AI cannot write to Frontend files | `allowedPaths` in agent JSON |
| TDD enforcement | Tests must be written before implementation | Agent prompts + `dev-workflow` skill |
| ADR auto-check | AI automatically detects violations of project technical rules | `adr-quick-reference` skill + `code-review` agent |
| Approval gates | Human approval required before important operations (implementation plans, schema changes, infra apply) | Agent prompts + `allowedTools` settings |
| Dangerous command blocking | `rm -rf`, `git push --force`, `DROP TABLE`, etc. are automatically blocked by hooks | `preToolUse` hook (`security-hook.sh`) |

---

## 2. How Does the Development Flow Change?

### Before (Traditional)

```
Gather requirements → Read design docs → Write code → Write tests → Get reviewed
```

### After (kiro-cli)

```
Gather requirements → Write spec → Delegate to agent → Approve plan → Verify test results → Run review
```

What developers do:

| Developer's Work | Specifically |
|---|---|
| Write specs | Define what to build and how (`spec-writer` agent assists) |
| Approve plans | Review implementation plans and change file lists presented by agents |
| Judge test results | Not just green/red, but assess test validity |
| Review code | Review `code-review` agent findings and make final decisions |

What developers no longer do:

- Manually writing Zod schemas, Repositories, Services, Routes
- Running Prettier manually (automated by hooks)
- Visually checking for ADR violations (`code-review` agent auto-detects)

---

## 3. Agent List

| Agent | Role | Shortcut |
|---|---|---|
| `spec-writer` | Gather requirements and generate spec files | Ctrl+Shift+W |
| `backend-feature` | Implement Backend API with TDD | Ctrl+Shift+B |
| `frontend-feature` | Implement Frontend screens with TDD | Ctrl+Shift+F |
| `functions-feature` | Implement Serverless Functions with TDD | Ctrl+Shift+G |
| `e2e-test` | Generate and run TypeScript Keyword-Driven E2E tests | Ctrl+Shift+E |
| `code-review` | Review ADR compliance, security, test coverage (read-only) | Ctrl+Shift+R |
| `db-migration` | Prisma schema changes and migration execution | Ctrl+Shift+D |
| `bug-fix` | Identify root cause and fix bugs with minimal changes | Ctrl+Shift+X |
| `shared-package` | Add type definitions and constants to shared package | Ctrl+Shift+S |
| `infrastructure` | Manage cloud resources with Terraform | Ctrl+Shift+I |
| `design-updater` | Update design/ documents based on requirements or implementation drift | Ctrl+Shift+U |
| `system-guide` | Answer questions about specs, design, and implementation (with drift detection, read-only) | Ctrl+Shift+H |
| `client-doc` | Generate client-facing documentation in HTML | Ctrl+Shift+C |

---

## 4. Daily Usage

### Launch

```bash
kiro-cli chat --agent {agent-name}
# Examples:
kiro-cli chat --agent spec-writer
kiro-cli chat --agent backend-feature
```

### Typical Development Flow

```bash
# 1. Create spec
kiro-cli chat --agent spec-writer
# → .kiro/specs/{feature-name}/ is generated

# 2. Backend implementation
kiro-cli chat --agent backend-feature
# → "Please implement based on the spec in .kiro/specs/{feature-name}/"

# 3. Frontend implementation
kiro-cli chat --agent frontend-feature

# 4. E2E tests
kiro-cli chat --agent e2e-test

# 5. Code review
kiro-cli chat --agent code-review
```

### Session Management

- 1 session = 1 layer (Backend / Frontend / E2E) is a good guideline
- Use `/compact` to summarize the conversation when it gets long
- To switch phases, use `/quit` → launch a new session (the `/agent` command is not recommended)

---

## 5. Detailed Documentation

- Setup instructions → [onboarding.md](./onboarding.md)
- Internal structure details → [how-it-works.md](./how-it-works.md)
- How to use each agent → [agent-usage.md](./agent-usage.md)
- How to give effective instructions → [prompting-guide.md](./prompting-guide.md)
- Common failures → [pitfalls.md](./pitfalls.md)
