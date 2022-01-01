import json
import os

class Collection:
    def __init__(self, name,path):
        self.name = name
        self.path = path + "/" + name + ".json"
        self.data = []
        self.load()
    def load(self):
        if os.path.isfile(self.path):
            with open(self.path, "r") as f:
                self.data = json.load(f)
        else:
            self.save()

        return self.data
    
    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f)
    
    def add(self, item):
        self.data.append(item)
        self.save()
    
    def remove(self, item):
        try:
            self.data.remove(item)
            self.save()
        except ValueError:
            return "not yay"

    def __iter__(self):
        return iter(self.data)
    
    def data(self):
        return self.data

    def __len__(self):
        return len(self.data)
    
    def removeall(self):
        self.data = []
        self.save()

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
        return self.collections.keys()
    
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