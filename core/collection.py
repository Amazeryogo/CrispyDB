import json
import os


class Collection:
    def __init__(self, name, path):
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
        # get the id of the last item
        if len(self.data) > 0:
            item["_crispy-id"] = self.data[-1]["_crispy-id"] + 1
        else:
            item["_crispy-id"] = 1
        self.data.append(item)

    def remove(self, item):
        try:
            self.data.remove(item)
        except ValueError:
            return "not yay"

    def delete(self, key, value):
        for i in self.data:
            if i[key] == value:
                self.data.remove(i)
                return "deleted"
        return "not found"

    def __len__(self):
        return len(self.data)

    def removeall(self):
        self.data = []
        self.save()

    def keysearch(self, key):
        for i in self.data:
            if key in i.keys():
                return i

    def search(self, data):
        # take the keys of the data and search for them in the collection
        # if the key is found and the value is the same, return the item
        for i in self.data:
            for key in data.keys():
                if key in i.keys():
                    if i[key] == data[key] and key != "_crispy-id":
                        return i
                    else:
                        continue
                else:
                    continue
        return "not found"

