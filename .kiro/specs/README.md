# Kiro Specs Directory

This directory manages **work-in-progress implementation specs** used in Kiro's Spec-Driven Development.

## Difference from `design/`

| `design/` | `.kiro/specs/` |
|-----------|----------------|
| Persistent design documents (finalized, reviewed) | Work-in-progress specs (per agent task unit) |
| Team-reviewed and approved | In progress, not finalized |
| Changes via separate ticket/PR | Updated by agents as work progresses |
| Source of truth | Copied from `design/` with supplementary details |

## Usage

### 1. When starting new feature development

The `spec-writer` agent automatically creates a subdirectory in Step 3 (spec file creation).
To create manually, copy `_template/`:

```bash
cp -r .kiro/specs/_template .kiro/specs/{feature-name}
# Example: cp -r .kiro/specs/_template .kiro/specs/user-management
```

### 2. During implementation

Agents update `tasks.md` from `[TODO]` → `[IN_PROGRESS]` → `[DONE]`.

### 3. After implementation complete

- Reflect important design decisions in the corresponding `design/` documents
  - Launch the `design-updater` agent when reflection is needed
  - Same applies when code-review flags "discrepancy with design documents"
- Deletion of `specs/{feature-name}/` directory is **decided by the developer** (agents do not delete autonomously)
  - Timing: after PR merge (specs may be referenced during review)
  - Can be kept if reused for future modifications
  - Deletion is preserved in git history

## Directory Structure

```
specs/
├── README.md              ← this file
├── _template/             ← template for new feature development
│   ├── requirements.md
│   ├── design.md
│   └── tasks.md
└── {feature-name}/        ← feature in progress (e.g., user-management)
    ├── requirements.md
    ├── design.md
    └── tasks.md
```
