from flask import *
from core import *
from config import *
from forms import *
from flask_bootstrap import Bootstrap
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import pandas as pd


SECRET_KEY = os.urandom(32)

global LOGGED
LOGGED = False

global LOGGED_IP
LOGGED_IP = ""

Database = Database(config['path'])

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
bootstrap = Bootstrap(app)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=[rpm]
)


@app.route('/')
def index():
    return str({config['name']: config['version'], "WebUI": config['webUI']})


@app.route('/getdata/<collection>')
def getdata(collection):
    auth = request.authorization
    if auth:
        if auth.username == USERNAME and auth.password == PASSWORD:
            if collection not in Database.collections:
                return json.dumps({'error': 'Collection does not exist'})

            return str(Database.getCollectionData(collection))
        else:
            return json.dumps({'error': 'Invalid credentials'})
    else:
        return json.dumps({'error': 'Unauthorized'})

@app.route('/create/<collection>', methods=['GET', 'POST'])
@limiter.limit(ccpm)
def create(collection):
    auth = request.authorization
    if auth:
        if auth.username == USERNAME and auth.password == PASSWORD:
            if collection in Database.collections:
                return json.dumps({'error': 'Collection already exists'})

            Database.createCollection(collection)
            return json.dumps({'success': 'Collection created'})
        else:
            return json.dumps({'error': 'Invalid credentials'})
    else:
        return json.dumps({'error': 'Unauthorized'})


@app.route('/load/<collection>', methods=['GET', 'POST'])
@limiter.limit(rpm)
def load(collection):
    auth = request.authorization
    if auth:
        if auth.username == USERNAME and auth.password == PASSWORD:
            if collection not in Database.collections:
                return json.dumps({'error': 'Collection does not exist'})

            return str(Database.loadCollection(collection))
        else:
            return json.dumps({'error': 'Invalid credentials'})
    else:
        return json.dumps({'error': 'Unauthorized'})


@app.route('/save', methods=['GET', 'POST'])
@limiter.limit(rpm)
def save():
    auth = request.authorization
    if auth:
        if auth.username == USERNAME and auth.password == PASSWORD:
            Database.save()
            return json.dumps({'success': 'Database saved'})
        else:
            return json.dumps({'error': 'Invalid credentials'})
    else:
        return json.dumps({'error': 'Unauthorized'})


@app.route('/add/<collection>', methods=['GET', 'POST'])
@limiter.limit(rpm)
def add(collection):
    auth = request.authorization
    if auth:
        if auth.username == USERNAME and auth.password == PASSWORD:
            if collection not in Database.collections:
                return json.dumps({'error': 'Collection does not exist'})

            data = request.get_json()
            Database.addToCollection(collection, data)
            return json.dumps({'success': 'Item added'})
        else:
            return json.dumps({'error': 'Invalid credentials'})
    else:
        return json.dumps({'error': 'Unauthorized'})


@app.route('/remove/<collection>', methods=['GET', 'POST'])
@limiter.limit(rpm)
def remove(collection):
    auth = request.authorization
    if auth:
        if auth.username == USERNAME and auth.password == PASSWORD:
            if collection not in Database.collections:
                return json.dumps({'error': 'Collection does not exist'})

            data = request.get_json()
            Database.removeFromCollection(collection, data)
            return json.dumps({'success': 'Data removed'})
        else:
            return json.dumps({'error': 'Invalid credentials'})
    else:
        return json.dumps({'error': 'Unauthorized'})


@app.route('/delete/<collection>', methods=['GET', 'POST'])
@limiter.limit(cdpm)
def delete(collection):
    auth = request.authorization
    if auth:
        if auth.username == USERNAME and auth.password == PASSWORD:
            if collection not in Database.collections:
                return json.dumps({'error': 'Collection does not exist'})

            Database.deleteCollection(collection)
            return json.dumps({'success': 'Collection deleted'})
        else:
            return json.dumps({'error': 'Invalid credentials'})
    else:
        return json.dumps({'error': 'Unauthorized'})


