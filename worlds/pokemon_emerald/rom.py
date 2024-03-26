"""
Classes and functions related to creating a ROM patch
"""
import copy
import os
import pkgutil
from typing import TYPE_CHECKING, Dict, List, Tuple

import bsdiff4

from worlds.Files import APDeltaPatch
from settings import get_settings

from .data import TrainerPokemonDataTypeEnum, BASE_OFFSET, data
from .items import reverse_offset_item_value
from .options import (RandomizeWildPokemon, RandomizeTrainerParties, EliteFourRequirement, NormanRequirement,
                      MatchTrainerLevels)
from .pokemon import HM_MOVES, get_random_move
from .util import bool_array_to_int, encode_string, get_easter_egg

if TYPE_CHECKING:
    from . import PokemonEmeraldWorld


_LOOPING_MUSIC = [
    "MUS_GSC_ROUTE38", "MUS_GSC_PEWTER", "MUS_ROUTE101", "MUS_ROUTE110", "MUS_ROUTE120", "MUS_ROUTE122",
    "MUS_PETALBURG", "MUS_OLDALE", "MUS_GYM", "MUS_SURF", "MUS_PETALBURG_WOODS", "MUS_LILYCOVE_MUSEUM",
    "MUS_OCEANIC_MUSEUM", "MUS_ENCOUNTER_GIRL", "MUS_ENCOUNTER_MALE", "MUS_ABANDONED_SHIP", "MUS_FORTREE",
    "MUS_BIRCH_LAB", "MUS_B_TOWER_RS", "MUS_ENCOUNTER_SWIMMER", "MUS_CAVE_OF_ORIGIN", "MUS_ENCOUNTER_RICH",
    "MUS_VERDANTURF", "MUS_RUSTBORO", "MUS_POKE_CENTER", "MUS_CAUGHT", "MUS_VICTORY_GYM_LEADER", "MUS_VICTORY_LEAGUE",
    "MUS_VICTORY_WILD", "MUS_C_VS_LEGEND_BEAST", "MUS_ROUTE104", "MUS_ROUTE119", "MUS_CYCLING", "MUS_POKE_MART",
    "MUS_LITTLEROOT", "MUS_MT_CHIMNEY", "MUS_ENCOUNTER_FEMALE", "MUS_LILYCOVE", "MUS_DESERT", "MUS_HELP",
    "MUS_UNDERWATER", "MUS_VICTORY_TRAINER", "MUS_ENCOUNTER_MAY", "MUS_ENCOUNTER_INTENSE", "MUS_ENCOUNTER_COOL",
    "MUS_ROUTE113", "MUS_ENCOUNTER_AQUA", "MUS_FOLLOW_ME", "MUS_ENCOUNTER_BRENDAN", "MUS_EVER_GRANDE",
    "MUS_ENCOUNTER_SUSPICIOUS", "MUS_VICTORY_AQUA_MAGMA", "MUS_GAME_CORNER", "MUS_DEWFORD", "MUS_SAFARI_ZONE",
    "MUS_VICTORY_ROAD", "MUS_AQUA_MAGMA_HIDEOUT", "MUS_SAILING", "MUS_MT_PYRE", "MUS_SLATEPORT", "MUS_MT_PYRE_EXTERIOR",
    "MUS_SCHOOL", "MUS_HALL_OF_FAME", "MUS_FALLARBOR", "MUS_SEALED_CHAMBER", "MUS_CONTEST_WINNER", "MUS_CONTEST",
    "MUS_ENCOUNTER_MAGMA", "MUS_ABNORMAL_WEATHER", "MUS_WEATHER_GROUDON", "MUS_SOOTOPOLIS", "MUS_HALL_OF_FAME_ROOM",
    "MUS_TRICK_HOUSE", "MUS_ENCOUNTER_TWINS", "MUS_ENCOUNTER_ELITE_FOUR", "MUS_ENCOUNTER_HIKER", "MUS_CONTEST_LOBBY",
    "MUS_ENCOUNTER_INTERVIEWER", "MUS_ENCOUNTER_CHAMPION", "MUS_B_FRONTIER", "MUS_B_ARENA", "MUS_B_PYRAMID",
    "MUS_B_PYRAMID_TOP", "MUS_B_PALACE", "MUS_B_TOWER", "MUS_B_DOME", "MUS_B_PIKE", "MUS_B_FACTORY", "MUS_VS_RAYQUAZA",
    "MUS_VS_FRONTIER_BRAIN", "MUS_VS_MEW", "MUS_B_DOME_LOBBY", "MUS_VS_WILD", "MUS_VS_AQUA_MAGMA", "MUS_VS_TRAINER",
    "MUS_VS_GYM_LEADER", "MUS_VS_CHAMPION", "MUS_VS_REGI", "MUS_VS_KYOGRE_GROUDON", "MUS_VS_RIVAL", "MUS_VS_ELITE_FOUR",
    "MUS_VS_AQUA_MAGMA_LEADER", "MUS_RG_FOLLOW_ME", "MUS_RG_GAME_CORNER", "MUS_RG_ROCKET_HIDEOUT", "MUS_RG_GYM",
    "MUS_RG_CINNABAR", "MUS_RG_LAVENDER", "MUS_RG_CYCLING", "MUS_RG_ENCOUNTER_ROCKET", "MUS_RG_ENCOUNTER_GIRL",
    "MUS_RG_ENCOUNTER_BOY", "MUS_RG_HALL_OF_FAME", "MUS_RG_VIRIDIAN_FOREST", "MUS_RG_MT_MOON", "MUS_RG_POKE_MANSION",
    "MUS_RG_ROUTE1", "MUS_RG_ROUTE24", "MUS_RG_ROUTE3", "MUS_RG_ROUTE11", "MUS_RG_VICTORY_ROAD", "MUS_RG_VS_GYM_LEADER",
    "MUS_RG_VS_TRAINER", "MUS_RG_VS_WILD", "MUS_RG_VS_CHAMPION", "MUS_RG_PALLET", "MUS_RG_OAK_LAB", "MUS_RG_OAK",
    "MUS_RG_POKE_CENTER", "MUS_RG_SS_ANNE", "MUS_RG_SURF", "MUS_RG_POKE_TOWER", "MUS_RG_SILPH", "MUS_RG_FUCHSIA",
    "MUS_RG_CELADON", "MUS_RG_VICTORY_TRAINER", "MUS_RG_VICTORY_WILD", "MUS_RG_VICTORY_GYM_LEADER", "MUS_RG_VERMILLION",
    "MUS_RG_PEWTER", "MUS_RG_ENCOUNTER_RIVAL", "MUS_RG_RIVAL_EXIT", "MUS_RG_CAUGHT", "MUS_RG_POKE_JUMP",
    "MUS_RG_UNION_ROOM", "MUS_RG_NET_CENTER", "MUS_RG_MYSTERY_GIFT", "MUS_RG_BERRY_PICK", "MUS_RG_SEVII_CAVE",
    "MUS_RG_TEACHY_TV_SHOW", "MUS_RG_SEVII_ROUTE", "MUS_RG_SEVII_DUNGEON", "MUS_RG_SEVII_123", "MUS_RG_SEVII_45",
    "MUS_RG_SEVII_67", "MUS_RG_VS_DEOXYS", "MUS_RG_VS_MEWTWO", "MUS_RG_VS_LEGEND", "MUS_RG_ENCOUNTER_GYM_LEADER",
    "MUS_RG_ENCOUNTER_DEOXYS", "MUS_RG_TRAINER_TOWER", "MUS_RG_SLOW_PALLET", "MUS_RG_TEACHY_TV_MENU",
]

