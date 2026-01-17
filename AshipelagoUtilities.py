import os
import sys

def setup_lib_path(file: str):
    """Takes the local dependencies and moves them out of the apworld zip file to a temporary directory so the DLLs can be loaded."""
    base_path = os.path.dirname(file)
    lib_path = os.path.join(base_path, "lib")

    print(f"Using local lib folder for: {base_path}")
    if lib_path not in sys.path:
        sys.path.append(lib_path)
    print(f"lib folder added to path: {lib_path}")
    return lib_path