@app.route('/keysearch/<collection>', methods=['GET', 'POST'])
def keysearch(collection):
    auth = request.authorization
    if auth:
        if auth.username == USERNAME and auth.password == PASSWORD:
            if collection not in Database.collections:
                return json.dumps({'error': 'Collection does not exist'})

            data = request.get_json()
            return json.dumps(Database.keysearch(collection, data))
        else:
            return json.dumps({'error': 'Invalid credentials'})
    else:
        return json.dumps({'error': 'Unauthorized'})


@app.route('/search/<collection>', methods=['GET', 'POST'])
def search(collection):
    auth = request.authorization
    if auth:
        if auth.username == USERNAME and auth.password == PASSWORD:
            if collection not in Database.collections:
                return json.dumps({'error': 'Collection does not exist'})

            data = request.get_json()
            return json.dumps(Database.search(collection, data))
        else:
            return json.dumps({'error': 'Invalid credentials'})
    else:
        return json.dumps({'error': 'Unauthorized'})


@app.route('/web/status')
def web_status():
    return str(webUI)


@app.route('/web')
def web():
    return render_template('Intro.html')


@app.route('/web/login', methods=['GET', 'POST'])
@limiter.exempt
def web_login():
    if webUI == True:
        form = LoginForm()
        if form.validate_on_submit():
            if form.username.data == USERNAME and form.password.data == PASSWORD:
                global LOGGED
                LOGGED = True
                global LOGGED_IP
                LOGGED_IP = request.remote_addr
                return redirect(url_for('web_dashboard'))
            else:
                print("ERROR")

        return render_template('login.html', form=form, name=name)
    else:
        return "WebUI is off"


@app.route('/web/dashboard', methods=['GET', 'POST'])
def web_dashboard():
    newcollection = NewCollectionForm()
    if webUI == True:
        if LOGGED == True and LOGGED_IP == request.remote_addr:
            if newcollection.validate_on_submit():
                if newcollection.name.data not in Database.collections:
                    if newcollection.name.data != '':
                        Database.createCollection(newcollection.name.data)
                        return redirect(url_for('web_dashboard'))
                    else:
                        pass
                else:
                    return "Collection already exists"
            collections = Database.collections
            return render_template('index.html', collections=collections, nform=newcollection, name=name)
        else:
            return redirect(url_for('web_login'))
    else:
        return "WebUI is off"


# commands for the cli are below

@app.route('/web/deleteall/<collection>', methods=['GET', 'POST'])
def web_deleteall(collection):
    if webUI == True:
        if LOGGED == True and LOGGED_IP == request.remote_addr:
            if collection not in Database.collections:
                return "Collection does not exist"
            else:
                Database.removeAllFromCollection(collection)
                return redirect(url_for('web_dashboard'))
        else:
            return redirect(url_for('web_login'))
    else:
        return "WebUI is off"


@app.route('/web/collections/<collection>', methods=['GET', 'POST'])
def web_collections(collection):
    if webUI == True:
        if LOGGED == True and LOGGED_IP == request.remote_addr:
            if collection not in Database.collections:
                return "Collection does not exist"
            else:
                data = Database.loadCollection(collection)
                return render_template('collection.html', collection=collection, data=data)
        else:
            return redirect(url_for('web_login'))
    else:
        return "WebUI is off"


@app.route('/web/getdata/<collection>', methods=['GET'])
def webgetdata(collection):
    if webUI == True:
        if LOGGED == True and LOGGED_IP == request.remote_addr:
            if collection not in Database.collections:
                return "Collection does not exist"
            else:
                x = str(Database.loadCollection(collection))
                return x
        else:
            return redirect(url_for('web_login'))
    else:
        return "WebUI is off"

@app.route('/web/logout')
def web_logout():
    global LOGGED, LOGGED_IP
    LOGGED = False
    LOGGED_IP = None
    return redirect(url_for('web_login'))


@app.route('/web/delete/<collection>', methods=['GET', 'POST'])
def web_delete_collection(collection):
    if webUI == True:
        if LOGGED == True and LOGGED_IP == request.remote_addr:
            if collection not in Database.collections:
                return "Collection does not exist"
            else:
                Database.deleteCollection(collection)
                return redirect(url_for('web_dashboard'))
        else:
            return redirect(url_for('web_login'))

