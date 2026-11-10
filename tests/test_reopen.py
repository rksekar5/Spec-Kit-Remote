"""Acceptance coverage for issue #4 using real SQLite files and CLI processes."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import tasks

APP = Path(__file__).resolve().parents[1] / 'tasks.py'


class ReopenTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / 'tasks.db'
        self.db = tasks.connect(self.path)
        self.first = tasks.add_task(self.db, 'Review invoice')
        self.second = tasks.add_task(self.db, 'Unrelated task')
        tasks.complete_task(self.db, self.first)

    def tearDown(self):
        self.db.close()
        self.temp.cleanup()

    def cli(self, *args, path=None):
        return subprocess.run([sys.executable, str(APP), '--db', str(path or self.path), *args],
                              capture_output=True, text=True)

    def snapshot(self):
        return list(self.db.iterdump())

    def test_reopen_persists_and_preserves_identity_schema_and_others(self):
        before = tasks.list_tasks(self.db)
        schema = self.db.execute("SELECT sql FROM sqlite_master WHERE type='table'").fetchall()
        result = self.cli('reopen', str(self.first))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, f'Reopened task {self.first}.\n')
        self.assertEqual(result.stderr, '')
        expected = [dict(row) for row in before]
        expected[0]['status'] = 'open'
        self.assertEqual(json.loads(self.cli('list', '--json').stdout), expected)
        self.assertEqual(self.db.execute("SELECT sql FROM sqlite_master WHERE type='table'").fetchall(), schema)

    def test_open_task_can_be_reopened_twice_without_changes(self):
        before = self.snapshot()
        for _ in range(2):
            result = self.cli('reopen', str(self.second))
            self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.snapshot(), before)

    def test_missing_ids_fail_without_mutation(self):
        before = self.snapshot()
        for task_id in ['0', '-1', '999', str(2**63), str(-(2**63)-1)]:
            with self.subTest(task_id=task_id):
                result = self.cli('reopen', task_id)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, '')
                self.assertEqual(result.stderr, f'Error: Task {task_id} does not exist.\n')
                self.assertEqual(self.snapshot(), before)

    def test_invalid_id_is_rejected_before_creating_database(self):
        path = Path(self.temp.name) / 'must-not-exist.db'
        result = self.cli('reopen', 'abc', path=path)
        self.assertEqual(result.returncode, 2)
        self.assertIn('invalid int value', result.stderr)
        self.assertNotIn('Traceback', result.stderr)
        self.assertFalse(path.exists())

    def test_empty_database_reports_missing_id(self):
        with self.db:
            self.db.execute('DELETE FROM tasks')
        before = self.snapshot()
        result = self.cli('reopen', '1')
        self.assertEqual(result.returncode, 2)
        self.assertIn('Task 1 does not exist.', result.stderr)
        self.assertEqual(self.snapshot(), before)

    def test_filters_and_done_after_reopen_remain_compatible(self):
        self.assertEqual(self.cli('reopen', str(self.first)).returncode, 0)
        opened = self.cli('list', '--search', 'INVOICE', '--status', 'open', '--json')
        self.assertEqual(json.loads(opened.stdout), [
            {'id': self.first, 'title': 'Review invoice', 'status': 'open'}])
        self.assertEqual(json.loads(self.cli('list', '--status', 'done', '--json').stdout), [])
        self.assertEqual(self.cli('done', str(self.first)).returncode, 0)
        self.assertEqual(json.loads(self.cli('list', '--status', 'done', '--json').stdout)[0]['id'], self.first)


if __name__ == '__main__':
    unittest.main()
