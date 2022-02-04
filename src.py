import uuid
from flask import *
from core import *
from config import *
import config
from forms import *
from flask_bootstrap import Bootstrap
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

SECRET_KEY = os.urandom(32)

global LOGGED
LOGGED = False

global LOGGED_IP
LOGGED_IP = ""

Database = Database(config.config['path'])

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
    return str({config.config['name']: config.config['version'], "WebUI": config.config['webUI']})


@app.route('/getdata/<collection>')
def getdata(collection):
    token = request.args.get('token')
    if token in config.tokens:
        if collection in Database.collections:
            return str(Database.loadCollection(collection))
        else:
            return json.dumps({'error': 'Collection does not exist'})
    else:
        return json.dumps({'error': 'Unauthorized'})


@app.route('/create/token', methods=['GET', 'POST'])
@limiter.limit(rpm)
def createToken():
    auth = request.authorization
    if auth:
        if auth.username == USERNAME and auth.password == PASSWORD:
            token = str(uuid.uuid4())
            config.tokens.append(token)
            with open('config/tokens.json', 'w') as f:
                json.dump(config.tokens, f, indent=4)
            print("TOKEN HAS BEEN CREATED, {}".format(token))
            return json.dumps({'success': token})
        else:
            return json.dumps({'error': 'Invalid credentials'})
    else:
        return json.dumps({'error': 'Unauthorized'})


@app.route('/changeauth', methods=['GET', 'POST'])
def changeauth():
    auth = request.authorization
    newpass = request.args.get('newpassword')
    if auth:
        if auth.username == USERNAME and auth.password == PASSWORD:
            if newpass:
                config.config['admin password'] = newpass
                with open('config/config.json', 'w') as f:
                    json.dump(config, f, indent=4)
                    print("PASSWORD HAS BEEN CHANGED, PLEASE RESTART CRISPYDB!!!")
                return json.dumps({'success': 'Password changed'})
            else:
                return json.dumps({'error': 'Invalid new password'})
        else:
            return json.dumps({'error': 'Invalid credentials'})
    else:
        return json.dumps({'error': 'Unauthorized'})


@app.route('/create/<collection>', methods=['GET', 'POST'])
@limiter.limit(ccpm)
def create(collection):
    token = request.args.get('token')
    if token in config.tokens:
        if collection in Database.collections:
            return json.dumps({'error': 'Collection already exists'})
        else:
            Database.createCollection(collection)
            return json.dumps({'success': 'Collection created'})
    else:
        return json.dumps({'error': 'Unauthorized'})


@app.route('/load/<collection>', methods=['GET', 'POST'])
@limiter.limit(rpm)
def load(collection):
    token = request.args.get('token')
    if token in config.tokens:
        if collection in Database.collections:
            Database.loadCollection(collection)
            return json.dumps({'success': 'Collection loaded'})
        else:
            return json.dumps({'error': 'Collection does not exist'})
    else:
        return json.dumps({'error': 'Unauthorized'})


@app.route('/save', methods=['GET', 'POST'])
@limiter.limit(rpm)
def save():
    token = request.args.get('token')
    if token in config.tokens:
        if request.method == 'POST':
            data = request.get_json()
            if data:
                Database.saveCollection(data)
                return json.dumps({'success': 'Collection saved'})
            else:
                return json.dumps({'error': 'Invalid data'})
        else:
            return json.dumps({'error': 'Invalid request'})
    else:
        return json.dumps({'error': 'Unauthorized'})


@app.route('/add/<collection>', methods=['GET', 'POST'])
@limiter.limit(rpm)
def add(collection):
    token = request.args.get('token')
    if token in config.tokens:
        if collection in Database.collections:
            if request.method == 'POST':
                data = request.get_json()
                if data:
                    Database.addToCollection(collection, data)
                    return json.dumps({'success': 'Document added'})
                else:
                    return json.dumps({'error': 'Invalid data'})
            else:
                return json.dumps({'error': 'Invalid request'})
        else:
            return json.dumps({'error': 'Collection does not exist'})
    else:
        return json.dumps({'error': 'Unauthorized'})


