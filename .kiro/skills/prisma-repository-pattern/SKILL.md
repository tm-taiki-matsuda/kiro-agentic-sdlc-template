---
name: "Prisma Repository Pattern"
description: "Prisma Repository implementation pattern. Logical delete (is_deleted), optimistic lock (version), $queryRaw, and TDD test patterns. Referenced by backend-feature in Step 3 (Repository implementation)."
---

# Prisma Repository Implementation Pattern

> **File paths in this skill reflect the default structure. Always check `code-structure/SKILL.md` for the actual paths in your project.**

## Basic Class Structure

```typescript
// backend/src/shared/repositories/{feature}.repository.ts
import type { PrismaClient } from "@prisma/client";

export class {Feature}Repository {
  constructor(private readonly prisma: PrismaClient) {}

  async findAll(/* params */): Promise<{Feature}Data[]> {
    const result = await this.prisma.$queryRaw<{Feature}Data[]>`
      SELECT id, field1, field2, version
      FROM {table_name}
      WHERE is_deleted = false
      ORDER BY id
    `;
    return result;
  }

  async findById(id: number): Promise<{Feature}Data | null> {
    const result = await this.prisma.$queryRaw<{Feature}Data[]>`
      SELECT id, field1, field2, version
      FROM {table_name}
      WHERE id = ${id}
        AND is_deleted = FALSE
    `;
    return result[0] ?? null;
  }

  async create(data: CreateInput, userId: string): Promise<{ id: number; version: number }> {
    const result = await this.prisma.$queryRaw<{ id: number; version: number }[]>`
      INSERT INTO {table_name} (
        field1, field2,
        created_by, created_at, updated_by, updated_at,
        version, is_deleted
      ) VALUES (
        ${data.field1}, ${data.field2},
        ${userId}, ${getCurrentDate()}, ${userId}, ${getCurrentDate()},
        1, false
      ) RETURNING id, version
    `;
    // Note: using CURRENT_TIMESTAMP in SQL is also acceptable
    // created_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
    return result[0]!;
  }

  async update(
    id: number,
    data: UpdateInput,
    version: number,
    userId: string,
  ): Promise<{ id: number; version: number } | null> {
    const result = await this.prisma.$queryRaw<{ id: number; version: number }[]>`
      UPDATE {table_name}
      SET field1 = ${data.field1},
          field2 = ${data.field2},
          version = version + 1,
          updated_by = ${userId},
          updated_at = ${getCurrentDate()}
      WHERE id = ${id}
        AND version = ${version}
        AND is_deleted = FALSE
      RETURNING id, version
    `;
    return result[0] ?? null;
  }

  async softDelete(id: number, version: number, userId: string): Promise<boolean> {
    const result = await this.prisma.$queryRaw<{ id: number }[]>`
      UPDATE {table_name}
      SET is_deleted = true,
          updated_by = ${userId},
          updated_at = ${getCurrentDate()}
      WHERE id = ${id}
        AND version = ${version}
        AND is_deleted = FALSE
      RETURNING id
    `;
    return result.length > 0;
  }
}
```

## Required Rules

| Rule | ❌ Wrong | ✅ Correct |
|------|---------|-----------|
| Logical delete | `prisma.xxx.delete()` / `DELETE FROM` | `UPDATE SET is_deleted = true` |
| Optimistic lock | Update without version check | `WHERE version = ${version}` |
| Date retrieval | `new Date()` | `getCurrentDate()` or `CURRENT_TIMESTAMP` in SQL |
| All queries | No `is_deleted` filter | `AND is_deleted = FALSE` |
| Imports | No `.js` extension | `import { ... } from './xxx.js'` |

## Handling count=0 After Optimistic Lock Update (done in Service layer)

```typescript
// Service layer implementation
const updated = await repository.update(id, data, version, userId);
if (!updated) {
  throw new ConflictError("This data has been updated by another user.");
}
```

The Repository's update method returns `null` (when 0 rows updated).
Throwing `ConflictError` is the **Service layer's** responsibility.

## Prisma findMany Pattern (when not using `$queryRaw`)

```typescript
async findAll(year: number): Promise<{Feature}Data[]> {
  return await this.prisma.{tableName}.findMany({
    where: {
      year: year,
      is_deleted: false,
    },
    orderBy: { id: 'asc' },
  });
}

async updateWithLock(id: number, data: UpdateInput, version: number): Promise<number> {
  const result = await this.prisma.{tableName}.updateMany({
    where: { id, version, is_deleted: false },
    data: {
      ...data,
      version: { increment: 1 },
      updated_at: getCurrentDate(),
    },
  });
  return result.count; // 0 means optimistic lock failure
}
```

## Repository TDD Test Pattern

```typescript
// backend/tests/unit/repositories/{feature}.repository.test.ts
import { PrismaClient } from "@prisma/client";
import { mockDeep, DeepMockProxy } from "jest-mock-extended";
import { {Feature}Repository } from "../../../src/shared/repositories/{feature}.repository.js";

describe("{Feature}Repository", () => {
  let prisma: DeepMockProxy<PrismaClient>;
  let repository: {Feature}Repository;

  beforeEach(() => {
    prisma = mockDeep<PrismaClient>();
    repository = new {Feature}Repository(prisma);
  });

  it("happy-path_findAll_with-data_includes-is_deleted-filter", async () => {
    const mockData = [{ id: 1, field1: "test", is_deleted: false, version: 1 }];
    prisma.$queryRaw.mockResolvedValue(mockData);

    const result = await repository.findAll();

    // Assert that is_deleted = false filter is included in SQL
    expect(prisma.$queryRaw).toHaveBeenCalledWith(
      expect.arrayContaining([expect.stringContaining("is_deleted = false")])
    );
    expect(result).toEqual(mockData);
  });

  it("happy-path_update_version-match_returns-updated-result", async () => {
    const mockResult = [{ id: 1, version: 2 }];
    prisma.$queryRaw.mockResolvedValue(mockResult);

    const result = await repository.update(1, { field1: "new" }, 1, "user1");

    expect(result).toEqual({ id: 1, version: 2 });
  });

  it("error-case_update_version-mismatch_returns-null", async () => {
    prisma.$queryRaw.mockResolvedValue([]);

    const result = await repository.update(1, { field1: "new" }, 999, "user1");

    expect(result).toBeNull();
  });

  it("happy-path_softDelete_is_deleted-updated-to-true", async () => {
    prisma.$queryRaw.mockResolvedValue([{ id: 1 }]);

    const result = await repository.softDelete(1, 1, "user1");

    expect(result).toBe(true);
    // Verify DELETE statement was not called
    expect(prisma.$executeRaw).not.toHaveBeenCalledWith(
      expect.arrayContaining([expect.stringContaining("DELETE")])
    );
  });
});
```

## Add Export to index.ts

```typescript
// Add to backend/src/shared/repositories/index.ts
export { {Feature}Repository } from "./{feature}.repository.js";
```

## Import Pattern

```typescript
// Correct imports (.js extension required)
import { getCurrentDate } from "../utils/date-utils.js";
import { ConflictError } from "../errors/AppError.js";
import type { {Feature}Repository } from "../repositories/{feature}.repository.js";
```
