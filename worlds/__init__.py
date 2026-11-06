import importlib
import importlib.abc
import importlib.machinery
import logging
import os
import sys
import zipimport
import time
import dataclasses
import json
from pathlib import Path
from types import ModuleType
from typing import Any, Sequence
from zipfile import ZipFile, BadZipFile

from Utils import local_path, user_path, Version, version_tuple, tuplize_version, messagebox
from .AutoWorld import AutoWorldRegister, network_data_package, test_worlds_filter
from .Files import APWorldContainer, InvalidDataError

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
    "add_apworld_spec",
    "load_world_sources",
]


failed_world_loads: dict[str, str] = {}

logger = logging.getLogger("Worlds")
logger.propagate = False
logger.setLevel(logging.INFO)

@dataclasses.dataclass(order=True)
class WorldSource:
    path: str  # typically relative path from this module
    is_zip: bool = False
    relative: bool = True  # relative to regular world import folder
    time_taken: float = -1.0
    manifest: dict[str, Any] = dataclasses.field(default_factory=dict)

    @property
    def game(self) -> str | None:
        return self.manifest.get("game")

    @property
    def version(self) -> Version:
        return tuplize_version(self.manifest.get("world_version", "0.0.0"))

    @property
    def min_ap_version(self) -> Version:
        return tuplize_version(self.manifest.get("minimum_ap_version", "0.0.0"))

    @property
    def max_ap_version(self) -> Version:
        max_version = self.manifest.get("maximum_ap_version")
        if max_version:
            return tuplize_version(max_version)
        return version_tuple

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
                    if sys.stdout:
                        e.add_note(f"Affected world source: {self.resolved_path}")
                        raise e
                    else:
                        err_message = f"{e}\nAffected world source: {self.resolved_path}"
                        messagebox("Couldn't load worlds", err_message, error=True)
                        sys.exit(1)
            except BadZipFile as e:
                err_message = (f"The world source {self.resolved_path} is not a valid zip. "
                               "It is likely either corrupted, or was packaged incorrectly.")

                if sys.stdout:
                    raise RuntimeError(err_message) from e
                else:
                    messagebox("Couldn't load worlds", err_message, error=True)
                    sys.exit(1)
            else:
                # re-read and add in manifest
                assert apworld.path
                with ZipFile(apworld.path, "r") as zf:
                    manifest = apworld.read_contents(zf)
                # version/compatible_version shouldn't be needed by world, makes it consistent with folder world
                manifest.pop("version", None)
                manifest.pop("compatible_version", None)
                self.manifest = manifest
        else:
            if not (
                os.path.isfile(os.path.join(self.resolved_path, "__init__.py"))
                or os.path.isfile(os.path.join(self.resolved_path, "__init__.pyc"))
            ):
                raise RuntimeError(f"Could not find __init__.py in {self.resolved_path}")

            for dirpath, _dirnames, filenames in os.walk(self.resolved_path):
                for file in filenames:
                    if file.endswith("archipelago.json"):
                        with open(os.path.join(dirpath, file), "r") as f:
                            self.manifest = json.load(f)
                        break
                if self.manifest:
                    break

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self.path}, is_zip={self.is_zip}, relative={self.relative}, "
                f"manifest={self.manifest})")

    @property
    def resolved_path(self) -> str:
        if self.relative:
            return os.path.join(local_folder, self.path)
        return self.path

    def load(self) -> tuple[bool, str]:
        try:
            start = time.perf_counter()

            if self.min_ap_version > version_tuple:
                raise ValueError(
                    f"Did not load {source.resolved_path} "
                    f"as its minimum core version {source.min_ap_version} "
                    f"is higher than current core version {version_tuple}."
                )
            elif self.max_ap_version < version_tuple:
                raise ValueError(
                    f"Did not load {source.resolved_path} "
                    f"as its maximum core version {source.max_ap_version} "
                    f"is lower than current core version {version_tuple}."
                )
            if self.is_zip:
                # May be redundant if added earlier during initial reading, but means standalone load calls will work,
                # and also fixes the source used if a previous one was invalid
                add_apworld_spec(self)
            importlib.import_module(f".{self.name}", "worlds")
            if self.game in AutoWorldRegister.world_types:
                AutoWorldRegister.world_types[self.game].world_version = self.version
                AutoWorldRegister.world_types[self.game].manifest = self.manifest

            self.time_taken = time.perf_counter() - start
            return True, ""

        except Exception as e:
            # A single world failing can still mean enough is working for the user, log and carry on
            import traceback
            import io
            file_like = io.StringIO()
            print(f"Could not load world {self}:", file=file_like)
            traceback.print_exc(file=file_like)
            file_like.seek(0)
            reason = file_like.read()
            logging.exception(reason)
            failed_world_loads[os.path.basename(self.path).rsplit(".", 1)[0]] = reason
            return False, str(e)

    @property
    def name(self) -> str:
        return Path(self.path).stem


apworld_module_specs = {}
class APWorldModuleFinder(importlib.abc.MetaPathFinder):
    def find_spec(
            self, fullname: str, _path: Sequence[str] | None, _target: ModuleType | None = None
    ) -> importlib.machinery.ModuleSpec | None:
        return apworld_module_specs.get(fullname)
sys.meta_path.insert(0, APWorldModuleFinder())


def add_apworld_spec(source: WorldSource):
    importer = zipimport.zipimporter(source.resolved_path)

    spec = importer.find_spec(f"worlds.{source.name}")
    apworld_module_specs[f"worlds.{source.name}"] = spec


# find potential world containers, currently folders and zip-importable .apworld's
logger.info("Indexing worlds")
world_sources: list[WorldSource] = []
for folder in (folder for folder in (user_folder, local_folder) if folder):
    relative = folder == local_folder
    for entry in os.scandir(folder):
        # prevent loading of __pycache__ and allow _* for non-world folders, disable files/folders starting with "."
        if not entry.name.startswith(("_", ".")):
            if test_worlds_filter is not None and Path(entry.name).stem not in test_worlds_filter:
                continue
            file_name = entry.name if relative else os.path.join(folder, entry.name)
            is_packaged = entry.is_file() and entry.name.endswith(".apworld")
            if entry.is_dir() or is_packaged:
                try:
                    source = WorldSource(file_name, is_zip=is_packaged, relative=relative)
                    world_sources.append(source)
                except Exception as e:
                    logging.warning(f"Not adding {entry.name} to world sources due to error creating it")
                    logging.warning(e)


# Try adding apworld specs so apworlds can be imported inside of other worlds.
# If there's a source that can't load, then this may point to it and differ from what would actually get loaded,
# so this means users may have to clean out invalid worlds if another imports them.
world_sources.sort(key=lambda source: source.version, reverse=True)
world_sources.sort(key=lambda source: source.is_zip)  # ensure folder worlds are loaded first
earlier_worlds = set()
for source in world_sources:
    if source.is_zip:
        add_apworld_spec(source)
    earlier_worlds.add(source.name)


run_main_load = False

def load_world_sources() -> None:
    global run_main_load
    if run_main_load:
        return
    run_main_load = True

    logger.info("Processing found worlds")
    world_sources.sort(key=lambda source: source.version, reverse=True)
    world_sources.sort(key=lambda source: source.is_zip)  # ensure folder worlds are loaded first

    for source in world_sources:
        if source.game and source.game in AutoWorldRegister.world_types:
            logging.warning(f"Did not load {source.resolved_path} as its game {source.game} is already loaded.")
        logger.info(source.name)
        source.load()
