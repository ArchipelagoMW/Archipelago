"""
Pulls data from JSON files in worlds/pokemon_emerald/data/ into classes.
This also includes marrying automatically extracted data with manually
defined data (like location labels or usable pokemon species), some cleanup
and sorting, and Warp methods.
"""
from dataclasses import dataclass
from enum import IntEnum
import json
from typing import Dict, List, NamedTuple, Optional, Set, Tuple, Any, Union
import pkgutil
import pkg_resources

from BaseClasses import ItemClassification

class Warp:
    """
    Represents warp events in the game like doorways or warp pads
    """
    is_one_way: bool
    source_map: str
    source_ids: List[int]
    dest_map: str
    dest_ids: int
    parent_region: Optional[str]

    def __init__(self, encoded_string: Optional[str] = None, parent_region: Optional[str] = None) -> None:
        if encoded_string is not None:
            decoded_warp = Warp.decode(encoded_string)
            self.is_one_way = decoded_warp.is_one_way
            self.source_map = decoded_warp.source_map
            self.source_ids = decoded_warp.source_ids
            self.dest_map = decoded_warp.dest_map
            self.dest_ids = decoded_warp.dest_ids
        self.parent_region = parent_region

    def encode(self) -> str:
        """
        Returns a string encoding of this warp
        """
        source_ids_string = ""
        for source_id in self.source_ids:
            source_ids_string += str(source_id) + ","
        source_ids_string = source_ids_string[:-1] # Remove last ","

        return f"{self.source_map}:{source_ids_string}/{self.dest_map}:{self.dest_ids}{'!' if self.is_one_way else ''}"

    def connects_to(self, other: 'Warp') -> bool:
        """
        Returns true if this warp sends the player to `other`
        """
        return self.dest_map == other.source_map and set(self.dest_ids) <= set(other.source_ids)

    @staticmethod
    def decode(encoded_string: str) -> 'Warp':
        """
        Create a Warp object from an encoded string
        """
        warp = Warp()
        warp.is_one_way = encoded_string.endswith("!")
        if warp.is_one_way:
            encoded_string = encoded_string[:-1]

        warp_source, warp_dest = encoded_string.split("/")
        warp_source_map, warp_source_indices = warp_source.split(":")
        warp_dest_map, warp_dest_indices = warp_dest.split(":")

        warp.source_map = warp_source_map
        warp.dest_map = warp_dest_map

        warp.source_ids = [int(index) for index in warp_source_indices.split(",")]
        warp.dest_ids = [int(index) for index in warp_dest_indices.split(",")]

        return warp


class ItemData(NamedTuple):
    label: str
    item_id: int
    classification: ItemClassification
    tags: Set[str]


class LocationData(NamedTuple):
    name: str
    label: str
    parent_region: str
    default_item: int
    rom_address: int
    flag: int
    tags: Set[str]


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


class BaseStats(NamedTuple):
    hp: int
    attack: int
    defense: int
    speed: int
    special_attack: int
    special_defense: int


class LearnsetMove(NamedTuple):
    level: int
    move_id: int


class EvolutionMethodEnum(IntEnum):
    LEVEL = 0
    LEVEL_ATK_LT_DEF = 1
    LEVEL_ATK_EQ_DEF = 2
    LEVEL_ATK_GT_DEF = 3
    LEVEL_SILCOON = 4
    LEVEL_CASCOON = 5
    LEVEL_NINJASK = 6
    LEVEL_SHEDINJA = 7
    ITEM = 8
    FRIENDSHIP = 9
    FRIENDSHIP_DAY = 10
    FRIENDSHIP_NIGHT = 11


def _str_to_evolution_method(string: str) -> EvolutionMethodEnum:
    if string == "LEVEL":
        return EvolutionMethodEnum.LEVEL
    if string == "LEVEL_ATK_LT_DEF":
        return EvolutionMethodEnum.LEVEL_ATK_LT_DEF
    if string == "LEVEL_ATK_EQ_DEF":
        return EvolutionMethodEnum.LEVEL_ATK_EQ_DEF
    if string == "LEVEL_ATK_GT_DEF":
        return EvolutionMethodEnum.LEVEL_ATK_GT_DEF
    if string == "LEVEL_SILCOON":
        return EvolutionMethodEnum.LEVEL_SILCOON
    if string == "LEVEL_CASCOON":
        return EvolutionMethodEnum.LEVEL_CASCOON
    if string == "LEVEL_NINJASK":
        return EvolutionMethodEnum.LEVEL_NINJASK
    if string == "LEVEL_SHEDINJA":
        return EvolutionMethodEnum.LEVEL_SHEDINJA
    if string == "FRIENDSHIP":
        return EvolutionMethodEnum.FRIENDSHIP
    if string == "FRIENDSHIP_DAY":
        return EvolutionMethodEnum.FRIENDSHIP_DAY
    if string == "FRIENDSHIP_NIGHT":
        return EvolutionMethodEnum.FRIENDSHIP_NIGHT


class EvolutionData(NamedTuple):
    method: EvolutionMethodEnum
    param: int
    species_id: int


