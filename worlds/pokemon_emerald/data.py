"""
Pulls data from JSON files in worlds/pokemon_emerald/data/ into classes.
This also includes marrying automatically extracted data with manually
defined data (like location labels or usable pokemon species), some cleanup
and sorting, and Warp methods.
"""
from dataclasses import dataclass
from enum import IntEnum
import json
from typing import Dict, List, NamedTuple, Optional, Set, FrozenSet, Tuple, Any, Union
import pkgutil
import pkg_resources

from BaseClasses import ItemClassification


BASE_OFFSET = 3860000


class Warp:
    """
    Represents warp events in the game like doorways or warp pads
    """
    is_one_way: bool
    source_map: str
    source_ids: List[int]
    dest_map: str
    dest_ids: List[int]
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
        source_ids_string = source_ids_string[:-1]  # Remove last ","

        dest_ids_string = ""
        for dest_id in self.dest_ids:
            dest_ids_string += str(dest_id) + ","
        dest_ids_string = dest_ids_string[:-1]  # Remove last ","

        return f"{self.source_map}:{source_ids_string}/{self.dest_map}:{dest_ids_string}{'!' if self.is_one_way else ''}"

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
    tags: FrozenSet[str]


class LocationData(NamedTuple):
    name: str
    label: str
    parent_region: str
    default_item: int
    address: Union[int, List[int]]
    flag: int
    tags: FrozenSet[str]


class EncounterTableData(NamedTuple):
    slots: List[int]
    address: int


@dataclass
class MapData:
    name: str
    header_address: int
    land_encounters: Optional[EncounterTableData]
    water_encounters: Optional[EncounterTableData]
    fishing_encounters: Optional[EncounterTableData]


class EventData(NamedTuple):
    name: str
    parent_region: str


class RegionData:
    name: str
    parent_map: MapData
    has_grass: bool
    has_water: bool
    has_fishing: bool
    exits: List[str]
    warps: List[str]
    locations: List[str]
    events: List[EventData]

    def __init__(self, name: str, parent_map: MapData, has_grass: bool, has_water: bool, has_fishing: bool):
        self.name = name
        self.parent_map = parent_map
        self.has_grass = has_grass
        self.has_water = has_water
        self.has_fishing = has_fishing
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
    address: int


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
    friendship: int
    learnset: List[LearnsetMove]
    tm_hm_compatibility: int
    learnset_address: int
    address: int


class AbilityData(NamedTuple):
    ability_id: int
    label: str


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
    address: int


@dataclass
class TrainerData:
    trainer_id: int
    party: TrainerPartyData
    address: int
    script_address: int


class PokemonEmeraldData:
    starters: Tuple[int, int, int]
    constants: Dict[str, int]
    ram_addresses: Dict[str, int]
    rom_addresses: Dict[str, int]
    regions: Dict[str, RegionData]
    locations: Dict[str, LocationData]
    items: Dict[int, ItemData]
    species: List[Optional[SpeciesData]]
    static_encounters: List[StaticEncounterData]
    tmhm_moves: List[int]
    abilities: List[AbilityData]
    maps: Dict[str, MapData]
    warps: Dict[str, Warp]
    warp_map: Dict[str, Optional[str]]
    trainers: List[TrainerData]

    def __init__(self) -> None:
        self.starters = (277, 280, 283)
        self.constants = {}
        self.ram_addresses = {}
        self.rom_addresses = {}
        self.regions = {}
        self.locations = {}
        self.items = {}
        self.species = []
        self.static_encounters = []
        self.tmhm_moves = []
        self.abilities = []
        self.maps = {}
        self.warps = {}
        self.warp_map = {}
        self.trainers = []


def load_json_data(data_name: str) -> Union[List[Any], Dict[str, Any]]:
    return json.loads(pkgutil.get_data(__name__, "data/" + data_name).decode('utf-8-sig'))


data = PokemonEmeraldData()