_FANFARES: Dict[str, int] = {
    "MUS_LEVEL_UP":             80,
    "MUS_OBTAIN_ITEM":         160,
    "MUS_EVOLVED":             220,
    "MUS_OBTAIN_TMHM":         220,
    "MUS_HEAL":                160,
    "MUS_OBTAIN_BADGE":        340,
    "MUS_MOVE_DELETED":        180,
    "MUS_OBTAIN_BERRY":        120,
    "MUS_AWAKEN_LEGEND":       710,
    "MUS_SLOTS_JACKPOT":       250,
    "MUS_SLOTS_WIN":           150,
    "MUS_TOO_BAD":             160,
    "MUS_RG_POKE_FLUTE":       450,
    "MUS_RG_OBTAIN_KEY_ITEM":  170,
    "MUS_RG_DEX_RATING":       196,
    "MUS_OBTAIN_B_POINTS":     313,
    "MUS_OBTAIN_SYMBOL":       318,
    "MUS_REGISTER_MATCH_CALL": 135,
}

CAVE_EVENT_NAME_TO_ID = {
    "TERRA_CAVE_ROUTE_114_1": 1,
    "TERRA_CAVE_ROUTE_114_2": 2,
    "TERRA_CAVE_ROUTE_115_1": 3,
    "TERRA_CAVE_ROUTE_115_2": 4,
    "TERRA_CAVE_ROUTE_116_1": 5,
    "TERRA_CAVE_ROUTE_116_2": 6,
    "TERRA_CAVE_ROUTE_118_1": 7,
    "TERRA_CAVE_ROUTE_118_2": 8,
    "MARINE_CAVE_ROUTE_105_1": 9,
    "MARINE_CAVE_ROUTE_105_2": 10,
    "MARINE_CAVE_ROUTE_125_1": 11,
    "MARINE_CAVE_ROUTE_125_2": 12,
    "MARINE_CAVE_ROUTE_127_1": 13,
    "MARINE_CAVE_ROUTE_127_2": 14,
    "MARINE_CAVE_ROUTE_129_1": 15,
    "MARINE_CAVE_ROUTE_129_2": 16,
}


def _set_bytes_le(byte_array: bytearray, address: int, size: int, value: int) -> None:
    offset = 0
    while size > 0:
        byte_array[address + offset] = value & 0xFF
        value = value >> 8
        offset += 1
        size -= 1


class PokemonEmeraldDeltaPatch(APDeltaPatch):
    game = "Pokemon Emerald"
    hash = "605b89b67018abcea91e693a4dd25be3"
    patch_file_ending = ".apemerald"
    result_file_ending = ".gba"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()


