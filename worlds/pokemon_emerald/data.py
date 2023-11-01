"""
Pulls data from JSON files in worlds/pokemon_emerald/data/ into classes.
This also includes marrying automatically extracted data with manually
defined data (like location labels or usable pokemon species), some cleanup
and sorting, and Warp methods.
"""
from dataclasses import dataclass
import copy
from enum import IntEnum
import orjson
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
    rom_address: int
    flag: int
    tags: FrozenSet[str]


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
    ram_addresses: Dict[str, int]
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
        self.maps = []
        self.warps = {}
        self.warp_map = {}
        self.trainers = []


def load_json_data(data_name: str) -> Union[List[Any], Dict[str, Any]]:
    return orjson.loads(pkgutil.get_data(__name__, "data/" + data_name).decode('utf-8-sig'))


data = PokemonEmeraldData()

def create_data_copy() -> PokemonEmeraldData:
    new_copy = PokemonEmeraldData()
    new_copy.species = copy.deepcopy(data.species)
    new_copy.tmhm_moves = copy.deepcopy(data.tmhm_moves)
    new_copy.maps = copy.deepcopy(data.maps)
    new_copy.static_encounters = copy.deepcopy(data.static_encounters)
    new_copy.trainers = copy.deepcopy(data.trainers)


def _init() -> None:
    extracted_data: Dict[str, Any] = load_json_data("extracted_data.json")
    data.constants = extracted_data["constants"]
    data.ram_addresses = extracted_data["misc_ram_addresses"]
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
        ("SPECIES_BULBASAUR", "Bulbasaur"),
        ("SPECIES_IVYSAUR", "Ivysaur"),
        ("SPECIES_VENUSAUR", "Venusaur"),
        ("SPECIES_CHARMANDER", "Charmander"),
        ("SPECIES_CHARMELEON", "Charmeleon"),
        ("SPECIES_CHARIZARD", "Charizard"),
        ("SPECIES_SQUIRTLE", "Squirtle"),
        ("SPECIES_WARTORTLE", "Wartortle"),
        ("SPECIES_BLASTOISE", "Blastoise"),
        ("SPECIES_CATERPIE", "Caterpie"),
        ("SPECIES_METAPOD", "Metapod"),
        ("SPECIES_BUTTERFREE", "Butterfree"),
        ("SPECIES_WEEDLE", "Weedle"),
        ("SPECIES_KAKUNA", "Kakuna"),
        ("SPECIES_BEEDRILL", "Beedrill"),
        ("SPECIES_PIDGEY", "Pidgey"),
        ("SPECIES_PIDGEOTTO", "Pidgeotto"),
        ("SPECIES_PIDGEOT", "Pidgeot"),
        ("SPECIES_RATTATA", "Rattata"),
        ("SPECIES_RATICATE", "Raticate"),
        ("SPECIES_SPEAROW", "Spearow"),
        ("SPECIES_FEAROW", "Fearow"),
        ("SPECIES_EKANS", "Ekans"),
        ("SPECIES_ARBOK", "Arbok"),
        ("SPECIES_PIKACHU", "Pikachu"),
        ("SPECIES_RAICHU", "Raichu"),
        ("SPECIES_SANDSHREW", "Sandshrew"),
        ("SPECIES_SANDSLASH", "Sandslash"),
        ("SPECIES_NIDORAN_F", "Nidoran Female"),
        ("SPECIES_NIDORINA", "Nidorina"),
        ("SPECIES_NIDOQUEEN", "Nidoqueen"),
        ("SPECIES_NIDORAN_M", "Nidoran Male"),
        ("SPECIES_NIDORINO", "Nidorino"),
        ("SPECIES_NIDOKING", "Nidoking"),
        ("SPECIES_CLEFAIRY", "Clefairy"),
        ("SPECIES_CLEFABLE", "Clefable"),
        ("SPECIES_VULPIX", "Vulpix"),
        ("SPECIES_NINETALES", "Ninetales"),
        ("SPECIES_JIGGLYPUFF", "Jigglypuff"),
        ("SPECIES_WIGGLYTUFF", "Wigglytuff"),
        ("SPECIES_ZUBAT", "Zubat"),
        ("SPECIES_GOLBAT", "Golbat"),
        ("SPECIES_ODDISH", "Oddish"),
        ("SPECIES_GLOOM", "Gloom"),
        ("SPECIES_VILEPLUME", "Vileplume"),
        ("SPECIES_PARAS", "Paras"),
        ("SPECIES_PARASECT", "Parasect"),
        ("SPECIES_VENONAT", "Venonat"),
        ("SPECIES_VENOMOTH", "Venomoth"),
        ("SPECIES_DIGLETT", "Diglett"),
        ("SPECIES_DUGTRIO", "Dugtrio"),
        ("SPECIES_MEOWTH", "Meowth"),
        ("SPECIES_PERSIAN", "Persian"),
        ("SPECIES_PSYDUCK", "Psyduck"),
        ("SPECIES_GOLDUCK", "Golduck"),
        ("SPECIES_MANKEY", "Mankey"),
        ("SPECIES_PRIMEAPE", "Primeape"),
        ("SPECIES_GROWLITHE", "Growlithe"),
        ("SPECIES_ARCANINE", "Arcanine"),
        ("SPECIES_POLIWAG", "Poliwag"),
        ("SPECIES_POLIWHIRL", "Poliwhirl"),
        ("SPECIES_POLIWRATH", "Poliwrath"),
        ("SPECIES_ABRA", "Abra"),
        ("SPECIES_KADABRA", "Kadabra"),
        ("SPECIES_ALAKAZAM", "Alakazam"),
        ("SPECIES_MACHOP", "Machop"),
        ("SPECIES_MACHOKE", "Machoke"),
        ("SPECIES_MACHAMP", "Machamp"),
        ("SPECIES_BELLSPROUT", "Bellsprout"),
        ("SPECIES_WEEPINBELL", "Weepinbell"),
        ("SPECIES_VICTREEBEL", "Victreebel"),
        ("SPECIES_TENTACOOL", "Tentacool"),
        ("SPECIES_TENTACRUEL", "Tentacruel"),
        ("SPECIES_GEODUDE", "Geodude"),
        ("SPECIES_GRAVELER", "Graveler"),
        ("SPECIES_GOLEM", "Golem"),
        ("SPECIES_PONYTA", "Ponyta"),
        ("SPECIES_RAPIDASH", "Rapidash"),
        ("SPECIES_SLOWPOKE", "Slowpoke"),
        ("SPECIES_SLOWBRO", "Slowbro"),
        ("SPECIES_MAGNEMITE", "Magnemite"),
        ("SPECIES_MAGNETON", "Magneton"),
        ("SPECIES_FARFETCHD", "Farfetch'd"),
        ("SPECIES_DODUO", "Doduo"),
        ("SPECIES_DODRIO", "Dodrio"),
        ("SPECIES_SEEL", "Seel"),
        ("SPECIES_DEWGONG", "Dewgong"),
        ("SPECIES_GRIMER", "Grimer"),
        ("SPECIES_MUK", "Muk"),
        ("SPECIES_SHELLDER", "Shellder"),
        ("SPECIES_CLOYSTER", "Cloyster"),
        ("SPECIES_GASTLY", "Gastly"),
        ("SPECIES_HAUNTER", "Haunter"),
        ("SPECIES_GENGAR", "Gengar"),
        ("SPECIES_ONIX", "Onix"),
        ("SPECIES_DROWZEE", "Drowzee"),
        ("SPECIES_HYPNO", "Hypno"),
        ("SPECIES_KRABBY", "Krabby"),
        ("SPECIES_KINGLER", "Kingler"),
        ("SPECIES_VOLTORB", "Voltorb"),
        ("SPECIES_ELECTRODE", "Electrode"),
        ("SPECIES_EXEGGCUTE", "Exeggcute"),
        ("SPECIES_EXEGGUTOR", "Exeggutor"),
        ("SPECIES_CUBONE", "Cubone"),
        ("SPECIES_MAROWAK", "Marowak"),
        ("SPECIES_HITMONLEE", "Hitmonlee"),
        ("SPECIES_HITMONCHAN", "Hitmonchan"),
        ("SPECIES_LICKITUNG", "Lickitung"),
        ("SPECIES_KOFFING", "Koffing"),
        ("SPECIES_WEEZING", "Weezing"),
        ("SPECIES_RHYHORN", "Rhyhorn"),
        ("SPECIES_RHYDON", "Rhydon"),
        ("SPECIES_CHANSEY", "Chansey"),
        ("SPECIES_TANGELA", "Tangela"),
        ("SPECIES_KANGASKHAN", "Kangaskhan"),
        ("SPECIES_HORSEA", "Horsea"),
        ("SPECIES_SEADRA", "Seadra"),
        ("SPECIES_GOLDEEN", "Goldeen"),
        ("SPECIES_SEAKING", "Seaking"),
        ("SPECIES_STARYU", "Staryu"),
        ("SPECIES_STARMIE", "Starmie"),
        ("SPECIES_MR_MIME", "Mr. Mime"),
        ("SPECIES_SCYTHER", "Scyther"),
        ("SPECIES_JYNX", "Jynx"),
        ("SPECIES_ELECTABUZZ", "Electabuzz"),
        ("SPECIES_MAGMAR", "Magmar"),
        ("SPECIES_PINSIR", "Pinsir"),
        ("SPECIES_TAUROS", "Tauros"),
        ("SPECIES_MAGIKARP", "Magikarp"),
        ("SPECIES_GYARADOS", "Gyarados"),
        ("SPECIES_LAPRAS", "Lapras"),
        ("SPECIES_DITTO", "Ditto"),
        ("SPECIES_EEVEE", "Eevee"),
        ("SPECIES_VAPOREON", "Vaporeon"),
        ("SPECIES_JOLTEON", "Jolteon"),
        ("SPECIES_FLAREON", "Flareon"),
        ("SPECIES_PORYGON", "Porygon"),
        ("SPECIES_OMANYTE", "Omanyte"),
        ("SPECIES_OMASTAR", "Omastar"),
        ("SPECIES_KABUTO", "Kabuto"),
        ("SPECIES_KABUTOPS", "Kabutops"),
        ("SPECIES_AERODACTYL", "Aerodactyl"),
        ("SPECIES_SNORLAX", "Snorlax"),
        ("SPECIES_ARTICUNO", "Articuno"),
        ("SPECIES_ZAPDOS", "Zapdos"),
        ("SPECIES_MOLTRES", "Moltres"),
        ("SPECIES_DRATINI", "Dratini"),
        ("SPECIES_DRAGONAIR", "Dragonair"),
        ("SPECIES_DRAGONITE", "Dragonite"),
        ("SPECIES_MEWTWO", "Mewtwo"),
        ("SPECIES_MEW", "Mew"),
        ("SPECIES_CHIKORITA", "Chikorita"),
        ("SPECIES_BAYLEEF", "Bayleaf"),
        ("SPECIES_MEGANIUM", "Meganium"),
        ("SPECIES_CYNDAQUIL", "Cindaquil"),
        ("SPECIES_QUILAVA", "Quilava"),
        ("SPECIES_TYPHLOSION", "Typhlosion"),
        ("SPECIES_TOTODILE", "Totodile"),
        ("SPECIES_CROCONAW", "Croconaw"),
        ("SPECIES_FERALIGATR", "Feraligatr"),
        ("SPECIES_SENTRET", "Sentret"),
        ("SPECIES_FURRET", "Furret"),
        ("SPECIES_HOOTHOOT", "Hoothoot"),
        ("SPECIES_NOCTOWL", "Noctowl"),
        ("SPECIES_LEDYBA", "Ledyba"),
        ("SPECIES_LEDIAN", "Ledian"),
        ("SPECIES_SPINARAK", "Spinarak"),
        ("SPECIES_ARIADOS", "Ariados"),
        ("SPECIES_CROBAT", "Crobat"),
        ("SPECIES_CHINCHOU", "Chinchou"),
        ("SPECIES_LANTURN", "Lanturn"),
        ("SPECIES_PICHU", "Pichu"),
        ("SPECIES_CLEFFA", "Cleffa"),
        ("SPECIES_IGGLYBUFF", "Igglybuff"),
        ("SPECIES_TOGEPI", "Togepi"),
        ("SPECIES_TOGETIC", "Togetic"),
        ("SPECIES_NATU", "Natu"),
        ("SPECIES_XATU", "Xatu"),
        ("SPECIES_MAREEP", "Mareep"),
        ("SPECIES_FLAAFFY", "Flaafy"),
        ("SPECIES_AMPHAROS", "Ampharos"),
        ("SPECIES_BELLOSSOM", "Bellossom"),
        ("SPECIES_MARILL", "Marill"),
        ("SPECIES_AZUMARILL", "Azumarill"),
        ("SPECIES_SUDOWOODO", "Sudowoodo"),
        ("SPECIES_POLITOED", "Politoed"),
        ("SPECIES_HOPPIP", "Hoppip"),
        ("SPECIES_SKIPLOOM", "Skiploom"),
        ("SPECIES_JUMPLUFF", "Jumpluff"),
        ("SPECIES_AIPOM", "Aipom"),
        ("SPECIES_SUNKERN", "Sunkern"),
        ("SPECIES_SUNFLORA", "Sunflora"),
        ("SPECIES_YANMA", "Yanma"),
        ("SPECIES_WOOPER", "Wooper"),
        ("SPECIES_QUAGSIRE", "Quagsire"),
        ("SPECIES_ESPEON", "Espeon"),
        ("SPECIES_UMBREON", "Umbreon"),
        ("SPECIES_MURKROW", "Murkrow"),
        ("SPECIES_SLOWKING", "Slowking"),
        ("SPECIES_MISDREAVUS", "Misdreavus"),
        ("SPECIES_UNOWN", "Unown"),
        ("SPECIES_WOBBUFFET", "Wobbuffet"),
        ("SPECIES_GIRAFARIG", "Girafarig"),
        ("SPECIES_PINECO", "Pineco"),
        ("SPECIES_FORRETRESS", "Forretress"),
        ("SPECIES_DUNSPARCE", "Dunsparce"),
        ("SPECIES_GLIGAR", "Gligar"),
        ("SPECIES_STEELIX", "Steelix"),
        ("SPECIES_SNUBBULL", "Snubbull"),
        ("SPECIES_GRANBULL", "Granbull"),
        ("SPECIES_QWILFISH", "Qwilfish"),
        ("SPECIES_SCIZOR", "Scizor"),
        ("SPECIES_SHUCKLE", "Shuckle"),
        ("SPECIES_HERACROSS", "Heracross"),
        ("SPECIES_SNEASEL", "Sneasel"),
        ("SPECIES_TEDDIURSA", "Teddiursa"),
        ("SPECIES_URSARING", "Ursaring"),
        ("SPECIES_SLUGMA", "Slugma"),
        ("SPECIES_MAGCARGO", "Magcargo"),
        ("SPECIES_SWINUB", "Swinub"),
        ("SPECIES_PILOSWINE", "Piloswine"),
        ("SPECIES_CORSOLA", "Corsola"),
        ("SPECIES_REMORAID", "Remoraid"),
        ("SPECIES_OCTILLERY", "Octillery"),
        ("SPECIES_DELIBIRD", "Delibird"),
        ("SPECIES_MANTINE", "Mantine"),
        ("SPECIES_SKARMORY", "Skarmory"),
        ("SPECIES_HOUNDOUR", "Houndour"),
        ("SPECIES_HOUNDOOM", "Houndoom"),
        ("SPECIES_KINGDRA", "Kingdra"),
        ("SPECIES_PHANPY", "Phanpy"),
        ("SPECIES_DONPHAN", "Donphan"),
        ("SPECIES_PORYGON2", "Porygon2"),
        ("SPECIES_STANTLER", "Stantler"),
        ("SPECIES_SMEARGLE", "Smeargle"),
        ("SPECIES_TYROGUE", "Tyrogue"),
        ("SPECIES_HITMONTOP", "Hitmontop"),
        ("SPECIES_SMOOCHUM", "Smoochum"),
        ("SPECIES_ELEKID", "Elekid"),
        ("SPECIES_MAGBY", "Magby"),
        ("SPECIES_MILTANK", "Miltank"),
        ("SPECIES_BLISSEY", "Blissey"),
        ("SPECIES_RAIKOU", "Raikou"),
        ("SPECIES_ENTEI", "Entei"),
        ("SPECIES_SUICUNE", "Suicune"),
        ("SPECIES_LARVITAR", "Larvitar"),
        ("SPECIES_PUPITAR", "Pupitar"),
        ("SPECIES_TYRANITAR", "Tyranitar"),
        ("SPECIES_LUGIA", "Lugia"),
        ("SPECIES_HO_OH", "Ho-oh"),
        ("SPECIES_CELEBI", "Celebi"),
        ("SPECIES_TREECKO", "Treecko"),
        ("SPECIES_GROVYLE", "Grovyle"),
        ("SPECIES_SCEPTILE", "Sceptile"),
        ("SPECIES_TORCHIC", "Torchic"),
        ("SPECIES_COMBUSKEN", "Combusken"),
        ("SPECIES_BLAZIKEN", "Blaziken"),
        ("SPECIES_MUDKIP", "Mudkip"),
        ("SPECIES_MARSHTOMP", "Marshtomp"),
        ("SPECIES_SWAMPERT", "Swampert"),
        ("SPECIES_POOCHYENA", "Poochyena"),
        ("SPECIES_MIGHTYENA", "Mightyena"),
        ("SPECIES_ZIGZAGOON", "Zigzagoon"),
        ("SPECIES_LINOONE", "Linoon"),
        ("SPECIES_WURMPLE", "Wurmple"),
        ("SPECIES_SILCOON", "Silcoon"),
        ("SPECIES_BEAUTIFLY", "Beautifly"),
        ("SPECIES_CASCOON", "Cascoon"),
        ("SPECIES_DUSTOX", "Dustox"),
        ("SPECIES_LOTAD", "Lotad"),
        ("SPECIES_LOMBRE", "Lombre"),
        ("SPECIES_LUDICOLO", "Ludicolo"),
        ("SPECIES_SEEDOT", "Seedot"),
        ("SPECIES_NUZLEAF", "Nuzleaf"),
        ("SPECIES_SHIFTRY", "Shiftry"),
        ("SPECIES_NINCADA", "Nincada"),
        ("SPECIES_NINJASK", "Ninjask"),
        ("SPECIES_SHEDINJA", "Shedinja"),
        ("SPECIES_TAILLOW", "Taillow"),
        ("SPECIES_SWELLOW", "Swellow"),
        ("SPECIES_SHROOMISH", "Shroomish"),
        ("SPECIES_BRELOOM", "Breloom"),
        ("SPECIES_SPINDA", "Spinda"),
        ("SPECIES_WINGULL", "Wingull"),
        ("SPECIES_PELIPPER", "Pelipper"),
        ("SPECIES_SURSKIT", "Surskit"),
        ("SPECIES_MASQUERAIN", "Masquerain"),
        ("SPECIES_WAILMER", "Wailmer"),
        ("SPECIES_WAILORD", "Wailord"),
        ("SPECIES_SKITTY", "Skitty"),
        ("SPECIES_DELCATTY", "Delcatty"),
        ("SPECIES_KECLEON", "Kecleon"),
        ("SPECIES_BALTOY", "Baltoy"),
        ("SPECIES_CLAYDOL", "Claydol"),
        ("SPECIES_NOSEPASS", "Nosepass"),
        ("SPECIES_TORKOAL", "Torkoal"),
        ("SPECIES_SABLEYE", "Sableye"),
        ("SPECIES_BARBOACH", "Barboach"),
        ("SPECIES_WHISCASH", "Whiscash"),
        ("SPECIES_LUVDISC", "Luvdisc"),
        ("SPECIES_CORPHISH", "Corphish"),
        ("SPECIES_CRAWDAUNT", "Crawdaunt"),
        ("SPECIES_FEEBAS", "Feebas"),
        ("SPECIES_MILOTIC", "Milotic"),
        ("SPECIES_CARVANHA", "Carvanha"),
        ("SPECIES_SHARPEDO", "Sharpedo"),
        ("SPECIES_TRAPINCH", "Trapinch"),
        ("SPECIES_VIBRAVA", "Vibrava"),
        ("SPECIES_FLYGON", "Flygon"),
        ("SPECIES_MAKUHITA", "Makuhita"),
        ("SPECIES_HARIYAMA", "Hariyama"),
        ("SPECIES_ELECTRIKE", "Electrike"),
        ("SPECIES_MANECTRIC", "Manectric"),
        ("SPECIES_NUMEL", "Numel"),
        ("SPECIES_CAMERUPT", "Camerupt"),
        ("SPECIES_SPHEAL", "Spheal"),
        ("SPECIES_SEALEO", "Sealeo"),
        ("SPECIES_WALREIN", "Walrein"),
        ("SPECIES_CACNEA", "Cacnea"),
        ("SPECIES_CACTURNE", "Cacturne"),
        ("SPECIES_SNORUNT", "Snorunt"),
        ("SPECIES_GLALIE", "Glalie"),
        ("SPECIES_LUNATONE", "Lunatone"),
        ("SPECIES_SOLROCK", "Solrock"),
        ("SPECIES_AZURILL", "Azurill"),
        ("SPECIES_SPOINK", "Spoink"),
        ("SPECIES_GRUMPIG", "Grumpig"),
        ("SPECIES_PLUSLE", "Plusle"),
        ("SPECIES_MINUN", "Minun"),
        ("SPECIES_MAWILE", "Mawile"),
        ("SPECIES_MEDITITE", "Meditite"),
        ("SPECIES_MEDICHAM", "Medicham"),
        ("SPECIES_SWABLU", "Swablu"),
        ("SPECIES_ALTARIA", "Altaria"),
        ("SPECIES_WYNAUT", "Wynaut"),
        ("SPECIES_DUSKULL", "Duskull"),
        ("SPECIES_DUSCLOPS", "Dusclops"),
        ("SPECIES_ROSELIA", "Roselia"),
        ("SPECIES_SLAKOTH", "Slakoth"),
        ("SPECIES_VIGOROTH", "Vigoroth"),
        ("SPECIES_SLAKING", "Slaking"),
        ("SPECIES_GULPIN", "Gulpin"),
        ("SPECIES_SWALOT", "Swalot"),
        ("SPECIES_TROPIUS", "Tropius"),
        ("SPECIES_WHISMUR", "Whismur"),
        ("SPECIES_LOUDRED", "Loudred"),
        ("SPECIES_EXPLOUD", "Exploud"),
        ("SPECIES_CLAMPERL", "Clamperl"),
        ("SPECIES_HUNTAIL", "Huntail"),
        ("SPECIES_GOREBYSS", "Gorebyss"),
        ("SPECIES_ABSOL", "Absol"),
        ("SPECIES_SHUPPET", "Shuppet"),
        ("SPECIES_BANETTE", "Banette"),
        ("SPECIES_SEVIPER", "Seviper"),
        ("SPECIES_ZANGOOSE", "Zangoose"),
        ("SPECIES_RELICANTH", "Relicanth"),
        ("SPECIES_ARON", "Aron"),
        ("SPECIES_LAIRON", "Lairon"),
        ("SPECIES_AGGRON", "Aggron"),
        ("SPECIES_CASTFORM", "Castform"),
        ("SPECIES_VOLBEAT", "Volbeat"),
        ("SPECIES_ILLUMISE", "Illumise"),
        ("SPECIES_LILEEP", "Lileep"),
        ("SPECIES_CRADILY", "Cradily"),
        ("SPECIES_ANORITH", "Anorith"),
        ("SPECIES_ARMALDO", "Armaldo"),
        ("SPECIES_RALTS", "Ralts"),
        ("SPECIES_KIRLIA", "Kirlia"),
        ("SPECIES_GARDEVOIR", "Gardevoir"),
        ("SPECIES_BAGON", "Bagon"),
        ("SPECIES_SHELGON", "Shelgon"),
        ("SPECIES_SALAMENCE", "Salamence"),
        ("SPECIES_BELDUM", "Beldum"),
        ("SPECIES_METANG", "Metang"),
        ("SPECIES_METAGROSS", "Metagross"),
        ("SPECIES_REGIROCK", "Regirock"),
        ("SPECIES_REGICE", "Regice"),
        ("SPECIES_REGISTEEL", "Registeel"),
        ("SPECIES_KYOGRE", "Kyogre"),
        ("SPECIES_GROUDON", "Groudon"),
        ("SPECIES_RAYQUAZA", "Rayquaza"),
        ("SPECIES_LATIAS", "Latias"),
        ("SPECIES_LATIOS", "Latios"),
        ("SPECIES_JIRACHI", "Jirachi"),
        ("SPECIES_DEOXYS", "Deoxys"),
        ("SPECIES_CHIMECHO", "Chimecho")
    ]

    species_list: List[SpeciesData] = []
    max_species_id = 0
    for species_name, species_label in all_species:
        species_id = data.constants[species_name]
        max_species_id = max(species_id, max_species_id)
        species_data = extracted_data["species"][species_id]

        learnset = [LearnsetMove(item["level"], item["move_id"]) for item in species_data["learnset"]["moves"]]

        species_list.append(SpeciesData(
            species_name,
            species_label,
            species_id,
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
            learnset,
            int(species_data["tmhm_learnset"], 16),
            species_data["learnset"]["rom_address"],
            species_data["rom_address"]
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
            static_encounter_json["rom_address"]
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
    for warp, destination in extracted_data["warps"].items():
        data.warp_map[warp] = None if destination == "" else destination

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
