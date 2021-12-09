from flask import *
import json
import os
from Database import *

with open('config.json', 'r') as f:
    config = json.load(f)

version = config['version']

Database = Database(config['path'])
app = Flask(__name__)


@app.route('/')
def index():
    return config

@app.route('/create/<collection>', methods=['GET','POST'])
def create(collection):
    if collection in Database.collections:
        return json.dumps({'error': 'Collection already exists'})

    Database.createCollection(collection)
    return json.dumps({'success': 'Collection created'})

@app.route('/load/<collection>', methods=['GET','POST'])
def load(collection):
    if collection not in Database.collections:
        return json.dumps({'error': 'Collection does not exist'})

    return str(Database.loadCollection(collection))

@app.route('/save/<collection>', methods=['GET','POST'])
def save(collection):
    if collection not in Database.collections:
        return json.dumps({'error': 'Collection does not exist'})

    Database.saveCollection(collection)
    return json.dumps({'success': 'Collection saved'})

@app.route('/add/<collection>', methods=['GET','POST'])
def add(collection):
    if collection not in Database.collections:
        return json.dumps({'error': 'Collection does not exist'})

    data = request.get_json()
    Database.add_to_collection(collection, data)
    return json.dumps({'success': 'Data added'})

@app.route('/remove/<collection>', methods=['GET','POST'])
def remove(collection):
    if collection not in Database.collections:
        return json.dumps({'error': 'Collection does not exist'})

    data = request.get_json()
    Database.remove_from_collection(collection, data)
    return json.dumps({'success': 'Data removed'})

@app.route('/delete/<collection>', methods=['GET','POST'])
def delete(collection):
    if collection not in Database.collections:
        return json.dumps({'error': 'Collection does not exist'})

    Database.deleteCollection(collection)
    return json.dumps({'success': 'Collection deleted'})


app.run()