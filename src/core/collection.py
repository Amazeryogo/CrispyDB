import json
import os
import uuid

class Collection:
    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.file = os.path.join(self.path, self.name + ".json")
        self.data = []
        self.load()

    def load(self):
        if not os.path.exists(self.file):
            self.data = []
            return

        with open(self.file, "r") as f:
            try:
                self.data = json.load(f)
            except json.JSONDecodeError:
                self.data = []

    def save(self):
        with open(self.file, "w") as f:
            json.dump(self.data, f, indent=4)

    def insert(self, documents):
        """Inserts a single document or a list of documents."""
        if not isinstance(documents, list):
            documents = [documents]

        count = 0
        for doc in documents:
            if '_id' not in doc:
                doc['_id'] = str(uuid.uuid4())
            self.data.append(doc)
            count += 1

        if count > 0:
            self.save()

        return count

    def search(self, query, sort=None, limit=None):
        results = []
        for item in self.data:
            if self._matches(item, query):
                results.append(item)

        if sort:
            for field, direction in reversed(sort):
                results.sort(key=lambda x: x.get(field), reverse=direction == -1)

        if limit:
            return results[:limit]

        return results

    def update(self, query, update_spec, multi=False):
        updated_count = 0
        for item in self.data:
            if self._matches(item, query):
                for op, value in update_spec.items():
                    if op == '$set':
                        for field, new_value in value.items():
                            item[field] = new_value
                updated_count += 1
                if not multi:
                    break
        if updated_count > 0:
            self.save()
        return updated_count

    def remove(self, query):
        items_to_remove = self.search(query)
        original_count = len(self.data)
        self.data = [item for item in self.data if item not in items_to_remove]
        removed_count = original_count - len(self.data)
        if removed_count > 0:
            self.save()
        return removed_count

    def _matches(self, item, query):
        if not query:
            return True

        for key, value in query.items():
            if key.startswith('$'):
                if key == '$or':
                    if not any(self._matches(item, sub_query) for sub_query in value):
                        return False
                elif key == '$and':
                    if not all(self._matches(item, sub_query) for sub_query in value):
                        return False
                else:
                    return False # Unrecognized operator
            elif isinstance(value, dict):
                # This handles comparison operators like $gt, $lt
                if not self._compare(item.get(key), value):
                    return False
            else:
                # This handles exact matches
                if item.get(key) != value:
                    return False
        return True

    def _compare(self, item_value, query_value):
        if item_value is None:
            return False
        for op, value in query_value.items():
            if op == '$gt':
                if not (item_value > value):
                    return False
            elif op == '$lt':
                if not (item_value < value):
                    return False
            elif op == '$gte':
                if not (item_value >= value):
                    return False
            elif op == '$lte':
                if not (item_value <= value):
                    return False
            elif op == '$ne':
                if not (item_value != value):
                    return False
            elif op == '$in':
                if isinstance(item_value, list):
                    if set(item_value).isdisjoint(set(value)):
                        return False
                else:
                    if item_value not in value:
                        return False
            elif op == '$nin':
                if isinstance(item_value, list):
                    if not set(item_value).isdisjoint(set(value)):
                        return False
                else:
                    if item_value in value:
                        return False
            else:
                return False # Unrecognized operator
        return True
