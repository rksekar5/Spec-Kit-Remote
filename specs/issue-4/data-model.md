# Data Model
Reuse tasks(id INTEGER PRIMARY KEY, title TEXT NOT NULL, status TEXT NOT NULL with open/done check).
No new fields or migration. Reopen maps done→open and open→open; title/ID and all other rows remain
unchanged. Missing IDs raise ValueError, rendered by the CLI as exit 2. Bind the ID parameter.
