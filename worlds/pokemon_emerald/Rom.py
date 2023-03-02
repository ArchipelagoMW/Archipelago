import hashlib
import bsdiff4
import os
from typing import Dict
from Patch import APDeltaPatch
import Utils
from .Data import get_extracted_data
from .Options import get_option_value
from .Pokemon import get_random_species


class PokemonEmeraldDeltaPatch(APDeltaPatch):
    game = "Pokemon Emerald"
    hash = "a9dec84dfe7f62ab2220bafaef7479da0929d066ece16a6885f6226db19085af"
    patch_file_ending = ".apemerald"
    result_file_ending = ".gba"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()


def generate_output(multiworld, player, output_directory: str):
    extracted_data = get_extracted_data()

    base_rom = get_base_rom_as_bytes()
    with open(os.path.join(os.path.dirname(__file__), f"base_patch.bsdiff4"), "rb") as stream:
        base_patch = bytes(stream.read())
        patched_rom = bytearray(bsdiff4.patch(base_rom, base_patch))

    # Set item values
    for location in multiworld.get_locations():
        if location.player != player:
            continue
        if location.is_event:
            continue

        if location.item and location.item.player == player:
            _set_bytes_little_endian(patched_rom, location.address, 2, location.item.code)
        else:
            _set_bytes_little_endian(patched_rom, location.address, 2, extracted_data["constants"]["ITEM_ARCHIPELAGO_PROGRESSION"])

    # Set encounter tables
    _randomize_encounter_tables(multiworld.per_slot_randoms[player], patched_rom)

    # Set exp multiplier
    numerator = min(get_option_value(multiworld, player, "exp_multiplier"), 2**16 - 1)
    _set_bytes_little_endian(patched_rom, extracted_data["misc_rom_addresses"]["sExpMultiplier"], 2, numerator)
    _set_bytes_little_endian(patched_rom, extracted_data["misc_rom_addresses"]["sExpMultiplier"] + 2, 2, 100)

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

        local_hash = hashlib.sha256()
        local_hash.update(base_rom_bytes)

        if (not local_hash.hexdigest() == PokemonEmeraldDeltaPatch.hash):
            raise AssertionError("Base ROM does not match expected hash. Please get Pokemon Emerald Version (USA, Europe) and dump it.")

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
def _randomize_encounter_tables(random, patched_rom):
    extracted_data = get_extracted_data()

    for map_data in extracted_data["maps"].values():
        land_encounters = map_data["land_encounters"]
        water_encounters = map_data["water_encounters"]
        fishing_encounters = map_data["fishing_encounters"]
        if (not land_encounters == None):
            new_encounters = _create_randomized_encounter_table(random, land_encounters["encounter_slots"])
            _replace_encounters(patched_rom, land_encounters["rom_address"], new_encounters)
        if (not water_encounters == None):
            new_encounters = _create_randomized_encounter_table(random, water_encounters["encounter_slots"])
            _replace_encounters(patched_rom, water_encounters["rom_address"], new_encounters)
        if (not fishing_encounters == None):
            new_encounters = _create_randomized_encounter_table(random, fishing_encounters["encounter_slots"])
            _replace_encounters(patched_rom, fishing_encounters["rom_address"], new_encounters)


def _create_randomized_encounter_table(random, default_slots):
    default_pokemon = [p_id for p_id in set(default_slots)]
    new_pokemon = []

    new_pokemon_map: Dict[int, int] = {}
    for pokemon_id in default_pokemon:
        new_pokemon_id = get_random_species(random).id
        new_pokemon_map[pokemon_id] = new_pokemon_id

    new_slots = []
    for slot in default_slots:
        new_slots.append(new_pokemon_map[slot])

    return new_slots


def _replace_encounters(data, table_address, encounter_slots):
    """Encounter tables are lists of
    struct {
        min_level:  0x01 bytes,
        max_level:  0x01 bytes,
        species_id: 0x02 bytes
    }
    """
    for slot_i, species_id in enumerate(encounter_slots):
        address = table_address + 2 + (4 * slot_i)
        _set_bytes_little_endian(data, address, 2, species_id)