@app.route('/removefrom/<collection>', methods=['GET', 'POST'])
@limiter.limit(rpm)
def remove(collection):
    token = request.args.get('token')
    if token in config.tokens:
        if collection in Database.collections:
            if request.method == 'POST':
                data = request.get_json()
                if data:
                    Database.removeFromCollection(collection, data)
                    return json.dumps({'success': 'Document removed'})
                else:
                    return json.dumps({'error': 'Invalid data'})
            else:
                return json.dumps({'error': 'Invalid request'})
        else:
            return json.dumps({'error': 'Collection does not exist'})
    else:
        return json.dumps({'error': 'Unauthorized'})


@app.route('/delete/<collection>', methods=['GET', 'POST'])
@limiter.limit(cdpm)
def delete(collection):
    token = request.args.get('token')
    if token in config.tokens:
        if collection in Database.collections:
            Database.deleteCollection(collection)
            return json.dumps({'success': 'Collection deleted'})
        else:
            return json.dumps({'error': 'Collection does not exist'})
    else:
        return json.dumps({'error': 'Unauthorized'})


@app.route('/keysearch/<collection>', methods=['GET', 'POST'])
def keysearch(collection):
    token = request.args.get('token')
    if token in config.tokens:
        if collection in Database.collections:
            if request.method == 'POST':
                data = request.get_json()
                if data:
                    return json.dumps(Database.keysearch(collection, data))
                else:
                    return json.dumps({'error': 'Invalid data'})
            else:
                return json.dumps({'error': 'Invalid request'})
        else:
            return json.dumps({'error': 'Collection does not exist'})


@app.route('/search/<collection>', methods=['GET', 'POST'])
def search(collection):
    token = request.args.get('token')
    if token in config.tokens:
        if collection in Database.collections:
            if request.method == 'POST':
                data = request.get_json()
                if data:
                    return json.dumps(Database.search(collection, data))
                else:
                    return json.dumps({'error': 'Invalid data'})
            else:
                return json.dumps({'error': 'Invalid request'})
        else:
            return json.dumps({'error': 'Collection does not exist'})
    else:
        return json.dumps({'error': 'Unauthorized'})


@app.route('/tokens', methods=['GET', 'POST'])
def tokens():
    token = request.args.get('token')
    if token in config.tokens:
        return json.dumps(tokens)
    else:
        return json.dumps({'error': 'Unauthorized'})


############################################################

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


@app.route('/web/createtoken', methods=['GET', 'POST'])
def web_createtoken():
    if webUI == True:
        if LOGGED == True and LOGGED_IP == request.remote_addr:
            token = str(uuid.uuid4())
            config.tokens.append(token)
            with open('config/tokens.json', 'w') as f:
                json.dump(config.tokens, f, indent=4)
                ret = "Token created: " + token
            return ret
        else:
            return redirect(url_for('web_login'))

# one piece lol
@app.route('/onepiece')
def onepiece():
    for x in eastereggs:
        if x["name"] == "onepiece":
            return x["lyrics"]

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

@app.route('/getallroutes')
def getallroutes():
    # print all routes in a json friendly format
    return str(app.url_map)


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


@app.route('/web/changeauth', methods=['GET', 'POST'])
def web_changeauth():
    global USERNAME, PASSWORD
    form = Changeauth()
    if webUI == True:
        if LOGGED == True and LOGGED_IP == request.remote_addr:
            if form.validate_on_submit():
                Oldpassword = form.old_password.data
                Newpassword = form.new_password.data
                if Oldpassword == PASSWORD:
                    if Newpassword != '':
                        PASSWORD = Newpassword
                        config.config['admin password'] = Newpassword
                        with open('config/config.json', 'w') as f:
                            json.dump(config, f, indent=4)
                            f.close()
                        return redirect(url_for('web_dashboard'))
        else:
            return redirect(url_for('web_login'))
    return render_template('changeauth.html', form=form)
