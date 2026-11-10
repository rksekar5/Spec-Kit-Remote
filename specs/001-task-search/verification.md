# Verification Evidence

Executed 2026-11-10 in the managed Linux environment, Python 3.12.

## Red / Green
The original baseline passed 2 regression tests. With the feature acceptance tests added but before
implementation, 9 tests ran with 4 failures and 3 errors: the new flags and function parameters did
not exist. After implementation, all 9 tests passed.

## Executed test output
```text
test_10000_task_search (test_search.SearchTests.test_10000_task_search) ... ok
test_cli_json_and_legacy (test_search.SearchTests.test_cli_json_and_legacy) ... ok
test_empty_results (test_search.SearchTests.test_empty_results) ... ok
test_invalid_status_is_nonmutating (test_search.SearchTests.test_invalid_status_is_nonmutating) ... ok
test_literal_case_and_whitespace (test_search.SearchTests.test_literal_case_and_whitespace) ... ok
test_read_only_legacy_schema_and_persistence (test_search.SearchTests.test_read_only_legacy_schema_and_persistence) ... ok
test_status_and_combination (test_search.SearchTests.test_status_and_combination) ... ok
test_add_list_done_persist (test_tasks.LegacyTests.test_add_list_done_persist) ... ok
test_invalid_title_and_missing_task (test_tasks.LegacyTests.test_invalid_title_and_missing_task) ... ok

----------------------------------------------------------------------
Ran 9 tests in 0.367s

OK
10,000-task CLI search: 0.029s
```

## Virtual CLI demo
Command: `bash scripts/demo.sh`. Uses a fresh temporary SQLite database.
```text
Added task 1.
Added task 2.
Added task 3.
Completed task 1.
[{"id": 2, "title": "Review invoice", "status": "open"}]
[]
```

## Coverage
| Requirements | Evidence |
|---|---|
| FR-001, FR-004, FR-008 | Literal case/Unicode/whitespace, quotes/wildcards/SQL-looking strings; unchanged database dump |
| FR-002, FR-003 | Individual status and combined predicates |
| FR-005, FR-009 | Legacy commands, ascending IDs, persisted data and JSON contract |
| FR-006 | Empty database and no-match text/JSON with success exits |
| FR-007 | Invalid status exit 2, valid choices in stderr, unchanged stored data |
| SC-001, SC-003 | Full test suite and real CLI subprocess/demo runs |
| SC-002 | 10,000-row CLI search completed in 0.029 seconds on this environment |

No browser test applies: this is a command-line application with no web UI.
Performance is one local measurement, not a cross-platform or production guarantee.
GitHub Project creation remains blocked by integration permissions, independently of application behavior.
