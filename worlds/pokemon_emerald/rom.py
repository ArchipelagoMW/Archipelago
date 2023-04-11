"""
Classes and functions related to creating a ROM patch
"""
from typing import Dict, List
import os

import bsdiff4

from BaseClasses import MultiWorld
from Options import Toggle
from Patch import APDeltaPatch
import Utils

from .data import SpeciesData, TrainerPokemonDataTypeEnum, data
from .items import reverse_offset_item_value
from .options import (RandomizeWildPokemon, RandomizeStarters, RandomizeTrainerParties, TmCompatibility,
    HmCompatibility, LevelUpMoves, EliteFourRequirement, NormanRequirement, get_option_value)
from .pokemon import (get_random_species, get_species_by_id, get_species_by_name,
    get_random_damaging_move, get_random_move)


class PokemonEmeraldDeltaPatch(APDeltaPatch):
    game = "Pokemon Emerald"
    hash = "605b89b67018abcea91e693a4dd25be3"
    patch_file_ending = ".apemerald"
    result_file_ending = ".gba"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()


def generate_output(multiworld: MultiWorld, player: int, output_directory: str) -> None:
    base_rom = get_base_rom_as_bytes()
    with open(os.path.join(os.path.dirname(__file__), "data/base_patch.bsdiff4"), "rb") as stream:
        base_patch = bytes(stream.read())
        patched_rom = bytearray(bsdiff4.patch(base_rom, base_patch))

    # Set item values
    for location in multiworld.get_locations(player):
        if location.is_event:
            continue

        if location.item and location.item.player == player:
            _set_bytes_little_endian(patched_rom, location.rom_address, 2, reverse_offset_item_value(location.item.code))
        else:
            _set_bytes_little_endian(patched_rom, location.rom_address, 2, data.constants["ITEM_ARCHIPELAGO_PROGRESSION"])

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

    for i, item_name in enumerate(start_inventory):
        if i >= 20:
            break

        address = data.rom_addresses["sNewGamePCItems"] + (i * 4)
        item = reverse_offset_item_value(multiworld.worlds[player].item_name_to_id[item_name])
        quantity = min(start_inventory[item_name], 99)
        _set_bytes_little_endian(patched_rom, address + 0, 2, item)
        _set_bytes_little_endian(patched_rom, address + 2, 2, quantity)

    # Randomize encounter tables
    if get_option_value(multiworld, player, "wild_pokemon") != RandomizeWildPokemon.option_vanilla:
        _randomize_encounter_tables(multiworld, player, patched_rom)

    # Randomize abilities
    if get_option_value(multiworld, player, "abilities") == Toggle.option_true:
        _randomize_abilities(multiworld, player, patched_rom)

    # Randomize TM moves
    if get_option_value(multiworld, player, "tm_moves") == Toggle.option_true:
        _randomize_tm_moves(multiworld, player, patched_rom)

    # Randomize learnsets
    if get_option_value(multiworld, player, "level_up_moves") != LevelUpMoves.option_vanilla:
        _randomize_learnsets(multiworld, player, patched_rom)

    # Randomize opponents
    if get_option_value(multiworld, player, "trainer_parties") != RandomizeTrainerParties.option_vanilla:
        _randomize_opponents(multiworld, player, patched_rom)

    # Randomize opponent double or single
    _randomize_opponent_battle_type(multiworld, player, patched_rom)

    # Randomize starters
    if get_option_value(multiworld, player, "starters") != RandomizeStarters.option_vanilla:
        _randomize_starters(multiworld, player, patched_rom)

    # Modify species
    _modify_species_info(multiworld, player, patched_rom)

    # Modify TM/HM compatibility
    _modify_tmhm_compatibility(multiworld, player, patched_rom)

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
    # };
    options_address = data.rom_addresses["gArchipelagoOptions"]

    # Set hold A to advance text
    turbo_a = 1 if get_option_value(multiworld, player, "turbo_a") == Toggle.option_true else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x00, 1, turbo_a)

    # Set ferry enabled
    enable_ferry = 1 if get_option_value(multiworld, player, "enable_ferry") == Toggle.option_true else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x01, 1, enable_ferry)

    # Set blind trainers
    blind_trainers = 1 if get_option_value(multiworld, player, "blind_trainers") == Toggle.option_true else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x02, 1, blind_trainers)

    # Set fly without badge
    fly_without_badge = 1 if get_option_value(multiworld, player, "fly_without_badge") == Toggle.option_true else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x03, 1, fly_without_badge)

    # Set exp modifier
    numerator = min(max(get_option_value(multiworld, player, "exp_modifier"), 0), 2**16 - 1)
    _set_bytes_little_endian(patched_rom, options_address + 0x04, 2, numerator)
    _set_bytes_little_endian(patched_rom, options_address + 0x06, 2, 100)

    # Set Birch pokemon
    _set_bytes_little_endian(patched_rom, options_address + 0x08, 2, get_random_species(multiworld.per_slot_randoms[player]).species_id)

    # Set guaranteed catch
    guaranteed_catch = 1 if get_option_value(multiworld, player, "guaranteed_catch") == Toggle.option_true else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x0A, 1, guaranteed_catch)

    # Set better shops
    better_shops = 1 if get_option_value(multiworld, player, "better_shops") == Toggle.option_true else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x0B, 1, better_shops)

    # Set elite four requirement
    elite_four_requires_gyms = 1 if get_option_value(multiworld, player, "elite_four_requirement") == EliteFourRequirement.option_gyms else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x0C, 1, elite_four_requires_gyms)

    # Set elite four count
    elite_four_count = min(max(get_option_value(multiworld, player, "elite_four_count"), 0), 8)
    _set_bytes_little_endian(patched_rom, options_address + 0x0D, 1, elite_four_count)

    # Set norman requirement
    norman_requires_gyms = 1 if get_option_value(multiworld, player, "norman_requirement") == NormanRequirement.option_gyms else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x0E, 1, norman_requires_gyms)

    # Set norman count
    norman_count = min(max(get_option_value(multiworld, player, "norman_count"), 0), 8)
    _set_bytes_little_endian(patched_rom, options_address + 0x0F, 1, norman_count)

    # Set starting badges
    _set_bytes_little_endian(patched_rom, options_address + 0x10, 1, starting_badges)

    # Set receive item messages type
    receive_item_messages_type = get_option_value(multiworld, player, "receive_item_messages")
    _set_bytes_little_endian(patched_rom, options_address + 0x11, 1, receive_item_messages_type)

    # Set better shops
    reusable_tms = 1 if get_option_value(multiworld, player, "reusable_tms") == Toggle.option_true else 0
    _set_bytes_little_endian(patched_rom, options_address + 0x12, 1, reusable_tms)

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
    with open(get_base_rom_path(), "rb") as infile:
        base_rom_bytes = bytes(infile.read())

    return base_rom_bytes


