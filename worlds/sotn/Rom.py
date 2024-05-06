import Utils
import random
import logging
from sys import platform
from worlds.Files import APDeltaPatch
from Utils import home_path, open_filename, messagebox
from settings import get_settings
from worlds.AutoWorld import World
from BaseClasses import ItemClassification
from .Items import (ItemData, item_table, IType, get_item_data_shop, tile_id_offset, hand_type_table, chest_type_table,
                    helmet_type_table, cloak_type_table, acc_type_table)
from .Locations import location_table
from .Candles import Candles
from .Enemies import Enemies

import hashlib
import os
import subprocess
import bsdiff4

USHASH = "acbb3a2e4a8f865f363dc06df147afa2"
AUDIOHASH = "8f4b1df20c0173f7c2e6a30bd3109ac8"
logger = logging.getLogger("Client")

shop_stock = {
        "Potion": 0x047a309c,
        "High potion": 0x047a30a4,
        "Elixir": 0x047a30ac,
        "Manna prism": 0x047a30b4,
        "Antivenom": 0x047a30bc,
        "Uncurse": 0x047a30c4,
        "Hammer": 0x047a30cc,
        "Magic missile": 0x047a30d4,
        "Bwaka knife": 0x047a30dc,
        "Boomerang": 0x047a30e4,
        "Javelin": 0x047a30ec,
        "Fire boomerang": 0x047a30f4,
        "Shuriken": 0x047a30fc,
        "Cross shuriken": 0x047a3104,
        "Buffalo star": 0x047a310c,
        "Flame star": 0x047a3114,
        "Library card": 0x047a311c,
        "Meal ticket": 0x047a3124,
        "Saber": 0x047a312c,
        "Mace": 0x047a3134,
        "Damascus sword": 0x047a313c,
        "Firebrand": 0x047a3144,
        "Icebrand": 0x047a314c,
        "Thunderbrand": 0x047a3154,
        "Harper": 0x047a315c,
        "Leather shield": 0x047a3164,
        "Iron shield": 0x047a316c,
        "Velvet hat": 0x047a3174,
        "Leather hat": 0x047a317c,
        "Circlet": 0x047a3184,
        "Silver crown": 0x047a318c,
        "Iron cuirass": 0x047a3194,
        "Steel cuirass": 0x047a319c,
        "Diamond plate": 0x047a31a4,
        "Reverse cloak": 0x047a31ac,
        "Elven cloak": 0x047a31b4,
        "Joseph's cloak": 0x047a31bc,
        "Medal": 0x047a31c4,
        "Ring of pales": 0x047a31cc,
        "Gauntlet": 0x047a31d4,
        "Duplicator": 0x047a31dc
}


