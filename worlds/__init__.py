import importlib
import importlib.abc
import importlib.machinery
import importlib.util
import logging
import os
import pathlib
import sys
import types
import typing
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
    "world_sources_by_game",
    "world_sources_by_module",
    "gameless_world_sources",
    "local_folder",
    "user_folder",
    "GamesPackage",
    "DataPackage",
    "failed_world_loads",
    "ensure_worlds_loaded",
}


failed_world_loads: List[str] = []
failed_world_module_loads_set: set[str] = set()
world_sources_by_game: Dict[str, "WorldSource"] = {}
gameless_world_sources: List["WorldSource"] = []
world_sources_by_module: Dict[str, "WorldSource"] = {}
loaded_modules: set[str] = set()
world_loading_enabled = True
"""Set to False to disable world loading"""


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
"""
Modified by AutoWorldRegister as new worlds are registered.

Call `ensure_worlds_loaded()` before accessing if a datapackage containing all games is required.
"""


from .AutoWorld import AutoWorldRegister


@dataclasses.dataclass(order=True)
class WorldSource:
    path: str  # typically relative path from this module
    type: typing.Literal["zip", "py", "pyc"]
    relative: bool = True  # relative to regular world import folder
    time_taken: float = -1.0
    game: str | None = dataclasses.field(init=False)
    module_name: str = dataclasses.field(init=False)

    def __post_init__(self):
        self.module_name, self.game = self.find_game_and_module()
        if self.game is None:
            # warnings.warn(f"Could not determine game for {self.module_name}")
            pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.path}, type={self.type}, relative={self.relative}, game={self.game})"

    @property
    def is_zip(self):
        return self.type == "zip"

    @property
    def resolved_path(self) -> str:
        if self.relative:
            return os.path.join(local_folder, self.path)
        return self.path

    @property
    def resolved_file_path(self) -> str:
        file_type = self.type
        if file_type == "zip":
            return self.resolved_path
        elif file_type == "py":
            return os.path.join(self.resolved_path, "__init__.py")
        else:
            return os.path.join(self.resolved_path, "__init__.pyc")

    def find_game_from_world_info(self, ap_data_file: AnyStr) -> str | None:
        import json
        ap_data = json.loads(ap_data_file)
        game = ap_data.get("game", None)
        if isinstance(game, str):
            logging.debug("%s provides the game '%s'", self.path, game)
            return game
        else:
            logging.warning("%s provides an ap_info.json, but no game could be found within it. It will always be"
                            " loaded when specific games are requested to be loaded.", self.path)
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
                    logging.warning("No ap_info.json found for %s", self.path)
                    return "worlds." + module_name, None
                else:
                    return "worlds." + module_name, self.find_game_from_world_info(init_file)
        else:
            full_path = os.path.join(path, 'ap_info.json')
            if os.path.isfile(full_path):
                with open(full_path, "r") as f:
                    return "worlds." + self.path, self.find_game_from_world_info(f.read())
            else:
                logging.warning("No ap_info.json found for %s", self.path)
                # warnings.warn(f"Could not open {full_path} to determine game")
                return "worlds." + self.path, None


# find potential world containers, currently folders and zip-importable .apworld's
world_sources: List[WorldSource] = []


def scan_for_worlds_on_module_load():
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
                            source = WorldSource(file_name, relative=relative, type="py")
                        elif os.path.isfile(os.path.join(entry.path, '__init__.pyc')):
                            source = WorldSource(file_name, relative=relative, type="pyc")
                        else:
                            logging.warning(f"excluding {entry.name} from world sources because it has no __init__.py")
                    elif entry.is_file() and entry.name.endswith(".apworld"):
                        source = WorldSource(file_name, relative=relative, type="zip")

                    if source is not None:
                        module_name = source.module_name
                        if module_name in world_sources_by_module:
                            raise RuntimeError(f"World container for {module_name} already exists."
                                               f"\nAlready found: {world_sources_by_module[module_name]}"
                                               f"\nDuplicate: {source}")

                        world_sources.append(source)

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


scan_for_worlds_on_module_load()
del scan_for_worlds_on_module_load


# `zipimport.zipimporter` implements `create_module`, `exec_module`, `is_package` and `load_module` (deprecated), so it
# duck-types as a Loader, but we'll include the Loader abstract base class as a base to make type checkers expecting a
# Loader happy.
class ZipWorldLoader(zipimport.zipimporter, importlib.abc.Loader):
    world_source: WorldSource

    def __init__(self, world_source: WorldSource):
        super().__init__(world_source.resolved_file_path)
        self.world_source = world_source

    # zipimporter implements `exec_module` as of Python 3.10, replacing the deprecated `load_module`.
    def exec_module(self, module):
        start = time.perf_counter()
        super().exec_module(module)
        loaded_modules.add(module.__name__)
        self.world_source.time_taken = time.perf_counter() - start


