# CrispyDB

CrispyDB is a simple, file-based database that stores data in JSON format. It's designed to be easy to use and integrate into Python applications.

## Features

*   **Multiple Databases:** Manage multiple databases, each with its own set of collections.
*   **JSON-based:** Stores data in human-readable JSON files.
*   **Binary Data Storage:** Store and retrieve binary data, such as images and other files.
*   **Simple API:** An intuitive and easy-to-use API for interacting with the database.

## Installation

To install CrispyDB, you can clone this repository and install it in editable mode:

```bash
git clone https://github.com/Amazeryogo/Thought.git
cd Thought
pip install -e Crispylib
```

## Usage

Here's a simple example of how to use CrispyDB:

```python
from crispydb.db import CrispyDB

# Create a CrispyDB instance
crispy = CrispyDB('data')

# Get a database
db = crispy.db('my_database')

# Get a table
table = db.table('my_table')

# Add some data
table.add({'name': 'John Doe', 'age': 30})
table.add({'name': 'Jane Doe', 'age': 25})

# Search for data
results = table.search({'name': 'John Doe'})
print(results)
```

This will create a `data` directory in your project with the following structure:

```
data/
└── my_database/
    ├── my_table.json
    └── _bin/
```
