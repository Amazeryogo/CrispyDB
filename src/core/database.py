import os
from src.core.collection import Collection


class Database:
    def __init__(self, path):
        self.path = path
        self.collections = {}
        self.load()

    def load(self):
        for name in os.listdir(self.path):
            if name.endswith(".json"):
                self.collections[name[:-5]] = Collection(name[:-5], self.path)

    def getdata(self, name): return self.collections[name].data

    def createCollection(self, name):
        os.system("touch {}".format(self.path + "/" + name + ".json"))
        self.collections[name] = Collection(name, self.path)

    def getCollections(self): return list(self.collections.keys())

    def getCollectionData(self, name): return self.collections[name].data

    def loadCollection(self, name): return self.collections[name].load()

    def deleteCollection(self, name):
        del self.collections[name]
        os.remove(self.path + "/" + name + ".json")

    def search(self, collection, query): return self.collections[collection].search(query)

    def addToCollection(self, collection, item): self.collections[collection].add(item)

    def removeFromCollection(self, name, item): self.collections[name].remove(item)

    def saveCollection(self, name):
        for collection in self.collections:
            if collection == name:
                self.collections[collection].save()
        return "Collection saved"

    def nukeCollection(self, name): self.collections[name].removeall()

    def save(self):
        for collection in self.collections:
            self.collections[collection].save()
        return self
