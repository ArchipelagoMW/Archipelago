import pkgutil
from typing import NamedTuple, FrozenSet, Dict, Union, List, Any

from maseya.z3pr.math_helper import clamp
from orjson import orjson

from BaseClasses import ItemClassification


class ClairObscurItemData(NamedTuple):
    name: str
    item_id: int
    classification: ItemClassification
    type: str

class ClairObscurLocationData(NamedTuple):
    name: str
    region: str
    default_item: str

class ClairObscurRegionData:
    name: str
    parent_map: str
    exits: List[str]
    locations: List[str]
    condition: {}

    def __init__(self, name: str, parent_map: str, cond: {}):
        self.name = name
        self.parent_map = parent_map
        self.exits = []
        self.locations = []
        self.condition = cond if cond is not None else {}


class ClairObscurData:
    items: Dict[int, ClairObscurItemData]
    locations: Dict[str, ClairObscurLocationData]
    regions: Dict[str, ClairObscurRegionData]

    def __init__(self) -> None:
        self.items = {}
        self.locations = {}
        self.regions = {}


def load_json_data(data_name: str) -> Union[List[Any], Dict[str, Any]]:
    return orjson.loads(pkgutil.get_data(__name__, "data/" + data_name))

def _init() -> None:
    data.items = populate_data_items()
    data.locations = populate_data_locations()
    data.regions = populate_data_regions()


def populate_data_locations() -> Dict[str, ClairObscurLocationData]:
    locations = {}
    locations_json = load_json_data("locations.json")
    for location in locations_json:
        location_name: str = location["name"]


        new_location = ClairObscurLocationData(
            location_name,
            location["location"],
            location["original_item"]
        )

        locations[location_name] = new_location

    return locations

def populate_data_items() -> dict[int, ClairObscurItemData]:
    items = {}
    items_json = load_json_data("items.json")
    item_id = 0
    for item in items_json:
        item_name: str = item["name"]
        classification = None
        if item["progressive"] == 0:
            classification = ItemClassification.filler
        elif item["progressive"] == 1:
            classification = ItemClassification.progression
        elif item["progressive"] == 2:
            classification = ItemClassification.useful
        else:
            raise ValueError(f"Unknown classification '{item["progressive"]}' for {item_name}")

        items[item_id] = ClairObscurItemData(
            item_name,
            item_id,
            classification,
            item["type"],
        )

        item_id += 1

    return items

def populate_data_regions() -> Dict[str, ClairObscurRegionData]:
    regions = {}
    claimed_locations = []
    regions_json = load_json_data("regions.json")
    for region in regions_json:
        region_name = region["region_name"]
        current_region_data = ClairObscurRegionData(
            region_name,
            region["parent_map"],
            region["condition"]
        )

        for location_name in region["locations"]:
            if location_name in claimed_locations:
                AssertionError(f"Location {location_name} already claimed")

            current_region_data.locations.append(location_name)
            claimed_locations.append(location_name)

        current_region_data.locations.sort()

        regions[region_name] = current_region_data

    return regions


data = ClairObscurData()
_init()