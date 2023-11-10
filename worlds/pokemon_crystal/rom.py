from typing import TYPE_CHECKING
import os
import pkgutil
import bsdiff4

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
    random = world.multiworld.per_slot_randoms[world.player]
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
    starters = [get_random_poke(random), get_random_poke(
        random), get_random_poke(random)]

    # static = {
    # 	"RedGyarados": get_random_poke(random),
    # 	"Sudowoodo": get_random_poke(random),
    # 	"Suicune": get_random_poke(random),
    # 	"Ho_Oh": get_random_poke(random),
    # 	"UnionCaveLapras": get_random_poke(random),
    # 	"Snorlax": get_random_poke(random),
    # 	"Lugia": get_random_poke(random),
    # 	"CatchTutorial_1": get_random_poke(random),
    # 	"CatchTutorial_2": get_random_poke(random),
    # 	"CatchTutorial_3": get_random_poke(random),
    # 	"RocketHQTrap_1": get_random_poke(random),
    # 	"RocketHQTrap_2": get_random_poke(random),
    # 	"RocketHQTrap_3": get_random_poke(random),
    # 	"RocketHQElectrode_1": get_random_poke(random),
    # 	"RocketHQElectrode_2": get_random_poke(random),
    # 	"RocketHQElectrode_3": get_random_poke(random)
    # }

    for address_name, address in data.rom_addresses.items():
        if world.options.randomize_wilds:
            if (address_name.startswith("AP_WildGrass")):
                cur_address = address + 4
                for i in range(21):
                    write_bytes(
                        patched_rom, [get_random_poke(random)], cur_address)
                    cur_address += 2
            if (address_name.startswith("AP_WildWater")):
                cur_address = address + 2
                for i in range(3):
                    write_bytes(
                        patched_rom, [get_random_poke(random)], cur_address)
                    cur_address += 2
            if address_name == "AP_Misc_Intro_Wooper":
                write_bytes(
                    patched_rom, [get_random_poke(random)], address + 1)
        if world.options.randomize_starters:
            if (address_name.startswith("AP_Starter_CYNDAQUIL")):
                cur_address = address + 1
                write_bytes(patched_rom, [starters[0]], cur_address)
                if address_name.endswith("4"):
                    write_bytes(
                        patched_rom, [get_random_helditem(random)], cur_address + 2)
            if (address_name.startswith("AP_Starter_TOTODILE")):
                cur_address = address + 1
                write_bytes(patched_rom, [starters[1]], cur_address)
                if address_name.endswith("4"):
                    write_bytes(
                        patched_rom, [get_random_helditem(random)], cur_address + 2)
            if (address_name.startswith("AP_Starter_CHIKORITA")):
                cur_address = address + 1
                write_bytes(patched_rom, [starters[2]], cur_address)
                if address_name.endswith("4"):
                    write_bytes(
                        patched_rom, [get_random_helditem(random)], cur_address + 2)
        if world.options.full_tmhm_compatibility:
            if (address_name == "BaseData"):
                cur_address = address
                for i in range(251):
                    cur_address += 24
                    write_bytes(
                        patched_rom, [255, 255, 255, 255, 255, 255, 255, 15], cur_address)
                    cur_address += 8
        if world.options.blind_trainers:
            if address_name == "AP_Setting_Blind_Trainers":
                write_bytes(patched_rom, [0xC9], address)  # 0xC9 = ret
        if world.options.randomize_learnsets:
            if address_name.endswith("EvosAttacks"):
                pkmn_name = address_name[0:-11].upper()
                learnset_data = data.evo_attacks[pkmn_name]
                cur_address = address + (3 * len(learnset_data.evolutions)) + 1
                move_levels = []
                if world.options.randomize_learnsets > 1:
                    for move in learnset_data.moves:
                        if move[1] == "NO_MOVE":
                            move_levels.append(1)
                for move in learnset_data.moves:
                    if move[1] != "NO_MOVE":
                        move_levels.append(move[0])
                for level in move_levels:
                    write_bytes(
                        patched_rom, [level, get_random_move(random)], cur_address)
                    cur_address += 2
        if world.options.better_marts:
            if address_name == "Marts":
                better_mart_address = data.rom_addresses["MartBetterMart"] - 0x10000
                better_mart_bytes = better_mart_address.to_bytes(2, "little")
                cur_address = address
                for i in range(33):  # marts before goldenrod
                    # skip goldenrod and celadon
                    if i not in [6, 7, 8, 9, 10, 11, 12, 23, 24, 25, 26, 27]:
                        write_bytes(
                            patched_rom, better_mart_bytes, cur_address)
                    cur_address += 2

        # Set slot name
    for i, byte in enumerate(world.multiworld.player_name[world.player].encode("utf-8")):
        write_bytes(patched_rom, [byte],
                    data.rom_addresses["AP_Seed_Name"] + i)

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


def get_random_poke(random):
    return random.randint(1, 251)


def get_random_move(random):
    return random.randint(1, 251)


def get_random_helditem(random):
    helditems = [item_id for item_id, item in data.items.items()
                 if "Unique" not in item.tags and "INVALID" not in item.tags]
    return random.choice(helditems)
