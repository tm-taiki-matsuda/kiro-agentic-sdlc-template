---
name: "Security Constraints"
description: "Authentication, authorization, input validation, SQL injection prevention, secret management, audit logging, and network constraints. Referenced by all agents to prevent security violations."
---

# Security Constraints

> Security violations are treated as release blockers.
> Code violating the rules below will be flagged as 🔴 MUST by the `code-review` agent.

---

## Authentication & Authorization

> **The plugin names and structure below are examples from the default project setup.
> Update this section in `security-constraints/SKILL.md` to match your project's actual auth implementation.**

### Authentication Structure (example)

```
Registration order in app.ts:
  1. verifyJwtPlugin        — global preHandler (excludes paths that don't require auth)
  2. authPlugin             — provides fastify.authenticate decorator (used in Route onRequest)
  3. authorizerPlugin       — provides fastify.authorize() decorator (for fine-grained authz)
  4. permissionCheckPlugin  — global auto-authorization via path-based rule table
```

### Required Plugins (applied per Route)

```typescript
// ✅ Correct (required for all endpoints)
fastify.post('/api/items', {
  onRequest: [fastify.authenticate],   // JWT verification (required)
  // authorization is auto-applied by permission-check.ts plugin via path-based rules
}, handler)

// ✅ When fine-grained authorization is needed
fastify.post('/api/admin/special', {
  onRequest: [fastify.authenticate, fastify.authorize({ permissions: ['admin:special'] })],
}, handler)

// ❌ Prohibited: authentication without plugin
const token = request.headers.authorization?.split(' ')[1]
const decoded = jwt.decode(token)  // direct decode prohibited
```

### Rules

| Rule | Content |
|------|---------|
| `authenticate` required | Apply `onRequest: [fastify.authenticate]` to all API Routes (except health check) |
| Authorization auto-applied | `permission-check.ts` plugin auto-applies globally via path-based rule table |
| `authorize()` is optional | Add only when fine-grained authorization is needed |
| Manual if-role-check prohibited | Manual role checks inside Route handlers are prohibited |
| Direct JWT decode prohibited | Get from `request.user` instead |

---

## Input Validation

```typescript
// ✅ Correct
fastify.post('/api/items', {
  schema: { body: CreateItemSchema }  // Zod → fastify schema
}, handler)

// ❌ Prohibited: no validation
fastify.post('/api/items', handler)
```

- Apply Zod schema validation to all requests (body / querystring / params)
- Double validation with the same schema on the frontend as well

---

## SQL Injection Prevention

```typescript
// ✅ Correct (parameter binding)
const result = await prisma.$queryRaw`
  SELECT * FROM items WHERE id = ${id} AND is_deleted = false
`

// ❌ Prohibited: string concatenation
const result = await prisma.$queryRaw(
  `SELECT * FROM items WHERE id = ${id}`  // injectable
)
```

- When using `$queryRaw`, only tagged template literal form is allowed
- Dynamic table names and column name construction is prohibited (confirm with developer if needed)

---

## Secret Management

### Prohibited in Code

```typescript
// ❌ Prohibited: hardcoded in code
const apiKey = 'sk-1234567890abcdef'
const dbUrl = 'postgresql://user:pass@host/db'

// ❌ Prohibited: output secrets to console.log
console.log('database url:', process.env.DATABASE_URL)

// ✅ Correct: via environment variables (injected from secret management service in production)
const apiKey = process.env.API_KEY
```

### `.env` File Rules

| File | Purpose | Git tracked |
|------|---------|-------------|
| `.env.example` | Sample (dummy values) | ✅ OK to commit |
| `.env.local` | Local development | ❌ in `.gitignore` |
| `.env.ci` | CI environment (no secrets) | ✅ OK to commit |
| `*.secrets.tfvars` | Terraform secrets | ❌ in `.gitignore` |

---

## Audit Log (CUD Operations)

The `audit-log.ts` plugin automatically records POST/PATCH/DELETE 2xx responses in the `onSend` hook.
No manual output needed in route handlers.

---

## File Access

- File downloads: retrieve buffer from Blob Storage via Backend API → return binary directly (`reply.send(buffer)`)
- Selecting binary directly from DB and returning to client is prohibited
- File/object storage connection uses cloud-native auth in production, connection string locally

---

## Operations Requiring Approval (always confirm with developer before changing)

| Change Type | Reason |
|-------------|--------|
| Changes to `authenticate` / `authorize` plugins | Core of authentication/authorization |
| Changes to JWT verification logic | Risk of breaking token verification |
| Adding/removing access control role definitions | Risk of privilege escalation/revocation |
| Changes to secret management configuration | Risk of secret leakage |
| Changes to audit log plugin | Risk of losing traceability |
