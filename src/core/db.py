import os
import shutil
from .table import Table


class CrispyDB:
    def __init__(self, path):
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.dbs = {}
        self.load_dbs()

    def load_dbs(self):
        for name in os.listdir(self.path):
            db_path = os.path.join(self.path, name)
            if os.path.isdir(db_path):
                self.dbs[name] = DB(db_path)

    def db(self, name):
        if name not in self.dbs:
            db_path = os.path.join(self.path, name)
            if not os.path.exists(db_path):
                os.makedirs(db_path)
            self.dbs[name] = DB(db_path)
        return self.dbs[name]

    def delete_db(self, name):
        if name in self.dbs:
            self.dbs[name].nuke_db()
            del self.dbs[name]
            return True
        return False


import uuid

class DB:
    def __init__(self, path):
        self.path = path
        self.tables = {}
        self.binary_path = os.path.join(self.path, '_bin')
        if not os.path.exists(self.binary_path):
            os.makedirs(self.binary_path)
        self.load_tables()

    def load_tables(self):
        for name in os.listdir(self.path):
            if name.endswith(".json"):
                table_name = name[:-5]
                self.tables[table_name] = Table(table_name, self.path)

    def table(self, name):
        if name not in self.tables:
            self.tables[name] = Table(name, self.path)
        return self.tables[name]

    def delete_table(self, name):
        if name in self.tables:
            table_file = self.tables[name].file
            if os.path.exists(table_file):
                os.remove(table_file)
            del self.tables[name]
            return True
        return False

    def get_tables(self):
        return list(self.tables.keys())

    def nuke_db(self):
        shutil.rmtree(self.path)

    def store_binary(self, data):
        file_id = str(uuid.uuid4())
        file_path = os.path.join(self.binary_path, file_id)
        with open(file_path, 'wb') as f:
            f.write(data)
        return file_id

    def retrieve_binary(self, file_id):
        file_path = os.path.join(self.binary_path, file_id)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                return f.read()
        return None
