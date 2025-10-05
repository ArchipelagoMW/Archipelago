import importlib
import importlib.util
import logging
import os
import sys
import warnings
import zipimport
import time
import dataclasses
import json
from typing import List

from NetUtils import DataPackage
from Utils import local_path, user_path, Version, version_tuple, tuplize_version

local_folder = os.path.dirname(__file__)
user_folder = user_path("worlds") if user_path() != local_path() else user_path("custom_worlds")
try:
    os.makedirs(user_folder, exist_ok=True)
except OSError:  # can't access/write?
    user_folder = None

__all__ = [
    "network_data_package",
    "AutoWorldRegister",
    "world_sources",
    "local_folder",
    "user_folder",
    "failed_world_loads",
]


failed_world_loads: List[str] = []


@dataclasses.dataclass(order=True)
class WorldSource:
    path: str  # typically relative path from this module
    is_zip: bool = False
    relative: bool = True  # relative to regular world import folder
    time_taken: float = -1.0
    game: str | None = None # None if no manifest
    minimum_ap_version: Version | None = None
    maximum_ap_version: Version | None = None
    version: Version = Version(0, 0, 0)

    def __post_init__(self):
        # try to load manifest data
        if self.is_zip:
            apworld = APWorldContainer(self.resolved_path)
            try:
                apworld.read()
            except InvalidDataError as e:
                if version_tuple < (0, 7, 0):
                    logging.error(
                        f"Invalid or missing manifest file for {self.resolved_path}. "
                        "This apworld will stop working with Archipelago 0.7.0."
                    )
                    logging.error(e)
                else:
                    raise e

            self.game = apworld.game
            if apworld.world_version:
                self.version = apworld.world_version
        else:
            manifest = {}
            for dirpath, dirnames, filenames in os.walk(self.resolved_path):
                for file in filenames:
                    if file.endswith("archipelago.json"):
                        manifest = json.load(open(os.path.join(dirpath, file), "r"))
                        break
                if manifest:
                    break
            self.game = manifest.get("game")
            self.version = Version(*tuplize_version(manifest.get("world_version", "0.0.0")))

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self.path}, is_zip={self.is_zip}, relative={self.relative}, "
                f"game={self.game!r}, version={self.version}, minimum_ap_version={self.minimum_ap_version}), "
                f"maximum_ap_version={self.maximum_ap_version}")

    @property
    def resolved_path(self) -> str:
        if self.relative:
            return os.path.join(local_folder, self.path)
        return self.path

    def load(self) -> bool:
        try:
            start = time.perf_counter()
            if self.is_zip:
                importer = zipimport.zipimporter(self.resolved_path)
                spec = importer.find_spec(os.path.basename(self.path).rsplit(".", 1)[0])
                assert spec, f"{self.path} is not a loadable module"
                mod = importlib.util.module_from_spec(spec)

                mod.__package__ = f"worlds.{mod.__package__}"

                mod.__name__ = f"worlds.{mod.__name__}"
                sys.modules[mod.__name__] = mod
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", message="__package__ != __spec__.parent")
                    importer.exec_module(mod)
            else:
                importlib.import_module(f".{self.path}", "worlds")

            if self.game is not None:
                # game should be loaded now
                AutoWorldRegister.world_types[self.game].world_version = self.version

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


from .AutoWorld import AutoWorldRegister
from .Files import APWorldContainer, InvalidDataError

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

# load in order of version
world_sources.sort(key=lambda source: source.version, reverse=True)

def fail_world(game_name: str, reason: str, add_as_failed_to_load: bool = True) -> None:
    if add_as_failed_to_load:
        failed_world_loads.append(game_name)
    logging.warning(reason)

# load all worlds so they are registered
for world_source in world_sources:
    if world_source.minimum_ap_version and world_source.minimum_ap_version > version_tuple:
        fail_world(world_source.game,
                    f"Did not load {world_source.path} "
                    f"as its minimum core version {world_source.minimum_ap_version} "
                    f"is higher than current core version {version_tuple}.")
    elif world_source.maximum_ap_version and world_source.maximum_ap_version < version_tuple:
        fail_world(world_source.game,
                    f"Did not load {world_source.path} "
                    f"as its maximum core version {world_source.maximum_ap_version} "
                    f"is lower than current core version {version_tuple}.")
    elif world_source.game and world_source.game in AutoWorldRegister.world_types:
        fail_world(world_source.game,
                    f"Did not load {world_source.path} "
                    f"as its game {world_source.game} is already loaded.",
                    add_as_failed_to_load=False)
    else:
        world_source.load()

# Build the data package for each game.
network_data_package: DataPackage = {
    "games": {world_name: world.get_data_package_data() for world_name, world in AutoWorldRegister.world_types.items()},
}

