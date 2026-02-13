import json
import logging
from io import TextIOWrapper
from pathlib import Path
from zipfile import Path as ZipPath, ZipFile

from .ItemLocations import add_item, add_location
from .PackLoader import init_modpacks

INTERNAL_PATH = Path(__file__).parent.parent / "InternalPacks"


class BaseModpack:
    modpack_directories: list[tuple[Path, list]] = []
    """
    all paths that should be checked for modpacks should be in modpack_directories
    relative paths should be relative to ap root but should not be within an ap world
    """

    if INTERNAL_PATH.exists():
        modpack_directories.append((INTERNAL_PATH, []))
    else:
        world_root = Path(__file__).parent
        while not world_root.exists():
            world_root = world_root.parent
        filesystem = ZipFile(world_root)
        path = next(ZipPath(filesystem).glob("*"))
        modpack_directories.append((path / "InternalPacks", [filesystem]))

    def __init__(self, packPath: Path | ZipPath, filesystem: list[ZipFile]=None):
        self.__packPath = packPath
        self.__filesystem: list[ZipFile] | None = filesystem

        try:
            with self.open_file("header.json") as header:
                raw_header = json.load(header)
                self.packName: str = raw_header["packName"].lower()
                self.version: str = raw_header["version"]
                self.formatVersion: str = raw_header["formatVersion"]
                self.downloadLocation: str = raw_header["downloadLocation"]
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Pack doesn't have header: {self.__packPath}", e)
        except Exception as e:
            raise Exception(f"Occurred loading pack in: {self.__packPath}") from e
        self.logger = logging.getLogger(f"Factorio with modpacks: {self.packName}")

        self.__has_fully_initialized = False

        self.items_to_id: dict[str, int] = {}
        self.locations_to_id: dict[str, int] = {}

        self.logger.info(f"Initialised pack: {self.packName}")

    def __init_subclass__(cls, **kwargs):
        if cls.__name__ == 'BaseModpack':
            return
        logger = logging.getLogger(f"APModpackManager - factorio with modpacks")
        logger.debug(f'PackWorld subclass: {cls.__name__}, starting import of packs')
        init_modpacks(cls)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.packName}>"

    def __del__(self):
        if self.__filesystem:
            for f in reversed(self.__filesystem):
                f.close()

    def _add_item(self, name: str, item_id: int | None = None, groups: set[str] | None = None) -> None:
        item_id = add_item(name, item_id=item_id, groups=groups)
        self.items_to_id[name] = item_id

    def _add_location(self, name: str, location_id: int | None = None, groups: set[str] | None = None) -> None:
        location_id = add_location(name, location_id=location_id, groups=groups)
        self.locations_to_id[name] = location_id

    def open_file(self, relative_path: str) -> TextIOWrapper:
        """
        Use to access files in the pack

        It is suggested to use this with context manager e.g.
        ```
        with self.open_file("file_name") as file:
            #do file stuff
            pass
        ```
        """
        path = self.__packPath / relative_path

        return path.open("r")

    def init_items(self):
        """
        Use to register all the items the pack uses
        Use self._add_item to add the items to the pack

        This might be ran every time ap is loaded (no matter the context) so keep code fast and minimal
        This is also the last time a pack can add items
        """
        raise NotImplementedError("init_items must be implemented by subclass")

    def init_locations(self):
        """
        Use to register all the locations the pack uses
        Use self._add_locations to add the items to the pack

        This might be ran every time ap is loaded (no matter the context) so keep code fast and minimal
        This is also the last time a pack can add locations
        """
        raise NotImplementedError("init_locations must be implemented by subclass")

    def _init_pack(self) -> None:
        """
        Ran once the first time the pack is loaded

        Can be overridden by subclass
        """
        pass

    def init_pack_check(self) -> None:
        """
        Runs _init_pack only once

        Can be overridden by subclass if you want something to happen every time the pack is used
        Do ensure to run `super()` though
        """
        if self.__has_fully_initialized:
            return
        self._init_pack()
        self.__has_fully_initialized = True