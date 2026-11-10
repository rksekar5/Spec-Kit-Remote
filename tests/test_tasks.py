import tempfile
import unittest
from pathlib import Path
import tasks


class LegacyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / 'tasks.db'
        self.db = tasks.connect(self.path)

    def tearDown(self):
        self.db.close()
        self.temp.cleanup()

    def test_add_list_done_persist(self):
        task_id = tasks.add_task(self.db, '  Pay invoice  ')
        self.assertEqual(tasks.list_tasks(self.db), [{'id': task_id, 'title': 'Pay invoice', 'status': 'open'}])
        tasks.complete_task(self.db, task_id)
        self.db.close()
        self.db = tasks.connect(self.path)
        self.assertEqual(tasks.list_tasks(self.db)[0]['status'], 'done')

    def test_invalid_title_and_missing_task(self):
        for title in ['', '  ', 'a' * 201, 'line\nbreak']:
            with self.assertRaises(ValueError):
                tasks.add_task(self.db, title)
        with self.assertRaises(ValueError):
            tasks.complete_task(self.db, 999)


if __name__ == '__main__':
    unittest.main()
