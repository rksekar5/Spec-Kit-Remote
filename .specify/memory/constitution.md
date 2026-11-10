# Legacy Tasks Constitution

## Core Principles

### I. Simplicity
The application MUST use Python 3.11+ and the standard library only. Keep a single CLI module.

### II. Compatibility
Existing add, list, and done commands and persisted task records MUST continue to work.

### III. Verifiable behavior
Feature requirements MUST have automated acceptance tests, including invalid inputs and persistence.

### IV. Data integrity
Queries MUST bind user values as parameters. Search MUST be read-only and require no migration.

### V. Honest evidence
Documentation MUST distinguish executed checks from unavailable integrations and assumptions.

## Scope Constraints
A local, single-user command-line demonstration; no authentication, web server, or production hosting.

## Development Workflow
Write the spec, plan, and tasks before implementing the feature. Review requirements and converge
against the final code. Preserve a separately runnable baseline commit.

## Governance
Amendments require a written rationale and semantic version increment. Review these principles
at planning and convergence. Initial adoption establishes version 1.0.0; no deferred placeholders.

**Version**: 1.0.0 | **Ratified**: 2026-11-10 | **Last Amended**: 2026-11-10
