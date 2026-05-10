---
name: "EARS Notation Guide"
description: "Requirements writing guide using EARS notation (WHEN/THEN/IF/SHALL). How to write happy path, validation, authorization, error cases, and boundary values in requirements.md. Referenced by spec-writer when writing requirements."
---

# EARS Notation Requirements Writing Guide

EARS (Easy Approach to Requirements Syntax) is a notation for writing requirements at a testable granularity.
Used in the user stories section of requirements.md.

## Basic Syntax

| Pattern | Syntax | Use case |
|---------|--------|---------|
| Event-driven | `WHEN {condition/action} THEN the system {expected behavior}` | Main functional requirements |
| State/condition | `IF {precondition} THEN the system {behavior}` | Permission/status-dependent behavior |
| Obligation | `The system SHALL {behavior} {quality requirement}` | Performance/security requirements |
| Optional | `WHERE {context} IF {condition} THEN the system {behavior}` | Applies only in specific context |

## Templates by Requirement Category

### 1. Happy Path

```markdown
### Happy Path
WHEN the user opens the "{screen name}" screen THEN the system displays a list of {data type}
WHEN the user fills in all required fields and clicks the register button THEN the system registers {feature name} and navigates to the list screen
WHEN the user selects "Edit" on an existing {data type} THEN the system displays a pre-filled form for that data
WHEN the user saves the edited content THEN the system reflects the update and returns to the list screen
WHEN the user selects "Delete" and confirms THEN the system logically deletes the data and removes it from the list
```

### 2. Validation

```markdown
### Validation
WHEN the user submits with {field name} empty THEN the system displays "{field label} is required" below the {field name} field
WHEN the user enters an invalid date format in {date field} THEN the system displays "Invalid date format (e.g., 2025/04/01)"
WHEN the end date is entered before the start date THEN the system displays "End date must be on or after the start date"
WHEN a negative value is entered in {numeric field} THEN the system displays "{field label} must be 0 or greater"
WHEN {text field} exceeds {N} characters THEN the system displays "{field label} must be {N} characters or fewer"
```

### 3. Authorization & Role Control

```markdown
### Authorization
IF the user has the "Viewer" role THEN the system hides the register, edit, and delete buttons
IF an unauthenticated user accesses {URL} THEN the system redirects to the login screen
IF the user attempts to edit data from another organization THEN the system returns a 403 error
```

### 4. Error Cases

```markdown
### Error Cases
WHEN saving while the data has been updated by another user THEN the system displays "Data has been updated. Please check the latest data and try again."
WHEN the API times out or a network error occurs THEN the system displays "A communication error occurred. Please try again later."
WHEN the API returns a 500 error THEN the system displays "An unexpected error occurred." and logs the error details
```

### 5. Boundary Values & Edge Cases

```markdown
### Boundary Values
WHEN displaying a list with 0 {data type} items THEN the system displays "{Data type} has not been registered yet"
WHEN {data type} exceeds the maximum page size ({N} items) THEN the system displays pagination
```

## Optimistic Lock Conflict Requirement (required pattern)

```markdown
WHEN multiple users edit the same data simultaneously and the later user tries to save THEN
  the system displays "This data has already been updated. Please reload the page to see the latest version."
  and does not auto-save
```

## Good vs. Bad Requirements Examples

### ❌ Bad (ambiguous, not testable)

```markdown
# Bad: unclear what to display
WHEN the user registers THEN it is registered

# Bad: error message undefined
WHEN input is invalid THEN display an error

# Bad: condition is too compound
WHEN the user logs in and checks permissions and selects data and edits and saves THEN success
```

### ✅ Good (clear, testable)

```markdown
# Good: specific expected behavior
WHEN the user enters {name} and {category} and clicks the register button
THEN the system registers the data and navigates to the "List" screen,
     and the registered data appears at the top of the list

# Good: error message is clear
WHEN the user submits with {name} empty
THEN the system displays "Name is required" in red below the name field
     and the screen does not navigate

# Good: 1 condition, 1 result
WHEN the user clicks "Delete" in the "Confirm Deletion" dialog
THEN the system logically deletes the target data (is_deleted = true) and removes it from the list
```

## requirements.md Completion Criteria

- [ ] Happy path (1 action, 1 THEN granularity) is fully covered
- [ ] Validation error messages for each required field are specific
- [ ] Optimistic lock conflict error message is described
- [ ] Show/hide requirements based on role/permission are specified
- [ ] Boundary value behaviors (0 items, pagination) are described
- [ ] Each requirement is at a granularity that "can be converted to test code"
