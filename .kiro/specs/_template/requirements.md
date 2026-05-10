# Requirements: {Feature Name}

> **Created**: YYYY-MM-DD  
> **Agent**: feature-dev

## Overview

{One-paragraph overview of the feature. Describe what it achieves, who uses it, and why it is needed.}

## Screen Information

- **Screen URL**: `/{path}/list` (query parameter format; dynamic routes prohibited)
- **Related APIs**: `GET /api/v1/{feature}`, `POST /api/v1/{feature}`
- **Reference Documents**:
  - `design/features/{feature-doc}.md`
  - `design/api/specs/{api-spec}.yaml`

## User Stories (EARS Notation)

EARS notation: `WHEN [condition/event] THE SYSTEM SHALL [expected behavior]`  
Each requirement must be written at a granularity that can be tested independently.

### Happy Path

- WHEN the user {action} THEN the system displays {result}
- WHEN the user opens the list page THEN the system displays {N} {data type} items
- WHEN the user enters search conditions and clicks the search button THEN the system displays {data type} matching the conditions

### Validation

- WHEN the user submits with a required field empty THEN the system displays an error message requesting input for {field name}
- WHEN the user enters more than {N} characters THEN the system displays a character limit exceeded error

### Authorization

- IF the user does not have the {role} role THEN the system hides the {action} button
- WHEN an unauthorized user attempts {action} THEN the system returns a 403 error

### Error Cases

- IF the API returns an error THEN the system displays {error message} to the user
- IF a network error occurs THEN the system displays a message prompting a retry

### Boundary Values

- WHEN there are 0 data items THEN the system displays {empty state message}
- WHEN data exceeds the maximum count THEN the system displays pagination
