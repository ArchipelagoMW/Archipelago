"""
Pulls data from JSON files in worlds/pokemon_frlg/data/ into classes.
This also includes marrying automatically extracted data with manually
defined data (like location names or usable Pokémon species), some cleanup
and sorting, and Warp methods.
"""
import orjson
import pkgutil
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum, IntEnum
from pkg_resources import resource_listdir, resource_isdir
from typing import Dict, List, NamedTuple, Set, FrozenSet, Any, Tuple
from BaseClasses import ItemClassification

APWORLD_VERSION = "1.0.2"
POPTRACKER_CHECKSUM = 0x4A497E8F
NUM_REAL_SPECIES = 386

@dataclass
class GameOption:
    default: int
    options: Dict[str | int | bool, int]
    option_group: int
    option_number: int

GAME_OPTIONS: Dict[str, GameOption] = {
    "Text Speed": GameOption(3, {"Slow": 0, "Mid": 1, "Fast": 2, "Instant": 3}, 1, 0),
    "Turbo Button": GameOption(0, {"Off": 0, False: 0, "A": 1, "B": 2, "A/B": 3}, 1, 2),
    "Auto Run": GameOption(0, {"Off": 0, False: 0, "On": 1, True: 1}, 1, 4),
    "Button Mode": GameOption(0, {"Help": 0, "L/R": 1, "L=A": 2}, 1, 5),
    "Frame": GameOption(0, dict(zip(range(1, 11), range(10))), -1, 0),
    "Battle Scene": GameOption(1, {"Off": 0, False: 0, "On": 1, True: 1}, 1, 7),
    "Battle Style": GameOption(0, {"Shift": 0, "Set": 1}, 1, 8),
    "Show Effectiveness": GameOption(1, {"Off": 0, False: 0, "On": 1, True: 1}, 1, 9),
    "Experience Multiplier": GameOption(100, dict(zip([i * 10 for i in range(101)], [i * 10 for i in range(101)])), -2, 0),
    "Experience Distribution": GameOption(0, {"Gen III": 0, "Gen VI": 1, "Gen VIII": 2}, 1, 10),
    "Sound": GameOption(0, {"Mono": 0, "Stereo": 1}, 1, 12),
    "Low HP Beep": GameOption(1, {"Off": 0, False: 0, "On": 1, True: 1}, 1, 13),
    "Skip Fanfares": GameOption(0, {"Off": 0, False: 0, "On": 1, True: 1}, 1, 14),
    "Bike Music": GameOption(1, {"Off": 0, False: 0, "On": 1, True: 1}, 1, 15),
    "Surf Music": GameOption(1, {"Off": 0, False: 0, "On": 1, True: 1}, 2, 0),
    "Guaranteed Catch": GameOption(0, {"Off": 0, False: 0, "On": 1, True: 1}, 2, 1),
    "Guaranteed Run": GameOption(0, {"Off": 0, False: 0, "On": 1, True: 1}, 2, 2),
    "Encounter Rates": GameOption(0, {"Vanilla": 0, "Normalized": 1}, 2, 3),
    "Blind Trainers": GameOption(0, {"Off": 0, False: 0, "On": 1, True: 1}, 2, 4),
    "Skip Nicknames": GameOption(0, {"Off": 0, False: 0, "On": 1, True: 1}, 2, 5),
    "Item Messages": GameOption(1, {"All": 0, "Progression": 1, "None": 2}, 2, 6)
}

class Warp:
    """
    Represents warp events in the game like doorways or warp pads
    """
    is_one_way: bool
    source_map: str
    source_ids: List[int]
    dest_map: str
    dest_ids: List[int]
    name: str | None
    parent_region_id: str | None

    def __init__(self,
                 encoded_string: str | None = None,
                 name: str | None = None,
                 parent_region_id: str | None = None) -> None:
        if encoded_string is not None:
            decoded_warp = Warp.decode(encoded_string)
            self.is_one_way = decoded_warp.is_one_way
            self.source_map = decoded_warp.source_map
            self.source_ids = decoded_warp.source_ids
            self.dest_map = decoded_warp.dest_map
            self.dest_ids = decoded_warp.dest_ids
        self.name = name
        self.parent_region_id = parent_region_id

    def connects_to(self, other: "Warp") -> bool:
        """
        Returns true if this warp sends the player to `other`
        """
        return self.dest_map == other.source_map and set(self.dest_ids) <= set(other.source_ids)

    @staticmethod
    def decode(encoded_string: str) -> "Warp":
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
    name: str
    item_id: int
    price: int
    classification: ItemClassification
    tags: FrozenSet[str]


class LocationCategory(IntEnum):
    OVERWORLD_ITEM = 0
    NPC_GIFT = 1
    HIDDEN_ITEM = 2
    TOWN_VISIT = 3
    SHOP_ITEM = 4
    TRAINER = 5
    TRAINER_REMATCH = 6
    FAME_ENTRY = 7
    POKEDEX = 8
    EVENT = 9
    EVENT_WILD_POKEMON = 10
    EVENT_STATIC_POKEMON = 11
    EVENT_LEGENDARY_POKEMON = 12
    EVENT_EVOLUTION_POKEMON = 13
    EVENT_TRAINER_SCALING = 14
    EVENT_WILD_POKEMON_SCALING = 15
    EVENT_STATIC_POKEMON_SCALING = 16


class LocationData(NamedTuple):
    id: str
    name: str
    parent_region_id: str
    default_item: int
    address: Dict[str, int | List[int]]
    flag: int
    category: LocationCategory
    include: FrozenSet[str]
    tags: FrozenSet[str]


@dataclass
class EncounterSpeciesData:
    species_id: int
    min_level: int
    max_level: int


class EncounterTableData(NamedTuple):
    slots: Dict[str, List[EncounterSpeciesData]]
    address: Dict[str, int]


class EncounterType(Enum):
    LAND = "Land"
    WATER = "Water"
    FISHING = "Fishing"


@dataclass
class MapData:
    name: str
    header_address: Dict[str, int]
    warp_table_address: Dict[str, int]
    encounters: Dict[EncounterType, EncounterTableData]
    kanto: bool


class EventData(NamedTuple):
    id: str
    name: str | List[str]
    item: str | List[str]
    parent_region_id: str
    category: LocationCategory


class RegionData:
    id: str
    name: str
    parent_map: MapData | None
    encounter_region: str
    has_land: bool
    has_water: bool
    has_fishing: bool
    kanto: bool
    exits: Dict[str, str | List[str]]
    warps: List[str]
    locations: List[str]
    events: List[str]

    def __init__(self, region_id: str, name: str, parent_map: MapData | None, encounter_region: str,
                 has_land: bool, has_water: bool, has_fishing: bool, kanto: bool):
        self.id = region_id
        self.name = name
        self.parent_map = parent_map
        self.encounter_region = encounter_region
        self.has_land = has_land
        self.has_water = has_water
        self.has_fishing = has_fishing
        self.kanto = kanto
        self.exits = {}
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
    ITEM_HELD = 9
    FRIENDSHIP = 10


class EvolutionData(NamedTuple):
    param: int
    param2: int
    species_id: int
    method: EvolutionMethodEnum


@dataclass
class SpeciesData:
    species_id_name: str
    name: str
    species_id: int
    national_dex_number: int
    base_stats: BaseStats
    types: Tuple[int, int]
    abilities: Tuple[int, int]
    evolutions: List[EvolutionData]
    pre_evolution: int | None
    catch_rate: int
    friendship: int
    learnset: List[LearnsetMove]
    tm_hm_compatibility: int
    learnset_address: Dict[str, int]
    address: Dict[str, int]


@dataclass
class StarterData:
    species_id: int
    address: Dict[str, int]


@dataclass
class MiscPokemonData:
    species_id: Dict[str, int]
    level: Dict[str, int]
    address: Dict[str, int]
    level_address: Dict[str, int]


@dataclass
class TradePokemonData:
    species_id: Dict[str, int]
    species_address: Dict[str, int]
    requested_species_id: Dict[str, int]
    requested_species_address: Dict[str, int]


class TrainerPokemonDataTypeEnum(IntEnum):
    NO_ITEM_DEFAULT_MOVES = 0
    NO_ITEM_CUSTOM_MOVES = 1
    ITEM_DEFAULT_MOVES = 2
    ITEM_CUSTOM_MOVES = 3


POKEMON_DATA_TYPE: Dict[str, TrainerPokemonDataTypeEnum] = {
    "NO_ITEM_DEFAULT_MOVES": TrainerPokemonDataTypeEnum.NO_ITEM_DEFAULT_MOVES,
    "NO_ITEM_CUSTOM_MOVES": TrainerPokemonDataTypeEnum.NO_ITEM_CUSTOM_MOVES,
    "ITEM_DEFAULT_MOVES": TrainerPokemonDataTypeEnum.ITEM_DEFAULT_MOVES,
    "ITEM_CUSTOM_MOVES": TrainerPokemonDataTypeEnum.ITEM_CUSTOM_MOVES
}


@dataclass
class TrainerPokemonData:
    species_id: int
    level: int
    moves: Tuple[int, int, int, int] | None
    locked: bool


@dataclass
class TrainerPartyData:
    pokemon: List[TrainerPokemonData]
    pokemon_data_type: TrainerPokemonDataTypeEnum
    base_level: int
    address: Dict[str, int]


@dataclass
class TrainerData:
    party: TrainerPartyData
    address: Dict[str, int]


@dataclass
class MoveData:
    effect: int
    power: int
    type: int
    accuracy: int
    pp: int
    secondary_effect_chance: int
    target: int
    priority: int
    flags: int
    category: int
    address: Dict[str, int]


@dataclass
class ScalingData:
    region: str
    kanto: bool
    connections: List[str]
    type: EncounterType | None
    category: LocationCategory
    locations: Dict[str, List[str]]


@dataclass
class FlyData:
    name: str
    display_name: str
    map: str
    region: str
    map_group: int
    map_num: int
    x_pos: int
    y_pos: int
    region_map_id: int
    region_map_index: int


class PokemonFRLGData:
    rom_names: Dict[str, str]
    rom_checksum: int
    constants: Dict[str, int]
    ram_addresses: Dict[str, Dict[str, int]]
    rom_addresses: Dict[str, Dict[str, int]]
    regions: Dict[str, RegionData]
    locations: Dict[str, LocationData]
    events: Dict[str, EventData]
    items: Dict[int, ItemData]
    maps: Dict[str, MapData]
    warps: Dict[str, Warp]
    warp_map: Dict[str, str | None]
    warp_name_map: Dict[str, str]
    entrance_name_map: Dict[int, Dict[int, str]]
    species: Dict[int, SpeciesData]
    evolutions: Dict[str, EvolutionData]
    starters: Dict[str, StarterData]
    legendary_pokemon: Dict[str, MiscPokemonData]
    misc_pokemon: Dict[str, MiscPokemonData]
    trade_pokemon: Dict[str, TradePokemonData]
    trainers: Dict[str, TrainerData]
    tmhm_moves: List[int]
    moves: Dict[str, MoveData]
    scaling: Dict[str, ScalingData]
    type_damage_categories: List[int]
    num_moves_per_damage_category: Dict[int, int]

    def __init__(self) -> None:
        self.constants = {}
        self.ram_addresses = {}
        self.rom_addresses = {}
        self.regions = {}
        self.locations = {}
        self.events = {}
        self.items = {}
        self.maps = {}
        self.warps = {}
        self.warp_map = {}
        self.warp_name_map = {}
        self.entrance_name_map = {}
        self.species = {}
        self.evolutions = {}
        self.starters = {}
        self.legendary_pokemon = {}
        self.misc_pokemon = {}
        self.trade_pokemon = {}
        self.trainers = {}
        self.tmhm_moves = []
        self.moves = {}
        self.scaling = {}
        self.type_damage_categories = []
        self.num_moves_per_damage_category = defaultdict(lambda: 0)


