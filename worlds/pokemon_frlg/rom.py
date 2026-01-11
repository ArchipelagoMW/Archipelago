"""
Classes and functions related to creating a ROM patch
"""
import bsdiff4
import struct
from typing import TYPE_CHECKING, Dict, List, Tuple

from worlds.Files import APPatchExtension, APProcedurePatch, APTokenMixin, APTokenTypes
from settings import get_settings
from .data import data, APWORLD_VERSION, GAME_OPTIONS, EvolutionMethodEnum, TrainerPokemonDataTypeEnum
from.groups import location_groups
from .items import is_single_purchase_item
from .locations import PokemonFRLGLocation
from .options import (CardKey, Dexsanity, FlashRequired, ForceFullyEvolved, IslandPasses, ItemfinderRequired,
                      HmCompatibility, LevelScaling, RandomizeDamageCategories, RandomizeLegendaryPokemon,
                      RandomizeMiscPokemon, RandomizeMoveTypes, RandomizeStarters, RandomizeTrainerParties,
                      RandomizeWildPokemon, ShopPrices, ShuffleFlyUnlocks, ShuffleHiddenItems, TmTutorCompatibility,
                      Trainersanity, ViridianCityRoadblock)
from .pokemon import randomize_tutor_moves
from .util import bool_array_to_int, bound, encode_string

if TYPE_CHECKING:
    from . import PokemonFRLGWorld

FIRERED_REV0_HASH = "e26ee0d44e809351c8ce2d73c7400cdd"
FIRERED_REV1_HASH = "51901a6e40661b3914aa333c802e24e8"
LEAFGREEN_REV0_HASH = "612ca9473451fa42b51d1711031ed5f6"
LEAFGREEN_REV1_HASH = "9d33a02159e018d09073e700e1fd10fd"

_LOOPING_MUSIC = [
    "MUS_RS_VS_GYM_LEADER", "MUS_RS_VS_TRAINER", "MUS_SCHOOL", "MUS_FOLLOW_ME", "MUS_GAME_CORNER", "MUS_ROCKET_HIDEOUT",
    "MUS_GYM", "MUS_CINNABAR", "MUS_LAVENDER", "MUS_CYCLING", "MUS_ENCOUNTER_ROCKET", "MUS_ENCOUNTER_GIRL",
    "MUS_ENCOUNTER_BOY", "MUS_HALL_OF_FAME", "MUS_VIRIDIAN_FOREST", "MUS_MT_MOON", "MUS_POKE_MANSION", "MUS_ROUTE1",
    "MUS_ROUTE24", "MUS_ROUTE3", "MUS_ROUTE11", "MUS_VICTORY_ROAD", "MUS_VS_GYM_LEADER", "MUS_VS_TRAINER",
    "MUS_VS_WILD", "MUS_VS_CHAMPION", "MUS_PALLET", "MUS_OAK_LAB", "MUS_OAK", "MUS_POKE_CENTER", "MUS_SS_ANNE",
    "MUS_SURF", "MUS_POKE_TOWER", "MUS_SILPH", "MUS_FUCHSIA", "MUS_CELADON", "MUS_VICTORY_TRAINER", "MUS_VICTORY_WILD",
    "MUS_VICTORY_GYM_LEADER", "MUS_VERMILLION", "MUS_PEWTER", "MUS_ENCOUNTER_RIVAL", "MUS_RIVAL_EXIT", "MUS_CAUGHT",
    "MUS_POKE_JUMP", "MUS_UNION_ROOM", "MUS_NET_CENTER", "MUS_MYSTERY_GIFT", "MUS_BERRY_PICK", "MUS_SEVII_CAVE",
    "MUS_TEACHY_TV_SHOW", "MUS_SEVII_ROUTE", "MUS_SEVII_DUNGEON", "MUS_SEVII_123", "MUS_SEVII_45", "MUS_SEVII_67",
    "MUS_VS_DEOXYS", "MUS_VS_MEWTWO", "MUS_VS_LEGEND", "MUS_ENCOUNTER_GYM_LEADER", "MUS_ENCOUNTER_DEOXYS",
    "MUS_TRAINER_TOWER", "MUS_SLOW_PALLET", "MUS_TEACHY_TV_MENU"
]

_FANFARES: Dict[str, int] = {
    "MUS_LEVEL_UP": 80,
    "MUS_OBTAIN_ITEM": 160,
    "MUS_EVOLVED": 220,
    "MUS_OBTAIN_TMHM": 220,
    "MUS_HEAL": 160,
    "MUS_OBTAIN_BADGE": 340,
    "MUS_MOVE_DELETED": 180,
    "MUS_OBTAIN_BERRY": 120,
    "MUS_SLOTS_JACKPOT": 250,
    "MUS_SLOTS_WIN": 150,
    "MUS_TOO_BAD": 160,
    "MUS_POKE_FLUTE": 450,
    "MUS_OBTAIN_KEY_ITEM": 170,
    "MUS_DEX_RATING": 196
}


class PokemonFRLGPatchExtension(APPatchExtension):
    game = "Pokemon FireRed and LeafGreen"

    @staticmethod
    def apply_bsdiff4(caller: APProcedurePatch, rom: bytes, patch: str) -> bytes:
        rom_data = bytearray(rom)
        if rom_data[0xBC] == 1:
            return bsdiff4.patch(rom, caller.get_file("base_patch_rev1.bsdiff4"))
        return bsdiff4.patch(rom, caller.get_file(patch))

    @staticmethod
    def apply_tokens(caller: APProcedurePatch, rom: bytes, token_file: str) -> bytes:
        rom_data = bytearray(rom)
        if rom_data[0xBC] == 1:
            token_data = caller.get_file("token_data_rev1.bin")
        else:
            token_data = caller.get_file(token_file)
        token_count = int.from_bytes(token_data[0:4], "little")
        bpr = 4
        for _ in range(token_count):
            token_type = token_data[bpr:bpr + 1][0]
            offset = int.from_bytes(token_data[bpr + 1:bpr + 5], "little")
            size = int.from_bytes(token_data[bpr + 5:bpr + 9], "little")
            data = token_data[bpr + 9:bpr + 9 + size]
            if token_type in [APTokenTypes.AND_8, APTokenTypes.OR_8, APTokenTypes.XOR_8]:
                arg = data[0]
                if token_type == APTokenTypes.AND_8:
                    rom_data[offset] = rom_data[offset] & arg
                elif token_type == APTokenTypes.OR_8:
                    rom_data[offset] = rom_data[offset] | arg
                else:
                    rom_data[offset] = rom_data[offset] ^ arg
            elif token_type in [APTokenTypes.COPY, APTokenTypes.RLE]:
                length = int.from_bytes(data[:4], "little")
                value = int.from_bytes(data[4:], "little")
                if token_type == APTokenTypes.COPY:
                    rom_data[offset: offset + length] = rom_data[value: value + length]
                else:
                    rom_data[offset: offset + length] = bytes([value] * length)
            else:
                rom_data[offset:offset + len(data)] = data
            bpr += 9 + size
        return bytes(rom_data)


class PokemonFireRedProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Pokemon FireRed and LeafGreen"
    hash = [FIRERED_REV0_HASH, FIRERED_REV1_HASH]
    patch_file_ending = ".apfirered"
    result_file_ending = ".gba"

    procedure = [
        ("apply_bsdiff4", ["base_patch_rev0.bsdiff4"]),
        ("apply_tokens", ["token_data_rev0.bin"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_settings().pokemon_frlg_settings.firered_rom_file, "rb") as infile:
            base_rom_bytes = bytes(infile.read())
        return base_rom_bytes


class PokemonLeafGreenProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Pokemon FireRed and LeafGreen"
    hash = [LEAFGREEN_REV0_HASH, LEAFGREEN_REV1_HASH]
    patch_file_ending = ".apleafgreen"
    result_file_ending = ".gba"

    procedure = [
        ("apply_bsdiff4", ["base_patch_rev0.bsdiff4"]),
        ("apply_tokens", ["token_data_rev0.bin"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_settings().pokemon_frlg_settings.leafgreen_rom_file, "rb") as infile:
            base_rom_bytes = bytes(infile.read())
        return base_rom_bytes


class PokemonFRLGPatchData:
    tokens: Dict[str, APTokenMixin]
    game_version: str
    revision_keys: List[str]

    def __init__(self) -> None:
        self.tokens = {}
        self.game_version = ""
        self.revision_keys = []
        self.token_data = []

    def set_game_version(self, game_version: str) -> None:
        self.game_version = game_version
        self.revision_keys.append(game_version)
        self.revision_keys.append(f"{game_version}_rev1")
        for key in self.revision_keys:
            self.tokens[key] = APTokenMixin()

    def write_token(self,
                    addresses: Dict[str, int | List[int]],
                    offset: int,
                    data: bytes | Tuple[int, int] | int) -> None:
        for key in self.revision_keys:
            address = addresses[key]
            if type(address) is int:
                self.tokens[key].write_token(APTokenTypes.WRITE, address + offset, data)
            elif type(address) is list:
                for addr in address:
                    self.tokens[key].write_token(APTokenTypes.WRITE, addr + offset, data)

    def get_rev_token_bytes(self, key: str) -> bytes:
        return self.tokens[key].get_token_binary()


def write_tokens(world: "PokemonFRLGWorld") -> None:
    patch = world.patch_data

    # Set item values
    location_info: List[Tuple[int, int, str]] = []
    for location in world.get_locations():
        assert isinstance(location, PokemonFRLGLocation)
        if location.address is None:
            continue
        if location.item is None:
            continue

        item_address = location.item_address

        if not world.options.remote_items and location.item.player == world.player:
            item_id = location.item.code
        else:
            item_id = data.constants["ITEM_ARCHIPELAGO_PROGRESSION"]

        patch.write_token(item_address, 0, struct.pack("<H", item_id))

        # Creates a list of item information to store in tables later. Those tables are used to display the item and
        # player name in a text box. In the case of not enough space, the game will default to "found an ARCHIPELAGO
        # ITEM"
        location_info.append((location.address, location.item.player, location.item.name))

    if world.options.trainersanity:
        rival_rewards = ["RIVAL_OAKS_LAB", "RIVAL_ROUTE22_EARLY", "RIVAL_CERULEAN", "RIVAL_SS_ANNE",
                         "RIVAL_POKEMON_TOWER", "RIVAL_SILPH", "RIVAL_ROUTE22_LATE", "CHAMPION_FIRST"]
        if not world.options.kanto_only:
            rival_rewards.append("CHAMPION_REMATCH")
        for trainer in rival_rewards:
            try:
                location = world.get_location(data.locations[f"TRAINER_{trainer}_BULBASAUR_REWARD"].name)
                alternates = [f"TRAINER_{trainer}_CHARMANDER", f"TRAINER_{trainer}_SQUIRTLE"]
                location_info.extend(
                    (
                        data.constants["TRAINER_FLAGS_START"] + data.constants[alternate],
                        location.item.player,
                        location.item.name
                    ) for alternate in alternates)
            except KeyError:
                continue

    player_name_ids: Dict[str, int] = {world.player_name: 0}
    player_name_address = data.rom_addresses["gArchipelagoPlayerNames"]
    for j, b in enumerate(encode_string(world.player_name, 17)):
        patch.write_token(player_name_address,
                          j,
                          struct.pack("<B", b))
    item_name_offsets: Dict[str, int] = {}
    item_name_address = data.rom_addresses["gArchipelagoItemNames"]
    next_item_name_offset = 0
    name_table_address = data.rom_addresses["gArchipelagoNameTable"]
    for i, (flag, item_player, item_name) in enumerate(sorted(location_info, key=lambda t: t[0])):
        player_name = world.multiworld.get_player_name(item_player)

        if player_name not in player_name_ids:
            # Only space for 1000 player names
            if len(player_name_ids) >= 1000:
                continue

            player_name_ids[player_name] = len(player_name_ids)
            for j, b in enumerate(encode_string(player_name, 17)):
                patch.write_token(player_name_address,
                                  (player_name_ids[player_name] * 17) + j,
                                  struct.pack("<B", b))

        if item_name not in item_name_offsets:
            if len(item_name) > 35:
                item_name = item_name[:34] + "…"

            # Only 36 * 2000 bytes for item names
            if next_item_name_offset + len(item_name) + 1 > 36 * 2000:
                continue

            item_name_offsets[item_name] = next_item_name_offset
            next_item_name_offset += len(item_name) + 1
            patch.write_token(item_name_address, item_name_offsets[item_name], encode_string(item_name) + b"\xFF")

        # There should always be enough space for one entry per location
        patch.write_token(name_table_address, (i * 5) + 0, struct.pack("<H", flag))
        patch.write_token(name_table_address, (i * 5) + 2, struct.pack("<H", item_name_offsets[item_name]))
        patch.write_token(name_table_address, (i * 5) + 4, struct.pack("<H", player_name_ids[player_name]))

    # Set starting items
    start_inventory = world.options.start_inventory.value.copy()

    starting_items: List[Tuple[str, int]] = []
    for item, quantity in start_inventory.items():
        if "Unique" in data.items[world.item_name_to_id[item]].tags:
            quantity = 1
        if quantity > 999:
            quantity = 999
        starting_items.append((item, quantity))

    for i, starting_item in enumerate(starting_items, 1):
        item_address = data.rom_addresses["gArchipelagoStartingItems"]
        count_address = data.rom_addresses["gArchipelagoStartingItemsCount"]
        item = world.item_name_to_id[starting_item[0]]
        patch.write_token(item_address, (i * 2), struct.pack("<H", item))
        patch.write_token(count_address, (i * 2), struct.pack("<H", starting_item[1]))

    # Set shuffled entrances
    _set_shuffled_entrances(world)

    # Set randomized fly destinations
    _set_randomized_fly_destinations(world)

    # Set shop data
    _set_shop_data(world)

    # Set species data
    _set_species_info(world)

    # Set wild encounters
    _set_wild_encounters(world)

    # Set starters
    _set_starters(world)

    # Set legendaries
    _set_legendaries(world)

    # Set misc Pokémon
    _set_misc_pokemon(world)

    # Set trade Pokémon
    _set_trade_pokemon(world)

    # Set trainer parties
    _set_trainer_parties(world)

    # Set TM/HM compatibility
    _set_tmhm_compatibility(world)

    # Set TM Moves
    _set_tm_moves(world)

    # Randomize move tutors
    _randomize_move_tutors(world)

    # Set types damage catagories
    _set_types_damage_categories(world)

    # Set moves
    _set_moves(world)

    # Options
    # struct
    # ArchipelagoOptions
    # {
    # /* 0x00 */ u8 windowFrameType;
    # /* 0x01 */ u16 expMultiplier;
    # /* 0x03 */ u16 textSpeedOption:2; // 0 = Slow, 1 = Mid, 2 = Fast, 3 = Instant
    #            u16 turboA:2; // 0 = Off, 1 = A, 2 = B, 3 = A/B
    #            u16 autoRun:1;
    #            u16 buttonMode:2; // 0 = Help, 1 = L/R, 2 = L=A
    #            u16 battleScene:1;
    #            u16 battleStyle:1; // 0 = Shift, 1 = Set
    #            u16 showEffectiveness:1;
    #            u16 expDistribution:2; // 0 = Gen III, 1 = Gen VI, 2 = Gen VIII
    #            u16 sound:1; // 0 = Mono, 1 = Stereo
    #            u16 lowHPBeep:1;
    #            u16 skipFanfares:1;
    #            u16 bikeMusic:1;
    # /* 0x05 */ u16 surfMusic:1;
    #            u16 guaranteedCatch:1;
    #            u16 guaranteedRun:1;
    #            u16 normalizeEncounterRates:1;
    #            u16 blindTrainers:1;
    #            u16 skipNicknames:1;
    #            u16 itemMessages:2; // 0 = Show All, 1 = Show Progression Only, 2 = Show None
    # /* 0x06 */ bool8 betterShopsEnabled;
    # /* 0x07 */ bool8 reusableTms;
    # /* 0x08 */ bool8 unlockSeenDexInfo;
    # /* 0x09 */ bool8 physicalSpecialSplit;
    #
    # /* 0x0A */ bool8 openViridianCity;
    # /* 0x0B */ u8 route3Requirement; // 0 = Open, 1 = Defeat Brock, 2 = Defeat Any Gym Leader,
    #                                     3 = Boulder Badge, 4 = Any Badge
    # /* 0x0C */ bool8 openCeruleanCity;
    # /* 0x0D */ bool8 modifyRoute2;
    # /* 0x0E */ bool8 modifyRoute9;
    # /* 0x0F */ bool8 blockUndergroundTunnels;
    # /* 0x10 */ bool8 route12Boulders;
    # /* 0x11 */ bool8 modifyRoute10;
    # /* 0x12 */ bool8 modifyRoute12;
    # /* 0x13 */ bool8 modifyRoute16;
    # /* 0x14 */ bool8 openSilphCo;
    # /* 0x15 */ bool8 removeSaffronRockets;
    # /* 0x16 */ bool8 modifyRoute23;
    # /* 0x17 */ bool8 route23Trees;
    # /* 0x18 */ bool8 blockPokemonTower;
    # /* 0x19 */ bool8 victoryRoadRocks;
    # /* 0x1A */ bool8 earlyFameGossip;
    # /* 0x1B */ bool8 blockVermilionSailing;
    # /* 0x1C */ bool8 allElevatorsLocked;
    #
    # /* 0x1D */ bool8 giovanniRequiresGyms;
    # /* 0x1E */ u8 giovanniRequiredCount;
    # /* 0x1F */ bool8 route22GateRequiresGyms;
    # /* 0x20 */ u8 route22GateRequiredCount;
    # /* 0x21 */ bool8 route23GuardRequiresGyms;
    # /* 0x22 */ u8 route23GuardRequiredCount;
    # /* 0x23 */ bool8 eliteFourRequiresGyms;
    # /* 0x24 */ u8 eliteFourRequiredCount;
    # /* 0x25 */ bool8 eliteFourRematchRequiresGyms;
    # /* 0x26 */ u8 eliteFourRematchRequiredCount;
    # /* 0x27 */ u8 ceruleanCaveRequirement; // 0 = Vanilla, 1 = Become Champion, 2 = Restore Network Center,
    #                                           3 = Badges, 4 = Gyms
    # /* 0x28 */ u8 ceruleanCaveRequiredCount;
    # /* 0x29 */ u8 cinnabarFossilCount;
    # /* 0x2A */ u8 rematchRequiresGyms;
    #
    # /* 0x2B */ u32 startingMoney;
    #
    # /* 0x2F */ bool8 itemfinderRequired;
    # /* 0x30 */ bool8 flashRequired;
    # /* 0x31 */ bool8 fameCheckerRequired;
    # /* 0x32 */ bool8 bikeRequiresJumpingShoes;
    # /* 0x33 */ bool8 acrobaticBike;
    #
    # /* 0x34 */ u8 oaksAideRequiredCounts[5]; // Route 2, Route 10, Route 11, Route 16, Route 15
    #
    # /* 0x39 */ bool8 reccuringHiddenItems;
    # /* 0x3A */ bool8 isTrainersanity;
    # /* 0x3B */ bool8 isDexsanity;
    # /* 0x3C */ bool8 extraKeyItems;
    # /* 0x3D */ bool8 kantoOnly;
    # /* 0x3E */ bool8 flyUnlocks;
    # /* 0x3F */ bool8 isFamesanity;
    # /* 0x40 */ bool8 gymKeys;
    # /* 0x41 */ bool8 isShopsanity;
    #
    # /* 0x42 */ u8 removeBadgeRequirement; // Flash, Cut, Fly, Strength, Surf, Rock Smash, Waterfall
    # /* 0x43 */ u8 additionalDarkCaves; // Mt. Moon, Diglett's Cave, Victory Road
    #
    # /* 0x44 */ bool8 passesSplit;
    # /* 0x45 */ bool8 cardKeysSplit;
    # /* 0x46 */ bool8 teasSplit;
    #
    # /* 0x47 */ u8 startingLocation;
    # /* 0x48 */ u8 startingRespawn;
    # /* 0x49 */ u8 free_fly_id;
    # /* 0x4A */ u8 town_free_fly_id;
    # /* 0x4B */ u16 resortGorgeousMon;
    # /* 0x4D */ u16 introSpecies;
    # /* 0x4F */ u16 pcItemId;
    # /* 0x51 */ bool8 remoteItems;
    # /* 0x52 */ bool8 internalEntrancesRandomized;
    # /* 0x53 */ bool8 randomized;
    # /* 0x54 */ u8 version[16];
    # }
    options_address = data.rom_addresses["gArchipelagoOptions"]

    # Set game options
    game_options_1 = 0
    game_options_2 = 0
    for option_name, option in GAME_OPTIONS.items():
        if option_name in world.options.game_options.value.keys():
            value = option.options[world.options.game_options.value[option_name]]
        else:
            value = option.default
        if option.option_group == -1:
            patch.write_token(options_address, 0x00, struct.pack("<B", value))
        elif option.option_group == -2:
            patch.write_token(options_address, 0x01, struct.pack("<H", value))
        elif option.option_group == 1:
            game_options_1 |= (value << option.option_number)
        elif option.option_group == 2:
            game_options_2 |= (value << option.option_number)
    patch.write_token(options_address, 0x03, struct.pack("<H", game_options_1))
    patch.write_token(options_address, 0x05, struct.pack("<H", game_options_2))

    # Set better shops
    better_shops = 1 if world.options.better_shops else 0
    patch.write_token(options_address, 0x06, struct.pack("<B", better_shops))

    # Set reusable TMs and Move Tutors
    reusable_tm_tutors = 1 if world.options.reusable_tm_tutors else 0
    patch.write_token(options_address, 0x07, struct.pack("<B", reusable_tm_tutors))

    # Set unlock seen dex info
    all_pokemon_seen = 1 if world.options.all_pokemon_seen else 0
    patch.write_token(options_address, 0x08, struct.pack("<B", all_pokemon_seen))

    # Set physical/special split
    physical_special_split = 1 if world.options.physical_special_split else 0
    patch.write_token(options_address, 0x09, struct.pack("<B", physical_special_split))

    # Set Viridian City roadblock
    open_viridian = 1 if world.options.viridian_city_roadblock.value == ViridianCityRoadblock.option_open else 0
    patch.write_token(options_address, 0x0A, struct.pack("<B", open_viridian))

    # Set Pewter City roadblock
    route_3_condition = world.options.pewter_city_roadblock.value
    patch.write_token(options_address, 0x0B, struct.pack("<B", route_3_condition))

    # Set Cerulean City roadblocks
    open_cerulean = 1 if "Remove Cerulean Roadblocks" in world.options.modify_world_state.value else 0
    patch.write_token(options_address, 0x0C, struct.pack("<B", open_cerulean))

    # Set Route 2 modification
    route_2_modified = 1 if "Modify Route 2" in world.options.modify_world_state.value else 0
    patch.write_token(options_address, 0x0D, struct.pack("<B", route_2_modified))

    # Set Route 9 modification
    route_9_modified = 1 if "Modify Route 9" in world.options.modify_world_state.value else 0
    patch.write_token(options_address, 0x0E, struct.pack("<B", route_9_modified))

    # Set Underground Tunnels blocked
    block_tunnels = 1 if "Block Tunnels" in world.options.modify_world_state.value else 0
    patch.write_token(options_address, 0x0F, struct.pack("<B", block_tunnels))

    # Set Route 12 boulders
    route_12_boulders = 1 if "Route 12 Boulders" in world.options.modify_world_state.value else 0
    patch.write_token(options_address, 0x10, struct.pack("<B", route_12_boulders))

    # Set Route 10 modification
    route_10_modified = 1 if "Modify Route 10" in world.options.modify_world_state.value else 0
    patch.write_token(options_address, 0x11, struct.pack("<B", route_10_modified))

    # Set Route 12 modification
    route_12_modified = 1 if "Modify Route 12" in world.options.modify_world_state.value else 0
    patch.write_token(options_address, 0x12, struct.pack("<B", route_12_modified))

    # Set Route 16 modification
    route_16_modified = 1 if "Modify Route 16" in world.options.modify_world_state.value else 0
    patch.write_token(options_address, 0x13, struct.pack("<B", route_16_modified))

    # Set open Silph Co.
    open_silph = 1 if "Open Silph" in world.options.modify_world_state.value else 0
    patch.write_token(options_address, 0x14, struct.pack("<B", open_silph))

    # Set remove Saffron Rockets
    remove_saffron_rockets = 1 if "Remove Saffron Rockets" in world.options.modify_world_state.value else 0
    patch.write_token(options_address, 0x15, struct.pack("<B", remove_saffron_rockets))

    # Set Route 23 modification
    route_23_modified = 1 if "Modify Route 23" in world.options.modify_world_state.value else 0
    patch.write_token(options_address, 0x16, struct.pack("<B", route_23_modified))

    # Set Route 23 trees
    route_23_trees = 1 if "Route 23 Trees" in world.options.modify_world_state.value else 0
    patch.write_token(options_address, 0x17, struct.pack("<B", route_23_trees))

    # Set Pokémon Tower blocked
    block_tower = 1 if "Block Tower" in world.options.modify_world_state.value else 0
    patch.write_token(options_address, 0x18, struct.pack("<B", block_tower))

    # Set Victory Road rocks
    victory_road_rocks = 1 if "Victory Road Rocks" in world.options.modify_world_state.value else 0
    patch.write_token(options_address, 0x19, struct.pack("<B", victory_road_rocks))

    # Set early gossipers
    early_gossipers = 1 if "Early Gossipers" in world.options.modify_world_state.value else 0
    patch.write_token(options_address, 0x1A, struct.pack("<B", early_gossipers))

    # Set block Vermilion sailing
    block_vermilion_sailing = 1 if "Block Vermilion Sailing" in world.options.modify_world_state.value else 0
    patch.write_token(options_address, 0x1B, struct.pack("<B", block_vermilion_sailing))

    # Set all elevators locked
    all_elevators_locked = 1 if "All Elevators Locked" in world.options.modify_world_state.value else 0
    patch.write_token(options_address, 0x1C, struct.pack("<B", all_elevators_locked))

    # Set Viridian Gym Rrquirement
    viridian_gym_requirement = world.options.viridian_gym_requirement.value
    patch.write_token(options_address, 0x1D, struct.pack("<B", viridian_gym_requirement))

    # Set Viridian Gym count
    viridian_gym_count = world.options.viridian_gym_count.value
    patch.write_token(options_address, 0x1E, struct.pack("<B", viridian_gym_count))

    # Set Route 22 requirement
    route_22_requirement = world.options.route22_gate_requirement.value
    patch.write_token(options_address, 0x1F, struct.pack("<B", route_22_requirement))

    # Set Route 22 count
    route_22_count = world.options.route22_gate_count.value
    patch.write_token(options_address, 0x20, struct.pack("<B", route_22_count))

    # Set Route 23 requirement
    route_23_requirement = world.options.route23_guard_requirement.value
    patch.write_token(options_address, 0x21, struct.pack("<B", route_23_requirement))

    # Set Route 23 count
    route_23_count = world.options.route23_guard_count.value
    patch.write_token(options_address, 0x22, struct.pack("<B", route_23_count))

    # Set Elite Four requirement
    elite_four_requirement = world.options.elite_four_requirement.value
    patch.write_token(options_address, 0x23, struct.pack("<B", elite_four_requirement))

    # Set Elite Four count
    elite_four_count = world.options.elite_four_count.value
    patch.write_token(options_address, 0x24, struct.pack("<B", elite_four_count))

    # Set Elite Four Rematch requirement
    elite_four_rematch_requirement = world.options.elite_four_requirement.value
    patch.write_token(options_address, 0x25, struct.pack("<B", elite_four_rematch_requirement))

    # Set Elite Four Rematch count
    elite_four_rematch_count = world.options.elite_four_rematch_count.value
    patch.write_token(options_address, 0x26, struct.pack("<B", elite_four_rematch_count))

    # Set Cerulean Cave requirement
    cerulean_cave_requirement = world.options.cerulean_cave_requirement.value
    patch.write_token(options_address, 0x27, struct.pack("<B", cerulean_cave_requirement))

    # Set Cerulean Cave count
    cerulean_cave_count = world.options.cerulean_cave_count.value
    patch.write_token(options_address, 0x28, struct.pack("<B", cerulean_cave_count))

    # Set Fossil count
    fossil_count = world.options.fossil_count.value
    patch.write_token(options_address, 0x29, struct.pack("<B", fossil_count))

    # Set rematch requirements
    rematch_requirements = world.options.rematch_requirements.value
    patch.write_token(options_address, 0x2A, struct.pack("<B", rematch_requirements))

    # Set starting money
    patch.write_token(options_address, 0x2B, struct.pack("<I", world.options.starting_money.value))

    # Set itemfinder required
    itemfinder_required = 1 if world.options.itemfinder_required.value == ItemfinderRequired.option_required else 0
    patch.write_token(options_address, 0x2F, struct.pack("<B", itemfinder_required))

    # Set flash required
    flash_required = 1 if world.options.flash_required.value == FlashRequired.option_required else 0
    patch.write_token(options_address, 0x30, struct.pack("<B", flash_required))

    # Set fame checker required
    fame_checker_required = 1 if world.options.fame_checker_required else 0
    patch.write_token(options_address, 0x31, struct.pack("<B", fame_checker_required))

    # Set bicycle requires jumping shoes
    bicycle_requires_jumping_shoes = 1 if world.options.bicycle_requires_jumping_shoes else 0
    patch.write_token(options_address, 0x32, struct.pack("<B", bicycle_requires_jumping_shoes))

    # Set acrobatic bicycle
    acrobatic_bicycle = 1 if world.options.acrobatic_bicycle else 0
    patch.write_token(options_address, 0x33, struct.pack("<B", acrobatic_bicycle))

    # Set Oak's Aides counts
    oaks_aide_route_2 = world.options.oaks_aide_route_2.value
    patch.write_token(options_address, 0x34, struct.pack("<B", oaks_aide_route_2))
    oaks_aide_route_10 = world.options.oaks_aide_route_10.value
    patch.write_token(options_address, 0x35, struct.pack("<B", oaks_aide_route_10))
    oaks_aide_route_11 = world.options.oaks_aide_route_11.value
    patch.write_token(options_address, 0x36, struct.pack("<B", oaks_aide_route_11))
    oaks_aide_route_16 = world.options.oaks_aide_route_16.value
    patch.write_token(options_address, 0x37, struct.pack("<B", oaks_aide_route_16))
    oaks_aide_route_15 = world.options.oaks_aide_route_15.value
    patch.write_token(options_address, 0x38, struct.pack("<B", oaks_aide_route_15))

    # Set recurring hidden items shuffled
    recurring_hidden_items = 1 if world.options.shuffle_hidden.value == ShuffleHiddenItems.option_all else 0
    patch.write_token(options_address, 0x39, struct.pack("<B", recurring_hidden_items))

    # Set trainersanity
    trainersanity = 1 if world.options.trainersanity.value != Trainersanity.special_range_names["none"] else 0
    patch.write_token(options_address, 0x3A, struct.pack("<B", trainersanity))

    # Set dexsanity
    dexsanity = 1 if world.options.dexsanity.value != Dexsanity.special_range_names["none"] else 0
    patch.write_token(options_address, 0x3B, struct.pack("<B", dexsanity))

    # Set extra key items
    extra_key_items = 1 if world.options.extra_key_items else 0
    patch.write_token(options_address, 0x3C, struct.pack("<B", extra_key_items))

    # Set kanto only
    kanto_only = 1 if world.options.kanto_only else 0
    patch.write_token(options_address, 0x3D, struct.pack("<B", kanto_only))

    # Set fly unlocks
    fly_unlocks = 1 if (world.options.shuffle_fly_unlocks.value != ShuffleFlyUnlocks.option_off or
                        world.options.randomize_fly_destinations) else 0
    patch.write_token(options_address, 0x3E, struct.pack("<B", fly_unlocks))

    # Set famesanity
    famesanity = 1 if world.options.famesanity else 0
    patch.write_token(options_address, 0x3F, struct.pack("<B", famesanity))

    # Set gym keys
    gym_keys = 1 if world.options.gym_keys else 0
    patch.write_token(options_address, 0x40, struct.pack("<B", gym_keys))

    # Set shopsanity
    shopsanity = 1 if world.options.shopsanity else 0
    patch.write_token(options_address, 0x41, struct.pack("<B", shopsanity))

    # Set remove badge requirements
    hms = ["Flash", "Cut", "Fly", "Strength", "Surf", "Rock Smash", "Waterfall"]
    remove_badge_requirements = 0
    for i, hm in enumerate(hms):
        if hm in world.options.remove_badge_requirement.value:
            remove_badge_requirements |= (1 << i)
    patch.write_token(options_address, 0x42, struct.pack("<B", remove_badge_requirements))

    # Set additional dark caves
    dark_caves = ["Mt. Moon", "Diglett's Cave", "Victory Road"]
    map_ids = [["MAP_MT_MOON_1F", "MAP_MT_MOON_B1F", "MAP_MT_MOON_B2F"],
               ["MAP_DIGLETTS_CAVE_B1F"],
               ["MAP_VICTORY_ROAD_1F", "MAP_VICTORY_ROAD_2F", "MAP_VICTORY_ROAD_3F"]]
    additional_dark_caves = 0
    for i, dark_cave in enumerate(dark_caves):
        if dark_cave in world.options.additional_dark_caves.value:
            additional_dark_caves |= (1 << i)
            for map_id in map_ids[i]:
                map_data = world.modified_maps[map_id]
                header_address = map_data.header_address
                patch.write_token(header_address, 21, struct.pack("<B", 1))
    patch.write_token(options_address, 0x43, struct.pack("<B", additional_dark_caves))

    # Set passes split
    passes_split = 1 if world.options.island_passes.value in {IslandPasses.option_split,
                                                              IslandPasses.option_progressive_split} else 0
    patch.write_token(options_address, 0x44, struct.pack("<B", passes_split))

    # Set card keys split
    card_keys_split = 1 if world.options.card_key.value in {CardKey.option_split, CardKey.option_progressive} else 0
    patch.write_token(options_address, 0x45, struct.pack("<B", card_keys_split))

    # Set teas split
    teas_split = 1 if world.options.split_teas else 0
    patch.write_token(options_address, 0x46, struct.pack("<B", teas_split))

    # Set starting town
    starting_town = data.constants[world.starting_town]
    patch.write_token(options_address, 0x47, struct.pack("<B", starting_town))

    # Set starting respawn
    starting_respawn = data.constants[world.starting_respawn]
    patch.write_token(options_address, 0x48, struct.pack("<B", starting_respawn))

    # Set free fly location
    patch.write_token(options_address, 0x49, struct.pack("<B", world.free_fly_location_id))

    # Set town map fly location
    patch.write_token(options_address, 0x4A, struct.pack("<B", world.town_map_fly_location_id))

    # Set resort gorgeous mon
    patch.write_token(options_address, 0x4B, struct.pack("<H", world.logic.resort_gorgeous_pokemon))

    # Set intro species
    species_id = world.random.choice(list(data.species.keys()))
    patch.write_token(options_address, 0x4D, struct.pack("<H", species_id))

    # Set PC item ID
    pc_item_location = world.get_location("Player's PC - PC Item")
    if not world.options.remote_items and pc_item_location.item.player == world.player:
        item_id = pc_item_location.item.code
    else:
        item_id = data.constants["ITEM_ARCHIPELAGO_PROGRESSION"]
    patch.write_token(options_address, 0x4F, struct.pack("<H", item_id))

    # Set remote items
    remote_items = 1 if world.options.remote_items else 0
    patch.write_token(options_address, 0x51, struct.pack("<B", remote_items))

    # Set interior ER
    shuffle_interiors = 1 if world.options.shuffle_interiors else 0
    patch.write_token(options_address, 0x52, struct.pack("<B", shuffle_interiors))

    # Set that the game has been randomized
    patch.write_token(options_address, 0x53, struct.pack("<B", 1))

    # Set apworld version
    apworld_version = f"AP v{APWORLD_VERSION}"
    for j, b in enumerate(encode_string(apworld_version, 16)):
        patch.write_token(options_address, 0x54 + j, struct.pack("<B", b))

    # Set total darkness
    if "Total Darkness" in world.options.modify_world_state.value:
        flash_level_address = data.rom_addresses["sFlashLevelToRadius"]
        patch.write_token(flash_level_address, 8, struct.pack("<H", 0))

    # Set skip elite four
    if world.options.skip_elite_four:
        indigo_address = data.maps["MAP_INDIGO_PLATEAU_POKEMON_CENTER_1F"].warp_table_address
        champion_address = data.maps["MAP_POKEMON_LEAGUE_CHAMPIONS_ROOM"].warp_table_address
        patch.write_token(indigo_address,
                          14,
                          struct.pack("<H", data.constants["MAP_POKEMON_LEAGUE_CHAMPIONS_ROOM"]))
        patch.write_token(champion_address,
                          6,
                          struct.pack("<H", data.constants["MAP_INDIGO_PLATEAU_POKEMON_CENTER_1F"]))

    # Randomize music
    if world.options.randomize_music:
        # The "randomized sound table" is a patchboard that redirects sounds just before they get played
        randomized_looping_music = _LOOPING_MUSIC.copy()
        world.random.shuffle(randomized_looping_music)
        sound_table_address = data.rom_addresses["gRandomizedSoundTable"]
        for original_music, randomized_music in zip(_LOOPING_MUSIC, randomized_looping_music):
            patch.write_token(sound_table_address,
                              data.constants[original_music] * 2,
                              struct.pack("<H", data.constants[randomized_music]))

    # Randomize fanfares
    if world.options.randomize_fanfares:
        # Shuffle the lists, pair new tracks with original tracks, set the new track ids, and set new fanfare durations
        randomized_fanfares = [fanfare_name for fanfare_name in _FANFARES]
        world.random.shuffle(randomized_fanfares)
        sound_table_address = data.rom_addresses["gRandomizedSoundTable"]
        fanfares_address = data.rom_addresses["sFanfares"]
        for i, fanfare_data in enumerate(zip(_FANFARES.keys(), randomized_fanfares)):
            patch.write_token(sound_table_address,
                              data.constants[fanfare_data[0]] * 2,
                              struct.pack("<H", data.constants[fanfare_data[1]]))
            patch.write_token(fanfares_address,
                              (i * 4) + 2,
                              struct.pack("<H", data.constants[fanfare_data[1]]))

    # Set slot auth
    patch.write_token(data.rom_addresses["gArchipelagoInfo"], 0, world.auth)

    # Set apworld version in ROM header
    apworld_version_address = {}
    for key in patch.revision_keys:
        apworld_version_address[key] = 0x178
    patch.write_token(apworld_version_address, 0, APWORLD_VERSION.encode("ascii"))


def _set_shuffled_entrances(world: "PokemonFRLGWorld") -> None:
    if world.er_placement_state is None:
        return

    patch = world.patch_data
    for source_name, dest_name in world.er_placement_state.pairings:
        source_id = data.warp_name_map[source_name]
        dest_id = data.warp_name_map[dest_name]
        source_warp_data = data.warps[source_id]
        dest_warp_data = data.warps[dest_id]
        source_warp_table_address = data.maps[source_warp_data.source_map].warp_table_address
        dest_map_id = data.constants[dest_warp_data.source_map]
        if len(source_warp_data.source_ids) <= len(dest_warp_data.source_ids):
            for i, source_warp_id in enumerate(source_warp_data.source_ids):
                dest_warp_id = dest_warp_data.source_ids[i]
                patch.write_token(source_warp_table_address,
                                  (source_warp_id * 8) + 5,
                                  struct.pack("<B", dest_warp_id))
                patch.write_token(source_warp_table_address,
                                  (source_warp_id * 8) + 6,
                                  struct.pack("<H", dest_map_id))
        elif len(dest_warp_data.source_ids) == 1:
            dest_warp_id = dest_warp_data.source_ids[0]
            for source_warp_id in source_warp_data.source_ids:
                patch.write_token(source_warp_table_address,
                                  (source_warp_id * 8) + 5,
                                  struct.pack("<B", dest_warp_id))
                patch.write_token(source_warp_table_address,
                                  (source_warp_id * 8) + 6,
                                  struct.pack("<H", dest_map_id))
        elif len(source_warp_data.source_ids) > len(dest_warp_data.source_ids):
            for i, source_warp_id in enumerate(source_warp_data.source_ids):
                if i <= 1:
                    dest_warp_id = dest_warp_data.source_ids[0]
                else:
                    dest_warp_id = dest_warp_data.source_ids[1]
                patch.write_token(source_warp_table_address,
                                  (source_warp_id * 8) + 5,
                                  struct.pack("<B", dest_warp_id))
                patch.write_token(source_warp_table_address,
                                  (source_warp_id * 8) + 6,
                                  struct.pack("<H", dest_map_id))


def _set_randomized_fly_destinations(world: "PokemonFRLGWorld") -> None:
    if not world.options.randomize_fly_destinations:
        return

    patch = world.patch_data
    fly_id_map = {
        "SPAWN_PALLET_TOWN": "MAPSEC_PALLET_TOWN",
        "SPAWN_VIRIDIAN_CITY": "MAPSEC_VIRIDIAN_CITY",
        "SPAWN_PEWTER_CITY": "MAPSEC_PEWTER_CITY",
        "SPAWN_CERULEAN_CITY": "MAPSEC_CERULEAN_CITY",
        "SPAWN_LAVENDER_TOWN": "MAPSEC_LAVENDER_TOWN",
        "SPAWN_VERMILION_CITY": "MAPSEC_VERMILION_CITY",
        "SPAWN_CELADON_CITY": "MAPSEC_CELADON_CITY",
        "SPAWN_FUCHSIA_CITY": "MAPSEC_FUCHSIA_CITY",
        "SPAWN_CINNABAR_ISLAND": "MAPSEC_CINNABAR_ISLAND",
        "SPAWN_INDIGO_PLATEAU": "MAPSEC_INDIGO_PLATEAU",
        "SPAWN_SAFFRON_CITY": "MAPSEC_SAFFRON_CITY",
        "SPAWN_ROUTE4": "MAPSEC_ROUTE_4_POKECENTER",
        "SPAWN_ROUTE10": "MAPSEC_ROUTE_10_POKECENTER",
        "SPAWN_ONE_ISLAND": "MAPSEC_ONE_ISLAND",
        "SPAWN_TWO_ISLAND": "MAPSEC_TWO_ISLAND",
        "SPAWN_THREE_ISLAND": "MAPSEC_THREE_ISLAND",
        "SPAWN_FOUR_ISLAND": "MAPSEC_FOUR_ISLAND",
        "SPAWN_FIVE_ISLAND": "MAPSEC_FIVE_ISLAND",
        "SPAWN_SEVEN_ISLAND": "MAPSEC_SEVEN_ISLAND",
        "SPAWN_SIX_ISLAND": "MAPSEC_SIX_ISLAND"
    }

    fly_layer_offset = 0x294
    fly_point_table_address = data.rom_addresses["sFlyPoints"]
    fly_map_kanto_address = data.rom_addresses["sRegionMapSections_Kanto"]
    fly_map_sevii_123_address = data.rom_addresses["sRegionMapSections_Sevii123"]
    fly_map_sevii_45_address = data.rom_addresses["sRegionMapSections_Sevii45"]
    fly_map_sevii_67_address = data.rom_addresses["sRegionMapSections_Sevii67"]
    fly_map_address = [fly_map_kanto_address, fly_map_sevii_123_address,
                       fly_map_sevii_45_address, fly_map_sevii_67_address]
    fly_name_array_address = data.rom_addresses["gFlyUnlockNames"]
    for i in range(fly_layer_offset, fly_layer_offset + 0x14A):
        value = data.constants["MAPSEC_NONE"]
        patch.write_token(fly_map_kanto_address, i, struct.pack("<B", value))
        patch.write_token(fly_map_sevii_123_address, i, struct.pack("<B", value))
        patch.write_token(fly_map_sevii_45_address, i, struct.pack("<B", value))
        patch.write_token(fly_map_sevii_67_address, i, struct.pack("<B", value))
    for fly_id, fly_data in world.fly_destination_data.items():
        fly_id_offset = (data.constants[fly_id] - 1) * 8
        fly_map_offset = fly_layer_offset + fly_data.region_map_index
        fly_name_offset = (data.constants[fly_id] - 1) * 17
        fly_map_value = data.constants[fly_id_map[fly_id]]
        patch.write_token(fly_point_table_address, fly_id_offset, struct.pack("<B", fly_data.map_group))
        patch.write_token(fly_point_table_address, fly_id_offset + 1, struct.pack("<B", fly_data.map_num))
        patch.write_token(fly_point_table_address, fly_id_offset + 2, struct.pack("<H", fly_data.x_pos))
        patch.write_token(fly_point_table_address, fly_id_offset + 4, struct.pack("<H", fly_data.y_pos))
        patch.write_token(fly_map_address[fly_data.region_map_id - 1],
                          fly_map_offset,
                          struct.pack("<B", fly_map_value))
        for j, b in enumerate(encode_string(fly_data.display_name, 17)):
            patch.write_token(fly_name_array_address, fly_name_offset + j, struct.pack("<B", b))


def _set_shop_data(world: "PokemonFRLGWorld") -> None:
    patch = world.patch_data
    shop_locations= [loc for loc in world.get_locations()
                     if loc.name in location_groups["Shops"]
                     or loc.name in location_groups["Vending Machines"]]
    prize_cornor_locations = [loc for loc in world.get_locations()
                              if loc.name in location_groups["Prizes"]]
    already_set_prices: Dict[str, int] = {}

    for location in shop_locations:
        if location.item is None:
            continue

        already_set = False
        item_address = location.item_address

        if location.item.player != world.player:
            price = 2000
            if location.item.useful:
                price = round(price * 0.5)
            elif location.item.filler:
                price = round(price * 0.1)
            patch.write_token(item_address, 2, struct.pack("<H", data.constants["ITEM_ARCHIPELAGO_PROGRESSION"]))
        else:
            if location.item.name in already_set_prices and world.options.consistent_shop_prices:
                price = already_set_prices[location.item.name]
                already_set = True
            else:
                price = data.items[world.item_name_to_id[location.item.name]].price
            if location.item.code is not None:
                patch.write_token(item_address, 2, struct.pack("<H", location.item.code))

        if not already_set:
            if world.options.shop_prices == ShopPrices.option_cheap:
                price = round(price * 0.5)
            elif world.options.shop_prices == ShopPrices.option_affordable:
                price = world.random.randint(round(price * 0.5), price)
            elif world.options.shop_prices == ShopPrices.option_standard:
                price = world.random.randint(round(price * 0.5), round(price * 1.5))
            elif world.options.shop_prices == ShopPrices.option_expensive:
                price = world.random.randint(price, round(price * 1.5))

        patch.write_token(item_address, 4, struct.pack("<H", price))

        if location.item.player == world.player:
            already_set_prices[location.item.name] = price

        if ((location.item.player and is_single_purchase_item(location.item) or location.item.player != world.player)
                and location.address is not None):
            patch.write_token(item_address, 6, struct.pack("<B", 0))

    for location in prize_cornor_locations:
        if location.item is None:
            continue

        item_address = location.item_address

        if location.item.player != world.player:
            patch.write_token(item_address, 2, struct.pack("<H", data.constants["ITEM_ARCHIPELAGO_PROGRESSION"]))
        elif location.item.code is not None:
            patch.write_token(item_address, 2, struct.pack("<H", location.item.code))


def _set_species_info(world: "PokemonFRLGWorld") -> None:
    patch = world.patch_data
    for species in world.modified_species.values():
        address = species.address
        patch.write_token(address, 0x00, struct.pack("<B", species.base_stats[0]))
        patch.write_token(address, 0x01, struct.pack("<B", species.base_stats[1]))
        patch.write_token(address, 0x02, struct.pack("<B", species.base_stats[2]))
        patch.write_token(address, 0x03, struct.pack("<B", species.base_stats[3]))
        patch.write_token(address, 0x04, struct.pack("<B", species.base_stats[4]))
        patch.write_token(address, 0x05, struct.pack("<B", species.base_stats[5]))
        patch.write_token(address, 0x06, struct.pack("<B", species.types[0]))
        patch.write_token(address, 0x07, struct.pack("<B", species.types[1]))
        patch.write_token(address, 0x08, struct.pack("<B", species.catch_rate))
        patch.write_token(address, 0x16, struct.pack("<B", species.abilities[0]))
        patch.write_token(address, 0x17, struct.pack("<B", species.abilities[1]))

        for i, learnset_move in enumerate(species.learnset):
            learnset_address = species.learnset_address
            level_move = learnset_move.level << 9 | learnset_move.move_id
            patch.write_token(learnset_address, i * 2, struct.pack("<H", level_move))


def _set_wild_encounters(world: "PokemonFRLGWorld") -> None:
    if (world.options.level_scaling == LevelScaling.option_off and
            world.options.wild_pokemon == RandomizeWildPokemon.option_vanilla):
        return

    patch = world.patch_data
    for map_data in world.modified_maps.values():
        for table in map_data.encounters.values():
            if table is not None:
                for i, species_data in enumerate(table.slots[patch.game_version]):
                    address = table.address
                    patch.write_token(address, (i * 4) + 0x00, struct.pack("<B", species_data.min_level))
                    patch.write_token(address, (i * 4) + 0x01, struct.pack("<B", species_data.max_level))
                    patch.write_token(address, (i * 4) + 0x02, struct.pack("<H", species_data.species_id))


def _set_starters(world: "PokemonFRLGWorld") -> None:
    if world.options.starters == RandomizeStarters.option_vanilla:
        return

    patch = world.patch_data
    for name, starter in world.modified_starters.items():
        patch.write_token(starter.address, 0, struct.pack("<H", starter.species_id))


def _set_legendaries(world: "PokemonFRLGWorld") -> None:
    if (world.options.level_scaling == LevelScaling.option_off and
            world.options.legendary_pokemon == RandomizeLegendaryPokemon.option_vanilla):
        return

    patch = world.patch_data
    for name, legendary in world.modified_legendary_pokemon.items():
        patch.write_token(legendary.address, 0, struct.pack("<H", legendary.species_id[patch.game_version]))
        patch.write_token(legendary.level_address, 0, struct.pack("<B", legendary.level[patch.game_version]))


def _set_misc_pokemon(world: "PokemonFRLGWorld") -> None:
    if (world.options.level_scaling == LevelScaling.option_off and
            world.options.misc_pokemon == RandomizeMiscPokemon.option_vanilla):
        return

    patch = world.patch_data
    for name, misc_pokemon in world.modified_misc_pokemon.items():
        patch.write_token(misc_pokemon.address,
                          0,
                          struct.pack("<H", misc_pokemon.species_id[patch.game_version]))
        if misc_pokemon.level[patch.game_version] != 0:
            patch.write_token(misc_pokemon.level_address,
                              0,
                              struct.pack("<B", misc_pokemon.level[patch.game_version]))


def _set_trade_pokemon(world: "PokemonFRLGWorld") -> None:
    patch = world.patch_data
    for name, trade_pokemon in world.modified_trade_pokemon.items():
        patch.write_token(trade_pokemon.species_address,
                          0,
                          struct.pack("<H", trade_pokemon.species_id[patch.game_version]))
        patch.write_token(trade_pokemon.requested_species_address,
                          0,
                          struct.pack("<H", trade_pokemon.requested_species_id[patch.game_version]))


def _set_trainer_parties(world: "PokemonFRLGWorld") -> None:
    if (world.options.level_scaling == LevelScaling.option_off and
            world.options.trainers == RandomizeTrainerParties.option_vanilla and
            world.options.starters == RandomizeStarters.option_vanilla and
            world.options.modify_trainer_levels.value == 100):
        return

    patch = world.patch_data
    for trainer in world.modified_trainers.values():
        party_address = trainer.party.address

        if trainer.party.pokemon_data_type in {TrainerPokemonDataTypeEnum.NO_ITEM_DEFAULT_MOVES,
                                               TrainerPokemonDataTypeEnum.ITEM_DEFAULT_MOVES}:
            pokemon_data_size = 8
        else:
            pokemon_data_size = 16

        for i, pokemon in enumerate(trainer.party.pokemon):
            pokemon_offset = (i * pokemon_data_size)
            level = round(pokemon.level * (world.options.modify_trainer_levels.value / 100))
            level = bound(level, 1, 100)
            species_id = pokemon.species_id

            if world.options.force_fully_evolved != ForceFullyEvolved.special_range_names["never"]:
                evolve = True
                if world.options.force_fully_evolved == ForceFullyEvolved.special_range_names["species"]:
                    while evolve:
                        evolve = False
                        species_data = world.modified_species[species_id]
                        evolutions = species_data.evolutions.copy()
                        world.random.shuffle(evolutions)
                        for evolution in evolutions:
                            if evolution.method in range(EvolutionMethodEnum.LEVEL, EvolutionMethodEnum.ITEM):
                                if level >= evolution.param:
                                    species_id = evolution.species_id
                                    evolve = True
                                    break
                            else:
                                evolution_data = world.modified_species[evolution.species_id]
                                evolution_level = sum(evolution_data.base_stats) / 15
                                if level > evolution_level:
                                    species_id = evolution.species_id
                                    evolve = True
                                    break
                elif level >= world.options.force_fully_evolved.value:
                    while evolve:
                        species_data = world.modified_species[species_id]
                        if len(species_data.evolutions) > 0:
                            evolution = world.random.choice(species_data.evolutions)
                            species_id = evolution.species_id
                        else:
                            evolve = False

            patch.write_token(party_address, pokemon_offset + 0x02, struct.pack("<B", level))
            patch.write_token(party_address, pokemon_offset + 0x04, struct.pack("<H", species_id))
            if trainer.party.pokemon_data_type in {TrainerPokemonDataTypeEnum.NO_ITEM_CUSTOM_MOVES,
                                                   TrainerPokemonDataTypeEnum.ITEM_CUSTOM_MOVES}:
                offset = 2 if trainer.party.pokemon_data_type == TrainerPokemonDataTypeEnum.ITEM_CUSTOM_MOVES else 0
                patch.write_token(party_address,
                                  pokemon_offset + offset + 0x06,
                                  struct.pack("<H", pokemon.moves[0]))
                patch.write_token(party_address,
                                  pokemon_offset + offset + 0x08,
                                  struct.pack("<H", pokemon.moves[1]))
                patch.write_token(party_address,
                                  pokemon_offset + offset + 0x0A,
                                  struct.pack("<H", pokemon.moves[2]))
                patch.write_token(party_address,
                                  pokemon_offset + offset + 0x0C,
                                  struct.pack("<H", pokemon.moves[3]))


def _set_tmhm_compatibility(world: "PokemonFRLGWorld") -> None:
    if (world.options.hm_compatibility == HmCompatibility.special_range_names["vanilla"] and
            world.options.tm_tutor_compatibility == TmTutorCompatibility.special_range_names["vanilla"]):
        return

    patch = world.patch_data
    learnsets_address = data.rom_addresses["sTMHMLearnsets"]
    for species in world.modified_species.values():
        patch.write_token(learnsets_address,
                          species.species_id * 8,
                          struct.pack("<Q", species.tm_hm_compatibility))


def _set_tm_moves(world: "PokemonFRLGWorld") -> None:
    if not world.options.tm_tutor_moves:
        return

    patch = world.patch_data
    address = data.rom_addresses["sTMHMMoves"]
    for i, move in enumerate(world.modified_tmhm_moves):
        # Don't modify HMs
        if i >= 50:
            break
        patch.write_token(address, i * 2, struct.pack("<H", move))


def _randomize_move_tutors(world: "PokemonFRLGWorld") -> None:
    patch = world.patch_data

    if world.options.tm_tutor_moves:
        new_tutor_moves = randomize_tutor_moves(world)
        address = data.rom_addresses["gTutorMoves"]

        for i, move in enumerate(new_tutor_moves):
            patch.write_token(address, i * 2, struct.pack("<H", move))

    if world.options.tm_tutor_compatibility != TmTutorCompatibility.special_range_names["vanilla"]:
        learnsets_address = data.rom_addresses["sTutorLearnsets"]

        for species in world.modified_species.values():
            patch.write_token(
                learnsets_address,
                species.species_id * 2,
                struct.pack("<H", bool_array_to_int([
                    world.random.randrange(0, 100) < world.options.tm_tutor_compatibility.value
                    for _ in range(16)
                ]))
            )


def _set_types_damage_categories(world: "PokemonFRLGWorld") -> None:
    if world.options.damage_categories == RandomizeDamageCategories.option_vanilla:
        return

    patch = world.patch_data
    address = data.rom_addresses["sDamageTypeTable"]
    for i, damage_category in enumerate(world.modified_type_damage_categories):
        patch.write_token(address, i, struct.pack("<B", damage_category))


def _set_moves(world: "PokemonFRLGWorld") -> None:
    if (world.options.move_types == RandomizeMoveTypes.option_vanilla and
            world.options.damage_categories == RandomizeDamageCategories.option_vanilla):
        return

    patch = world.patch_data
    for move in world.modified_moves.values():
        address = move.address
        patch.write_token(address, 2, struct.pack("<B", move.type))
        patch.write_token(address, 9, struct.pack("<B", move.category))
