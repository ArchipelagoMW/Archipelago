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
    condition: Dict[str, int]

class ClairObscurRegionData:
    name: str
    locations: List[str]

    def __init__(self, name: str):
        self.name = name
        self.locations = []

class ClairObscurRegionConnection:
    origin_region: str
    destination_region: str
    condition: {}
    pictos_level: int

    def __init__(self, cond: {}, origin: str, destination: str, pictos: int):
        self.origin_region = origin
        self.destination_region = destination
        self.condition = cond if cond is not None else {}
        self.pictos_level = pictos if pictos is not None else 1

class ClairObscurData:
    items: Dict[int, ClairObscurItemData]
    locations: Dict[str, ClairObscurLocationData]
    regions: Dict[str, ClairObscurRegionData]
    connections: List[ClairObscurRegionConnection]

    def __init__(self) -> None:
        self.items = {}
        self.locations = {}
        self.regions = {}
        self.connections = []


def load_json_data(data_name: str) -> Union[List[Any], Dict[str, Any]]:
    return orjson.loads(pkgutil.get_data(__name__, "data/" + data_name))

def _init() -> None:
    data.items = populate_data_items()
    data.locations = populate_data_locations()
    data.regions = populate_data_regions()
    data.connections = populate_data_connections()

def populate_data_locations() -> Dict[str, ClairObscurLocationData]:
    locations = {}
    locations_json = load_json_data("locations.json")
    for location in locations_json:
        location_name: str = location["name"]
        location_condition = location["condition"]

        new_location = ClairObscurLocationData(
            location_name,
            location["location"],
            location["original_item"],
            location_condition
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
            item["type"]
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
            region_name
        )

        for location_name in region["locations"]:
            if location_name in claimed_locations:
                AssertionError(f"Location {location_name} already claimed")

            current_region_data.locations.append(location_name)
            claimed_locations.append(location_name)

        current_region_data.locations.sort()

        regions[region_name] = current_region_data

    return regions

def populate_data_connections() -> List[ClairObscurRegionConnection]:
    region_connections = []
    conns_json = load_json_data("connections.json")
    for conn in conns_json:
        conn_from = conn["from"]
        conn_to = conn["to"]
        conn_condition = conn["condition"]
        conn_pictos = int(conn["pictos_level"])

        new_connection = ClairObscurRegionConnection(
            conn_condition,
            conn_from,
            conn_to,
            conn_pictos
        )

        region_connections.append(new_connection)

    return region_connections

data = ClairObscurData()
_init()