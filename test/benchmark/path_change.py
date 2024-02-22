import sys
import os


def change_home():
    """Allow scripts to run from "this" folder."""
    old_home = os.path.dirname(__file__)
    sys.path.remove(old_home)
    new_home = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
    os.chdir(new_home)
    sys.path.append(new_home)
    # fallback to local import
    sys.path.append(old_home)

    from Utils import local_path
    local_path.cached_path = new_home