class SourceWorldLoader(importlib.machinery.SourceFileLoader):
    world_source: WorldSource

    def __init__(self, fullname, world_source: "WorldSource"):
        super().__init__(fullname, world_source.resolved_file_path)
        self.world_source = world_source

    def exec_module(self, module):
        start = time.perf_counter()
        super().exec_module(module)
        loaded_modules.add(module.__name__)
        self.world_source.time_taken = time.perf_counter() - start


class BytecodeWorldLoader(importlib.machinery.SourcelessFileLoader):
    world_source: WorldSource

    def __init__(self, fullname, world_source: WorldSource):
        super().__init__(fullname, world_source.resolved_file_path)
        self.world_source = world_source

    def exec_module(self, module):
        start = time.perf_counter()
        super().exec_module(module)
        loaded_modules.add(module.__name__)
        self.world_source.time_taken = time.perf_counter() - start


class WorldFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname: str, path: typing.Sequence[str] | None, target: types.ModuleType | None = None
                  ) -> importlib.machinery.ModuleSpec | None:
        if fullname.startswith("worlds.") and fullname in world_sources_by_module:
            if not world_loading_enabled:
                raise RuntimeError(f"Could not load world {fullname}, world loading is not allowed at this time.")

            logging.debug("Attempting to find spec with name '%s', path '%s' and target_module '%s'",
                          fullname, path, target)
            world_source = world_sources_by_module[fullname]
            loader: importlib.abc.Loader
            if world_source.is_zip:
                loader = ZipWorldLoader(world_source)
                spec = importlib.util.spec_from_loader(fullname, loader)
                if spec is None:
                    raise RuntimeError(f"{world_source.path} is not a loadable module")
                return spec
            else:
                if world_source.type == "py":
                    loader = SourceWorldLoader(fullname, world_source)
                else:
                    loader = BytecodeWorldLoader(fullname, world_source)
                return importlib.util.spec_from_file_location(fullname, world_source.resolved_file_path,
                                                              loader=loader,
                                                              submodule_search_locations=[world_source.resolved_path])
        else:
            # Handling of other modules will be left to the other meta path finders in sys.meta_path.
            return None


# This is where the magic happens.
# Insert our meta path finder for worlds before the others so that we intercept the builtin meta path finder that is
# usually able to handle importing non-zip worlds.
# Our meta path finder is also capable of importing zipped worlds.
# -- If it is not desired to intercept the loading of non-zip worlds (Python seems to be capable of loading them itself,
# but you lose easier module execution benchmarking), then the meta path finder can be appended to the end of the list
# instead, and it will only handle zipped worlds.
sys.meta_path.insert(0, WorldFinder())


def ensure_worlds_loaded(games: set[str] | str | None = None):
    if isinstance(games, str):
        games = {games}

    if games is None:
        # Ensure all worlds are loaded.
        sources = world_sources
    elif len(games) == 0:
        return
    else:
        # Load everything by game name, and then load everything that has not specified a game name. It's possible that
        # there is a world that provides a game to be loaded, but does not provide the meta file used to determine game
        # provided by a world.
        # All worlds with unspecified games are always loaded in-case one of them tries to provide a world for a game
        # that has already been loaded, in which case an error should be logged.
        sources = [world_sources_by_game[game] for game in games if game in world_sources_by_game]
        sources.extend(gameless_world_sources)
    logging.debug(f"Ensuring {len(sources)} worlds are loaded.")
    for world_source in sources:
        module_name = world_source.module_name
        # `sys.modules` seems to be able to contain modules that cannot be used because they need reloading, so we also
        # check `loaded_modules` and let `importlib.import_module()` handle the reloading if the module needs it.
        if module_name in sys.modules and module_name in loaded_modules:
            # Already loaded.
            logging.debug("%s already loaded", module_name)
            continue
        if module_name in failed_world_module_loads_set:
            # Already failed to load.
            logging.debug("%s already failed to load", module_name)
            continue

        logging.debug(f"Ensuring {module_name} is loaded")
        try:
            importlib.import_module(module_name, "worlds")
            # todo: We don't currently have a good way to pair up games with modules that do not provide a meta file
            #  indicating what game they provide. It would be good to be able to check that all loaded world modules
            #  load a world that supports a different game. It should be possible to determine the package of a
            #  registered world class in most cases, which could then be linked up with a world in
            #  `gameless_world_sources`.
            if world_source.game is not None and world_source.game not in AutoWorldRegister.world_types:
                warnings.warn(f"World {world_source.module_name} claims to contain the game {world_source.game}, but no"
                              f" world for this game was found after loading.")
                assert world_source.game in AutoWorldRegister.world_types
        except Exception:
            # A single world failing can still mean enough is working for the user, log and carry on
            import traceback
            import io
            file_like = io.StringIO()
            print(f"Could not load world {world_source}:", file=file_like)
            traceback.print_exc(file=file_like)
            file_like.seek(0)
            logging.exception(file_like.read())
            failed_world_loads.append(os.path.basename(world_source.path).rsplit(".", 1)[0])
            failed_world_module_loads_set.add(module_name)