def get_base_rom_path() -> str:
    options = Utils.get_options()
    file_name = options["pokemon_emerald_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.local_path(file_name)
    return file_name


def _set_bytes_little_endian(byte_array, address, size, value) -> None:
    offset = 0
    while size > 0:
        byte_array[address + offset] = value & 0xFF
        value = value >> 8
        offset += 1
        size -= 1


def _randomize_encounter_tables(multiworld, player, rom) -> None:
    """
    For every encounter table, replace each unique species.
    So if a table only has 2 species across multiple slots, it will
    still have 2 species in the same respective slots after randomization.
    """
    for map_data in data.maps:
        if map_data.land_encounters is not None:
            new_encounters = _create_randomized_encounter_table(multiworld, player, map_data.land_encounters.slots)
            _replace_encounters(rom, map_data.land_encounters.rom_address, new_encounters)
        if map_data.water_encounters is not None:
            new_encounters = _create_randomized_encounter_table(multiworld, player, map_data.water_encounters.slots)
            _replace_encounters(rom, map_data.water_encounters.rom_address, new_encounters)
        if map_data.fishing_encounters is not None:
            new_encounters = _create_randomized_encounter_table(multiworld, player, map_data.fishing_encounters.slots)
            _replace_encounters(rom, map_data.fishing_encounters.rom_address, new_encounters)


def _create_randomized_encounter_table(multiworld: MultiWorld, player: int, default_slots: List[int]) -> List[int]:
    random = multiworld.per_slot_randoms[player]

    should_match_bst = get_option_value(multiworld, player, "wild_pokemon") in [RandomizeWildPokemon.option_match_base_stats, RandomizeWildPokemon.option_match_base_stats_and_type]
    should_match_type = get_option_value(multiworld, player, "wild_pokemon") in [RandomizeWildPokemon.option_match_type, RandomizeWildPokemon.option_match_base_stats_and_type]
    should_allow_legendaries = get_option_value(multiworld, player, "allow_wild_legendaries") == Toggle.option_true

    default_pokemon = [p_id for p_id in set(default_slots)]

    new_pokemon_map: Dict[int, int] = {}
    for pokemon_id in default_pokemon:
        target_bst = sum(get_species_by_id(pokemon_id).base_stats) if should_match_bst else None
        target_type = random.choice(get_species_by_id(pokemon_id).types) if should_match_type else None
        new_pokemon_id = get_random_species(random, target_bst, target_type, should_allow_legendaries).species_id
        new_pokemon_map[pokemon_id] = new_pokemon_id

    new_slots: List[int] = []
    for slot in default_slots:
        new_slots.append(new_pokemon_map[slot])

    return new_slots


def _replace_encounters(rom, table_address, encounter_slots) -> None:
    """Encounter tables are lists of
    struct {
        min_level:  0x01 bytes,
        max_level:  0x01 bytes,
        species_id: 0x02 bytes
    }
    """
    for slot_i, species_id in enumerate(encounter_slots):
        address = table_address + 2 + (4 * slot_i)
        _set_bytes_little_endian(rom, address, 2, species_id)


def _randomize_opponents(multiworld: MultiWorld, player: int, rom: bytearray) -> None:
    random = multiworld.per_slot_randoms[player]
    should_match_bst = get_option_value(multiworld, player, "trainer_parties") in [RandomizeTrainerParties.option_match_base_stats, RandomizeTrainerParties.option_match_base_stats_and_type]
    should_match_type = get_option_value(multiworld, player, "trainer_parties") in [RandomizeTrainerParties.option_match_type, RandomizeTrainerParties.option_match_base_stats_and_type]
    should_allow_legendaries = get_option_value(multiworld, player, "allow_trainer_legendaries") == Toggle.option_true

    for trainer_data in data.trainers:
        party_address = trainer_data.party.rom_address

        pokemon_data_size: int
        if (
            trainer_data.party.pokemon_data_type == TrainerPokemonDataTypeEnum.NO_ITEM_DEFAULT_MOVES or
            trainer_data.party.pokemon_data_type == TrainerPokemonDataTypeEnum.ITEM_DEFAULT_MOVES
        ):
            pokemon_data_size = 8
        else: # Custom Moves
            pokemon_data_size = 16

        new_party: List[SpeciesData] = []
        for pokemon_data in trainer_data.party.pokemon:
            target_bst = sum(get_species_by_id(pokemon_data.species_id).base_stats) if should_match_bst else None
            target_type = random.choice(get_species_by_id(pokemon_data.species_id).types) if should_match_type else None
            new_party.append(get_random_species(random, target_bst, target_type, should_allow_legendaries))

        for i, species in enumerate(new_party):
            pokemon_address = party_address + (i * pokemon_data_size)

            # Replace custom moves if applicable
            # TODO: This replaces custom moves with a random move regardless of whether that move
            # is learnable by that species. Should eventually be able to pick and choose from
            # the level up learnset and learnable tms/hms instead. Especially if moves aren't randomized
            if trainer_data.party.pokemon_data_type == TrainerPokemonDataTypeEnum.NO_ITEM_CUSTOM_MOVES:
                _set_bytes_little_endian(rom, pokemon_address + 0x06, 2, get_random_move(random))
                _set_bytes_little_endian(rom, pokemon_address + 0x08, 2, get_random_move(random))
                _set_bytes_little_endian(rom, pokemon_address + 0x0A, 2, get_random_move(random))
                _set_bytes_little_endian(rom, pokemon_address + 0x0C, 2, get_random_move(random))
            elif trainer_data.party.pokemon_data_type == TrainerPokemonDataTypeEnum.ITEM_CUSTOM_MOVES:
                _set_bytes_little_endian(rom, pokemon_address + 0x08, 2, get_random_move(random))
                _set_bytes_little_endian(rom, pokemon_address + 0x0A, 2, get_random_move(random))
                _set_bytes_little_endian(rom, pokemon_address + 0x0C, 2, get_random_move(random))
                _set_bytes_little_endian(rom, pokemon_address + 0x0E, 2, get_random_move(random))

            # Replace species
            _set_bytes_little_endian(rom, pokemon_address + 0x04, 2, species.species_id)


def _randomize_opponent_battle_type(multiworld: MultiWorld, player: int, rom: bytearray) -> None:
    probability = get_option_value(multiworld, player, "double_battle_chance") / 100

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


def _randomize_starters(multiworld: MultiWorld, player: int, rom: bytearray) -> None:
    random = multiworld.per_slot_randoms[player]
    i = 0
    j = 0

    # TODO: Follow evolution pattern if possible. Needs evolution data
    # (trainer_name, starter_index_in_team, is_evolved_form)
    rival_teams = [
        [
            ("TRAINER_BRENDAN_ROUTE_103_TREECKO", 0, False),
            ("TRAINER_BRENDAN_RUSTBORO_TREECKO",  1, False),
            ("TRAINER_BRENDAN_ROUTE_110_TREECKO", 2, True ),
            ("TRAINER_BRENDAN_ROUTE_119_TREECKO", 2, True ),
            ("TRAINER_BRENDAN_LILYCOVE_TREECKO",  3, True ),
            ("TRAINER_MAY_ROUTE_103_TREECKO",     0, True ),
            ("TRAINER_MAY_RUSTBORO_TREECKO",      1, True ),
            ("TRAINER_MAY_ROUTE_110_TREECKO",     2, True ),
            ("TRAINER_MAY_ROUTE_119_TREECKO",     2, True ),
            ("TRAINER_MAY_LILYCOVE_TREECKO",      3, True )
        ],
        [
            ("TRAINER_BRENDAN_ROUTE_103_TORCHIC", 0, False),
            ("TRAINER_BRENDAN_RUSTBORO_TORCHIC",  1, False),
            ("TRAINER_BRENDAN_ROUTE_110_TORCHIC", 2, True ),
            ("TRAINER_BRENDAN_ROUTE_119_TORCHIC", 2, True ),
            ("TRAINER_BRENDAN_LILYCOVE_TORCHIC",  3, True ),
            ("TRAINER_MAY_ROUTE_103_TORCHIC",     0, True ),
            ("TRAINER_MAY_RUSTBORO_TORCHIC",      1, True ),
            ("TRAINER_MAY_ROUTE_110_TORCHIC",     2, True ),
            ("TRAINER_MAY_ROUTE_119_TORCHIC",     2, True ),
            ("TRAINER_MAY_LILYCOVE_TORCHIC",      3, True )
        ],
        [
            ("TRAINER_BRENDAN_ROUTE_103_MUDKIP", 0, False),
            ("TRAINER_BRENDAN_RUSTBORO_MUDKIP",  1, False),
            ("TRAINER_BRENDAN_ROUTE_110_MUDKIP", 2, True ),
            ("TRAINER_BRENDAN_ROUTE_119_MUDKIP", 2, True ),
            ("TRAINER_BRENDAN_LILYCOVE_MUDKIP",  3, True ),
            ("TRAINER_MAY_ROUTE_103_MUDKIP",     0, True ),
            ("TRAINER_MAY_RUSTBORO_MUDKIP",      1, True ),
            ("TRAINER_MAY_ROUTE_110_MUDKIP",     2, True ),
            ("TRAINER_MAY_ROUTE_119_MUDKIP",     2, True ),
            ("TRAINER_MAY_LILYCOVE_MUDKIP",      3, True )
        ]
    ]

    for k in multiworld.player_name[player]:
        i += ord(k)
        j += i * i

    should_match_bst = get_option_value(multiworld, player, "starters") in [RandomizeStarters.option_match_base_stats, RandomizeStarters.option_match_base_stats_and_type]
    should_match_type = get_option_value(multiworld, player, "starters") in [RandomizeStarters.option_match_type, RandomizeStarters.option_match_base_stats_and_type]
    should_allow_legendaries = get_option_value(multiworld, player, "allow_starter_legendaries") == Toggle.option_true

    starter_1_bst = sum(get_species_by_name("Treecko").base_stats) if should_match_bst else None
    starter_2_bst = sum(get_species_by_name("Torchic").base_stats) if should_match_bst else None
    starter_3_bst = sum(get_species_by_name("Mudkip").base_stats)  if should_match_bst else None

    starter_1_type = random.choice(get_species_by_name("Treecko").types) if should_match_type else None
    starter_2_type = random.choice(get_species_by_name("Torchic").types) if should_match_type else None
    starter_3_type = random.choice(get_species_by_name("Mudkip").types)  if should_match_type else None

    address = data.rom_addresses["sStarterMon"]
    starter_1 = get_random_species(random, starter_1_bst, starter_1_type, should_allow_legendaries)
    starter_2 = get_random_species(random, starter_2_bst, starter_2_type, should_allow_legendaries)
    starter_3 = get_random_species(random, starter_3_bst, starter_3_type, should_allow_legendaries)

    egg = 96 + j - (i * 0x077C)
    starter_1 = get_species_by_id(egg) if j == 0x14E03A else starter_1
    starter_2 = get_species_by_id(egg) if j == 0x14E03A else starter_2
    starter_3 = get_species_by_id(egg) if j == 0x14E03A else starter_3

    _set_bytes_little_endian(rom, address + 0, 2, starter_1.species_id)
    _set_bytes_little_endian(rom, address + 2, 2, starter_2.species_id)
    _set_bytes_little_endian(rom, address + 4, 2, starter_3.species_id)

    # Override starter onto rival's teams
    for i, starter in enumerate([starter_2, starter_3, starter_1]):
        for trainer_name, starter_position, is_evolved in rival_teams[i]:
            trainer_data = data.trainers[data.constants[trainer_name]]
            pokemon_address = trainer_data.party.rom_address + (starter_position * 8) # All rivals have default moves
            _set_bytes_little_endian(rom, pokemon_address + 0x04, 2, starter.species_id)


def _randomize_abilities(multiworld: MultiWorld, player: int, rom: bytearray) -> None:
    random = multiworld.per_slot_randoms[player]
    ability_label_to_value = {ability.label.lower(): ability.ability_id for ability in data.abilities}

    ability_blacklist_labels = set(["cacophony"])
    option_ability_blacklist = get_option_value(multiworld, player, "ability_blacklist")
    if option_ability_blacklist is not None:
        ability_blacklist_labels |= set([ability_label.lower() for ability_label in option_ability_blacklist])

    ability_blacklist = set([ability_label_to_value[label] for label in ability_blacklist_labels])
    ability_whitelist = [ability.ability_id for ability in data.abilities if ability.ability_id not in ability_blacklist]

    for species in data.species:
        old_abilities = species.abilities
        new_abilities = [random.choice(ability_whitelist), random.choice(ability_whitelist)]

        if old_abilities[0] != 0:
            _set_bytes_little_endian(rom, species.rom_address + 22, 1, new_abilities[0])
        if old_abilities[1] != 0:
            _set_bytes_little_endian(rom, species.rom_address + 23, 1, new_abilities[1])


def _randomize_learnsets(multiworld: MultiWorld, player: int, rom: bytearray) -> None:
    random = multiworld.per_slot_randoms[player]

    for species in data.species:
        old_learnset = species.learnset
        new_learnset: List[int] = []

        i = 0

        # Replace filler MOVE_NONEs at start of list
        while old_learnset[i].move_id == 0:
            if get_option_value(multiworld, player, "level_up_moves") == LevelUpMoves.option_start_with_four_moves:
                new_learnset.append(get_random_move(random, set(new_learnset)))
            else:
                new_learnset.append(0)
            i += 1

        while i < len(old_learnset):
            # Guarantees the starter has a move to damage wild pokemon
            if i == 3:
                new_move = get_random_damaging_move(random, set(new_learnset))
            else:
                new_move = get_random_move(random, set(new_learnset))

            new_learnset.append(new_move)

            i += 1

        new_learnset = [old_learnset[i].level << 9 | move_id for i, move_id in enumerate(new_learnset)]
        _replace_learnset(species.learnset_rom_address, new_learnset, rom)


def _randomize_tm_moves(multiworld: MultiWorld, player: int, rom: bytearray) -> None:
    random = multiworld.per_slot_randoms[player]
    tm_list_address = data.rom_addresses["sTMHMMoves"]

    for i in range(50):
        new_move = get_random_move(random)
        _set_bytes_little_endian(rom, tm_list_address + (i * 2), 2, new_move)



def _replace_learnset(learnset_address: int, new_learnset: List[int], rom: bytearray) -> None:
    for i, level_move in enumerate(new_learnset):
        _set_bytes_little_endian(rom, learnset_address + (i * 2), 2, level_move)


def _modify_species_info(multiworld: MultiWorld, player: int, rom: bytearray) -> None:
    min_catch_rate = min(get_option_value(multiworld, player, "min_catch_rate"), 255)

    for species in data.species:
        if species.catch_rate < min_catch_rate:
            _set_bytes_little_endian(rom, species.rom_address + 8, 1, min_catch_rate)


def _modify_tmhm_compatibility(multiworld: MultiWorld, player: int, rom: bytearray) -> None:
    random = multiworld.per_slot_randoms[player]

    learnsets_address = data.rom_addresses["gTMHMLearnsets"]
    size_of_learnset = 8

    tm_compatibility = get_option_value(multiworld, player, "tm_compatibility")
    hm_compatibility = get_option_value(multiworld, player, "hm_compatibility")

    for species in data.species:
        compatibility_array = [False if bit == "0" else True for bit in list(species.tm_hm_compatibility)]

        tm_compatibility_array = compatibility_array[0:50]
        if tm_compatibility == TmCompatibility.option_fully_compatible:
            tm_compatibility_array = [True for i in tm_compatibility_array]
        elif tm_compatibility == TmCompatibility.option_completely_random:
            tm_compatibility_array = [random.choice([True, False]) for i in tm_compatibility_array]

        hm_compatibility_array = compatibility_array[50:58]
        if hm_compatibility == HmCompatibility.option_fully_compatible:
            hm_compatibility_array = [True for i in hm_compatibility_array]
        elif hm_compatibility == HmCompatibility.option_completely_random:
            hm_compatibility_array = [random.choice([True, False]) for i in hm_compatibility_array]

        compatibility_array = [] + tm_compatibility_array + hm_compatibility_array + [False, False, False, False, False, False]
        compatibility_bytes = _tmhm_compatibility_array_to_bytearray(compatibility_array)

        for i, byte in enumerate(compatibility_bytes):
            address = learnsets_address + (species.species_id * size_of_learnset) + i
            _set_bytes_little_endian(rom, address, 1, byte)


# TODO: Read compatibility from ROM during extraction
def _tmhm_compatibility_array_to_bytearray(compatibility: List[bool]) -> bytearray:
    bits = [1 if bit else 0 for bit in compatibility]
    bits.reverse()

    bytes = []
    while len(bits) > 0:
        byte = 0
        for i in range(8):
            byte += bits.pop() << i

        bytes.append(byte)

    return bytearray(bytes)
