"""
Classes and functions related to creating a ROM patch
"""
import copy
import os
import pkgutil
from typing import Dict, List, Tuple

import bsdiff4

from BaseClasses import MultiWorld
from worlds.Files import APDeltaPatch
from settings import get_settings

from .data import PokemonEmeraldData, TrainerPokemonDataTypeEnum, BASE_OFFSET, data
from .items import reverse_offset_item_value
from .options import RandomizeWildPokemon, RandomizeTrainerParties, EliteFourRequirement, NormanRequirement
from .pokemon import get_random_species, get_random_move
from .util import encode_string, get_easter_egg


_LOOPING_MUSIC = [
    "MUS_GSC_ROUTE38", "MUS_GSC_PEWTER", "MUS_ROUTE101", "MUS_ROUTE110", "MUS_ROUTE120", "MUS_ROUTE122",
    "MUS_PETALBURG", "MUS_OLDALE", "MUS_GYM", "MUS_SURF", "MUS_PETALBURG_WOODS", "MUS_LEVEL_UP", "MUS_LILYCOVE_MUSEUM",
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
    "MUS_ENCOUNTER_INTERVIEWER", "MUS_ENCOUNTER_CHAMPION", "MUS_END", "MUS_B_FRONTIER", "MUS_B_ARENA", "MUS_B_PYRAMID",
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
    "MUS_RG_ENCOUNTER_DEOXYS", "MUS_RG_TRAINER_TOWER", "MUS_RG_SLOW_PALLET", "MUS_RG_TEACHY_TV_MENU"
]

_FANFARES = [
    "MUS_OBTAIN_BADGE", "MUS_OBTAIN_ITEM", "MUS_EVOLVED", "MUS_OBTAIN_TMHM", "MUS_OBTAIN_BERRY", "MUS_HEAL",
    "MUS_MOVE_DELETED", "MUS_TOO_BAD", "MUS_OBTAIN_B_POINTS", "MUS_REGISTER_MATCH_CALL", "MUS_OBTAIN_SYMBOL",
    "MUS_RG_JIGGLYPUFF", "MUS_RG_HEAL", "MUS_RG_DEX_RATING", "MUS_RG_OBTAIN_KEY_ITEM", "MUS_RG_CAUGHT_INTRO",
    "MUS_RG_PHOTO", "MUS_RG_POKE_FLUTE"
]



class PokemonEmeraldDeltaPatch(APDeltaPatch):
    game = "Pokemon Emerald"
    hash = "605b89b67018abcea91e693a4dd25be3"
    patch_file_ending = ".apemerald"
    result_file_ending = ".gba"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()


location_visited_event_to_id_map = {
    "EVENT_VISITED_LITTLEROOT_TOWN": 0,
    "EVENT_VISITED_OLDALE_TOWN": 1,
    "EVENT_VISITED_PETALBURG_CITY": 2,
    "EVENT_VISITED_RUSTBORO_CITY": 3,
    "EVENT_VISITED_DEWFORD_TOWN": 4,
    "EVENT_VISITED_SLATEPORT_CITY": 5,
    "EVENT_VISITED_MAUVILLE_CITY": 6,
    "EVENT_VISITED_VERDANTURF_TOWN": 7,
    "EVENT_VISITED_FALLARBOR_TOWN": 8,
    "EVENT_VISITED_LAVARIDGE_TOWN": 9,
    "EVENT_VISITED_FORTREE_CITY": 10,
    "EVENT_VISITED_LILYCOVE_CITY": 11,
    "EVENT_VISITED_MOSSDEEP_CITY": 12,
    "EVENT_VISITED_SOOTOPOLIS_CITY": 13,
    "EVENT_VISITED_PACIFIDLOG_TOWN": 14,
    "EVENT_VISITED_EVER_GRANDE_CITY": 15,
    "EVENT_VISITED_BATTLE_FRONTIER": 16,
    "EVENT_VISITED_SOUTHERN_ISLAND": 17
}

cave_event_to_id_map = {
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
    "MARINE_CAVE_ROUTE_129_2": 16
}


