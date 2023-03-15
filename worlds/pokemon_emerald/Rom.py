import bsdiff4
import os
from typing import Dict, List
from BaseClasses import MultiWorld
from Options import Toggle
from Patch import APDeltaPatch
import Utils
from .Data import get_extracted_data
from .Items import reverse_offset_item_value
from .Options import get_option_value, RandomizeWildPokemon, RandomizeStarters, RandomizeTrainerParties, TmCompatibility, HmCompatibility, LevelUpMoves
from .Pokemon import get_random_species, get_species_by_id, get_species_by_name, get_random_damaging_move, get_random_move, species_data


class PokemonEmeraldDeltaPatch(APDeltaPatch):
    game = "Pokemon Emerald"
    hash = "605b89b67018abcea91e693a4dd25be3"
    patch_file_ending = ".apemerald"
    result_file_ending = ".gba"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()


def generate_output(multiworld: MultiWorld, player: int, output_directory: str):
    extracted_data = get_extracted_data()

    base_rom = get_base_rom_as_bytes()
    with open(os.path.join(os.path.dirname(__file__), f"data/base_patch.bsdiff4"), "rb") as stream:
        base_patch = bytes(stream.read())
        patched_rom = bytearray(bsdiff4.patch(base_rom, base_patch))

    # Set item values
    for location in multiworld.get_locations():
        if location.player != player:
            continue
        if location.is_event:
            continue

        if location.item and location.item.player == player:
            _set_bytes_little_endian(patched_rom, location.rom_address, 2, reverse_offset_item_value(location.item.code))
        else:
            _set_bytes_little_endian(patched_rom, location.rom_address, 2, extracted_data["constants"]["ITEM_ARCHIPELAGO_PROGRESSION"])

    # Randomize encounter tables
    if (get_option_value(multiworld, player, "wild_pokemon") != RandomizeWildPokemon.option_vanilla):
        _randomize_encounter_tables(multiworld, player, patched_rom)

    # Randomize abilities
    if (get_option_value(multiworld, player, "abilities") == Toggle.option_true):
        _randomize_abilities(multiworld, player, patched_rom)

    # Randomize learnsets
    if (get_option_value(multiworld, player, "level_up_moves") != LevelUpMoves.option_vanilla):
        _randomize_learnsets(multiworld, player, patched_rom)

    # Randomize opponents
    if (get_option_value(multiworld, player, "trainer_parties") != RandomizeTrainerParties.option_vanilla):
        _randomize_opponents(multiworld, player, patched_rom)

    # Randomize starters
    if (get_option_value(multiworld, player, "starters") != RandomizeStarters.option_vanilla):
        _randomize_starters(multiworld, player, patched_rom)

    # Modify species
    _modify_species_info(multiworld, player, patched_rom)

    # Modify TM/HM compatibility
    _modify_tmhm_compatibility(multiworld, player, patched_rom)

    # Options
    # struct ArchipelagoOptions
    # {
    #     bool8 advanceTextWithHoldA;
    #     bool8 isFerryEnabled;
    #     bool8 areTrainersBlind;
    #     u16 expMultiplierNumerator;
    #     u16 expMultiplierDenominator;
    #     u16 birchPokemon;
    # } __attribute__((packed));
    options_address = extracted_data["misc_rom_addresses"]["gArchipelagoOptions"]

    # Set hold A to advance text
    turbo_a = 1 if get_option_value(multiworld, player, "turbo_a") == Toggle.option_true else 0
    _set_bytes_little_endian(patched_rom, options_address + 0, 1, turbo_a)

    # Set ferry enabled
    enable_ferry = 1 if get_option_value(multiworld, player, "enable_ferry") == Toggle.option_true else 0
    _set_bytes_little_endian(patched_rom, options_address + 1, 1, enable_ferry)

    # Set blind trainers
    blind_trainers = 1 if get_option_value(multiworld, player, "blind_trainers") == Toggle.option_true else 0
    _set_bytes_little_endian(patched_rom, options_address + 2, 1, blind_trainers)

    # Set exp modifier
    numerator = min(get_option_value(multiworld, player, "exp_modifier"), 2**16 - 1)
    _set_bytes_little_endian(patched_rom, options_address + 3, 2, numerator)
    _set_bytes_little_endian(patched_rom, options_address + 5, 2, 100)

    # Set Birch pokemon
    _set_bytes_little_endian(patched_rom, options_address + 7, 2, get_random_species(multiworld.per_slot_randoms[player]).id)

    # Write Output
    outfile_player_name = f"_P{player}"
    outfile_player_name += f"_{multiworld.get_file_safe_player_name(player).replace(' ', '_')}" \
        if multiworld.player_name[player] != "Player%d" % player else ""

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


