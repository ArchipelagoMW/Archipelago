"""
This module provides the Context class for code generation, which provides access to large amounts of game data.
"""

from dataclasses import dataclass, field
import typing

from .util import get_json_object, load_json_with_includes


@dataclass
class Context:
    """
    A class providing access to game data relevant to randomization.
    """

    rando_data: dict[str, typing.Any]
    """
    Stores data about what locations, items, regions, etc exist in the world. Typically loaded from `data/in`.
    """
    item_data: list[typing.Dict[str, typing.Any]]
    """
    Stores CrossCode's `item_database.json`, containing details about all of its items.
    """
    database: dict[str, typing.Any]
    """
    Stores CrossCode's `database.json`, containing details about areas and quests.
    """
    cached_location_ids: dict[str, int]
    """
    A list of cached location ids to respect when creating location objects.
    """
    cached_item_ids: dict[str, int]
    """
    A list of cached item ids for the dynamically allocated item area.
    """
    num_items: int = field(init=False)
    """
    The number of items in the item database.
    """
    area_names: dict[str, str]
    """
    Dict associating internal area names with their English fancy names.
    """

    def __post_init__(self):
        self.num_items = len(self.item_data)


def make_context_from_package(package: str) -> Context:
    """
    Create a context class from JSON data within a python package.

    This requires all the data described in the entry point for this codegen module.
    """
    master = load_json_with_includes(package, "data/in/master.json")

    cached_location_ids: dict[str, int] = {}
    try:
        cached_location_ids = get_json_object(package, "data/out/locations.json")
    except FileNotFoundError:
        pass

    cached_item_ids: dict[str, int] = {}
    try:
        cached_item_ids = get_json_object(package, "data/out/items.json")
    except FileNotFoundError:
        pass

    database = get_json_object(package, "data/assets/data/database.json")

    area_names = {
        name: data["name"]["en_US"] for name, data in database["areas"].items()
    }

    return Context(
        master,
        get_json_object(package, "data/assets/data/item-database.json")["items"],
        database,
        cached_location_ids,
        cached_item_ids,
        area_names
    )
