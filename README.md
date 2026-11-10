# Legacy Tasks

A deliberately small legacy-style Python/SQLite command-line application.
Requires Python 3.11+; no application dependencies or services to install.

```sh
python3 tasks.py add "Pay invoice"
python3 tasks.py add "Review release"
python3 tasks.py list
python3 tasks.py done 1
python3 tasks.py list --json
python3 -m unittest discover -s tests -v
```

Data persists in `tasks.db` in the working directory. Select another file with
`python3 tasks.py --db /path/to/tasks.db list`. The parent directory must exist.
This is a local single-user demo, not a hosted or multi-user service.