# Excludes extras like copies of Unown and special species values like SPECIES_EGG
ALL_SPECIES: List[Tuple[str, str, int]] = [
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
    ("SPECIES_NIDORAN_F", "Nidoran F", 29),
    ("SPECIES_NIDORINA", "Nidorina", 30),
    ("SPECIES_NIDOQUEEN", "Nidoqueen", 31),
    ("SPECIES_NIDORAN_M", "Nidoran M", 32),
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
    ("SPECIES_BAYLEEF", "Bayleef", 153),
    ("SPECIES_MEGANIUM", "Meganium", 154),
    ("SPECIES_CYNDAQUIL", "Cyndaquil", 155),
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
    ("SPECIES_FLAAFFY", "Flaaffy", 180),
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
    ("SPECIES_HO_OH", "Ho-Oh", 250),
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
    ("SPECIES_LINOONE", "Linoone", 264),
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


def load_json_data(data_name: str) -> List[Any] | Dict[str, Any]:
    return orjson.loads(pkgutil.get_data(__name__, "data/" + data_name).decode("utf-8-sig"))


def init() -> None:
    extracted_data: Dict[str, Any] = load_json_data("extracted_data.json")
    data.rom_names = extracted_data["rom_names"]
    data.rom_checksum = extracted_data["rom_checksum"]
    data.constants = extracted_data["constants"]
    data.ram_addresses = extracted_data["misc_ram_addresses"]
    data.rom_addresses = extracted_data["misc_rom_addresses"]

    location_data = load_json_data("locations.json")
    event_data = load_json_data("events.json")
    item_data = load_json_data("items.json")

    # Create map data
    for map_name, map_json in extracted_data["maps"].items():
        encounter_tables: Dict[EncounterType, EncounterTableData] = {}
        if "land_encounters" in map_json:
            land_slots: Dict[str, List[EncounterSpeciesData]] = {}
            for version, slots in map_json["land_encounters"]["slots"].items():
                version_slots: List[EncounterSpeciesData] = []
                for slot_data in slots:
                    version_slots.append(EncounterSpeciesData(
                        slot_data["default_species"],
                        slot_data["min_level"],
                        slot_data["max_level"]
                    ))
                land_slots[version] = version_slots
            encounter_tables[EncounterType.LAND] = EncounterTableData(
                land_slots,
                map_json["land_encounters"]["address"]
            )
        if "water_encounters" in map_json:
            water_slots: Dict[str, List[EncounterSpeciesData]] = {}
            for version, slots in map_json["water_encounters"]["slots"].items():
                version_slots: List[EncounterSpeciesData] = []
                for slot_data in slots:
                    version_slots.append(EncounterSpeciesData(
                        slot_data["default_species"],
                        slot_data["min_level"],
                        slot_data["max_level"]
                    ))
                water_slots[version] = version_slots
            encounter_tables[EncounterType.WATER] = EncounterTableData(
                water_slots,
                map_json["water_encounters"]["address"]
            )
        if "fishing_encounters" in map_json:
            fishing_slots: Dict[str, List[EncounterSpeciesData]] = {}
            for version, slots in map_json["fishing_encounters"]["slots"].items():
                version_slots: List[EncounterSpeciesData] = []
                for slot_data in slots:
                    version_slots.append(EncounterSpeciesData(
                        slot_data["default_species"],
                        slot_data["min_level"],
                        slot_data["max_level"]
                    ))
                fishing_slots[version] = version_slots
            encounter_tables[EncounterType.FISHING] = EncounterTableData(
                fishing_slots,
                map_json["fishing_encounters"]["address"]
            )

        data.maps[map_name] = MapData(
            map_name,
            map_json["header_address"],
            map_json["warp_table_address"],
            encounter_tables,
            True
        )

    # Load/merge region json files
    region_json_list = []
    for file in resource_listdir(__name__, "data/regions"):
        if not resource_isdir(__name__, "data/regions/" + file):
            region_json_list.append(load_json_data("regions/" + file))

    regions_json = {}
    for region_subset in region_json_list:
        for region_id, region_json in region_subset.items():
            if region_id in regions_json:
                raise AssertionError(f"Pokemon FRLG: Region [{region_id}] was defined multiple times")
            regions_json[region_id] = region_json

    # Create region data
    claimed_locations: Set[str] = set()
    claimed_warps: Set[str] = set()

    for region_id, region_json in regions_json.items():
        parent_map = data.maps[region_json["parent_map"]] if region_json["parent_map"] is not None else None

        if parent_map is not None:
            parent_map.kanto = region_json["kanto"]

        new_region = RegionData(
            region_id,
            region_json["name"],
            parent_map,
            region_json["encounter_region"],
            region_json["has_land"],
            region_json["has_water"],
            region_json["has_fishing"],
            region_json["kanto"]
        )

        # Locations
        for location_id in region_json["locations"]:
            if location_id in claimed_locations:
                raise AssertionError(f"Pokemon FRLG: Location [{location_id}] was claimed by multiple regions")

            location_json = extracted_data["locations"][location_id]

            if "BULBASAUR_REWARD" in location_id:
                import re
                trainer = re.match("TRAINER_([A-Z0-9_]+)_BULBASAUR_REWARD", location_id).group(1)
                alternate_rival_jsons = [extracted_data["locations"][alternate] for alternate in [
                    f"TRAINER_{trainer}_CHARMANDER_REWARD",
                    f"TRAINER_{trainer}_SQUIRTLE_REWARD"
                ]]

                location_address: Dict[str, List[int]] = dict()

                for game_version_revision in location_json["address"].keys():
                    location_address[game_version_revision] = [location_json["address"][game_version_revision]]

                for game_version_revision in location_address.keys():
                    for alternate_rival_json in alternate_rival_jsons:
                        location_address[game_version_revision].append(
                            alternate_rival_json["address"][game_version_revision])

                new_location = LocationData(
                    location_id,
                    location_data[location_id]["name"],
                    region_id,
                    location_json["default_item"],
                    location_address,
                    location_json["flag"],
                    LocationCategory[location_data[location_id]["category"]],
                    frozenset(location_data[location_id]["include"]),
                    frozenset(location_data[location_id]["tags"])
                )
            else:
                new_location = LocationData(
                    location_id,
                    location_data[location_id]["name"],
                    region_id,
                    location_json["default_item"],
                    location_json["address"],
                    location_json["flag"],
                    LocationCategory[location_data[location_id]["category"]],
                    frozenset(location_data[location_id]["include"]),
                    frozenset(location_data[location_id]["tags"])
                )

            new_region.locations.append(location_id)
            data.locations[location_id] = new_location
            claimed_locations.add(location_id)

        # Events
        for event_id in region_json["events"]:
            new_event = EventData(
                event_id,
                event_data[event_id]["name"],
                event_data[event_id]["item"],
                region_id,
                LocationCategory[event_data[event_id]["category"]]
            )
            new_region.events.append(event_id)
            data.events[event_id] = new_event

        # Exits
        new_region.exits = region_json["exits"]

        # Warps
        for encoded_warp, name in region_json["warps"].items():
            if encoded_warp in claimed_warps:
                raise AssertionError(f"Pokemon FRLG: Warp [{encoded_warp}] was claimed by multiple regions")
            new_region.warps.append(encoded_warp)
            data.warps[encoded_warp] = Warp(encoded_warp, name, region_id)
            claimed_warps.add(encoded_warp)
            if name != "":
                map_id = data.constants[data.warps[encoded_warp].source_map]
                if map_id not in data.entrance_name_map:
                    data.entrance_name_map[map_id] = {}
                for warp_id in data.warps[encoded_warp].source_ids:
                    data.entrance_name_map[map_id][warp_id] = name
                data.warp_name_map[name] = encoded_warp

        data.regions[region_id] = new_region

    # Create item data
    for item_id_name, attributes in item_data.items():
        if attributes["classification"] == "PROGRESSION":
            item_classification = ItemClassification.progression
        elif attributes["classification"] == "USEFUL":
            item_classification = ItemClassification.useful
        elif attributes["classification"] == "FILLER":
            item_classification = ItemClassification.filler
        elif attributes["classification"] == "TRAP":
            item_classification = ItemClassification.trap
        else:
            raise ValueError(f"Unknown classification {attributes['classification']} for item {item_id_name}")

        data.items[data.constants[item_id_name]] = ItemData(
            attributes["name"],
            data.constants[item_id_name],
            extracted_data["item_prices"][item_id_name],
            item_classification,
            frozenset(attributes["tags"])
        )

    # Create warp map
    for warp, destination in extracted_data["warps"].items():
        data.warp_map[warp] = None if destination == "" else destination

    # Create species data
    max_species_id = 0
    for species_id_name, species_name, species_dex_number in ALL_SPECIES:
        species_id = data.constants[species_id_name]
        max_species_id = max(species_id, max_species_id)
        species_data = extracted_data["species"][species_id]
        num_evolutions = len(species_data["evolutions"])
        evolution_index = 1

        learnset = [LearnsetMove(item["level"], item["move_id"]) for item in species_data["learnset"]["moves"]]

        data.species[species_id] = SpeciesData(
            species_id_name,
            species_name,
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
                evolution_data["param"],
                evolution_data["param2"],
                evolution_data["species"],
                EvolutionMethodEnum[evolution_data["method"]]
            ) for evolution_data in species_data["evolutions"]],
            None,
            species_data["catch_rate"],
            species_data["friendship"],
            learnset,
            int(species_data["tmhm_learnset"], 16),
            species_data["learnset"]["address"],
            species_data["address"]
        )

        for evolution_data in data.species[species_id].evolutions:
            if num_evolutions > 1:
                data.evolutions[f"{species_name} {evolution_index}"] = EvolutionData(
                    evolution_data.param,
                    evolution_data.param2,
                    evolution_data.species_id,
                    evolution_data.method
                )
                evolution_index += 1
            else:
                data.evolutions[species_name] = EvolutionData(
                    evolution_data.param,
                    evolution_data.param2,
                    evolution_data.species_id,
                    evolution_data.method
                )

    for species in data.species.values():
        for evolution in species.evolutions:
            data.species[evolution.species_id].pre_evolution = species.species_id

    # Create starter data
    for name, starter_data in extracted_data["starter_pokemon"].items():
        data.starters[name] = StarterData(
            starter_data["species"],
            starter_data["address"]
        )

    # Create legendary Pokémon data
    for name, legendary_data in extracted_data["legendary_pokemon"].items():
        data.legendary_pokemon[name] = MiscPokemonData(
            legendary_data["species"],
            legendary_data["level"],
            legendary_data["address"],
            legendary_data["level_address"]
        )

    # Create misc Pokémon data
    for name, misc_data in extracted_data["misc_pokemon"].items():
        data.misc_pokemon[name] = MiscPokemonData(
            misc_data["species"],
            misc_data["level"],
            misc_data["address"],
            misc_data["level_address"]
        )

    # Create trade Pokémon data
    for name, trade_pokemon in extracted_data["trade_pokemon"].items():
        data.trade_pokemon[name] = TradePokemonData(
            trade_pokemon["species"],
            trade_pokemon["species_address"],
            trade_pokemon["requested_species"],
            trade_pokemon["requested_species_address"]
        )

    # Create trainer data
    for name, trainer_data in extracted_data["trainers"].items():
        party_data = trainer_data["party"]
        data.trainers[name] = TrainerData(
            TrainerPartyData([
                TrainerPokemonData(
                    pokemon["species"],
                    pokemon["level"],
                    (pokemon["moves"][0],
                     pokemon["moves"][1],
                     pokemon["moves"][2],
                     pokemon["moves"][3]) if "moves" in pokemon else None,
                    False
                ) for pokemon in party_data],
                POKEMON_DATA_TYPE[trainer_data["data_type"]],
                trainer_data["base_level"],
                trainer_data["party_address"]
            ),
            trainer_data["address"]
        )

    # TM/HM Moves
    data.tmhm_moves = extracted_data["tmhm_moves"]

    # Type damage categories
    data.type_damage_categories = extracted_data["damage_type_table"]

    # Create move data
    for name, move_data in extracted_data["moves"].items():
        data.moves[name] = MoveData(
            move_data["effect"],
            move_data["power"],
            move_data["type"],
            move_data["accuracy"],
            move_data["pp"],
            move_data["secondary_effect_chance"],
            move_data["target"],
            move_data["priority"],
            move_data["flags"],
            move_data["category"],
            move_data["address"]
        )
        if name not in ["MOVE_NONE", "MOVE_STRUGGLE"]:
            data.num_moves_per_damage_category[move_data["category"]] += 1

    # Load/merge scaling json files
    scaling_json_list = []
    for file in resource_listdir(__name__, "data/scalings"):
        if not resource_isdir(__name__, "data/scalings/" + file):
            scaling_json_list.append(load_json_data("scalings/" + file))

    scalings_json = {}
    for scaling_subset in scaling_json_list:
        for scaling_id, scaling_json in scaling_subset.items():
            if scaling_id in scalings_json:
                raise AssertionError(f"Pokemon FRLG: Scaling [{scaling_id}] was defined multiple times")
            scalings_json[scaling_id] = scaling_json

    for scaling_id, scaling_json in scalings_json.items():
        scaling_data = ScalingData(
            scaling_json["region"],
            scaling_json["kanto"],
            scaling_json["connections"],
            EncounterType[scaling_json["type"]] if "type" in scaling_json else None,
            LocationCategory[scaling_json["category"]],
            scaling_json["locations"]
        )

        data.scaling[scaling_id] = scaling_data


data = PokemonFRLGData()
init()

LEGENDARY_POKEMON = frozenset([data.constants[species] for species in [
    "SPECIES_ARTICUNO",
    "SPECIES_ZAPDOS",
    "SPECIES_MOLTRES",
    "SPECIES_MEWTWO",
    "SPECIES_MEW",
    "SPECIES_RAIKOU",
    "SPECIES_ENTEI",
    "SPECIES_SUICUNE",
    "SPECIES_LUGIA",
    "SPECIES_HO_OH",
    "SPECIES_CELEBI",
    "SPECIES_REGIROCK",
    "SPECIES_REGICE",
    "SPECIES_REGISTEEL",
    "SPECIES_LATIAS",
    "SPECIES_LATIOS",
    "SPECIES_KYOGRE",
    "SPECIES_GROUDON",
    "SPECIES_RAYQUAZA",
    "SPECIES_JIRACHI",
    "SPECIES_DEOXYS",
]])

