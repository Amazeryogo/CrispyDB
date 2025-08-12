import unittest
import os
import shutil
import sys

# Add the src directory to the Python path to allow importing CrispyDB modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.collection import Collection

class TestCollection(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory and a collection for each test."""
        self.test_dir = "temp_test_data"
        os.makedirs(self.test_dir, exist_ok=True)
        self.collection = Collection(path=self.test_dir, name="test_users")

        # Initial data for the tests
        self.users_data = [
            {'name': 'Alice', 'age': 30, 'city': 'New York', 'tags': ['developer', 'python']},
            {'name': 'Bob', 'age': 25, 'city': 'Los Angeles', 'tags': ['designer', 'javascript']},
            {'name': 'Charlie', 'age': 35, 'city': 'New York', 'tags': ['manager', 'leadership']},
            {'name': 'David', 'age': 30, 'city': 'Chicago', 'tags': ['developer', 'java']},
        ]
        # Use a copy of the list to avoid modifying the original during tests
        self.collection.data = list(self.users_data)
        self.collection.save()

    def tearDown(self):
        """Clean up the temporary directory after each test."""
        shutil.rmtree(self.test_dir)

    def test_search_exact_match(self):
        """Test searching for an exact document."""
        results = self.collection.search({'name': 'Alice'})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['age'], 30)

    def test_search_gt_operator(self):
        """Test the '$gt' (greater than) operator."""
        results = self.collection.search({'age': {'$gt': 30}})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], 'Charlie')

    def test_search_gte_operator(self):
        """Test the '$gte' (greater than or equal to) operator."""
        results = self.collection.search({'age': {'$gte': 30}})
        self.assertEqual(len(results), 3)

    def test_search_lt_operator(self):
        """Test the '$lt' (less than) operator."""
        results = self.collection.search({'age': {'$lt': 30}})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], 'Bob')

    def test_search_lte_operator(self):
        """Test the '$lte' (less than or equal to) operator."""
        results = self.collection.search({'age': {'$lte': 30}})
        self.assertEqual(len(results), 3)

    def test_search_ne_operator(self):
        """Test the '$ne' (not equal) operator."""
        results = self.collection.search({'city': {'$ne': 'New York'}})
        self.assertEqual(len(results), 2)

    def test_search_in_operator(self):
        """Test the '$in' operator for lists."""
        results = self.collection.search({'tags': {'$in': ['python', 'java']}})
        self.assertEqual(len(results), 2)

    def test_search_nin_operator(self):
        """Test the '$nin' (not in) operator for lists."""
        results = self.collection.search({'tags': {'$nin': ['python', 'java']}})
        self.assertEqual(len(results), 2)

    def test_search_and_operator(self):
        """Test the '$and' operator."""
        query = {'$and': [{'city': 'New York'}, {'age': {'$lt': 35}}]}
        results = self.collection.search(query)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], 'Alice')

    def test_search_or_operator(self):
        """Test the '$or' operator."""
        query = {'$or': [{'city': 'Los Angeles'}, {'age': 35}]}
        results = self.collection.search(query)
        self.assertEqual(len(results), 2)

    def test_update_single_document(self):
        """Test updating a single document with '$set'."""
        query = {'name': 'Alice'}
        update_spec = {'$set': {'age': 31, 'city': 'Boston'}}
        updated_count = self.collection.update(query, update_spec)
        self.assertEqual(updated_count, 1)

        # Verify the update
        results = self.collection.search({'name': 'Alice'})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['age'], 31)
        self.assertEqual(results[0]['city'], 'Boston')

    def test_update_multiple_documents(self):
        """Test updating multiple documents with 'multi=True'."""
        query = {'city': 'New York'}
        update_spec = {'$set': {'city': 'NYC'}}
        updated_count = self.collection.update(query, update_spec, multi=True)
        self.assertEqual(updated_count, 2)

        # Verify the update
        results = self.collection.search({'city': 'NYC'})
        self.assertEqual(len(results), 2)

    def test_remove_single_document(self):
        """Test removing a single document."""
        query = {'name': 'David'}
        removed_count = self.collection.remove(query)
        self.assertEqual(removed_count, 1)
        self.assertEqual(len(self.collection.data), 3)

    def test_remove_multiple_documents(self):
        """Test removing multiple documents matching a query."""
        query = {'city': 'New York'}
        removed_count = self.collection.remove(query)
        self.assertEqual(removed_count, 2)
        self.assertEqual(len(self.collection.data), 2)

    def test_remove_all_documents(self):
        """Test removing all documents with an empty query."""
        removed_count = self.collection.remove({})
        self.assertEqual(removed_count, 4)
        self.assertEqual(len(self.collection.data), 0)

if __name__ == '__main__':
    unittest.main()
