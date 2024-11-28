import ast
import importlib
import importlib.util
import logging
import os
import pathlib
import sys
import types
import warnings
import zipfile
import zipimport
import time
import dataclasses
from typing import Dict, List, TypedDict, AnyStr

from Utils import local_path, user_path

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
    "GamesPackage",
    "DataPackage",
    "failed_world_loads",
    "ensure_all_worlds_loaded",
}


failed_world_loads: List[str] = []
failed_world_module_loads_set: set[str] = set()
world_sources_by_game: Dict[str, "WorldSource"] = {}
gameless_world_sources: List["WorldSource"] = []
world_sources_by_module: Dict[str, "WorldSource"] = {}
loaded_modules: set[str] = set()


class GamesPackage(TypedDict, total=False):
    item_name_groups: Dict[str, List[str]]
    item_name_to_id: Dict[str, int]
    location_name_groups: Dict[str, List[str]]
    location_name_to_id: Dict[str, int]
    checksum: str


class DataPackage(TypedDict):
    games: Dict[str, GamesPackage]

network_data_package: DataPackage = {
    "games": {}
}

from .AutoWorld import AutoWorldRegister


@dataclasses.dataclass(order=True)
class WorldSource:
    path: str  # typically relative path from this module
    is_zip: bool = False
    relative: bool = True  # relative to regular world import folder
    time_taken: float = -1.0
    game: str | None = None
    module_name: str = dataclasses.field(init=False)

    def __post_init__(self):
        self.module_name, self.game = self.find_game_and_module()
        if self.game is None:
            # warnings.warn(f"Could not determine game for {self.module_name}")
            pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.path}, is_zip={self.is_zip}, relative={self.relative}, game={self.game})"

    @property
    def resolved_path(self) -> str:
        if self.relative:
            return os.path.join(local_folder, self.path)
        return self.path

    def find_game_from_world_info(self, ap_data_file: AnyStr) -> str:
        import json
        ap_data = json.loads(ap_data_file)
        game = ap_data.get("game", None)
        if isinstance(game, str):
            print(f"Found world for {game}")
            return game
        else:
            print("Could not determine game for %s. It will always be loaded." % self.path)
            # warnings.warn("Could not find game in TODO")
            return None

    def find_game_and_module(self) -> tuple[str, str | None]:
        path = self.resolved_path
        if self.is_zip:
            with zipfile.ZipFile(path) as zf:
                directories = [f.name for f in zipfile.Path(zf).iterdir() if f.is_dir()]

                if len(directories) == 1 and directories[0] in pathlib.Path(path).stem:
                    module_name = directories[0]
                try:
                    init_file = zf.read(module_name + "/ap_info.json")
                except KeyError:
                    return "worlds." + module_name, None
                else:
                    return "worlds." + module_name, self.find_game_from_world_info(init_file)
        else:
            full_path = os.path.join(path, 'ap_info.json')
            if os.path.isfile(full_path):
                with open(full_path, "r") as f:
                    return "worlds." + self.path, self.find_game_from_world_info(f.read())
            else:
                # warnings.warn(f"Could not open {full_path} to determine game")
                return "worlds." + self.path, None


# find potential world containers, currently folders and zip-importable .apworld's
world_sources: List[WorldSource] = []
for folder in (folder for folder in (user_folder, local_folder) if folder):
    relative = folder == local_folder
    for entry in os.scandir(folder):
        # prevent loading of __pycache__ and allow _* for non-world folders, disable files/folders starting with "."
        if not entry.name.startswith(("_", ".")):
            file_name = entry.name if relative else os.path.join(folder, entry.name)
            source = None
            try:
                if entry.is_dir():
                    if os.path.isfile(os.path.join(entry.path, '__init__.py')):
                        source = WorldSource(file_name, relative=relative)
                    elif os.path.isfile(os.path.join(entry.path, '__init__.pyc')):
                        source = WorldSource(file_name, relative=relative)
                    else:
                        logging.warning(f"excluding {entry.name} from world sources because it has no __init__.py")
                elif entry.is_file() and entry.name.endswith(".apworld"):
                    source = WorldSource(file_name, is_zip=True, relative=relative)

                if source is not None:
                    world_sources.append(source)
                    # todo: Is `world_sources_by_game` even needed?
                    if source.game is not None:
                        world_sources_by_game[source.game] = source
                    else:
                        gameless_world_sources.append(source)
                    world_sources_by_module[source.module_name] = source

            except Exception:
                # A single world failing can still mean enough is working for the user, log and carry on
                import traceback
                import io

                file_like = io.StringIO()
                print(f"Could not load world {file_name}:", file=file_like)
                traceback.print_exc(file=file_like)
                file_like.seek(0)
                logging.exception(file_like.read())
                failed_world_loads.append(os.path.basename(file_name).rsplit(".", 1)[0])


class ZipLoader:
    def __init__(self, source, importer, loader):
        self.source = source
        self.importer = importer
        self.loader = loader

    def exec_module(self, mod):
        if hasattr(self.loader, "exec_module"):
            self.loader.exec_module(mod)
        mod.__package__ = f"worlds.{mod.__package__}"

        mod.__name__ = f"worlds.{mod.__name__}"
        sys.modules[mod.__name__] = mod
        loaded_modules.add(mod.__name__)
        # self.source.time_taken = time.perf_counter() - self.source.time_taken

        # This causes the module to be loaded twice, causing the world to be registered twice and fail the second
        # time...
        # with warnings.catch_warnings():
        #     warnings.filterwarnings("ignore", message="__package__ != __spec__.parent")
        #     # Found no equivalent for < 3.10
        #     if hasattr(self.importer, "exec_module"):
        #         self.importer.exec_module(mod)

    def create_module(self, spec):
        # Use default module creation according to importlib.util.module_from_spec(spec)
        return None
        # mod = self.create(spec)
        # #mod = self.loader.create_module(spec)
        # #mod = types.ModuleType(spec.name)
        # mod = importlib.util.module_from_spec(spec)
        #
        # #mod.__package__ = f"worlds.{mod.__package__}"
        #
        # mod.__package__ = f"worlds.{spec.parent}"
        #
        # mod.__name__ = f"worlds.{mod.__name__}"
        #
        # return mod