fly_blacklist_map = {
    "Pallet Town": "ITEM_FLY_PALLET",
    "Viridian City": "ITEM_FLY_VIRIDIAN",
    "Pewter City": "ITEM_FLY_PEWTER",
    "Cerulean City": "ITEM_FLY_CERULEAN",
    "Lavender Town": "ITEM_FLY_LAVENDER",
    "Vermilion City": "ITEM_FLY_VERMILION",
    "Celadon City": "ITEM_FLY_CELADON",
    "Fuchsia City": "ITEM_FLY_FUCHSIA",
    "Cinnabar Island": "ITEM_FLY_CINNABAR",
    "Indigo Plateau": "ITEM_FLY_INDIGO",
    "Saffron City": "ITEM_FLY_SAFFRON",
    "One Island": "ITEM_FLY_ONE_ISLAND",
    "Two Island": "ITEM_FLY_TWO_ISLAND",
    "Three Island": "ITEM_FLY_THREE_ISLAND",
    "Four Island": "ITEM_FLY_FOUR_ISLAND",
    "Five Island": "ITEM_FLY_FIVE_ISLAND",
    "Six Island": "ITEM_FLY_SIX_ISLAND",
    "Seven Island": "ITEM_FLY_SEVEN_ISLAND",
    "Route 4": "ITEM_FLY_ROUTE4",
    "Route 10": "ITEM_FLY_ROUTE10"
}

starting_town_blacklist_map = {
    "Pallet Town": "SPAWN_PALLET_TOWN",
    "Viridian City": "SPAWN_VIRIDIAN_CITY",
    "Pewter City": "SPAWN_PEWTER_CITY",
    "Cerulean City": "SPAWN_CERULEAN_CITY",
    "Lavender Town": "SPAWN_LAVENDER_TOWN",
    "Vermilion City": "SPAWN_VERMILION_CITY",
    "Celadon City": "SPAWN_CELADON_CITY",
    "Fuchsia City": "SPAWN_FUCHSIA_CITY",
    "Cinnabar Island": "SPAWN_CINNABAR_ISLAND",
    "Saffron City": "SPAWN_SAFFRON_CITY",
    "Route 4": "SPAWN_ROUTE4",
    "Route 10": "SPAWN_ROUTE10",
    "One Island": "SPAWN_ONE_ISLAND",
    "Two Island": "SPAWN_TWO_ISLAND",
    "Three Island": "SPAWN_THREE_ISLAND",
    "Four Island": "SPAWN_FOUR_ISLAND",
    "Five Island": "SPAWN_FIVE_ISLAND",
    "Seven Island": "SPAWN_SEVEN_ISLAND",
    "Six Island": "SPAWN_SIX_ISLAND"
}

ability_name_map = {j: data.constants[i] for i, j in [
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
    ("ABILITY_COMPOUND_EYES", "Compoundeyes"),
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
    ("ABILITY_LIGHTNING_ROD", "Lightningrod"),
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
]}

