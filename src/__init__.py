import uuid
from flask import *
from src.core import *
from src.core import CrispyDB
from src.configman import *
import src.configman as config
from src.forms import *
from flask_bootstrap import Bootstrap
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import io

SECRET_KEY = os.urandom(32)

global LOGGED
LOGGED = False

global LOGGED_IP
LOGGED_IP = ""

app = Flask(__name__)
db = None

def init_db():
    global db
    crispy = CrispyDB(config.config['path'])
    db = crispy.db('main')
app.config['SECRET_KEY'] = SECRET_KEY
bootstrap = Bootstrap(app)
limiter = Limiter(
    app,
    default_limits=[rpm]
)

@app.route('/')
def index():
    if config.config['webUI'] == "True":
        return str({config.config['name']: config.config['version'],
                    "WebUI": config.config['webUI']}) + '<a href="/login">Login</a> '
    else:
        return str({config.config['name']: config.config['version'], "WebUI": config.config['webUI']})


@app.route('/getdata/<collection>')
def getdata(collection):
    token = request.args.get('token')
    if token in config.tokens:
        if collection in db.get_tables():
            return json.dumps(db.table(collection).data)
        else:
            return json.dumps({'error': 'Collection does not exist'})
    else:
        return json.dumps({'error': 'Unauthorized'})


@app.route('/create/token', methods=['GET', 'POST'])
@limiter.limit(rpm)
def createToken():
    auth = request.authorization
    if auth:
        for user in users:
            if auth.username == user['username'] and auth.password == user['password']:
                if user['role'] == 'admin':
                    token = str(uuid.uuid4())
                    config.tokens.append(token)
                    with open('src/config/tokens.json', 'w') as f:
                        json.dump(config.tokens, f, indent=4)
                    print("TOKEN HAS BEEN CREATED, {}".format(token))
                    return json.dumps(token)
        return json.dumps({'error': 'Invalid credentials'})
    else:
        return json.dumps({'error': 'Unauthorized'})


@app.route("/flush/token", methods=['GET', 'POST'])
@limiter.limit(rpm)
def flushToken():
    token = request.args.get('token')
    if token in config.tokens:
        config.tokens.remove(token)
        with open('src/config/tokens.json', 'w') as f:
            json.dump(config.tokens, f, indent=4)
        print("TOKEN HAS BEEN FLUSHED, {}".format(token))
        return json.dumps({'success': 'Token has been flushed'})
    else:
        return json.dumps({'error': 'token not found'})


@app.route('/create/<collection>', methods=['GET', 'POST'])
@limiter.limit(ccpm)
def create(collection):
    token = request.args.get('token')
    if token in config.tokens:
        if collection in db.get_tables():
            return json.dumps({'error': 'Collection already exists'})
        else:
            db.table(collection)
            return json.dumps({'success': 'Collection created'})
    else:
        return json.dumps({'error': 'Unauthorized'})


@app.route('/add/<collection>', methods=['GET', 'POST'])
@limiter.limit(rpm)
def add(collection):
    token = request.args.get('token')
    if token in config.tokens:
        if collection in db.get_tables():
            if request.method == 'POST':
                data = request.get_json()
                if data:
                    db.table(collection).add(data)
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
        if collection in db.get_tables():
            if request.method == 'POST':
                data = request.get_json()
                if data:
                    if db.table(collection).remove(data):
                        return json.dumps({'success': 'Document removed'})
                    else:
                        return json.dumps({'error': 'Document not found'})
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
        if collection in db.get_tables():
            db.delete_table(collection)
            return json.dumps({'success': 'Collection deleted'})
        else:
            return json.dumps({'error': 'Collection does not exist'})
    else:
        return json.dumps({'error': 'Unauthorized'})


@app.route('/search/<collection>', methods=['GET', 'POST'])
def search(collection):
    token = request.args.get('token')
    if token in config.tokens:
        if collection in db.get_tables():
            if request.method == 'POST':
                data = request.get_json()
                if data:
                    return json.dumps(db.table(collection).search(data))
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
        return json.dumps(config.tokens)
    else:
        return json.dumps({'error': 'Unauthorized'})


