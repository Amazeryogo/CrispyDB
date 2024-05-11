import json
import os
from dataclasses import dataclass


@dataclass
class Collection:
    name: str
    path: str
    data = []
    x = None

    def load(self):
        if not os.path.exists(self.path):
            return "not found"
        self.x = lambda x: json.loads(open(self.path + "/" + self.name + ".json", "r").read())

    def save(self):
        x = open(self.path + "/" + self.name + ".json", "a")
        x.write(json.dumps(self.data))

    def add(self, item):
        self.data.append(item)
        self.save()

    def remove(self, item):
        try:
            self.data.remove(item)
            self.save()
        except ValueError:
            return "not found"

    def update(self, x, y):
        for i in self.data:
            if i[x] == x:
                i[y] = y
                self.save()
                return "updated"
        return "not found"

    def removeall(self):
        self.data = []
        self.save()

    def search(self, x):
        for i in self.data:
            if i[x] == x:
                return i
        return "not found"
