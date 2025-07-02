from typing import Dict

from BaseClasses import Location
from worlds.clair_obscur.Const import BASE_OFFSET, LOCATION_OFFSET
from worlds.clair_obscur.Data import data


class ClairObscurLocation(Location):
    game: str = "Clair Obscur Expedition 33"

def offset_item_value(item_id: int) -> int:
    """
    Returns the AP item id for a given item value
    """
    return BASE_OFFSET + LOCATION_OFFSET + item_id

def reverse_offset_item_value(item_id: int) -> int:
    """
    Returns the item value for a given AP item id
    """
    return BASE_OFFSET - LOCATION_OFFSET - item_id


def create_location_name_to_ap_id() -> Dict[str, int]:
    """
    Creates a map from item name to their AP item id
    """
    name_to_ap_id = {}
    index = 1
    for location in data.locations:
        name_to_ap_id[location.name] = offset_item_value(index)
        index += 1

    return name_to_ap_id