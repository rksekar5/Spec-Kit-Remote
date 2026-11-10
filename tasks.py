"""Small legacy task tracker. Python standard library only."""
import argparse
import json
import sqlite3
from contextlib import closing


def connect(path):
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open', 'done')))")
    db.commit()
    return db


def add_task(db, title):
    title = title.strip()
    if not title or len(title) > 200 or any(ord(c) < 32 or ord(c) == 127 for c in title):
        raise ValueError('Title must contain 1–200 characters without control characters.')
    with db:
        cursor = db.execute('INSERT INTO tasks(title) VALUES (?)', (title,))
    return cursor.lastrowid


def list_tasks(db, search='', status='all'):
    """Read tasks in legacy order with literal Unicode matching; no schema changes."""
    if status not in ('all', 'open', 'done'):
        raise ValueError('Status must be all, open, or done.')
    query = 'SELECT id, title, status FROM tasks'
    parameters = ()
    if status != 'all':
        query += ' WHERE status = ?'
        parameters = (status,)
    query += ' ORDER BY id'
    needle = search.strip().casefold()
    return [dict(row) for row in db.execute(query, parameters)
            if needle in row['title'].casefold()]


def complete_task(db, task_id):
    with db:
        cursor = db.execute("UPDATE tasks SET status = 'done' WHERE id = ?", (task_id,))
    if not cursor.rowcount:
        raise ValueError(f'Task {task_id} does not exist.')


def main(argv=None):
    parser = argparse.ArgumentParser(description='Legacy Tasks — a local task tracker')
    parser.add_argument('--db', default='tasks.db', help='SQLite database path (default: tasks.db)')
    commands = parser.add_subparsers(dest='command', required=True)
    add = commands.add_parser('add', help='Add a task')
    add.add_argument('title')
    listing = commands.add_parser('list', help='List tasks')
    listing.add_argument('--search', default='', help='Literal case-insensitive title fragment')
    listing.add_argument('--status', choices=('all', 'open', 'done'), default='all', help='Filter completion status')
    listing.add_argument('--json', action='store_true', help='Output a JSON array')
    done = commands.add_parser('done', help='Complete a task')
    done.add_argument('id', type=int)
    args = parser.parse_args(argv)
    try:
        with closing(connect(args.db)) as db:
            if args.command == 'add':
                print(f'Added task {add_task(db, args.title)}.')
            elif args.command == 'done':
                complete_task(db, args.id)
                print(f'Completed task {args.id}.')
            else:
                rows = list_tasks(db, search=args.search, status=args.status)
                if args.json:
                    print(json.dumps(rows, ensure_ascii=False))
                elif not rows:
                    print('No tasks found.')
                else:
                    for row in rows:
                        print(f"{row['id']:>4}  [{row['status']}] {row['title']}")
    except (ValueError, sqlite3.Error) as error:
        parser.exit(2, f'Error: {error}\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
