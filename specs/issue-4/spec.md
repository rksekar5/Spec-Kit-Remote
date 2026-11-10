# Feature Specification: Reopen a Task
**Branch**: `codex/issue-4-reopen` | **Created**: 2026-11-10 | **Status**: Ready
**Input**: GitHub issue #4, reopen a completed task while preserving existing behavior.

## User Scenarios & Testing
### US1 — Resume completed work (P1)
As a task owner, I want to reopen a completed task without recreating it.
**Independent test**: Complete a task, reopen it, and start a fresh process to inspect it.
**Acceptance**:
- Given a completed task, when reopening its ID, then its status becomes open and persists.
- Given its title and ID, when reopening it, then both are unchanged and no task is duplicated.

### US2 — Safe repeated and invalid commands (P2)
As a task owner, I want predictable results when repeating a command or mistyping an ID.
**Independent test**: Reopen an open task twice and attempt nonexistent and malformed IDs.
**Acceptance**:
- Reopening an already-open task succeeds and preserves its data.
- A missing ID fails with code 2 and a clear message, without changing stored tasks.
- A noninteger ID fails with code 2 before opening or creating a database.

### US3 — Existing workflows remain compatible (P1)
As an existing user, I want add/list/done, searches, and machine-readable output to keep working.
**Independent test**: Run the existing suite and check a reopened task in open/done filtered lists.
**Acceptance**:
- The reopened task appears in matching open searches and disappears from done searches.
- Existing commands, output contracts, and records remain valid without migration.

### Edge Cases
Repeated reopen succeeds. Negative, zero, or nonexistent integer IDs are treated as missing IDs.
Empty databases have no matching ID. Invalid syntax uses the existing argument-error convention.
Existing storage errors keep the baseline behavior. The command changes only the specified task.

## Requirements
- **FR-001**: Users MUST reopen an existing completed task by its integer ID.
- **FR-002**: Reopening MUST preserve the task's ID/title, other tasks, schema, and stored row count.
- **FR-003**: Reopening an already-open task MUST succeed without duplicating or otherwise changing it.
- **FR-004**: Missing IDs MUST return exit code 2 and `Task ID does not exist.` with ID substituted;
  existing records MUST remain unchanged.
- **FR-005**: Noninteger IDs MUST return exit code 2 before database access.
- **FR-006**: A successful reopen MUST persist across application restarts, exit 0, and print `Reopened task ID.`.
- **FR-007**: Existing add/list/done, search/status filters, ascending order, and JSON shape MUST remain compatible.
- **FR-008**: The README MUST include a runnable reopen example.

### Key Entities
Existing Task: integer ID, title and status (open/done). New transition: done→open; open→open is idempotent.

## Success Criteria
- **SC-001**: Every listed acceptance scenario is covered by passing automated tests.
- **SC-002**: Existing regression tests and the demo pass without changing their expected behavior.
- **SC-003**: A user can reopen a completed task with one command and see its open status on the next listing.

## Assumptions and Scope
Local single-user CLI; no new dependencies, schema migration, workflow modifications or credentials.
This feature uses the existing database path and error conventions. Tests are required.

## Clarification Review
Scope, state transitions, persistence, errors, output, compatibility, and completion criteria are clear.
No critical unanswered questions. Numeric missing IDs retain the baseline policy; no new ID restrictions.
