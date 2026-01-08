"""
This module generates map markers for locations to appear in the CrossCode world map.
"""

import typing
import json

from .context import Context

class Marker(typing.TypedDict):
    type: str
    x: float
    y: float
    level: int
    map: str
    mwid: int
    settings: dict[str, typing.Any]

class MarkerGenerator:
    ctx: Context
    map_cache: dict[str, dict[str, typing.Any]]
    area_cache: dict[str, dict[str, typing.Any]]

    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx
        self.map_cache = {}
        self.area_cache = {}

    def __load_map(self, name: str) -> dict[str, typing.Any]:
        try:
            return self.map_cache[name]
        except KeyError:
            pass

        path = name.replace(".", "/")
        with open(f"worlds/crosscode/data/assets/data/maps/{path}.json") as f:
            self.map_cache[name] = json.load(f)

        return self.map_cache[name]

    def __load_area(self, name: str) -> dict[str, typing.Any]:
        try:
            return self.area_cache[name]
        except KeyError:
            pass

        with open(f"worlds/crosscode/data/assets/data/areas/{name}.json") as f:
            self.area_cache[name] = json.load(f)

        return self.area_cache[name]

    def generate_marker(self, raw_loc: dict[str, typing.Any], mwid: int) -> typing.Optional[Marker]:
        loc_data = raw_loc.get("location", None)
        if loc_data is None:
            return None

        map_name = loc_data.get("map", None)
        if map_name is None:
            return None
        map_id = loc_data.get("mapId", None)
        if map_id is None:
            return None

        map = self.__load_map(map_name)

        raw_entity = None
        for entity in map["entities"]:
            if entity["settings"].get("mapId", None) == map_id:
                raw_entity = entity
                break

        if raw_entity is None:
            return None

        # This code based on extractMarkers() from CCItemRandomizer by 2676mr

        map_width = map["mapWidth"]
        map_height = map["mapHeight"]

        x = raw_entity["x"]
        y = raw_entity["y"]

        level = raw_entity["level"]
        if isinstance(level, dict):
            level = level["level"]
        height = map["levels"][level]["height"]

        px = x / (map_width * 16)
        py = (y + height) / (map_height * 16)

        area_name = map["attributes"]["area"]
        area = self.__load_area(area_name)

        map_floor = None
        map_index = 0

        for floor in area["floors"]:
            for idx, map in enumerate(floor["maps"]):
                if map["path"] == map_name:
                    map_floor = floor
                    # add one because 0 indicates no map
                    map_index = idx + 1
                    break
            else:
                continue
            break

        if map_floor is None:
            return None

        startX = len(map_floor["tiles"][0])
        startY = len(map_floor["tiles"])
        endX = 0;
        endY = 0;

        for y, row in enumerate(map_floor["tiles"]):
            for x, col in enumerate(row):
                if col == map_index:
                    startY = min(y, startY)
                    startX = min(x, startX)
                    endY = max(y, endY)
                    endX = max(x, endX)

        tx = startX + (endX - startX) * px
        ty = startY + (endY - startY) * py

        mx = tx * 8
        my = ty * 8

        settings = {}

        if raw_entity["type"] == "Chest":
            settings["defaultClearance"] = raw_loc.get("clearance", "Default");

        return {
            "type": raw_entity["type"],
            "level": map_floor["level"],
            "x": mx,
            "y": my,
            "map": map_name,
            "mwid": mwid,
            "settings": settings,
        }
