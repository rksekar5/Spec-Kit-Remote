# Tasks: Reopen Task
## Phase 1: Setup
- [X] T001 Review existing CLI/error/schema contracts in tasks.py and tests/test_tasks.py (FR-007).
## Phase 2: Acceptance tests
- [X] T002 Add and run failing tests in tests/test_reopen.py covering FR-001–007 and SC-001–003.
## Phase 3: US1 — Resume completed work
- [X] T003 [US1] Implement parameterized reopen_task and CLI dispatch in tasks.py (FR-001/002/006).
## Phase 4: US2 — Safe repeats and invalid IDs
- [X] T004 [US2] Match idempotent/missing/invalid conventions in tasks.py and verify tests/test_reopen.py (FR-003–005).
## Phase 5: US3 — Compatibility
- [X] T005 [US3] Run all tests and baseline demo; document results in specs/issue-4/execution.md (FR-007, SC-001–003).
## Phase 6: Documentation
- [X] T006 Add README.md example and actual evidence in specs/issue-4/execution.md (FR-008, Constitution V).

Dependencies: T001→T002→T003→T004→T005→T006. MVP is US1 with validation and persistence.
Implementation edits share tasks.py and remain sequential. README work can be prepared separately
after the contract is fixed. No parallel implementation agents are needed.
