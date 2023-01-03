import importlib
import os
import sys
import typing
import warnings
import zipimport

folder = os.path.dirname(__file__)

__all__ = {
    "lookup_any_item_id_to_name",
    "lookup_any_location_id_to_name",
    "network_data_package",
    "AutoWorldRegister",
    "world_sources",
    "folder",
}

if typing.TYPE_CHECKING:
    from .AutoWorld import World


class GamesPackage(typing.TypedDict):
    item_name_to_id: typing.Dict[str, int]
    location_name_to_id: typing.Dict[str, int]
    version: int


class DataPackage(typing.TypedDict):
    version: int
    games: typing.Dict[str, GamesPackage]


class WorldSource(typing.NamedTuple):
    path: str  # typically relative path from this module
    is_zip: bool = False


# find potential world containers, currently folders and zip-importable .apworld's
world_sources: typing.List[WorldSource] = []
file: os.DirEntry  # for me (Berserker) at least, PyCharm doesn't seem to infer the type correctly
for file in os.scandir(folder):
    # prevent loading of __pycache__ and allow _* for non-world folders, disable files/folders starting with "."
    if not file.name.startswith(("_", ".")):
        if file.is_dir():
            world_sources.append(WorldSource(file.name))
        elif file.is_file() and file.name.endswith(".apworld"):
            world_sources.append(WorldSource(file.name, is_zip=True))

# import all submodules to trigger AutoWorldRegister
world_sources.sort()
for world_source in world_sources:
    if world_source.is_zip:
        importer = zipimport.zipimporter(os.path.join(folder, world_source.path))
        if hasattr(importer, "find_spec"):  # new in Python 3.10
            spec = importer.find_spec(world_source.path.split(".", 1)[0])
            mod = importlib.util.module_from_spec(spec)
        else:  # TODO: remove with 3.8 support
            mod = importer.load_module(world_source.path.split(".", 1)[0])

        mod.__package__ = f"worlds.{mod.__package__}"
        mod.__name__ = f"worlds.{mod.__name__}"
        sys.modules[mod.__name__] = mod
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="__package__ != __spec__.parent")
            # Found no equivalent for < 3.10
            if hasattr(importer, "exec_module"):
                importer.exec_module(mod)
    else:
        importlib.import_module(f".{world_source.path}", "worlds")

lookup_any_item_id_to_name = {}
lookup_any_location_id_to_name = {}
games: typing.Dict[str, GamesPackage] = {}

from .AutoWorld import AutoWorldRegister

for world_name, world in AutoWorldRegister.world_types.items():
    games[world_name] = {
        "item_name_to_id": world.item_name_to_id,
        "location_name_to_id": world.location_name_to_id,
        "version": world.data_version,
        # seems clients don't actually want this. Keeping it here in case someone changes their mind.
        # "item_name_groups": {name: tuple(items) for name, items in world.item_name_groups.items()}
    }
    lookup_any_item_id_to_name.update(world.item_id_to_name)
    lookup_any_location_id_to_name.update(world.location_id_to_name)

network_data_package: DataPackage = {
    "games": games,
}

# Set entire datapackage to version 0 if any of them are set to 0
if any(not world.data_version for world in AutoWorldRegister.world_types.values()):
    import logging

    logging.warning(f"Datapackage is in custom mode. Custom Worlds: "
                    f"{[world for world in AutoWorldRegister.world_types.values() if not world.data_version]}")