move_name_map = {j: data.constants[i] for i, j in [
    ("MOVE_POUND", "Pound"),
    ("MOVE_KARATE_CHOP", "Karate Chop"),
    ("MOVE_DOUBLE_SLAP", "Doubleslap"),
    ("MOVE_COMET_PUNCH", "Comet Punch"),
    ("MOVE_MEGA_PUNCH", "Mega Punch"),
    ("MOVE_PAY_DAY", "Pay Day"),
    ("MOVE_FIRE_PUNCH", "Fire Punch"),
    ("MOVE_ICE_PUNCH", "Ice Punch"),
    ("MOVE_THUNDER_PUNCH", "Thunderpunch"),
    ("MOVE_SCRATCH", "Scratch"),
    ("MOVE_VICE_GRIP", "Vicegrip"),
    ("MOVE_GUILLOTINE", "Guillotine"),
    ("MOVE_RAZOR_WIND", "Razor Wind"),
    ("MOVE_SWORDS_DANCE", "Swords Dance"),
    ("MOVE_CUT", "Cut"),
    ("MOVE_GUST", "Gust"),
    ("MOVE_WING_ATTACK", "Wing Attack"),
    ("MOVE_WHIRLWIND", "Whirlwind"),
    ("MOVE_FLY", "Fly"),
    ("MOVE_BIND", "Bind"),
    ("MOVE_SLAM", "Slam"),
    ("MOVE_VINE_WHIP", "Vine Whip"),
    ("MOVE_STOMP", "Stomp"),
    ("MOVE_DOUBLE_KICK", "Double Kick"),
    ("MOVE_MEGA_KICK", "Mega Kick"),
    ("MOVE_JUMP_KICK", "Jump Kick"),
    ("MOVE_ROLLING_KICK", "Rolling Kick"),
    ("MOVE_SAND_ATTACK", "Sand-Attack"),
    ("MOVE_HEADBUTT", "Headbutt"),
    ("MOVE_HORN_ATTACK", "Horn Attack"),
    ("MOVE_FURY_ATTACK", "Fury Attack"),
    ("MOVE_HORN_DRILL", "Horn Drill"),
    ("MOVE_TACKLE", "Tackle"),
    ("MOVE_BODY_SLAM", "Body Slam"),
    ("MOVE_WRAP", "Wrap"),
    ("MOVE_TAKE_DOWN", "Take Down"),
    ("MOVE_THRASH", "Thrash"),
    ("MOVE_DOUBLE_EDGE", "Double-Edge"),
    ("MOVE_TAIL_WHIP", "Tail Whip"),
    ("MOVE_POISON_STING", "Poison Sting"),
    ("MOVE_TWINEEDLE", "Twineedle"),
    ("MOVE_PIN_MISSILE", "Pin Missile"),
    ("MOVE_LEER", "Leer"),
    ("MOVE_BITE", "Bite"),
    ("MOVE_GROWL", "Growl"),
    ("MOVE_ROAR", "Roar"),
    ("MOVE_SING", "Sing"),
    ("MOVE_SUPERSONIC", "Supersonic"),
    ("MOVE_SONIC_BOOM", "Sonicboom"),
    ("MOVE_DISABLE", "Disable"),
    ("MOVE_ACID", "Acid"),
    ("MOVE_EMBER", "Ember"),
    ("MOVE_FLAMETHROWER", "Flamethrower"),
    ("MOVE_MIST", "Mist"),
    ("MOVE_WATER_GUN", "Water Gun"),
    ("MOVE_HYDRO_PUMP", "Hydro Pump"),
    ("MOVE_SURF", "Surf"),
    ("MOVE_ICE_BEAM", "Ice Beam"),
    ("MOVE_BLIZZARD", "Blizzard"),
    ("MOVE_PSYBEAM", "Psybeam"),
    ("MOVE_BUBBLE_BEAM", "Bubblebeam"),
    ("MOVE_AURORA_BEAM", "Aurora Beam"),
    ("MOVE_HYPER_BEAM", "Hyper Beam"),
    ("MOVE_PECK", "Peck"),
    ("MOVE_DRILL_PECK", "Drill Peck"),
    ("MOVE_SUBMISSION", "Submission"),
    ("MOVE_LOW_KICK", "Low Kick"),
    ("MOVE_COUNTER", "Counter"),
    ("MOVE_SEISMIC_TOSS", "Seismic Toss"),
    ("MOVE_STRENGTH", "Strength"),
    ("MOVE_ABSORB", "Absorb"),
    ("MOVE_MEGA_DRAIN", "Mega Drain"),
    ("MOVE_LEECH_SEED", "Leech Seed"),
    ("MOVE_GROWTH", "Growth"),
    ("MOVE_RAZOR_LEAF", "Razor Leaf"),
    ("MOVE_SOLAR_BEAM", "Solarbeam"),
    ("MOVE_POISON_POWDER", "Poisonpowder"),
    ("MOVE_STUN_SPORE", "Stun Spore"),
    ("MOVE_SLEEP_POWDER", "Sleep Powder"),
    ("MOVE_PETAL_DANCE", "Petal Dance"),
    ("MOVE_STRING_SHOT", "String Shot"),
    ("MOVE_DRAGON_RAGE", "Dragon Rage"),
    ("MOVE_FIRE_SPIN", "Fire Spin"),
    ("MOVE_THUNDER_SHOCK", "Thundershock"),
    ("MOVE_THUNDERBOLT", "Thunderbolt"),
    ("MOVE_THUNDER_WAVE", "Thunder Wave"),
    ("MOVE_THUNDER", "Thunder"),
    ("MOVE_ROCK_THROW", "Rock Throw"),
    ("MOVE_EARTHQUAKE", "Earthquake"),
    ("MOVE_FISSURE", "Fissure"),
    ("MOVE_DIG", "Dig"),
    ("MOVE_TOXIC", "Toxic"),
    ("MOVE_CONFUSION", "Confusion"),
    ("MOVE_PSYCHIC", "Psychic"),
    ("MOVE_HYPNOSIS", "Hypnosis"),
    ("MOVE_MEDITATE", "Meditate"),
    ("MOVE_AGILITY", "Agility"),
    ("MOVE_QUICK_ATTACK", "Quick Attack"),
    ("MOVE_RAGE", "Rage"),
    ("MOVE_TELEPORT", "Teleport"),
    ("MOVE_NIGHT_SHADE", "Night Shade"),
    ("MOVE_MIMIC", "Mimic"),
    ("MOVE_SCREECH", "Screech"),
    ("MOVE_DOUBLE_TEAM", "Double Team"),
    ("MOVE_RECOVER", "Recover"),
    ("MOVE_HARDEN", "Harden"),
    ("MOVE_MINIMIZE", "Minimize"),
    ("MOVE_SMOKESCREEN", "Smokescreen"),
    ("MOVE_CONFUSE_RAY", "Confuse Ray"),
    ("MOVE_WITHDRAW", "Withdraw"),
    ("MOVE_DEFENSE_CURL", "Defense Curl"),
    ("MOVE_BARRIER", "Barrier"),
    ("MOVE_LIGHT_SCREEN", "Light Screen"),
    ("MOVE_HAZE", "Haze"),
    ("MOVE_REFLECT", "Reflect"),
    ("MOVE_FOCUS_ENERGY", "Focus Energy"),
    ("MOVE_BIDE", "Bide"),
    ("MOVE_METRONOME", "Metronome"),
    ("MOVE_MIRROR_MOVE", "Mirror Move"),
    ("MOVE_SELF_DESTRUCT", "Selfdestruct"),
    ("MOVE_EGG_BOMB", "Egg Bomb"),
    ("MOVE_LICK", "Lick"),
    ("MOVE_SMOG", "Smog"),
    ("MOVE_SLUDGE", "Sludge"),
    ("MOVE_BONE_CLUB", "Bone Club"),
    ("MOVE_FIRE_BLAST", "Fire Blast"),
    ("MOVE_WATERFALL", "Waterfall"),
    ("MOVE_CLAMP", "Clamp"),
    ("MOVE_SWIFT", "Swift"),
    ("MOVE_SKULL_BASH", "Skull Bash"),
    ("MOVE_SPIKE_CANNON", "Spike Cannon"),
    ("MOVE_CONSTRICT", "Constrict"),
    ("MOVE_AMNESIA", "Amnesia"),
    ("MOVE_KINESIS", "Kinesis"),
    ("MOVE_SOFT_BOILED", "Softboiled"),
    ("MOVE_HI_JUMP_KICK", "Hi Jump Kick"),
    ("MOVE_GLARE", "Glare"),
    ("MOVE_DREAM_EATER", "Dream Eater"),
    ("MOVE_POISON_GAS", "Poison Gas"),
    ("MOVE_BARRAGE", "Barrage"),
    ("MOVE_LEECH_LIFE", "Leech Life"),
    ("MOVE_LOVELY_KISS", "Lovely Kiss"),
    ("MOVE_SKY_ATTACK", "Sky Attack"),
    ("MOVE_TRANSFORM", "Transform"),
    ("MOVE_BUBBLE", "Bubble"),
    ("MOVE_DIZZY_PUNCH", "Dizzy Punch"),
    ("MOVE_SPORE", "Spore"),
    ("MOVE_FLASH", "Flash"),
    ("MOVE_PSYWAVE", "Psywave"),
    ("MOVE_SPLASH", "Splash"),
    ("MOVE_ACID_ARMOR", "Acid Armor"),
    ("MOVE_CRABHAMMER", "Crabhammer"),
    ("MOVE_EXPLOSION", "Explosion"),
    ("MOVE_FURY_SWIPES", "Fury Swipes"),
    ("MOVE_BONEMERANG", "Bonemerang"),
    ("MOVE_REST", "Rest"),
    ("MOVE_ROCK_SLIDE", "Rock Slide"),
    ("MOVE_HYPER_FANG", "Hyper Fang"),
    ("MOVE_SHARPEN", "Sharpen"),
    ("MOVE_CONVERSION", "Conversion"),
    ("MOVE_TRI_ATTACK", "Tri Attack"),
    ("MOVE_SUPER_FANG", "Super Fang"),
    ("MOVE_SLASH", "Slash"),
    ("MOVE_SUBSTITUTE", "Substitute"),
    ("MOVE_SKETCH", "Sketch"),
    ("MOVE_TRIPLE_KICK", "Triple Kick"),
    ("MOVE_THIEF", "Thief"),
    ("MOVE_SPIDER_WEB", "Spider Web"),
    ("MOVE_MIND_READER", "Mind Reader"),
    ("MOVE_NIGHTMARE", "Nightmare"),
    ("MOVE_FLAME_WHEEL", "Flame Wheel"),
    ("MOVE_SNORE", "Snore"),
    ("MOVE_CURSE", "Curse"),
    ("MOVE_FLAIL", "Flail"),
    ("MOVE_CONVERSION_2", "Conversion 2"),
    ("MOVE_AEROBLAST", "Aeroblast"),
    ("MOVE_COTTON_SPORE", "Cotton Spore"),
    ("MOVE_REVERSAL", "Reversal"),
    ("MOVE_SPITE", "Spite"),
    ("MOVE_POWDER_SNOW", "Powder Snow"),
    ("MOVE_PROTECT", "Protect"),
    ("MOVE_MACH_PUNCH", "Mach Punch"),
    ("MOVE_SCARY_FACE", "Scary Face"),
    ("MOVE_FAINT_ATTACK", "Faint Attack"),
    ("MOVE_SWEET_KISS", "Sweet Kiss"),
    ("MOVE_BELLY_DRUM", "Belly Drum"),
    ("MOVE_SLUDGE_BOMB", "Sludge Bomb"),
    ("MOVE_MUD_SLAP", "Mud-Slap"),
    ("MOVE_OCTAZOOKA", "Octazooka"),
    ("MOVE_SPIKES", "Spikes"),
    ("MOVE_ZAP_CANNON", "Zap Cannon"),
    ("MOVE_FORESIGHT", "Foresight"),
    ("MOVE_DESTINY_BOND", "Destiny Bond"),
    ("MOVE_PERISH_SONG", "Perish Song"),
    ("MOVE_ICY_WIND", "Icy Wind"),
    ("MOVE_DETECT", "Detect"),
    ("MOVE_BONE_RUSH", "Bone Rush"),
    ("MOVE_LOCK_ON", "Lock-On"),
    ("MOVE_OUTRAGE", "Outrage"),
    ("MOVE_SANDSTORM", "Sandstorm"),
    ("MOVE_GIGA_DRAIN", "Giga Drain"),
    ("MOVE_ENDURE", "Endure"),
    ("MOVE_CHARM", "Charm"),
    ("MOVE_ROLLOUT", "Rollout"),
    ("MOVE_FALSE_SWIPE", "False Swipe"),
    ("MOVE_SWAGGER", "Swagger"),
    ("MOVE_MILK_DRINK", "Milk Drink"),
    ("MOVE_SPARK", "Spark"),
    ("MOVE_FURY_CUTTER", "Fury Cutter"),
    ("MOVE_STEEL_WING", "Steel Wing"),
    ("MOVE_MEAN_LOOK", "Mean Look"),
    ("MOVE_ATTRACT", "Attract"),
    ("MOVE_SLEEP_TALK", "Sleep Talk"),
    ("MOVE_HEAL_BELL", "Heal Bell"),
    ("MOVE_RETURN", "Return"),
    ("MOVE_PRESENT", "Present"),
    ("MOVE_FRUSTRATION", "Frustration"),
    ("MOVE_SAFEGUARD", "Safeguard"),
    ("MOVE_PAIN_SPLIT", "Pain Split"),
    ("MOVE_SACRED_FIRE", "Sacred Fire"),
    ("MOVE_MAGNITUDE", "Magnitude"),
    ("MOVE_DYNAMIC_PUNCH", "Dynamicpunch"),
    ("MOVE_MEGAHORN", "Megahorn"),
    ("MOVE_DRAGON_BREATH", "Dragonbreath"),
    ("MOVE_BATON_PASS", "Baton Pass"),
    ("MOVE_ENCORE", "Encore"),
    ("MOVE_PURSUIT", "Pursuit"),
    ("MOVE_RAPID_SPIN", "Rapid Spin"),
    ("MOVE_SWEET_SCENT", "Sweet Scent"),
    ("MOVE_IRON_TAIL", "Iron Tail"),
    ("MOVE_METAL_CLAW", "Metal Claw"),
    ("MOVE_VITAL_THROW", "Vital Throw"),
    ("MOVE_MORNING_SUN", "Morning Sun"),
    ("MOVE_SYNTHESIS", "Synthesis"),
    ("MOVE_MOONLIGHT", "Moonlight"),
    ("MOVE_HIDDEN_POWER", "Hidden Power"),
    ("MOVE_CROSS_CHOP", "Cross Chop"),
    ("MOVE_TWISTER", "Twister"),
    ("MOVE_RAIN_DANCE", "Rain Dance"),
    ("MOVE_SUNNY_DAY", "Sunny Day"),
    ("MOVE_CRUNCH", "Crunch"),
    ("MOVE_MIRROR_COAT", "Mirror Coat"),
    ("MOVE_PSYCH_UP", "Psych Up"),
    ("MOVE_EXTREME_SPEED", "Extremespeed"),
    ("MOVE_ANCIENT_POWER", "Ancientpower"),
    ("MOVE_SHADOW_BALL", "Shadow Ball"),
    ("MOVE_FUTURE_SIGHT", "Future Sight"),
    ("MOVE_ROCK_SMASH", "Rock Smash"),
    ("MOVE_WHIRLPOOL", "Whirlpool"),
    ("MOVE_BEAT_UP", "Beat Up"),
    ("MOVE_FAKE_OUT", "Fake Out"),
    ("MOVE_UPROAR", "Uproar"),
    ("MOVE_STOCKPILE", "Stockpile"),
    ("MOVE_SPIT_UP", "Spit Up"),
    ("MOVE_SWALLOW", "Swallow"),
    ("MOVE_HEAT_WAVE", "Heat Wave"),
    ("MOVE_HAIL", "Hail"),
    ("MOVE_TORMENT", "Torment"),
    ("MOVE_FLATTER", "Flatter"),
    ("MOVE_WILL_O_WISP", "Will-O-Wisp"),
    ("MOVE_MEMENTO", "Memento"),
    ("MOVE_FACADE", "Facade"),
    ("MOVE_FOCUS_PUNCH", "Focus Punch"),
    ("MOVE_SMELLING_SALT", "Smellingsalt"),
    ("MOVE_FOLLOW_ME", "Follow Me"),
    ("MOVE_NATURE_POWER", "Nature Power"),
    ("MOVE_CHARGE", "Charge"),
    ("MOVE_TAUNT", "Taunt"),
    ("MOVE_HELPING_HAND", "Helping Hand"),
    ("MOVE_TRICK", "Trick"),
    ("MOVE_ROLE_PLAY", "Role Play"),
    ("MOVE_WISH", "Wish"),
    ("MOVE_ASSIST", "Assist"),
    ("MOVE_INGRAIN", "Ingrain"),
    ("MOVE_SUPERPOWER", "Superpower"),
    ("MOVE_MAGIC_COAT", "Magic Coat"),
    ("MOVE_RECYCLE", "Recycle"),
    ("MOVE_REVENGE", "Revenge"),
    ("MOVE_BRICK_BREAK", "Brick Break"),
    ("MOVE_YAWN", "Yawn"),
    ("MOVE_KNOCK_OFF", "Knock Off"),
    ("MOVE_ENDEAVOR", "Endeavor"),
    ("MOVE_ERUPTION", "Eruption"),
    ("MOVE_SKILL_SWAP", "Skill Swap"),
    ("MOVE_IMPRISON", "Imprison"),
    ("MOVE_REFRESH", "Refresh"),
    ("MOVE_GRUDGE", "Grudge"),
    ("MOVE_SNATCH", "Snatch"),
    ("MOVE_SECRET_POWER", "Secret Power"),
    ("MOVE_DIVE", "Dive"),
    ("MOVE_ARM_THRUST", "Arm Thrust"),
    ("MOVE_CAMOUFLAGE", "Camouflage"),
    ("MOVE_TAIL_GLOW", "Tail Glow"),
    ("MOVE_LUSTER_PURGE", "Luster Purge"),
    ("MOVE_MIST_BALL", "Mist Ball"),
    ("MOVE_FEATHER_DANCE", "Featherdance"),
    ("MOVE_TEETER_DANCE", "Teeter Dance"),
    ("MOVE_BLAZE_KICK", "Blaze Kick"),
    ("MOVE_MUD_SPORT", "Mud Sport"),
    ("MOVE_ICE_BALL", "Ice Ball"),
    ("MOVE_NEEDLE_ARM", "Needle Arm"),
    ("MOVE_SLACK_OFF", "Slack Off"),
    ("MOVE_HYPER_VOICE", "Hyper Voice"),
    ("MOVE_POISON_FANG", "Poison Fang"),
    ("MOVE_CRUSH_CLAW", "Crush Claw"),
    ("MOVE_BLAST_BURN", "Blast Burn"),
    ("MOVE_HYDRO_CANNON", "Hydro Cannon"),
    ("MOVE_METEOR_MASH", "Meteor Mash"),
    ("MOVE_ASTONISH", "Astonish"),
    ("MOVE_WEATHER_BALL", "Weather Ball"),
    ("MOVE_AROMATHERAPY", "Aromatherapy"),
    ("MOVE_FAKE_TEARS", "Fake Tears"),
    ("MOVE_AIR_CUTTER", "Air Cutter"),
    ("MOVE_OVERHEAT", "Overheat"),
    ("MOVE_ODOR_SLEUTH", "Odor Sleuth"),
    ("MOVE_ROCK_TOMB", "Rock Tomb"),
    ("MOVE_SILVER_WIND", "Silver Wind"),
    ("MOVE_METAL_SOUND", "Metal Sound"),
    ("MOVE_GRASS_WHISTLE", "Grasswhistle"),
    ("MOVE_TICKLE", "Tickle"),
    ("MOVE_COSMIC_POWER", "Cosmic Power"),
    ("MOVE_WATER_SPOUT", "Water Spout"),
    ("MOVE_SIGNAL_BEAM", "Signal Beam"),
    ("MOVE_SHADOW_PUNCH", "Shadow Punch"),
    ("MOVE_EXTRASENSORY", "Extrasensory"),
    ("MOVE_SKY_UPPERCUT", "Sky Uppercut"),
    ("MOVE_SAND_TOMB", "Sand Tomb"),
    ("MOVE_SHEER_COLD", "Sheer Cold"),
    ("MOVE_MUDDY_WATER", "Muddy Water"),
    ("MOVE_BULLET_SEED", "Bullet Seed"),
    ("MOVE_AERIAL_ACE", "Aerial Ace"),
    ("MOVE_ICICLE_SPEAR", "Icicle Spear"),
    ("MOVE_IRON_DEFENSE", "Iron Defense"),
    ("MOVE_BLOCK", "Block"),
    ("MOVE_HOWL", "Howl"),
    ("MOVE_DRAGON_CLAW", "Dragon Claw"),
    ("MOVE_FRENZY_PLANT", "Frenzy Plant"),
    ("MOVE_BULK_UP", "Bulk Up"),
    ("MOVE_BOUNCE", "Bounce"),
    ("MOVE_MUD_SHOT", "Mud Shot"),
    ("MOVE_POISON_TAIL", "Poison Tail"),
    ("MOVE_COVET", "Covet"),
    ("MOVE_VOLT_TACKLE", "Volt Tackle"),
    ("MOVE_MAGICAL_LEAF", "Magical Leaf"),
    ("MOVE_WATER_SPORT", "Water Sport"),
    ("MOVE_CALM_MIND", "Calm Mind"),
    ("MOVE_LEAF_BLADE", "Leaf Blade"),
    ("MOVE_DRAGON_DANCE", "Dragon Dance"),
    ("MOVE_ROCK_BLAST", "Rock Blast"),
    ("MOVE_SHOCK_WAVE", "Shock Wave"),
    ("MOVE_WATER_PULSE", "Water Pulse"),
    ("MOVE_DOOM_DESIRE", "Doom Desire"),
    ("MOVE_PSYCHO_BOOST", "Psycho Boost")
]}

pallet_fly_destinations: List[FlyData] = [
    FlyData("Player's House", "PALLET TOWN", "Pallet Town", "Pallet Town", 3, 0, 6, 8, 1, 246),
    FlyData("Rival's House", "PALLET TOWN", "Pallet Town", "Pallet Town", 3, 0, 15, 8, 1, 246),
    FlyData("Professor Oak's Lab", "PALLET TOWN", "Pallet Town", "Pallet Town", 3, 0, 16, 14, 1, 246)
]

