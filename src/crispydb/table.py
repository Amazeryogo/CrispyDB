import json
import os


class Table:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.file = os.path.join(self.path, self.name + ".json")
        self.data = []
        self.load()

    def load(self):
        if not os.path.exists(self.file):
            # If the file doesn't exist, create it with an empty list
            with open(self.file, 'w') as f:
                json.dump([], f)
        else:
            with open(self.file, 'r') as f:
                try:
                    self.data = json.load(f)
                except json.JSONDecodeError:
                    self.data = []

    def save(self):
        with open(self.file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def add(self, item):
        self.data.append(item)
        self.save()

    def remove(self, query):
        item_found = False
        initial_len = len(self.data)

        # This will remove all items that match the query
        self.data = [item for item in self.data if not self._matches(item, query)]

        if len(self.data) < initial_len:
            item_found = True

        if item_found:
            self.save()
            return True
        else:
            return False

    def update(self, query, new_data):
        item_found = False
        for item in self.data:
            if self._matches(item, query):
                item.update(new_data)
                item_found = True
        if item_found:
            self.save()
            return True
        return False

    def removeall(self):
        self.data = []
        self.save()

    def search(self, query):
        results = []
        for item in self.data:
            if self._matches(item, query):
                results.append(item)
        return results

    def _matches(self, item, query):
        for key, value in query.items():
            if key not in item or item[key] != value:
                return False
        return True
