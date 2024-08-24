import store
import os
import time

class CachedSeed:
    pass

class SeedCache:
    def __init__(self):
        self._store = store.FileStore(os.path.join(os.path.dirname(__file__), '_seeds'))

    def make_key(self, flags, seed):
        return f'{flags}.{seed}'

    def has(self, key):
        return self._store.has(key)

    def get(self, key):
        doc = self._store.get(key)
        if doc is None:
            return None

        cached_seed = CachedSeed()
        for k in doc:
            setattr(cached_seed, k, doc[k])

        return cached_seed

    def put(self, task_result):
        key = self.make_key(task_result['binary_flags'], task_result['seed'])
        self._store.update(key, **task_result)
        return key