viridian_fly_destinations: List[FlyData] = [
    FlyData("Viridian Pokemon Center", "VIRIDIAN CITY", "Viridian City", "Viridian City (South)", 3, 1, 26, 27, 1, 180),
    FlyData("Virdian Nickname House", "VIRIDIAN CITY", "Viridian City", "Viridian City (South)", 3, 1, 25, 12, 1, 180),
    FlyData("Viridian School", "VIRIDIAN CITY", "Viridian City", "Viridian City (South)", 3, 1, 25, 19, 1, 180),
    FlyData("Viridian Poke Mart", "VIRIDIAN CITY", "Viridian City", "Viridian City (South)", 3, 1, 36, 20, 1, 180),
    FlyData("Viridian Gym", "VIRIDIAN CITY", "Viridian City", "Viridian City (North)", 3, 1, 36, 11, 1, 180),
    FlyData("Viridian Forest South Gate", "ROUTE 2", "Route 2", "Route 2 (Southwest)", 3, 20, 5, 52, 1, 136),
    FlyData("Route 2 Gate (South)", "ROUTE 2", "Route 2", "Route 2 (Southeast)", 3, 20, 18, 47, 1, 136),
    FlyData("Route 22 Gate (South)", "ROUTE 22", "Route 22", "Route 22 (West)", 3, 41, 8, 6, 1, 178)
]

pewter_fly_destinations: List[FlyData] = [
    FlyData("Pewter Museum (West)", "PEWTER CITY", "Pewter City", "Pewter City", 3, 2, 17, 7, 1, 92),
    FlyData("Pewter Gym", "PEWTER CITY", "Pewter City", "Pewter City", 3, 2, 15, 17, 1, 92),
    FlyData("Pewter Poke Mart", "PEWTER CITY", "Pewter City", "Pewter City", 3, 2, 28, 19, 1, 92),
    FlyData("Pewter Nidoran House", "PEWTER CITY", "Pewter City", "Pewter City", 3, 2, 33, 12, 1, 92),
    FlyData("Pewter Pokemon Center", "PEWTER CITY", "Pewter City", "Pewter City", 3, 2, 17, 26, 1, 92),
    FlyData("Pewter Info House", "PEWTER CITY", "Pewter City", "Pewter City", 3, 2, 9, 31, 1, 92),
    FlyData("Pewter Museum (East)", "PEWTER CITY", "Pewter City", "Pewter City (Near Museum)", 3, 2, 25, 5, 1, 92),
    FlyData("Viridian Forest North Gate", "ROUTE 2", "Route 2", "Route 2 (Northwest)", 3, 20, 5, 13, 1, 114),
    FlyData("Diglett's Cave North Entrance", "ROUTE 2", "Route 2", "Route 2 (Northeast)", 3, 20, 17, 12, 1, 114),
    FlyData("Route 2 Trade House", "ROUTE 2", "Route 2", "Route 2 (Northeast)", 3, 20, 17, 23, 1, 114),
    FlyData("Route 2 Gate (North)", "ROUTE 2", "Route 2", "Route 2 (East)", 3, 20, 18, 41, 1, 136)
]

cerulean_fly_destinations: List[FlyData] = [
    FlyData("Badge Guy's House (Front)", "CERULEAN CITY", "Cerulean City", "Cerulean City", 3, 3, 10, 12, 1, 80),
    FlyData("Robbed House (Front)", "CERULEAN CITY", "Cerulean City", "Cerulean City", 3, 3, 30, 12, 1, 80),
    FlyData("Cerulean Trade House", "CERULEAN CITY", "Cerulean City", "Cerulean City", 3, 3, 15, 18, 1, 80),
    FlyData("Cerulean Pokemon Center", "CERULEAN CITY", "Cerulean City", "Cerulean City", 3, 3, 22, 20, 1, 80),
    FlyData("Cerulean Gym", "CERULEAN CITY", "Cerulean City", "Cerulean City", 3, 3, 31, 22, 1, 80),
    FlyData("Bike Shop", "CERULEAN CITY", "Cerulean City", "Cerulean City", 3, 3, 13, 29, 1, 80),
    FlyData("Cerulean Poke Mart", "CERULEAN CITY", "Cerulean City", "Cerulean City", 3, 3, 29, 29, 1, 80),
    FlyData("Wonder News House", "CERULEAN CITY", "Cerulean City", "Cerulean City", 3, 3, 23, 29, 1, 80),
    FlyData("Berry Powder Man's House", "CERULEAN CITY", "Cerulean City", "Cerulean City", 3, 3, 17, 12, 1, 80),
    FlyData("Badge Guy's House (Back)", "CERULEAN CITY", "Cerulean City", "Cerulean City (Backyard)", 3, 3, 10, 8, 1,
            80),
    FlyData("Robbed House (Back)", "CERULEAN CITY", "Cerulean City", "Cerulean City (Outskirts)", 3, 3, 31, 8, 1, 80),
    FlyData("Cerulean Cave", "CERULEAN CITY", "Cerulean City", "Cerulean City (Near Cave)", 3, 3, 1, 13, 1, 80),
    FlyData("Mt. Moon (East)", "ROUTE 4", "Route 4", "Route 4 (East)", 3, 22, 32, 6, 1, 75),
    FlyData("Route 5 Gate (North)", "ROUTE 5", "Route 5", "Route 5", 3, 23, 24, 32, 1, 124),
    FlyData("Route 5 Pokemon Day Care", "ROUTE 5", "Route 5", "Route 5 (Near Daycare)", 3, 23, 23, 26, 1, 124),
    FlyData("Underground Path North Entrance", "ROUTE 5", "Route 5", "Route 5 (Near Underground)", 3, 23, 31, 32, 1,
            124),
    FlyData("Sea Cottage", "ROUTE 25", "Route 25", "Route 25", 3, 44, 51, 5, 1, 38)
]

vermilion_fly_destinations: List[FlyData] = [
    FlyData("Vermilion Fishing House", "VERMILION CITY", "Vermilion City", "Vermilion City", 3, 5, 9, 7, 1, 212),
    FlyData("Vermilion Pokemon Center", "VERMILION CITY", "Vermilion City", "Vermilion City", 3, 5, 15, 7, 1, 212),
    FlyData("Pokemon Fan Club", "VERMILION CITY", "Vermilion City", "Vermilion City", 3, 5, 12, 18, 1, 212),
    FlyData("Vermilion Trade House", "VERMILION CITY", "Vermilion City", "Vermilion City", 3, 5, 19, 18, 1, 212),
    FlyData("Vermilion Poke Mart", "VERMILION CITY", "Vermilion City", "Vermilion City", 3, 5, 29, 18, 1, 212),
    FlyData("Vermilion Pidgey House", "VERMILION CITY", "Vermilion City", "Vermilion City", 3, 5, 28, 25, 1, 212),
    FlyData("Vermilion Gym", "VERMILION CITY", "Vermilion City", "Vermilion City (Near Gym)", 3, 5, 14, 26, 1, 212),
    FlyData("Vermilion Harbor", "VERMILION CITY", "Vermilion City", "Vermilion City (Near Harbor)", 3, 5, 23, 34, 1,
            212),
    FlyData("Route 6 Gate (South)", "ROUTE 6", "Route 6", "Route 6", 3, 24, 12, 6, 1, 168),
    FlyData("Underground Path South Entrance", "ROUTE 6", "Route 6", "Route 6 (Near Underground)", 3, 24, 19, 14, 1,
            168),
    FlyData("Diglett's Cave South Entrance", "ROUTE 11", "Route 11", "Route 11 (West)", 3, 29, 6, 8, 1, 213),
    FlyData("Route 11 Gate (West)", "ROUTE 11", "Route 11", "Route 11 (West)", 3, 29, 58, 10, 1, 215),
    FlyData("Route 11 Gate (East)", "ROUTE 11", "Route 11", "Route 11 (East)", 3, 29, 65, 10, 1, 215)
]

lavender_fly_destinations: List[FlyData] = [
    FlyData("Pokemon Tower", "LAVENDER TOWN", "Lavender Town", "Lavender Town", 3, 4, 18, 7, 1, 150),
    FlyData("Lavender Pokemon Center", "LAVENDER TOWN", "Lavender Town", "Lavender Town", 3, 4, 6, 6, 1, 150),
    FlyData("Volunteer Pokemon House", "LAVENDER TOWN", "Lavender Town", "Lavender Town", 3, 4, 10, 12, 1, 150),
    FlyData("Lavender Cubone House", "LAVENDER TOWN", "Lavender Town", "Lavender Town", 3, 4, 5, 17, 1, 150),
    FlyData("Name Rater's House", "LAVENDER TOWN", "Lavender Town", "Lavender Town", 3, 4, 10, 17, 1, 150),
    FlyData("Lavender Poke Mart", "LAVENDER TOWN", "Lavender Town", "Lavender Town", 3, 4, 20, 16, 1, 150),
    FlyData("Route 8 Gate (East)", "ROUTE 8", "Route 8", "Route 8", 3, 26, 7, 10, 1, 147),
    FlyData("Underground Path East Entrance", "ROUTE 8", "Route 8", "Route 8 (Near Underground)", 3, 26, 13, 5, 1, 147),
    FlyData("Route 12 Gate (North)", "ROUTE 12", "Route 12", "Route 12 (North)", 3, 30, 14, 15, 1, 172),
    FlyData("Route 12 Gate (South)", "ROUTE 12", "Route 12", "Route 12 (Center)", 3, 30, 14, 22, 1, 172),
    FlyData("Route 12 Fishing House", "ROUTE 12", "Route 12", "Route 12 (South)", 3, 30, 12, 87, 1, 238)
]

celadon_fly_destinations: List[FlyData] = [
    FlyData("Celadon Game Corner", "CELADON CITY", "Celadon City", "Celadon City", 3, 6, 34, 22, 1, 143),
    FlyData("Celadon Department Store (West)", "CELADON CITY", "Celadon City", "Celadon City", 3, 6, 11, 15, 1, 143),
    FlyData("Celadon Department Store (East)", "CELADON CITY", "Celadon City", "Celadon City", 3, 6, 15, 15, 1, 143),
    FlyData("Celadon Condominiums (Front)", "CELADON CITY", "Celadon City", "Celadon City", 3, 6, 30, 12, 1, 143),
    FlyData("Celadon Pokemon Center", "CELADON CITY", "Celadon City", "Celadon City", 3, 6, 48, 12, 1, 143),
    FlyData("Celadon Game Corner Prize Room", "CELADON CITY", "Celadon City", "Celadon City", 3, 6, 39, 21, 1, 143),
    FlyData("Celadon Restaurant", "CELADON CITY", "Celadon City", "Celadon City", 3, 6, 37, 30, 1, 143),
    FlyData("Celadon Rocket House", "CELADON CITY", "Celadon City", "Celadon City", 3, 6, 41, 30, 1, 143),
    FlyData("Celadon Hotel", "CELADON CITY", "Celadon City", "Celadon City", 3, 6, 49, 30, 1, 143),
    FlyData("Celadon Condominiums (Back)", "CELADON CITY", "Celadon City", "Celadon City", 3, 6, 30, 4, 1, 143),
    FlyData("Celadon Gym", "CELADON CITY", "Celadon City", "Celadon City (Near Gym)", 3, 6, 11, 31, 1, 143),
    FlyData("Route 7 Gate (West)", "ROUTE 7", "Route 7", "Route 7", 3, 25, 15, 10, 1, 145),
    FlyData("Underground Path West Entrance", "ROUTE 7", "Route 7", "Route 7 (Near Underground)", 3, 25, 7, 15, 1, 144),
    FlyData("Route 16 Gate (Northeast)", "ROUTE 16", "Route 16", "Route 16 (Northeast)", 3, 34, 27, 6, 1, 141),
    FlyData("Route 16 Fly House", "ROUTE 16", "Route 16", "Route 16 (Northwest)", 3, 34, 10, 6, 1, 139),
    FlyData("Route 16 Gate (Northwest)", "ROUTE 16", "Route 16", "Route 16 (Northwest)", 3, 34, 20, 6, 1, 140),
    FlyData("Route 16 Gate (Southeast)", "ROUTE 16", "Route 16", "Route 16 (Center)", 3, 34, 27, 13, 1, 141)
]

fuchsia_fly_destinations: List[FlyData] = [
    FlyData("Safari Zone Entrance", "FUCHSIA CITY", "Fuchsia City", "Fuchsia City", 3, 7, 24, 6, 1, 276),
    FlyData("Safari Zone Warden's House", "FUCHSIA CITY", "Fuchsia City", "Fuchsia City", 3, 7, 33, 32, 1, 276),
    FlyData("Fuchsia Poke Mart", "FUCHSIA CITY", "Fuchsia City", "Fuchsia City", 3, 7, 11, 16, 1, 276),
    FlyData("Safari Zone Office", "FUCHSIA CITY", "Fuchsia City", "Fuchsia City", 3, 7, 28, 17, 1, 276),
    FlyData("Fuchsia Gym", "FUCHSIA CITY", "Fuchsia City", "Fuchsia City", 3, 7, 9, 33, 1, 276),
    FlyData("Bill's Grandpa's House", "FUCHSIA CITY", "Fuchsia City", "Fuchsia City", 3, 7, 14, 32, 1, 276),
    FlyData("Fuchsia Pokemon Center", "FUCHSIA CITY", "Fuchsia City", "Fuchsia City", 3, 7, 25, 32, 1, 276),
    FlyData("Fuchsia Fishing House (Front)", "FUCHSIA CITY", "Fuchsia City", "Fuchsia City", 3, 7, 38, 32, 1, 276),
    FlyData("Move Deleter's House", "FUCHSIA CITY", "Fuchsia City", "Fuchsia City", 3, 7, 19, 32, 1, 276),
    FlyData("Fuchsia Fishing House (Back)", "FUCHSIA CITY", "Fuchsia City", "Fuchsia City (Backyard)", 3, 7, 39, 28, 1,
            276),
    FlyData("Route 15 Gate (East)", "ROUTE 15", "Route 15", "Route 15 (South)", 3, 33, 16, 11, 1, 277),
    FlyData("Route 15 Gate (West)", "ROUTE 15", "Route 15", "Route 15 (Southwest)", 3, 33, 9, 11, 1, 277),
    FlyData("Route 18 Gate (East)", "ROUTE 18", "Route 18", "Route 18 (East)", 3, 36, 48, 9, 1, 275),
    FlyData("Seafoam Islands (North)", "ROUTE 20", "Route 20", "Route 20 (Near North Cave)", 3, 38, 60, 9, 1, 316)
]