def generate_output(modified_data: PokemonEmeraldData, multiworld: MultiWorld, player: int, output_directory: str) -> None:
    base_rom = get_base_rom_as_bytes()
    base_patch = pkgutil.get_data(__name__, "data/base_patch.bsdiff4")
    patched_rom = bytearray(bsdiff4.patch(base_rom, base_patch))

    # Set free fly location
    if multiworld.free_fly_location[player]:
        _set_bytes_little_endian(
            patched_rom,
            data.rom_addresses["gArchipelagoOptions"] + 0x16,
            1,
            multiworld.worlds[player].free_fly_location_id
        )

    location_info: List[Tuple[int, int, str]] = []
    for location in multiworld.get_locations(player):
        if location.address is None:
            continue

        if location.item is None:
            continue

        # Set local item values
        if not multiworld.remote_items[player] and location.item.player == player:
            if type(location.item_address) is int:
                _set_bytes_little_endian(
                    patched_rom,
                    location.item_address,
                    2,
                    reverse_offset_item_value(location.item.code)
                )
            elif type(location.item_address) is list:
                for address in location.item_address:
                    _set_bytes_little_endian(patched_rom, address, 2, reverse_offset_item_value(location.item.code))
        else:
            if type(location.item_address) is int:
                _set_bytes_little_endian(
                    patched_rom,
                    location.item_address,
                    2,
                    data.constants["ITEM_ARCHIPELAGO_PROGRESSION"]
                )
            elif type(location.item_address) is list:
                for address in location.item_address:
                    _set_bytes_little_endian(patched_rom, address, 2, data.constants["ITEM_ARCHIPELAGO_PROGRESSION"])

            # Creates a list of item information to store in tables later. Those tables are used to display the item and
            # player name in a text box. In the case of not enough space, the game will default to "found an ARCHIPELAGO
            # ITEM"
            location_info.append((location.address - BASE_OFFSET, location.item.player, location.item.name))

    player_name_ids: Dict[str, int] = {multiworld.player_name[player]: 0}
    item_name_offsets: Dict[str, int] = {}
    next_item_name_offset = 0
    for i, (flag, item_player, item_name) in enumerate(sorted(location_info, key=lambda t: t[0])):
        # The player's own items are still set in the table with the value 0 to indicate the game should not show any
        # message (the message for receiving an item will pop up when the client eventually gives it to them).
        # In race mode, no item location data is included, and only recieved (or own) items will show any text box.
        if item_player == player or multiworld.is_race:
            _set_bytes_little_endian(patched_rom, data.rom_addresses["gArchipelagoNameTable"] + (i * 5) + 0, 2, flag)
            _set_bytes_little_endian(patched_rom, data.rom_addresses["gArchipelagoNameTable"] + (i * 5) + 2, 2, 0)
            _set_bytes_little_endian(patched_rom, data.rom_addresses["gArchipelagoNameTable"] + (i * 5) + 4, 1, 0)
        else:
            player_name = multiworld.player_name[item_player]

            if player_name not in player_name_ids:
                # Only space for 50 player names
                if len(player_name_ids) >= 50:
                    continue

                player_name_ids[player_name] = len(player_name_ids)
                for j, b in enumerate(encode_string(player_name, 17)):
                    _set_bytes_little_endian(
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
                    _set_bytes_little_endian(
                        patched_rom,
                        data.rom_addresses["gArchipelagoItemNames"] + (item_name_offsets[item_name]) + j,
                        1,
                        b
                    )

            # There should always be enough space for one entry per location
            _set_bytes_little_endian(patched_rom, data.rom_addresses["gArchipelagoNameTable"] + (i * 5) + 0, 2, flag)
            _set_bytes_little_endian(patched_rom, data.rom_addresses["gArchipelagoNameTable"] + (i * 5) + 2, 2, item_name_offsets[item_name])
            _set_bytes_little_endian(patched_rom, data.rom_addresses["gArchipelagoNameTable"] + (i * 5) + 4, 1, player_name_ids[player_name])

    easter_egg = get_easter_egg(multiworld.easter_egg[player].value)

    # Set start inventory
    start_inventory = multiworld.start_inventory[player].value.copy()

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
        item = reverse_offset_item_value(multiworld.worlds[player].item_name_to_id[slot[0]])
        _set_bytes_little_endian(patched_rom, address + 0, 2, item)
        _set_bytes_little_endian(patched_rom, address + 2, 2, slot[1])

    # Set species data
    _set_species_info(modified_data, patched_rom, easter_egg)

    # Set encounter tables
    if multiworld.wild_pokemon[player] != RandomizeWildPokemon.option_vanilla:
        _set_encounter_tables(modified_data, patched_rom)

    # Set opponent data
    if multiworld.trainer_parties[player] != RandomizeTrainerParties.option_vanilla or easter_egg[0] == 2:
        _set_opponents(modified_data, patched_rom, easter_egg)

    # Set static pokemon
    _set_static_encounters(modified_data, patched_rom)

    # Set starters
    _set_starters(modified_data, patched_rom)

    # Set TM moves
    _set_tm_moves(modified_data, patched_rom, easter_egg)

    # Randomize move tutor moves
    if multiworld.move_tutor_moves[player] or easter_egg[0] == 2:
        _randomize_move_tutor_moves(multiworld, player, patched_rom, easter_egg)

    # Set TM/HM compatibility
    _set_tmhm_compatibility(modified_data, patched_rom)

    # Randomize opponent double or single
    _randomize_opponent_battle_type(multiworld, player, patched_rom)

    # Options
    # struct ArchipelagoOptions
    # {
    #     /* 0x00 */ bool8 advanceTextWithHoldA;
    #     /* 0x01 */ u8 terraCaveLocationId:4;
    #                u8 marineCaveLocationId:4;
    #     /* 0x02 */ bool8 areTrainersBlind;
    #     /* 0x03 */ bool8 canFlyWithoutBadge;
    #     /* 0x04 */ u16 expMultiplierNumerator;
    #     /* 0x06 */ u16 expMultiplierDenominator;
    #     /* 0x08 */ u16 birchPokemon;
    #     /* 0x0A */ bool8 guaranteedCatch;
    #     /* 0x0B */ bool8 betterShopsEnabled;
    #     /* 0x0C */ bool8 eliteFourRequiresGyms;
    #     /* 0x0D */ u8 eliteFourRequiredCount;
    #     /* 0x0E */ bool8 normanRequiresGyms;
    #     /* 0x0F */ u8 normanRequiredCount;
    #     /* 0x10 */ u8 startingBadges;
    #     /* 0x11 */ u8 receivedItemMessageFilter; // 0 = Show All; 1 = Show Progression Only; 2 = Show None
    #     /* 0x12 */ bool8 reusableTms;
    #     /* 0x14 */ u16 removedBlockers;
    #     /* 0x13 */ bool8 addRoute115Boulders;
    #     /* 0x14 */ u16 removedBlockers;
    #     /* 0x14 */ u16 removedBlockers;
    #     /* 0x16 */ u8 freeFlyLocation;
    #     /* 0x17 */ bool8 matchTrainerLevels;
    #     /* 0x18 */ u8 activeEasterEgg;
    #     /* 0x19 */ u16 matchTrainerLevelsMultiplierNumerator;
    #     /* 0x1B */ u16 matchTrainerLevelsMultiplierDenominator;
    #     /* 0x1D */ u8 berryTreesRandomized;
    # };
    options_address = data.rom_addresses["gArchipelagoOptions"]

    # Set hold A to advance text
    turbo_a = 1 if multiworld.turbo_a[player] else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x00, 1, turbo_a)

    # Set terra/marine cave locations
    terra_cave_id = cave_event_to_id_map[multiworld.get_location("TERRA_CAVE_LOCATION", player).item.name]
    marine_cave_id = cave_event_to_id_map[multiworld.get_location("MARINE_CAVE_LOCATION", player).item.name]
    _set_bytes_little_endian(patched_rom, options_address + 0x01, 1, marine_cave_id & (terra_cave_id << 4))

    # Set blind trainers
    blind_trainers = 1 if multiworld.blind_trainers[player] else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x02, 1, blind_trainers)

    # Set fly without badge
    fly_without_badge = 1 if multiworld.fly_without_badge[player] else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x03, 1, fly_without_badge)

    # Set exp modifier
    numerator = min(max(multiworld.exp_modifier[player].value, 0), 2**16 - 1)
    _set_bytes_little_endian(patched_rom, options_address + 0x04, 2, numerator)
    _set_bytes_little_endian(patched_rom, options_address + 0x06, 2, 100)

    # Set Birch pokemon
    _set_bytes_little_endian(
        patched_rom,
        options_address + 0x08,
        2,
        get_random_species(multiworld.per_slot_randoms[player], data.species).species_id
    )

    # Set guaranteed catch
    guaranteed_catch = 1 if multiworld.guaranteed_catch[player] else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x0A, 1, guaranteed_catch)

    # Set better shops
    better_shops = 1 if multiworld.better_shops[player] else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x0B, 1, better_shops)

    # Set elite four requirement
    elite_four_requires_gyms = 1 if multiworld.elite_four_requirement[player] == EliteFourRequirement.option_gyms else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x0C, 1, elite_four_requires_gyms)

    # Set elite four count
    elite_four_count = min(max(multiworld.elite_four_count[player].value, 0), 8)
    _set_bytes_little_endian(patched_rom, options_address + 0x0D, 1, elite_four_count)

    # Set norman requirement
    norman_requires_gyms = 1 if multiworld.norman_requirement[player] == NormanRequirement.option_gyms else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x0E, 1, norman_requires_gyms)

    # Set norman count
    norman_count = min(max(multiworld.norman_count[player].value, 0), 8)
    _set_bytes_little_endian(patched_rom, options_address + 0x0F, 1, norman_count)

    # Set starting badges
    _set_bytes_little_endian(patched_rom, options_address + 0x10, 1, starting_badges)

    # Set receive item messages type
    receive_item_messages_type = multiworld.receive_item_messages[player].value
    _set_bytes_little_endian(patched_rom, options_address + 0x11, 1, receive_item_messages_type)

    # Set reusable TMs
    reusable_tms = 1 if multiworld.reusable_tms[player] else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x12, 1, reusable_tms)

    # Set route 115 boulders
    route_115_boulders = 1 if multiworld.extra_boulders[player] else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x13, 1, route_115_boulders)

    # Set removed blockers
    list_of_removed_roadblocks = multiworld.remove_roadblocks[player].value
    removed_roadblocks = 0
    removed_roadblocks |= (1 << 0) if "Safari Zone Construction Workers" in list_of_removed_roadblocks else 0
    removed_roadblocks |= (1 << 1) if "Lilycove City Wailmer" in list_of_removed_roadblocks else 0
    removed_roadblocks |= (1 << 2) if "Route 110 Aqua Grunts" in list_of_removed_roadblocks else 0
    removed_roadblocks |= (1 << 3) if "Aqua Hideout Grunts" in list_of_removed_roadblocks else 0
    removed_roadblocks |= (1 << 4) if "Route 119 Aqua Grunts" in list_of_removed_roadblocks else 0
    removed_roadblocks |= (1 << 5) if "Route 112 Magma Grunts" in list_of_removed_roadblocks else 0
    removed_roadblocks |= (1 << 6) if "Seafloor Cavern Aqua Grunt" in list_of_removed_roadblocks else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x14, 2, removed_roadblocks)

    # Set match trainer levels
    match_trainer_levels = 1 if multiworld.match_trainer_levels[player] else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x17, 1, match_trainer_levels)

    # Set easter egg data
    _set_bytes_little_endian(patched_rom, options_address + 0x18, 1, easter_egg[0])

    if easter_egg[0] == 2:
        _set_bytes_little_endian(patched_rom, data.rom_addresses["gBattleMoves"] + (easter_egg[1] * 12) + 4, 1, 50)
        _set_bytes_little_endian(patched_rom, data.rom_addresses["gBattleMoves"] + (data.constants["MOVE_CUT"] * 12) + 4, 1, 1)
        _set_bytes_little_endian(patched_rom, data.rom_addresses["gBattleMoves"] + (data.constants["MOVE_FLY"] * 12) + 4, 1, 1)
        _set_bytes_little_endian(patched_rom, data.rom_addresses["gBattleMoves"] + (data.constants["MOVE_SURF"] * 12) + 4, 1, 1)
        _set_bytes_little_endian(patched_rom, data.rom_addresses["gBattleMoves"] + (data.constants["MOVE_STRENGTH"] * 12) + 4, 1, 1)
        _set_bytes_little_endian(patched_rom, data.rom_addresses["gBattleMoves"] + (data.constants["MOVE_FLASH"] * 12) + 4, 1, 1)
        _set_bytes_little_endian(patched_rom, data.rom_addresses["gBattleMoves"] + (data.constants["MOVE_ROCK_SMASH"] * 12) + 4, 1, 1)
        _set_bytes_little_endian(patched_rom, data.rom_addresses["gBattleMoves"] + (data.constants["MOVE_WATERFALL"] * 12) + 4, 1, 1)
        _set_bytes_little_endian(patched_rom, data.rom_addresses["gBattleMoves"] + (data.constants["MOVE_DIVE"] * 12) + 4, 1, 1)

    # Set match trainer levels multiplier
    match_trainer_levels_multiplier = min(max(multiworld.match_trainer_levels_multiplier[player].value, 0), 2**16 - 1)
    _set_bytes_little_endian(patched_rom, options_address + 0x19, 2, match_trainer_levels_multiplier)
    _set_bytes_little_endian(patched_rom, options_address + 0x1B, 2, 100)

    # Mark berry trees as randomized
    berry_trees = 1 if multiworld.berry_trees[player] else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x1D, 1, berry_trees)

    # Swap route 115 layout if bumpy slope enabled
    if multiworld.extra_bumpy_slope[player]:
        _set_bytes_little_endian(
            patched_rom,
            [map_data for map_data in modified_data.maps if map_data.name == "MAP_ROUTE115"][0].header_address + 0x12,
            2,
            442  # Id of alternate Route 115 map layout; don't want to add >400 new constants for one value
        )

    # Set slot name
    for i, byte in enumerate(multiworld.player_name[player].encode("utf-8")):
        _set_bytes_little_endian(patched_rom, data.rom_addresses["gArchipelagoInfo"] + i, 1, byte)

    # Randomize music
    if multiworld.music[player]:
        randomized_looping_music = copy.copy(_LOOPING_MUSIC)
        multiworld.worlds[player].random.shuffle(randomized_looping_music)
        for original_music, randomized_music in zip(_LOOPING_MUSIC, randomized_looping_music):
            _set_bytes_little_endian(
                patched_rom,
                data.rom_addresses["gRandomizedSoundTable"] + (data.constants[original_music] * 2),
                2,
                data.constants[randomized_music]
            )

    # Randomize fanfares
    if multiworld.fanfares[player]:
        randomized_fanfares = copy.copy(_FANFARES)
        multiworld.worlds[player].random.shuffle(randomized_fanfares)
        for original_fanfare, randomized_fanfare in zip(_FANFARES, randomized_fanfares):
            _set_bytes_little_endian(
                patched_rom,
                data.rom_addresses["gRandomizedSoundTable"] + (data.constants[original_fanfare] * 2),
                2,
                data.constants[randomized_fanfare]
            )

    # Write Output
    outfile_player_name = f"_P{player}"
    outfile_player_name += f"_{multiworld.get_file_safe_player_name(player).replace(' ', '_')}" \
        if multiworld.player_name[player] != f"Player{player}" else ""

    output_path = os.path.join(output_directory, f"AP_{multiworld.seed_name}{outfile_player_name}.gba")
    with open(output_path, "wb") as outfile:
        outfile.write(patched_rom)
    patch = PokemonEmeraldDeltaPatch(os.path.splitext(output_path)[0] + ".apemerald", player=player,
                                     player_name=multiworld.player_name[player], patched_path=output_path)

    patch.write()
    os.unlink(output_path)


