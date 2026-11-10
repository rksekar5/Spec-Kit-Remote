# Implementation Plan: Task Search and Status Filters
**Branch**: `001-task-search` | **Date**: 2026-11-10 | **Spec**: [spec.md](spec.md)

## Summary
Extend the existing list command with optional search and status flags. Filter status with bound
SQLite parameters and title with Python casefold substring matching; preserve schema and ordering.

## Technical Context
**Language/Version**: Python 3.11+  
**Primary Dependencies**: Standard library only  
**Storage**: Existing SQLite tasks table; no migrations  
**Testing**: unittest, subprocess CLI integration, temporary databases  
**Target Platform**: Local Python runtime; verified on Linux  
**Project Type**: CLI  
**Performance Goals**: Filter 10,000 tasks in under 1 second  
**Constraints**: No network, no runtime dependencies; existing commands remain compatible  
**Scale/Scope**: Single user, up to 10,000 tasks

## Constitution Check
Pre-research and post-design: PASS for all five principles. Single module and standard library;
backward-compatible defaults; automated acceptance tests; bound SQL and no migration; evidence
records distinguish local test results from GitHub integration limitations.

## Project Structure
- `tasks.py`: existing storage helpers and argparse CLI; extend list_tasks and list arguments.
- `tests/test_tasks.py`: retain baseline tests.
- `tests/test_search.py`: behavioral, persistence, performance, and subprocess tests.
- `scripts/demo.sh`: repeatable virtual run using a temporary database.
- `README.md`: setup, commands, feature and evidence links.
- `specs/001-task-search/`: spec, plan, research, data-model, contracts/cli.md, quickstart,
  tasks, checklists and verification report.
- `docs/workflow.md`: exact tool version, commands, skill execution ledger, limitations.

**Structure Decision**: Keep one application module; do not introduce frameworks or layers.

## Phases
0. Research literal Unicode matching, SQL safety, and legacy compatibility.
1. Define data model and CLI contract, then review requirements.
2. Generate tasks, analyze coverage, write failing tests, implement, run demo, and converge.

## Complexity Tracking
No violations. Linear title filtering is intentional at the stated local dataset size.
