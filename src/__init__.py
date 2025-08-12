import uuid
from flask import Flask, request, jsonify
from src.core import *
from src.core import CrispyDB
from src.configman import *
import src.configman as config
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import io
import traceback

SECRET_KEY = os.urandom(32)

app = Flask(__name__)
db = None

def init_db():
    global db
    path = app.config.get('DB_PATH', 'crispydb_data')
    crispy = CrispyDB(path=path)
    db = crispy.db('main')
app.config['SECRET_KEY'] = SECRET_KEY
limiter = Limiter(
    app,
    default_limits=[rpm]
)

from functools import wraps

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            # Expecting "Bearer <token>"
            try:
                token_type, token = request.headers['Authorization'].split()
                if token_type.lower() != 'bearer':
                    raise ValueError
            except ValueError:
                return {"error": "Invalid Authorization header format"}, 401

        master_token = app.config.get('MASTER_TOKEN', 'DEFAULT_MASTER_TOKEN')

        if not token or token != master_token:
            return {"error": "Unauthorized"}, 401

        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    return {
        "name": config.config.get('name', 'CrispyDB'),
        "version": config.config.get('version', '0.0.0'),
        "api": "v1"
    }, 200

@app.route('/<collection>/insert', methods=['POST'])
@require_auth
def insert(collection):
    """Inserts a single document or a list of documents into a collection."""
    documents = request.get_json()
    if not documents:
        return {"error": "Request body must contain a valid JSON document or list of documents"}, 400

    try:
        coll = db.collection(collection)
        inserted_count = coll.insert(documents)
        return {"success": f"Inserted {inserted_count} document(s) into '{collection}'"}, 201
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}, 500

@app.route('/<collection>/search', methods=['POST'])
@require_auth
def search(collection):
    """Searches a collection based on a query."""
    query = request.get_json()
    if query is None:
        return {"error": "Request body must contain a valid JSON query"}, 400

    try:
        coll = db.collection(collection)
        results = coll.search(query)
        return jsonify(results), 200
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}, 500

@app.route('/<collection>/update', methods=['PUT'])
@require_auth
def update(collection):
    """Updates documents in a collection based on a query."""
    payload = request.get_json()
    if not payload or 'query' not in payload or 'update_spec' not in payload:
        return {"error": "Request body must contain 'query' and 'update_spec' keys"}, 400

    query = payload.get('query')
    update_spec = payload.get('update_spec')
    multi = payload.get('multi', False)

    try:
        coll = db.collection(collection)
        updated_count = coll.update(query, update_spec, multi=multi)
        return {"success": f"Updated {updated_count} document(s) in '{collection}'"}, 200
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}, 500

@app.route('/<collection>/remove', methods=['DELETE'])
@require_auth
def remove(collection):
    """Removes documents from a collection based on a query."""
    query = request.get_json()
    if query is None:
        return {"error": "Request body must contain a valid JSON query"}, 400

    try:
        coll = db.collection(collection)
        removed_count = coll.remove(query)
        return {"success": f"Removed {removed_count} document(s) from '{collection}'"}, 200
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}, 500
