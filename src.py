from flask import *
from core import *
from config import *
from forms import *


SECRET_KEY = os.urandom(32)

global LOGGED
LOGGED = False

global LOGGED_IP
LOGGED_IP = ""

if config['environment'] != 'production' and config['environment'] != 'development':
    print('[ERROR] Environment not set correctly')
    sys.exit(1)

if python_version != platform.python_version():
    print("Python version mismatch")
    sys.exit(1)

if webUI == True:
    print("Web UI is on")
else:
    print("WebUI is off ")


Database = Database(config['path'])
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
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
        if auth.username == USERNAME and auth.password == PASSWORD:
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
        if auth.username == USERNAME and auth.password == PASSWORD:
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
        if auth.username == USERNAME and auth.password == PASSWORD:
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
        if auth.username == USERNAME and auth.password == PASSWORD:
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
        if auth.username == USERNAME and auth.password == PASSWORD:
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
        if auth.username == USERNAME and auth.password == PASSWORD:
            if collection not in Database.collections:
                return json.dumps({'error': 'Collection does not exist'})

            Database.deleteCollection(collection)
            return json.dumps({'success': 'Collection deleted'})
        else:
            return json.dumps({'error': 'Invalid credentials'})
    else:
        return json.dumps({'error': 'Unauthorized'})

@app.route('/search/<collection>', methods=['GET','POST'])
@limiter.limit(rpm)
def search(collection):
    auth = request.authorization
    if auth:
        if auth.username == USERNAME and auth.password == PASSWORD:
            if collection not in Database.collections:
                return json.dumps({'error': 'Collection does not exist'})

            data = request.get_json()
            return str(Database.search_in_collection(collection, data))
        else:
            return json.dumps({'error': 'Invalid credentials'})
    else:
        return json.dumps({'error': 'Unauthorized'})

@app.route('/web/status')
def web_status():
    return webUI

@app.route('/web')
def web():
    return render_template('Intro.html')

@app.route('/web/login', methods=['GET','POST'])
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
                print(LOGGED_IP)
                return redirect(url_for('web_dashboard'))
            else:
                print("ERROR")

        return render_template('login.html', form=form,name=name)
    else:
        return "WebUI is off"

@app.route('/web/dashboard', methods=['GET','POST'])
def web_dashboard():
    newcollection = NewCollectionForm()
    if webUI == True:
        if LOGGED == True and LOGGED_IP == request.remote_addr:
            if newcollection.validate_on_submit():
                if newcollection.name.data not in Database.collections:
                    Database.createCollection(newcollection.name.data)
                    return redirect(url_for('web_dashboard'))
                else:
                    return "Collection already exists"
            collections = Database.collections
            return render_template('index.html',collections=collections,nform=newcollection,name=name)
        else:
            return redirect(url_for('web_login'))
    else:
        return "WebUI is off"

@app.route('/web/collections/<collection>', methods=['GET','POST'])
def web_collections(collection):
    if webUI == True:
        if LOGGED == True and LOGGED_IP == request.remote_addr:
            if collection not in Database.collections:
                return "Collection does not exist"
            else:
                form = AddDataForm()
                if form.validate_on_submit():
                    Database.add_to_collection(collection, form.data.data)
                    return redirect(url_for('web_collections', collection=collection))
                # get the data in collection
                data = Database.loadCollection(collection)
                return render_template('collection.html',collection=collection,data=data,form=form)
        else:
            return redirect(url_for('web_login'))
    else:
        return "WebUI is off"


@app.route('/getdata/<collection>', methods=['GET','POST'])
def getdata(collection):
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

# idk how to make easter eggs, so just gonna leave this here
@app.route('/why/am/i/so/lonely')
@limiter.exempt
def why():
    return "I'm lonely"
