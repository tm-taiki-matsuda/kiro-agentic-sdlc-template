---
name: "React Query Hook Pattern"
description: "TDD implementation patterns for API fetch hooks (useQuery) and custom hooks (useState + direct services calls). getErrorMessage, isSaving, and 409 handling. Referenced by frontend-feature in Steps 3–5."
---

# API Hook & Custom Hook TDD Pattern

> **File paths in this skill reflect the default structure. Always check `code-structure/SKILL.md` for the actual paths in your project.**
> **Utility names (`apiClient`, `getErrorMessage`) are examples from the default setup. Replace with your project's actual HTTP client and error handler.**

## Directory Structure

```
frontend/src/
├── apis/
│   └── {category}/{ApiId}/    # e.g., items/LIST001, orders/ORD001
│       ├── types.ts            ← type definitions
│       ├── use{Feature}.ts     ← API hook (fetch data with useQuery)
│       └── use{Feature}.test.ts
├── services/
│   └── {feature}Service.ts     ← CUD operations (direct axios calls)
└── features/
    └── {domain}/
        └── {section}/
            ├── schemas/
            │   └── {domain}Schema.ts    ← Zod validation
            └── hooks/
                ├── use{Section}.ts      ← custom hook (useState + services)
                └── use{Section}.test.ts
```

## Type Definitions (types.ts)

```typescript
// frontend/src/apis/{category}/{ApiId}/types.ts
export interface {Feature}Item {
  id: number;
  field1: string;
  field2: number;
  version: number;  // for optimistic lock (required)
  created_at: string;
}

export interface {Feature}ListResponse {
  contents: {Feature}Item[];
  totalCount: number;
  offset: number;
  limit: number;
}

export interface Create{Feature}Input {
  field1: string;
  field2: number;
}

export interface Update{Feature}Input {
  field1: string;
  field2: number;
  version: number;  // required: optimistic lock
}
```

## API Hook (useQuery for data fetching only)

```typescript
// frontend/src/apis/{category}/{ApiId}/use{Feature}.ts
import { useQuery } from '@tanstack/react-query';
import apiClient from '@/lib/axios';
import type { {Feature}ListResponse } from './types';

export const use{Feature}List = (params: { year: number }) => {
  return useQuery<{Feature}ListResponse>({
    queryKey: ['{feature}', params],
    queryFn: async () => {
      const { data } = await apiClient.get('/api/v1/{feature}', { params });
      return data;
    },
  });
};

export const use{Feature}Detail = (id: number | null) => {
  return useQuery({
    queryKey: ['{feature}', 'detail', id],
    queryFn: async () => {
      const { data } = await apiClient.get(`/api/v1/{feature}/detail?id=${id}`);
      return data;
    },
    enabled: !!id,
  });
};
```

## Services (CUD operations — do not use useMutation)

```typescript
// frontend/src/services/{feature}Service.ts
import apiClient from '@/lib/axios';
import type { Create{Feature}Input, Update{Feature}Input } from '@/apis/{category}/{ApiId}/types';

export const {feature}Service = {
  create: async (data: Create{Feature}Input) => {
    const { data: result } = await apiClient.post('/api/v1/{feature}', data);
    return result;
  },

  update: async (id: number, data: Update{Feature}Input) => {
    const { data: result } = await apiClient.patch(`/api/v1/{feature}?id=${id}`, data);
    return result;
  },

  delete: async (id: number, version: number) => {
    await apiClient.patch(`/api/v1/{feature}?id=${id}`, { is_deleted: true, version });
  },
};
```

## Custom Hook (useState + direct services calls)