saffron_fly_destinations: List[FlyData] = [
    FlyData("Silph Co.", "SAFFRON CITY", "Saffron City", "Saffron City", 3, 10, 33, 31, 1, 146),
    FlyData("Copycat's House", "SAFFRON CITY", "Saffron City", "Saffron City", 3, 10, 22, 15, 1, 146),
    FlyData("Saffron Dojo", "SAFFRON CITY", "Saffron City", "Saffron City", 3, 10, 40, 13, 1, 146),
    FlyData("Saffron Gym", "SAFFRON CITY", "Saffron City", "Saffron City", 3, 10, 46, 13, 1, 146),
    FlyData("Saffron Pidgey House", "SAFFRON CITY", "Saffron City", "Saffron City", 3, 10, 27, 22, 1, 146),
    FlyData("Saffron Poke Mart", "SAFFRON CITY", "Saffron City", "Saffron City", 3, 10, 40, 22, 1, 146),
    FlyData("Saffron Pokemon Center", "SAFFRON CITY", "Saffron City", "Saffron City", 3, 10, 24, 39, 1, 146),
    FlyData("Mr. Psychic's House", "SAFFRON CITY", "Saffron City", "Saffron City", 3, 10, 43, 39, 1, 146),
    FlyData("Route 7 Gate (East)", "SAFFRON CITY", "Saffron City", "Saffron City", 3, 10, 8, 27, 1, 146),
    FlyData("Route 5 Gate (South)", "SAFFRON CITY", "Saffron City", "Saffron City", 3, 10, 34, 6, 1, 146),
    FlyData("Route 8 Gate (West)", "SAFFRON CITY", "Saffron City", "Saffron City", 3, 10, 58, 27, 1, 146),
    FlyData("Route 6 Gate (North)", "SAFFRON CITY", "Saffron City", "Saffron City", 3, 10, 34, 46, 1, 146),
    FlyData("Pokemon Trainer Fan Club", "SAFFRON CITY", "Saffron City", "Saffron City", 3, 10, 47, 22, 1, 146)
]

cinnabar_fly_destinations: List[FlyData] = [
    FlyData("Pokemon Mansion", "CINNABAR ISLAND", "Cinnabar Island", "Cinnabar Island", 3, 8, 8, 4, 1, 312),
    FlyData("Cinnabar Gym", "CINNABAR ISLAND", "Cinnabar Island", "Cinnabar Island", 3, 8, 20, 5, 1, 312),
    FlyData("Pokemon Lab", "CINNABAR ISLAND", "Cinnabar Island", "Cinnabar Island", 3, 8, 8, 10, 1, 312),
    FlyData("Cinnabar Pokemon Center", "CINNABAR ISLAND", "Cinnabar Island", "Cinnabar Island", 3, 8, 14, 12, 1, 312),
    FlyData("Cinnabar Poke Mart", "CINNABAR ISLAND", "Cinnabar Island", "Cinnabar Island", 3, 8, 19, 12, 1, 312),
    FlyData("Seafoam Islands (South)", "ROUTE 20", "Route 20", "Route 20 (Near South Cave)", 3, 38, 72, 15, 1, 317)
]

indigo_fly_destinations: List[FlyData] = [
    FlyData("Indigo Plateau Pokemon Center", "INDIGO PLATEAU", "Indigo Plateau", "Indigo Plateau", 3, 9, 11, 7, 1, 68),
    FlyData("Route 22 Gate (North)", "ROUTE 23", "Route 23", "Route 23 (South)", 3, 42, 8, 153, 1, 156),
    FlyData("Victory Road (West)", "ROUTE 23", "Route 23", "Route 23 (Near Cave)", 3, 42, 5, 29, 1, 90),
    FlyData("Victory Road (East)", "ROUTE 23", "Route 23", "Route 23 (North)", 3, 42, 18, 29, 1, 90)
]

route_4_fly_destinations: List[FlyData] = [
    FlyData("Mt. Moon (West)", "ROUTE 4", "Route 4", "Route 4 (West)", 3, 22, 19, 6, 1, 75),
    FlyData("Route 4 Pokemon Center", "ROUTE 4", "Route 4", "Route 4 (West)", 3, 22, 12, 6, 1, 74)
]

route_10_fly_destinations: List[FlyData] = [
    FlyData("Rock Tunnel (North)", "ROUTE 10", "Route 10", "Route 10 (North)", 3, 28, 8, 20, 1, 84),
    FlyData("Route 10 Pokemon Center", "ROUTE 10", "Route 10", "Route 10 (North)", 3, 28, 13, 21, 1, 84),
    FlyData("Rock Tunnel (South)", "ROUTE 10", "Route 10", "Route 10 (South)", 3, 28, 8, 58, 1, 128),
    FlyData("Power Plant (Front)", "ROUTE 10", "Route 10", "Route 10 (Near Power Plant)", 3, 28, 7, 41, 1, 106),
    FlyData("Power Plant (Back)", "ROUTE 10", "Route 10", "Route 10 (Near Power Plant Back)", 3, 28, 2, 37, 1, 106)
]

navel_rock_fly_destinations: List[FlyData] = [
    FlyData("Navel Rock", "NAVEL ROCK", "Navel Rock Exterior", "Navel Rock Exterior", 2, 0, 9, 9, 3, 186),
    FlyData("Navel Rock Harbor", "NAVEL ROCK", "Navel Rock Exterior", "Navel Rock Exterior", 2, 0, 9, 16, 3, 186)
]

birth_island_fly_destinations: List[FlyData] = [
    FlyData("Birth Island Harbor", "BIRTH ISLAND", "Birth Island Exterior", "Birth Island Exterior", 2, 56, 15, 24, 4,
            304)
]

one_island_fly_destinations: List[FlyData] = [
    FlyData("One Island Pokemon Center", "ONE ISLAND", "One Island", "One Island Town", 3, 12, 14, 6, 2, 177),
    FlyData("One Island Old Couple's House", "ONE ISLAND", "One Island", "One Island Town", 3, 12, 19, 10, 2, 177),
    FlyData("One Island Lass' House", "ONE ISLAND", "One Island", "One Island Town", 3, 12, 8, 12, 2, 177),
    FlyData("One Island Harbor", "ONE ISLAND", "One Island", "One Island Town", 3, 12, 12, 18, 2, 177),
    FlyData("Ember Spa", "KINDLE ROAD", "Kindle Road", "Kindle Road (Center)", 3, 45, 15, 59, 2, 112),
    FlyData("Mt. Ember", "KINDLE ROAD", "Kindle Road", "Kindle Road (North)", 3, 45, 11, 6, 2, 68)
]

two_island_fly_destinations: List[FlyData] = [
    FlyData("Two Island Game Corner", "TWO ISLAND", "Two Island", "Two Island Town", 3, 13, 39, 10, 2, 207),
    FlyData("Move Maniac's House", "TWO ISLAND", "Two Island", "Two Island Town", 3, 13, 33, 10, 2, 207),
    FlyData("Two Island Pokemon Center", "TWO ISLAND", "Two Island", "Two Island Town", 3, 13, 21, 8, 2, 207),
    FlyData("Two Island Harbor", "TWO ISLAND", "Two Island", "Two Island Town", 3, 13, 10, 8, 2, 207),
    FlyData("Starter Tutor's House", "CAPE BRINK", "Cape Brink", "Cape Brink", 3, 47, 12, 17, 2, 163)
]

three_island_fly_destinations: List[FlyData] = [
    FlyData("Three Isle Path (West)", "THREE ISLE PORT", "Three Isle Port", "Three Isle Port (West)", 3, 49, 16, 5, 2,
            304),
    FlyData("Three Island Harbor", "THREE ISLE PORT", "Three Isle Port", "Three Isle Port (West)", 3, 49, 12, 13, 2,
            304),
    FlyData("Three Isle Path (East)", "THREE ISLE PORT", "Three Isle Port", "Three Isle Port (East)", 3, 49, 38, 6, 2,
            305),
    FlyData("Lostelle's House", "THREE ISLAND", "Three Island", "Three Island Town (South)", 3, 14, 3, 32, 2, 282),
    FlyData("Three Island Pokemon Center", "THREE ISLAND", "Three Island", "Three Island Town (South)", 3, 14, 14, 28,
            2, 282),
    FlyData("Three Island Poke Mart", "THREE ISLAND", "Three Island", "Three Island Town (North)", 3, 14, 18, 13, 2,
            282),
    FlyData("Sabrina Fan's House", "THREE ISLAND", "Three Island", "Three Island Town (North)", 3, 14, 4, 7, 2, 282),
    FlyData("Three Island Beauty's House", "THREE ISLAND", "Three Island", "Three Island Town (North)", 3, 14, 12, 7, 2,
            282),
    FlyData("Three Island Worried Father's House", "THREE ISLAND", "Three Island", "Three Island Town (North)", 3, 14,
            12, 13, 2, 282),
    FlyData("Lostelle's Friend's House", "THREE ISLAND", "Three Island", "Three Island Town (North)", 3, 14, 13, 20, 2,
            282),
    FlyData("Berry Forest", "BOND BRIDGE", "Bond Bridge", "Bond Bridge", 3, 48, 12, 7, 2, 278)
]

four_island_fly_destinations: List[FlyData] = [
    FlyData("Four Island Pokemon Center", "FOUR ISLAND", "Four Island", "Four Island Town", 3, 15, 18, 21, 3, 91),
    FlyData("Four Island Pokemon Day Care", "FOUR ISLAND", "Four Island", "Four Island Town", 3, 15, 12, 14, 3, 91),
    FlyData("Four Island Move Tutor's House", "FOUR ISLAND", "Four Island", "Four Island Town", 3, 15, 25, 15, 3, 91),
    FlyData("Lorelei's House", "FOUR ISLAND", "Four Island", "Four Island Town", 3, 15, 33, 24, 3, 91),
    FlyData("Sticker Man's House", "FOUR ISLAND", "Four Island", "Four Island Town", 3, 15, 25, 27, 3, 91),
    FlyData("Four Island Harbor", "FOUR ISLAND", "Four Island", "Four Island Town", 3, 15, 10, 28, 3, 91),
    FlyData("Four Island Poke Mart", "FOUR ISLAND", "Four Island", "Four Island Town", 3, 15, 22, 27, 3, 91),
    FlyData("Icefall Cave", "FOUR ISLAND", "Four Island", "Four Island Town (Near Cave)", 3, 15, 38, 13, 3, 91)
]

five_island_fly_destinations: List[FlyData] = [
    FlyData("Five Island Harbor", "FIVE ISLAND", "Five Island", "Five Island Town", 3, 16, 12, 14, 3, 258),
    FlyData("Five Island Pokemon Center", "FIVE ISLAND", "Five Island", "Five Island Town", 3, 16, 18, 7, 3, 258),
    FlyData("Five Island Couple's House", "FIVE ISLAND", "Five Island", "Five Island Town", 3, 16, 12, 7, 3, 258),
    FlyData("Five Island Old Man's House", "FIVE ISLAND", "Five Island", "Five Island Town", 3, 16, 22, 10, 3, 258),
    FlyData("Rocket Warehouse", "FIVE ISLE MEADOW", "Five Isle Meadow", "Five Isle Meadow", 3, 56, 12, 22, 3, 281),
    FlyData("Selphy's House", "RESORT GORGEOUS", "Resort Gorgeous", "Resort Gorgeous (Near Resort)", 3, 54, 39, 9, 3,
            215),
    FlyData("Lost Cave", "RESORT GORGEOUS", "Resort Gorgeous", "Resort Gorgeous (Near Cave)", 3, 54, 64, 14, 3, 216)
]