def get_base_rom_as_bytes() -> bytes:
    with open(get_settings().pokemon_emerald_settings.rom_file, "rb") as infile:
        base_rom_bytes = bytes(infile.read())

    return base_rom_bytes


def _set_bytes_little_endian(byte_array: bytearray, address: int, size: int, value: int) -> None:
    offset = 0
    while size > 0:
        byte_array[address + offset] = value & 0xFF
        value = value >> 8
        offset += 1
        size -= 1


def _set_encounter_tables(modified_data: PokemonEmeraldData, rom: bytearray) -> None:
    """
    Encounter tables are lists of
    struct {
        min_level:  0x01 bytes,
        max_level:  0x01 bytes,
        species_id: 0x02 bytes
    }
    """

    for map_data in modified_data.maps:
        tables = [map_data.land_encounters, map_data.water_encounters, map_data.fishing_encounters]
        for table in tables:
            if table is not None:
                for i, species_id in enumerate(table.slots):
                    address = table.address + 2 + (4 * i)
                    _set_bytes_little_endian(rom, address, 2, species_id)


def _set_species_info(modified_data: PokemonEmeraldData, rom: bytearray, easter_egg: Tuple[int, int]) -> None:
    for species in modified_data.species:
        if species is not None:
            _set_bytes_little_endian(rom, species.address + 6, 1, species.types[0])
            _set_bytes_little_endian(rom, species.address + 7, 1, species.types[1])
            _set_bytes_little_endian(rom, species.address + 8, 1, species.catch_rate)
            _set_bytes_little_endian(rom, species.address + 22, 1, species.abilities[0])
            _set_bytes_little_endian(rom, species.address + 23, 1, species.abilities[1])

            if easter_egg[0] == 3:
                _set_bytes_little_endian(rom, species.address + 22, 1, easter_egg[1])
                _set_bytes_little_endian(rom, species.address + 23, 1, easter_egg[1])

            for i, learnset_move in enumerate(species.learnset):
                level_move = learnset_move.level << 9 | learnset_move.move_id
                if easter_egg[0] == 2:
                    level_move = learnset_move.level << 9 | easter_egg[1]

                _set_bytes_little_endian(rom, species.learnset_address + (i * 2), 2, level_move)


