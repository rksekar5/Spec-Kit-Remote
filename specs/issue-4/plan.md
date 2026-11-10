# Implementation Plan: Reopen Task
**Branch**: codex/issue-4-reopen | **Date**: 2026-11-10 | **Spec**: [spec.md](spec.md)

## Summary
Add reopen_task(db, task_id) alongside complete_task, using a parameterized UPDATE and the same
rowcount/error convention. Add an argparse reopen subcommand with an integer ID and success message.

## Technical Context
Python 3.11+, sqlite3 and argparse; no dependencies. Existing file-backed SQLite schema.
Tests: unittest, temporary files, CLI subprocesses. Local single-user target. One primary-key update
per command; no new performance requirement or migration.

## Constitution Check
Before research and after design: all five principles pass. Keep one module and stdlib only;
preserve legacy defaults; add meaningful tests; bind IDs; report actual execution evidence.

## Project Structure
- tasks.py: add reopen_task and subcommand/dispatch.
- tests/test_reopen.py: state, persistence, invalid inputs, schema/data preservation and CLI integration.
- README.md: usage example.
- specs/issue-4/: specification, research, model, CLI contract, quickstart, checklists, tasks and execution logs.
No workflow, governance, dependency or credential changes in this feature PR.

## Phases
Research existing update semantics; define contract; generate tasks; test before implementation;
implement; run full suite/demo; assess convergence.

## Complexity Tracking
No deviations. Explicit small helper avoids refactoring the existing complete command.
