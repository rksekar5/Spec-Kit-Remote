# Tasks: Task Search and Status Filters

## Phase 1: Setup
- [X] T001 Review legacy tests and ignore rules in tests/test_tasks.py and .gitignore (FR-005).

## Phase 2: Foundation
- [X] T002 Add failing acceptance tests in tests/test_search.py for FR-001–009 and SC-001–003.

## Phase 3: US1 — Title Search (P1)
Independent test: literal/Unicode/whitespace queries return exact IDs.
- [X] T003 [US1] Extend list_tasks in tasks.py with literal Unicode title matching (FR-001, FR-004, FR-008).

## Phase 4: US3 — Compatibility (P1)
Independent test: old database records, order, JSON and commands remain valid.
- [X] T004 [US3] Retain legacy defaults and empty/JSON output in tasks.py; verify tests/test_search.py (FR-005, FR-006, FR-009).

## Phase 5: US2 — Status Filters (P2)
Independent test: all/open/done and combined search; invalid status exits 2.
- [X] T005 [US2] Add parameterized status filtering and CLI search/status arguments in tasks.py (FR-002, FR-003, FR-007).

## Phase 6: Validation and Documentation
- [X] T006 Add scripts/demo.sh and feature usage to README.md; run end-to-end demo (SC-001, SC-003).
- [X] T007 Run tests and 10,000-task timing check; record evidence in specs/001-task-search/verification.md (SC-001–003).
- [X] T008 Document command provenance, skills and external limitations in docs/workflow.md (Constitution V).

## Dependencies and Strategy
T001 → T002 → T003 → T004 → T005 → T006 → T007 → T008.
MVP is US1. US3 preserves compatibility before status integration. All application edits share
one file, so implementation is sequential. After T005, documentation and demo preparation can
proceed independently. Tests precede implementation and must fail on the baseline.
