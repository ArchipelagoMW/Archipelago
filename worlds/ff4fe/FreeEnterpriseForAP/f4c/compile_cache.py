import os
import hashlib
import pickle
import re

class CompileCache:
    def __init__(self, path):
        self._cache_path = path
        self._used_names = set()

    def get_block_cache_name(self, block):
        tag = block['type'] + ' ' + block['parameters'].strip()
        tag = re.sub(r'\s+', '_', tag)

        md5 = hashlib.md5()
        sha1 = hashlib.sha1()
        md5.update(block['body'].encode('utf-8'))
        sha1.update(block['body'].encode('utf-8'))

        return '{}_{}_{}'.format(tag, md5.hexdigest(), sha1.hexdigest())

    def load(self, cache_name):
        path = os.path.join(self._cache_path, cache_name)
        if os.path.exists(path):
            self._used_names.add(cache_name)
            with open(path, 'rb') as infile:
                data = pickle.load(infile)
            return data

        return None

    def save(self, cache_name, data):
        path = os.path.join(self._cache_path, cache_name)
        if not os.path.exists(self._cache_path):
            os.makedirs(self._cache_path)
        with open(path, 'wb') as outfile:
            pickle.dump(data, outfile)
        self._used_names.add(cache_name)

    def cleanup(self):
        if not os.path.exists(self._cache_path):
            return

        for filename in os.listdir(self._cache_path):
            filepath = os.path.join(self._cache_path, filename)
            if filename not in self._used_names and os.path.isfile(filepath):
                os.unlink(filepath)