class StaticEncounterData(NamedTuple):
    species_id: int
    rom_address: int


@dataclass
class SpeciesData:
    name: str
    label: str
    species_id: int
    national_dex_number: int
    base_stats: BaseStats
    types: Tuple[int, int]
    abilities: Tuple[int, int]
    evolutions: List[EvolutionData]
    pre_evolution: Optional[int]
    catch_rate: int
    learnset: List[LearnsetMove]
    tm_hm_compatibility: int
    learnset_rom_address: int
    rom_address: int


class AbilityData(NamedTuple):
    ability_id: int
    label: str


class EncounterTableData(NamedTuple):
    slots: List[int]
    rom_address: int


@dataclass
class MapData:
    name: str
    land_encounters: Optional[EncounterTableData]
    water_encounters: Optional[EncounterTableData]
    fishing_encounters: Optional[EncounterTableData]


class TrainerPokemonDataTypeEnum(IntEnum):
    NO_ITEM_DEFAULT_MOVES = 0
    ITEM_DEFAULT_MOVES = 1
    NO_ITEM_CUSTOM_MOVES = 2
    ITEM_CUSTOM_MOVES = 3


def _str_to_pokemon_data_type(string: str) -> TrainerPokemonDataTypeEnum:
    if string == "NO_ITEM_DEFAULT_MOVES":
        return TrainerPokemonDataTypeEnum.NO_ITEM_DEFAULT_MOVES
    if string == "ITEM_DEFAULT_MOVES":
        return TrainerPokemonDataTypeEnum.ITEM_DEFAULT_MOVES
    if string == "NO_ITEM_CUSTOM_MOVES":
        return TrainerPokemonDataTypeEnum.NO_ITEM_CUSTOM_MOVES
    if string == "ITEM_CUSTOM_MOVES":
        return TrainerPokemonDataTypeEnum.ITEM_CUSTOM_MOVES


@dataclass
class TrainerPokemonData:
    species_id: int
    level: int
    moves: Optional[Tuple[int, int, int, int]]


@dataclass
class TrainerPartyData:
    pokemon: List[TrainerPokemonData]
    pokemon_data_type: TrainerPokemonDataTypeEnum
    rom_address: int


@dataclass
class TrainerData:
    trainer_id: int
    party: TrainerPartyData
    rom_address: int
    battle_script_rom_address: int


class PokemonEmeraldData:
    starters: Tuple[int, int, int]
    constants: Dict[str, int]
    rom_addresses: Dict[str, int]
    regions: Dict[str, RegionData]
    locations: Dict[str, LocationData]
    items: Dict[int, ItemData]
    species: List[Optional[SpeciesData]]
    static_encounters: List[StaticEncounterData]
    tmhm_moves: List[int]
    abilities: List[AbilityData]
    maps: List[MapData]
    warps: Dict[str, Warp]
    warp_map: Dict[str, Optional[str]]
    trainers: List[TrainerData]

    def __init__(self):
        self.starters = (277, 280, 283)
        self.constants = {}
        self.rom_addresses = {}
        self.regions = {}
        self.locations = {}
        self.items = {}
        self.species = []
        self.static_encounters = []
        self.tmhm_moves = []
        self.abilities = []
        self.maps = []
        self.warps = {}
        self.warp_map = {}
        self.trainers = []


def load_json_data(data_name: str) -> Union[List[str], Dict[str, Any]]:
    return json.loads(pkgutil.get_data(__name__, "data/" + data_name).decode())


config: Dict[str, Any] = load_json_data("config.json")
data = PokemonEmeraldData()

