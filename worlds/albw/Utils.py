import orjson
import os
import shutil
import sys
import tempfile
import zipfile
from Utils import local_path

def setup_lib():
    # clean up any files from old versions of the apworld
    for path in [local_path("."), local_path("lib")]:
        if os.path.exists(path):
            for entry in os.scandir(path):
                if entry.name.startswith("albwrandomizer"):
                    fullpath = os.path.join(path, entry.name)
                    if entry.is_dir():
                        shutil.rmtree(fullpath)
                    else:
                        os.remove(fullpath)

    apworld_path = os.path.dirname(os.path.dirname(__file__))
    if apworld_path.endswith(".apworld"):
        with zipfile.ZipFile(apworld_path, "r") as apworld:
            with apworld.open("albw/archipelago.json", "r") as manifest_file:
                manifest = orjson.loads(manifest_file.read())
            version = manifest["world_version"]
            tmp_path = os.path.join(tempfile.gettempdir(), f"albwrandomizer_{version}")
            try:
                if os.path.exists(tmp_path):
                    shutil.rmtree(tmp_path)
                os.mkdir(tmp_path)
                randomizer_path = os.path.join(tmp_path, "albwrandomizer")
                os.mkdir(randomizer_path)
                for info in apworld.infolist():
                    if not info.is_dir() and info.filename.startswith("albw/albwrandomizer/"):
                        info.filename = os.path.basename(info.filename)
                        apworld.extract(info, randomizer_path)
            except:
                pass
            if not tmp_path in sys.path:
                sys.path.append(tmp_path)
    else:
        path = os.path.join(os.path.dirname(__file__), "albwrandomizer")
        if not path in sys.path:
            sys.path.append(path)