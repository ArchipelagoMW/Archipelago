from typing import Dict
from .data import LOCATIONS_DATA, ITEMS_DATA


def build_location_room_to_watches() -> Dict[int, dict[str, dict]]:
    location_room_to_watches: Dict[int, dict[str, dict]] = {}
    for loc_name, location in LOCATIONS_DATA.items():
        room_id = location["stage_id"] * 0x100 + location["floor_id"]
        if room_id not in location_room_to_watches:
            location_room_to_watches[room_id] = {}
        location_room_to_watches[room_id][loc_name] = location
    return location_room_to_watches


def build_location_name_to_id_dict() -> Dict[str, int]:
    location_name_to_id: Dict[str, int] = {}
    for loc_name, location in LOCATIONS_DATA.items():
        # ids do nothing, but I think AP wants unique ids?
        location_name_to_id[loc_name] = (len(location_name_to_id) + 1)
    return location_name_to_id


def build_item_name_to_id_dict() -> Dict[str, int]:
    item_name_to_id: Dict[str, int] = {}
    for item_name, item in ITEMS_DATA.items():
        index = item["id"]
        item_name_to_id[item_name] = index
    return item_name_to_id


def build_item_id_to_name_dict() -> Dict[int, str]:
    item_id_to_name: Dict[int, str] = {}
    for item_name, item in ITEMS_DATA.items():
        index = item["id"]
        item_id_to_name[index] = item_name
    return item_id_to_name