def _set_bytes_little_endian(byte_array, address, size, value):
    offset = 0
    while (size > 0):
        byte_array[address + offset] = value & 0xFF
        value = value >> 8
        offset += 1
        size -= 1


# For every encounter table, replace each unique species.
# So if a table only has 2 species across multiple slots, it will
# still have 2 species in the same respective slots after randomization.
# TODO: Account for access to pokemon who can learn required HMs
def _randomize_encounter_tables(multiworld, player, rom):
    extracted_data = get_extracted_data()

    # Sort alphabetically by map key for reproducibility
    maps_json = [m[1] for m in sorted(extracted_data["maps"].items(), key=lambda m: m[0])]

    for map_data in maps_json:
        land_encounters = map_data["land_encounters"]
        water_encounters = map_data["water_encounters"]
        fishing_encounters = map_data["fishing_encounters"]
        if (not land_encounters == None):
            new_encounters = _create_randomized_encounter_table(multiworld, player, land_encounters["encounter_slots"])
            _replace_encounters(rom, land_encounters["rom_address"], new_encounters)
        if (not water_encounters == None):
            new_encounters = _create_randomized_encounter_table(multiworld, player, water_encounters["encounter_slots"])
            _replace_encounters(rom, water_encounters["rom_address"], new_encounters)
        if (not fishing_encounters == None):
            new_encounters = _create_randomized_encounter_table(multiworld, player, fishing_encounters["encounter_slots"])
            _replace_encounters(rom, fishing_encounters["rom_address"], new_encounters)


def _create_randomized_encounter_table(multiworld: MultiWorld, player: int, default_slots):
    random = multiworld.per_slot_randoms[player]
    match_bst = get_option_value(multiworld, player, "wild_pokemon") in [RandomizeWildPokemon.option_match_base_stats, RandomizeWildPokemon.option_match_base_stats_and_type]
    match_type = get_option_value(multiworld, player, "wild_pokemon") in [RandomizeWildPokemon.option_match_type, RandomizeWildPokemon.option_match_base_stats_and_type]

    default_pokemon = [p_id for p_id in set(default_slots)]

    new_pokemon_map: Dict[int, int] = {}
    for pokemon_id in default_pokemon:
        bst = None if not match_bst else sum(get_species_by_id(pokemon_id).base_stats)
        type = None if not match_type else random.choice(get_species_by_id(pokemon_id).types)
        new_pokemon_id = get_random_species(random, bst, type).id
        new_pokemon_map[pokemon_id] = new_pokemon_id

    new_slots = []
    for slot in default_slots:
        new_slots.append(new_pokemon_map[slot])

    return new_slots


def _replace_encounters(rom, table_address, encounter_slots):
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


