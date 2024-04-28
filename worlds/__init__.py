import dataclasses
import importlib
import os
import pkgutil
import sys
import time
import warnings
import zipimport
from typing import Dict, Iterable, List, Optional, Tuple, TypedDict, Union

import orjson

from Utils import cache_path, local_path, user_path
from .AutoWorld import AutoWorldRegister

local_folder = os.path.dirname(__file__)
user_folder = user_path("worlds") if user_path() != local_path() else None

__all__ = {
    "network_data_package",
    "AutoWorldRegister",
    "world_sources",
    "local_folder",
    "user_folder",
    "GamesPackage",
    "DataPackage",
    "failed_world_loads",
    "load_worlds",
    "load_all_worlds",
}

failed_world_loads: List[str] = []


class GamesPackage(TypedDict, total=False):
    item_name_groups: Dict[str, List[str]]
    item_name_to_id: Dict[str, int]
    location_name_groups: Dict[str, List[str]]
    location_name_to_id: Dict[str, int]
    checksum: str
    version: int  # TODO: Remove support after per game data packages API change.


class DataPackage(TypedDict):
    games: Dict[str, GamesPackage]


@dataclasses.dataclass(order=True)
class WorldSource:
    path: str  # typically relative path from this module
    is_zip: bool = False
    relative: bool = True  # relative to regular world import folder
    time_taken: Optional[float] = None

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
                if hasattr(importer, "find_spec"):  # new in Python 3.10
                    spec = importer.find_spec(os.path.basename(self.path).rsplit(".", 1)[0])
                    assert spec, f"{self.path} is not a loadable module"
                    mod = importlib.util.module_from_spec(spec)
                else:  # TODO: remove with 3.8 support
                    mod = importer.load_module(os.path.basename(self.path).rsplit(".", 1)[0])

                mod.__package__ = f"worlds.{mod.__package__}"
                mod.__name__ = f"worlds.{mod.__name__}"
                sys.modules[mod.__name__] = mod
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", message="__package__ != __spec__.parent")
                    # Found no equivalent for < 3.10
                    if hasattr(importer, "exec_module"):
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
            import logging
            logging.exception(file_like.read())
            failed_world_loads.append(os.path.basename(self.path).rsplit(".", 1)[0])
            return False


def scan_worlds() -> List[WorldSource]:
    # find potential world containers, currently folders and zip-importable .apworld's
    sources: List[WorldSource] = []
    for folder in (folder for folder in (user_folder, local_folder) if folder):
        relative = folder == local_folder
        for entry in os.scandir(folder):
            # prevent loading of __pycache__ and allow _* for non-world folders, disable files/folders starting with "."
            if not entry.name.startswith(("_", ".")):
                file_name = entry.name if relative else os.path.join(folder, entry.name)
                if entry.is_dir():
                    sources.append(WorldSource(file_name, relative=relative))
                elif entry.is_file() and entry.name.endswith(".apworld"):
                    sources.append(WorldSource(file_name, is_zip=True, relative=relative))
    sources.sort()
    return sources


def get_world_paths_from_name(name: str) -> Tuple[str, str]:
    for source, data in world_data.items():
        if data["game"] == name:
            return source, data["path"]
    else:
        raise ModuleNotFoundError(f"No game found for {name}")


class WorldJson(TypedDict):
    game: str
    path: str
    settings: Union[str, None]


def get_worlds_info() -> Tuple[Dict[str, WorldJson], bool]:
    should_update = False
    world_data: Dict[str, WorldJson] = {}
    try:
        cached_time = os.path.getmtime(cached_worlds_path)
        world_data = orjson.loads(pkgutil.get_data(__name__, cached_worlds_path))
        for world in world_sources:
            if os.path.getmtime(world.resolved_path) > cached_time:
                should_update = True
                break
    except (FileNotFoundError, orjson.JSONDecodeError):
        should_update = True

    return world_data, should_update


def load_all_worlds() -> DataPackage:
    # import all submodules to trigger AutoWorldRegister
    games: Dict[str, GamesPackage] = {}
    json_data: Dict[str, WorldJson] = {}
    for world_source in world_sources:
        world_source.load()

    for world_name, world in AutoWorldRegister.world_types.items():
        games[world_name] = world.get_data_package_data()
        # GitHub runners won't allow me to write to their cache
        if "runner" in cached_worlds_path:
            continue
        json_name = [name for name in world.__module__.split(".") if "world" not in name][0]
        if world.zip_path:
            json_name += ".apworld"
        world_json: WorldJson = {"game": world.game, "path": world.__file__,
                                 "settings": str(world.settings_key) if hasattr(world, "settings") else None}
        json_data[json_name] = world_json

    if "runner" not in cached_worlds_path:
        with open(cached_worlds_path, "wb") as f:
            f.write(orjson.dumps(json_data))
    return DataPackage(games=games)


def load_worlds(games: Union[Iterable[str], str]) -> DataPackage:
    if isinstance(games, str):
        games = (games,)
    to_load: List[Tuple[str, str]] = [get_world_paths_from_name(game) for game in games]

    for source in world_sources:
        lookup_index = 0 if source.relative else 1
        for paths in to_load:
            if source.path == paths[lookup_index]:
                remove_index = to_load.index(paths)
                break
        else:
            continue
        source.load()
        to_load.pop(remove_index)

    package: Dict[str, GamesPackage] = {}
    for world_name, world in AutoWorldRegister.world_types.items():
        package[world_name] = world.get_data_package_data()

    return DataPackage(games=package)


world_sources = scan_worlds()
cached_worlds_path = cache_path("worlds.json")
world_data, needs_update = get_worlds_info()
# TODO change to check if we need to update once everything expects lazy loading
# if needs_update:
network_data_package = load_all_worlds()
