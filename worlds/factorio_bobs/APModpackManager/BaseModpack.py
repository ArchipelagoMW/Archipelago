import json
import logging
from io import TextIOWrapper
from pathlib import Path

from .ItemLocations import add_item, add_location


class BaseModpack:
    def __init__(self, packPath: Path):
        self.__packPath = packPath
        self.__is_zip = False
        try:
            with open(self.__packPath/"header.json") as header:
                self.packName = json.load(header)["packName"]
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Pack doesn't have header: {self.__packPath}", e)
        except Exception as e:
            raise Exception(f"Occurred loading pack in: {self.__packPath}") from e
        self.logger = logging.getLogger(f"APModpackManager - factorio with modpacks: {self.packName}")

        self.items_to_id: dict[str, int] | None = None
        self.locations_to_id: dict[str, int] | None = None

        self.logger.info(f"Initialised pack: {self.packName}")

    def _add_item(self, name: str, item_id: int | None = None) -> None:
        item_id = add_item(name, item_id)
        self.items_to_id[name] = item_id

    def _add_location(self, name: str, location_id: int | None = None) -> None:
        location_id = add_location(name, location_id)
        self.locations_to_id[name] = location_id

    def open_file(self, relative_path: str) -> TextIOWrapper:
        return open(self.__packPath/relative_path, "r")

    def init_items(self):
        raise NotImplementedError("init_items must be implemented by subclass")

    def init_locations(self):
        raise NotImplementedError("init_locations must be implemented by subclass")