def _randomize_opponents(multiworld: MultiWorld, player: int, rom: bytearray):
    random = multiworld.per_slot_randoms[player]
    trainers_json = get_extracted_data()["trainers"]
    match_bst = get_option_value(multiworld, player, "trainer_parties") in [RandomizeTrainerParties.option_match_base_stats, RandomizeTrainerParties.option_match_base_stats_and_type]
    match_type = get_option_value(multiworld, player, "trainer_parties") in [RandomizeTrainerParties.option_match_type, RandomizeTrainerParties.option_match_base_stats_and_type]

    for i, trainer_data in enumerate(trainers_json):
        party_address = trainer_data["party_rom_address"]

        pokemon_data_size: int
        if (
            trainer_data["pokemon_data_type"] == "NO_ITEM_DEFAULT_MOVES" or
            trainer_data["pokemon_data_type"] == "ITEM_DEFAULT_MOVES"
        ):
            pokemon_data_size = 8
        else: # Custom Moves
            pokemon_data_size = 16

        new_party = []
        for pokemon_data in trainer_data["party"]:
            bst = sum(get_species_by_id(pokemon_data["species"]).base_stats) if match_bst else None
            type = random.choice(get_species_by_id(pokemon_data["species"]).types) if match_type else None
            new_party.append(get_random_species(random, bst, type))

        for j, species in enumerate(new_party):
            pokemon_address = party_address + (j * pokemon_data_size)

            # Replace custom moves if applicable
            # TODO: This replaces custom moves with a random move regardless of whether that move
            # is learnable by that species. Should eventually be able to pick and choose from
            # the level up learnset and learnable tms/hms instead. Especially if moves aren't randomized
            if (trainer_data["pokemon_data_type"] == "NO_ITEM_CUSTOM_MOVES"):
                _set_bytes_little_endian(rom, pokemon_address + 0x06, 2, get_random_move(random))
                _set_bytes_little_endian(rom, pokemon_address + 0x08, 2, get_random_move(random))
                _set_bytes_little_endian(rom, pokemon_address + 0x0A, 2, get_random_move(random))
                _set_bytes_little_endian(rom, pokemon_address + 0x0C, 2, get_random_move(random))
            elif (trainer_data["pokemon_data_type"] == "ITEM_CUSTOM_MOVES"):
                _set_bytes_little_endian(rom, pokemon_address + 0x08, 2, get_random_move(random))
                _set_bytes_little_endian(rom, pokemon_address + 0x0A, 2, get_random_move(random))
                _set_bytes_little_endian(rom, pokemon_address + 0x0C, 2, get_random_move(random))
                _set_bytes_little_endian(rom, pokemon_address + 0x0E, 2, get_random_move(random))

            # Replace species
            _set_bytes_little_endian(rom, pokemon_address + 0x04, 2, species.id)


def _randomize_starters(multiworld, player, rom):
    random = multiworld.per_slot_randoms[player]

    match_bst = get_option_value(multiworld, player, "starters") in [RandomizeStarters.option_match_base_stats, RandomizeStarters.option_match_base_stats_and_type]
    match_type = get_option_value(multiworld, player, "starters") in [RandomizeStarters.option_match_type, RandomizeStarters.option_match_base_stats_and_type]

    starter_1_bst = None if not match_bst else sum(get_species_by_name("Treecko").base_stats)
    starter_2_bst = None if not match_bst else sum(get_species_by_name("Torchic").base_stats)
    starter_3_bst = None if not match_bst else sum(get_species_by_name("Mudkip").base_stats)

    starter_1_type = None if not match_type else random.choice(get_species_by_name("Treecko").types)
    starter_2_type = None if not match_type else random.choice(get_species_by_name("Torchic").types)
    starter_3_type = None if not match_type else random.choice(get_species_by_name("Mudkip").types)

    address = get_extracted_data()["misc_rom_addresses"]["sStarterMon"]
    starter_1 = get_random_species(random, starter_1_bst, starter_1_type)
    starter_2 = get_random_species(random, starter_2_bst, starter_2_type)
    starter_3 = get_random_species(random, starter_3_bst, starter_3_type)

    _set_bytes_little_endian(rom, address + 0, 2, starter_1.id)
    _set_bytes_little_endian(rom, address + 2, 2, starter_2.id)
    _set_bytes_little_endian(rom, address + 4, 2, starter_3.id)


def _randomize_abilities(multiworld: MultiWorld, player: int, rom: bytearray):
    random = multiworld.per_slot_randoms[player]

    num_abilities = get_extracted_data()["constants"]["ABILITIES_COUNT"]

    for species_data in get_extracted_data()["species"]:
        old_abilities = species_data["abilities"]
        new_abilities = [random.randrange(0, num_abilities), random.randrange(0, num_abilities)]

        if (old_abilities[0] != 0):
            _set_bytes_little_endian(rom, species_data["rom_address"] + 22, 1, new_abilities[0])
        if (old_abilities[1] != 0):
            _set_bytes_little_endian(rom, species_data["rom_address"] + 23, 1, new_abilities[1])


