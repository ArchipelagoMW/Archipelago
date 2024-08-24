import os

USE_JSON = False

if USE_JSON:
    import json
    serializer = json
    FILE_MODE = ''
else:
    import pickle
    serializer = pickle
    FILE_MODE = 'b'

class AbstractStore:
    def __init__(self):
        pass

    def has(self, key):
        return False

    def get(self, key):
        return None

    def update(self, key, **fields):
        pass

class FileStore(AbstractStore):
    def __init__(self, path):
        self._path = path
        if not os.path.isdir(self._path):
            os.makedirs(self._path)

    def _key_path(self, key):
        return os.path.join(self._path, key)

    def has(self, key):
        return os.path.exists(self._key_path(key))

    def get(self, key):
        if os.path.exists(self._key_path(key)):
            with open(self._key_path(key), 'r' + FILE_MODE) as infile:
                return serializer.load(infile)

        return None

    def update(self, key, **fields):
        doc = self.get(key)
        if doc is None:
            doc = fields
        else:
            doc.update(fields)

        with open(self._key_path(key), 'w' + FILE_MODE) as outfile:
            serializer.dump(doc, outfile)