class SOTNDeltaPatch(APDeltaPatch):
    hash = USHASH
    game = "Symphony of the Night"
    patch_file_ending = ".apsotn"
    result_file_ending: str = ".cue"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def patch(self, target: str):
        """Base + Delta -> Patched"""
        file_name = target[:-4]
        patch_path = file_name + ".apsotn"

        audio_name = target[0:target.rfind('/') + 1]
        audio_name += "Castlevania - Symphony of the Night (USA) (Track 2).bin"

        if os.path.exists(audio_name):
            logger.info("Track 2 already exist")
        else:
            logger.info("Copying track 2")
            with open(get_settings().sotn_settings.audio_file, "rb") as infile:
                audio_rom = bytearray(infile.read())
            with open(audio_name, "wb") as stream:
                stream.write(audio_rom)

        if not (os.path.exists(file_name + ".bin") and os.path.exists(file_name + ".cue")):
            logger.info("Patched ROM doesn't exist")

            with open(patch_path, "rb") as infile:
                diff_patch = bytes(infile.read())
            with open(get_settings().sotn_settings.rom_file, "rb") as infile:
                original_rom = bytearray(infile.read())

            patched_rom = original_rom.copy()
            music_slice = original_rom[0x000affd0:0x000b9ea5]  # Size 0x9ed5 / 40661
            original_slice = music_slice + original_rom[0x04389c6c:0x06a868a4]

            patched_slice = bsdiff4.patch(bytes(original_slice), diff_patch)

            # Patch Clock Room cutscene
            write_char(patched_rom, 0x0aeaa0, 0x00)
            write_char(patched_rom, 0x119af4, 0x00)

            # patchPowerOfSireFlashing Patches researched by MottZilla.
            write_word(patched_rom, 0x00136580, 0x03e00008)

            patched_rom[0x000affd0:0x000b9ea5] = patched_slice[0:0x9ed5]
            patched_rom[0x04389c6c:0x06a868a4] = patched_slice[0x9ed5:]

            # Duplicate Sanity options
            patched_rom[0xf50c6] = patched_rom[0x0438d85e]

            with open(target[:-4] + ".bin", "wb") as stream:
                stream.write(patched_rom)

            target_bin = target[:-4] + ".bin"
            track1_name = target[target.rfind('/') + 1:-4]

            cue_file = f'FILE "{track1_name}.bin" BINARY\n  TRACK 01 MODE2/2352\n\tINDEX 01 00:00:00\n'
            cue_file += f'FILE "Castlevania - Symphony of the Night (USA) (Track 2).bin" BINARY\n  TRACK 02 AUDIO\n'
            cue_file += f'\tINDEX 00 00:00:00\n\tINDEX 01 00:02:00'
            with open(target[:-4] + ".cue", 'wb') as outfile:
                outfile.write(bytes(cue_file, 'utf-8'))

            error_recalc_path = ""
            if platform == "win32":
                if os.path.exists("error_recalc.exe"):
                    error_recalc_path = "error_recalc.exe"
                elif os.path.exists(f"{home_path('lib')}\\error_recalc.exe"):
                    error_recalc_path = f"{home_path('lib')}\\error_recalc.exe"
            elif platform.startswith("linux") or platform.startswith("darwin"):
                if os.path.exists("error_recalc"):
                    error_recalc_path = "./error_recalc"
                elif os.path.exists(f"{home_path('lib')}/error_recalc"):
                    error_recalc_path = f"{home_path('lib')}/error_recalc"
            else:
                logger.info("Error_recalc not find on /lib folder !!!")

            if error_recalc_path == "":
                try:
                    error_recalc_path = open_filename("Error recalc binary", (("All", "*.*"),))
                except Exception as e:
                    messagebox("Error", str(e), error=True)

            if error_recalc_path != "":
                subprocess.call([error_recalc_path, target_bin])
            else:
                messagebox("Error", "Could not find Error_recalc binary", error=True)
        else:
            logger.info("Patched ROM already exist")


