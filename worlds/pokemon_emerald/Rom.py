import bsdiff4
import os
from Patch import APDeltaPatch
from .data.Pokemon import get_random_species
from .Util import get_data_json, set_bytes_little_endian

def get_base_rom_as_bytes() -> bytes:
    with open(os.path.join(os.path.dirname(__file__), f"pokeemerald-vanilla.gba"), "rb") as infile:
        base_rom_bytes = bytes(infile.read())
    return base_rom_bytes

# For every encounter table, replace each unique species.
# So if a table only has 2 species across multiple slots, it will
# still have 2 species in the same respective slots after randomization.
# TODO: Account for access to pokemon who can learn required HMs
def randomize_encounter_tables(self, patched_rom):
    data = get_data_json()

    for map_name, tables in data["encounter_tables"].items():
        for table in tables.values():
            default_pokemon = [p for p in set(table["encounter_slots"])]
            new_pokemon = []

            for pokemon in default_pokemon:
                new_pokemon_id = get_random_species(self.multiworld.per_slot_randoms[self.player]).id
                new_pokemon.append(new_pokemon_id)
            
            for slot_i, slot in enumerate(table["encounter_slots"]):
                """Encounter tables are lists of
                struct {
                    min_level:  0x01 bytes,
                    max_level:  0x01 bytes,
                    species_id: 0x02 bytes
                }
                """
                address = table["rom_address"] + 2 + (slot_i * 4)
                set_bytes_little_endian(patched_rom, address, 2, new_pokemon[default_pokemon.index(slot)])

def generate_output(self, output_directory: str):
    data = get_data_json() 

    base_rom = get_base_rom_as_bytes()
    with open(os.path.join(os.path.dirname(__file__), f"base_patch.bsdiff4"), "rb") as stream:
        base_patch = bytes(stream.read())
        patched_rom = bytearray(bsdiff4.patch(base_rom, base_patch))

    for location in self.multiworld.get_locations():
        if location.player != self.player:
            continue

        if location.item and location.item.player == self.player:
            set_bytes_little_endian(patched_rom, location.address, 2, location.item.code)
        else:
            set_bytes_little_endian(patched_rom, location.address, 2, data["constants"]["items"]["ITEM_ARCHIPELAGO_PROGRESSION"])

    randomize_encounter_tables(self, patched_rom)

    outfile_player_name = f"_P{self.player}"
    outfile_player_name += f"_{self.multiworld.get_file_safe_player_name(self.player).replace(' ', '_')}" \
        if self.multiworld.player_name[self.player] != "Player%d" % self.player else ""

    output_path = os.path.join(output_directory, f"AP_{self.multiworld.seed_name}{outfile_player_name}.gba")
    with open(output_path, "wb") as outfile:
        outfile.write(patched_rom)
    patch = PokemonEmeraldDeltaPatch(os.path.splitext(output_path)[0] + ".apemerald", player=self.player,
                            player_name=self.multiworld.player_name[self.player], patched_path=output_path)

    patch.write()
    os.unlink(output_path)


class PokemonEmeraldDeltaPatch(APDeltaPatch):
    hash = "605b89b67018abcea91e693a4dd25be3"
    game = "Pokemon Emerald"
    patch_file_ending = ".apemerald"
    result_file_ending = ".gba"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()
