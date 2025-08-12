import unittest
import os
import shutil
import sys
import requests
import json
import subprocess
from threading import Thread
from werkzeug.serving import make_server

# Add the src directory to the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from __init__ import app, init_db
import configman

# --- Configuration for testing ---
TEST_HOST = '127.0.0.1'
TEST_PORT = 5001
API_BASE_URL = f"http://{TEST_HOST}:{TEST_PORT}"
TEST_COLLECTION = 'test_integration_coll'
TEST_DATA_DIR = 'temp_integration_test_data'

# Set a master token for testing and define headers
TEST_MASTER_TOKEN = 'TEST_MASTER_TOKEN'
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {TEST_MASTER_TOKEN}'
}

class ServerThread(Thread):
    def __init__(self, app):
        Thread.__init__(self)
        self.server = make_server(TEST_HOST, TEST_PORT, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()

class TestIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the test environment and start the API server."""
        app.config['TESTING'] = True
        app.config['DB_PATH'] = TEST_DATA_DIR
        app.config['MASTER_TOKEN'] = TEST_MASTER_TOKEN

        # Ensure the test data directory is clean
        if os.path.exists(TEST_DATA_DIR):
            shutil.rmtree(TEST_DATA_DIR)
        os.makedirs(TEST_DATA_DIR)

        init_db()

        # Start the Flask server in a background thread
        cls.server_thread = ServerThread(app)
        cls.server_thread.start()
        import time
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        """Shut down the server and clean up."""
        cls.server_thread.shutdown()
        shutil.rmtree(TEST_DATA_DIR)

    def setUp(self):
        """Clean the test collection before each test by removing all documents."""
        # Use the API to remove all documents from the test collection
        requests.delete(f"{API_BASE_URL}/{TEST_COLLECTION}/remove", headers=HEADERS, json={})

    def test_api_insert(self):
        """Test inserting a document via the API."""
        url = f"{API_BASE_URL}/{TEST_COLLECTION}/insert"
        doc = {'name': 'test_doc', 'value': 123}
        response = requests.post(url, headers=HEADERS, json=doc)

        self.assertEqual(response.status_code, 201, msg=f"API Error: {response.text}")
        self.assertIn('success', response.json())

    def test_api_search(self):
        """Test searching for a document via the API."""
        # First, insert a document to search for
        requests.post(f"{API_BASE_URL}/{TEST_COLLECTION}/insert", headers=HEADERS, json={'name': 'search_me', 'value': 456})

        url = f"{API_BASE_URL}/{TEST_COLLECTION}/search"
        query = {'name': 'search_me'}
        response = requests.post(url, headers=HEADERS, json=query)

        self.assertEqual(response.status_code, 200, msg=f"API Error: {response.text}")
        results = response.json()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['value'], 456)

    def test_api_update(self):
        """Test updating a document via the API."""
        requests.post(f"{API_BASE_URL}/{TEST_COLLECTION}/insert", headers=HEADERS, json={'name': 'update_me', 'value': 111})

        url = f"{API_BASE_URL}/{TEST_COLLECTION}/update"
        payload = {
            'query': {'name': 'update_me'},
            'update_spec': {'$set': {'value': 999}}
        }
        response = requests.put(url, headers=HEADERS, json=payload)

        self.assertEqual(response.status_code, 200, msg=f"API Error: {response.text}")
        self.assertIn('Updated 1 document(s)', response.json()['success'])

    def test_api_remove(self):
        """Test removing a document via the API."""
        requests.post(f"{API_BASE_URL}/{TEST_COLLECTION}/insert", headers=HEADERS, json={'name': 'delete_me'})

        url = f"{API_BASE_URL}/{TEST_COLLECTION}/remove"
        query = {'name': 'delete_me'}
        response = requests.delete(url, headers=HEADERS, json=query)

        self.assertEqual(response.status_code, 200, msg=f"API Error: {response.text}")
        self.assertIn('Removed 1 document(s)', response.json()['success'])

    def test_cli_search(self):
        """Test the CLI search command."""
        requests.post(f"{API_BASE_URL}/{TEST_COLLECTION}/insert", headers=HEADERS, json={'name': 'cli_search_me'})

        env = os.environ.copy()
        env['CRISPY_API_URL'] = API_BASE_URL
        env['CRISPY_TOKEN'] = TEST_MASTER_TOKEN

        query_json = '{"name": "cli_search_me"}'
        result = subprocess.run(
            ['python', 'cli.py', 'search', TEST_COLLECTION, query_json],
            capture_output=True, text=True, env=env
        )
        self.assertEqual(result.returncode, 0, msg=f"CLI Error: {result.stderr}")
        self.assertIn('cli_search_me', result.stdout)


if __name__ == '__main__':
    unittest.main()
