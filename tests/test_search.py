import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest
import tasks

APP = Path(__file__).resolve().parents[1] / 'tasks.py'


class SearchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / 'legacy.db'
        self.db = tasks.connect(self.path)
        for title in ['Pay Invoice', 'Review invoice', 'Release notes', 'Straße repair', '100%_complete', "O'Brien"]:
            tasks.add_task(self.db, title)
        tasks.complete_task(self.db, 1)

    def tearDown(self):
        self.db.close()
        self.temp.cleanup()

    def ids(self, **kwargs):
        return [row['id'] for row in tasks.list_tasks(self.db, **kwargs)]

    def cli(self, *args):
        return subprocess.run([sys.executable, str(APP), '--db', str(self.path), *args], capture_output=True, text=True)

    def test_literal_case_and_whitespace(self):
        self.assertEqual(self.ids(search=' INVOICE '), [1, 2])
        self.assertEqual(self.ids(search='strasse'), [4])
        self.assertEqual(self.ids(search='%'), [5])
        self.assertEqual(self.ids(search='_'), [5])
        self.assertEqual(self.ids(search="'"), [6])
        self.assertEqual(self.ids(search="' OR 1=1 --"), [])
        self.assertEqual(self.ids(search=''), list(range(1, 7)))
        self.assertEqual(self.ids(search='  '), list(range(1, 7)))

    def test_status_and_combination(self):
        self.assertEqual(self.ids(status='all'), list(range(1, 7)))
        self.assertEqual(self.ids(status='done'), [1])
        self.assertEqual(self.ids(status='open'), list(range(2, 7)))
        self.assertEqual(self.ids(search='invoice', status='open'), [2])
        self.assertEqual(self.ids(search='invoice', status='done'), [1])
        with self.assertRaises(ValueError):
            self.ids(status='bad')

    def test_read_only_legacy_schema_and_persistence(self):
        before = list(self.db.iterdump())
        self.ids(search='invoice', status='done')
        self.assertEqual(before, list(self.db.iterdump()))
        self.db.close()
        self.db = tasks.connect(self.path)
        self.assertEqual(self.ids(), list(range(1, 7)))
        self.assertEqual(self.ids(status='done'), [1])

    def test_cli_json_and_legacy(self):
        result = self.cli('list', '--search', 'invoice', '--status', 'open', '--json')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), [{'id': 2, 'title': 'Review invoice', 'status': 'open'}])
        self.assertEqual(len(json.loads(self.cli('list', '--json').stdout)), 6)
        self.assertEqual(self.cli('add', 'Follow up').returncode, 0)
        self.assertEqual(self.cli('done', '7').returncode, 0)
        self.assertIn('[done] Follow up', self.cli('list').stdout)

    def test_empty_results(self):
        for args, expected in [((), 'No tasks found.'), (('--json',), '[]')]:
            result = self.cli('list', '--search', 'missing', *args)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout.strip(), expected)
        self.db.execute('DELETE FROM tasks')
        self.db.commit()
        self.assertEqual(self.cli('list', '--json').stdout.strip(), '[]')

    def test_invalid_status_is_nonmutating(self):
        before = list(self.db.iterdump())
        result = self.cli('list', '--status', 'invalid')
        self.assertEqual(result.returncode, 2)
        self.assertIn('invalid choice', result.stderr)
        self.assertIn('open', result.stderr)
        self.assertEqual(list(self.db.iterdump()), before)

    def test_10000_task_search(self):
        with self.db:
            self.db.execute('DELETE FROM tasks')
            self.db.executemany('INSERT INTO tasks(title) VALUES (?)', [(f'Invoice {i}',) for i in range(10000)])
        start = time.perf_counter()
        result = self.cli('list', '--search', 'invoice 9999', '--status', 'open', '--json')
        elapsed = time.perf_counter() - start
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)), 1)
        self.assertLess(elapsed, 1.0)
        print(f'10,000-task CLI search: {elapsed:.3f}s')


if __name__ == '__main__':
    unittest.main()
