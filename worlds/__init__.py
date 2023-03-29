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


class GamesData(typing.TypedDict):
    item_name_groups: typing.Dict[str, typing.List[str]]
    item_name_to_id: typing.Dict[str, int]
    location_name_groups: typing.Dict[str, typing.List[str]]
    location_name_to_id: typing.Dict[str, int]
    version: int


class GamesPackage(GamesData, total=False):
    checksum: str


class DataPackage(typing.TypedDict):
    games: typing.Dict[str, GamesPackage]


class WorldSource(typing.NamedTuple):
    path: str  # typically relative path from this module
    is_zip: bool = False

    def __repr__(self):
        return f"{self.__class__.__name__}({self.path}, is_zip={self.is_zip})"


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
    try:
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
    except Exception as e:
        # A single world failing can still mean enough is working for the user, log and carry on
        import traceback
        import io
        file_like = io.StringIO()
        print(f"Could not load world {world_source}:", file=file_like)
        traceback.print_exc(file=file_like)
        file_like.seek(0)
        import logging
        logging.exception(file_like.read())

lookup_any_item_id_to_name = {}
lookup_any_location_id_to_name = {}
games: typing.Dict[str, GamesPackage] = {}

from .AutoWorld import AutoWorldRegister

# Build the data package for each game.
for world_name, world in AutoWorldRegister.world_types.items():
    games[world_name] = world.get_data_package_data()
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
