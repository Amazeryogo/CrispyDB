import unittest
import os
import shutil
from crispydb.db import CrispyDB

class TestCrispyDB(unittest.TestCase):
    def setUp(self):
        self.db_path = 'test_db'
        if os.path.exists(self.db_path):
            shutil.rmtree(self.db_path)
        self.crispy = CrispyDB(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            shutil.rmtree(self.db_path)

    def test_create_and_get_db(self):
        db = self.crispy.db('my_db')
        self.assertTrue(os.path.isdir(os.path.join(self.db_path, 'my_db')))
        self.assertIn('my_db', self.crispy.dbs)

    def test_delete_db(self):
        self.crispy.db('my_db_to_delete')
        self.assertTrue(self.crispy.delete_db('my_db_to_delete'))
        self.assertFalse(os.path.exists(os.path.join(self.db_path, 'my_db_to_delete')))
        self.assertNotIn('my_db_to_delete', self.crispy.dbs)

    def test_create_and_get_table(self):
        db = self.crispy.db('my_db')
        table = db.table('my_table')
        self.assertTrue(os.path.exists(os.path.join(self.db_path, 'my_db', 'my_table.json')))
        self.assertIn('my_table', db.tables)

    def test_delete_table(self):
        db = self.crispy.db('my_db')
        db.table('my_table_to_delete')
        self.assertTrue(db.delete_table('my_table_to_delete'))
        self.assertFalse(os.path.exists(os.path.join(self.db_path, 'my_db', 'my_table_to_delete.json')))
        self.assertNotIn('my_table_to_delete', db.tables)

    def test_add_and_search_data(self):
        db = self.crispy.db('my_db')
        table = db.table('my_table')
        table.add({'name': 'test', 'value': 1})
        table.add({'name': 'test2', 'value': 2})
        results = table.search({'name': 'test'})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['value'], 1)

    def test_update_data(self):
        db = self.crispy.db('my_db')
        table = db.table('my_table')
        table.add({'name': 'test', 'value': 1})
        table.update({'name': 'test'}, {'value': 2})
        results = table.search({'name': 'test'})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['value'], 2)

    def test_remove_data(self):
        db = self.crispy.db('my_db')
        table = db.table('my_table')
        table.add({'name': 'test', 'value': 1})
        table.remove({'name': 'test'})
        results = table.search({'name': 'test'})
        self.assertEqual(len(results), 0)

    def test_binary_storage(self):
        db = self.crispy.db('my_db')
        binary_data = b'test_binary_data'
        file_id = db.store_binary(binary_data)
        retrieved_data = db.retrieve_binary(file_id)
        self.assertEqual(binary_data, retrieved_data)

if __name__ == '__main__':
    unittest.main()
