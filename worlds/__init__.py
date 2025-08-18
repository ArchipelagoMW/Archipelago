import importlib
import importlib.util
import logging
import os
import sys
import warnings
import zipimport
import time
import dataclasses
import zipfile
import json
import platform
from typing import List

from NetUtils import DataPackage
from Utils import local_path, user_path, version_tuple, tuplize_version

local_folder = os.path.dirname(__file__)
user_folder = user_path("worlds") if user_path() != local_path() else user_path("custom_worlds")
try:
    os.makedirs(user_folder, exist_ok=True)
except OSError:  # can't access/write?
    user_folder = None

__all__ = {
    "network_data_package",
    "AutoWorldRegister",
    "world_sources",
    "local_folder",
    "user_folder",
    "failed_world_loads",
}


failed_world_loads: List[str] = []


@dataclasses.dataclass(order=True)
class WorldSource:
    path: str  # typically relative path from this module
    is_zip: bool = False
    relative: bool = True  # relative to regular world import folder
    time_taken: float = -1.0

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.path}, is_zip={self.is_zip}, relative={self.relative})"

    @property
    def resolved_path(self) -> str:
        if self.relative:
            return os.path.join(local_folder, self.path)
        return self.path

    def check_manifest(self, manifest: Dict[str, Any]) -> None:
        if "min_generator_version" in manifest:
            min_ver = tuplize_version(manifest["min_generator_version"])
            if min_ver > version_tuple:
                raise Exception(f"World \"{manifest['game']}\" requires generator version {min_ver.as_simple_string()}"
                                f" or higher, however generator is of version {version_tuple.as_simple_string()}")
        if "max_generator_version" in manifest:
            max_ver = tuplize_version(manifest["max_generator_version"])
            if max_ver < version_tuple:
                raise Exception(f"World \"{manifest['game']}\" requires generator version {max_ver.as_simple_string()}"
                                f" or lower, however generator is of version {version_tuple.as_simple_string()}")
        if "arch" in manifest:
            if manifest["arch"] != "any" and manifest["arch"] != platform.machine():
                raise Exception(f"World \"{manifest['game']}\" is intended for architecture {manifest['arch']}, "
                                f"however system is of architecture {platform.machine}")
        if "os" in manifest:
            if manifest["os"] != "any" and manifest["os"] != platform.system():
                raise Exception(f"World \"{manifest['game']}\" is intended for os {manifest['os']}, "
                                f"however system is of os {platform.system}")
        if "pyversion" in manifest:
            if manifest["pyversion"] != "any" and manifest["pyversion"] != f"{sys.version_info[0]}.{sys.version_info[1]}":
                raise Exception(f"World \"{manifest['game']}\" is intended for Python version {manifest['pyversion']}, "
                                f"however Python version {sys.version_info[0]}.{sys.version_info[1]} is being used.")

    def load(self) -> bool:
        try:
            start = time.perf_counter()
            if self.is_zip:
                with zipfile.ZipFile(self.resolved_path) as zf:
                    if zipfile.Path(zf, os.path.join(self.path, "metadata.json")).exists():
                        manifest = json.loads(zf.read(os.path.join(self.path, "metadata.json")))
                        self.check_manifest(manifest)
                importer = zipimport.zipimporter(self.resolved_path)
                spec = importer.find_spec(os.path.basename(self.path).rsplit(".", 1)[0].split('-', 1)[0])
                assert spec, f"{self.path} is not a loadable module"
                mod = importlib.util.module_from_spec(spec)

                mod.__package__ = f"worlds.{mod.__package__}"

                mod.__name__ = f"worlds.{mod.__name__}"
                sys.modules[mod.__name__] = mod
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", message="__package__ != __spec__.parent")
                    importer.exec_module(mod)
            else:
                if os.path.exists(os.path.join(self.resolved_path, "metadata.json")):
                    self.check_manifest(json.load(open(os.path.join(self.resolved_path, "metadata.json"), "r")))
                importlib.import_module(f".{self.path}", "worlds")
            self.time_taken = time.perf_counter()-start
            return True

        except Exception:
            # A single world failing can still mean enough is working for the user, log and carry on
            import traceback
            import io
            file_like = io.StringIO()
            print(f"Could not load world {self}:", file=file_like)
            traceback.print_exc(file=file_like)
            file_like.seek(0)
            logging.exception(file_like.read())
            failed_world_loads.append(os.path.basename(self.path).rsplit(".", 1)[0])
            return False


# find potential world containers, currently folders and zip-importable .apworld's
world_sources: List[WorldSource] = []
for folder in (folder for folder in (user_folder, local_folder) if folder):
    relative = folder == local_folder
    for entry in os.scandir(folder):
        # prevent loading of __pycache__ and allow _* for non-world folders, disable files/folders starting with "."
        if not entry.name.startswith(("_", ".")):
            file_name = entry.name if relative else os.path.join(folder, entry.name)
            if entry.is_dir():
                if os.path.isfile(os.path.join(entry.path, '__init__.py')):
                    world_sources.append(WorldSource(file_name, relative=relative))
                elif os.path.isfile(os.path.join(entry.path, '__init__.pyc')):
                    world_sources.append(WorldSource(file_name, relative=relative))
                else:
                    logging.warning(f"excluding {entry.name} from world sources because it has no __init__.py")
            elif entry.is_file() and entry.name.endswith(".apworld"):
                world_sources.append(WorldSource(file_name, is_zip=True, relative=relative))

# import all submodules to trigger AutoWorldRegister
world_sources.sort()
for world_source in world_sources:
    world_source.load()

# Build the data package for each game.
from .AutoWorld import AutoWorldRegister

network_data_package: DataPackage = {
    "games": {world_name: world.get_data_package_data() for world_name, world in AutoWorldRegister.world_types.items()},
}

