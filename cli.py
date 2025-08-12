import argparse
import requests
import json
import os
import sys

# Add the src directory to the python path to allow importing configman
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
import configman

# --- Configuration ---
# Load configuration to get API URL and master token
try:
    # Allow overriding API URL and Token with environment variables for testing
    default_url = f"http://{configman.config.get('host', '127.0.0.1')}:{configman.config.get('port', 5000)}"
    API_BASE_URL = os.environ.get('CRISPY_API_URL', default_url)
    default_token = configman.config.get('master_token', 'DEFAULT_MASTER_TOKEN')
    MASTER_TOKEN = os.environ.get('CRISPY_TOKEN', default_token)
except Exception as e:
    print(f"Error loading configuration: {e}")
    sys.exit(1)

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {MASTER_TOKEN}'
}

# --- Command Functions ---

def search_command(args):
    """Handles the 'search' command."""
    collection = args.collection
    try:
        query = json.loads(args.query)
    except json.JSONDecodeError:
        print("Error: Query must be a valid JSON string.")
        return

    url = f"{API_BASE_URL}/{collection}/search"
    try:
        response = requests.post(url, headers=HEADERS, json=query)
        response.raise_for_status()
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        if e.response is not None:
            print(f"Response: {e.response.text}")

def insert_command(args):
    """Handles the 'insert' command."""
    collection = args.collection
    try:
        document = json.loads(args.document)
    except json.JSONDecodeError:
        print("Error: Document must be a valid JSON string.")
        return

    url = f"{API_BASE_URL}/{collection}/insert"
    try:
        response = requests.post(url, headers=HEADERS, json=document)
        response.raise_for_status()
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        if e.response is not None:
            print(f"Response: {e.response.text}")

def update_command(args):
    """Handles the 'update' command."""
    collection = args.collection
    try:
        query = json.loads(args.query)
        update_spec = json.loads(args.update_spec)
    except json.JSONDecodeError:
        print("Error: Query and update_spec must be valid JSON strings.")
        return

    payload = {
        "query": query,
        "update_spec": update_spec,
        "multi": args.multi
    }
    url = f"{API_BASE_URL}/{collection}/update"
    try:
        response = requests.put(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        if e.response is not None:
            print(f"Response: {e.response.text}")

def remove_command(args):
    """Handles the 'remove' command."""
    collection = args.collection
    try:
        query = json.loads(args.query)
    except json.JSONDecodeError:
        print("Error: Query must be a valid JSON string.")
        return

    url = f"{API_BASE_URL}/{collection}/remove"
    try:
        response = requests.delete(url, headers=HEADERS, json=query)
        response.raise_for_status()
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        if e.response is not None:
            print(f"Response: {e.response.text}")

# --- Main Parser Setup ---

def main():
    parser = argparse.ArgumentParser(
        description="A command-line interface for the CrispyDB."
    )
    subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands')

    # --- Search Command Parser ---
    parser_search = subparsers.add_parser('search', help='Search for documents in a collection.')
    parser_search.add_argument('collection', type=str, help='The name of the collection to search in.')
    parser_search.add_argument('query', type=str, help='The search query in JSON format.')
    parser_search.set_defaults(func=search_command)

    # --- Insert Command Parser ---
    parser_insert = subparsers.add_parser('insert', help='Insert a document into a collection.')
    parser_insert.add_argument('collection', type=str, help='The name of the collection.')
    parser_insert.add_argument('document', type=str, help='The document to insert in JSON format.')
    parser_insert.set_defaults(func=insert_command)

    # --- Update Command Parser ---
    parser_update = subparsers.add_parser('update', help='Update documents in a collection.')
    parser_update.add_argument('collection', type=str, help='The name of the collection.')
    parser_update.add_argument('query', type=str, help='The search query in JSON format.')
    parser_update.add_argument('update_spec', type=str, help='The update specification in JSON format (e.g., \'{"$set": {"key": "value"}}\').')
    parser_update.add_argument('--multi', action='store_true', help='Update multiple documents. Defaults to false.')
    parser_update.set_defaults(func=update_command)

    # --- Remove Command Parser ---
    parser_remove = subparsers.add_parser('remove', help='Remove documents from a collection.')
    parser_remove.add_argument('collection', type=str, help='The name of the collection.')
    parser_remove.add_argument('query', type=str, help='The search query in JSON format.')
    parser_remove.set_defaults(func=remove_command)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
