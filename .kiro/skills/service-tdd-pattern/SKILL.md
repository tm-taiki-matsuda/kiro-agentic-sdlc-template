---
name: "Service TDD Pattern"
description: "Backend Service layer TDD implementation pattern. @Transactional decorator, ConflictError, permission checks, and Repository mocking. Referenced by backend-feature in Step 4 (Service implementation)."
---

# Backend Service Layer TDD Pattern

> **File paths in this skill reflect the default structure. Always check `code-structure/SKILL.md` for the actual paths in your project.**

## Basic Class Structure

```typescript
// backend/src/shared/services/{feature}.service.ts
import type { PrismaClient } from "@prisma/client";
import { ConflictError, NotFoundError, ForbiddenError } from "../errors/AppError.js";
import { {Feature}Repository } from "../repositories/{feature}.repository.js";
import type {
  Get{Feature}Query,
  Get{Feature}Response,
  Create{Feature}Request,
  Create{Feature}Response,
  Update{Feature}Request,
  Update{Feature}Response,
} from "../schemas/{feature}Schema.js";
import { Transactional } from "../lib/decorators/transactional.js";

export class {Feature}Service {
  prisma: PrismaClient;
  private repository: {Feature}Repository;

  constructor(prisma: PrismaClient, repository: {Feature}Repository) {
    this.prisma = prisma;
    this.repository = repository;
  }

  // ─── Read operations (@Transactional not needed) ───

  async getList(query: Get{Feature}Query, userId: string): Promise<Get{Feature}Response> {
    const items = await this.repository.findAll(query);
    return {
      contents: items,
      totalCount: items.length,
      offset: query.offset ?? 0,
      limit: query.limit ?? 20,
    };
  }

  async getById(id: number, userId: string): Promise<{Feature}Response> {
    const item = await this.repository.findById(id);
    if (!item) throw new NotFoundError("{Resource} not found");
    return item;
  }

  // ─── Write operations (@Transactional required) ───

  @Transactional
  async create(request: Create{Feature}Request, userId: string): Promise<Create{Feature}Response> {
    const result = await this.repository.create(request, userId);
    return result;
  }

  @Transactional
  async update(
    id: number,
    request: Update{Feature}Request,
    userId: string,
  ): Promise<Update{Feature}Response> {
    const updated = await this.repository.update(id, request, request.version, userId);
    if (!updated) {
      // Optimistic lock failure → ConflictError
      throw new ConflictError("This data has been updated by another user.");
    }
    return updated;
  }

  @Transactional
  async delete(id: number, version: number, userId: string): Promise<void> {
    const deleted = await this.repository.softDelete(id, version, userId);
    if (!deleted) {
      throw new ConflictError("This data has been updated by another user.");
    }
  }
}
```

## @Transactional Decorator Required Rules

```typescript
import { Transactional } from "../lib/decorators/transactional.js";

// ✅ Apply @Transactional to all CUD operations (Create/Update/Delete)
@Transactional
async create(...) { ... }

@Transactional
async update(...) { ... }

@Transactional
async delete(...) { ... }

// ✅ Not needed for read operations
async getList(...) { ... }
async getById(...) { ... }
```

### Direct $transaction Usage Pattern for Large Services

When Repository needs to be dynamically created within a transaction:

```typescript
// ✅ Direct $transaction usage (when tx needs to be passed to Repository)
async create(request: CreateRequest, userId: string) {
  return this.prisma.$transaction(async (tx) => {
    const repository = new {Feature}Repository(tx);
    const result = await repository.create(request, userId);
    // related table operations within the same transaction
    await repository.createRelated(result.id, request.relatedData, userId);
    return result;
  });
}
```

**When to use which:**
- Simple CUD → `@Transactional` decorator
- Multiple Repositories in same transaction → direct `$transaction`

## Service TDD Test Pattern

