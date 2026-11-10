# Research
Spec Kit's plan workflow requested a research agent; its findings were reviewed against tasks.py.
Decision: use a dedicated helper matching complete_task with a bound ID and SQLite transaction.
Rationale: minimal additive change, unchanged schema/error conventions. Generalizing both transitions
would add unrelated refactoring. SQLite UPDATE rowcount counts matched rows in this configuration;
idempotence is explicitly tested so an already-open task cannot be mistaken for a missing task.
Alternative: SELECT then UPDATE is unnecessary here. Validate integer syntax in argparse before DB
access; allow zero/negative integers to follow baseline missing-ID semantics. Tests use actual files
and fresh subprocesses, proving persistence and unchanged legacy contracts. No unresolved research.
