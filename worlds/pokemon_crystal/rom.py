from typing import TYPE_CHECKING
import os
import pkgutil
import bsdiff4
import random

from worlds.Files import APDeltaPatch
from settings import get_settings

from .items import reverse_offset_item_value
from .data import data

if TYPE_CHECKING:
    from . import PokemonCrystalWorld
else:
    PokemonCrystalWorld = object


class PokemonCrystalDeltaPatch(APDeltaPatch):
    game = "Pokemon Crystal"
    hash = "9f2922b235a5eeb78d65594e82ef5dde"
    patch_file_ending = ".apcrystal"
    result_file_ending = ".gbc"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()


def generate_output(world: PokemonCrystalWorld, output_directory: str) -> None:
    base_rom = get_base_rom_as_bytes()
    base_patch = pkgutil.get_data(__name__, "data/basepatch.bsdiff4")
    patched_rom = bytearray(bsdiff4.patch(base_rom, base_patch))

    # Set item values
    for location in world.multiworld.get_locations(world.player):
        # Set free fly location
        if location.address is None:
            continue

        if location.item and location.item.player == world.player:
            write_bytes(
                patched_rom,
                [reverse_offset_item_value(location.item.code)],
                location.rom_address
            )
        else:
            write_bytes(
                patched_rom,
                [184],
                location.rom_address
            )
    starters = [get_random_poke(), get_random_poke(), get_random_poke()]

    for address_name, address in data.rom_addresses.items():
        if world.options.randomize_wilds:
            if (address_name.startswith("AP_WildGrass")):
                cur_address = address + 4
                for i in range(21):
                    write_bytes(patched_rom, [get_random_poke()], cur_address)
                    cur_address += 2
            if (address_name.startswith("AP_WildWater")):
                cur_address = address + 2
                for i in range(3):
                    write_bytes(patched_rom, [get_random_poke()], cur_address)
                    cur_address += 2
        if world.options.randomize_starters:
            if (address_name.startswith("AP_Starter_CYNDAQUIL")):
                cur_address = address + 1
                write_bytes(patched_rom, [starters[0]], cur_address)
            if (address_name.startswith("AP_Starter_TOTODILE")):
                cur_address = address + 1
                write_bytes(patched_rom, [starters[1]], cur_address)
            if (address_name.startswith("AP_Starter_CHIKORITA")):
                cur_address = address + 1
                write_bytes(patched_rom, [starters[2]], cur_address)
        if world.options.full_tmhm_compatibility:
            if (address_name == "BaseData"):
                cur_address = address
                for i in range(251):
                    cur_address += 24
                    write_bytes(
                        patched_rom, [255, 255, 255, 255, 255, 255, 255, 15], cur_address)
                    cur_address += 8

    out_file_name = world.multiworld.get_out_file_name_base(world.player)
    output_path = os.path.join(output_directory, f"{out_file_name}.gbc")
    with open(output_path, "wb") as out_file:
        out_file.write(patched_rom)
    patch = PokemonCrystalDeltaPatch(os.path.splitext(output_path)[0] + ".apcrystal", player=world.player,
                                     player_name=world.multiworld.player_name[world.player], patched_path=output_path)

    patch.write()
    os.unlink(output_path)


def get_base_rom_as_bytes() -> bytes:
    with open(get_settings().pokemon_crystal_settings.rom_file, "rb") as infile:
        base_rom_bytes = bytes(infile.read())

    return base_rom_bytes


def write_bytes(data, byte_array, address):
    for byte in byte_array:
        data[address] = byte
        address += 1


def get_random_poke():
    return random.randint(1, 251)