def create_patch(world: "PokemonEmeraldWorld", output_directory: str) -> None:
    base_rom = get_base_rom_as_bytes()
    base_patch = pkgutil.get_data(__name__, "data/base_patch.bsdiff4")
    patched_rom = bytearray(bsdiff4.patch(base_rom, base_patch))

    # Set free fly location
    if world.options.free_fly_location:
        _set_bytes_le(
            patched_rom,
            data.rom_addresses["gArchipelagoOptions"] + 0x20,
            1,
            world.free_fly_location_id
        )

    location_info: List[Tuple[int, int, str]] = []
    for location in world.multiworld.get_locations(world.player):
        if location.address is None:
            continue

        if location.item is None:
            continue

        # Set local item values
        if not world.options.remote_items and location.item.player == world.player:
            if type(location.item_address) is int:
                _set_bytes_le(
                    patched_rom,
                    location.item_address,
                    2,
                    reverse_offset_item_value(location.item.code)
                )
            elif type(location.item_address) is list:
                for address in location.item_address:
                    _set_bytes_le(patched_rom, address, 2, reverse_offset_item_value(location.item.code))
        else:
            if type(location.item_address) is int:
                _set_bytes_le(
                    patched_rom,
                    location.item_address,
                    2,
                    data.constants["ITEM_ARCHIPELAGO_PROGRESSION"]
                )
            elif type(location.item_address) is list:
                for address in location.item_address:
                    _set_bytes_le(patched_rom, address, 2, data.constants["ITEM_ARCHIPELAGO_PROGRESSION"])

            # Creates a list of item information to store in tables later. Those tables are used to display the item and
            # player name in a text box. In the case of not enough space, the game will default to "found an ARCHIPELAGO
            # ITEM"
            location_info.append((location.address - BASE_OFFSET, location.item.player, location.item.name))

    if world.options.trainersanity:
        # Duplicate entries for rival fights
        # For each of the 5 fights, there are 6 variations that have to be accounted for (for starters * genders)
        # The Brendan Mudkip is used as a proxy in the rest of the AP code
        for locale in ["ROUTE_103", "ROUTE_110", "ROUTE_119", "RUSTBORO", "LILYCOVE"]:
            location = world.multiworld.get_location(data.locations[f"TRAINER_BRENDAN_{locale}_MUDKIP_REWARD"].label, world.player)
            alternates = [
                f"TRAINER_BRENDAN_{locale}_TREECKO",
                f"TRAINER_BRENDAN_{locale}_TORCHIC",
                f"TRAINER_MAY_{locale}_MUDKIP",
                f"TRAINER_MAY_{locale}_TREECKO",
                f"TRAINER_MAY_{locale}_TORCHIC",
            ]
            location_info.extend((
                data.constants["TRAINER_FLAGS_START"] + data.constants[trainer],
                location.item.player,
                location.item.name
            ) for trainer in alternates)

    player_name_ids: Dict[str, int] = {world.multiworld.player_name[world.player]: 0}
    item_name_offsets: Dict[str, int] = {}
    next_item_name_offset = 0
    for i, (flag, item_player, item_name) in enumerate(sorted(location_info, key=lambda t: t[0])):
        # The player's own items are still set in the table with the value 0 to indicate the game should not show any
        # message (the message for receiving an item will pop up when the client eventually gives it to them).
        # In race mode, no item location data is included, and only recieved (or own) items will show any text box.
        if item_player == world.player or world.multiworld.is_race:
            _set_bytes_le(patched_rom, data.rom_addresses["gArchipelagoNameTable"] + (i * 5) + 0, 2, flag)
            _set_bytes_le(patched_rom, data.rom_addresses["gArchipelagoNameTable"] + (i * 5) + 2, 2, 0)
            _set_bytes_le(patched_rom, data.rom_addresses["gArchipelagoNameTable"] + (i * 5) + 4, 1, 0)
        else:
            player_name = world.multiworld.player_name[item_player]

            if player_name not in player_name_ids:
                # Only space for 50 player names
                if len(player_name_ids) >= 50:
                    continue

                player_name_ids[player_name] = len(player_name_ids)
                for j, b in enumerate(encode_string(player_name, 17)):
                    _set_bytes_le(
                        patched_rom,
                        data.rom_addresses["gArchipelagoPlayerNames"] + (player_name_ids[player_name] * 17) + j,
                        1,
                        b
                    )

            if item_name not in item_name_offsets:
                if len(item_name) > 35:
                    item_name = item_name[:34] + "…"

                # Only 36 * 250 bytes for item names
                if next_item_name_offset + len(item_name) + 1 > 36 * 250:
                    continue

                item_name_offsets[item_name] = next_item_name_offset
                next_item_name_offset += len(item_name) + 1
                for j, b in enumerate(encode_string(item_name) + b"\xFF"):
                    _set_bytes_le(
                        patched_rom,
                        data.rom_addresses["gArchipelagoItemNames"] + (item_name_offsets[item_name]) + j,
                        1,
                        b
                    )

            # There should always be enough space for one entry per location
            _set_bytes_le(patched_rom, data.rom_addresses["gArchipelagoNameTable"] + (i * 5) + 0, 2, flag)
            _set_bytes_le(patched_rom, data.rom_addresses["gArchipelagoNameTable"] + (i * 5) + 2, 2, item_name_offsets[item_name])
            _set_bytes_le(patched_rom, data.rom_addresses["gArchipelagoNameTable"] + (i * 5) + 4, 1, player_name_ids[player_name])

    easter_egg = get_easter_egg(world.options.easter_egg.value)

    # Set start inventory
    start_inventory = world.options.start_inventory.value.copy()

    starting_badges = 0
    if start_inventory.pop("Stone Badge", 0) > 0:
        starting_badges |= (1 << 0)
    if start_inventory.pop("Knuckle Badge", 0) > 0:
        starting_badges |= (1 << 1)
    if start_inventory.pop("Dynamo Badge", 0) > 0:
        starting_badges |= (1 << 2)
    if start_inventory.pop("Heat Badge", 0) > 0:
        starting_badges |= (1 << 3)
    if start_inventory.pop("Balance Badge", 0) > 0:
        starting_badges |= (1 << 4)
    if start_inventory.pop("Feather Badge", 0) > 0:
        starting_badges |= (1 << 5)
    if start_inventory.pop("Mind Badge", 0) > 0:
        starting_badges |= (1 << 6)
    if start_inventory.pop("Rain Badge", 0) > 0:
        starting_badges |= (1 << 7)

    pc_slots: List[Tuple[str, int]] = []
    while any(qty > 0 for qty in start_inventory.values()):
        if len(pc_slots) >= 19:
            break

        for i, item_name in enumerate(start_inventory.keys()):
            if len(pc_slots) >= 19:
                break

            quantity = min(start_inventory[item_name], 999)
            if quantity == 0:
                continue

            start_inventory[item_name] -= quantity

            pc_slots.append((item_name, quantity))

    pc_slots.sort(reverse=True)

    for i, slot in enumerate(pc_slots):
        address = data.rom_addresses["sNewGamePCItems"] + (i * 4)
        item = reverse_offset_item_value(world.item_name_to_id[slot[0]])
        _set_bytes_le(patched_rom, address + 0, 2, item)
        _set_bytes_le(patched_rom, address + 2, 2, slot[1])

    # Set species data
    _set_species_info(world, patched_rom, easter_egg)

    # Set encounter tables
    if world.options.wild_pokemon != RandomizeWildPokemon.option_vanilla:
        _set_encounter_tables(world, patched_rom)

    # Set opponent data
    if world.options.trainer_parties != RandomizeTrainerParties.option_vanilla or easter_egg[0] == 2:
        _set_opponents(world, patched_rom, easter_egg)

    # Set legendary pokemon
    _set_legendary_encounters(world, patched_rom)

    # Set misc pokemon
    _set_misc_pokemon(world, patched_rom)

    # Set starters
    _set_starters(world, patched_rom)

    # Set TM moves
    _set_tm_moves(world, patched_rom, easter_egg)

    # Randomize move tutor moves
    _randomize_move_tutor_moves(world, patched_rom, easter_egg)

    # Set TM/HM compatibility
    _set_tmhm_compatibility(world, patched_rom)

    # Randomize opponent double or single
    _randomize_opponent_battle_type(world, patched_rom)

    # Options
    # struct ArchipelagoOptions
    # {
    #     /* 0x00 */ u16 birchPokemon;
    #     /* 0x02 */ bool8 advanceTextWithHoldA;
    #     /* 0x03 */ u8 receivedItemMessageFilter; // 0 = Show All; 1 = Show Progression Only; 2 = Show None
    #     /* 0x04 */ bool8 betterShopsEnabled;
    #     /* 0x05 */ bool8 reusableTms;
    #     /* 0x06 */ bool8 guaranteedCatch;
    #     /* 0x07 */ bool8 purgeSpinners;
    #     /* 0x08 */ bool8 areTrainersBlind;
    #     /* 0x09 */ u16 expMultiplierNumerator;
    #     /* 0x0B */ u16 expMultiplierDenominator;
    #     /* 0x0D */ bool8 matchTrainerLevels;
    #     /* 0x0E */ s8 matchTrainerLevelBonus;
    #     /* 0x0F */ bool8 eliteFourRequiresGyms;
    #     /* 0x10 */ u8 eliteFourRequiredCount;
    #     /* 0x11 */ bool8 normanRequiresGyms;
    #     /* 0x12 */ u8 normanRequiredCount;
    #     /* 0x13 */ u8 startingBadges;
    #     /* 0x14 */ u32 hmTotalBadgeRequirements;
    #     /* 0x18 */ u8 hmSpecificBadgeRequirements[8];
    #     /* 0x20 */ u8 freeFlyLocation;
    #     /* 0x21 */ u8 terraCaveLocationId:4;
    #                u8 marineCaveLocationId:4;
    #     /* 0x22 */ bool8 addRoute115Boulders;
    #     /* 0x23 */ bool8 addBumpySlopes;
    #     /* 0x24 */ bool8 modifyRoute118;
    #     /* 0x25 */ u16 removedBlockers;
    #     /* 0x27 */ bool8 berryTreesRandomized;
    #     /* 0x28 */ bool8 isDexsanity;
    #     /* 0x29 */ bool8 isTrainersanity;
    #     /* 0x2A */ bool8 isWarpRando;
    #     /* 0x2B */ u8 activeEasterEgg;
    #     /* 0x2C */ bool8 normalizeEncounterRates;
    #     /* 0x2D */ bool8 allowWonderTrading;
    #     /* 0x2E */ u16 matchTrainerLevelMultiplierNumerator;
    #     /* 0x30 */ u16 matchTrainerLevelMultiplierDenominator;
    #     /* 0x32 */ bool8 allowSkippingFanfares;
    # };
    options_address = data.rom_addresses["gArchipelagoOptions"]

    # Set Birch pokemon
    _set_bytes_le(
        patched_rom,
        options_address + 0x00,
        2,
        world.random.choice(list(data.species.keys()))
    )

    # Set hold A to advance text
    _set_bytes_le(patched_rom, options_address + 0x02, 1, 1 if world.options.turbo_a else 0)

    # Set receive item messages type
    _set_bytes_le(patched_rom, options_address + 0x03, 1, world.options.receive_item_messages.value)

    # Set better shops
    _set_bytes_le(patched_rom, options_address + 0x04, 1, 1 if world.options.better_shops else 0)

    # Set reusable TMs
    _set_bytes_le(patched_rom, options_address + 0x05, 1, 1 if world.options.reusable_tms_tutors else 0)

    # Set guaranteed catch
    _set_bytes_le(patched_rom, options_address + 0x06, 1, 1 if world.options.guaranteed_catch else 0)

    # Set purge spinners
    _set_bytes_le(patched_rom, options_address + 0x07, 1, 1 if world.options.purge_spinners else 0)

    # Set blind trainers
    _set_bytes_le(patched_rom, options_address + 0x08, 1, 1 if world.options.blind_trainers else 0)

    # Set exp modifier
    _set_bytes_le(patched_rom, options_address + 0x09, 2, min(max(world.options.exp_modifier.value, 0), 2**16 - 1))
    _set_bytes_le(patched_rom, options_address + 0x0B, 2, 100)

    # Set match trainer levels
    _set_bytes_le(patched_rom, options_address + 0x0D, 1, 1 if world.options.match_trainer_levels else 0)

    # Set match trainer levels bonus
    if world.options.match_trainer_levels == MatchTrainerLevels.option_additive:
        match_trainer_levels_bonus = max(min(world.options.match_trainer_levels_bonus.value, 100), -100)
        _set_bytes_le(patched_rom, options_address + 0x0E, 1, match_trainer_levels_bonus)  # Works with negatives
    elif world.options.match_trainer_levels == MatchTrainerLevels.option_multiplicative:
        _set_bytes_le(patched_rom, options_address + 0x2E, 2, world.options.match_trainer_levels_bonus.value + 100)
        _set_bytes_le(patched_rom, options_address + 0x30, 2, 100)

    # Set elite four requirement
    _set_bytes_le(
        patched_rom,
        options_address + 0x0F,
        1,
        1 if world.options.elite_four_requirement == EliteFourRequirement.option_gyms else 0
    )

    # Set elite four count
    _set_bytes_le(patched_rom, options_address + 0x10, 1, min(max(world.options.elite_four_count.value, 0), 8))

    # Set norman requirement
    _set_bytes_le(
        patched_rom,
        options_address + 0x11,
        1,
        1 if world.options.norman_requirement == NormanRequirement.option_gyms else 0
    )

    # Set norman count
    _set_bytes_le(patched_rom, options_address + 0x12, 1, min(max(world.options.norman_count.value, 0), 8))

    # Set starting badges
    _set_bytes_le(patched_rom, options_address + 0x13, 1, starting_badges)

    # Set HM badge requirements
    field_move_order = [
        "HM01 Cut",
        "HM05 Flash",
        "HM06 Rock Smash",
        "HM04 Strength",
        "HM03 Surf",
        "HM02 Fly",
        "HM08 Dive",
        "HM07 Waterfall",
    ]
    badge_to_bit = {
        "Stone Badge": 1 << 0,
        "Knuckle Badge": 1 << 1,
        "Dynamo Badge": 1 << 2,
        "Heat Badge": 1 << 3,
        "Balance Badge": 1 << 4,
        "Feather Badge": 1 << 5,
        "Mind Badge": 1 << 6,
        "Rain Badge": 1 << 7,
    }

    # Number of badges
    # Uses 4 bits per HM. 0-8 means it's a valid requirement, otherwise use specific badges.
    hm_badge_counts = 0
    for i, hm in enumerate(field_move_order):
        hm_badge_counts |= (world.hm_requirements[hm] if isinstance(world.hm_requirements[hm], int) else 0xF) << (i * 4)
    _set_bytes_le(patched_rom, options_address + 0x14, 4, hm_badge_counts)

    # Specific badges
    for i, hm in enumerate(field_move_order):
        if isinstance(world.hm_requirements, list):
            bitfield = 0
            for badge in world.hm_requirements:
                bitfield |= badge_to_bit[badge]
            _set_bytes_le(patched_rom, options_address + 0x18 + i, 1, bitfield)

    # Set terra/marine cave locations
    terra_cave_id = CAVE_EVENT_NAME_TO_ID[world.multiworld.get_location("TERRA_CAVE_LOCATION", world.player).item.name]
    marine_cave_id = CAVE_EVENT_NAME_TO_ID[world.multiworld.get_location("MARINE_CAVE_LOCATION", world.player).item.name]
    _set_bytes_le(patched_rom, options_address + 0x21, 1, terra_cave_id | (marine_cave_id << 4))

    # Set route 115 boulders
    _set_bytes_le(patched_rom, options_address + 0x22, 1, 1 if world.options.extra_boulders else 0)

    # Swap route 115 layout if bumpy slope enabled
    _set_bytes_le(patched_rom, options_address + 0x23, 1, 1 if world.options.extra_bumpy_slope else 0)

    # Swap route 115 layout if bumpy slope enabled
    _set_bytes_le(patched_rom, options_address + 0x24, 1, 1 if world.options.modify_118 else 0)

    # Set removed blockers
    removed_roadblocks = world.options.remove_roadblocks.value
    removed_roadblocks_bitfield = 0
    removed_roadblocks_bitfield |= (1 << 0) if "Safari Zone Construction Workers" in removed_roadblocks else 0
    removed_roadblocks_bitfield |= (1 << 1) if "Lilycove City Wailmer" in removed_roadblocks else 0
    removed_roadblocks_bitfield |= (1 << 2) if "Route 110 Aqua Grunts" in removed_roadblocks else 0
    removed_roadblocks_bitfield |= (1 << 3) if "Aqua Hideout Grunts" in removed_roadblocks else 0
    removed_roadblocks_bitfield |= (1 << 4) if "Route 119 Aqua Grunts" in removed_roadblocks else 0
    removed_roadblocks_bitfield |= (1 << 5) if "Route 112 Magma Grunts" in removed_roadblocks else 0
    removed_roadblocks_bitfield |= (1 << 6) if "Seafloor Cavern Aqua Grunt" in removed_roadblocks else 0
    _set_bytes_le(patched_rom, options_address + 0x25, 2, removed_roadblocks_bitfield)

    # Mark berry trees as randomized
    _set_bytes_le(patched_rom, options_address + 0x27, 1, 1 if world.options.berry_trees else 0)

    # Mark dexsanity as enabled
    _set_bytes_le(patched_rom, options_address + 0x28, 1, 1 if world.options.dexsanity else 0)

    # Mark trainersanity as enabled
    _set_bytes_le(patched_rom, options_address + 0x29, 1, 1 if world.options.trainersanity else 0)

    # Set easter egg data
    _set_bytes_le(patched_rom, options_address + 0x2B, 1, easter_egg[0])

    # Set normalize encounter rates
    _set_bytes_le(patched_rom, options_address + 0x2C, 1, 1 if world.options.normalize_encounter_rates else 0)

    # Set allow wonder trading
    _set_bytes_le(patched_rom, options_address + 0x2D, 1, 1 if world.options.enable_wonder_trading else 0)

    # Set allowed to skip fanfares
    _set_bytes_le(patched_rom, options_address + 0x32, 1, 1 if world.options.fanfares else 0)

    if easter_egg[0] == 2:
        _set_bytes_le(patched_rom, data.rom_addresses["gBattleMoves"] + (easter_egg[1] * 12) + 4, 1, 50)
        _set_bytes_le(patched_rom, data.rom_addresses["gBattleMoves"] + (data.constants["MOVE_CUT"] * 12) + 4, 1, 1)
        _set_bytes_le(patched_rom, data.rom_addresses["gBattleMoves"] + (data.constants["MOVE_FLY"] * 12) + 4, 1, 1)
        _set_bytes_le(patched_rom, data.rom_addresses["gBattleMoves"] + (data.constants["MOVE_SURF"] * 12) + 4, 1, 1)
        _set_bytes_le(patched_rom, data.rom_addresses["gBattleMoves"] + (data.constants["MOVE_STRENGTH"] * 12) + 4, 1, 1)
        _set_bytes_le(patched_rom, data.rom_addresses["gBattleMoves"] + (data.constants["MOVE_FLASH"] * 12) + 4, 1, 1)
        _set_bytes_le(patched_rom, data.rom_addresses["gBattleMoves"] + (data.constants["MOVE_ROCK_SMASH"] * 12) + 4, 1, 1)
        _set_bytes_le(patched_rom, data.rom_addresses["gBattleMoves"] + (data.constants["MOVE_WATERFALL"] * 12) + 4, 1, 1)
        _set_bytes_le(patched_rom, data.rom_addresses["gBattleMoves"] + (data.constants["MOVE_DIVE"] * 12) + 4, 1, 1)
        _set_bytes_le(patched_rom, data.rom_addresses["gBattleMoves"] + (data.constants["MOVE_DIG"] * 12) + 4, 1, 1)

    # Set slot auth
    for i, byte in enumerate(world.auth):
        _set_bytes_le(patched_rom, data.rom_addresses["gArchipelagoInfo"] + i, 1, byte)

    # Randomize music
    if world.options.music:
        # The "randomized sound table" is a patchboard that redirects sounds just before they get played
        randomized_looping_music = copy.copy(_LOOPING_MUSIC)
        world.random.shuffle(randomized_looping_music)
        for original_music, randomized_music in zip(_LOOPING_MUSIC, randomized_looping_music):
            _set_bytes_le(
                patched_rom,
                data.rom_addresses["gRandomizedSoundTable"] + (data.constants[original_music] * 2),
                2,
                data.constants[randomized_music]
            )

    # Randomize fanfares
    if world.options.fanfares:
        # Shuffle the lists, pair new tracks with original tracks, set the new track ids, and set new fanfare durations
        randomized_fanfares = [fanfare_name for fanfare_name in _FANFARES]
        world.random.shuffle(randomized_fanfares)
        for i, fanfare_pair in enumerate(zip(_FANFARES.keys(), randomized_fanfares)):
            _set_bytes_le(
                patched_rom,
                data.rom_addresses["gRandomizedSoundTable"] + (data.constants[fanfare_pair[0]] * 2),
                2,
                data.constants[fanfare_pair[1]]
            )
            _set_bytes_le(
                patched_rom,
                data.rom_addresses["sFanfares"] + (i * 4) + 2,
                2,
                _FANFARES[fanfare_pair[1]]
            )

    # Write Output
    out_file_name = world.multiworld.get_out_file_name_base(world.player)
    output_path = os.path.join(output_directory, f"{out_file_name}.gba")
    with open(output_path, "wb") as out_file:
        out_file.write(patched_rom)
    patch = PokemonEmeraldDeltaPatch(os.path.splitext(output_path)[0] + ".apemerald", player=world.player,
                                     player_name=world.multiworld.get_player_name(world.player),
                                     patched_path=output_path)

    patch.write()
    os.unlink(output_path)


