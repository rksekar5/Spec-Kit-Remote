# CLI Contract
```text
python3 tasks.py [--db PATH] add TITLE
python3 tasks.py [--db PATH] done ID
python3 tasks.py [--db PATH] list [--search TEXT] [--status {all,open,done}] [--json]
```
Default database is `tasks.db` in current directory. Global --db precedes the subcommand.
Default search is empty and status is all. Search is trimmed, literal, Unicode casefolded.
No accent removal or Unicode normalization. Both filters combine with AND.

Success exits 0. List output: right-aligned ID, two spaces, `[status] title`, one task per line.
No matches prints `No tasks found.`. JSON outputs an array with id (integer), title and status
(strings), including `[]` for no matches. Ordering is ascending ID.
Invalid arguments/status exit 2 on stderr, with argparse choices/help. Storage errors also exit 2.
Existing DB records remain unchanged by listing. A missing DB is created as in the baseline.
