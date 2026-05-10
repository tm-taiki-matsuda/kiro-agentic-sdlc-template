# kiro-framework

A framework for AI-driven development with kiro-cli.
Designed for monorepo projects using Next.js + Fastify + Prisma + TypeScript.

---

## Overview

This framework is a generalized template of kiro-cli configuration (agents, skills, prompts, hooks, and workflows).
Copy it to a new project and immediately start AI-driven Spec-Driven Development.

### Target Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 15 App Router + shadcn/ui + TailwindCSS |
| Backend | Fastify 5.x + TypeScript + Awilix DI |
| Database | PostgreSQL + Prisma |
| Functions | Serverless Functions (e.g., Azure Functions v4) |
| Infrastructure | Terraform (cloud-agnostic) |
| Shared | TypeScript package |

---

## Directory Structure

```
kiro-framework/
├── .kiro/                    kiro-cli configuration
│   ├── agents/               agent definitions (13 agents)
│   ├── prompts/              agent prompts (13 files)
│   ├── skills/               skills (18 files)
│   ├── settings/             global settings
│   │   ├── cli.json          model, feature flags, compaction settings
│   │   └── mcp.json.example  global MCP sample
│   ├── scripts/              hook scripts (11 files)
│   ├── specs/                work-in-progress specs (working directory)
│   │   └── _template/        spec templates
│   └── shared-agent-config.json  common denied paths for all agents
│
├── kiro/                     documentation
│   ├── guide/                developer guides
│   │   ├── README.md         guide reading order
│   │   ├── getting-started.md  overview and development flow
│   │   ├── onboarding.md     setup procedure
│   │   ├── agent-usage.md    how to use all agents
│   │   ├── how-it-works.md   internal structure explanation
│   │   ├── prompting-guide.md  how to give effective instructions
│   │   ├── faq.md            frequently asked questions
│   │   ├── pitfalls.md       common failure patterns
│   │   ├── troubleshooting.md  troubleshooting guide
│   │   ├── development-procedures.md  standard development procedures
│   │   ├── architecture-decisions.md  design philosophy
│   │   ├── architecture-diagram.md    architecture diagrams
│   │   ├── glossary.md       glossary
│   │   ├── todo-guide.md     task management operation rules
│   │   ├── lessons-guide.md  lessons recording operation rules
│   │   ├── quick-tutorial.md  hands-on: code-review
│   │   ├── quick-tutorial-implementation.md  hands-on: spec-writer
│   │   ├── quick-tutorial-fullcycle.md  hands-on: full cycle
│   │   └── ops/              operations and maintenance docs
│   └── workflows/            workflow diagrams (Mermaid) 19 files
│
└── tasks/                    task management (placed at project root)
    ├── todo.md               session-level task management
    └── lessons.md            lessons and improvement pattern records
```

---

## Agent List (13 Agents)

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

## Quick Start

### 1. Install kiro-cli

```bash
wget https://desktop-release.q.us-east-1.amazonaws.com/latest/kiro-cli.deb
sudo dpkg -i kiro-cli.deb
sudo apt-get install -f -y
kiro-cli --version
```

### 2. Apply framework to your project

```bash
# Copy .kiro/ to project root
cp -r kiro-framework/.kiro /path/to/your-project/
cp -r kiro-framework/kiro /path/to/your-project/
cp -r kiro-framework/tasks /path/to/your-project/
```

### 3. Configure project-specific information

```bash
cd /path/to/your-project

# Required: fill in product context
vi .kiro/skills/product-context/SKILL.md

# If needed: adjust tech stack and code structure
vi .kiro/skills/tech-stack/SKILL.md
vi .kiro/skills/code-structure/SKILL.md
```

### 4. Set environment variables

```bash
export DESIGN_DIR=/path/to/your-project/design
export DATABASE_URL=postgresql://user:password@localhost:5432/your_db
```

### 5. Verify

```bash
kiro-cli chat --agent spec-writer
```

---

## Key Design Principles

### Specialization
13 agents are separated by layer. The AI responsible for Backend physically cannot write to Frontend files.

### Physical Constraints
Write scope restrictions via `allowedPaths` cannot be bypassed by AI judgment.

### TDD Required
All agents are designed to follow "test first → implementation" order.

### Approval Gates
Human approval is required before important operations such as implementation plans, schema changes, and infrastructure apply.

---

## Customization

See [kiro/guide/ops/customization-guide.md](./kiro/guide/ops/customization-guide.md) for how to add project-specific configuration.

---

## Documentation

See [kiro/guide/README.md](./kiro/guide/README.md) for detailed documentation.

---

## Version

Compatible with kiro-cli 2.1.1

## License

MIT License — see [LICENSE](./LICENSE) for details.
