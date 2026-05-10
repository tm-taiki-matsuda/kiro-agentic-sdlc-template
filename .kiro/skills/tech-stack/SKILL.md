---
name: "Tech Stack & ADR"
description: "Monorepo structure, ADR-001 through ADR-008, test commands, environment variables, and local development environment. Referenced by all agents before implementation to prevent ADR violations."
---

# Tech Stack & ADR

## Monorepo Structure

```
{project-name}/
├── backend/       Fastify 5.x + TypeScript + Prisma + Awilix DI
├── frontend/      Next.js 15 App Router + shadcn/ui + TailwindCSS
├── database/      Prisma schema (source of truth) + migrations
├── shared/        shared package (type definitions, constants)
├── functions/     Serverless Functions (batch processing, async processing)
├── infrastructure/ Terraform (cloud resources)
└── design/        design documents (screen specs, API specs, DB specs)
```

## Architecture Decision Records (ADR)

### ADR-001: No Dynamic Routes
**Decision**: Next.js `[id]` dynamic routes are prohibited. Use `?id=123` query parameter pattern only.
**Reason**: Static hosting environments may not support dynamic routes.
**Correct**: `/items/detail?id=123` → `frontend/src/app/items/detail/page.tsx`
**Prohibited**: `frontend/src/app/items/[id]/page.tsx`

### ADR-002: Database Schema Ownership
**Decision**: `database/prisma/schema.prisma` is the single source of truth.
`backend/prisma/schema.prisma` and `functions/prisma/schema.prisma` are generated files (synced with `npm run db:generate`).
**Prohibited**: Directly editing schema.prisma in backend or functions.

### ADR-003: API Versioning and Response Format
**Decision**: All routes are registered with `/api` prefix.
**Standard response format**:
```typescript
interface ApiResponse<T> {
  contents: T[];
  totalCount: number;
  offset: number;
  limit: number;
}
```

### ADR-004: DI via Awilix
**Decision**: Services and repositories are injected via Awilix container. Direct Prisma calls from routes are prohibited.
**Scope**: Repository → TRANSIENT, Service → SCOPED (per request).
**Layers**: Routes → Services → Repositories → Prisma

### ADR-005: Logical Delete Only
**Decision**: `DELETE` SQL statements are prohibited. Update to `is_deleted = true` instead.
All mutable tables must have `is_deleted Boolean @default(false)`.

### ADR-006: Optimistic Lock Required
**Decision**: All mutable tables must have `version Int @default(1)`.
On update, verify version match → increment. Return HTTP 409 on mismatch.

### ADR-007: Date Retrieval
**Decision**: Direct use of `new Date()` is prohibited.
Backend: `import { getCurrentDate } from '../utils/date-utils.js'`
Frontend: `import { getCurrentDate } from '@/utils/dateUtils'`
**Reason**: To allow date control via `USE_MOCK_DATE` / `MOCK_DATE` environment variables.

### ADR-008: ES Modules Import Extensions
**Decision**: Backend TypeScript file imports must always include `.js` extension.
Use `import type` for type-only imports.

## Test Commands

```bash
# Backend
cd backend
npm run test:unit         # unit tests (no DB required)
npm run test:mock         # mock tests
npm run test:integration  # DB integration tests (PostgreSQL required)
npm run test:coverage     # coverage report

# Frontend
cd frontend
npm test                  # Jest unit tests (React Testing Library)
npm run test:e2e          # Playwright E2E tests
npm run test:keyword      # TypeScript Keyword-Driven tests
npm run test:e2e:ui       # Playwright UI mode

# Database
cd database
npm run db:migrate        # run Prisma migration
npm run db:generate       # generate Prisma client (sync backend/functions)
npm run db:reset          # full reset + seed
npm run db:studio         # Prisma Studio GUI
```

## Key Environment Variables

```bash
# Backend (.env)
DATABASE_URL=postgresql://user:password@localhost:5432/{db_name}
JWT_SECRET=...
ALLOWED_ORIGINS=http://localhost:3000
APPLICATIONINSIGHTS_CONNECTION_STRING=...  # or your observability service
CLOUD_STORAGE_CONNECTION_STRING=...        # or your object storage service
BLOB_CONTAINER_NAME={container-name}       # or your storage bucket/container name
USE_MOCK=false
USE_MOCK_DATE=false
MOCK_DATE=2025-03-15T10:30:00Z

# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:3000
NEXT_PUBLIC_USE_MSW=false
NEXT_PUBLIC_SKIP_AUTH=false
NEXT_PUBLIC_USE_MOCK_DATE=false
NEXT_PUBLIC_MOCK_DATE=2025-03-15
```

## Local Development Environment

```bash
# Start services with Docker Compose
cd config
docker-compose up -d
# PostgreSQL dev: 5432, test: 5433
# local cloud storage emulator (e.g., Azurite for Azure): 10000-10002

# Start Backend
cd backend && npm run dev   # http://localhost:3000

# Start Frontend
cd frontend && npm run dev  # http://localhost:3001
```

## Swagger UI

After starting Backend: `http://localhost:3000/docs`
Automatically updated when schema changes.

## Transaction Management

Apply `@Transactional` decorator to CUD operations in the Service layer.
Not needed for read operations (`getAll`, `getById`).
`tsconfig.json` requires `experimentalDecorators: true` and `emitDecoratorMetadata: true`.