def _init():
    extracted_data: Dict[str, any] = load_json_data("extracted_data.json")
    data.constants = extracted_data["constants"]
    data.rom_addresses = extracted_data["misc_rom_addresses"]

    location_attributes_json = load_json_data("locations.json")

    # Load/merge region json files
    region_json_list = []
    for file in pkg_resources.resource_listdir(__name__, "data/regions"):
        if not pkg_resources.resource_isdir(__name__, "data/regions/" + file):
            region_json_list.append(load_json_data("regions/" + file))

    regions_json = {}
    for region_subset in region_json_list:
        for region_name, region_json in region_subset.items():
            if region_name in regions_json:
                raise AssertionError("Region [{region_name}] was defined multiple times")
            regions_json[region_name] = region_json

    # Create region data
    claimed_locations: Set[str] = set()
    claimed_warps: Set[str] = set()

    data.regions = {}
    for region_name, region_json in regions_json.items():
        new_region = RegionData(region_name)

        # Locations
        for location_name in region_json["locations"]:
            if location_name in claimed_locations:
                raise AssertionError(f"Location [{location_name}] was claimed by multiple regions")

            location_json = extracted_data["locations"][location_name]
            new_location = LocationData(
                location_name,
                location_attributes_json[location_name]["label"],
                region_name,
                location_json["default_item"],
                location_json["rom_address"],
                location_json["flag"],
                set(location_attributes_json[location_name]["tags"])
            )
            new_region.locations.append(location_name)
            data.locations[location_name] = new_location
            claimed_locations.add(location_name)

        new_region.locations.sort()

        # Events
        for event in region_json["events"]:
            new_region.events.append(EventData(event, region_name))

        # Exits
        for region_exit in region_json["exits"]:
            new_region.exits.append(region_exit)

        # Warps
        for encoded_warp in region_json["warps"]:
            if encoded_warp in claimed_warps:
                raise AssertionError(f"Warp [{encoded_warp}] was claimed by multiple regions")
            new_region.warps.append(encoded_warp)
            data.warps[encoded_warp] = Warp(encoded_warp, region_name)
            claimed_warps.add(encoded_warp)

        new_region.warps.sort()

        data.regions[region_name] = new_region

    # Create item data
    items_json = load_json_data("items.json")

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
            raise ValueError(f"Unknown classification {attributes['classification']} for item {item_constant_name}")

        data.items[data.constants[item_constant_name]] = ItemData(
            attributes["label"],
            data.constants[item_constant_name],
            item_classification,
            set(attributes["tags"])
        )

    # Create species data
    species_json = load_json_data("pokemon.json")
    species_list: List[SpeciesData] = []
    max_species_id = 0
    for species_name, species_attributes in species_json.items():
        species_id = data.constants[species_name]
        max_species_id = max(species_id, max_species_id)
        individual_species_json = extracted_data["species"][species_id]

        learnset = [LearnsetMove(item["level"], item["move_id"]) for item in individual_species_json["learnset"]["moves"]]

        species_list.append(SpeciesData(
            species_name,
            species_attributes["label"],
            species_id,
            species_attributes["national_dex_number"],
            BaseStats(
                individual_species_json["base_stats"][0],
                individual_species_json["base_stats"][1],
                individual_species_json["base_stats"][2],
                individual_species_json["base_stats"][3],
                individual_species_json["base_stats"][4],
                individual_species_json["base_stats"][5]
            ),
            (individual_species_json["types"][0], individual_species_json["types"][1]),
            (individual_species_json["abilities"][0], individual_species_json["abilities"][1]),
            [EvolutionData(
                _str_to_evolution_method(evolution_json["method"]),
                evolution_json["param"],
                evolution_json["species"],
            ) for evolution_json in individual_species_json["evolutions"]],
            None,
            individual_species_json["catch_rate"],
            learnset,
            int(individual_species_json["tmhm_learnset"], 16),
            individual_species_json["learnset"]["rom_address"],
            individual_species_json["rom_address"]
        ))

    data.species = [None for i in range(max_species_id + 1)]

    for species in species_list:
        data.species[species.species_id] = species

    for species in data.species:
        if species is not None:
            for evolution in species.evolutions:
                data.species[evolution.species_id].pre_evolution = species.species_id

    # Create static encounter data
    for static_encounter_json in extracted_data["static_encounters"]:
        data.static_encounters.append(StaticEncounterData(
            static_encounter_json["species"],
            static_encounter_json["rom_address"]
        ))

    # TM moves
    data.tmhm_moves = extracted_data["tmhm_moves"]

    # Create ability data
    abilities_json = load_json_data("abilities.json")
    for ability_name, ability_json in abilities_json.items():
        data.abilities.append(AbilityData(
            data.constants[ability_name],
            ability_json["label"]
        ))

    # Create map data
    for map_name, map_json in extracted_data["maps"].items():
        land_encounters = None
        water_encounters = None
        fishing_encounters = None

        if map_json["land_encounters"] is not None:
            land_encounters = EncounterTableData(
                map_json["land_encounters"]["encounter_slots"],
                map_json["land_encounters"]["rom_address"]
            )
        if map_json["water_encounters"] is not None:
            water_encounters = EncounterTableData(
                map_json["water_encounters"]["encounter_slots"],
                map_json["water_encounters"]["rom_address"]
            )
        if map_json["fishing_encounters"] is not None:
            fishing_encounters = EncounterTableData(
                map_json["fishing_encounters"]["encounter_slots"],
                map_json["fishing_encounters"]["rom_address"]
            )

        data.maps.append(MapData(
            map_name,
            land_encounters,
            water_encounters,
            fishing_encounters
        ))

    data.maps.sort(key=lambda map: map.name)

    # Create warp map
    for encoded_warp, warp in data.warps.items():
        for encoded_other_warp, other_warp in data.warps.items():
            if warp.connects_to(other_warp):
                data.warp_map[encoded_warp] = encoded_other_warp
                break

        if encoded_warp not in data.warp_map:
            data.warp_map[encoded_warp] = None

    # Create trainer data
    for i, trainer_json in enumerate(extracted_data["trainers"]):
        party_json = trainer_json["party"]
        pokemon_data_type = _str_to_pokemon_data_type(trainer_json["pokemon_data_type"])
        data.trainers.append(TrainerData(
            i,
            TrainerPartyData(
                [TrainerPokemonData(
                    p["species"],
                    p["level"],
                    (p["moves"][0], p["moves"][1], p["moves"][2], p["moves"][3])
                ) for p in party_json],
                pokemon_data_type,
                trainer_json["party_rom_address"]
            ),
            trainer_json["rom_address"],
            trainer_json["battle_script_rom_address"]
        ))

_init()
