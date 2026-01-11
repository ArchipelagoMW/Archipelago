import logging

from .BaseModpack import BaseModpack
from .ItemLocations import items_to_id, locations_to_id, item_groups, location_groups
from .PackLoader import modpacks


logger = logging.getLogger(f"APModpackManager - factorio with modpacks")



def get_items() -> dict[str, int]:
    if items_to_id:
        return items_to_id
    if not modpacks:
        raise Exception("No modpacks found, ensure modpacks exist and that packs are initialized before calling get_items()")
    for modpack in modpacks.values():
        modpack.init_items()
    return items_to_id

def get_item_groups() -> dict[str, set[str]]:
    if not items_to_id:
        get_items() # forces items to initialize if not already
    return item_groups

def get_locations() -> dict[str, int]:
    if locations_to_id:
        return locations_to_id
    if not modpacks:
        raise Exception("No modpacks found, ensure modpacks exist and that packs are initialized before calling get_locations()")
    for modpack in modpacks.values():
        modpack.init_locations()
    return locations_to_id

def get_location_groups() -> dict[str, set[str]]:
    if not items_to_id:
        get_locations() # forces locations to initialize if not already
    return location_groups
