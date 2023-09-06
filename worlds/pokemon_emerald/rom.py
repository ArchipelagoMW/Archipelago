"""
Classes and functions related to creating a ROM patch
"""
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
from .pokemon import get_random_species
from .util import encode_string, get_easter_egg


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


def generate_output(modified_data: PokemonEmeraldData, multiworld: MultiWorld, player: int, output_directory: str) -> None:
    base_rom = get_base_rom_as_bytes()
    base_patch = pkgutil.get_data(__name__, "data/base_patch.bsdiff4")
    patched_rom = bytearray(bsdiff4.patch(base_rom, base_patch))

    location_info: List[Tuple[int, int, str]] = []
    for location in multiworld.get_locations(player):
        # Set free fly location
        if location.address is None:
            if multiworld.free_fly_location[player] and location.name == "EVENT_VISITED_LITTLEROOT_TOWN":
                _set_bytes_little_endian(
                    patched_rom,
                    data.rom_addresses["gArchipelagoOptions"] + 0x16,
                    1,
                    multiworld.worlds[player].free_fly_location_id
                )
            continue

        if location.item is None:
            continue

        # Set local item values
        if not multiworld.remote_items[player] and location.item.player == player:
            _set_bytes_little_endian(patched_rom, location.rom_address, 2, reverse_offset_item_value(location.item.code))
        else:
            _set_bytes_little_endian(patched_rom, location.rom_address, 2, data.constants["ITEM_ARCHIPELAGO_PROGRESSION"])

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
    if multiworld.trainer_parties[player] != RandomizeTrainerParties.option_vanilla:
        _set_opponents(modified_data, patched_rom, easter_egg)

    # Set static pokemon
    _set_static_encounters(modified_data, patched_rom)

    # Set starters
    _set_starters(modified_data, patched_rom)

    # Set TM moves
    _set_tm_moves(modified_data, patched_rom, easter_egg)

    # Set TM/HM compatibility
    _set_tmhm_compatibility(modified_data, patched_rom)

    # Randomize opponent double or single
    _randomize_opponent_battle_type(multiworld, player, patched_rom)

    # Options
    # struct ArchipelagoOptions
    # {
    #     /* 0x00 */ bool8 advanceTextWithHoldA;
    #     /* 0x01 */ bool8 isFerryEnabled;
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
    #     /* 0x19 */ u8 matchTrainerLevelsMultiplierNumerator;
    #     /* 0x1B */ u8 matchTrainerLevelsMultiplierDenominator;
    # };
    options_address = data.rom_addresses["gArchipelagoOptions"]

    # Set hold A to advance text
    turbo_a = 1 if multiworld.turbo_a[player] else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x00, 1, turbo_a)

    # Set ferry enabled
    enable_ferry = 1 if multiworld.enable_ferry[player] else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x01, 1, enable_ferry)

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
    _set_bytes_little_endian(patched_rom, options_address + 0x08, 2, get_random_species(multiworld.per_slot_randoms[player], data.species).species_id)

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

    # Set match trainer levels multiplier
    match_trainer_levels_multiplier = min(max(multiworld.match_trainer_levels_multiplier[player].value, 0), 2**16 - 1)
    _set_bytes_little_endian(patched_rom, options_address + 0x19, 2, match_trainer_levels_multiplier)
    _set_bytes_little_endian(patched_rom, options_address + 0x1B, 2, 100)

    if easter_egg[0] == 2:
        _set_bytes_little_endian(patched_rom, data.rom_addresses["gBattleMoves"] + (easter_egg[1] * 12) + 4, 1, 50)

    # Set slot name
    for i, byte in enumerate(multiworld.player_name[player].encode("utf-8")):
        _set_bytes_little_endian(patched_rom, data.rom_addresses["gArchipelagoInfo"] + i, 1, byte)

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
                    address = table.rom_address + 2 + (4 * i)
                    _set_bytes_little_endian(rom, address, 2, species_id)


def _set_species_info(modified_data: PokemonEmeraldData, rom: bytearray, easter_egg: Tuple[int, int]) -> None:
    for species in modified_data.species:
        if species is not None:
            _set_bytes_little_endian(rom, species.rom_address + 6, 1, species.types[0])
            _set_bytes_little_endian(rom, species.rom_address + 7, 1, species.types[1])
            _set_bytes_little_endian(rom, species.rom_address + 8, 1, species.catch_rate)
            _set_bytes_little_endian(rom, species.rom_address + 22, 1, species.abilities[0])
            _set_bytes_little_endian(rom, species.rom_address + 23, 1, species.abilities[1])

            if easter_egg[0] == 3:
                _set_bytes_little_endian(rom, species.rom_address + 22, 1, easter_egg[1])
                _set_bytes_little_endian(rom, species.rom_address + 23, 1, easter_egg[1])

            for i, learnset_move in enumerate(species.learnset):
                level_move = learnset_move.level << 9 | learnset_move.move_id
                if easter_egg[0] == 2:
                    level_move = learnset_move.level << 9 | easter_egg[1]

                _set_bytes_little_endian(rom, species.learnset_rom_address + (i * 2), 2, level_move)


def _set_opponents(modified_data: PokemonEmeraldData, rom: bytearray, easter_egg: Tuple[int, int]) -> None:
    for trainer in modified_data.trainers:
        party_address = trainer.party.rom_address

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
        _set_bytes_little_endian(rom, encounter.rom_address, 2, encounter.species_id)


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
        if trainer_data.battle_script_rom_address != 0 and len(trainer_data.party.pokemon) > 1:
            if multiworld.per_slot_randoms[player].random() < probability:
                # Set the trainer to be a double battle
                _set_bytes_little_endian(rom, trainer_data.rom_address + 0x18, 1, 1)

                # Swap the battle type in the script for the purpose of loading the right text
                # and setting data to the right places
                original_battle_type = rom[trainer_data.battle_script_rom_address + 1]
                if original_battle_type in battle_type_map:
                    _set_bytes_little_endian(rom, trainer_data.battle_script_rom_address + 1, 1, battle_type_map[original_battle_type])
