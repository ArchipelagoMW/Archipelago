import json
# import orjson
import pkgutil
from typing import Dict, List, NamedTuple, Optional, Set, FrozenSet, Tuple, Any, Union

from BaseClasses import ItemClassification

BASE_OFFSET = 7680000


class ItemData(NamedTuple):
    label: str
    item_id: int
    item_const: str
    classification: ItemClassification
    tags: FrozenSet[str]


class LocationData(NamedTuple):
    name: str
    label: str
    parent_region: str
    default_item: int
    rom_address: int
    flag: int
    tags: FrozenSet[str]
    # location_type: str
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


class LearnsetData(NamedTuple):
    level: int
    move: str


class PokemonData(NamedTuple):
    id: int
    base_stats: List[int]
    types: List[str]
    evolutions: List[List[str]]
    learnset: List[LearnsetData]
    tm_hm: List[str]


class MoveData(NamedTuple):
    id: int
    type: str
    power: int
    accuracy: int
    pp: int
    is_hm: bool


class TrainerData(NamedTuple):
    trainer_type: str
    pokemon: List[List[str]]
    name_length: int


class PokemonCrystalData:
    rom_addresses: Dict[str, int]
    ram_addresses: Dict[str, int]
    event_flags: Dict[str, int]
    regions: Dict[str, RegionData]
    locations: Dict[str, LocationData]
    items: Dict[int, ItemData]
    trainers: Dict[str, TrainerData]
    pokemon: Dict[str, PokemonData]
    moves: Dict[str, MoveData]

    def __init__(self) -> None:
        self.rom_addresses = {}
        self.ram_addresses = {}
        self.event_flags = {}
        self.regions = {}
        self.locations = {}
        self.items = {}
        self.trainers = {}
        self.pokemon = {}
        self.moves = {}


def load_json_data(data_name: str) -> Union[List[Any], Dict[str, Any]]:
    return json.loads(pkgutil.get_data(__name__, "data/" + data_name).decode('utf-8-sig'))
    # return orjson.loads(pkgutil.get_data(__name__, "data/" + data_name).decode('utf-8-sig'))


data = PokemonCrystalData()


def _init() -> None:
    location_data = load_json_data("locations.json")
    regions_json = load_json_data("regions.json")

    items_json = load_json_data("items.json")

    data_json = load_json_data("data.json")
    rom_address_data = data_json["rom_addresses"]
    ram_address_data = data_json["ram_addresses"]
    event_flag_data = data_json["event_flags"]
    item_codes = data_json["items"]
    pokemon_data = data_json["pokemon"]
    move_data = data_json["moves"]
    trainer_data = data_json["trainers"]

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
                location_json["label"],
                region_name,
                item_codes[location_json["default_item"]],
                rom_address_data[location_json["script"]],
                event_flag_data[location_json["flag"]],
                frozenset(location_json["tags"]),
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

        data.items[item_codes[item_constant_name]] = ItemData(
            attributes["name"],
            item_codes[item_constant_name],
            item_constant_name,
            item_classification,
            frozenset(attributes["tags"])
        )

    data.ram_addresses = {}
    for address_name, address in ram_address_data.items():
        data.ram_addresses[address_name] = address

    data.rom_addresses = {}
    for address_name, address in rom_address_data.items():
        data.rom_addresses[address_name] = address

    data.event_flags = {}
    for event_name, event_number in event_flag_data.items():
        data.event_flags[event_name] = event_number

    data.pokemon = {}
    for pokemon_name, pokemon_data in data_json["pokemon"].items():
        data.pokemon[pokemon_name] = PokemonData(
            pokemon_data["id"],
            pokemon_data["base_stats"],
            pokemon_data["types"],
            pokemon_data["evolutions"],
            [LearnsetData(move[0], move[1])
             for move in pokemon_data["learnset"]],
            pokemon_data["tm_hm"])

    data.moves = {}
    for move_name, move_attributes in move_data.items():
        data.moves[move_name] = MoveData(
            move_attributes["id"],
            move_attributes["type"],
            move_attributes["power"],
            move_attributes["accuracy"],
            move_attributes["pp"],
            move_attributes["is_hm"],
        )

    data.trainers = {}
    for trainer_name, trainer_attributes in trainer_data.items():
        data.trainers[trainer_name] = TrainerData(
            trainer_attributes["trainer_type"],
            trainer_attributes["pokemon"],
            trainer_attributes["name_length"]
        )


_init()
