---
name: "Fastify Route Pattern"
description: "Fastify Route layer implementation pattern. authenticate plugin, Zod validation, DI resolution, list response format, and Route test template. Referenced by backend-feature in Step 5 (Route implementation)."
---

# Fastify Route Implementation Pattern

> **File paths in this skill reflect the default structure. Always check `code-structure/SKILL.md` for the actual paths in your project.**

## Authentication & Authorization Mechanism

> **The plugin names below (`authenticate`, `permission-check`, `audit-log`) are examples from the default project setup.
> Replace with your project's actual auth/authz mechanism as defined in `security-constraints/SKILL.md`.**

- **Authentication**: Apply an auth hook to each route (e.g., `onRequest: [fastify.authenticate]`)
- **Authorization**: Apply globally via a permission plugin, or per-route as needed
- **Audit log**: Record CUD operations automatically via a plugin, or implement manually

## Basic Route File Structure

```typescript
// backend/src/api/routes/v1/{feature}.ts
import type { FastifyInstance, FastifyRequest, FastifyReply } from "fastify";
import {
  Create{Feature}RequestSchema,
  Create{Feature}ResponseSchema,
  Update{Feature}RequestSchema,
  Update{Feature}ResponseSchema,
  Get{Feature}ListQuerySchema,
  Get{Feature}ListResponseSchema,
  type Create{Feature}Request,
  type Update{Feature}Request,
} from "../../../shared/schemas/{feature}Schema.js";
import type { {Feature}Service } from "../../../shared/services/{feature}.service.js";
import { createFastifySchema } from "../../../shared/utils/zod-to-json-schema.js";

const {feature}Routes = async (fastify: FastifyInstance) => {

  // GET / — list
  fastify.get(
    "/",
    {
      onRequest: [fastify.authenticate],
      schema: {
        querystring: createFastifySchema(Get{Feature}ListQuerySchema),
        response: { 200: createFastifySchema(Get{Feature}ListResponseSchema) },
      },
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      const query = Get{Feature}ListQuerySchema.parse(request.query);
      const user = request.user;
      if (!user || !user.userId) {
        return reply.status(401).send({ errors: [{ code: "AUTH_001", message: "Authentication required" }] });
      }
      const service = request.diScope.resolve<{Feature}Service>("{feature}Service");
      const result = await service.getList(query, user.email);
      return reply.status(200).send(result);
    },
  );

  // GET /detail?id={id} — single item (?id= query parameter; /detail subpath also acceptable)
  fastify.get(
    "/detail",
    {
      onRequest: [fastify.authenticate],
      schema: {
        querystring: createFastifySchema(Get{Feature}DetailQuerySchema),
        response: { 200: createFastifySchema(Get{Feature}DetailResponseSchema) },
      },
    },
    async (request: FastifyRequest, reply: FastifyReply) => {
      const { id } = Get{Feature}DetailQuerySchema.parse(request.query);
      const user = request.user;
      if (!user || !user.userId) {
        return reply.status(401).send({ errors: [{ code: "AUTH_001", message: "Authentication required" }] });
      }
      const service = request.diScope.resolve<{Feature}Service>("{feature}Service");
      const result = await service.getById(id, user.email);
      return reply.status(200).send(result);
    },
  );

  // POST / — create
  fastify.post<{ Body: Create{Feature}Request }>(
    "/",
    {
      onRequest: [fastify.authenticate],
      schema: {
        body: createFastifySchema(Create{Feature}RequestSchema),
        response: { 201: createFastifySchema(Create{Feature}ResponseSchema) },
      },
    },
    async (request: FastifyRequest<{ Body: Create{Feature}Request }>, reply: FastifyReply) => {
      const validatedData = Create{Feature}RequestSchema.parse(request.body);
      const user = request.user;
      if (!user || !user.userId) {
        return reply.status(401).send({ errors: [{ code: "AUTH_001", message: "Authentication required" }] });
      }
      const service = request.diScope.resolve<{Feature}Service>("{feature}Service");
      const result = await service.create(validatedData, user.email);
      return reply.status(201).send(result);
    },
  );

  // PATCH /?id={id} — update
  fastify.patch<{ Body: Update{Feature}Request }>(
    "/",
    {
      onRequest: [fastify.authenticate],
      schema: {
        querystring: createFastifySchema(Update{Feature}QuerySchema),
        body: createFastifySchema(Update{Feature}RequestSchema),
        response: { 200: createFastifySchema(Update{Feature}ResponseSchema) },
      },
    },
    async (request: FastifyRequest<{ Body: Update{Feature}Request }>, reply: FastifyReply) => {
      const { id } = Update{Feature}QuerySchema.parse(request.query);
      const validatedData = Update{Feature}RequestSchema.parse(request.body);
      const user = request.user;
      if (!user || !user.userId) {
        return reply.status(401).send({ errors: [{ code: "AUTH_001", message: "Authentication required" }] });
      }
      const service = request.diScope.resolve<{Feature}Service>("{feature}Service");
      const result = await service.update(id, validatedData, user.email);
      return reply.status(200).send(result);
    },
  );
};

export default {feature}Routes;
```