def get_base_rom_as_bytes() -> bytes:
    with open(get_settings().pokemon_emerald_settings.rom_file, "rb") as infile:
        base_rom_bytes = bytes(infile.read())

    return base_rom_bytes


def _set_encounter_tables(world: "PokemonEmeraldWorld", rom: bytearray) -> None:
    """
    Encounter tables are lists of
    struct {
        min_level:  0x01 bytes,
        max_level:  0x01 bytes,
        species_id: 0x02 bytes
    }
    """
    for map_data in world.modified_maps.values():
        tables = [map_data.land_encounters, map_data.water_encounters, map_data.fishing_encounters]
        for table in tables:
            if table is not None:
                for i, species_id in enumerate(table.slots):
                    address = table.address + 2 + (4 * i)
                    _set_bytes_le(rom, address, 2, species_id)


def _set_species_info(world: "PokemonEmeraldWorld", rom: bytearray, easter_egg: Tuple[int, int]) -> None:
    for species in world.modified_species.values():
        _set_bytes_le(rom, species.address + 6, 1, species.types[0])
        _set_bytes_le(rom, species.address + 7, 1, species.types[1])
        _set_bytes_le(rom, species.address + 8, 1, species.catch_rate)
        _set_bytes_le(rom, species.address + 22, 1, species.abilities[0])
        _set_bytes_le(rom, species.address + 23, 1, species.abilities[1])

        if easter_egg[0] == 3:
            _set_bytes_le(rom, species.address + 22, 1, easter_egg[1])
            _set_bytes_le(rom, species.address + 23, 1, easter_egg[1])

        for i, learnset_move in enumerate(species.learnset):
            level_move = learnset_move.level << 9 | learnset_move.move_id
            if easter_egg[0] == 2:
                level_move = learnset_move.level << 9 | easter_egg[1]

            _set_bytes_le(rom, species.learnset_address + (i * 2), 2, level_move)