six_island_fly_destinations: List[FlyData] = [
    FlyData("Six Island Harbor", "SIX ISLAND", "Six Island", "Six Island Town", 3, 18, 11, 23, 4, 127),
    FlyData("Six Island Pokemon Center", "SIX ISLAND", "Six Island", "Six Island Town", 3, 18, 11, 12, 4, 127),
    FlyData("Six Island Old Man's House", "SIX ISLAND", "Six Island", "Six Island Town", 3, 18, 16, 18, 4, 127),
    FlyData("Six Island Poke Mart", "SIX ISLAND", "Six Island", "Six Island Town", 3, 18, 20, 12, 4, 127),
    FlyData("Water Path Heracross Woman's House", "WATER PATH", "Water Path", "Water Path (North)", 3, 60, 5, 14, 4,
            84),
    FlyData("Water Path Man's House", "WATER PATH", "Water Path", "Water Path (North)", 3, 60, 11, 20, 4, 84),
    FlyData("Dotted Hole", "RUIN VALLEY", "Ruin Valley", "Ruin Valley", 3, 61, 24, 25, 4, 192),
    FlyData("Pattern Bush (East)", "GREEN PATH", "Green Path", "Green Path (East)", 3, 59, 63, 11, 4, 83),
    FlyData("Pattern Bush (West)", "GREEN PATH", "Green Path", "Green Path (West)", 3, 59, 45, 11, 4, 82),
    FlyData("Altering Cave", "OUTCAST ISLAND", "Outcast Island", "Outcast Island", 3, 58, 7, 22, 4, 15)
]

seven_island_fly_destinations: List[FlyData] = [
    FlyData("Seven Island Trainer Battle House", "SEVEN ISLAND", "Seven Island", "Seven Island Town", 3, 17, 11, 10, 4,
            181),
    FlyData("Seven Island Poke Mart", "SEVEN ISLAND", "Seven Island", "Seven Island Town", 3, 17, 5, 10, 4, 181),
    FlyData("Seven Island Pokemon Center", "SEVEN ISLAND", "Seven Island", "Seven Island Town", 3, 17, 12, 4, 4, 181),
    FlyData("Seven Island Harbor", "SEVEN ISLAND", "Seven Island", "Seven Island Town", 3, 17, 16, 13, 4, 181),
    FlyData("Tanoby Key", "SEVAULT CANYON", "Sevault Canyon", "Sevault Canyon", 3, 64, 7, 18, 4, 204),
    FlyData("Sevault Canyon Chansey House", "SEVAULT CANYON", "Sevault Canyon", "Sevault Canyon", 3, 64, 14, 62, 4,
            248),
    FlyData("Viapois Chamber", "TANOBY RUINS", "Tanoby Ruins", "Tanoby Ruins (Viapois Island)", 3, 65, 11, 7, 4, 267),
    FlyData("Rixy Chamber", "TANOBY RUINS", "Tanoby Ruins", "Tanoby Ruins (Rixy Island)", 3, 65, 12, 16, 4, 267),
    FlyData("Scufib Chamber", "TANOBY RUINS", "Tanoby Ruins", "Tanoby Ruins (Scufib Island)", 3, 65, 32, 10, 4, 268),
    FlyData("Dilford Chamber", "TANOBY RUINS", "Tanoby Ruins", "Tanoby Ruins (Dilford Island)", 3, 65, 44, 12, 4, 269),
    FlyData("Weepth Chamber", "TANOBY RUINS", "Tanoby Ruins", "Tanoby Ruins (Weepth Island)", 3, 65, 88, 9, 4, 271),
    FlyData("Liptoo Chamber", "TANOBY RUINS", "Tanoby Ruins", "Tanoby Ruins (Liptoo Island)", 3, 65, 103, 11, 4, 272),
    FlyData("Monean Chamber", "TANOBY RUINS", "Tanoby Ruins", "Tanoby Ruins (Monean Island)", 3, 65, 120, 11, 4, 273),
    FlyData("Trainer Tower", "TRAINER TOWER", "Trainer Tower Exterior", "Trainer Tower Exterior (North)", 3, 62, 58, 8,
            4, 137)
]

kanto_fly_destinations: List[FlyData] = [
    *pallet_fly_destinations, *viridian_fly_destinations, *pewter_fly_destinations, *cerulean_fly_destinations,
    *vermilion_fly_destinations, *lavender_fly_destinations, *celadon_fly_destinations, *fuchsia_fly_destinations,
    *saffron_fly_destinations, *cinnabar_fly_destinations, *indigo_fly_destinations, *route_4_fly_destinations,
    *route_10_fly_destinations
]

sevii_123_fly_destinations: List[FlyData] = [
    *one_island_fly_destinations, *two_island_fly_destinations, *three_island_fly_destinations
]

sevii_45_fly_destinations: List[FlyData] = [
    *four_island_fly_destinations, *five_island_fly_destinations, *navel_rock_fly_destinations
]

sevii_67_fly_destinations: List[FlyData] = [
    *six_island_fly_destinations, *seven_island_fly_destinations, *birth_island_fly_destinations
]

sevii_fly_destinations: List[FlyData] = [
    *sevii_123_fly_destinations, *sevii_45_fly_destinations, *sevii_67_fly_destinations
]

all_fly_destinations: List[FlyData] = [
    *kanto_fly_destinations, *sevii_fly_destinations
]

fly_destination_areas: Dict[str, List[FlyData]] = {
    "Pallet Town Fly Destination": pallet_fly_destinations,
    "Viridian City Fly Destination": viridian_fly_destinations,
    "Pewter City Fly Destination": pewter_fly_destinations,
    "Route 4 Fly Destination": route_4_fly_destinations,
    "Cerulean City Fly Destination": cerulean_fly_destinations,
    "Vermilion City Fly Destination": vermilion_fly_destinations,
    "Route 10 Fly Destination": route_10_fly_destinations,
    "Lavender Town Fly Destination": lavender_fly_destinations,
    "Celadon City Fly Destination": celadon_fly_destinations,
    "Fuchsia City Fly Destination": fuchsia_fly_destinations,
    "Saffron City Fly Destination": saffron_fly_destinations,
    "Cinnabar Island Fly Destination": cinnabar_fly_destinations,
    "Indigo Plateau Fly Destination": indigo_fly_destinations,
    "One Island Fly Destination": one_island_fly_destinations,
    "Two Island Fly Destination": two_island_fly_destinations,
    "Three Island Fly Destination": three_island_fly_destinations,
    "Four Island Fly Destination": four_island_fly_destinations,
    "Five Island Fly Destination": five_island_fly_destinations,
    "Six Island Fly Destination": six_island_fly_destinations,
    "Seven Island Fly Destination": seven_island_fly_destinations,
}

fly_destination_maps: Dict[str, List[FlyData]] = {
    "Pallet Town Fly Destination": kanto_fly_destinations,
    "Viridian City Fly Destination": kanto_fly_destinations,
    "Pewter City Fly Destination": kanto_fly_destinations,
    "Route 4 Fly Destination": kanto_fly_destinations,
    "Cerulean City Fly Destination": kanto_fly_destinations,
    "Vermilion City Fly Destination": kanto_fly_destinations,
    "Route 10 Fly Destination": kanto_fly_destinations,
    "Lavender Town Fly Destination": kanto_fly_destinations,
    "Celadon City Fly Destination": kanto_fly_destinations,
    "Fuchsia City Fly Destination": kanto_fly_destinations,
    "Saffron City Fly Destination": kanto_fly_destinations,
    "Cinnabar Island Fly Destination": kanto_fly_destinations,
    "Indigo Plateau Fly Destination": kanto_fly_destinations,
    "One Island Fly Destination": sevii_123_fly_destinations,
    "Two Island Fly Destination": sevii_123_fly_destinations,
    "Three Island Fly Destination": sevii_123_fly_destinations,
    "Four Island Fly Destination": sevii_45_fly_destinations,
    "Five Island Fly Destination": sevii_45_fly_destinations,
    "Six Island Fly Destination": sevii_67_fly_destinations,
    "Seven Island Fly Destination": sevii_67_fly_destinations,
}

fly_destination_regions: Dict[str, List[FlyData]] = {
    "Pallet Town Fly Destination": kanto_fly_destinations,
    "Viridian City Fly Destination": kanto_fly_destinations,
    "Pewter City Fly Destination": kanto_fly_destinations,
    "Route 4 Fly Destination": kanto_fly_destinations,
    "Cerulean City Fly Destination": kanto_fly_destinations,
    "Vermilion City Fly Destination": kanto_fly_destinations,
    "Route 10 Fly Destination": kanto_fly_destinations,
    "Lavender Town Fly Destination": kanto_fly_destinations,
    "Celadon City Fly Destination": kanto_fly_destinations,
    "Fuchsia City Fly Destination": kanto_fly_destinations,
    "Saffron City Fly Destination": kanto_fly_destinations,
    "Cinnabar Island Fly Destination": kanto_fly_destinations,
    "Indigo Plateau Fly Destination": kanto_fly_destinations,
    "One Island Fly Destination": sevii_fly_destinations,
    "Two Island Fly Destination": sevii_fly_destinations,
    "Three Island Fly Destination": sevii_fly_destinations,
    "Four Island Fly Destination": sevii_fly_destinations,
    "Five Island Fly Destination": sevii_fly_destinations,
    "Six Island Fly Destination": sevii_fly_destinations,
    "Seven Island Fly Destination": sevii_fly_destinations,
}

fly_destination_random: Dict[str, List[FlyData]] = {
    "Pallet Town Fly Destination": all_fly_destinations,
    "Viridian City Fly Destination": all_fly_destinations,
    "Pewter City Fly Destination": all_fly_destinations,
    "Route 4 Fly Destination": all_fly_destinations,
    "Cerulean City Fly Destination": all_fly_destinations,
    "Vermilion City Fly Destination": all_fly_destinations,
    "Route 10 Fly Destination": all_fly_destinations,
    "Lavender Town Fly Destination": all_fly_destinations,
    "Celadon City Fly Destination": all_fly_destinations,
    "Fuchsia City Fly Destination": all_fly_destinations,
    "Saffron City Fly Destination": all_fly_destinations,
    "Cinnabar Island Fly Destination": all_fly_destinations,
    "Indigo Plateau Fly Destination": all_fly_destinations,
    "One Island Fly Destination": all_fly_destinations,
    "Two Island Fly Destination": all_fly_destinations,
    "Three Island Fly Destination": all_fly_destinations,
    "Four Island Fly Destination": all_fly_destinations,
    "Five Island Fly Destination": all_fly_destinations,
    "Six Island Fly Destination": all_fly_destinations,
    "Seven Island Fly Destination": all_fly_destinations,
}

fly_plando_maps: Dict[str, FlyData] = {}
for fly_data in all_fly_destinations:
    fly_plando_maps[fly_data.name] = fly_data

NATIONAL_ID_TO_SPECIES_ID = {species.national_dex_number: i for i, species in data.species.items()}
NAME_TO_SPECIES_ID = {species.name: i for i, species in data.species.items()}

