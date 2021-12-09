from flask import *
import json
from core import *
import sys
import platform
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

with open('config/config.json', 'r') as f:
    config = json.load(f)
with open('config/admin.json', 'r') as f:
    admin = json.load(f)




# request per minute
rpm = str(config['rpm']) + ' per minute'
#collection creation per minute
ccpm = str(config['ccpm']) + ' per minute'
# collection deletion per minute
cdpm = str(config['cdpm']) + ' per minute'
version = config['version']
python_version = config['python version']
PORT = config['port']
HOST = config['host']

if config['environment'] != 'production' or config['environment'] != 'development':
    print('[ERROR] Environment not set correctly')
    sys.exit(1)

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

if config['hide_config'] != True and config['environment'] == 'production':
            print("WARNING: CONFIG IS NOT HIDDEN")
            print("CHANGE IMMEDIATELY")
            print("THIS IS A SECURITY RISK IN PRODUCTION, CHANGE IT IN THE config/config.json FILE")
else:
    print("CONFIG IS HIDDEN")


@app.route('/')
def index():
    if config['hide_config'] == True:

        return "CrispyDB is running,{}".format(version) 
    else:
        if config['environment'] == 'production':
            return "SECURITY ERROR, ADMIN, PLEASE CHECK  THE LOGS"
        else:
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

# idk how to make easter eggs, so just gonna leave this here
@app.route('/why/am/i/so/lonely')
@limiter.exempt()
def why():
    return "I'm lonely"


app.run(host=HOST, port=PORT)