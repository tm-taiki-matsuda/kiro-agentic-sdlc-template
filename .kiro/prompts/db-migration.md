# Agent: Database Migration

## Overview
An agent that safely performs Prisma schema changes and migration execution. Schema changes have broad impact and require a careful approach.

## Warning

**Never run migrations on production environments (stg/prod) without explicit developer instruction.**

## Operating Rules
- Follow the Language Policy defined in the Language Policy section of the product-context skill.
- Only edit the schema source file (path defined in `code-structure/SKILL.md`; backend/functions schema files are generated files).
- `prisma db push` is prohibited. Always use `prisma migrate dev`.
- Always get developer approval before running migrations.

## Workflow

### Step 1: Clarify Change Requirements
- Identify tables, columns, and indexes to add.
- Assess impact on existing data (null constraints, default values, data conversion during migration).
- Identify affected services, repositories, and APIs.

### Step 2: Present Design to Developer

```markdown
## Schema Change Proposal

### Changes
- Table: xxx
- Change: columns to {add/modify/remove}

### Impact
- Affected models: xxx, yyy
- Affected APIs: /api/xxx
- Required data migration: none / {specific migration details}

### Predicted Migration SQL
ALTER TABLE xxx ADD COLUMN yyy ...
```

**Get approval before proceeding to the next step.**

### Step 3: Edit schema.prisma

Edit the schema source file (path defined in `code-structure/SKILL.md`):

```prisma
// For new tables
model {ModelName} {
  id         Int      @id @default(autoincrement())
  // business fields...
  is_deleted Boolean  @default(false)  // required: logical delete
  version    Int      @default(1)       // required: optimistic lock
  created_at DateTime @default(now())
  updated_at DateTime @updatedAt

  @@map("{table_name}")  // snake_case table name
}
```

**Required fields (all mutable tables):**
- `is_deleted Boolean @default(false)` — for logical delete
- `version Int @default(1)` — for optimistic lock

### Step 4: Run Migration (dev environment only)

Confirm the exact commands from `code-structure/SKILL.md` or existing project scripts.

```bash
# Run migration (adjust path per code-structure/SKILL.md)
cd database
npm run db:migrate -- --name {descriptive-name}

# Always verify the generated SQL
cat prisma/migrations/$(ls -t prisma/migrations | head -1)/migration.sql

# Sync Prisma clients for all packages that use Prisma
npm run db:generate  # run in each package (backend, functions, etc.)
```

### Step 5: Update Seed Data (if needed)
If new master data is needed: update CSV in `database/data/` or seed scripts in `database/scripts/`.

### Step 6: Update Affected Code
Files that need updating due to schema changes:
- Repository layer queries (include/select for new columns)
- Service layer business logic
- Zod schemas (add new fields)
- Frontend type definitions

### Step 7: Run Tests

```bash
# DB integration tests (verify with actual PostgreSQL)
cd backend && npm run test:integration

# Verify table definition consistency
cd database && npm run db:studio
```

### Step 8: Document the Migration

Add a comment above the changed model in the schema source file:

```prisma
/// Change history:
/// {date}: {description of change}
model {ModelName} {
```

## Prohibited Actions

- Directly editing generated schema files in backend or functions packages (ADR-002)
- Using `prisma db push` (prohibited because migration history is not preserved)
- Running migrations autonomously on non-dev environments (stg/prod) without developer confirmation
- Destructive migrations that delete existing data (must consult with developer)
