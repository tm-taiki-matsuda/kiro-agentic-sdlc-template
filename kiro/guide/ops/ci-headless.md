# Kiro CLI Headless Mode — CI/CD Integration Guide

With Kiro CLI 2.0+, agents can be run headlessly on CI/CD pipelines using the `--no-interactive` flag and `KIRO_API_KEY` environment variable.

---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| Kiro CLI | v2.0+ (check with `kiro-cli --version`) |
| KIRO_API_KEY | API key obtained from your AWS account |
| DATABASE_URL | PostgreSQL connection string equivalent to local |
| Node.js | v18+ |

---

## Basic Headless Execution

```bash
# Set environment variables and run headlessly
export KIRO_API_KEY="your-api-key"
export DATABASE_URL="postgresql://..."

# Launch agent in non-interactive mode
kiro-cli chat --agent code-review --no-interactive --prompt "Review the code in git diff main...HEAD"
```

With `--no-interactive`:
- Interactive prompts are not displayed
- Confirmation dialogs are auto-skipped (depending on agent configuration)
- Automatically exits after processing completes

---

## CI/CD Pipeline Configuration Examples

### Pattern 1: Automatic PR Code Review

```yaml
# azure-pipelines-kiro-review.yml
trigger: none
pr:
  branches:
    include:
      - main
      - develop

pool:
  vmImage: ubuntu-latest

variables:
  - group: kiro-secrets  # variable group storing KIRO_API_KEY, DATABASE_URL

steps:
  - checkout: self
    fetchDepth: 0  # full history needed for git diff

  - task: NodeTool@0
    inputs:
      versionSpec: '20.x'

  - script: |
      npm install -g kiro-cli
      kiro-cli --version
    displayName: 'Install Kiro CLI'

  - script: |
      # Create symbolic link
      # Create symbolic link if .kiro is managed separately
      # ln -sf /path/to/kiro-config/.kiro .kiro

      # Run code review on PR changes
      kiro-cli chat --agent code-review \
        --no-interactive \
        --prompt "Review the changes in the $(System.PullRequest.SourceBranch) branch. Check git diff origin/$(System.PullRequest.TargetBranch)...HEAD and report any ADR violations, security issues, or missing tests." \
        --output review-result.md
    displayName: 'Kiro Code Review'
    env:
      KIRO_API_KEY: $(KIRO_API_KEY)
      DATABASE_URL: $(DATABASE_URL)

  - script: |
      # Post review result as PR comment
      if [ -f review-result.md ]; then
        echo "## 🤖 Kiro Code Review" > comment.md
        cat review-result.md >> comment.md
        # Post comment via Azure DevOps REST API
        curl -s -u ":$(System.AccessToken)" \
          -H "Content-Type: application/json" \
          -X POST \
          "$(System.TeamFoundationCollectionUri)$(System.TeamProject)/_apis/git/repositories/$(Build.Repository.ID)/pullRequests/$(System.PullRequest.PullRequestId)/threads?api-version=7.1" \
          -d "{\"comments\": [{\"content\": \"$(cat comment.md | jq -Rs .)\", \"commentType\": 1}], \"status\": 1}"
      fi
    displayName: 'Post Review Result as PR Comment'
    condition: always()
    env:
      SYSTEM_ACCESSTOKEN: $(System.AccessToken)
```

### Pattern 2: Automatic Bug Analysis on Test Failure

```yaml
# Add to existing pipeline as additional step

# Add after test step
- script: |
    # Only run when tests fail
    if [ "$(Agent.JobStatus)" == "Failed" ]; then
      # Create symbolic link if .kiro is managed separately
      # ln -sf /path/to/kiro-config/.kiro .kiro

      kiro-cli chat --agent bug-fix \
        --no-interactive \
        --prompt "Tests failed in CI. Check the failing test logs, identify the root cause, and suggest a fix. Do not modify code (analysis only)." \
        --output bugfix-analysis.md

      echo "## 🔍 Kiro Bug Analysis Results"
      cat bugfix-analysis.md
    fi
  displayName: 'Automatic Bug Analysis on Test Failure'
  condition: failed()
  env:
    KIRO_API_KEY: $(KIRO_API_KEY)
```

---

## Setting Up Variable Groups

```bash
# Create variable group with Azure CLI (first time only)
az pipelines variable-group create \
  --name "kiro-secrets" \
  --variables \
    KIRO_API_KEY="your-api-key" \
    DATABASE_URL="postgresql://user:pass@host:5432/db" \
  --authorize true
```

**Important**: Store `KIRO_API_KEY` as a secret variable (click the "Lock" icon in Azure DevOps).

---

## Headless Mode Options

| Option | Description |
|--------|-------------|
| `--no-interactive` | Disable interactive prompts |
| `--agent <name>` | Specify agent to use |
| `--prompt <text>` | Specify initial prompt |
| `--output <file>` | Save output to file |
| `--timeout <seconds>` | Timeout in seconds (default: 300) |
| `--model <model-id>` | Override model |

---

## Verify Headless Mode Locally

```bash
# Test headless mode locally
export KIRO_API_KEY="your-api-key"

kiro-cli chat --agent code-review \
  --no-interactive \
  --prompt "Review the latest commit" \
  --timeout 120
```

---

## Recommended Scenarios and Notes

### Recommended Scenarios
- **PR auto-review** — Early detection of ADR violations and security issues
- **Test failure analysis** — Automatic root cause identification on CI failure
- **Code generation quality check** — Validate specs generated by spec-writer

### Not Recommended for CI (cannot be used on CI)
- **backend-feature / frontend-feature** — Agents that modify code are dangerous to run autonomously on CI
- **db-migration** — Database changes always require manual developer confirmation
- **e2e-test** — Requires browser environment (separate Playwright CI setup needed)

### Security Notes
- Store `KIRO_API_KEY` as a secret variable in the variable group, do not output to logs
- Manage `DATABASE_URL` similarly as a secret variable
- Restrict write paths with `toolsSettings.fs_write.allowedPaths` (code-review has no fs_write tool, so no writes possible)

---

## Troubleshooting

### `KIRO_API_KEY not found` error
→ Verify the variable group is linked to the correct pipeline. Check that `variables: - group: kiro-secrets` is in the pipeline YAML.

### Agent times out
→ Extend with the `--timeout` option. Code review typically takes 60–120 seconds.

### `.kiro/` not found error
→ Create a symbolic link if `.kiro/` is managed separately from the project root.
