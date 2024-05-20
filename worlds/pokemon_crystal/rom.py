from typing import TYPE_CHECKING
import os
import pkgutil
import bsdiff4
import copy

from worlds.Files import APDeltaPatch
from settings import get_settings
from .phone_data import phone_scripts

from .items import reverse_offset_item_value, item_const_name_to_id
from .data import data
from .utils import get_random_pokemon_id, convert_to_ingame_text, get_random_filler_item

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
    random = world.random
    base_rom = get_base_rom_as_bytes()
    base_patch = pkgutil.get_data(__name__, "data/basepatch.bsdiff4")
    patched_rom = bytearray(bsdiff4.patch(base_rom, base_patch))

    for location in world.multiworld.get_locations(world.player):
        if location.address is None:
            continue

        if location.item and location.item.player == world.player:
            item_id = reverse_offset_item_value(location.item.code)
            item_id = item_id - 256 if item_id > 256 else item_id
            write_bytes(patched_rom, [item_id], location.rom_address)
        else:
            write_bytes(patched_rom, [item_const_name_to_id("AP_ITEM")], location.rom_address)

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
                write_bytes(patched_rom, [item_const_name_to_id(get_random_filler_item(random))], cyndaquil_address + 2)
                write_bytes(patched_rom, [item_const_name_to_id(get_random_filler_item(random))], totodile_address + 2)
                write_bytes(patched_rom, [item_const_name_to_id(get_random_filler_item(random))], chikorita_address + 2)

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

        for fish_name, fish_data in data.fish.items():
            cur_address = data.rom_addresses["AP_FishMons_" + fish_name] + 1
            for i, _poke in enumerate(fish_data.old):
                if world.options.normalize_encounter_rates:
                    encounter_rate = int(((i + 1) / 3) * 255)
                    write_bytes(patched_rom, [encounter_rate], cur_address - 1)
                random_poke = get_random_pokemon_id(random)
                write_bytes(patched_rom, [random_poke], cur_address)
                cur_address += 3
            for i, _poke in enumerate(fish_data.good):
                if world.options.normalize_encounter_rates:
                    encounter_rate = int(((i + 1) / 4) * 255)
                    write_bytes(patched_rom, [encounter_rate], cur_address - 1)
                random_poke = get_random_pokemon_id(random)
                write_bytes(patched_rom, [random_poke], cur_address)
                cur_address += 3
            for i, _poke in enumerate(fish_data.super):
                if world.options.normalize_encounter_rates:
                    encounter_rate = int(((i + 1) / 4) * 255)
                    write_bytes(patched_rom, [encounter_rate], cur_address - 1)
                random_poke = get_random_pokemon_id(random)
                write_bytes(patched_rom, [random_poke], cur_address)
                cur_address += 3

        for tree_set in ["Canyon", "Town", "Route", "Kanto", "Lake", "Forest"]:
            address = data.rom_addresses["TreeMonSet_" + tree_set] + 1
            for i in range(0, 2):
                for j in range(0, 6):
                    if world.options.normalize_encounter_rates:
                        encounter_rate = int(((j + 1) / 6) * 255)
                        write_bytes(patched_rom, [encounter_rate], address - 1)
                    random_poke = get_random_pokemon_id(random)
                    write_bytes(patched_rom, [random_poke], address)
                    address += 3
                address += 1
        address = data.rom_addresses["TreeMonSet_Rock"] + 1
        for i in range(0, 2):
            if world.options.normalize_encounter_rates:
                write_bytes(patched_rom, [((i + 1) * 128) - 1], address - 1)
                random_poke = get_random_pokemon_id(random)
                write_bytes(patched_rom, [random_poke], address)
                address += 3

    if world.options.normalize_encounter_rates:
        write_bytes(patched_rom, [14, 0, 28, 2, 42, 4, 57, 6, 71, 8, 86, 10, 100, 12],
                    data.rom_addresses["AP_Prob_GrassMon"])
        write_bytes(patched_rom, [33, 0, 66, 2, 100, 4],
                    data.rom_addresses["AP_Prob_WaterMon"])

    if world.options.randomize_learnsets > 0:
        for pkmn_name, pkmn_data in world.generated_pokemon.items():
            address = data.rom_addresses["AP_EvosAttacks_" + pkmn_name]
            address = address + sum([len(evo) for evo in pkmn_data.evolutions]) + 1
            for move in pkmn_data.learnset:
                move_id = data.moves[move.move].id
                write_bytes(patched_rom, [move.level, move_id], address)
                address += 2

    for pkmn_name, pals in world.generated_palettes.items():
        address = data.rom_addresses["AP_Stats_Palette_" + pkmn_name]
        write_bytes(patched_rom, pals[0] + pals[1], address)

    for pkmn_name, pkmn_data in world.generated_pokemon.items():
        tm_bytes = [0, 0, 0, 0, 0, 0, 0, 0]
        for tm in pkmn_data.tm_hm:
            tm_num = data.tmhm[tm].tm_num
            tm_bytes[int(tm_num / 8)] |= 1 << tm_num % 8
        address = data.rom_addresses["AP_Stats_TMHM_" + pkmn_name]
        write_bytes(patched_rom, tm_bytes, address)

    if world.options.randomize_types > 0:
        for pkmn_name, pkmn_data in world.generated_pokemon.items():
            address = data.rom_addresses["AP_Stats_Types_" + pkmn_name]
            pkmn_types = pkmn_data.types if len(pkmn_data.types) == 2 else [pkmn_data.types[0], pkmn_data.types[0]]
            type_ids = [data.type_ids[pkmn_types[0]], data.type_ids[pkmn_types[1]]]
            write_bytes(patched_rom, type_ids, address)

    if world.options.randomize_base_stats.value > 0:
        for pkmn_name, pkmn_data in world.generated_pokemon.items():
            address = data.rom_addresses["AP_Stats_Base_" + pkmn_name]
            write_bytes(patched_rom, pkmn_data.base_stats, address)

    for trainer_name, trainer_data in world.generated_trainers.items():
        address = data.rom_addresses["AP_TrainerParty_" + trainer_name]
        address += trainer_data.name_length + 1  # skip name and type
        for pokemon in trainer_data.pokemon:
            pokemon_data = [pokemon[0], data.pokemon[pokemon[1]].id]
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

    if world.options.randomize_tm_moves.value:
        tm_moves = [tm_data.move_id for _name, tm_data in world.generated_tms.items()]
        address = data.rom_addresses["AP_Setting_TMMoves"]
        write_bytes(patched_rom, tm_moves, address)

    if world.options.enable_mischief:
        address = data.rom_addresses["AP_Misc_FuchsiaTrainers"] + 1
        write_bytes(patched_rom, [0x0a], address + 2)  # spin speed
        for c in world.generated_misc.fu:
            write_coords = [c[1] + 4, c[0] + 4]
            write_bytes(patched_rom, write_coords, address)
            address += 13
        for pair in world.generated_misc.sa.pairs:
            addresses = [data.rom_addresses["AP_Misc_SG_" + warp] + 2 for warp in pair]
            ids = [world.generated_misc.sa.warps[warp].id for warp in pair]
            write_bytes(patched_rom, [ids[1]], addresses[0])  # reverse ids
            write_bytes(patched_rom, [ids[0]], addresses[1])
        eg_warp_counts = [1, 3, 3, 2]
        for i in range(0, 4):
            address = data.rom_addresses["AP_Misc_EG_" + str(i + 1)]
            warp_count = eg_warp_counts[i]
            line_warps = world.generated_misc.ec[i][:warp_count]
            line_warps.sort(key=lambda warp: warp[0])
            for warp in line_warps:
                write_bytes(patched_rom, [warp[1], warp[0]], address)
                address += 5
        for i in range(0, 3):
            address = data.rom_addresses["AP_Misc_OK_" + str(i + 1)]
            write_bytes(patched_rom, [0x65, 0xFF], address + 1)
            write_bytes(patched_rom, [0xFF], address + 4)
        for i in range(0, 5):
            answer = world.generated_misc.ra[i]
            byte = 0x08 if answer == "Y" else 0x09
            address = data.rom_addresses["AP_Misc_Ra_" + str(i + 1)]
            write_bytes(patched_rom, [byte], address)

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

    for label in ["AP_Setting_HMBadge_Cut1",
                  "AP_Setting_HMBadge_Cut2",
                  "AP_Setting_HMBadge_Fly",
                  "AP_Setting_HMBadge_Surf1",
                  "AP_Setting_HMBadge_Surf2",
                  "AP_Setting_HMBadge_Strength1",
                  "AP_Setting_HMBadge_Strength2",
                  "AP_Setting_HMBadge_Flash",
                  "AP_Setting_HMBadge_Whirlpool1",
                  "AP_Setting_HMBadge_Whirlpool2",
                  "AP_Setting_HMBadge_Waterfall1",
                  "AP_Setting_HMBadge_Waterfall2"]:
        address = data.rom_addresses[label] + 1
        write_bytes(patched_rom, [world.options.hm_badge_requirements], address)

    exp_modifier_address = data.rom_addresses["AP_Setting_ExpModifier"] + 1
    write_bytes(patched_rom, [world.options.experience_modifier], exp_modifier_address)

    elite_four_text = convert_to_ingame_text("{:02d}".format(world.options.elite_four_badges.value))
    write_bytes(patched_rom, elite_four_text, data.rom_addresses["AP_Setting_VictoryRoadBadges_Text"] + 1)
    write_bytes(patched_rom, [world.options.elite_four_badges - 1],
                data.rom_addresses["AP_Setting_VictoryRoadBadges"] + 1)
    rocket_badges = world.options.elite_four_badges - 2 if world.options.elite_four_badges > 1 else 0
    write_bytes(patched_rom, [rocket_badges], data.rom_addresses["AP_Setting_RocketBadges"] + 1)

    red_text = convert_to_ingame_text("{:02d}".format(world.options.red_badges.value))
    write_bytes(patched_rom, red_text, data.rom_addresses["AP_Setting_RedBadges_Text"] + 1)
    write_bytes(patched_rom, red_text, data.rom_addresses["AP_Setting_RedBadges_Text2"] + 1)
    write_bytes(patched_rom, [world.options.red_badges - 1], data.rom_addresses["AP_Setting_RedBadges"] + 1)

    for i in range(0, 16):
        address = data.rom_addresses["AP_Setting_PhoneCallTrapTexts"] + (i * 0x400)
        script = world.generated_phone_traps[i]
        s_bytes = script.get_script_bytes()
        # print(len(s_bytes))
        write_bytes(patched_rom, s_bytes, address)
        address = data.rom_addresses["AP_Setting_SpecialCalls"] + (6 * i) + 2
        write_bytes(patched_rom, [script.caller_id], address)

    phone_location_bytes = []
    for loc in world.generated_phone_indices:
        phone_location_bytes += list(loc.to_bytes(4, "little"))
    phone_location_address = data.rom_addresses["AP_Setting_Phone_Trap_Locations"]
    write_bytes(patched_rom, phone_location_bytes, phone_location_address)

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
    item = random.choice(helditems)
    return item if item < 256 else item - 256
