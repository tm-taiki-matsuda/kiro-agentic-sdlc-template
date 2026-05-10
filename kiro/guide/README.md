# kiro-cli Documentation Guide

> This directory contains human-facing documentation for development with kiro-cli.
> Reading order varies by role. Follow the guide below.

---

## For PMs & Managers

| Order | Document | Time | Content |
|:----:|----------|:----:|---------|
| 1 | [getting-started.md](./getting-started.md) | 15 min | kiro-cli overview, how development flow changes, safety mechanisms |
| 2 | [glossary.md](./glossary.md) | 10 min | Terminology: "agent", "spec", "ADR", etc. |

---

## For Engineers New to AI Development Tools

| Order | Document | Time | Content |
|:----:|----------|:----:|---------|
| 1 | [glossary.md](./glossary.md) → AI basics section | 5 min | LLM, prompt, hallucination, and other basic concepts |
| 2 | [getting-started.md](./getting-started.md) | 15 min | Overview, safety mechanisms, daily usage |
| 3 | [onboarding.md](./onboarding.md) | 20 min | Installation and setup (hands-on) |
| 4 | [quick-tutorial.md](./quick-tutorial.md) | 15 min | Hands-on: code review with code-review agent |
| 5 | [quick-tutorial-implementation.md](./quick-tutorial-implementation.md) | 15 min | Hands-on: spec creation with spec-writer |
| 6 | [quick-tutorial-fullcycle.md](./quick-tutorial-fullcycle.md) | 20 min | Hands-on: full cycle from spec → implementation → review |
| 7 | [prompting-guide.md](./prompting-guide.md) | 10 min | How to give effective instructions to AI agents |
| 8 | [development-procedures.md](./development-procedures.md) | 20 min | Standard development procedures |
| 9 | [agent-usage.md](./agent-usage.md) | — | Reference: how to use all 13 agents with prompt examples |

> Once comfortable:
> - [faq.md](./faq.md) — Frequently asked questions
> - [pitfalls.md](./pitfalls.md) — Common failure patterns and how to avoid them
> - [troubleshooting.md](./troubleshooting.md) — Reference when stuck
> - [todo-guide.md](./todo-guide.md) / [lessons-guide.md](./lessons-guide.md) — Task management and lessons recording rules

---

## For Engineers Experienced with AI Development Tools (Claude Code / Copilot / Cursor, etc.)

| Order | Document | Time | Content |
|:----:|----------|:----:|---------|
| 1 | [getting-started.md](./getting-started.md) | 10 min | Understand differences from other tools |
| 2 | [architecture-decisions.md](./architecture-decisions.md) | 10 min | Design philosophy: why 13 separate agents |
| 3 | [how-it-works.md](./how-it-works.md) | 15 min | Internals: JSON structure, 3 resource types, 5 hook triggers |
| 4 | [onboarding.md](./onboarding.md) | 10 min | Setup |
| 5 | [agent-usage.md](./agent-usage.md) | — | Agent list and skill assignment table |
| 6 | [ops/review-summary.md](./ops/review-summary.md) | 15 min | Past review discussions and configuration maturity |

> To customize the configuration:
> - [ops/customization-guide.md](./ops/customization-guide.md) — How to add agents/skills/hooks

---

## For Operations & Maintenance

| Document | Content |
|----------|---------|
| [ops/version-upgrade.md](./ops/version-upgrade.md) | kiro-cli version upgrade procedure |
| [ops/ci-headless.md](./ops/ci-headless.md) | CI/CD headless execution guide |
| [ops/review-summary.md](./ops/review-summary.md) | Pre-review input material for configuration reviews |
| [ops/migration-log.md](./ops/migration-log.md) | Migration history |
| [ops/customization-guide.md](./ops/customization-guide.md) | How to add agents/skills/hooks |

---

## Full Document List

### Introduction & Reference

| File | Content |
|------|---------|
| [getting-started.md](./getting-started.md) | kiro-cli overview and how development flow changes |
| [glossary.md](./glossary.md) | Glossary |
| [onboarding.md](./onboarding.md) | Installation and setup procedure |
| [quick-tutorial.md](./quick-tutorial.md) | Hands-on: code-review |
| [quick-tutorial-implementation.md](./quick-tutorial-implementation.md) | Hands-on: spec-writer |
| [quick-tutorial-fullcycle.md](./quick-tutorial-fullcycle.md) | Hands-on: full cycle experience |
| [prompting-guide.md](./prompting-guide.md) | How to give effective instructions to AI agents |
| [how-it-works.md](./how-it-works.md) | Internals (agents, skills, hooks, MCP) |
| [architecture-decisions.md](./architecture-decisions.md) | Design philosophy (why this configuration) |
| [architecture-diagram.md](./architecture-diagram.md) | Architecture diagrams (Mermaid) |

### Daily Development

| File | Content |
|------|---------|
| [agent-usage.md](./agent-usage.md) | How to use all 13 agents with prompt examples |
| [development-procedures.md](./development-procedures.md) | Standard development procedures |
| [faq.md](./faq.md) | Frequently asked questions |
| [pitfalls.md](./pitfalls.md) | Common failure patterns (for new team members) |
| [troubleshooting.md](./troubleshooting.md) | Common problems and solutions |
| [todo-guide.md](./todo-guide.md) | todo.md / handoff operation rules |
| [lessons-guide.md](./lessons-guide.md) | lessons.md operation and skill promotion flow |
| [../workflows/README.md](../workflows/README.md) | Workflow diagram list (Mermaid) |

### Operations & Maintenance (ops/)

| File | Content |
|------|---------|
| [ops/version-upgrade.md](./ops/version-upgrade.md) | Version upgrade procedure |
| [ops/ci-headless.md](./ops/ci-headless.md) | CI/CD headless execution |
| [ops/review-summary.md](./ops/review-summary.md) | Pre-review configuration material |
| [ops/migration-log.md](./ops/migration-log.md) | Migration history |
| [ops/customization-guide.md](./ops/customization-guide.md) | Configuration customization procedure |
