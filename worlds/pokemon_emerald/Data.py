from enum import Enum
import json
import os
from typing import List, Optional, Dict, MutableSet, NamedTuple
from BaseClasses import ItemClassification


class ItemData(NamedTuple):
    label: str
    classification: ItemClassification
    tags: MutableSet[str]


class LocationData:
    name: str
    region_name: str
    default_item: int
    rom_address: Optional[int]
    flag: int
    tags: MutableSet[str]

    def __init__(self, name: str, region_name: str, default_item: int, rom_address: Optional[int], flag: int):
        self.name = name
        self.region_name = region_name
        self.default_item = default_item
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
    warps: List[str]
    locations: List[LocationData]

    def __init__(self, name: str):
        self.name = name
        self.exits = []
        self.warps = []
        self.locations = []
    

def load_json(filepath):
    json_string = ""
    with open(filepath, "r") as infile:
        for line in infile.readlines():
            json_string += line
    return json.loads(json_string)


extracted_data = None
def get_extracted_data() -> Dict[str, any]:
    global extracted_data
    if (extracted_data == None):
        extracted_data = load_json(os.path.join(os.path.dirname(__file__), "data/extracted_data.json"))
    
    return extracted_data


item_attributes = None
def get_item_attributes() -> Dict[str, ItemData]:
    global item_attributes
    extracted_data = get_extracted_data()
    if (item_attributes == None):
        item_attributes = {}
        items_json = load_json(os.path.join(os.path.dirname(__file__), "data/items.json"))

        for item_constant_name, attributes in items_json.items():
            item_id = extracted_data["constants"][item_constant_name]
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


# TODO: Could generalize this with regex
# Or this function is maybe superfluous
def str_to_tag(string):
    if (string == "HIDDEN_ITEM"):
        return "HiddenItem"
    if (string == "GROUND_ITEM"):
        return "GroundItem"
    elif (string == "NPC_GIFT"):
        return "NpcGift"


def load_region_jsons() -> List[Dict[str, any]]:
    regions_dir = os.path.join(os.path.dirname(__file__), "data/regions")

    region_jsons = []

    for file in os.listdir(regions_dir):
        if os.path.isfile(os.path.join(regions_dir, file)):
            region_jsons.append(load_json(os.path.join(regions_dir, file)))
    
    return region_jsons


def merge_region_jsons(region_jsons: List[Dict[str, any]]) -> Dict[str, any]:
    merged_regions = {}

    for region_subset in region_jsons:
        for region_name, region_data in region_subset.items():
            if (region_name in merged_regions):
                raise AssertionError("Region [{region_name}] was defined multiple times")
            merged_regions[region_name] = region_data
    
    return merged_regions


location_to_region_map = None
def get_location_to_region_map() -> Dict[str, str]:
    if (location_to_region_map == None):
        raise AssertionError("Cannot get_location_to_region_map before region data has been loaded")
    return location_to_region_map


warp_to_region_map = None
def get_warp_to_region_map() -> Dict[str, str]:
    if (warp_to_region_map == None):
        raise AssertionError("Cannot get_warp_to_region_map before region data has been loaded")
    return warp_to_region_map


def create_region_data() -> Dict[str, RegionData]:
    global location_to_region_map
    global warp_to_region_map
    location_to_region_map = {}
    warp_to_region_map = {}

    extracted_data = get_extracted_data()
    region_jsons = load_region_jsons()
    regions_json = merge_region_jsons(region_jsons)


    # RegionDatas
    regions = {}
    for region_name, region_json in regions_json.items():
        new_region = RegionData(region_name)
        for location_name in region_json["locations"]:
            if (location_name in location_to_region_map):
                raise AssertionError(f"Location [{location_name}] was claimed by multiple regions")
            location_to_region_map[location_name] = region_name

        for exit in region_json["exits"]:
            new_region.exits.append(exit)
        for encoded_warp in region_json["warps"]:
            if (encoded_warp in location_to_region_map):
                raise AssertionError(f"Warp [{encoded_warp}] was claimed by multiple regions")
            warp_to_region_map[encoded_warp] = region_name
            new_region.warps.append(encoded_warp)

        regions[region_name] = new_region

    # LocationDatas
    for location_name, location_json in extracted_data["locations"].items():
        new_location = LocationData(
            location_name,
            location_to_region_map[location_name],
            location_json["default_item"],
            location_json["rom_address"],
            location_json["flag"]
        )
        new_location.tags.add(str_to_tag(location_json["type"]))
        regions[new_location.region_name].locations.append(new_location)

    # Badges aren't extracted locations, so enumerate them explicitly
    for i in range(0, 8):
        location_name = f"BADGE_{i + 1}"
        item_code = extracted_data["constants"][f"ITEM_{location_name}"]
        new_location = LocationData(
            location_name,
            location_to_region_map[location_name],
            item_code,
            extracted_data["misc_rom_addresses"]["gGymBadgeItems"] + (i * 2),
            extracted_data["constants"][f"FLAG_BADGE0{i + 1}_GET"]
        )
        new_location.tags.add("Badge")
        regions[new_location.region_name].locations.append(new_location)
    
    return regions


region_data = None
def get_region_data():
    global region_data
    if (region_data == None):
        region_data = create_region_data()

    return region_data


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


# TODO: Fix and call
def create_encounters_from_json():
    extracted_data = get_extracted_data()
    encounters = {}
    for map_name, encounter_table in extracted_data["encounter_tables"].items():
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
