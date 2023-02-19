from enum import Enum
import json
import os
from typing import List, Optional, Dict, MutableSet


class LocationData:
    name: str
    map_name: str
    default_item: int
    ram_address: Optional[int]
    rom_address: Optional[int]
    flag: int
    tags: MutableSet[str]

    def __init__(self, name: str, map_name: str, default_item: int, ram_address: Optional[int], rom_address: Optional[int], flag: int):
        self.name = name
        self.map_name = map_name
        self.default_item = default_item
        self.ram_address = ram_address
        self.rom_address = rom_address
        self.flag = flag
        self.tags = set()


class EncounterType(Enum):
    LAND = 1
    WATER = 2
    FISHING = 3
    # STATIC = 4


class EncounterTableData:
    encounter_type: EncounterType
    map_name: str
    encounter_slots: List[int]
    ram_address: int
    rom_address: int

    def __init__(self, encounter_type: EncounterType, map_name: str, encounter_slots: List[int], ram_address: int, rom_address: int):
        self.encounter_type = encounter_type
        self.map_name = map_name
        self.encounter_slots = encounter_slots
        self.ram_address = ram_address
        self.rom_address = rom_address


class MapData:
    name: str
    connections: List[str]
    warps: List[str]
    locations: List[LocationData]
    land_encounters: Optional[EncounterTableData]
    water_encounters: Optional[EncounterTableData]
    fishing_encounters: Optional[EncounterTableData]

    def __init__(self, name: str):
        self.name = name
        self.connections = []
        self.warps = []
        self.locations = []


data_json = None
def get_data_json():
    global data_json
    if (data_json == None):
        json_string = ""
        with open(os.path.join(os.path.dirname(__file__), f"data/data.json"), "r") as infile:
            for line in infile.readlines():
                json_string += line
        data_json = json.loads(json_string)
    
    return data_json


data = None
def get_data():
    global data
    if (data == None):
        data = create_maps_from_json()
    return data


remapped_locations = {
    "RECEIVED_HM01": "MAP_RUSTBORO_CITY_CUTTERS_HOUSE",
    "RECEIVED_WAILMER_PAIL": "MAP_ROUTE104_PRETTY_PETAL_FLOWER_SHOP",
    "ITEM_BADGE_1": "MAP_RUSTBORO_CITY_GYM",
    "ITEM_BADGE_2": "MAP_DEWFORD_TOWN_GYM",
    "ITEM_BADGE_3": "MAP_MAUVILLE_CITY_GYM",
    "ITEM_BADGE_4": "MAP_LAVARIDGE_TOWN_GYM_1F",
    "ITEM_BADGE_5": "MAP_PETALBURG_CITY_GYM",
    "ITEM_BADGE_6": "MAP_FORTREE_CITY_GYM",
    "ITEM_BADGE_7": "MAP_MOSSDEEP_CITY_GYM",
    "ITEM_BADGE_8": "MAP_SOOTOPOLIS_CITY_GYM_1F",
}
def get_region_name_for(location_name: str, default_value: str):
    global remapped_locations
    if (location_name in remapped_locations):
        return remapped_locations[location_name]
    
    return default_value


def create_maps_from_json() -> Dict[str, MapData]:
    data_json = get_data_json()

    maps = {}
    # TODO: Map connections/warps currently only have info for their destination.
    # Some maps (especially caves) have two warps leading to the same destination map.
    # The source code specifies a destination ID to distinguish these warps.
    for map_json in data_json["maps"]:
        new_map = MapData(map_json["name"])
        new_map.connections = [connection for connection in map_json["connections"]]
        # MAP_DYNAMIC is mostly used for secret bases and online rooms
        # With the exceptions of Terra Cave, Marine Cave, and the Dept. Store elevator
        # These shouldn't affect logic for now
        # TODO: Handle MAP_DYNAMIC edge cases
        new_map.warps = [warp for warp in map_json["warps"] if (not warp == "MAP_DYNAMIC")]
        maps[map_json["name"]] = new_map
    
    # -------------------------------------------------------------------------
    # Ground/Hidden Item Locations
    # -------------------------------------------------------------------------
    # Ground Items
    for item_json in data_json["ball_items"]:
        new_location = LocationData(
            item_json["name"],
            item_json["map_name"],
            item_json["default_item"],
            None,
            item_json["rom_address"],
            item_json["flag"]
        )
        new_location.tags.add("GroundItem")
        maps[new_location.map_name].locations.append(new_location)

    # Hidden Items
    for item_json in data_json["hidden_items"]:
        new_location = LocationData(
            item_json["name"],
            item_json["map_name"],
            item_json["default_item"],
            None,
            item_json["rom_address"],
            item_json["flag"]
        )
        new_location.tags.add("HiddenItem")
        maps[new_location.map_name].locations.append(new_location)

    # NPC Gifts
    for item_json in data_json["npc_gifts"]:
        map_name = get_region_name_for(item_json["name"], None)
        new_location = LocationData(
            item_json["name"],
            map_name,
            item_json["default_item"],
            None,
            item_json["rom_address"],
            item_json["flag"]
        )
        new_location.tags.add("NpcGift")
        maps[new_location.map_name].locations.append(new_location)

    # Badges
    for i in range(0, 8):
        item_name = f"ITEM_BADGE_{i + 1}"
        item_code = data_json["constants"]["items"][item_name]
        map_name = get_region_name_for(item_name, None)
        new_location = LocationData(
            item_name,
            map_name,
            item_code,
            None,
            data_json["misc_rom_addresses"]["gGymBadgeItems"] + (i * 2),
            data_json["constants"]["flags"][f"FLAG_BADGE0{i + 1}_GET"]
        )
        new_location.tags.add("Badge")
        maps[new_location.map_name].locations.append(new_location)

    # -------------------------------------------------------------------------
    # Encounter Tables
    # -------------------------------------------------------------------------
    for map_name, encounter_table in data_json["encounter_tables"].items():
        if ("land_encounters" in encounter_table):
            land_encounters_json = encounter_table["land_encounters"]
            encounter_slots = [slot for slot in land_encounters_json["encounter_slots"]]
            land_encounters = EncounterTableData(
                EncounterType.LAND,
                map_name,
                encounter_slots,
                land_encounters_json["ram_address"],
                land_encounters_json["rom_address"]
            )
            maps[map_name].land_encounters = land_encounters

        if ("water_encounters" in encounter_table):
            water_encounters_json = encounter_table["water_encounters"]
            encounter_slots = [slot for slot in water_encounters_json["encounter_slots"]]
            water_encounters = EncounterTableData(
                EncounterType.WATER,
                map_name,
                encounter_slots,
                water_encounters_json["ram_address"],
                water_encounters_json["rom_address"]
            )
            maps[map_name].water_encounters = water_encounters

        if ("fishing_encounters" in encounter_table):
            fishing_encounters_json = encounter_table["fishing_encounters"]
            encounter_slots = [slot for slot in fishing_encounters_json["encounter_slots"]]
            fishing_encounters = EncounterTableData(
                EncounterType.FISHING,
                map_name,
                encounter_slots,
                fishing_encounters_json["ram_address"],
                fishing_encounters_json["rom_address"]
            )
            maps[map_name].fishing_encounters = fishing_encounters
    
    return maps
