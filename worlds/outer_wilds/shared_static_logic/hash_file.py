import hashlib


# This is a separate file only because Python's import/module system is a mess.
# Apparently any way for pickle_static_data.py to import the local jsonc module either only works
# as a script or only works as a module, and we want this hash_file function in both contexts.
# Since hash_file itself needs no relative imports, making it a separate file works.


def hash_file(path):
    md5 = hashlib.md5()

    with open(path, 'rb') as f:
        content = f.read()
        content = content.replace(b'\r\n', b'\n')
        md5.update(content)

    return md5.hexdigest()
