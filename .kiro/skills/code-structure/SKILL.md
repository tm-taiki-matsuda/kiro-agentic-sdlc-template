---
name: "Code Structure & Naming Conventions"
description: "Backend/Frontend directory maps, naming conventions, import rules, and Zod schema management. Referenced by all agents when deciding where to place code."
---

# Code Structure & Naming Conventions

> **⚠️ This file is the single source of truth for directory structure.**
> All agents use the paths defined here. When applying this framework to a new project,
> update this file first to match your actual directory layout.
> All other skills and prompts that reference file paths defer to this file.

> **Last verified**: {update when project starts}

## Backend Directory Map

```
backend/src/
├── api/
│   ├── routes/v1/         # Route handlers (thin: validation → service → response)
│   ├── plugins/           # Fastify plugins
│   │   ├── auth.ts        # authenticate decorator (JWT auth, applied per Route)
│   │   ├── authorizer.ts  # authorize decorator (role/permission checks)
│   │   ├── verify-jwt.ts  # JWT verification (global preHandler)
│   │   ├── permission-check.ts  # global authorization (path-based rule table)
│   │   ├── audit-log.ts   # audit log (auto-records CUD 2xx responses)
│   │   ├── error-handler.ts  # error handling (AppError → HTTP response)
│   │   └── ...
│   ├── app.ts             # app configuration
│   └── server.ts          # server startup
├── shared/
│   ├── services/          # business logic layer (SCOPED DI)
│   ├── repositories/      # data access layer (TRANSIENT DI, Prisma calls only)
│   ├── clients/           # external service clients
│   │   └── interfaces/    # client interfaces
│   ├── lib/               # DI container, Prisma, decorators
│   │   ├── container.ts   # Awilix DI container configuration
│   │   ├── prisma.ts      # Prisma client
│   │   └── decorators/
│   │       └── transactional.ts
│   ├── utils/             # utilities (no side effects)
│   │   ├── date-utils.ts  # date retrieval (alternative to new Date(), ADR-007)
│   │   ├── zod-to-json-schema.ts
│   │   └── {report-exporter}.ts   # report / file output (optional)
│   ├── schemas/           # Zod schemas (per endpoint: {feature}Schema.ts)
│   ├── config/            # environment configuration (environment.ts)
│   ├── constants/         # constants
│   ├── errors/            # AppError
│   ├── exporters/         # report / file output
│   └── types/             # common type definitions
└── types/                 # global type definitions
```

### Route Registration Pattern
```typescript
// Add /api prefix in app.ts
app.register(routes, { prefix: "/api" });

// Register each route with v1 prefix in routes/index.ts
fastify.register(itemsRoutes, { prefix: "/v1/items" });
// → final path: GET /api/v1/items
```

### DI Resolution Pattern
```typescript
// Resolve service in routes
const itemService = request.diScope.resolve<ItemService>('itemService');
```

## Frontend Directory Map

```
frontend/src/
├── app/                              # Next.js App Router (flat layout)
│   ├── login/                        # login page
│   ├── {feature}/                    # feature pages
│   │   ├── register/page.tsx         # registration page
│   │   └── detail/page.tsx           # detail page (?id=123)
│   └── auth/callback/                # auth callback
├── features/                         # feature-specific code
│   └── {feature}/
│       ├── MainContent.tsx           # top-level component
│       ├── hooks/                    # business logic hooks (useXxx.ts)
│       ├── types/                    # local types
│       └── utils/                    # dataMappers, calculations, validators
├── apis/                             # API hooks and types
├── components/
│   ├── ui/                           # shadcn/ui components
│   ├── common/                       # shared components
│   ├── layouts/                      # layout components
│   └── auth/                         # auth-related components
├── hooks/                            # shared hooks
├── services/api/                     # API service layer (axios calls)
├── lib/
│   ├── api/                          # API utilities
│   ├── auth/                         # auth utilities
│   └── dateUtils.ts                  # date retrieval (ADR-007)
└── utils/
    └── errorHandler.ts               # error message utilities
```

### Page Routing Pattern
```
// List page
frontend/src/app/{feature}/page.tsx
URL: /{feature}

// Detail page (query parameter format)
frontend/src/app/{feature}/detail/page.tsx
URL: /{feature}/detail?id=123

// Registration page
frontend/src/app/{feature}/register/page.tsx
URL: /{feature}/register
```

## Naming Conventions

| Target | Convention | Example |
|--------|-----------|---------|
| DB tables | snake_case plural | `items`, `order_details` |
| Backend Route files | kebab-case.ts | `items.ts`, `order-details.ts` |
| Backend Repository/Service | camelCase.ts | `items.repository.ts`, `items.service.ts` |
| Backend classes | PascalCase | `ItemService`, `ItemRepository` |
| Backend functions | camelCase | `getItemById`, `createItem` |
| Frontend components | PascalCase.tsx | `MainContent.tsx` |
| Frontend hooks | use + PascalCase.ts | `useItemList.ts`, `useItemForm.ts` |
| Zod schemas | {feature}Schema.ts | `itemsSchema.ts`, `ordersSchema.ts` |
| Test files | same name + .test.ts(x) | `useItemList.test.ts` |

## Import Rules

```typescript
// ✅ Correct: use shared package
import { {ConstantName}, type {TypeName} } from '@{project}/shared';

// ❌ Prohibited: cross package boundary direct import
import { {ConstantName} } from '../../shared/constants/codes';

// ✅ Correct: Backend .js extension
import { ItemRepository } from './item.repository.js';
import type { IStorageClient } from './interfaces/IStorageClient.js';

// ❌ Prohibited: any type
const data: any = response.data;  // use unknown + type guard instead
```

## Zod Schema Management

```
backend/src/shared/schemas/
├── itemsSchema.ts        # items API
├── ordersSchema.ts       # orders API
├── usersSchema.ts        # users API
└── ...
```

Naming: `{feature}Schema.ts`, exports: `{Feature}Schema`, `{Feature}ResponseSchema`

## MSW Mock Handlers (Frontend)

```
frontend/src/mocks/
├── data/          # mock data (TypeScript)
└── handlers/      # MSW handlers (must exactly match real API paths)
    └── index.ts   # export all handlers
```

## Test File Placement

```
# Frontend unit tests (same directory as component)
frontend/src/app/.../page.tsx
frontend/src/app/.../page.test.tsx

# Frontend E2E tests (TypeScript Keyword-Driven)
frontend/tests/testcases/{IT-ID}-{FEATURE}-{NNN}.spec.ts

# Backend tests
backend/tests/unit/repositories/   # Repository layer
backend/tests/unit/services/        # Service layer
backend/tests/integration/          # mock and DB integration tests
```
