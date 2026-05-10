---
name: "Serverless Functions Guide"
description: "Serverless Functions definition patterns, directory structure, Outbox pattern, and test commands. Referenced by functions-feature agent when adding or modifying functions."
---

# Serverless Functions

## Overview

Serverless layer responsible for batch processing, async processing, and notification delivery.
Implemented with Serverless Functions (e.g., Azure Functions, AWS Lambda) + TypeScript.

## Function Directory Structure

```
functions/src/
├── functions/
│   ├── {category}/      # category-based directories
│   │   ├── {funcId}/    # one directory per function
│   │   └── README.md
│   └── shared/          # shared processing
│       ├── dlq-processor/
│       └── outbox-processor/
├── repositories/        # data access layer
├── services/            # business logic layer
├── shared/              # shared utilities
│   ├── lib/
│   ├── errors/
│   ├── types/
│   └── constants/
├── config/
│   └── environment.ts   # environment variable configuration
└── index.ts             # registration entry point for all functions
```

## Serverless Functions API Style

> The code samples below use **Azure Functions v4** as a concrete example.
> Adapt trigger types and SDK imports to your runtime (e.g., AWS Lambda handler signature).

### Timer Trigger (Scheduled Batch)

```typescript
// src/functions/{category}/{funcId}/index.ts
// Example: Azure Functions v4
import { app, InvocationContext, Timer } from '@azure/functions';

export async function {funcId}Handler(
  myTimer: Timer,
  context: InvocationContext
): Promise<void> {
  context.log('{funcId} started');
  // processing
  context.log('{funcId} complete');
}

app.timer('{funcId}', {
  schedule: '0 0 9 * * 1-5',  // weekdays at 9am
  handler: {funcId}Handler,
});
```

### Event Trigger (Event Processing)

```typescript
// Example: Azure Functions v4 — EventGrid trigger
import { app, EventGridEvent, InvocationContext } from '@azure/functions';

app.eventGrid('{funcId}', {
  handler: async (event: EventGridEvent, context: InvocationContext) => {
    context.log('Event trigger received:', event.eventType);
    // processing
  },
});
```

### Register in index.ts

Always import new functions in `src/index.ts`:

```typescript
// src/index.ts
import './functions/{category}/{funcId}/index';
// ... add new functions here
```

## Using Prisma Schema

`functions/` uses a **generated copy** of `database/prisma/schema.prisma` (synced via `npm run db:generate`, ADR-002).

```bash
# Sync schema and regenerate client
cd functions && npm run db:generate
```

## Test Commands

```bash
cd functions
npm test                    # all tests
npm run test:unit           # unit tests (tests/unit/)
npm run test:integration    # integration tests (tests/integration/)
npm run test:coverage       # coverage report
```

## Local Execution

```bash
# Start PostgreSQL + local storage emulator with Docker first
cd config && docker-compose up -d

cd functions
npm run dev   # start Functions emulator
```

## Environment Variables

Centrally managed in `functions/src/config/environment.ts`:

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string |
| `EVENT_TRIGGER_ENDPOINT` | Event trigger endpoint |
| `SECRET_MANAGER_URL` | Secret management service URL (or equivalent) |

## Outbox Pattern

Send notifications via the Outbox pattern (`shared/outbox-processor`).
Do not call event bus / email APIs directly. Write to DB first, then send asynchronously.

```
Function → insert into DB outbox table
outbox-processor runs periodically → fetch unsent records → send → update status
```

## Safety Constraints

- Do not modify `database/prisma/schema.prisma` directly (ADR-002)
- Use `getCurrentDate()` (`new Date()` prohibited, ADR-007)
- Logical delete only (`is_deleted = true`, ADR-005)
- Do not output secrets to `console.log` or `context.log`