def get_base_rom_bytes() -> bytes:
    with open(get_settings().sotn_settings.rom_file, "rb") as infile:
        base_rom_bytes = bytes(infile.read())

    with open(get_settings().sotn_settings.audio_file, "rb") as infile:
        audio_rom_bytes = bytes(infile.read())

    basemd5 = hashlib.md5()
    basemd5.update(base_rom_bytes)
    if USHASH != basemd5.hexdigest():
        raise Exception('Supplied Track 1 Base Rom does not match known MD5 for SLU067 release. '
                        'Get the correct game and version, then dump it')

    audiomd5 = hashlib.md5()
    audiomd5.update(audio_rom_bytes)
    if AUDIOHASH != audiomd5.hexdigest():
        raise Exception('Supplied Track 2 Audio Rom does not match known MD5 for SLU067 release. '
                        'Get the correct game and version, then dump it')

    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options = get_settings()
    if not file_name:
        file_name = options["sotn_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


def write_char(buffer, address: int, value: int):
    buffer[address] = (value & 0xFF)


def write_short(buffer, address: int, value: int):
    x1, x2 = (value & 0xFFFF).to_bytes(2, 'little')
    buffer[address] = x1
    buffer[address + 1] = x2


def write_word(buffer, address: int, value):
    x1, x2, x3, x4 = (value & 0xFFFFFFFF).to_bytes(4, 'little')
    buffer[address] = x1
    buffer[address + 1] = x2
    buffer[address + 2] = x3
    buffer[address + 3] = x4
    return address + 4


def replace_shop_text(buffer, new_text):
    start_address = 0x047d5650

    for c in new_text:
        if c == " ":
            write_char(buffer, start_address, 0x00)
        else:
            write_char(buffer, start_address, ord(c) - 0x20)
        start_address += 1

    write_char(buffer, start_address, 0xff)
    write_char(buffer, start_address + 1, 0x00)


# ALWAYS REMEMBER that the slice will change if more addresses are added Slice: 0x04389c6c:0x06a868a4
# Music extra slice 0x000affd0:0x000b0c2c changed max to 0x000b9ea5 for enemy drop

def patch_rom(world: World, output_directory: str) -> None:
    original_rom = bytearray(get_base_rom_bytes())
    patched_rom = original_rom.copy()
    no4 = world.options.opened_no4
    are = world.options.opened_are
    no2 = world.options.opened_no2
    songs = world.options.rng_songs
    shop = world.options.rng_shop
    shop_prog = world.options.noprog_shop
    shop_lib = world.options.lib_shop
    prices = world.options.rng_prices
    bosses = world.options.bosses_need
    exp = world.options.exp_need
    candles = world.options.rng_candles
    candles_prog = world.options.noprog_candles
    drops = world.options.rng_drops
    drops_prog = world.options.noprog_drops
    esanity = world.options.enemysanity
    dsanity = world.options.dropsanity
    if bosses > 20:
        bosses = 20
    if exp > 20:
        exp = 20
    # Convert exploration to rooms
    exp = int((exp * 10) / 0.107)

    relics_vlad = ["Heart of Vlad", "Tooth of Vlad", "Rib of Vlad", "Ring of Vlad", "Eye of Vlad"]

    for loc in world.multiworld.get_locations(world.player):
        if loc.item and loc.item.player == world.player:
            if (loc.item.name == "Victory" or loc.item.name == "Boss token" or "Enemysanity" in loc.name or
                    "Dropsanity" in loc.name):
                continue
            item_data = item_table[loc.item.name]
            loc_data = location_table[loc.name]
            if loc_data.rom_address:
                for address in loc_data.rom_address:
                    if loc_data.no_offset:
                        if item_data.type in [IType.RELIC, IType.TRAP, IType.BOOST]:
                            write_short(patched_rom, address, 0x0000)
                        else:
                            write_short(patched_rom, address, item_data.get_item_id_no_offset())
                    else:
                        if loc_data.can_be_relic:
                            if item_data.type == IType.RELIC:
                                write_short(patched_rom, address, item_data.get_item_id())
                                if loc.name == "Jewel of Open":
                                    replace_shop_text(patched_rom, loc.item.name)
                                    # Fix shop menu check
                                    write_char(patched_rom, 0x047dbde0, item_data.get_item_id() + 0x64)
                            else:
                                # Skill of wolf, bat card can't be item. Replace with ghost card instead
                                if loc.name == "Skill of Wolf" or loc.name == "Bat Card":
                                    write_short(patched_rom, address, 0x0013)
                                elif loc.name == "Jewel of Open":
                                    replace_shop_text(patched_rom, "Ghost Card")
                                    write_short(patched_rom, address, 0x0013)
                                    write_char(patched_rom, 0x047dbde0, 0x77)
                                elif loc.name in relics_vlad:
                                    write_short(patched_rom, address, 0x0013)
                                else:
                                    write_short(patched_rom, address, loc_data.relic_index)
                                    write_short(patched_rom, address - 4, 0x000c)
                                    for a in loc_data.item_address:
                                        if loc.item.name == "Life Vessel":
                                            write_short(patched_rom, a, 0x0017)
                                        elif loc.item.name == "Heart Vessel":
                                            write_short(patched_rom, a, 0x000c)
                                        else:
                                            write_short(patched_rom, a, item_data.get_item_id())
                        else:
                            if item_data.type == IType.RELIC:
                                write_short(patched_rom, address, 0x0007)
                            else:
                                write_short(patched_rom, address, item_data.get_item_id())
        elif loc.item and loc.item.player != world.player:
            loc_data = location_table[loc.name]
            if loc_data.rom_address:
                for address in loc_data.rom_address:
                    if loc_data.no_offset:
                        write_short(patched_rom, address, 0x0000)
                    else:
                        if loc_data.can_be_relic:
                            if loc.name == "Skill of Wolf" or loc.name == "Bat Card":
                                write_short(patched_rom, address, 0x0013)
                            elif loc.name == "Jewel of Open":
                                write_short(patched_rom, address, 0x0013)
                                replace_shop_text(patched_rom, "Ghost Card")
                                write_char(patched_rom, 0x047dbde0, 0x77)
                            elif loc.name in relics_vlad:
                                write_short(patched_rom, address, 0x0013)
                            else:
                                write_short(patched_rom, address, loc_data.relic_index)
                                write_short(patched_rom, address - 4, 0x000c)
                                if (loc.item.classification == ItemClassification.filler or
                                        loc.item.classification == ItemClassification.trap):
                                    for a in loc_data.item_address:
                                        write_short(patched_rom, a, 0x0004)
                                else:
                                    for a in loc_data.item_address:
                                        write_short(patched_rom, a, 0x0003)
                        else:
                            if loc.item.classification == ItemClassification.filler:
                                write_short(patched_rom, address, 0x0004)
                            else:
                                write_short(patched_rom, address, 0x0003)

    offset = 0x0492df64
    offset = write_word(patched_rom, offset, 0xa0202ee8)
    offset = write_word(patched_rom, offset, 0x080735cc)
    offset = write_word(patched_rom, offset, 0x00000000)
    write_word(patched_rom, 0x4952454, 0x0806b647)
    write_word(patched_rom, 0x4952474, 0x0806b647)

    # Patch Alchemy Laboratory cutscene
    write_short(patched_rom, 0x054f0f44 + 2, 0x1000)

    """
    The flag that get set on NO4 switch: 0x03be1c and the instruction is jz, r2, 80181230 on 0x5430404 we patched
    to jne r0, r0 so it never branch.

    The flag that get set on ARE switch: 0x03be9d and the instruction is jz, r2, 801b6f84 on 0x440110c we patched
    to jne r0, r0 so it never branch.

    The flag that get set on NO2 switch: 0x03be4c and the instruction is jz, r2, 801c1028 on 0x46c0968 we patched
    to jne r0, r0 so it never branch.
    """
    #  NO3 and NP3 doesn't share instruction.
    if no4:
        # Open NO4 too soon, make death skippable. Keep close till visit Alchemy Laboratory
        # write_word(patched_rom, 0x4ba8798, 0x14000005)
        write_word(patched_rom, 0x05430404, 0x14000005)

    if are:
        write_word(patched_rom, 0x0440110c, 0x14000066)

    if no2:
        write_word(patched_rom, 0x046c0968, 0x1400000b)
    # Write bosses need it on index -1 of RNO0
    write_char(patched_rom, 0x04f85ae3, bosses)
    # Write exploration need it on index -3 of RNO0
    write_short(patched_rom, 0x04f85ae1, exp)
    """
    The instruction that check relics of Vlad is jnz r2, 801c1790 we gonna change to je r0, r0 so it's always 
    branch. ROM is @ 0x4fcf7b4 and RAM is @ 0x801c132c
    """
    write_word(patched_rom, 0x04fcf7b4, 0x10000118)

    seed_num = world.multiworld.seed
    write_seed(patched_rom, seed_num)

    if songs:
        randomize_music(patched_rom)

    if shop:
        randomize_shop(patched_rom, shop_prog, shop_lib)

    if prices != 0 and prices <= 3:
        randomize_prices(patched_rom, prices)

    randomize_candles(patched_rom, candles, candles_prog)
    randomize_drops(patched_rom, drops, drops_prog)

    sanity = 0

    if esanity:
        sanity |= (1 << 0)
    if dsanity:
        sanity |= (1 << 1)

    # 0xf50c6
    write_char(patched_rom, 0x0438d85e, sanity)

    music_slice = original_rom[0x000affd0:0x000b9ea5]
    music_patched = patched_rom[0x000affd0:0x000b9ea5]

    original_slice = music_slice + original_rom[0x04389c6c:0x06a868a4]
    patched_slice = music_patched + patched_rom[0x04389c6c:0x06a868a4]

    print("Generating patch. Please wait!")

    patch = bsdiff4.diff(bytes(original_slice), bytes(patched_slice))

    patch_path = os.path.join(output_directory, f"{world.multiworld.get_out_file_name_base(world.player)}.apsotn")

    with open(patch_path, 'wb') as outfile:
        outfile.write(patch)


def write_seed(buffer, seed) -> None:
    write_short(buffer, 0x043930c4, 0x78b4)
    write_short(buffer, 0x043930d4, 0x78d4)
    write_short(buffer, 0x0439312c, 0x78b4)
    write_short(buffer, 0x0439313c, 0x78d4)
    write_short(buffer, 0x04393484, 0x78b4)
    write_short(buffer, 0x04393494, 0x78d4)
    # No idea why, but SOTN.io write those values.

    start_address = 0x04389c6c

    for n in str(seed):
        write_char(buffer, start_address, 0x82)
        start_address += 1
        write_char(buffer, start_address, ord(n) + 0x1f)
        start_address += 1
    write_char(buffer, start_address, 0x00)
    write_char(buffer, start_address + 1, 0x00)
    write_char(buffer, start_address + 2, 0x00)


def write_to_file(buffer, filename=""):
    if filename == "":
        output_file = get_settings().sotn_settings.rom_file
    else:
        output_file = filename

    with open(output_file, 'wb') as outfile:
        outfile.write(buffer)


def randomize_music(buffer):
    music = {
        "Lost Painting": 0x01,
        "Curse Zone": 0x03,
        "Requiem for the gods": 0x05,
        "Rainbow cemetery": 0x07,
        "Wood carving partita": 0x09,
        "Crystal teardrops": 0x0b,
        "Marble gallery": 0x0d,
        "Dracula's castle": 0x0f,
        "The tragic prince": 0x11,
        "Tower of mist": 0x13,
        "Door of holy spirits": 0x15,
        "Dance of pales": 0x17,
        "Abandoned pít": 0x19,
        "Heavenly doorway": 0x1b,
        "Festival of servants": 0x1d,
        "Wandering ghosts": 0x23,
        "The door to the abyss": 0x25,
        "Dance of gold": 0x2e,
        "Enchanted banquet": 0x30,
        "Death ballad": 0x34,
        "Final toccata": 0x38
    }
    music_addresses = {
        "Lost Painting": [0x00b0788, 0x6757ad8, 0x6757b74, 0x00b06d8, 0x00b080c],
        "Curse Zone": [0x00b0704, 0x6a7c4f0, 0x6a7c58c],
        "Requiem for the gods": [0x00b00d8],
        "Rainbow cemetery": [0x00b0054, 0x609505c],
        "Wood carving partita": [0x00b0028, 0x00b036c, 0x47e5ec4, 0x47e6060],
        "Crystal teardrops": [0x00b015c, 0x61d1fa8, 0x61d1fec, 0x61d2188],
        "Marble gallery": [0x00affd0],
        "Dracula's castle": [0x00b0104, 0x00b0c2c, 0x4ba6cb0, 0x4bb0064],
        "The tragic prince": [0x00b020c, 0x55a2f90, 0x55a3008],
        "Tower of mist": [0x00afffc],
        "Door of holy spirits": [0x00b0838, 0x6487b44, 0x6487bec],
        "Dance of pales": [0x00b0080, 0x5fea9dc],
        "Abandoned pít": [0x00b00ac, 0x66cc898, 0x00b075c, 0x6644d10],
        "Heavenly doorway": [0x00b01b4, 0x00b0864],
        "Festival of servants": [0x47e5e08, 0x54eca88, 0x55a2ed0, 0x59ee490, 0x6129480, 0x61d20f4, 0x67ec2bc, 0x689e4f0,
                                 0x69e8318],
        "Wandering ghosts": [0x00b0188, 0x6126570],
        "The door to the abyss": [0x00b0130, 0x00b07e0],
        "Dance of gold": [0x00b01e0, 0x54ecb58, 0x54ecbd4],
        "Enchanted banquet": [0x5b074f4, 0x6757a78],
        "Death ballad": [0x56dc624, 0x5fddd24, 0x5fddd80, 0x5fddda0, 0x5fdde14, 0x6094500, 0x6094534, 0x632e8c8,
                         0x65a88e8, 0x65a8908, 0x6644bc4, 0x6a7c490],
        "Final toccata": [0x00b08bc, 0x00b07b4, 0x00b0680, 0x00b06ac, 0x00b0730, 0x00b0890, 0x59ee534, 0x59ee5ac,
                          0x65a8960, 0x65a89f0, 0x67ec31c, 0x67ec3b8]
    }

    for key, value in music_addresses.items():
        rng_song, rng_value = random.choice(list(music.items()))
        for address in value:
            write_char(buffer, address, rng_value)
        music.pop(rng_song)


def randomize_shop(buffer, prog, lib):
    forbid_items = [169, 195, 217, 226]

    if prog:
        forbid_items = [169, 183, 195, 203, 217, 226, 241, 242]

    for i, (key, value) in enumerate(shop_stock.items()):
        if lib and i == 0:
            rng_item = 166
        else:
            rng_item = random.choice([i for i in range(1, 259) if i not in forbid_items])
        item_name: str
        item_data: ItemData
        item_name, item_data = get_item_data_shop(rng_item)
        type_value = 0x00
        offset = -0xa9
        if item_data.type == IType.HELMET:
            type_value = 0x01
        elif item_data.type == IType.ARMOR:
            type_value = 0x02
        elif item_data.type == IType.CLOAK:
            type_value = 0x03
        elif item_data.type == IType.ACCESSORY:
            type_value = 0x04
        else:
            offset = 0x00
        write_char(buffer, value, type_value)
        write_short(buffer, value + 2, rng_item + offset)


def randomize_prices(buffer, prices):
    min_prices = 1
    max_prices = 100

    if prices == 2:
        min_prices = 100
        max_prices = 1000
    if prices == 3:
        min_prices = 1000
        max_prices = 10000

    for key, value in shop_stock.items():
        rng_price = random.randrange(min_prices, max_prices)
        write_word(buffer, value + 4, rng_price)


def randomize_candles(buffer, rng_choice=0, prog=False):
    if rng_choice == 0:
        return

    forbid_items = [169, 195, 217, 226]

    if prog:
        forbid_items = [169, 183, 195, 203, 217, 226, 241, 242]

    rng_item = 0
    rng_type = 0
    for candle in Candles:
        if candle.name == "Stopwatch" and (candle.zone == "NO0" or candle.zone == "RNO0"):
            print(f"DEBUG: Don't change stopwatch")
            continue
        if rng_choice == 1:
            if candle.name in ["Heart", "Big heart"]:
                rng_item = random.choice([0, 1])
            elif candle.name in ["$1", "$25", "$50", "$100", "$250", "$400", "$1000", "$2000"]:
                rng_item = random.choice([2, 3, 4, 5, 6, 7, 9, 10])
            elif (candle.name in
                  ["Dagger", "Axe", "Cross", "Holy water", "Stopwatch", "Bible", "Rebound Stone", "Vibhuti", "Agunea"]):
                rng_item = random.choice([14, 15, 16, 17, 18, 19, 20, 21, 22])
            elif candle.name == "Uncurse":
                rng_item = random.choice([i for i in range(1, 259) if i not in forbid_items])
                rng_type = 1
            else:
                print(f"DEBUG: ERROR {candle.name}")
                pass
        if rng_choice == 2:
            rng_type = random.randrange(0, 2)

            if rng_type == 0:
                rng_item = random.choice([i for i in range(0, 24) if i not in [8, 11, 13]])
            else:
                rng_item = random.choice([i for i in range(1, 259) if i not in forbid_items])

        item_id = (candle.offset << 8) | rng_item
        if candle.offset & rng_item >= tile_id_offset:
            item_id += tile_id_offset
        else:
            if rng_type == 1:
                item_id += tile_id_offset

        for a in candle.addresses:
            write_short(buffer, a, item_id)


def randomize_drops(buffer, rng_choice=0, prog=False):
    if rng_choice == 0:
        return

    forbid_items = [169, 195, 217, 226]

    if prog:
        forbid_items = [169, 183, 195, 203, 217, 226, 241, 242]

    rng_item = 0
    rng_type = 0

    for enemy in Enemies:
        if rng_choice == 1:
            for a in enemy.addresses:
                if enemy.name in ["Heart", "Big heart"]:
                    rng_item = random.choice([0, 1])
                elif enemy.name in ["$1", "$25", "$50", "$100", "$250", "$400", "$1000", "$2000"]:
                    rng_item = random.choice([2, 3, 4, 5, 6, 7, 9, 10])
                elif enemy.name in ["Dagger", "Axe", "Cross", "Holy water", "Stopwatch", "Bible", "Rebound Stone",
                                    "Vibhuti", "Agunea"]:
                    print("DEBUG: NOT Need it anymore for enemies")
                    rng_item = random.choice([14, 15, 16, 17, 18, 19, 20, 21, 22])
                elif enemy.name in hand_type_table:
                    rng_item = random.randrange(1, 169)
                    rng_type = 1
                elif enemy.name in chest_type_table:
                    chest_table = [x for x in range(170, 195) if x not in forbid_items]
                    chest_table.append(258)
                    rng_item = random.choice(chest_table)
                    rng_type = 1
                elif enemy.name in helmet_type_table:
                    rng_item = random.choice([i for i in range(196, 217) if i not in forbid_items])
                    rng_type = 1
                elif enemy.name in cloak_type_table:
                    rng_item = random.choice([i for i in range(218, 226) if i not in forbid_items])
                    rng_type = 1
                elif enemy.name in acc_type_table:
                    rng_item = random.choice([i for i in range(227, 258) if i not in forbid_items])
                    rng_type = 1
                else:
                    print(f"DEBUG: ERROR {enemy.name}")

                item_id = rng_item
                if rng_item >= tile_id_offset:
                    item_id += tile_id_offset
                else:
                    if rng_type == 1:
                        item_id += tile_id_offset

                write_short(buffer, a, item_id)

        if rng_choice == 2:
            for a in enemy.addresses:
                rng_type = random.randrange(0, 2)

                if rng_type == 0:
                    rng_item = random.choice([i for i in range(2, 12) if i not in [8]])
                else:
                    rng_item = random.choice([i for i in range(1, 259) if i not in forbid_items])

                item_id = rng_item
                if rng_item >= tile_id_offset:
                    item_id += tile_id_offset
                else:
                    if rng_type == 1:
                        item_id += tile_id_offset

                write_short(buffer, a, item_id)

