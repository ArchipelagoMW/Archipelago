import orjson
import pkgutil
from typing import Dict, List, NamedTuple, Optional, Set, FrozenSet, Tuple, Any, Union

from BaseClasses import ItemClassification

BASE_OFFSET = 7680000


class ItemData(NamedTuple):
    label: str
    item_id: int
    classification: ItemClassification
    # tags: FrozenSet[str]


class LocationData(NamedTuple):
    name: str
    # label: str
    parent_region: str
    default_item: int
    rom_address: int
    # flag: int
    # tags: FrozenSet[str]
    location_type: str
    script: str


class EventData(NamedTuple):
    name: str
    parent_region: str


class RegionData:
    name: str
    exits: List[str]
    warps: List[str]
    locations: List[str]
    events: List[EventData]

    def __init__(self, name: str):
        self.name = name
        self.exits = []
        self.warps = []
        self.locations = []
        self.events = []


class PokemonCrystalData:
    rom_addresses: Dict[str, int]
    regions: Dict[str, RegionData]
    locations: Dict[str, LocationData]
    items: Dict[int, ItemData]

    def __init__(self) -> None:
        self.rom_addresses = {}
        self.regions = {}
        self.locations = {}
        self.items = {}


def load_json_data(data_name: str) -> Union[List[Any], Dict[str, Any]]:
    return orjson.loads(pkgutil.get_data(__name__, "data/" + data_name).decode('utf-8-sig'))


data = PokemonCrystalData()


def _init() -> None:
    location_data = load_json_data("locations.json")
    regions_json = load_json_data("regions.json")
    rom_address_data = load_json_data("rom_addresses.json")
    items_json = load_json_data("items.json")
    item_codes_json = load_json_data("item_codes.json")

    claimed_locations: Set[str] = set()
    claimed_warps: Set[str] = set()

    data.regions = {}

    for region_name, region_json in regions_json.items():
        new_region = RegionData(region_name)

        # Locations
        for location_name in region_json["locations"]:
            if location_name in claimed_locations:
                raise AssertionError(
                    f"Location [{location_name}] was claimed by multiple regions")
            location_json = location_data[location_name]
            new_location = LocationData(
                location_name,
                region_name,
                item_codes_json[location_json["default_item"]],
                rom_address_data[location_json["script"]],
                location_json["type"],
                location_json["script"]
            )
            new_region.locations.append(location_name)
            data.locations[location_name] = new_location
            claimed_locations.add(location_name)

        new_region.locations.sort()
        # events
        for event in region_json["events"]:
            new_region.events.append(EventData(event, region_name))

        # Exits
        for region_exit in region_json["exits"]:
            new_region.exits.append(region_exit)

        data.regions[region_name] = new_region

    # items

    data.items = {}
    for item_constant_name, attributes in items_json.items():
        item_classification = None
        if attributes["classification"] == "PROGRESSION":
            item_classification = ItemClassification.progression
        elif attributes["classification"] == "USEFUL":
            item_classification = ItemClassification.useful
        elif attributes["classification"] == "FILLER":
            item_classification = ItemClassification.filler
        elif attributes["classification"] == "TRAP":
            item_classification = ItemClassification.trap
        else:
            item_classification = ItemClassification.filler
            # raise ValueError(f"Unknown classification {attributes['classification']} for item {item_constant_name}")

        data.items[item_codes_json[item_constant_name]] = ItemData(
            attributes["name"],
            item_codes_json[item_constant_name],
            item_classification
        )

    data.rom_addresses = {}
    for address_name, address in rom_address_data.items():
        data.rom_addresses[address_name] = address


_init()
