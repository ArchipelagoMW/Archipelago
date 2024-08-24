import os
import pickle

class FlatFileCache:
    def __init__(self, path):
        self.path = path

    def load(self, *timestamps):
        if os.path.exists(self.path):
            newest_mtime = None
            for timestamp in timestamps:
                # if timestamp is a path, then use the modified time of the path
                if type(timestamp) is str and os.path.exists(timestamp):
                    mtime = os.path.getmtime(timestamp)
                else:
                    mtime = int(timestamp)

                if newest_mtime is None or newest_mtime < mtime:
                    newest_mtime = mtime

            if newest_mtime is None or os.path.getmtime(self.path) > newest_mtime:
                # cached file is valid, load it and return its data
                with open(self.path, "rb") as infile:
                    result = pickle.load(infile)

                return result

        # cached file is invalid
        return None

    def save(self, **kwargs):
        with open(self.path, 'wb') as outfile:
            pickle.dump(kwargs, outfile)
