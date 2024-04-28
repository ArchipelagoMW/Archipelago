import importlib
import os
import pkgutil
import sys
import warnings
import zipimport
import orjson
import time
import dataclasses
from typing import Dict, List, Iterable, Tuple, TypedDict, Optional, Union

from Utils import cache_path, local_path, user_path

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
    return sources


def get_world_by_name(name: str) -> str:
    for world in world_data:
        if world["game"] == name:
            return world
    else:
        raise ModuleNotFoundError(f"No game found that matches {name}")


def get_worlds_info() -> Tuple[Dict[str, Dict[str, str]], bool]:
    should_update = False
    world_data = {}
    try:
        worlds_path = cache_path("worlds.json")
        world_data = orjson.loads(pkgutil.get_data(__name__, worlds_path))
        for world in world_sources:
            if os.path.getmtime(world.resolved_path) > os.path.getmtime(worlds_path):
                should_update = True
                break
    except orjson.JSONDecodeError:
        should_update = True

    return world_data, should_update


def load_all_worlds() -> Tuple[DataPackage, Dict[str, Dict[str, str]]]:
    # import all submodules to trigger AutoWorldRegister
    from .AutoWorld import AutoWorldRegister
    world_sources.sort()

    for world_source in world_sources:
        world_source.load()

    games: Dict[str, GamesPackage] = {}
    json_data: Dict[str, Dict[str, str]] = {}
    for world_name, world in AutoWorldRegister.world_types.items():
        games[world_name] = world.get_data_package_data()
        json_data[world.__module__] = {"game": world.game}
        if getattr(world, "settings", None):
            json_data[world.__module__].update({"settings": str(world.settings_key)})

    return DataPackage(games=games), json_data


def load_worlds(games: Union[Iterable[str], str]) -> DataPackage:
    if isinstance(games, str):
        games = [games]

    from .AutoWorld import AutoWorldRegister
    to_load: List[str] = []
    for source, data in world_data.items():
        if data["game"] in games:
            to_load.append(source)

    for world_source in [source for source in world_sources if source.path in to_load]:
        world_source.load()

    package: Dict[str, GamesPackage] = {}
    for world_name, world in AutoWorldRegister.world_types.items():
        package[world_name] = world.get_data_package_data()
    
    return DataPackage(games=package)


# if typing.TYPE_CHECKING:
# network_data_package = load_all_worlds()


world_sources = scan_worlds()
world_data, needs_update = get_worlds_info()
# TODO change to check if we need to update once everything expects lazy loading
# network_data_package, world_data = load_all_worlds()
network_data_package = load_worlds("The Messenger")
with open(cache_path("worlds.json"), "wb") as f:
    f.write(orjson.dumps(world_data))