def _set_opponents(world: "PokemonEmeraldWorld", rom: bytearray, easter_egg: Tuple[int, int]) -> None:
    for trainer in world.modified_trainers:
        party_address = trainer.party.address

        pokemon_data_size: int
        if trainer.party.pokemon_data_type in {TrainerPokemonDataTypeEnum.NO_ITEM_DEFAULT_MOVES, TrainerPokemonDataTypeEnum.ITEM_DEFAULT_MOVES}:
            pokemon_data_size = 8
        else:  # Custom Moves
            pokemon_data_size = 16

        for i, pokemon in enumerate(trainer.party.pokemon):
            pokemon_address = party_address + (i * pokemon_data_size)

            # Replace species
            _set_bytes_le(rom, pokemon_address + 0x04, 2, pokemon.species_id)

            # Replace custom moves if applicable
            if trainer.party.pokemon_data_type == TrainerPokemonDataTypeEnum.NO_ITEM_CUSTOM_MOVES:
                if easter_egg[0] == 2:
                    _set_bytes_le(rom, pokemon_address + 0x06, 2, easter_egg[1])
                    _set_bytes_le(rom, pokemon_address + 0x08, 2, easter_egg[1])
                    _set_bytes_le(rom, pokemon_address + 0x0A, 2, easter_egg[1])
                    _set_bytes_le(rom, pokemon_address + 0x0C, 2, easter_egg[1])
                else:
                    _set_bytes_le(rom, pokemon_address + 0x06, 2, pokemon.moves[0])
                    _set_bytes_le(rom, pokemon_address + 0x08, 2, pokemon.moves[1])
                    _set_bytes_le(rom, pokemon_address + 0x0A, 2, pokemon.moves[2])
                    _set_bytes_le(rom, pokemon_address + 0x0C, 2, pokemon.moves[3])
            elif trainer.party.pokemon_data_type == TrainerPokemonDataTypeEnum.ITEM_CUSTOM_MOVES:
                if easter_egg[0] == 2:
                    _set_bytes_le(rom, pokemon_address + 0x08, 2, easter_egg[1])
                    _set_bytes_le(rom, pokemon_address + 0x0A, 2, easter_egg[1])
                    _set_bytes_le(rom, pokemon_address + 0x0C, 2, easter_egg[1])
                    _set_bytes_le(rom, pokemon_address + 0x0E, 2, easter_egg[1])
                else:
                    _set_bytes_le(rom, pokemon_address + 0x08, 2, pokemon.moves[0])
                    _set_bytes_le(rom, pokemon_address + 0x0A, 2, pokemon.moves[1])
                    _set_bytes_le(rom, pokemon_address + 0x0C, 2, pokemon.moves[2])
                    _set_bytes_le(rom, pokemon_address + 0x0E, 2, pokemon.moves[3])