def _randomize_learnsets(multiworld: MultiWorld, player: int, rom: bytearray):
    random = multiworld.per_slot_randoms[player]

    for species_data in get_extracted_data()["species"]:
        old_learnset = species_data["learnset"]["moves"]
        new_learnset: List[int] = []

        i = 0

        # Replace filler MOVE_NONEs at start of list
        while (old_learnset[i]["move_id"] == 0):
            if (get_option_value(multiworld, player, "level_up_moves") == LevelUpMoves.option_start_with_four_moves):
                new_learnset.append(get_random_move(random, set(new_learnset)))
            else:
                new_learnset.append(0)
            i += 1

        while (i < len(old_learnset)):
            # Guarantees the starter can defeat the Zigzagoon and gain XP
            if (i == 3):
                new_move = get_random_damaging_move(random, set(new_learnset))
            else:
                new_move = get_random_move(random, set(new_learnset))

            new_learnset.append(new_move)

            i += 1

        new_learnset = [old_learnset[i]["level"] << 9 | move_id for i, move_id in enumerate(new_learnset)]
        _replace_learnset(species_data["learnset"]["rom_address"], new_learnset, rom)


def _replace_learnset(learnset_address: int, new_learnset: List[int], rom: bytearray):
    for i, level_move in enumerate(new_learnset):
        _set_bytes_little_endian(rom, learnset_address + (i * 2), 2, level_move)


def _modify_species_info(multiworld: MultiWorld, player: int, rom: bytearray):
    min_catch_rate = min(get_option_value(multiworld, player, "min_catch_rate"), 255)

    for species in species_data:
        species_info_address = get_extracted_data()["species"][species.id]["rom_address"]
        if (species.catch_rate < min_catch_rate):
            _set_bytes_little_endian(rom, species_info_address + 8, 1, min_catch_rate)


def _modify_tmhm_compatibility(multiworld: MultiWorld, player: int, rom: bytearray):
    random = multiworld.per_slot_randoms[player]

    learnsets_address = get_extracted_data()["misc_rom_addresses"]["gTMHMLearnsets"]
    size_of_learnset = 8

    tm_compatibility = get_option_value(multiworld, player, "tm_compatibility")
    hm_compatibility = get_option_value(multiworld, player, "hm_compatibility")

    for species in species_data:
        compatibility_array = [False if bit == "0" else True for bit in list(species.tm_hm_compatibility)]

        tm_compatibility_array = compatibility_array[0:50]
        if (tm_compatibility == TmCompatibility.option_fully_compatible):
            tm_compatibility_array = [True for i in tm_compatibility_array]
        elif (tm_compatibility == TmCompatibility.option_completely_random):
            tm_compatibility_array = [random.choice([True, False]) for i in tm_compatibility_array]

        hm_compatibility_array = compatibility_array[50:58]
        if (hm_compatibility == HmCompatibility.option_fully_compatible):
            hm_compatibility_array = [True for i in hm_compatibility_array]
        elif (hm_compatibility == HmCompatibility.option_completely_random):
            hm_compatibility_array = [random.choice([True, False]) for i in hm_compatibility_array]

        compatibility_array = [] + tm_compatibility_array + hm_compatibility_array + [False, False, False, False, False, False]
        compatibility_bytes = _tmhm_compatibility_array_to_bytearray(compatibility_array)

        for i, byte in enumerate(compatibility_bytes):
            address = learnsets_address + (species.id * size_of_learnset) + i
            _set_bytes_little_endian(rom, address, 1, byte)


def _tmhm_compatibility_array_to_bytearray(compatibility: List[bool]) -> bytearray:
    bits = [1 if bit else 0 for bit in compatibility]
    bits.reverse()

    bytes = []
    while (len(bits) > 0):
        byte = 0
        for i in range(8):
            byte += bits.pop() << i
        
        bytes.append(byte)

    return bytearray(bytes)
