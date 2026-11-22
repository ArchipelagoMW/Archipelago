"""Ids of every location and item, frozen in data/ids.json so that game updates don't move them.

A name keeps its id forever, even once the game drops it; new names go at the end
(python -m worlds.dota_2.tools.update_ids).
"""
import json
from importlib import resources

with resources.files(__package__).joinpath("data/ids.json").open("r", encoding="utf-8") as _f:
    _IDS = json.load(_f)
LOCATION_IDS: dict[str, int] = _IDS["locations"]
ITEM_IDS: dict[str, int] = _IDS["items"]


def id_of(ids: dict[str, int], name: str) -> int:
    if name not in ids:
        raise KeyError(f"{name!r} has no id in data/ids.json: run python -m worlds.dota_2.tools.update_ids")
    return ids[name]
