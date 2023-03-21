from enum import Enum
import json
import os
from typing import Dict, List, MutableSet, NamedTuple, Optional
from BaseClasses import ItemClassification


extracted_data = None
region_data = None
item_attributes = None
location_attributes = None
warp_to_region_map = None
location_to_region_map = None
_config = None


class ItemData(NamedTuple):
    label: str
    classification: ItemClassification
    tags: MutableSet[str]


class LocationAttributes(NamedTuple):
    label: str
    tags: MutableSet[str]


class LocationData:
    name: str
    label: str
    region_name: str
    default_item: int
    rom_address: Optional[int]
    flag: int
    tags: MutableSet[str]

    def __init__(self, name: str, region_name: str, default_item: int, rom_address: Optional[int], flag: int):
        attributes = get_location_attributes()[name]
        self.name = name
        self.label = attributes.label
        self.region_name = region_name
        self.default_item = default_item
        self.rom_address = rom_address
        self.flag = flag
        self.tags = attributes.tags


class EventData:
    name: str
    region_name: str

    def __init__(self, name: str, region_name: str):
        self.name = name
        self.region_name = region_name


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
    events: List[EventData]

    def __init__(self, name: str):
        self.name = name
        self.exits = []
        self.warps = []
        self.locations = []
        self.events = []


# Not currently reading encounter data until output.
# But we will eventually need to in order to logically check
# that players can obtain a pokemon that can use required HMs
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


def load_json(filepath):
    json_string = ""
    with open(filepath, "r", encoding="utf-8") as infile:
        for line in infile.readlines():
            json_string += line
    return json.loads(json_string)


def get_config() -> Dict[str, any]:
    global _config
    if _config is None:
        _config = load_json(os.path.join(os.path.dirname(__file__), "data/config.json"))

    return _config


def get_extracted_data() -> Dict[str, any]:
    global extracted_data
    if extracted_data is None:
        extracted_data = load_json(os.path.join(os.path.dirname(__file__), "data/extracted_data.json"))
    
    return extracted_data


def get_region_data():
    global region_data
    if region_data is None:
        region_data = create_region_data()

    return region_data


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

        # Locations
        for location_name in region_json["locations"]:
            if location_name in location_to_region_map:
                raise AssertionError(f"Location [{location_name}] was claimed by multiple regions")
            location_to_region_map[location_name] = region_name

        # Events
        for event in region_json["events"]:
            new_region.events.append(EventData(event, region_name))

        # Exits
        for region_exit in region_json["exits"]:
            new_region.exits.append(region_exit)

        # Warps
        for encoded_warp in region_json["warps"]:
            if encoded_warp in location_to_region_map:
                raise AssertionError(f"Warp [{encoded_warp}] was claimed by multiple regions")
            warp_to_region_map[encoded_warp] = region_name
            new_region.warps.append(encoded_warp)

        regions[region_name] = new_region

    # LocationDatas
    for location_name, region_name in location_to_region_map.items():
        location_json = extracted_data["locations"][location_name]
        new_location = LocationData(
            location_name,
            location_to_region_map[location_name],
            location_json["default_item"],
            location_json["rom_address"],
            location_json["flag"]
        )
        regions[new_location.region_name].locations.append(new_location)

    return regions


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
            if region_name in merged_regions:
                raise AssertionError("Region [{region_name}] was defined multiple times")
            merged_regions[region_name] = region_data

    return merged_regions


def get_location_to_region_map() -> Dict[str, str]:
    if location_to_region_map is None:
        raise AssertionError("Cannot get_location_to_region_map before region data has been loaded")
    return location_to_region_map


def get_warp_to_region_map() -> Dict[str, str]:
    if warp_to_region_map is None:
        raise AssertionError("Cannot get_warp_to_region_map before region data has been loaded")
    return warp_to_region_map


def get_item_attributes() -> Dict[int, ItemData]:
    global item_attributes
    extracted_data = get_extracted_data()
    if item_attributes is None:
        item_attributes = {}
        items_json = load_json(os.path.join(os.path.dirname(__file__), "data/items.json"))

        for item_constant_name, attributes in items_json.items():
            item_id = extracted_data["constants"][item_constant_name]
            item_attributes[item_id] = ItemData(
                attributes["label"],
                _str_to_item_classification(attributes["classification"]),
                set(attributes["tags"])
            )

    return item_attributes


def get_location_attributes() -> Dict[str, LocationAttributes]:
    global location_attributes
    if location_attributes is None:
        location_attributes = {}
        locations_json = load_json(os.path.join(os.path.dirname(__file__), "data/locations.json"))

        for location_constant_name, attributes in locations_json.items():
            location_attributes[location_constant_name] = LocationAttributes(
                attributes["label"],
                set(attributes["tags"])
            )

    return location_attributes


def _str_to_item_classification(string):
    if string == "PROGRESSION":
        return ItemClassification.progression
    elif string == "USEFUL":
        return ItemClassification.useful
    elif string == "FILLER":
        return ItemClassification.filler
    elif string == "TRAP":
        return ItemClassification.trap