## Route Registration in routes/index.ts

```typescript
// Add to backend/src/api/routes/index.ts (dynamic import pattern)
await fastify.register(import("./v1/{feature}.js"), { prefix: "/v1/{feature}" });
// → final path: /api/v1/{feature} (app.ts already adds /api prefix)
```

## List Response Format (required)

```typescript
return reply.status(200).send({
  contents: items,
  totalCount: total,
  offset: query.offset,
  limit: query.limit,
});
```

## Route Test Template

```typescript
// backend/tests/unit/routes/{feature}.route.test.ts
import { createApp } from "../../helpers/app.js";
import type { FastifyInstance } from "fastify";

describe("{Feature} Route Tests", () => {
  let app: FastifyInstance;

  beforeAll(async () => {
    app = await createApp();
    await app.ready();
  });

  afterAll(async () => {
    await app.close();
  });

  describe("GET /api/v1/{feature}", () => {
    it("happy-path_GET_list_authenticated_returns-200", async () => {
      const response = await app.inject({
        method: "GET",
        url: "/api/v1/{feature}",
        headers: { "x-api-mock": "true", "x-mock-user-id": "test-user" },
      });
      expect(response.statusCode).toBe(200);
      const body = JSON.parse(response.body);
      expect(body).toHaveProperty("contents");
      expect(body).toHaveProperty("totalCount");
    });

    it("error-case_GET_unauthenticated_returns-401", async () => {
      const response = await app.inject({
        method: "GET",
        url: "/api/v1/{feature}",
      });
      expect(response.statusCode).toBe(401);
    });
  });

  describe("PATCH /api/v1/{feature}?id=1", () => {
    it("error-case_PATCH_optimistic-lock-conflict_returns-409", async () => {
      const response = await app.inject({
        method: "PATCH",
        url: "/api/v1/{feature}?id=1",
        headers: { "x-api-mock": "true", "x-mock-user-id": "test-user", "content-type": "application/json" },
        payload: { version: 999 },
      });
      expect(response.statusCode).toBe(409);
    });
  });
});
```

## DI Resolution Naming Convention

```typescript
// {Feature}Service → "{feature}Service" (camelCase)
const service = request.diScope.resolve<{Feature}Service>("{feature}Service");
```

## Implementation Checklist

- [ ] Registered in `routes/index.ts` with `{ prefix: '/v1/{feature}' }`
- [ ] `onRequest: [fastify.authenticate]` applied
- [ ] Authorization auto-applied by permission-check plugin (no manual needed)
- [ ] Request/response defined with `createFastifySchema(ZodSchema)`
- [ ] Single item retrieval uses `/detail?id=` query parameter (no dynamic routes)
- [ ] List response is `{ contents, totalCount, offset, limit }`
- [ ] Audit log auto-recorded by audit-log plugin (no manual needed)
- [ ] Updates use `fastify.patch` (PATCH, not PUT)
- [ ] Route tests: success (200/201), validation (400), unauthenticated (401), conflict (409)