TRAINER_REMATCH_MAP: Dict[str, List[str]] = {
    "TRAINER_BEAUTY_GRACE_REWARD": ["TRAINER_BEAUTY_GRACE_2_REWARD"],
    "TRAINER_BEAUTY_SHEILA_REWARD": ["TRAINER_BEAUTY_SHEILA_2_REWARD"],
    "TRAINER_BIKER_JAREN_REWARD": ["TRAINER_BIKER_JAREN_2_REWARD"],
    "TRAINER_BIKER_JAXON_REWARD": ["TRAINER_BIKER_JAXON_2_REWARD"],
    "TRAINER_BIKER_LUKAS_REWARD": ["TRAINER_BIKER_LUKAS_2_REWARD"],
    "TRAINER_BIKER_RUBEN_REWARD": ["TRAINER_BIKER_RUBEN_2_REWARD"],
    "TRAINER_BIRD_KEEPER_BENNY_REWARD": ["TRAINER_BIRD_KEEPER_BENNY_2_REWARD",
                                         "TRAINER_BIRD_KEEPER_BENNY_3_REWARD"],
    "TRAINER_BIRD_KEEPER_CHAZ_REWARD": ["TRAINER_BIRD_KEEPER_CHAZ_2_REWARD"],
    "TRAINER_BIRD_KEEPER_CHESTER_REWARD": ["TRAINER_BIRD_KEEPER_CHESTER_2_REWARD",
                                           "TRAINER_BIRD_KEEPER_CHESTER_3_REWARD"],
    "TRAINER_BIRD_KEEPER_HAROLD_REWARD": ["TRAINER_BIRD_KEEPER_HAROLD_2_REWARD"],
    "TRAINER_BIRD_KEEPER_JACOB_REWARD": ["TRAINER_BIRD_KEEPER_JACOB_2_REWARD",
                                         "TRAINER_BIRD_KEEPER_JACOB_3_REWARD"],
    "TRAINER_BIRD_KEEPER_MARLON_REWARD": ["TRAINER_BIRD_KEEPER_MARLON_2_REWARD",
                                          "TRAINER_BIRD_KEEPER_MARLON_3_REWARD"],
    "TRAINER_BIRD_KEEPER_MILO_REWARD": ["TRAINER_BIRD_KEEPER_MILO_2_REWARD"],
    "TRAINER_BIRD_KEEPER_ROBERT_REWARD": ["TRAINER_BIRD_KEEPER_ROBERT_2_REWARD",
                                          "TRAINER_BIRD_KEEPER_ROBERT_3_REWARD"],
    "TRAINER_BLACK_BELT_HUGH_REWARD": ["TRAINER_BLACK_BELT_HUGH_2_REWARD",
                                       "TRAINER_BLACK_BELT_HUGH_3_REWARD"],
    "TRAINER_BLACK_BELT_SHEA_REWARD": ["TRAINER_BLACK_BELT_SHEA_2_REWARD",
                                       "TRAINER_BLACK_BELT_SHEA_3_REWARD"],
    "TRAINER_BUG_CATCHER_COLTON_REWARD": ["TRAINER_BUG_CATCHER_COLTON_2_REWARD",
                                          "TRAINER_BUG_CATCHER_COLTON_3_REWARD",
                                          "TRAINER_BUG_CATCHER_COLTON_4_REWARD"],
    "TRAINER_CAMPER_CHRIS_REWARD": ["TRAINER_CAMPER_CHRIS_2_REWARD",
                                    "TRAINER_CAMPER_CHRIS_3_REWARD",
                                    "TRAINER_CAMPER_CHRIS_4_REWARD"],
    "TRAINER_CAMPER_JEFF_REWARD": ["TRAINER_CAMPER_JEFF_2_REWARD",
                                   "TRAINER_CAMPER_JEFF_3_REWARD",
                                   "TRAINER_CAMPER_JEFF_4_REWARD"],
    "TRAINER_CAMPER_RICKY_REWARD": ["TRAINER_CAMPER_RICKY_2_REWARD",
                                    "TRAINER_CAMPER_RICKY_3_REWARD",
                                    "TRAINER_CAMPER_RICKY_4_REWARD"],
    "TRAINER_COOLTRAINER_LEROY_REWARD": ["TRAINER_COOLTRAINER_LEROY_2_REWARD"],
    "TRAINER_COOLTRAINER_MICHELLE_REWARD": ["TRAINER_COOLTRAINER_MICHELLE_2_REWARD"],
    "TRAINER_COOL_COUPLE_LEX_NYA_REWARD": ["TRAINER_COOL_COUPLE_LEX_NYA_2_REWARD"],
    "TRAINER_CRUSH_GIRL_CYNDY_REWARD": ["TRAINER_CRUSH_GIRL_CYNDY_2_REWARD"],
    "TRAINER_CRUSH_GIRL_SHARON_REWARD": ["TRAINER_CRUSH_GIRL_SHARON_2_REWARD",
                                         "TRAINER_CRUSH_GIRL_SHARON_3_REWARD"],
    "TRAINER_CRUSH_GIRL_TANYA_REWARD": ["TRAINER_CRUSH_GIRL_TANYA_2_REWARD",
                                        "TRAINER_CRUSH_GIRL_TANYA_3_REWARD"],
    "TRAINER_CRUSH_KIN_MIK_KIA_REWARD": ["TRAINER_CRUSH_KIN_MIK_KIA_2_REWARD",
                                         "TRAINER_CRUSH_KIN_MIK_KIA_3_REWARD"],
    "TRAINER_CRUSH_KIN_RON_MYA_REWARD": ["TRAINER_CRUSH_KIN_RON_MYA_2_REWARD",
                                         "TRAINER_CRUSH_KIN_RON_MYA_3_REWARD",
                                         "TRAINER_CRUSH_KIN_RON_MYA_4_REWARD"],
    "TRAINER_CUE_BALL_CAMRON_REWARD": ["TRAINER_CUE_BALL_CAMRON_2_REWARD"],
    "TRAINER_CUE_BALL_COREY_REWARD": ["TRAINER_CUE_BALL_COREY_2_REWARD"],
    "TRAINER_CUE_BALL_ISAIAH_REWARD": ["TRAINER_CUE_BALL_ISAIAH_2_REWARD"],
    "TRAINER_ENGINEER_BERNIE_REWARD": ["TRAINER_ENGINEER_BERNIE_2_REWARD"],
    "TRAINER_FISHERMAN_ELLIOT_REWARD": ["TRAINER_FISHERMAN_ELLIOT_2_REWARD"],
    "TRAINER_FISHERMAN_WADE_REWARD": ["TRAINER_FISHERMAN_WADE_2_REWARD"],
    "TRAINER_GAMER_DARIAN_REWARD": ["TRAINER_GAMER_DARIAN_2_REWARD"],
    "TRAINER_GAMER_RICH_REWARD": ["TRAINER_GAMER_RICH_2_REWARD"],
    "TRAINER_HIKER_EARL_REWARD": ["TRAINER_HIKER_EARL_2_REWARD"],
    "TRAINER_HIKER_FRANKLIN_REWARD": ["TRAINER_HIKER_FRANKLIN_2_REWARD"],
    "TRAINER_HIKER_JEREMY_REWARD": ["TRAINER_HIKER_JEREMY_2_REWARD"],
    "TRAINER_HIKER_TRENT_REWARD": ["TRAINER_HIKER_TRENT_2_REWARD"],
    "TRAINER_JUGGLER_MASON_REWARD": ["TRAINER_JUGGLER_MASON_2_REWARD"],
    "TRAINER_LASS_JANICE_REWARD": ["TRAINER_LASS_JANICE_2_REWARD",
                                   "TRAINER_LASS_JANICE_3_REWARD"],
    "TRAINER_LASS_MEGAN_REWARD": ["TRAINER_LASS_MEGAN_2_REWARD",
                                  "TRAINER_LASS_MEGAN_3_REWARD"],
    "TRAINER_LASS_RELI_REWARD": ["TRAINER_LASS_RELI_2_REWARD",
                                 "TRAINER_LASS_RELI_3_REWARD"],
    "TRAINER_PAINTER_RAYNA_REWARD": ["TRAINER_PAINTER_RAYNA_2_REWARD"],
    "TRAINER_PICNICKER_ALICIA_REWARD": ["TRAINER_PICNICKER_ALICIA_2_REWARD",
                                        "TRAINER_PICNICKER_ALICIA_3_REWARD",
                                        "TRAINER_PICNICKER_ALICIA_4_REWARD"],
    "TRAINER_PICNICKER_BECKY_REWARD": ["TRAINER_PICNICKER_BECKY_2_REWARD",
                                       "TRAINER_PICNICKER_BECKY_3_REWARD",
                                       "TRAINER_PICNICKER_BECKY_4_REWARD"],
    "TRAINER_PICNICKER_ISABELLE_REWARD": ["TRAINER_PICNICKER_ISABELLE_2_REWARD",
                                          "TRAINER_PICNICKER_ISABELLE_3_REWARD",
                                          "TRAINER_PICNICKER_ISABELLE_4_REWARD"],
    "TRAINER_PICNICKER_KELSEY_REWARD": ["TRAINER_PICNICKER_KELSEY_2_REWARD",
                                        "TRAINER_PICNICKER_KELSEY_3_REWARD",
                                        "TRAINER_PICNICKER_KELSEY_4_REWARD"],
    "TRAINER_PICNICKER_MISSY_REWARD": ["TRAINER_PICNICKER_MISSY_2_REWARD",
                                       "TRAINER_PICNICKER_MISSY_3_REWARD"],
    "TRAINER_PICNICKER_SUSIE_REWARD": ["TRAINER_PICNICKER_SUSIE_2_REWARD",
                                       "TRAINER_PICNICKER_SUSIE_3_REWARD",
                                       "TRAINER_PICNICKER_SUSIE_4_REWARD"],
    "TRAINER_PKMN_BREEDER_ALIZE_REWARD": ["TRAINER_PKMN_BREEDER_ALIZE_2_REWARD"],
    "TRAINER_PKMN_RANGER_JACKSON_REWARD": ["TRAINER_PKMN_RANGER_JACKSON_2_REWARD"],
    "TRAINER_PKMN_RANGER_KATELYN_REWARD": ["TRAINER_PKMN_RANGER_KATELYN_2_REWARD"],
    "TRAINER_PKMN_RANGER_MADELINE_REWARD": ["TRAINER_PKMN_RANGER_MADELINE_2_REWARD"],
    "TRAINER_PKMN_RANGER_NICOLAS_REWARD": ["TRAINER_PKMN_RANGER_NICOLAS_2_REWARD"],
    "TRAINER_POKEMANIAC_HECTOR_REWARD": ["TRAINER_POKEMANIAC_HECTOR_2_REWARD"],
    "TRAINER_POKEMANIAC_HERMAN_REWARD": ["TRAINER_POKEMANIAC_HERMAN_2_REWARD",
                                         "TRAINER_POKEMANIAC_HERMAN_3_REWARD"],
    "TRAINER_POKEMANIAC_MARK_REWARD": ["TRAINER_POKEMANIAC_MARK_2_REWARD",
                                       "TRAINER_POKEMANIAC_MARK_3_REWARD"],
    "TRAINER_PSYCHIC_DARIO_REWARD": ["TRAINER_PSYCHIC_DARIO_2_REWARD"],
    "TRAINER_PSYCHIC_JACLYN_REWARD": ["TRAINER_PSYCHIC_JACLYN_2_REWARD"],
    "TRAINER_PSYCHIC_RODETTE_REWARD": ["TRAINER_PSYCHIC_RODETTE_2_REWARD"],
    "TRAINER_ROCKER_LUCA_REWARD": ["TRAINER_ROCKER_LUCA_2_REWARD"],
    "TRAINER_RUIN_MANIAC_LARRY_REWARD": ["TRAINER_RUIN_MANIAC_LARRY_2_REWARD"],
    "TRAINER_SIS_AND_BRO_LIL_IAN_REWARD": ["TRAINER_SIS_AND_BRO_LIL_IAN_2_REWARD",
                                           "TRAINER_SIS_AND_BRO_LIL_IAN_3_REWARD"],
    "TRAINER_SUPER_NERD_GLENN_REWARD": ["TRAINER_SUPER_NERD_GLENN_2_REWARD"],
    "TRAINER_SWIMMER_FEMALE_ALICE_REWARD": ["TRAINER_SWIMMER_FEMALE_ALICE_2_REWARD"],
    "TRAINER_SWIMMER_FEMALE_MELISSA_REWARD": ["TRAINER_SWIMMER_FEMALE_MELISSA_2_REWARD"],
    "TRAINER_SWIMMER_FEMALE_NICOLE_REWARD": ["TRAINER_SWIMMER_FEMALE_NICOLE_2_REWARD"],
    "TRAINER_SWIMMER_MALE_DARRIN_REWARD": ["TRAINER_SWIMMER_MALE_DARRIN_2_REWARD"],
    "TRAINER_SWIMMER_MALE_FINN_REWARD": ["TRAINER_SWIMMER_MALE_FINN_2_REWARD"],
    "TRAINER_SWIMMER_MALE_JACK_REWARD": ["TRAINER_SWIMMER_MALE_JACK_2_REWARD"],
    "TRAINER_SWIMMER_MALE_MATTHEW_REWARD": ["TRAINER_SWIMMER_MALE_MATTHEW_2_REWARD"],
    "TRAINER_SWIMMER_MALE_SAMIR_REWARD": ["TRAINER_SWIMMER_MALE_SAMIR_2_REWARD"],
    "TRAINER_SWIMMER_MALE_TONY_REWARD": ["TRAINER_SWIMMER_MALE_TONY_2_REWARD"],
    "TRAINER_TAMER_EVAN_REWARD": ["TRAINER_TAMER_EVAN_2_REWARD"],
    "TRAINER_TUBER_AMIRA_REWARD": ["TRAINER_TUBER_AMIRA_2_REWARD"],
    "TRAINER_TWINS_ELI_ANNE_REWARD": ["TRAINER_TWINS_ELI_ANNE_2_REWARD"],
    "TRAINER_TWINS_JOY_MEG_REWARD": ["TRAINER_TWINS_JOY_MEG_2_REWARD"],
    "TRAINER_YOUNGSTER_BEN_REWARD": ["TRAINER_YOUNGSTER_BEN_2_REWARD",
                                     "TRAINER_YOUNGSTER_BEN_3_REWARD",
                                     "TRAINER_YOUNGSTER_BEN_4_REWARD"],
    "TRAINER_YOUNGSTER_CHAD_REWARD": ["TRAINER_YOUNGSTER_CHAD_2_REWARD",
                                      "TRAINER_YOUNGSTER_CHAD_3_REWARD",
                                      "TRAINER_YOUNGSTER_CHAD_4_REWARD"],
    "TRAINER_YOUNGSTER_DESTIN_REWARD": ["TRAINER_YOUNGSTER_DESTIN_2_REWARD"],
    "TRAINER_YOUNGSTER_TIMMY_REWARD": ["TRAINER_YOUNGSTER_TIMMY_2_REWARD",
                                       "TRAINER_YOUNGSTER_TIMMY_3_REWARD",
                                       "TRAINER_YOUNGSTER_TIMMY_4_REWARD"],
    "TRAINER_YOUNGSTER_YASU_REWARD": ["TRAINER_YOUNGSTER_YASU_2_REWARD",
                                      "TRAINER_YOUNGSTER_YASU_3_REWARD"],
    "TRAINER_YOUNG_COUPLE_GIA_JES_REWARD": ["TRAINER_YOUNG_COUPLE_GIA_JES_2_REWARD",
                                            "TRAINER_YOUNG_COUPLE_GIA_JES_3_REWARD"]
}
