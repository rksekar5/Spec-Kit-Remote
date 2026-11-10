# Quickstart Validation
Requires Python 3.11+, no installation.

```sh
python3 -m unittest discover -s tests -v
bash scripts/demo.sh
```

The demo uses a temporary database, adds two invoice tasks and one release task, completes the
first invoice task, then searches open invoice tasks. Expect only the second invoice task.
A search with no matches returns `[]`. The demo deletes only its own temporary directory.

Interactive examples:
```sh
python3 tasks.py add "Pay Invoice"
python3 tasks.py list --search invoice --status open
python3 tasks.py done 1
python3 tasks.py list --status done --json
```
See [CLI contract](contracts/cli.md) for exact outputs and errors.
