# Quickstart
Python 3.11+, no install required. Use a temporary directory so existing user data is untouched.
```sh
demo_dir=$(mktemp -d)
python3 tasks.py --db "$demo_dir/demo.db" add 'Review invoice'
python3 tasks.py --db "$demo_dir/demo.db" done 1
python3 tasks.py --db "$demo_dir/demo.db" reopen 1
python3 tasks.py --db "$demo_dir/demo.db" list --search invoice --status open --json
python3 -m unittest discover -s tests -v
```
Expected: `Reopened task 1.` and one open task with ID 1 and the original title.