def _set_opponents(modified_data: PokemonEmeraldData, rom: bytearray, easter_egg: Tuple[int, int]) -> None:
    for trainer in modified_data.trainers:
        party_address = trainer.party.address

        pokemon_data_size: int
        if trainer.party.pokemon_data_type in {TrainerPokemonDataTypeEnum.NO_ITEM_DEFAULT_MOVES, TrainerPokemonDataTypeEnum.ITEM_DEFAULT_MOVES}:
            pokemon_data_size = 8
        else:  # Custom Moves
            pokemon_data_size = 16

        for i, pokemon in enumerate(trainer.party.pokemon):
            pokemon_address = party_address + (i * pokemon_data_size)

            # Replace species
            _set_bytes_little_endian(rom, pokemon_address + 0x04, 2, pokemon.species_id)

            # Replace custom moves if applicable
            if trainer.party.pokemon_data_type == TrainerPokemonDataTypeEnum.NO_ITEM_CUSTOM_MOVES:
                if easter_egg[0] == 2:
                    _set_bytes_little_endian(rom, pokemon_address + 0x06, 2, easter_egg[1])
                    _set_bytes_little_endian(rom, pokemon_address + 0x08, 2, easter_egg[1])
                    _set_bytes_little_endian(rom, pokemon_address + 0x0A, 2, easter_egg[1])
                    _set_bytes_little_endian(rom, pokemon_address + 0x0C, 2, easter_egg[1])
                else:
                    _set_bytes_little_endian(rom, pokemon_address + 0x06, 2, pokemon.moves[0])
                    _set_bytes_little_endian(rom, pokemon_address + 0x08, 2, pokemon.moves[1])
                    _set_bytes_little_endian(rom, pokemon_address + 0x0A, 2, pokemon.moves[2])
                    _set_bytes_little_endian(rom, pokemon_address + 0x0C, 2, pokemon.moves[3])
            elif trainer.party.pokemon_data_type == TrainerPokemonDataTypeEnum.ITEM_CUSTOM_MOVES:
                if easter_egg[0] == 2:
                    _set_bytes_little_endian(rom, pokemon_address + 0x08, 2, easter_egg[1])
                    _set_bytes_little_endian(rom, pokemon_address + 0x0A, 2, easter_egg[1])
                    _set_bytes_little_endian(rom, pokemon_address + 0x0C, 2, easter_egg[1])
                    _set_bytes_little_endian(rom, pokemon_address + 0x0E, 2, easter_egg[1])
                else:
                    _set_bytes_little_endian(rom, pokemon_address + 0x08, 2, pokemon.moves[0])
                    _set_bytes_little_endian(rom, pokemon_address + 0x0A, 2, pokemon.moves[1])
                    _set_bytes_little_endian(rom, pokemon_address + 0x0C, 2, pokemon.moves[2])
                    _set_bytes_little_endian(rom, pokemon_address + 0x0E, 2, pokemon.moves[3])


