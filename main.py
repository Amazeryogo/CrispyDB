from flask import *
import json
import os
from core import *
import sys
import platform
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

with open('config/config.json', 'r') as f:
    config = json.load(f)


    

with open('config/admin.json', 'r') as f:
    admin = json.load(f)


request_per_minutes = config['rpm']
collection_creation_per_minute = config['ccpm']
ccpm = str(collection_creation_per_minute) + ' per minute'
collection_deletion_per_minute = config['cdpm']
cdpm = str(collection_deletion_per_minute) + ' per minute'
rpm = request_per_minutes
rpm = str(rpm) + " per minute"
version = config['version']
python_version = config['python version']

if python_version != platform.python_version():
    print("Python version mismatch")
    sys.exit(1)

Database = Database(config['path'])
app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=[rpm]
)



@app.route('/')
def index():
    return config

@app.route('/create/<collection>', methods=['GET','POST'])
@limiter.limit(ccpm)
def create(collection):
    auth = request.authorization
    if auth:
        if auth.username == admin['username'] and auth.password == admin['password']:
            if collection in Database.collections:
                return json.dumps({'error': 'Collection already exists'})

            Database.createCollection(collection)
            return json.dumps({'success': 'Collection created'})
        else:
            return json.dumps({'error': 'Invalid credentials'})
    else:
        return json.dumps({'error': 'Unauthorized'})

@app.route('/load/<collection>', methods=['GET','POST'])
@limiter.limit(rpm)
def load(collection):
    auth = request.authorization
    if auth:
        if auth.username == admin['username'] and auth.password == admin['password']:
            if collection not in Database.collections:
                return json.dumps({'error': 'Collection does not exist'})

            return str(Database.loadCollection(collection))
        else:
            return json.dumps({'error': 'Invalid credentials'})
    else:
        return json.dumps({'error': 'Unauthorized'})

@app.route('/save/<collection>', methods=['GET','POST'])
@limiter.limit(rpm)
def save(collection):
    auth = request.authorization
    if auth:
        if auth.username == admin['username'] and auth.password == admin['password']:
            if collection not in Database.collections:
                return json.dumps({'error': 'Collection does not exist'})

            Database.saveCollection(collection)
            return json.dumps({'success': 'Collection saved'})
        else:
            return json.dumps({'error': 'Invalid credentials'})
    else:
        return json.dumps({'error': 'Unauthorized'})

@app.route('/add/<collection>', methods=['GET','POST'])
@limiter.limit(rpm)
def add(collection):
    auth = request.authorization
    if auth:
        if auth.username == admin['username'] and auth.password == admin['password']:
            if collection not in Database.collections:
                return json.dumps({'error': 'Collection does not exist'})

            data = request.get_json()
            Database.add_to_collection(collection, data)
            return json.dumps({'success': 'Item added'})
        else:
            return json.dumps({'error': 'Invalid credentials'})
    else:
        return json.dumps({'error': 'Unauthorized'})

@app.route('/remove/<collection>', methods=['GET','POST'])
@limiter.limit(rpm)
def remove(collection):
    auth = request.authorization
    if auth:
        if auth.username == admin['username'] and auth.password == admin['password']:
            if collection not in Database.collections:
                return json.dumps({'error': 'Collection does not exist'})

            data = request.get_json()
            Database.remove_from_collection(collection, data)
            return json.dumps({'success': 'Data removed'})
        else:
            return json.dumps({'error': 'Invalid credentials'})
    else:
        return json.dumps({'error': 'Unauthorized'})

@app.route('/delete/<collection>', methods=['GET','POST'])
@limiter.limit(cdpm)
def delete(collection):
    auth = request.authorization
    if auth:
        if auth.username == admin['username'] and auth.password == admin['password']:
            if collection not in Database.collections:
                return json.dumps({'error': 'Collection does not exist'})

            Database.deleteCollection(collection)
            return json.dumps({'success': 'Collection deleted'})
        else:
            return json.dumps({'error': 'Invalid credentials'})
    else:
        return json.dumps({'error': 'Unauthorized'})



app.run()