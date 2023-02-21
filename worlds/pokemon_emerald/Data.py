from enum import Enum
import json
import os
from typing import List, Optional, Dict, MutableSet, NamedTuple
from BaseClasses import ItemClassification
    

def load_json(filename):
    json_string = ""
    with open(os.path.join(os.path.dirname(__file__), f"data/{filename}"), "r") as infile:
        for line in infile.readlines():
            json_string += line
    return json.loads(json_string)


data_json = None
def get_data_json():
    global data_json
    if (data_json == None):
        data_json = load_json("data.json")
    
    return data_json


class ItemData(NamedTuple):
    label: str
    classification: ItemClassification
    tags: MutableSet[str]


item_attributes = None
def get_item_attributes() -> Dict[str, ItemData]:
    global item_attributes
    data_json = get_data_json()
    if (item_attributes == None):
        item_attributes = {}
        items_json = load_json("items.json")

        for item_constant_name, attributes in items_json.items():
            item_id = data_json["constants"][item_constant_name]
            item_attributes[item_id] = ItemData(
                attributes["label"],
                str_to_item_classification(attributes["classification"]),
                set(attributes["tags"])
            )

    return item_attributes


def str_to_item_classification(string):
    if (string == "PROGRESSION"):
        return ItemClassification.progression
    if (string == "USEFUL"):
        return ItemClassification.useful
    elif (string == "FILLER"):
        return ItemClassification.filler
    elif (string == "TRAP"):
        return ItemClassification.trap


class LocationData:
    name: str
    region_name: str
    default_item: int
    ram_address: Optional[int]
    rom_address: Optional[int]
    flag: int
    tags: MutableSet[str]

    def __init__(self, name: str, region_name: str, default_item: int, ram_address: Optional[int], rom_address: Optional[int], flag: int):
        self.name = name
        self.region_name = region_name
        self.default_item = default_item
        self.ram_address = ram_address
        self.rom_address = rom_address
        self.flag = flag
        self.tags = set()


class WarpData:
    region_name: str
    encoded_string: str

    def __init__(self, encoded_string: str, region_name: str):
        self.encoded_string = encoded_string
        self.region_name = region_name


class RegionData:
    name: str
    exits: List[str]
    warps: List[WarpData]
    locations: List[LocationData]

    def __init__(self, name: str):
        self.name = name
        self.exits = []
        self.warps = []
        self.locations = []


regions_data = None
def get_regions_data():
    global regions_data
    if (regions_data == None):
        regions_data = create_regions_from_json()

    return regions_data


def create_regions_from_json() -> Dict[str, RegionData]:
    data_json = get_data_json()

    location_to_region_map = {}

    battle_frontier_json = load_json("regions/battle_frontier.json")
    city_regions_json = load_json("regions/cities.json")
    dungeon_regions_json = load_json("regions/dungeons.json")
    route_regions_json = load_json("regions/routes.json")

    regions_json = {}
    for region_name, region_json in battle_frontier_json.items():
        regions_json[region_name] = region_json
    for region_name, region_json in city_regions_json.items():
        regions_json[region_name] = region_json
    for region_name, region_json in dungeon_regions_json.items():
        regions_json[region_name] = region_json
    for region_name, region_json in route_regions_json.items():
        regions_json[region_name] = region_json
    
    regions = {}
    for region_name, region_json in regions_json.items():
        new_region = RegionData(region_name)
        for location_name in region_json["locations"]:
            location_to_region_map[location_name] = region_name
        for exit in region_json["exits"]:
            new_region.exits.append(exit)
        for encoded_warp in region_json["warps"]:
            new_region.warps.append(WarpData(encoded_warp, region_name))

        regions[region_name] = new_region

    # Ground Items
    for item_json in data_json["ball_items"]:
        new_location = LocationData(
            item_json["name"],
            location_to_region_map[item_json["name"]],
            item_json["default_item"],
            None,
            item_json["rom_address"],
            item_json["flag"]
        )
        new_location.tags.add("GroundItem")
        regions[new_location.region_name].locations.append(new_location)

    # Hidden Items
    for item_json in data_json["hidden_items"]:
        new_location = LocationData(
            item_json["name"],
            location_to_region_map[item_json["name"]],
            item_json["default_item"],
            None,
            item_json["rom_address"],
            item_json["flag"]
        )
        new_location.tags.add("HiddenItem")
        regions[new_location.region_name].locations.append(new_location)

    # NPC Gifts
    for item_json in data_json["npc_gifts"]:
        new_location = LocationData(
            item_json["name"],
            location_to_region_map[item_json["name"]],
            item_json["default_item"],
            None,
            item_json["rom_address"],
            item_json["flag"]
        )
        new_location.tags.add("NpcGift")
        regions[new_location.region_name].locations.append(new_location)

    # Badges
    for i in range(0, 8):
        item_name = f"ITEM_BADGE_{i + 1}"
        item_code = data_json["constants"][item_name]
        new_location = LocationData(
            item_name,
            location_to_region_map[item_json["name"]],
            item_code,
            None,
            data_json["misc_rom_addresses"]["gGymBadgeItems"] + (i * 2),
            data_json["constants"][f"FLAG_BADGE0{i + 1}_GET"]
        )
        new_location.tags.add("Badge")
        regions[new_location.region_name].locations.append(new_location)
    
    return regions


def get_warp_destination_region_name(warp: WarpData):
    regions_data = get_regions_data()
    
    source, dest = warp.encoded_string.split("/")
    dest_map_name, dest_id = dest.split(':')

    for region in regions_data.values():
        for region_warp in region.warps:
            region_warp_source, region_warp_dest = region_warp.encoded_string.split("/")
            region_warp_source_map_name, region_warp_source_id_string = region_warp_source.split(':')
            source_ids = region_warp_source_id_string.split(",")

            if (
                dest_map_name == region_warp_source_map_name and
                dest_id in source_ids
            ):
                return region_warp.region_name

    return None


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


class EncounterData:
    land_encounters: Optional[EncounterTableData]
    water_encounters: Optional[EncounterTableData]
    fishing_encounters: Optional[EncounterTableData]


def create_encounters_from_json():
    encounters = {}
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
            encounters[map_name].land_encounters = land_encounters

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
            encounters[map_name].water_encounters = water_encounters

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
            encounters[map_name].fishing_encounters = fishing_encounters
