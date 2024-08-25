import logging
import os
import pickle

class FlatFileCache:
    def __init__(self, path):
        self.path = path

    def load(self, *timestamps):
        if os.path.exists(self.path):
            return None

        # cached file is invalid
        return None

    def save(self, **kwargs):
        with open(self.path, 'wb') as outfile:
            pickle.dump(kwargs, outfile)