def _set_legendary_encounters(world: "PokemonEmeraldWorld", rom: bytearray) -> None:
    for encounter in world.modified_legendary_encounters:
        _set_bytes_le(rom, encounter.address, 2, encounter.species_id)


def _set_misc_pokemon(world: "PokemonEmeraldWorld", rom: bytearray) -> None:
    for encounter in world.modified_misc_pokemon:
        _set_bytes_le(rom, encounter.address, 2, encounter.species_id)


def _set_starters(world: "PokemonEmeraldWorld", rom: bytearray) -> None:
    address = data.rom_addresses["sStarterMon"]
    (starter_1, starter_2, starter_3) = world.modified_starters

    _set_bytes_le(rom, address + 0, 2, starter_1)
    _set_bytes_le(rom, address + 2, 2, starter_2)
    _set_bytes_le(rom, address + 4, 2, starter_3)


def _set_tm_moves(world: "PokemonEmeraldWorld", rom: bytearray, easter_egg: Tuple[int, int]) -> None:
    tmhm_list_address = data.rom_addresses["sTMHMMoves"]

    for i, move in enumerate(world.modified_tmhm_moves):
        # Don't modify HMs
        if i >= 50:
            break

        _set_bytes_le(rom, tmhm_list_address + (i * 2), 2, move)
        if easter_egg[0] == 2:
            _set_bytes_le(rom, tmhm_list_address + (i * 2), 2, easter_egg[1])


