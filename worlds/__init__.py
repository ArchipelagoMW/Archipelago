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
    version: Version = Version(0, 0, 0)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.path}, is_zip={self.is_zip}, relative={self.relative})"

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
apworlds: list[WorldSource] = []
for world_source in world_sources:
    # load all loose files first:
    if world_source.is_zip:
        apworlds.append(world_source)
    else:
        world_source.load()


from .AutoWorld import AutoWorldRegister

for world_source in world_sources:
    if not world_source.is_zip:
        # look for manifest
        manifest = {}
        for dirpath, dirnames, filenames in os.walk(world_source.resolved_path):
            for file in filenames:
                if file.endswith("archipelago.json"):
                    with open(os.path.join(dirpath, file), mode="r", encoding="utf-8") as manifest_file:
                        manifest = json.load(manifest_file)
                    break
            if manifest:
                break
        game = manifest.get("game")
        if game in AutoWorldRegister.world_types:
            AutoWorldRegister.world_types[game].world_version = tuplize_version(manifest.get("world_version", "0.0.0"))

if apworlds:
    # encapsulation for namespace / gc purposes
    def load_apworlds() -> None:
        global apworlds
        from .Files import APWorldContainer, InvalidDataError
        core_compatible: list[tuple[WorldSource, APWorldContainer]] = []

        def fail_world(game_name: str, reason: str, add_as_failed_to_load: bool = True) -> None:
            if add_as_failed_to_load:
                failed_world_loads.append(game_name)
            logging.warning(reason)

        for apworld_source in apworlds:
            apworld: APWorldContainer = APWorldContainer(apworld_source.resolved_path)
            # populate metadata
            try:
                apworld.read()
            except InvalidDataError as e:
                if version_tuple < (0, 7, 0):
                    logging.error(
                        f"Invalid or missing manifest file for {apworld_source.resolved_path}. "
                        "This apworld will stop working with Archipelago 0.7.0."
                    )
                    logging.error(e)
                else:
                    raise e

            if apworld.minimum_ap_version and apworld.minimum_ap_version > version_tuple:
                fail_world(apworld.game,
                           f"Did not load {apworld_source.path} "
                           f"as its minimum core version {apworld.minimum_ap_version} "
                           f"is higher than current core version {version_tuple}.")
            elif apworld.maximum_ap_version and apworld.maximum_ap_version < version_tuple:
                fail_world(apworld.game,
                           f"Did not load {apworld_source.path} "
                           f"as its maximum core version {apworld.maximum_ap_version} "
                           f"is lower than current core version {version_tuple}.")
            else:
                core_compatible.append((apworld_source, apworld))
        # load highest version first
        core_compatible.sort(
            key=lambda element: element[1].world_version if element[1].world_version else Version(0, 0, 0),
            reverse=True)
        for apworld_source, apworld in core_compatible:
            if apworld.game and apworld.game in AutoWorldRegister.world_types:
                fail_world(apworld.game,
                           f"Did not load {apworld_source.path} "
                           f"as its game {apworld.game} is already loaded.",
                           add_as_failed_to_load=False)
            else:
                apworld_source.load()
                if apworld.game in AutoWorldRegister.world_types:
                    # world could fail to load at this point
                    if apworld.world_version:
                        AutoWorldRegister.world_types[apworld.game].world_version = apworld.world_version
    load_apworlds()
    del load_apworlds

del apworlds

# Build the data package for each game.
network_data_package: DataPackage = {
    "games": {world_name: world.get_data_package_data() for world_name, world in AutoWorldRegister.world_types.items()},
}

