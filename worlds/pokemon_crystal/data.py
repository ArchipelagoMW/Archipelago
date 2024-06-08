import orjson
import pkgutil
from typing import Dict, List, NamedTuple, Set, FrozenSet, Any, Union

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
    script: str


class EventData(NamedTuple):
    name: str
    parent_region: str


class RegionData:
    name: str
    johto: bool
    silver_cave: bool
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


class EvolutionData(NamedTuple):
    evo_type: str
    level: Union[int, None]
    condition: Union[str, None]
    pokemon: str
    length: int


class PokemonData(NamedTuple):
    id: int
    base_stats: List[int]
    types: List[str]
    evolutions: List[EvolutionData]
    learnset: List[LearnsetData]
    tm_hm: List[str]
    is_base: bool
    bst: int


class MoveData(NamedTuple):
    id: int
    type: str
    power: int
    accuracy: int
    pp: int
    is_hm: bool
    name: str


class TMHMData(NamedTuple):
    tm_num: int
    type: str
    is_hm: bool
    move_id: int


class TrainerPokemon(NamedTuple):
    level: int
    pokemon: str
    item: Union[str, None]
    moves: List[str]


class TrainerData(NamedTuple):
    trainer_type: str
    pokemon: List[TrainerPokemon]
    name_length: int


class MiscWarp(NamedTuple):
    coords: List[int]
    id: int


class MiscSaffronWarps(NamedTuple):
    warps: Dict[str, MiscWarp]
    pairs: List[List[str]]


class MiscData(NamedTuple):
    fuchsia_gym_trainers: List[List[int]]
    radio_tower_questions: List[str]
    saffron_gym_warps: MiscSaffronWarps
    ecruteak_gym_warps: List[List[List[int]]]


class BankAddress(NamedTuple):
    bank: int
    address: int


class SfxData(NamedTuple):
    pointers: List[BankAddress]
    cries: Dict[str, int]


class MusicData(NamedTuple):
    consts: Dict[str, int]
    maps: List[str]


class EncounterMon(NamedTuple):
    level: int
    pokemon: str


class FishData(NamedTuple):
    old: List[EncounterMon]
    good: List[EncounterMon]
    super: List[EncounterMon]


class TreeMonData(NamedTuple):
    common: List[EncounterMon]
    rare: List[EncounterMon]


class WildData(NamedTuple):
    grass: Dict[str, List[EncounterMon]]
    water: Dict[str, List[EncounterMon]]
    fish: Dict[str, FishData]
    tree: Dict[str, TreeMonData]


class StaticPokemon(NamedTuple):
    pokemon: str
    addresses: List[str]


