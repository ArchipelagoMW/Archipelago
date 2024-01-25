from typing import TYPE_CHECKING
import os
import pkgutil
import bsdiff4

from worlds.Files import APDeltaPatch
from settings import get_settings

from .items import reverse_offset_item_value, item_const_name_to_id
from .data import data
from .utils import get_random_pokemon_id

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

    for location in world.multiworld.get_locations(world.player):
        if location.address is None:
            continue

        if location.item and location.item.player == world.player:
            write_bytes(patched_rom, [reverse_offset_item_value(location.item.code)], location.rom_address)
        else:
            write_bytes(patched_rom, [184], location.rom_address)

    static = {
        "RedGyarados": 2,
        "Sudowoodo": 0,
        "Suicune": 2,
        "Ho_Oh": 2,
        "UnionCaveLapras": 2,
        "Snorlax": 2,
        "Lugia": 2,
        "CatchTutorial_1": 0,
        "CatchTutorial_2": 0,
        "CatchTutorial_3": 0,
        "RocketHQTrap_1": 0,
        "RocketHQTrap_2": 0,
        "RocketHQTrap_3": 0,
        "RocketHQElectrode_1": 2,
        "RocketHQElectrode_2": 2,
        "RocketHQElectrode_3": 2,
        "Togepi": 0
    }

    if world.options.randomize_static_pokemon:
        for pokemon, count in static.items():
            new_pokemon = get_random_pokemon_id(random)
            base_flag = "AP_Static_" + pokemon
            if count == 0:
                address = data.rom_addresses[base_flag] + 1
                write_bytes(patched_rom, [new_pokemon], address)
            else:
                for i in range(1, count + 1):
                    address = data.rom_addresses[base_flag + "_" + str(i)] + 1
                    write_bytes(patched_rom, [new_pokemon], address)

    if world.options.randomize_starters:
        for i in range(1, 5):
            cyndaquil_address = data.rom_addresses["AP_Starter_CYNDAQUIL_" + str(i)] + 1
            cyndaquil_mon = data.pokemon[world.generated_starters[0][0]].id
            totodile_address = data.rom_addresses["AP_Starter_TOTODILE_" + str(i)] + 1
            totodile_mon = data.pokemon[world.generated_starters[1][0]].id
            chikorita_address = data.rom_addresses["AP_Starter_CHIKORITA_" + str(i)] + 1
            chikorita_mon = data.pokemon[world.generated_starters[2][0]].id
            write_bytes(patched_rom, [cyndaquil_mon], cyndaquil_address)
            write_bytes(patched_rom, [totodile_mon], totodile_address)
            write_bytes(patched_rom, [chikorita_mon], chikorita_address)
            if i == 4:
                write_bytes(patched_rom, [get_random_helditem(random)], cyndaquil_address + 2)
                write_bytes(patched_rom, [get_random_helditem(random)], totodile_address + 2)
                write_bytes(patched_rom, [get_random_helditem(random)], chikorita_address + 2)

    if world.options.randomize_wilds:
        for address_name, address in data.rom_addresses.items():
            if (address_name.startswith("AP_WildGrass")):
                cur_address = address + 4
                for i in range(7):
                    random_poke = get_random_pokemon_id(random)
                    write_bytes(patched_rom, [random_poke], cur_address)  # morn
                    write_bytes(patched_rom, [random_poke], cur_address + 14)  # day
                    write_bytes(patched_rom, [random_poke], cur_address + 28)  # nite
                    cur_address += 2
            if (address_name.startswith("AP_WildWater")):
                cur_address = address + 2
                for i in range(3):
                    write_bytes(patched_rom, [get_random_pokemon_id(random)], cur_address)
                    cur_address += 2
            if address_name == "AP_Misc_Intro_Wooper":
                write_bytes(patched_rom, [get_random_pokemon_id(random)], address + 1)

    if world.options.normalize_encounter_rates:
        write_bytes(patched_rom, [14, 0, 28, 2, 42, 4, 57, 6, 71, 8, 86, 10, 100, 12],
                    data.rom_addresses["AP_Prob_GrassMon"])
        write_bytes(patched_rom, [33, 0, 66, 2, 100, 4],
                    data.rom_addresses["AP_Prob_WaterMon"])

    if world.options.full_tmhm_compatibility:
        address = data.rom_addresses["BaseData"]
        for i in range(251):
            address += 24
            write_bytes(patched_rom, [255, 255, 255, 255, 255, 255, 255, 15], address)
            address += 8

    if world.options.randomize_learnsets > 0:
        for pkmn_name, pkmn_data in world.generated_pokemon.items():
            address = data.rom_addresses["AP_EvosAttacks_" + pkmn_name]
            address = address + sum([len(evo) for evo in pkmn_data.evolutions]) + 1
            for move in pkmn_data.learnset:
                move_id = data.moves[move.move].id
                write_bytes(patched_rom, [move.level, move_id], address)
                address += 2

    for trainer_name, trainer_data in world.generated_trainers.items():
        address = data.rom_addresses["AP_TrainerParty_" + trainer_name]
        address += trainer_data.name_length + 1  # skip name and type
        for pokemon in trainer_data.pokemon:
            pokemon_data = [pokemon[0]]
            pokemon_data.append(data.pokemon[pokemon[1]].id)
            if trainer_data.trainer_type in ["TRAINERTYPE_ITEM_MOVES", "TRAINERTYPE_ITEM"]:
                item_id = item_const_name_to_id(pokemon[2])
                pokemon_data.append(item_id)
            if trainer_data.trainer_type in ["TRAINERTYPE_ITEM_MOVES", "TRAINERTYPE_MOVES"]:
                for i in range(-4, 0):
                    if pokemon[i] != "NO_MOVE":
                        move_id = data.moves[pokemon[i]].id
                        pokemon_data.append(move_id)
            write_bytes(patched_rom, pokemon_data, address)
            address += len(pokemon)

    if world.options.blind_trainers:
        address = data.rom_addresses["AP_Setting_Blind_Trainers"]
        write_bytes(patched_rom, [0xC9], address)  # 0xC9 = ret

    if not world.options.item_receive_sound:
        address = data.rom_addresses["AP_Setting_ItemSFX"] + 1
        write_bytes(patched_rom, [0], address)

    if world.options.reusable_tms:
        address = data.rom_addresses["AP_Setting_ReusableTMs"] + 1
        write_bytes(patched_rom, [1], address)

    if world.options.guaranteed_catch:
        address = data.rom_addresses["AP_Setting_GuaranteedCatch"] + 1
        write_bytes(patched_rom, [1], address)

    if world.options.minimum_catch_rate > 0:
        address = data.rom_addresses["AP_Setting_MinCatchrate"] + 1
        write_bytes(patched_rom, [world.options.minimum_catch_rate], address)

    if world.options.better_marts:
        mart_address = data.rom_addresses["Marts"]
        better_mart_address = data.rom_addresses["MartBetterMart"] - 0x10000
        better_mart_bytes = better_mart_address.to_bytes(2, "little")
        for i in range(33):
            # skip goldenrod and celadon
            if i not in [6, 7, 8, 9, 10, 11, 12, 24, 25, 26, 27, 28]:
                write_bytes(patched_rom, better_mart_bytes, mart_address)
            mart_address += 2

    exp_modifier_address = data.rom_addresses["AP_Setting_ExpModifier"] + 1
    write_bytes(patched_rom, [world.options.experience_modifier], exp_modifier_address)

    start_inventory_address = data.rom_addresses["AP_Start_Inventory"]
    start_inventory = world.options.start_inventory.value.copy()
    for item, quantity in start_inventory.items():
        if quantity > 99:
            quantity = 99
        elif quantity == 0:
            quantity = 1
        item_code = reverse_offset_item_value(world.item_name_to_id[item])
        if item_code < 256:
            write_bytes(patched_rom, [item_code, quantity], start_inventory_address)
            start_inventory_address += 2

    # Set slot name
    for i, byte in enumerate(world.multiworld.player_name[world.player].encode("utf-8")):
        write_bytes(patched_rom, [byte], data.rom_addresses["AP_Seed_Name"] + i)

    out_file_name = world.multiworld.get_out_file_name_base(world.player)
    output_path = os.path.join(output_directory, f"{out_file_name}.gbc")
    with open(output_path, "wb") as out_file:
        out_file.write(patched_rom)
    patch = PokemonCrystalDeltaPatch(os.path.splitext(output_path)[0] + ".apcrystal",
                                     player=world.player, player_name=world.multiworld.player_name[world.player],
                                     patched_path=output_path)

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


def get_random_move(random):
    randommoves = [move.id for _name, move in data.moves.items() if not move.is_hm and move.id > 0]
    return random.choice(randommoves)


def get_random_helditem(random):
    helditems = [item_id for item_id, item in data.items.items(
    ) if "Unique" not in item.tags and "INVALID" not in item.tags]
    return random.choice(helditems)
