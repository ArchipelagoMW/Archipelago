import datetime
import pymongo

SEED_LIFETIME_IN_SECONDS = 60 * 60 * 24 * 7

class CachedSeed:
    def __init__(self, doc):
        self.metadata = dict()
        for k in doc:
            if k != '_id':
                setattr(self, k, doc[k])

class SeedStore:
    def __init__(self, db):
        self._db = db

    def create_indices(self):
        self._db['seeds'].create_index('seed_id', unique=True)
        self._db['seeds'].create_index(
            [('binary_flags', pymongo.ASCENDING), ('seed', pymongo.ASCENDING)], 
            unique=True)
        self._db['seeds'].create_index('lastAccessedTime', expireAfterSeconds=SEED_LIFETIME_IN_SECONDS)

    def put(self, seed_id, patch_data, **metadata):
        now = datetime.datetime.utcnow()
        doc = {
            'seed_id' : seed_id,
            'createdTime' : now,
            'lastAccessedTime' : now,
            'patch' : patch_data
            }
        doc.update(metadata)

        self._db['seeds'].insert_one(doc)

    def lookup(self, binary_flags=None, seed=None):
        cached_seed = self._db['seeds'].find_one(
            {'binary_flags' : binary_flags, 'seed' : seed}, 
            {'seed_id' : 1}
            )

        if cached_seed is None:
            return None
        else:
            return cached_seed['seed_id']

    def get(self, seed_id):
        doc = self._db['seeds'].find_one({'seed_id' : seed_id}, {'_id' : 0})
        if doc is not None:
            access_time = datetime.datetime.utcnow()
            doc['lastAccessedTime'] = access_time
            self._db['seeds'].update_one({'seed_id' : seed_id}, {'$set' : {'lastAccessedTime' : access_time}})
            return CachedSeed(doc)
        else:
            return None

    def set_metadata(self, seed_id, **metadata):
        assignments = {f'metadata.{k}' : metadata[k] for k in metadata}
        self._db['seeds'].update_one({'seed_id' : seed_id}, {'$set' : assignments})

