# Data Model
Existing `tasks`: `id INTEGER PRIMARY KEY`, `title TEXT NOT NULL`,
`status TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open', 'done'))`.
Titles are trimmed, 1–200 characters, with no ASCII control characters. IDs remain stable.
`add` creates open tasks. `done` changes open to done and is idempotent for existing done tasks.
Missing task IDs fail. No schema migration or additional persisted data.

Transient filter: search string (trimmed then Unicode casefolded), status (all/open/done).
All means no status predicate; both predicates otherwise combine with AND. Results ordered by ID.