class PokemonCrystalData:
    rom_version: int
    rom_addresses: Dict[str, int]
    ram_addresses: Dict[str, int]
    event_flags: Dict[str, int]
    regions: Dict[str, RegionData]
    locations: Dict[str, LocationData]
    items: Dict[int, ItemData]
    trainers: Dict[str, TrainerData]
    pokemon: Dict[str, PokemonData]
    moves: Dict[str, MoveData]
    wild: WildData
    types: List[str]
    type_ids: Dict[str, int]
    tmhm: Dict[str, TMHMData]
    tm_replace_map: List[int]
    misc: MiscData
    sfx: SfxData
    music: MusicData
    static: Dict[str, StaticPokemon]

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
    return orjson.loads(pkgutil.get_data(__name__, "data/" + data_name).decode('utf-8-sig'))


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
    move_data = data_json["moves"]
    trainer_data = data_json["trainers"]
    wild_data = data_json["wilds"]
    type_data = data_json["types"]
    fuchsia_data = data_json["misc"]["fuchsia_gym_trainers"]
    saffron_data = data_json["misc"]["saffron_gym_warps"]
    ecruteak_data = data_json["misc"]["ecruteak_gym_warps"]
    tmhm_data = data_json["tmhm"]

    data.rom_version = data_json["rom_version"]

    claimed_locations: Set[str] = set()

    data.regions = {}

    for region_name, region_json in regions_json.items():
        new_region = RegionData(region_name)

        # Locations
        for location_name in region_json["locations"]:
            if location_name in claimed_locations:
                raise AssertionError(f"Location [{location_name}] was claimed by multiple regions")
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
        new_region.johto = region_json["johto"]
        new_region.silver_cave = region_json["silver_cave"] if "silver_cave" in region_json else False
        data.regions[region_name] = new_region

    # items

    data.items = {}
    data.tm_replace_map = []
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
        if attributes["name"].startswith("TM") and item_constant_name != "TM_ROCK_SMASH":
            tm_num = attributes["name"][2:4]
            data.items[item_codes[item_constant_name] + 256] = ItemData(
                "TM" + tm_num,
                item_codes[item_constant_name],
                "TM_" + tm_num,
                item_classification,
                frozenset(attributes["tags"])
            )
            data.tm_replace_map.append(item_codes[item_constant_name] + BASE_OFFSET)

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
        evolutions = []
        for evo in pokemon_data["evolutions"]:
            if len(evo) == 4:
                evolutions.append(EvolutionData(evo[0], int(evo[1]), evo[2], evo[3], len(evo)))
            elif evo[0] == "EVOLVE_LEVEL":
                evolutions.append(EvolutionData(evo[0], int(evo[1]), None, evo[2], len(evo)))
            else:
                evolutions.append(EvolutionData(evo[0], None, evo[1], evo[2], len(evo)))
        data.pokemon[pokemon_name] = PokemonData(
            pokemon_data["id"],
            pokemon_data["base_stats"],
            pokemon_data["types"],
            evolutions,
            [LearnsetData(move[0], move[1]) for move in pokemon_data["learnset"]],
            pokemon_data["tm_hm"],
            pokemon_data["is_base"],
            pokemon_data["bst"]
        )

    data.moves = {}
    for move_name, move_attributes in move_data.items():
        data.moves[move_name] = MoveData(
            move_attributes["id"],
            move_attributes["type"],
            move_attributes["power"],
            move_attributes["accuracy"],
            move_attributes["pp"],
            move_attributes["is_hm"],
            move_attributes["name"],
        )

    data.trainers = {}
    for trainer_name, trainer_attributes in trainer_data.items():
        trainer_type = trainer_attributes["trainer_type"]
        pokemon = []
        for poke in trainer_attributes["pokemon"]:
            if trainer_type == "TRAINERTYPE_NORMAL":
                pokemon.append(TrainerPokemon(int(poke[0]), poke[1], None, []))
            elif trainer_type == "TRAINERTYPE_ITEM":
                pokemon.append(TrainerPokemon(int(poke[0]), poke[1], poke[2], []))
            elif trainer_type == "TRAINERTYPE_MOVES":
                pokemon.append(TrainerPokemon(int(poke[0]), poke[1], None, poke[2:]))
            else:
                pokemon.append(TrainerPokemon(int(poke[0]), poke[1], poke[2], poke[3:]))

        data.trainers[trainer_name] = TrainerData(
            trainer_type,
            pokemon,
            trainer_attributes["name_length"]
        )

    grass_dict = {}
    for grass_name, grass_data in wild_data["grass"].items():
        encounter_list = []
        for pkmn in grass_data:
            grass_encounter = EncounterMon(int(pkmn["level"]), pkmn["pokemon"])
            encounter_list.append(grass_encounter)
        grass_dict[grass_name] = encounter_list

    water_dict = {}
    for water_name, water_data in wild_data["water"].items():
        encounter_list = []
        for pkmn in water_data:
            water_encounter = EncounterMon(int(pkmn["level"]), pkmn["pokemon"])
            encounter_list.append(water_encounter)
        water_dict[water_name] = encounter_list

    fish_dict = {}
    for fish_name, fish_data in wild_data["fish"].items():
        old_encounters = []
        good_encounters = []
        super_encounters = []
        for pkmn in fish_data["Old"]:
            new_encounter = EncounterMon(int(pkmn["level"]), pkmn["pokemon"])
            old_encounters.append(new_encounter)
        for pkmn in fish_data["Good"]:
            new_encounter = EncounterMon(int(pkmn["level"]), pkmn["pokemon"])
            good_encounters.append(new_encounter)
        for pkmn in fish_data["Super"]:
            new_encounter = EncounterMon(int(pkmn["level"]), pkmn["pokemon"])
            super_encounters.append(new_encounter)

        fish_dict[fish_name] = FishData(
            old_encounters,
            good_encounters,
            super_encounters
        )

    tree_dict = {}
    for tree_name, tree_data in wild_data["tree"].items():
        common_list = []
        rare_list = []
        for pkmn in tree_data["common"]:
            tree_encounter = EncounterMon(int(pkmn["level"]), pkmn["pokemon"])
            common_list.append(tree_encounter)
        if "rare" in tree_data:
            for pkmn in tree_data["rare"]:
                tree_encounter = EncounterMon(int(pkmn["level"]), pkmn["pokemon"])
                rare_list.append(tree_encounter)
        tree_dict[tree_name] = TreeMonData(common_list, rare_list)

    data.wild = WildData(grass_dict, water_dict, fish_dict, tree_dict)

    saffron_warps = {}
    # print(sa_data)
    for warp_name, warp_data in saffron_data["warps"].items():
        saffron_warps[warp_name] = MiscWarp(warp_data["coords"], warp_data["id"])

    radio_tower_data = ["Y", "Y", "N", "Y", "N"]
    data.misc = MiscData(fuchsia_data, radio_tower_data, MiscSaffronWarps(saffron_warps, saffron_data["pairs"]),
                         ecruteak_data)

    data.types = type_data["types"]
    data.type_ids = type_data["ids"]

    data.tmhm = {}
    for tm_name, tm_data in tmhm_data.items():
        data.tmhm[tm_name] = TMHMData(
            tm_data["tm_num"],
            tm_data["type"],
            tm_data["is_hm"],
            move_data[tm_name]["id"]
        )

    sfx_pointers = []
    for sfx in data_json["sfx"]["pointers"]:
        sfx_pointers.append(BankAddress(sfx[0], sfx[1]))

    sfx_cries = {}

    for cry_name, cry in data_json["sfx"]["cries"].items():
        sfx_cries[cry_name] = cry

    data.sfx = SfxData(sfx_pointers, sfx_cries)

    music_consts = {}
    for music_name, music_id in data_json["music"]["consts"].items():
        music_consts[music_name] = music_id

    data.music = MusicData(music_consts, data_json["music"]["maps"])

    data.static = {
        "UnionCaveLapras": StaticPokemon("LAPRAS", [
            "AP_Static_UnionCaveLapras_1",
            "AP_Static_UnionCaveLapras_2"]),
        "EggTogepi": StaticPokemon("TOGEPI", ["AP_Static_Togepi"]),
        "RocketHQTrap1": StaticPokemon("VOLTORB", ["AP_Static_RocketHQTrap_1"]),
        "RocketHQTrap2": StaticPokemon("GEODUDE", ["AP_Static_RocketHQTrap_2"]),
        "RocketHQTrap3": StaticPokemon("KOFFING", ["AP_Static_RocketHQTrap_3"]),
        "RocketHQElectrode1": StaticPokemon("ELECTRODE",
                                            ["AP_Static_RocketHQElectrode_1_1", "AP_Static_RocketHQElectrode_1_2", ]),
        "RocketHQElectrode2": StaticPokemon("ELECTRODE",
                                            ["AP_Static_RocketHQElectrode_2_1", "AP_Static_RocketHQElectrode_2_2", ]),
        "RocketHQElectrode3": StaticPokemon("ELECTRODE",
                                            ["AP_Static_RocketHQElectrode_3_1", "AP_Static_RocketHQElectrode_3_2", ]),
        "RedGyarados": StaticPokemon("GYARADOS", ["AP_Static_RedGyarados_1",
                                                  "AP_Static_RedGyarados_2", ]),
        "Ho_Oh": StaticPokemon("HO_OH", ["AP_Static_Ho_Oh_1",
                                         "AP_Static_Ho_Oh_2", ]),
        "Suicune": StaticPokemon("SUICUNE", ["AP_Static_Suicune_1",
                                             "AP_Static_Suicune_2",
                                             "AP_Static_Suicune_3",
                                             "AP_Static_Suicune_4"]),
        "Lugia": StaticPokemon("LUGIA", ["AP_Static_Lugia_1",
                                         "AP_Static_Lugia_2", ]),
        "Raikou": StaticPokemon("RAIKOU", ["AP_Static_Raikou_1",
                                           "AP_Static_Raikou_2",
                                           "AP_Static_Raikou_3",
                                           "AP_Static_Raikou_4",
                                           "AP_Static_Raikou_5", ]),
        "Entei": StaticPokemon("ENTEI", ["AP_Static_Entei_1",
                                         "AP_Static_Entei_2",
                                         "AP_Static_Entei_3",
                                         "AP_Static_Entei_4",
                                         "AP_Static_Entei_5", ]),
        "Sudowoodo": StaticPokemon("SUDOWOODO", ["AP_Static_Sudowoodo", ]),
        "Snorlax": StaticPokemon("SNORLAX", ["AP_Static_Snorlax_1",
                                             "AP_Static_Snorlax_2"]),
        "CatchTutorial1": StaticPokemon("RATATTA", ["AP_Static_CatchTutorial_1", ]),
        "CatchTutorial2": StaticPokemon("RATATTA", ["AP_Static_CatchTutorial_2", ]),
        "CatchTutorial3": StaticPokemon("RATATTA", ["AP_Static_CatchTutorial_3", ])
    }


_init()
