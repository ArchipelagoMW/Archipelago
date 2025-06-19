from typing import Dict
from .data import LOCATIONS_DATA, ITEMS_DATA, DYNAMIC_FLAGS
from .data.Constants import SHOPS


def build_location_room_to_watches() -> Dict[int, dict[str, dict]]:
    location_room_to_watches: Dict[int, dict[str, dict]] = {}
    for loc_name, location in LOCATIONS_DATA.items():
        room_id = location["stage_id"] * 0x100 + location["floor_id"]
        if room_id not in location_room_to_watches:
            location_room_to_watches[room_id] = {}
        location_room_to_watches[room_id][loc_name] = location

        # Build Island shops
        if "island_shop" in location:
            for shop_id, shop in SHOPS.items():
                if shop_id not in location_room_to_watches:
                    location_room_to_watches[shop_id] = {}
                if "island_shop" in shop:
                    location_room_to_watches[shop_id][loc_name] = location
    return location_room_to_watches


def build_scene_to_dynamic_flag() -> Dict[int, list[dict]]:
    scene_to_dynamic_flag: Dict[int, list[dict]] = {}
    for flag_name, data in DYNAMIC_FLAGS.items():
        for scene in data["on_scenes"]:
            data["name"] = flag_name
            if scene not in scene_to_dynamic_flag:
                scene_to_dynamic_flag[scene] = []
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