@app.route('/upload/<collection>', methods=['POST'])
def upload_file(collection):
    token = request.args.get('token')
    if token not in config.tokens:
        return json.dumps({'error': 'Unauthorized'})
    if collection not in db.get_tables():
        return json.dumps({'error': 'Collection does not exist'})
    if 'file' not in request.files:
        return json.dumps({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return json.dumps({'error': 'No selected file'})
    if file:
        file_id = db.store_binary(file.read())
        return json.dumps({'success': 'File uploaded', 'file_id': file_id})


@app.route('/download/<file_id>')
def download_file(file_id):
    token = request.args.get('token')
    if token not in config.tokens:
        return json.dumps({'error': 'Unauthorized'})
    data = db.retrieve_binary(file_id)
    if data:
        return send_file(io.BytesIO(data), mimetype='application/octet-stream')
    else:
        return json.dumps({'error': 'File not found'})


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
    if webUI:
        form = LoginForm()
        if form.validate_on_submit():
            for user in users:
                if form.username.data == user['username'] and form.password.data == user['password']:
                    if user['role'] in ['admin', 'webui']:
                        global LOGGED
                        LOGGED = True
                        global LOGGED_IP
                        LOGGED_IP = request.remote_addr
                        session['role'] = user['role']
                        return redirect(url_for('web_dashboard'))
            print("ERROR")
        return render_template('login.html', form=form, name=name)
    else:
        return "WebUI is off"


@app.route('/web/dashboard', methods=['GET', 'POST'])
def web_dashboard():
    newcollection = NewCollectionForm()
    if webUI:
        if LOGGED == True and LOGGED_IP == request.remote_addr:
            if newcollection.validate_on_submit():
                if newcollection.name.data not in db.get_tables():
                    if newcollection.name.data != '':
                        db.table(newcollection.name.data)
                        return redirect(url_for('web_dashboard'))
                    else:
                        pass
                else:
                    return "Collection already exists"
            collections = db.get_tables()
            return render_template('index.html', collections=collections, nform=newcollection, name=name)
        else:
            return redirect(url_for('web_login'))
    else:
        return "WebUI is off"


@app.route('/web/edit/<collection>/<doc_id>', methods=['GET', 'POST'])
def web_edit_document(collection, doc_id):
    if webUI:
        if LOGGED and LOGGED_IP == request.remote_addr:
            if collection not in db.get_tables():
                return "Collection does not exist"

            table = db.table(collection)
            doc = table.search({'_id': doc_id})

            if not doc:
                return "Document not found"

            doc = doc[0]
            EditForm = create_edit_form(doc)
            form = EditForm(request.form, data=doc)

            if form.validate_on_submit():
                new_data = {}
                for field in form:
                    if field.name not in ['csrf_token', 'submit']:
                        new_data[field.name] = field.data
                table.update({'_id': doc_id}, new_data)
                return redirect(url_for('web_collections', collection=collection))

            return render_template('edit_document.html', form=form, collection=collection, doc_id=doc_id)
        else:
            return redirect(url_for('web_login'))
    else:
        return "WebUI is off"


# commands for the cli are below

@app.route('/web/deleteall/<collection>', methods=['GET', 'POST'])
def web_deleteall(collection):
    if webUI:
        if LOGGED == True and LOGGED_IP == request.remote_addr and session.get('role') == 'admin':
            if collection not in db.get_tables():
                return "Collection does not exist"
            else:
                db.table(collection).removeall()
                return redirect(url_for('web_dashboard'))
        else:
            return redirect(url_for('web_login'))
    else:
        return "WebUI is off"


@app.route('/web/collections/<collection>', methods=['GET', 'POST'])
def web_collections(collection):
    if webUI:
        if LOGGED == True and LOGGED_IP == request.remote_addr:
            if collection not in db.get_tables():
                return "Collection does not exist"
            else:
                data = db.table(collection).data
                return render_template('collection.html', collection=collection, data=data)
        else:
            return redirect(url_for('web_login'))
    else:
        return "WebUI is off"


@app.route('/web/createtoken', methods=['GET', 'POST'])
def web_createtoken():
    if webUI:
        if LOGGED == True and LOGGED_IP == request.remote_addr and session.get('role') == 'admin':
            token = str(uuid.uuid4())
            config.tokens.append(token)
            with open('config/tokens.json', 'w') as f:
                json.dump(config.tokens, f, indent=4)
                ret = "Token created: " + token
            return ret
        else:
            return redirect(url_for('web_login'))


@app.route('/web/getdata/<collection>', methods=['GET'])
def webgetdata(collection):
    if webUI:
        if LOGGED == True and LOGGED_IP == request.remote_addr:
            if collection not in db.get_tables():
                return "Collection does not exist"
            else:
                return json.dumps(db.table(collection).data)
        else:
            return redirect(url_for('web_login'))
    else:
        return "WebUI is off"


@app.route('/web/logout')
def web_logout():
    global LOGGED, LOGGED_IP
    LOGGED, LOGGED_IP = False, None
    session.pop('role', None)
    return redirect(url_for('web_login'))


@app.route('/getallroutes')
def getallroutes():
    # print all routes in a json friendly format
    return str(app.url_map)


@app.route('/web/delete/<collection>', methods=['GET', 'POST'])
def web_delete_collection(collection):
    if webUI:
        if LOGGED == True and LOGGED_IP == request.remote_addr and session.get('role') == 'admin':
            if collection not in db.get_tables():
                return "Collection does not exist"
            else:
                db.delete_table(collection)
                return redirect(url_for('web_dashboard'))
        else:
            return redirect(url_for('web_login'))


@app.route('/help/endpoints')
def help_endpoints():
    x = []
    for rule in app.url_map.iter_rules():
        x += [rule.rule]
    return str(x)
