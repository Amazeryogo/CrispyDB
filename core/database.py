import json
import os
from core.collection import Collection

class Database:
    def __init__(self, path):
        self.path = path
        self.collections = {}
        self.load()
        for file in os.listdir(self.path):
            if file.endswith(".json"):
                self.collections[file[:-5]] = Collection(file[:-5], self.path) 
                
    def load(self):
        for name in os.listdir(self.path):
            if name.endswith(".json"):
                self.collections[name[:-5]] = Collection(name[:-5], self.path)
    
    def createCollection(self, name):
        self.collections[name] = Collection(name, self.path)
    
    def get_collections(self):
        return list(self.collections.keys())
    
    def get_collection_data(self, name):
        return self.collections[name].data
    
    def loadCollection(self, name):
        return self.collections[name].load()

    def deleteCollection(self, name):
        del self.collections[name]
        os.remove(self.path + "/" + name + ".json")
    
    def add_to_collection(self, collection, item):
        self.collections[collection].add(item)
    
    def remove_from_collection(self, name, item):
        self.collections[name].remove(item)

    def saveCollection(self, name):
        self.collections[name].save()
    
    def removeall_from_collection(self,name):
        self.collections[name].removeall()
    
    def search_in_collection(self, name, search):
        return [item for item in self.collections[name].data if search in item]