class NormalLoader:
    world_source: WorldSource
    load_time = -1.0
    def __init__(self, base_loader, world_source):
        self.base_loader = base_loader
        self.world_source = world_source

    def exec_module(self, module):
        start = time.perf_counter()
        self.base_loader.exec_module(module)
        self.load_time += time.perf_counter() - start
        self.world_source.time_taken += self.load_time

    def create_module(self, spec):
        start = time.perf_counter()
        mod = importlib.util.module_from_spec(spec)
        self.load_time = time.perf_counter() - start
        return mod


class WorldFinder:
    @staticmethod
    def find_spec(name: str, path, target_module=None):
        if name.startswith("worlds.") and name in world_sources_by_module:
            print(f"Attempting to find spec with name '{name}', path '{path}' and target_module '{target_module}'")
            source = world_sources_by_module[name]
            # start = time.perf_counter()
            if source.is_zip:
                # source.time_taken = start
                importer = zipimport.zipimporter(source.resolved_path)
                spec = importer.find_spec(os.path.basename(source.path).rsplit(".", 1)[0])
                assert spec, f"{source.path} is not a loadable module"
                spec.loader = ZipLoader(source, importer, spec.loader)
                return spec
            else:
                # The default meta path finder can load these.
                # todo: What about .pyc?
                loaded_modules.add(name)
                return None
                # spec = importlib.util.find_spec(f".{source.path}", "worlds")
                # spec.loader = NormalLoader(spec.loader, source)
                # source.time_taken = time.perf_counter() - start
                # return spec
        else:
            print(f"skipping {name} with path {path}")
            return None


# Here's where the magic happens
sys.meta_path.append(WorldFinder())


def ensure_all_worlds_loaded(games: set[str] | None = None, log_skipped=True):
    if not games:
        # Ensure all worlds are loaded.
        sources = world_sources
    else:
        # Load everything we can by game name, and then load everything that has not specified a game name.
        sources = [world_sources_by_game[game] for game in games if game in world_sources_by_game]
        sources.extend(gameless_world_sources)
    print(f"starting to load {len(sources)} worlds")
    for source in sources:
        module_name = source.module_name
        if module_name in sys.modules and module_name in loaded_modules:
            print(f"{module_name} already loaded")
            #logging.info("%s already loaded", module_name)
            # Already loaded.
            continue
        if module_name in failed_world_module_loads_set:
            print(f"{module_name} already failed to load")
            #logging.info("%s already failed to load", module_name)
            # Already failed to load.
            continue
        print(f"Ensuring {module_name} is loaded")
        #logging.info(f"Ensuring {module_name} is loaded")
        try:
            # loaded_games = set(AutoWorldRegister.world_types.keys())
            start = time.perf_counter()
            importlib.import_module(module_name, "worlds")
            source.time_taken = time.perf_counter() - start
            if source.game is not None and source.game not in AutoWorldRegister.world_types:
                warnings.warn(f"World {source.module_name} claims to contain the game {source.game}, but no world for"
                              f" this game was found after loading.")
                assert source.game in AutoWorldRegister.world_types
            # todo: We don't currently have a good way to pair up modules with games. It would be good to be able to
            #  check that a loaded world
            # if source.game is not None:
            #     newly_loaded_games = set(AutoWorldRegister.world_types.keys())
            #     newly_loaded_games.difference_update(loaded_games)
            #     if len(newly_loaded_games) == 1:
            #         new_game = next(iter(newly_loaded_games))
            #         if new_game != source.game:
            #             warnings.warn(f"Loaded game '{new_game}' did not match the game name from ap_info.json:"
            #                           f" {source.game}")
        except Exception:
            # A single world failing can still mean enough is working for the user, log and carry on
            import traceback
            import io
            file_like = io.StringIO()
            print(f"Could not load world {source}:", file=file_like)
            traceback.print_exc(file=file_like)
            file_like.seek(0)
            logging.exception(file_like.read())
            failed_world_loads.append(os.path.basename(source.path).rsplit(".", 1)[0])
            failed_world_module_loads_set.add(module_name)

#
# """
#     for world_source in world_sources:
#         game = world_source.game
#         if games is not None and game is not None and game not in games:
#             AutoWorldRegister.unloaded_world_types.add(game)
#         else:
#             world_source.load()"""
#
# from .AutoWorld import AutoWorldRegister
#
# # import all submodules to trigger AutoWorldRegister
# world_sources.sort()
# for world_source in world_sources:
#     try:
#         world_source.find_game()
#     except Exception as ex:
#         import traceback
#         print(traceback.format_exc())
#
#
# def load_worlds(games: set[str] | None = None):
#     global worlds_loaded
#     if worlds_loaded:
#         warnings.warn("Attempted to load worlds when they are already loaded", stacklevel=-1)
#         return
#
#
#     for world_source in world_sources:
#         game = world_source.game
#         if games is not None and game is not None and game not in games:
#             AutoWorldRegister.unloaded_world_types.add(game)
#         else:
#             world_source.load()
#
#     # Build the data package for each game.
#     data_package_games = network_data_package["games"]
#     for world_name, world in AutoWorldRegister.world_types.items():
#         data_package_games[world_name] = world.get_data_package_data()
#
#     worlds_loaded = True
