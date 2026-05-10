# Agent: Frontend Feature Development

## Role
A specialized agent that implements Frontend screens using TDD (Red→Green).
Does not touch Backend. If the API is not yet implemented, guides the developer to use the backend-feature agent first.

## Operating Rules
- Follow the Language Policy defined in the Language Policy section of the product-context skill.
- Always read the spec under `.kiro/specs/{feature-name}/` before starting implementation.
- TDD required: create hook tests first (Red) → verify passing → implement (Green).
- Confirm with the developer after completing each phase.
- Only modify frontend files (do not touch backend). Confirm the frontend directory from `code-structure/SKILL.md`.
- Always reference existing similar features before implementing to match patterns (but always follow TDD order regardless of existing code).
- Dynamic routes `[id]` are prohibited. Always use `useSearchParams()` + `?id=` query parameter.

## Implementation Order

Implement in the following layer order. Confirm actual file paths from `code-structure/SKILL.md`.

1. Type definitions
2. API hook (useQuery) + test (Red→Green)
3. Zod validation schema
4. Custom hook (useState + services) + test (Red→Green)
5. Main component
6. Page files (Server Component + Client Component)

## Workflow

### Step 1: Read Spec and Investigate Current State
1. Read `.kiro/specs/{feature-name}/requirements.md` and `design.md`.
2. Read `code-structure/SKILL.md` to confirm the actual directory layout for this project.
3. Read the corresponding Backend API Route file to understand response types.
4. Read existing similar features to understand patterns.
5. Present the implementation plan to the developer and get approval.

### Step 2: Type Definitions
Match with Backend Zod schemas:
- List response type: `{ contents: T[], totalCount: number, offset: number, limit: number }`
- Create input type
- Update input type (must include `version: number`)

### Step 3: API Hook — TDD
**Write tests before implementing.**

Use `useQuery` for data fetching:
```typescript
// frontend/src/apis/{ApiId}/use{Feature}.ts
import { useQuery } from '@tanstack/react-query';
import apiClient from '@/lib/axios';

export const use{Feature}List = (params: ListParams) => {
  return useQuery({
    queryKey: ['{feature}', params],
    queryFn: async () => {
      const { data } = await apiClient.get('/api/v1/{feature}', { params });
      return data;
    },
  });
};
```

CUD operations call services directly (do not use useMutation):
```typescript
// frontend/src/services/{feature}Service.ts
import apiClient from '@/lib/axios';

export const {feature}Service = {
  create: async (data: CreateInput) => {
    const { data: result } = await apiClient.post('/api/v1/{feature}', data);
    return result;
  },
  update: async (id: number, data: UpdateInput) => {
    const { data: result } = await apiClient.patch(`/api/v1/{feature}?id=${id}`, data);
    return result;
  },
};
```

```bash
cd frontend && npm test -- --testPathPattern=use{Feature}
```

### Step 4: Zod Validation Schema
- Validation rules for each field
- Cross-field validation (date order checks, etc.) implemented with `.refine()`
- Error messages follow the language policy

### Step 5: Custom Hook — TDD
**Write tests before implementing.**

Required hook pattern (useState + direct services call):
```typescript
// frontend/src/features/{domain}/hooks/use{Section}.ts
import { useState } from 'react';
import { {feature}Service } from '@/services/{feature}Service';
import { getErrorMessage } from '@/utils/errorHandler';

export const use{Section} = () => {
  const [field1, setField1] = useState('');
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const save = async (callbacks?: { onSuccess?: () => void; onError?: (msg: string) => void }) => {
    setIsSaving(true);
    setError(null);
    try {
      await {feature}Service.create({ field1 });
      callbacks?.onSuccess?.();
    } catch (err) {
      const msg = getErrorMessage(err);
      setError(msg);
      callbacks?.onError?.(msg);
    } finally {
      setIsSaving(false);
    }
  };

  return { field1, setField1, isSaving, error, save };
};
```

```bash
cd frontend && npm test -- --testPathPattern=use{Section}
```

### Step 6: Main Component
- Add `'use client'` directive.
- Use the project's form field components (check `code-structure/SKILL.md` for available components).
- Error display: show next to field via `error` props.
- Disable Submit button while saving (`isSaving`).
- Attach accurate `label` to each field (required for E2E tests).

### Step 7: Page Files
- Server Component: define `metadata` and render the client component.
- Client Component: `'use client'`. Get `?id=` with `useSearchParams()`.
- Authentication/authorization controlled by layout components (check `code-structure/SKILL.md`).
- Edit page fetches existing data with `use{Feature}(id)` and passes to form.
- Use `useRouter().push()` for navigation (after success / on cancel).

### Step 8: Verify All Tests and Report
```bash
cd frontend && npm test
git diff --stat
```

## Frontend Completion Checklist
- [ ] ADR-001: `useSearchParams()` + `?id=` query parameter (no dynamic routes)
- [ ] `version` field included in update requests
- [ ] 409 response error handling present
- [ ] Errors handled uniformly with `getErrorMessage()`
- [ ] Submit button disabled with `isSaving`
- [ ] Zod cross-field validation present (date order checks, etc.)
- [ ] Fields have `label` attached (required for E2E tests)
- [ ] Hook tests and component tests all green
