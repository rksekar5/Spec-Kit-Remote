# Feature Specification: Task Search and Status Filters

**Feature Branch**: `001-task-search`  
**Created**: 2026-11-10  
**Status**: Ready for planning  
**Input**: Add title search and status filtering to the existing local task tracker.

## User Scenarios & Testing

### User Story 1 - Find tasks by title (Priority: P1)
As a task owner, I want to find tasks by a remembered title fragment.
**Independent Test**: Search a mixed-title list and compare the exact returned IDs.
**Acceptance Scenarios**:
1. Given `Pay Invoice` and `Review release`, when searching ` INVOICE `, then only `Pay Invoice` appears.
2. Given `Straße repair`, when searching `STRASSE`, then that task appears.
3. Given titles containing `%`, `_`, or quotes, when searching these characters, then they match literally.

### User Story 2 - Focus by completion status (Priority: P2)
As a task owner, I want open or completed tasks and optionally a title fragment.
**Independent Test**: Create two matching tasks, complete one, and verify each status selection.
**Acceptance Scenarios**:
1. Given open and done tasks, when selecting each status, then only that status appears.
2. Given several matching titles, when combining title and status, then both conditions must match.
3. Given an unsupported status, when listing, then an actionable error appears with failure code 2.

### User Story 3 - Preserve existing workflows (Priority: P1)
As an existing user, I want my stored tasks and existing commands to keep working.
**Independent Test**: Open an existing database, list without filters, add and complete tasks, and reopen it.
**Acceptance Scenarios**:
1. Given existing tasks, when listing without filters, then all tasks appear in ascending ID order.
2. Given no matches or no tasks, when listing, then a clear empty message or empty machine-readable list appears with success code 0.
3. Given existing data, when searching repeatedly, then task records and stored status remain unchanged.

### Edge Cases
Empty/whitespace search means no title restriction. Leading/trailing search whitespace is ignored.
Matching ignores Unicode case, but not accents or canonical normalization. Literal search has no
wildcard syntax. An unknown status is rejected before opening the database. A missing database is
initialized as the baseline does; missing parent directories produce an error. No migration is needed.

## Requirements

### Functional Requirements
- **FR-001**: Users MUST search titles by a literal, Unicode case-insensitive substring.
- **FR-002**: Users MUST select `all`, `open`, or `done`; default is `all`.
- **FR-003**: Search and status MUST combine using AND.
- **FR-004**: Empty/whitespace search MUST mean no restriction; surrounding whitespace MUST be trimmed.
- **FR-005**: Unfiltered listing, add, completion, persistent records, and ascending ID order MUST remain compatible.
- **FR-006**: Valid empty results MUST succeed and show `No tasks found.` or `[]` in machine-readable mode.
- **FR-007**: Unsupported status MUST return code 2, explain valid choices, and leave existing records unchanged.
- **FR-008**: Searching MUST not modify existing records or interpret input as executable query syntax.
- **FR-009**: Machine-readable output MUST preserve the array of objects with `id`, `title`, and `status`.

### Key Entities
- **Task**: Unique integer ID, title, completion status (`open` or `done`).
- **Filter**: Optional title fragment and status selection; not persisted.

## Success Criteria
- **SC-001**: All listed acceptance scenarios pass automated tests.
- **SC-002**: A filtered listing of 10,000 local tasks completes within 1 second in the development environment.
- **SC-003**: Existing records and legacy command results remain unchanged after read-only searches.

## Assumptions and Scope
Single-user local command-line application; English help and messages; Unicode titles. No web UI,
accounts, remote sync, pagination, fuzzy matching, or production hosting. Target at most 10,000 tasks.
The user delegated feature and implementation choices. Automated tests are required for this feature.

## Clarification Review — 2026-11-10
No critical ambiguities detected. Scope, data model, interaction, errors, performance, constraints,
terminology, and completion signals are clear. External integrations are not part of runtime behavior.
No user questions were needed; defaults above are design decisions, not user-provided answers.