def _set_static_encounters(modified_data: PokemonEmeraldData, rom: bytearray) -> None:
    for encounter in modified_data.static_encounters:
        _set_bytes_little_endian(rom, encounter.address, 2, encounter.species_id)


def _set_starters(modified_data: PokemonEmeraldData, rom: bytearray) -> None:
    address = data.rom_addresses["sStarterMon"]
    (starter_1, starter_2, starter_3) = modified_data.starters

    _set_bytes_little_endian(rom, address + 0, 2, starter_1)
    _set_bytes_little_endian(rom, address + 2, 2, starter_2)
    _set_bytes_little_endian(rom, address + 4, 2, starter_3)


def _set_tm_moves(modified_data: PokemonEmeraldData, rom: bytearray, easter_egg: Tuple[int, int]) -> None:
    tmhm_list_address = data.rom_addresses["sTMHMMoves"]

    for i, move in enumerate(modified_data.tmhm_moves):
        # Don't modify HMs
        if i >= 50:
            break

        _set_bytes_little_endian(rom, tmhm_list_address + (i * 2), 2, move)
        if easter_egg[0] == 2:
            _set_bytes_little_endian(rom, tmhm_list_address + (i * 2), 2, easter_egg[1])


def _set_tmhm_compatibility(modified_data: PokemonEmeraldData, rom: bytearray) -> None:
    learnsets_address = data.rom_addresses["gTMHMLearnsets"]

    for species in modified_data.species:
        if species is not None:
            _set_bytes_little_endian(rom, learnsets_address + (species.species_id * 8), 8, species.tm_hm_compatibility)


