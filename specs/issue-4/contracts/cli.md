# CLI Contract
`python3 tasks.py [--db PATH] reopen ID`
- ID is parsed by argparse as an integer. Bad syntax: stderr usage, exit 2, no DB access.
- Existing done/open row: status open, stdout `Reopened task ID.`, exit 0.
- Missing integer ID: stderr `Error: Task ID does not exist.`, exit 2.
- Existing SQLite error handling and default tasks.db path remain unchanged.
- A nonexistent database file is initialized by baseline connect(); the missing-ID command then fails.
- Reopening does not modify schema, identity, title, row count, or unrelated rows.