def _init() -> None:
    extracted_data: Dict[str, Any] = load_json_data("extracted_data.json")
    data.constants = extracted_data["constants"]
    data.ram_addresses = extracted_data["misc_ram_addresses"]
    data.rom_addresses = extracted_data["misc_rom_addresses"]

    location_attributes_json = load_json_data("locations.json")

    # Create map data
    for map_name, map_json in extracted_data["maps"].items():
        land_encounters = None
        water_encounters = None
        fishing_encounters = None

        if "land_encounters" in map_json:
            land_encounters = EncounterTableData(
                map_json["land_encounters"]["slots"],
                map_json["land_encounters"]["address"]
            )
        if "water_encounters" in map_json:
            water_encounters = EncounterTableData(
                map_json["water_encounters"]["slots"],
                map_json["water_encounters"]["address"]
            )
        if "fishing_encounters" in map_json:
            fishing_encounters = EncounterTableData(
                map_json["fishing_encounters"]["slots"],
                map_json["fishing_encounters"]["address"]
            )

        data.maps[map_name] = MapData(
            map_name,
            map_json["header_address"],
            land_encounters,
            water_encounters,
            fishing_encounters
        )

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
        new_region = RegionData(
            region_name,
            data.maps[region_json["parent_map"]],
            region_json["has_grass"],
            region_json["has_water"],
            region_json["has_fishing"]
        )

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
                location_json["address"],
                location_json["flag"],
                frozenset(location_attributes_json[location_name]["tags"])
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
            frozenset(attributes["tags"])
        )

    # Create species data

    # Excludes extras like copies of Unown and special species values like SPECIES_EGG.
    all_species: List[Tuple[str, str]] = [
        ("SPECIES_BULBASAUR", "Bulbasaur", 1),
        ("SPECIES_IVYSAUR", "Ivysaur", 2),
        ("SPECIES_VENUSAUR", "Venusaur", 3),
        ("SPECIES_CHARMANDER", "Charmander", 4),
        ("SPECIES_CHARMELEON", "Charmeleon", 5),
        ("SPECIES_CHARIZARD", "Charizard", 6),
        ("SPECIES_SQUIRTLE", "Squirtle", 7),
        ("SPECIES_WARTORTLE", "Wartortle", 8),
        ("SPECIES_BLASTOISE", "Blastoise", 9),
        ("SPECIES_CATERPIE", "Caterpie", 10),
        ("SPECIES_METAPOD", "Metapod", 11),
        ("SPECIES_BUTTERFREE", "Butterfree", 12),
        ("SPECIES_WEEDLE", "Weedle", 13),
        ("SPECIES_KAKUNA", "Kakuna", 14),
        ("SPECIES_BEEDRILL", "Beedrill", 15),
        ("SPECIES_PIDGEY", "Pidgey", 16),
        ("SPECIES_PIDGEOTTO", "Pidgeotto", 17),
        ("SPECIES_PIDGEOT", "Pidgeot", 18),
        ("SPECIES_RATTATA", "Rattata", 19),
        ("SPECIES_RATICATE", "Raticate", 20),
        ("SPECIES_SPEAROW", "Spearow", 21),
        ("SPECIES_FEAROW", "Fearow", 22),
        ("SPECIES_EKANS", "Ekans", 23),
        ("SPECIES_ARBOK", "Arbok", 24),
        ("SPECIES_PIKACHU", "Pikachu", 25),
        ("SPECIES_RAICHU", "Raichu", 26),
        ("SPECIES_SANDSHREW", "Sandshrew", 27),
        ("SPECIES_SANDSLASH", "Sandslash", 28),
        ("SPECIES_NIDORAN_F", "Nidoran Female", 29),
        ("SPECIES_NIDORINA", "Nidorina", 30),
        ("SPECIES_NIDOQUEEN", "Nidoqueen", 31),
        ("SPECIES_NIDORAN_M", "Nidoran Male", 32),
        ("SPECIES_NIDORINO", "Nidorino", 33),
        ("SPECIES_NIDOKING", "Nidoking", 34),
        ("SPECIES_CLEFAIRY", "Clefairy", 35),
        ("SPECIES_CLEFABLE", "Clefable", 36),
        ("SPECIES_VULPIX", "Vulpix", 37),
        ("SPECIES_NINETALES", "Ninetales", 38),
        ("SPECIES_JIGGLYPUFF", "Jigglypuff", 39),
        ("SPECIES_WIGGLYTUFF", "Wigglytuff", 40),
        ("SPECIES_ZUBAT", "Zubat", 41),
        ("SPECIES_GOLBAT", "Golbat", 42),
        ("SPECIES_ODDISH", "Oddish", 43),
        ("SPECIES_GLOOM", "Gloom", 44),
        ("SPECIES_VILEPLUME", "Vileplume", 45),
        ("SPECIES_PARAS", "Paras", 46),
        ("SPECIES_PARASECT", "Parasect", 47),
        ("SPECIES_VENONAT", "Venonat", 48),
        ("SPECIES_VENOMOTH", "Venomoth", 49),
        ("SPECIES_DIGLETT", "Diglett", 50),
        ("SPECIES_DUGTRIO", "Dugtrio", 51),
        ("SPECIES_MEOWTH", "Meowth", 52),
        ("SPECIES_PERSIAN", "Persian", 53),
        ("SPECIES_PSYDUCK", "Psyduck", 54),
        ("SPECIES_GOLDUCK", "Golduck", 55),
        ("SPECIES_MANKEY", "Mankey", 56),
        ("SPECIES_PRIMEAPE", "Primeape", 57),
        ("SPECIES_GROWLITHE", "Growlithe", 58),
        ("SPECIES_ARCANINE", "Arcanine", 59),
        ("SPECIES_POLIWAG", "Poliwag", 60),
        ("SPECIES_POLIWHIRL", "Poliwhirl", 61),
        ("SPECIES_POLIWRATH", "Poliwrath", 62),
        ("SPECIES_ABRA", "Abra", 63),
        ("SPECIES_KADABRA", "Kadabra", 64),
        ("SPECIES_ALAKAZAM", "Alakazam", 65),
        ("SPECIES_MACHOP", "Machop", 66),
        ("SPECIES_MACHOKE", "Machoke", 67),
        ("SPECIES_MACHAMP", "Machamp", 68),
        ("SPECIES_BELLSPROUT", "Bellsprout", 69),
        ("SPECIES_WEEPINBELL", "Weepinbell", 70),
        ("SPECIES_VICTREEBEL", "Victreebel", 71),
        ("SPECIES_TENTACOOL", "Tentacool", 72),
        ("SPECIES_TENTACRUEL", "Tentacruel", 73),
        ("SPECIES_GEODUDE", "Geodude", 74),
        ("SPECIES_GRAVELER", "Graveler", 75),
        ("SPECIES_GOLEM", "Golem", 76),
        ("SPECIES_PONYTA", "Ponyta", 77),
        ("SPECIES_RAPIDASH", "Rapidash", 78),
        ("SPECIES_SLOWPOKE", "Slowpoke", 79),
        ("SPECIES_SLOWBRO", "Slowbro", 80),
        ("SPECIES_MAGNEMITE", "Magnemite", 81),
        ("SPECIES_MAGNETON", "Magneton", 82),
        ("SPECIES_FARFETCHD", "Farfetch'd", 83),
        ("SPECIES_DODUO", "Doduo", 84),
        ("SPECIES_DODRIO", "Dodrio", 85),
        ("SPECIES_SEEL", "Seel", 86),
        ("SPECIES_DEWGONG", "Dewgong", 87),
        ("SPECIES_GRIMER", "Grimer", 88),
        ("SPECIES_MUK", "Muk", 89),
        ("SPECIES_SHELLDER", "Shellder", 90),
        ("SPECIES_CLOYSTER", "Cloyster", 91),
        ("SPECIES_GASTLY", "Gastly", 92),
        ("SPECIES_HAUNTER", "Haunter", 93),
        ("SPECIES_GENGAR", "Gengar", 94),
        ("SPECIES_ONIX", "Onix", 95),
        ("SPECIES_DROWZEE", "Drowzee", 96),
        ("SPECIES_HYPNO", "Hypno", 97),
        ("SPECIES_KRABBY", "Krabby", 98),
        ("SPECIES_KINGLER", "Kingler", 99),
        ("SPECIES_VOLTORB", "Voltorb", 100),
        ("SPECIES_ELECTRODE", "Electrode", 101),
        ("SPECIES_EXEGGCUTE", "Exeggcute", 102),
        ("SPECIES_EXEGGUTOR", "Exeggutor", 103),
        ("SPECIES_CUBONE", "Cubone", 104),
        ("SPECIES_MAROWAK", "Marowak", 105),
        ("SPECIES_HITMONLEE", "Hitmonlee", 106),
        ("SPECIES_HITMONCHAN", "Hitmonchan", 107),
        ("SPECIES_LICKITUNG", "Lickitung", 108),
        ("SPECIES_KOFFING", "Koffing", 109),
        ("SPECIES_WEEZING", "Weezing", 110),
        ("SPECIES_RHYHORN", "Rhyhorn", 111),
        ("SPECIES_RHYDON", "Rhydon", 112),
        ("SPECIES_CHANSEY", "Chansey", 113),
        ("SPECIES_TANGELA", "Tangela", 114),
        ("SPECIES_KANGASKHAN", "Kangaskhan", 115),
        ("SPECIES_HORSEA", "Horsea", 116),
        ("SPECIES_SEADRA", "Seadra", 117),
        ("SPECIES_GOLDEEN", "Goldeen", 118),
        ("SPECIES_SEAKING", "Seaking", 119),
        ("SPECIES_STARYU", "Staryu", 120),
        ("SPECIES_STARMIE", "Starmie", 121),
        ("SPECIES_MR_MIME", "Mr. Mime", 122),
        ("SPECIES_SCYTHER", "Scyther", 123),
        ("SPECIES_JYNX", "Jynx", 124),
        ("SPECIES_ELECTABUZZ", "Electabuzz", 125),
        ("SPECIES_MAGMAR", "Magmar", 126),
        ("SPECIES_PINSIR", "Pinsir", 127),
        ("SPECIES_TAUROS", "Tauros", 128),
        ("SPECIES_MAGIKARP", "Magikarp", 129),
        ("SPECIES_GYARADOS", "Gyarados", 130),
        ("SPECIES_LAPRAS", "Lapras", 131),
        ("SPECIES_DITTO", "Ditto", 132),
        ("SPECIES_EEVEE", "Eevee", 133),
        ("SPECIES_VAPOREON", "Vaporeon", 134),
        ("SPECIES_JOLTEON", "Jolteon", 135),
        ("SPECIES_FLAREON", "Flareon", 136),
        ("SPECIES_PORYGON", "Porygon", 137),
        ("SPECIES_OMANYTE", "Omanyte", 138),
        ("SPECIES_OMASTAR", "Omastar", 139),
        ("SPECIES_KABUTO", "Kabuto", 140),
        ("SPECIES_KABUTOPS", "Kabutops", 141),
        ("SPECIES_AERODACTYL", "Aerodactyl", 142),
        ("SPECIES_SNORLAX", "Snorlax", 143),
        ("SPECIES_ARTICUNO", "Articuno", 144),
        ("SPECIES_ZAPDOS", "Zapdos", 145),
        ("SPECIES_MOLTRES", "Moltres", 146),
        ("SPECIES_DRATINI", "Dratini", 147),
        ("SPECIES_DRAGONAIR", "Dragonair", 148),
        ("SPECIES_DRAGONITE", "Dragonite", 149),
        ("SPECIES_MEWTWO", "Mewtwo", 150),
        ("SPECIES_MEW", "Mew", 151),
        ("SPECIES_CHIKORITA", "Chikorita", 152),
        ("SPECIES_BAYLEEF", "Bayleaf", 153),
        ("SPECIES_MEGANIUM", "Meganium", 154),
        ("SPECIES_CYNDAQUIL", "Cindaquil", 155),
        ("SPECIES_QUILAVA", "Quilava", 156),
        ("SPECIES_TYPHLOSION", "Typhlosion", 157),
        ("SPECIES_TOTODILE", "Totodile", 158),
        ("SPECIES_CROCONAW", "Croconaw", 159),
        ("SPECIES_FERALIGATR", "Feraligatr", 160),
        ("SPECIES_SENTRET", "Sentret", 161),
        ("SPECIES_FURRET", "Furret", 162),
        ("SPECIES_HOOTHOOT", "Hoothoot", 163),
        ("SPECIES_NOCTOWL", "Noctowl", 164),
        ("SPECIES_LEDYBA", "Ledyba", 165),
        ("SPECIES_LEDIAN", "Ledian", 166),
        ("SPECIES_SPINARAK", "Spinarak", 167),
        ("SPECIES_ARIADOS", "Ariados", 168),
        ("SPECIES_CROBAT", "Crobat", 169),
        ("SPECIES_CHINCHOU", "Chinchou", 170),
        ("SPECIES_LANTURN", "Lanturn", 171),
        ("SPECIES_PICHU", "Pichu", 172),
        ("SPECIES_CLEFFA", "Cleffa", 173),
        ("SPECIES_IGGLYBUFF", "Igglybuff", 174),
        ("SPECIES_TOGEPI", "Togepi", 175),
        ("SPECIES_TOGETIC", "Togetic", 176),
        ("SPECIES_NATU", "Natu", 177),
        ("SPECIES_XATU", "Xatu", 178),
        ("SPECIES_MAREEP", "Mareep", 179),
        ("SPECIES_FLAAFFY", "Flaafy", 180),
        ("SPECIES_AMPHAROS", "Ampharos", 181),
        ("SPECIES_BELLOSSOM", "Bellossom", 182),
        ("SPECIES_MARILL", "Marill", 183),
        ("SPECIES_AZUMARILL", "Azumarill", 184),
        ("SPECIES_SUDOWOODO", "Sudowoodo", 185),
        ("SPECIES_POLITOED", "Politoed", 186),
        ("SPECIES_HOPPIP", "Hoppip", 187),
        ("SPECIES_SKIPLOOM", "Skiploom", 188),
        ("SPECIES_JUMPLUFF", "Jumpluff", 189),
        ("SPECIES_AIPOM", "Aipom", 190),
        ("SPECIES_SUNKERN", "Sunkern", 191),
        ("SPECIES_SUNFLORA", "Sunflora", 192),
        ("SPECIES_YANMA", "Yanma", 193),
        ("SPECIES_WOOPER", "Wooper", 194),
        ("SPECIES_QUAGSIRE", "Quagsire", 195),
        ("SPECIES_ESPEON", "Espeon", 196),
        ("SPECIES_UMBREON", "Umbreon", 197),
        ("SPECIES_MURKROW", "Murkrow", 198),
        ("SPECIES_SLOWKING", "Slowking", 199),
        ("SPECIES_MISDREAVUS", "Misdreavus", 200),
        ("SPECIES_UNOWN", "Unown", 201),
        ("SPECIES_WOBBUFFET", "Wobbuffet", 202),
        ("SPECIES_GIRAFARIG", "Girafarig", 203),
        ("SPECIES_PINECO", "Pineco", 204),
        ("SPECIES_FORRETRESS", "Forretress", 205),
        ("SPECIES_DUNSPARCE", "Dunsparce", 206),
        ("SPECIES_GLIGAR", "Gligar", 207),
        ("SPECIES_STEELIX", "Steelix", 208),
        ("SPECIES_SNUBBULL", "Snubbull", 209),
        ("SPECIES_GRANBULL", "Granbull", 210),
        ("SPECIES_QWILFISH", "Qwilfish", 211),
        ("SPECIES_SCIZOR", "Scizor", 212),
        ("SPECIES_SHUCKLE", "Shuckle", 213),
        ("SPECIES_HERACROSS", "Heracross", 214),
        ("SPECIES_SNEASEL", "Sneasel", 215),
        ("SPECIES_TEDDIURSA", "Teddiursa", 216),
        ("SPECIES_URSARING", "Ursaring", 217),
        ("SPECIES_SLUGMA", "Slugma", 218),
        ("SPECIES_MAGCARGO", "Magcargo", 219),
        ("SPECIES_SWINUB", "Swinub", 220),
        ("SPECIES_PILOSWINE", "Piloswine", 221),
        ("SPECIES_CORSOLA", "Corsola", 222),
        ("SPECIES_REMORAID", "Remoraid", 223),
        ("SPECIES_OCTILLERY", "Octillery", 224),
        ("SPECIES_DELIBIRD", "Delibird", 225),
        ("SPECIES_MANTINE", "Mantine", 226),
        ("SPECIES_SKARMORY", "Skarmory", 227),
        ("SPECIES_HOUNDOUR", "Houndour", 228),
        ("SPECIES_HOUNDOOM", "Houndoom", 229),
        ("SPECIES_KINGDRA", "Kingdra", 230),
        ("SPECIES_PHANPY", "Phanpy", 231),
        ("SPECIES_DONPHAN", "Donphan", 232),
        ("SPECIES_PORYGON2", "Porygon2", 233),
        ("SPECIES_STANTLER", "Stantler", 234),
        ("SPECIES_SMEARGLE", "Smeargle", 235),
        ("SPECIES_TYROGUE", "Tyrogue", 236),
        ("SPECIES_HITMONTOP", "Hitmontop", 237),
        ("SPECIES_SMOOCHUM", "Smoochum", 238),
        ("SPECIES_ELEKID", "Elekid", 239),
        ("SPECIES_MAGBY", "Magby", 240),
        ("SPECIES_MILTANK", "Miltank", 241),
        ("SPECIES_BLISSEY", "Blissey", 242),
        ("SPECIES_RAIKOU", "Raikou", 243),
        ("SPECIES_ENTEI", "Entei", 244),
        ("SPECIES_SUICUNE", "Suicune", 245),
        ("SPECIES_LARVITAR", "Larvitar", 246),
        ("SPECIES_PUPITAR", "Pupitar", 247),
        ("SPECIES_TYRANITAR", "Tyranitar", 248),
        ("SPECIES_LUGIA", "Lugia", 249),
        ("SPECIES_HO_OH", "Ho-oh", 250),
        ("SPECIES_CELEBI", "Celebi", 251),
        ("SPECIES_TREECKO", "Treecko", 252),
        ("SPECIES_GROVYLE", "Grovyle", 253),
        ("SPECIES_SCEPTILE", "Sceptile", 254),
        ("SPECIES_TORCHIC", "Torchic", 255),
        ("SPECIES_COMBUSKEN", "Combusken", 256),
        ("SPECIES_BLAZIKEN", "Blaziken", 257),
        ("SPECIES_MUDKIP", "Mudkip", 258),
        ("SPECIES_MARSHTOMP", "Marshtomp", 259),
        ("SPECIES_SWAMPERT", "Swampert", 260),
        ("SPECIES_POOCHYENA", "Poochyena", 261),
        ("SPECIES_MIGHTYENA", "Mightyena", 262),
        ("SPECIES_ZIGZAGOON", "Zigzagoon", 263),
        ("SPECIES_LINOONE", "Linoon", 264),
        ("SPECIES_WURMPLE", "Wurmple", 265),
        ("SPECIES_SILCOON", "Silcoon", 266),
        ("SPECIES_BEAUTIFLY", "Beautifly", 267),
        ("SPECIES_CASCOON", "Cascoon", 268),
        ("SPECIES_DUSTOX", "Dustox", 269),
        ("SPECIES_LOTAD", "Lotad", 270),
        ("SPECIES_LOMBRE", "Lombre", 271),
        ("SPECIES_LUDICOLO", "Ludicolo", 272),
        ("SPECIES_SEEDOT", "Seedot", 273),
        ("SPECIES_NUZLEAF", "Nuzleaf", 274),
        ("SPECIES_SHIFTRY", "Shiftry", 275),
        ("SPECIES_NINCADA", "Nincada", 290),
        ("SPECIES_NINJASK", "Ninjask", 291),
        ("SPECIES_SHEDINJA", "Shedinja", 292),
        ("SPECIES_TAILLOW", "Taillow", 276),
        ("SPECIES_SWELLOW", "Swellow", 277),
        ("SPECIES_SHROOMISH", "Shroomish", 285),
        ("SPECIES_BRELOOM", "Breloom", 286),
        ("SPECIES_SPINDA", "Spinda", 327),
        ("SPECIES_WINGULL", "Wingull", 278),
        ("SPECIES_PELIPPER", "Pelipper", 279),
        ("SPECIES_SURSKIT", "Surskit", 283),
        ("SPECIES_MASQUERAIN", "Masquerain", 284),
        ("SPECIES_WAILMER", "Wailmer", 320),
        ("SPECIES_WAILORD", "Wailord", 321),
        ("SPECIES_SKITTY", "Skitty", 300),
        ("SPECIES_DELCATTY", "Delcatty", 301),
        ("SPECIES_KECLEON", "Kecleon", 352),
        ("SPECIES_BALTOY", "Baltoy", 343),
        ("SPECIES_CLAYDOL", "Claydol", 344),
        ("SPECIES_NOSEPASS", "Nosepass", 299),
        ("SPECIES_TORKOAL", "Torkoal", 324),
        ("SPECIES_SABLEYE", "Sableye", 302),
        ("SPECIES_BARBOACH", "Barboach", 339),
        ("SPECIES_WHISCASH", "Whiscash", 340),
        ("SPECIES_LUVDISC", "Luvdisc", 370),
        ("SPECIES_CORPHISH", "Corphish", 341),
        ("SPECIES_CRAWDAUNT", "Crawdaunt", 342),
        ("SPECIES_FEEBAS", "Feebas", 349),
        ("SPECIES_MILOTIC", "Milotic", 350),
        ("SPECIES_CARVANHA", "Carvanha", 318),
        ("SPECIES_SHARPEDO", "Sharpedo", 319),
        ("SPECIES_TRAPINCH", "Trapinch", 328),
        ("SPECIES_VIBRAVA", "Vibrava", 329),
        ("SPECIES_FLYGON", "Flygon", 330),
        ("SPECIES_MAKUHITA", "Makuhita", 296),
        ("SPECIES_HARIYAMA", "Hariyama", 297),
        ("SPECIES_ELECTRIKE", "Electrike", 309),
        ("SPECIES_MANECTRIC", "Manectric", 310),
        ("SPECIES_NUMEL", "Numel", 322),
        ("SPECIES_CAMERUPT", "Camerupt", 323),
        ("SPECIES_SPHEAL", "Spheal", 363),
        ("SPECIES_SEALEO", "Sealeo", 364),
        ("SPECIES_WALREIN", "Walrein", 365),
        ("SPECIES_CACNEA", "Cacnea", 331),
        ("SPECIES_CACTURNE", "Cacturne", 332),
        ("SPECIES_SNORUNT", "Snorunt", 361),
        ("SPECIES_GLALIE", "Glalie", 362),
        ("SPECIES_LUNATONE", "Lunatone", 337),
        ("SPECIES_SOLROCK", "Solrock", 338),
        ("SPECIES_AZURILL", "Azurill", 298),
        ("SPECIES_SPOINK", "Spoink", 325),
        ("SPECIES_GRUMPIG", "Grumpig", 326),
        ("SPECIES_PLUSLE", "Plusle", 311),
        ("SPECIES_MINUN", "Minun", 312),
        ("SPECIES_MAWILE", "Mawile", 303),
        ("SPECIES_MEDITITE", "Meditite", 307),
        ("SPECIES_MEDICHAM", "Medicham", 308),
        ("SPECIES_SWABLU", "Swablu", 333),
        ("SPECIES_ALTARIA", "Altaria", 334),
        ("SPECIES_WYNAUT", "Wynaut", 360),
        ("SPECIES_DUSKULL", "Duskull", 355),
        ("SPECIES_DUSCLOPS", "Dusclops", 356),
        ("SPECIES_ROSELIA", "Roselia", 315),
        ("SPECIES_SLAKOTH", "Slakoth", 287),
        ("SPECIES_VIGOROTH", "Vigoroth", 288),
        ("SPECIES_SLAKING", "Slaking", 289),
        ("SPECIES_GULPIN", "Gulpin", 316),
        ("SPECIES_SWALOT", "Swalot", 317),
        ("SPECIES_TROPIUS", "Tropius", 357),
        ("SPECIES_WHISMUR", "Whismur", 293),
        ("SPECIES_LOUDRED", "Loudred", 294),
        ("SPECIES_EXPLOUD", "Exploud", 295),
        ("SPECIES_CLAMPERL", "Clamperl", 366),
        ("SPECIES_HUNTAIL", "Huntail", 367),
        ("SPECIES_GOREBYSS", "Gorebyss", 368),
        ("SPECIES_ABSOL", "Absol", 359),
        ("SPECIES_SHUPPET", "Shuppet", 353),
        ("SPECIES_BANETTE", "Banette", 354),
        ("SPECIES_SEVIPER", "Seviper", 336),
        ("SPECIES_ZANGOOSE", "Zangoose", 335),
        ("SPECIES_RELICANTH", "Relicanth", 369),
        ("SPECIES_ARON", "Aron", 304),
        ("SPECIES_LAIRON", "Lairon", 305),
        ("SPECIES_AGGRON", "Aggron", 306),
        ("SPECIES_CASTFORM", "Castform", 351),
        ("SPECIES_VOLBEAT", "Volbeat", 313),
        ("SPECIES_ILLUMISE", "Illumise", 314),
        ("SPECIES_LILEEP", "Lileep", 345),
        ("SPECIES_CRADILY", "Cradily", 346),
        ("SPECIES_ANORITH", "Anorith", 347),
        ("SPECIES_ARMALDO", "Armaldo", 348),
        ("SPECIES_RALTS", "Ralts", 280),
        ("SPECIES_KIRLIA", "Kirlia", 281),
        ("SPECIES_GARDEVOIR", "Gardevoir", 282),
        ("SPECIES_BAGON", "Bagon", 371),
        ("SPECIES_SHELGON", "Shelgon", 372),
        ("SPECIES_SALAMENCE", "Salamence", 373),
        ("SPECIES_BELDUM", "Beldum", 374),
        ("SPECIES_METANG", "Metang", 375),
        ("SPECIES_METAGROSS", "Metagross", 376),
        ("SPECIES_REGIROCK", "Regirock", 377),
        ("SPECIES_REGICE", "Regice", 378),
        ("SPECIES_REGISTEEL", "Registeel", 379),
        ("SPECIES_KYOGRE", "Kyogre", 382),
        ("SPECIES_GROUDON", "Groudon", 383),
        ("SPECIES_RAYQUAZA", "Rayquaza", 384),
        ("SPECIES_LATIAS", "Latias", 380),
        ("SPECIES_LATIOS", "Latios", 381),
        ("SPECIES_JIRACHI", "Jirachi", 385),
        ("SPECIES_DEOXYS", "Deoxys", 386),
        ("SPECIES_CHIMECHO", "Chimecho", 358),
    ]

    species_list: List[SpeciesData] = []
    max_species_id = 0
    for species_name, species_label, species_dex_number in all_species:
        species_id = data.constants[species_name]
        max_species_id = max(species_id, max_species_id)
        species_data = extracted_data["species"][species_id]

        learnset = [LearnsetMove(item["level"], item["move_id"]) for item in species_data["learnset"]["moves"]]

        species_list.append(SpeciesData(
            species_name,
            species_label,
            species_id,
            species_dex_number,
            BaseStats(
                species_data["base_stats"][0],
                species_data["base_stats"][1],
                species_data["base_stats"][2],
                species_data["base_stats"][3],
                species_data["base_stats"][4],
                species_data["base_stats"][5]
            ),
            (species_data["types"][0], species_data["types"][1]),
            (species_data["abilities"][0], species_data["abilities"][1]),
            [EvolutionData(
                _str_to_evolution_method(evolution_json["method"]),
                evolution_json["param"],
                evolution_json["species"],
            ) for evolution_json in species_data["evolutions"]],
            None,
            species_data["catch_rate"],
            species_data["friendship"],
            learnset,
            int(species_data["tmhm_learnset"], 16),
            species_data["learnset"]["address"],
            species_data["address"]
        ))

    data.species = [None for i in range(max_species_id + 1)]

    for species_data in species_list:
        data.species[species_data.species_id] = species_data

    for species in data.species:
        if species is not None:
            for evolution in species.evolutions:
                data.species[evolution.species_id].pre_evolution = species.species_id

    # Create static encounter data
    for static_encounter_json in extracted_data["static_encounters"]:
        data.static_encounters.append(StaticEncounterData(
            static_encounter_json["species"],
            static_encounter_json["address"]
        ))

    # TM moves
    data.tmhm_moves = extracted_data["tmhm_moves"]

    # Create ability data
    data.abilities = [AbilityData(data.constants[ability_data[0]], ability_data[1]) for ability_data in [
        ("ABILITY_STENCH", "Stench"),
        ("ABILITY_DRIZZLE", "Drizzle"),
        ("ABILITY_SPEED_BOOST", "Speed Boost"),
        ("ABILITY_BATTLE_ARMOR", "Battle Armor"),
        ("ABILITY_STURDY", "Sturdy"),
        ("ABILITY_DAMP", "Damp"),
        ("ABILITY_LIMBER", "Limber"),
        ("ABILITY_SAND_VEIL", "Sand Veil"),
        ("ABILITY_STATIC", "Static"),
        ("ABILITY_VOLT_ABSORB", "Volt Absorb"),
        ("ABILITY_WATER_ABSORB", "Water Absorb"),
        ("ABILITY_OBLIVIOUS", "Oblivious"),
        ("ABILITY_CLOUD_NINE", "Cloud Nine"),
        ("ABILITY_COMPOUND_EYES", "Compound Eyes"),
        ("ABILITY_INSOMNIA", "Insomnia"),
        ("ABILITY_COLOR_CHANGE", "Color Change"),
        ("ABILITY_IMMUNITY", "Immunity"),
        ("ABILITY_FLASH_FIRE", "Flash Fire"),
        ("ABILITY_SHIELD_DUST", "Shield Dust"),
        ("ABILITY_OWN_TEMPO", "Own Tempo"),
        ("ABILITY_SUCTION_CUPS", "Suction Cups"),
        ("ABILITY_INTIMIDATE", "Intimidate"),
        ("ABILITY_SHADOW_TAG", "Shadow Tag"),
        ("ABILITY_ROUGH_SKIN", "Rough Skin"),
        ("ABILITY_WONDER_GUARD", "Wonder Guard"),
        ("ABILITY_LEVITATE", "Levitate"),
        ("ABILITY_EFFECT_SPORE", "Effect Spore"),
        ("ABILITY_SYNCHRONIZE", "Synchronize"),
        ("ABILITY_CLEAR_BODY", "Clear Body"),
        ("ABILITY_NATURAL_CURE", "Natural Cure"),
        ("ABILITY_LIGHTNING_ROD", "Lightning Rod"),
        ("ABILITY_SERENE_GRACE", "Serene Grace"),
        ("ABILITY_SWIFT_SWIM", "Swift Swim"),
        ("ABILITY_CHLOROPHYLL", "Chlorophyll"),
        ("ABILITY_ILLUMINATE", "Illuminate"),
        ("ABILITY_TRACE", "Trace"),
        ("ABILITY_HUGE_POWER", "Huge Power"),
        ("ABILITY_POISON_POINT", "Poison Point"),
        ("ABILITY_INNER_FOCUS", "Inner Focus"),
        ("ABILITY_MAGMA_ARMOR", "Magma Armor"),
        ("ABILITY_WATER_VEIL", "Water Veil"),
        ("ABILITY_MAGNET_PULL", "Magnet Pull"),
        ("ABILITY_SOUNDPROOF", "Soundproof"),
        ("ABILITY_RAIN_DISH", "Rain Dish"),
        ("ABILITY_SAND_STREAM", "Sand Stream"),
        ("ABILITY_PRESSURE", "Pressure"),
        ("ABILITY_THICK_FAT", "Thick Fat"),
        ("ABILITY_EARLY_BIRD", "Early Bird"),
        ("ABILITY_FLAME_BODY", "Flame Body"),
        ("ABILITY_RUN_AWAY", "Run Away"),
        ("ABILITY_KEEN_EYE", "Keen Eye"),
        ("ABILITY_HYPER_CUTTER", "Hyper Cutter"),
        ("ABILITY_PICKUP", "Pickup"),
        ("ABILITY_TRUANT", "Truant"),
        ("ABILITY_HUSTLE", "Hustle"),
        ("ABILITY_CUTE_CHARM", "Cute Charm"),
        ("ABILITY_PLUS", "Plus"),
        ("ABILITY_MINUS", "Minus"),
        ("ABILITY_FORECAST", "Forecast"),
        ("ABILITY_STICKY_HOLD", "Sticky Hold"),
        ("ABILITY_SHED_SKIN", "Shed Skin"),
        ("ABILITY_GUTS", "Guts"),
        ("ABILITY_MARVEL_SCALE", "Marvel Scale"),
        ("ABILITY_LIQUID_OOZE", "Liquid Ooze"),
        ("ABILITY_OVERGROW", "Overgrow"),
        ("ABILITY_BLAZE", "Blaze"),
        ("ABILITY_TORRENT", "Torrent"),
        ("ABILITY_SWARM", "Swarm"),
        ("ABILITY_ROCK_HEAD", "Rock Head"),
        ("ABILITY_DROUGHT", "Drought"),
        ("ABILITY_ARENA_TRAP", "Arena Trap"),
        ("ABILITY_VITAL_SPIRIT", "Vital Spirit"),
        ("ABILITY_WHITE_SMOKE", "White Smoke"),
        ("ABILITY_PURE_POWER", "Pure Power"),
        ("ABILITY_SHELL_ARMOR", "Shell Armor"),
        ("ABILITY_CACOPHONY", "Cacophony"),
        ("ABILITY_AIR_LOCK", "Air Lock")
    ]]

    # Create warp map
    for warp, destination in extracted_data["warps"].items():
        data.warp_map[warp] = None if destination == "" else destination

        if encoded_warp not in data.warp_map:
            data.warp_map[encoded_warp] = None

    # Create trainer data
    for i, trainer_json in enumerate(extracted_data["trainers"]):
        party_json = trainer_json["party"]
        pokemon_data_type = _str_to_pokemon_data_type(trainer_json["data_type"])
        data.trainers.append(TrainerData(
            i,
            TrainerPartyData(
                [TrainerPokemonData(
                    p["species"],
                    p["level"],
                    (p["moves"][0], p["moves"][1], p["moves"][2], p["moves"][3]) if "moves" in p else None
                ) for p in party_json],
                pokemon_data_type,
                trainer_json["party_address"]
            ),
            trainer_json["address"],
            trainer_json["script_address"]
        ))


_init()