```typescript
// backend/tests/unit/services/{feature}.service.test.ts
import { jest } from '@jest/globals';
import { {Feature}Service } from "../../../src/shared/services/{feature}.service.js";
import { {Feature}Repository } from "../../../src/shared/repositories/{feature}.repository.js";
import { ConflictError } from "../../../src/shared/errors/AppError.js";

// Mock Repository
jest.mock('../../../src/shared/repositories/{feature}.repository.js');
const MockRepository = {Feature}Repository as jest.MockedClass<typeof {Feature}Repository>;

describe('{Feature}Service', () => {
  let service: {Feature}Service;
  let mockRepository: jest.Mocked<{Feature}Repository>;

  beforeEach(() => {
    jest.clearAllMocks();
    mockRepository = new MockRepository(null as any) as jest.Mocked<{Feature}Repository>;
    service = new {Feature}Service(null as any, mockRepository);
  });

  describe('getList', () => {
    it('happy-path_getList_with-data_returns-contents-and-totalCount', async () => {
      const mockItems = [{ id: 1, field1: 'test', version: 1 }];
      mockRepository.findAll.mockResolvedValue(mockItems);

      const result = await service.getList({ offset: 0, limit: 20 }, 'user1');

      expect(result.contents).toEqual(mockItems);
      expect(result.totalCount).toBe(1);
    });
  });

  describe('update', () => {
    it('happy-path_update_version-match_returns-updated-result', async () => {
      const mockResult = { id: 1, version: 2 };
      mockRepository.update.mockResolvedValue(mockResult);

      const result = await service.update(1, { field1: 'new', version: 1 }, 'user1');

      expect(result).toEqual(mockResult);
      expect(mockRepository.update).toHaveBeenCalledWith(1, expect.any(Object), 1, 'user1');
    });

    it('error-case_update_optimistic-lock-failure_throws-ConflictError', async () => {
      // Repository returns null = optimistic lock failure
      mockRepository.update.mockResolvedValue(null);

      await expect(
        service.update(1, { field1: 'new', version: 999 }, 'user1')
      ).rejects.toThrow(ConflictError);
    });
  });

  describe('create', () => {
    it('happy-path_create_success_returns-id-and-version', async () => {
      mockRepository.create.mockResolvedValue({ id: 1, version: 1 });

      const result = await service.create({ field1: 'new' }, 'user1');

      expect(result).toEqual({ id: 1, version: 1 });
    });
  });

  describe('delete', () => {
    it('happy-path_delete_logical-delete-success_does-not-throw', async () => {
      mockRepository.softDelete.mockResolvedValue(true);

      await expect(service.delete(1, 1, 'user1')).resolves.not.toThrow();
    });

    it('error-case_delete_optimistic-lock-failure_throws-ConflictError', async () => {
      mockRepository.softDelete.mockResolvedValue(false);

      await expect(service.delete(1, 999, 'user1')).rejects.toThrow(ConflictError);
    });
  });
});
```

## Test Execution Command

```bash
cd backend && npm run test:unit -- --testPathPattern={feature}.service
```

## Add Export to index.ts

```typescript
// Add to backend/src/shared/services/index.ts
export { {Feature}Service } from "./{feature}.service.js";
```

## Permission Check Pattern (optional)

```typescript
// Implement only when needed for specific features
private async checkPermission(userId: string, resource: string, action: string): Promise<void> {
  // Use your project's auth repository to check permissions
  const allowed = await this.checkUserPermission(userId, resource, action);
  if (!allowed) throw new ForbiddenError();
}
```

## Service Completion Checklist

- [ ] CUD methods have `@Transactional` decorator
- [ ] Optimistic lock failure (null return) throws `ConflictError`
- [ ] Use `getCurrentDate()` (no direct `new Date()`)
- [ ] Imports with `.js` extension
- [ ] Export added to services/index.ts
- [ ] Optimistic lock conflict test (verify ConflictError is thrown) present
- [ ] All tests green
