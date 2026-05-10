# kiro-cli Setup Guide

> Target version: kiro-cli 2.1.1 and later
> Last updated: 2026-05-10

## Prerequisites

| Tool | Version | Check Command | Purpose |
|------|---------|--------------|---------|
| Node.js | v18+ | `node --version` | MCP server execution |
| npm | v9+ | `npm --version` | Package management |
| Git | any | `git --version` | Repository management |

---

## 1. Install kiro-cli

### 1-1. Installation (first time)

#### Method A: deb package (recommended)

```bash
wget https://desktop-release.q.us-east-1.amazonaws.com/latest/kiro-cli.deb
sudo dpkg -i kiro-cli.deb
sudo apt-get install -f -y
```

#### Method B: Install from zip

```bash
curl --proto '=https' --tlsv1.2 -sSf \
  'https://desktop-release.q.us-east-1.amazonaws.com/latest/kirocli-x86_64-linux.zip' \
  -o kirocli.zip
unzip kirocli.zip
./kirocli/install.sh
```

### 1-2. Verify version

```bash
kiro-cli --version
# → Should display: kiro-cli 2.x.x
```

### 1-3. Update

```bash
wget -O kiro-cli.deb https://desktop-release.q.us-east-1.amazonaws.com/latest/kiro-cli.deb
sudo dpkg -i kiro-cli.deb
```

### 1-4. Authentication (first time only)

```bash
kiro-cli
# → Browser opens, prompts for authentication URL
```

---

## 2. Apply to Your Project

### 2-1. Copy the framework

Apply this framework to a new project:

```bash
# Copy .kiro/ to project root
cp -r kiro-framework/.kiro /path/to/your-project/
cp -r kiro-framework/kiro /path/to/your-project/
cp -r kiro-framework/tasks /path/to/your-project/

# Or manage with symbolic links
ln -s /path/to/kiro-framework/.kiro /path/to/your-project/.kiro
```

### 2-2. Configure project-specific information

Edit the following files to match your project:

```bash
# 1. Product context (required)
vi .kiro/skills/product-context/SKILL.md
# → Fill in system overview, key users, business rules, environment list
# → Review the "Assumed Project Structure" section and adjust if needed

# 2. Code structure (required if your directory layout differs)
vi .kiro/skills/code-structure/SKILL.md
# → This is the single source of truth for file paths used by all agents
# → Adjust directory structure, naming conventions, and import rules

# 3. Tech stack (if needed)
vi .kiro/skills/tech-stack/SKILL.md
# → Update project name, environment variables, and local dev commands
# → Replace cloud-provider-specific env vars with your actual service names
```

### 2-3. Create design document directory (if applicable)

Several agents (`spec-writer`, `system-guide`, `design-updater`, `client-doc`) reference
a `design/` directory for design documents. Create it if your project uses design docs:

```bash
mkdir -p design/screen design/api design/database
```

If you don't use a `design/` directory, you can either:
- Leave it empty (agents will simply find no results when searching)
- Remove the `knowledgeBase` resource entries from the relevant agent JSON files

### 2-4. Set environment variables

```bash
# Design document directory path (used by design-updater, spec-writer, system-guide)
export DESIGN_DIR=/path/to/your-project/design

# Database connection (used by db-migration, backend-feature, functions-feature)
# Adjust the connection string format for your database
export DATABASE_URL=postgresql://user:password@localhost:5432/your_db
```

### 2-5. Initialize task files

```bash
mkdir -p tasks
cat > tasks/todo.md << 'EOF'
# Task Management

## Active Tasks

(none)

## Completed Tasks

EOF

cat > tasks/lessons.md << 'EOF'
# Lessons Learned

## Record Format

### [YYYY-MM-DD] Category: Title

**Pattern**: What happened
**Cause**: Why it happened
**Action**: What to do next time
**Apply when**: What kind of work should reference this

---

EOF
```

---

## 3. Verify Setup

```bash
cd /path/to/your-project

# Check agent list
kiro-cli agent list

# Try launching spec-writer
kiro-cli chat --agent spec-writer
```

---

## 4. Initial Knowledge Base Setup

If you have a design document directory, initialize the knowledge base:

```bash
bash .kiro/scripts/setup-knowledge.sh
```

Or run manually in each agent:

```
/knowledge add design ./design
```

---

## 5. Next Steps

- Understand the overview → [getting-started.md](./getting-started.md)
- Understand the internals → [how-it-works.md](./how-it-works.md)
- How to use each agent → [agent-usage.md](./agent-usage.md)
- How to give effective instructions → [prompting-guide.md](./prompting-guide.md)
