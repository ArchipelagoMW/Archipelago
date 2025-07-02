import pkgutil
from typing import NamedTuple, FrozenSet, Dict, Union, List, Any

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
    default_item: int

class ClairObscurRegionData:
    name: str
    entrances: List[str]
    locations: List[str]

    def __init__(self, name: str):
        self.name = name
        self.entrances = []
        self.locations = []


class ClairObscurData:
    items: Dict[int, ClairObscurItemData]
    locations: List[ClairObscurLocationData]

    def __init__(self) -> None:
        self.items = {}
        self.locations = []


def load_json_data(data_name: str) -> Union[List[Any], Dict[str, Any]]:
    return orjson.loads(pkgutil.get_data(__name__, "data/" + data_name))

def _init() -> None:
    data.items = populate_data_items()
    data.locations = populate_data_locations()


def populate_data_locations() -> List[ClairObscurLocationData]:
    locations = []
    locations_json = load_json_data("locations.json")
    for location in locations_json:
        location_name: str = location["name"]


        new_location = ClairObscurLocationData(
            location_name,
            location["location"],
            location["original_item"]
        )

        locations.append(new_location)

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
            raise ValueError(f"Unknow classification {item["progressive"]} for {item_name}")

        items[item_id] = ClairObscurItemData(
            item_name,
            item_id,
            classification,
            item["type"],
        )

        item_id += 1

    return items

data = ClairObscurData()
_init()