def _randomize_opponent_battle_type(multiworld: MultiWorld, player: int, rom: bytearray) -> None:
    probability = multiworld.double_battle_chance[player].value / 100

    battle_type_map = {
        0: 4,
        1: 8,
        2: 6,
        3: 13,
    }

    for trainer_data in data.trainers:
        if trainer_data.script_address != 0 and len(trainer_data.party.pokemon) > 1:
            if multiworld.per_slot_randoms[player].random() < probability:
                # Set the trainer to be a double battle
                _set_bytes_little_endian(rom, trainer_data.address + 0x18, 1, 1)

                # Swap the battle type in the script for the purpose of loading the right text
                # and setting data to the right places
                original_battle_type = rom[trainer_data.script_address + 1]
                if original_battle_type in battle_type_map:
                    _set_bytes_little_endian(
                        rom,
                        trainer_data.script_address + 1,
                        1,
                        battle_type_map[original_battle_type]
                    )


def _randomize_move_tutor_moves(multiworld: MultiWorld, player: int, rom: bytearray, easter_egg: Tuple[int, int]) -> None:
    for i in range(30):
        if easter_egg[0] == 2:
            _set_bytes_little_endian(rom, data.rom_addresses["gTutorMoves"] + (i * 2), 2, easter_egg[1])
        else:
            _set_bytes_little_endian(
                rom,
                data.rom_addresses["gTutorMoves"] + (i * 2),
                2,
                get_random_move(multiworld.worlds[player].random, {data.constants["MOVE_CUT"],
                                                                   data.constants["MOVE_FLY"],
                                                                   data.constants["MOVE_SURF"],
                                                                   data.constants["MOVE_STRENGTH"],
                                                                   data.constants["MOVE_FLASH"],
                                                                   data.constants["MOVE_ROCK_SMASH"],
                                                                   data.constants["MOVE_WATERFALL"],
                                                                   data.constants["MOVE_DIVE"]})
            )