def _set_tmhm_compatibility(world: "PokemonEmeraldWorld", rom: bytearray) -> None:
    learnsets_address = data.rom_addresses["gTMHMLearnsets"]

    for species in world.modified_species.values():
        _set_bytes_le(rom, learnsets_address + (species.species_id * 8), 8, species.tm_hm_compatibility)


def _randomize_opponent_battle_type(world: "PokemonEmeraldWorld", rom: bytearray) -> None:
    probability = world.options.double_battle_chance.value / 100

    battle_type_map = {
        0: 4,
        1: 8,
        2: 6,
        3: 13,
    }

    for trainer_data in data.trainers:
        if trainer_data.script_address != 0 and len(trainer_data.party.pokemon) > 1:
            original_battle_type = rom[trainer_data.script_address + 1]
            if original_battle_type in battle_type_map:  # Don't touch anything other than regular single battles
                if world.random.random() < probability:
                    # Set the trainer to be a double battle
                    _set_bytes_le(rom, trainer_data.address + 0x18, 1, 1)

                    # Swap the battle type in the script for the purpose of loading the right text
                    # and setting data to the right places
                    _set_bytes_le(
                        rom,
                        trainer_data.script_address + 1,
                        1,
                        battle_type_map[original_battle_type]
                    )


def _randomize_move_tutor_moves(world: "PokemonEmeraldWorld", rom: bytearray, easter_egg: Tuple[int, int]) -> None:
    if easter_egg[0] == 2:
        for i in range(30):
            _set_bytes_le(rom, data.rom_addresses["gTutorMoves"] + (i * 2), 2, easter_egg[1])
    else:
        if world.options.tm_tutor_moves:
            new_tutor_moves = []
            for i in range(30):
                new_move = get_random_move(world.random, set(new_tutor_moves) | world.blacklisted_moves | HM_MOVES)
                new_tutor_moves.append(new_move)

                _set_bytes_le(rom, data.rom_addresses["gTutorMoves"] + (i * 2), 2, new_move)

    # Always set Fortree move tutor to Dig
    _set_bytes_le(rom, data.rom_addresses["gTutorMoves"] + (24 * 2), 2, data.constants["MOVE_DIG"])

    # Modify compatibility
    if world.options.tm_tutor_compatibility.value != -1:
        for species in data.species.values():
            _set_bytes_le(
                rom,
                data.rom_addresses["sTutorLearnsets"] + (species.species_id * 4),
                4,
                bool_array_to_int([world.random.randrange(0, 100) < world.options.tm_tutor_compatibility.value for _ in range(32)])
            )
