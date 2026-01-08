from typing import Dict
from .data import LOCATIONS_DATA, ITEMS_DATA, DYNAMIC_FLAGS
from .data.Hints import HINT_DATA
from .data.Entrances import ENTRANCES

def build_entrance_id_to_data():
    entrances = {}
    for i in ENTRANCES.values():
        entrances[i.id] = i
    return entrances

def build_hint_scene_to_watches() -> dict[int, list[str]]:
    hint_room_to_watches: dict[int, list[str]] = {}
    for name, data in HINT_DATA.items():
        for scene in data["scenes"]:
            hint_room_to_watches.setdefault(scene, [])
            hint_room_to_watches[scene].append(name)
    return hint_room_to_watches


def build_location_room_to_watches() -> Dict[int, dict[str, dict]]:
    location_room_to_watches: Dict[int, dict[str, dict]] = {}
    for loc_name, location in LOCATIONS_DATA.items():
        room_id = location["stage_id"] * 0x100 + location["floor_id"]
        location_room_to_watches.setdefault(room_id, {})
        location_room_to_watches[room_id][loc_name] = location

        # Add location to multiple rooms
        if "additional_rooms" in location:
            for room in location["additional_rooms"]:
                location_room_to_watches.setdefault(room, {})
                location_room_to_watches[room][loc_name] = location
    return location_room_to_watches


def build_scene_to_dynamic_flag() -> Dict[int, list[dict]]:
    scene_to_dynamic_flag: Dict[int, list[dict]] = {}
    for flag_name, data in DYNAMIC_FLAGS.items():
        data["name"] = flag_name
        for scene in data.get("on_scenes", []):
            scene_to_dynamic_flag.setdefault(scene, [])
            scene_to_dynamic_flag[scene].append(data)
    return scene_to_dynamic_flag


def build_location_name_to_id_dict() -> Dict[str, int]:
    location_name_to_id: Dict[str, int] = {}
    for loc_name, location in LOCATIONS_DATA.items():
        # ids are for sending flags
        location_name_to_id[loc_name] = location["id"]
    return location_name_to_id


def build_item_name_to_id_dict() -> Dict[str, int]:
    item_name_to_id: Dict[str, int] = {}
    for item_name, item in ITEMS_DATA.items():
        item_name_to_id[item_name] = item["id"]
    return item_name_to_id


def build_item_id_to_name_dict() -> Dict[int, str]:
    item_id_to_name: Dict[int, str] = {}
    for item_name, item in ITEMS_DATA.items():
        index = item["id"]
        item_id_to_name[index] = item_name
    return item_id_to_name