```typescript
// frontend/src/features/{domain}/{section}/hooks/use{Section}.ts
import { useState, useCallback } from 'react';
import { {feature}Service } from '@/services/{feature}Service';
import { getErrorMessage } from '@/utils/errorHandler';

export const use{Section} = (initialData?: {Feature}Item) => {
  // manage fields individually with useState
  const [field1, setField1] = useState(initialData?.field1 ?? '');
  const [field2, setField2] = useState(initialData?.field2 ?? 0);
  const [version, setVersion] = useState(initialData?.version ?? 0);

  // save state
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const save = useCallback(async (
    callbacks?: { onSuccess?: () => void; onError?: (msg: string) => void }
  ) => {
    setIsSaving(true);
    setError(null);
    try {
      if (initialData?.id) {
        // update (version required)
        await {feature}Service.update(initialData.id, { field1, field2, version });
      } else {
        // create
        await {feature}Service.create({ field1, field2 });
      }
      callbacks?.onSuccess?.();
    } catch (err) {
      const msg = getErrorMessage(err);
      setError(msg);
      callbacks?.onError?.(msg);
    } finally {
      setIsSaving(false);
    }
  }, [field1, field2, version, initialData]);

  return {
    field1, setField1,
    field2, setField2,
    isSaving, error, save,
  };
};
```

## 409 Conflict Error Handling

`getErrorMessage()` detects HTTP 409 and returns an appropriate message:

```typescript
// getErrorMessageByStatus in frontend/src/utils/errorHandler.ts
case 409:
  return 'This data has been updated by another user. Please reload the page.';
```

Explicitly handling 409 in a custom hook:
```typescript
} catch (err) {
  const axiosErr = err as { response?: { status?: number } };
  if (axiosErr.response?.status === 409) {
    setError('This data has been updated by another user. Please reload the page.');
  } else {
    setError(getErrorMessage(err));
  }
}
```

## Custom Hook TDD Test Pattern

```typescript
// frontend/src/features/{domain}/{section}/hooks/use{Section}.test.ts
import { renderHook, act } from '@testing-library/react';
import { use{Section} } from './use{Section}';

// mock services
jest.mock('@/services/{feature}Service', () => ({
  {feature}Service: {
    create: jest.fn(),
    update: jest.fn(),
  },
}));

import { {feature}Service } from '@/services/{feature}Service';

describe('use{Section}', () => {
  beforeEach(() => jest.clearAllMocks());

  it('initial values are set correctly', () => {
    const { result } = renderHook(() => use{Section}());
    expect(result.current.field1).toBe('');
    expect(result.current.isSaving).toBe(false);
    expect(result.current.error).toBeNull();
  });

  it('calls onSuccess when save succeeds', async () => {
    ({feature}Service.create as jest.Mock).mockResolvedValue({ id: 1 });
    const onSuccess = jest.fn();
    const { result } = renderHook(() => use{Section}());

    await act(async () => {
      await result.current.save({ onSuccess });
    });

    expect(onSuccess).toHaveBeenCalled();
    expect(result.current.error).toBeNull();
  });

  it('sets error when save fails', async () => {
    ({feature}Service.create as jest.Mock).mockRejectedValue({
      response: { status: 500 }
    });
    const { result } = renderHook(() => use{Section}());

    await act(async () => {
      await result.current.save();
    });

    expect(result.current.error).not.toBeNull();
  });

  it('sets conflict message on 409 error', async () => {
    ({feature}Service.update as jest.Mock).mockRejectedValue({
      response: { status: 409 }
    });
    const { result } = renderHook(() =>
      use{Section}({ id: 1, field1: 'test', field2: 1, version: 1, created_at: '' })
    );

    await act(async () => {
      await result.current.save();
    });

    expect(result.current.error).toContain('updated');
  });
});
```

## API Hook TDD Test Pattern

```typescript
// frontend/src/apis/{category}/{ApiId}/use{Feature}.test.ts
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import React from 'react';
import { use{Feature}List } from './use{Feature}';

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return ({ children }: { children: React.ReactNode }) =>
    React.createElement(QueryClientProvider, { client: queryClient }, children);
};

describe('use{Feature}List', () => {
  it('returns contents on successful data fetch', async () => {
    const { result } = renderHook(
      () => use{Feature}List({ year: 2025 }),
      { wrapper: createWrapper() }
    );

    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data?.contents).toBeDefined();
  });
});
```
