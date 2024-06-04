import Utils
import random
import logging
from sys import platform
from worlds.Files import APDeltaPatch
from Utils import home_path, open_filename, messagebox
from settings import get_settings
from worlds.AutoWorld import World
from BaseClasses import ItemClassification, Item
from .Items import (ItemData, item_table, IType, get_item_data_shop, tile_id_offset, hand_type_table, chest_type_table,
                    helmet_type_table, cloak_type_table, acc_type_table, SotnItem)
from .Locations import location_table, castle_table
from .Candles import Candles
from .Enemies import Enemy_dict, Global_drop

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

limited_locations = ["NO4 - Crystal cloak", "CAT - Mormegil", "RNO4 - Dark Blade", "RNZ0 - Ring of Arcana",
                     "NO3 - Holy mail", "NO3 - Jewel sword", "NZ0 - Basilard", "NZ0 - Sunglasses", "NZ0 - Cloth cape",
                     "DAI - Mystic pendant", "DAI - Ankh of life(Stairs)", "DAI - Morningstar", "DAI - Goggles",
                     "DAI - Silver plate", "DAI - Cutlass", "TOP - Platinum mail(Above Richter)", "TOP - Falchion",
                     "NZ1 - Gold plate", "NZ1 - Bekatowa", "NO1 - Gladius", "NO1 - Jewel knuckles", "LIB - Holy rod",
                     "LIB - Onyx", "LIB - Bronze cuirass", "NO0 - Alucart sword", "NO2 - Broadsword", "NO2 - Estoc",
                     "NO2 - Garnet", "ARE - Blood cloak", "ARE - Shield rod", "ARE - Knight shield(Chapel passage)",
                     "ARE - Holy sword(Hidden attic)", "NO4 - Bandanna", "NO4 - Secret boots", "NO4 - Nunchaku",
                     "NO4 - Knuckle duster(Holy)", "NO4 - Onyx(Holy)", "CHI - Combat knife", "CHI - Ring of ares",
                     "CAT - Bloodstone", "CAT - Icebrand", "CAT - Walk armor", "RNO3 - Beryl circlet",
                     "RNO3 - Talisman", "RNZ0 - Katana", "RNZ0 - Goddess shield", "RDAI - Twilight cloak",
                     "RDAI - Talwar", "RTOP - Sword of dawn", "RTOP - Bastard sword", "RTOP - Royal cloak",
                     "RTOP - Lightning mail", "RNZ1 - Moon rod", "RNZ1 - Sunstone(Hidden room)", "RNZ1 - Luminus",
                     "RNZ1 - Dragon helm", "RNO1 - Shotel", "RLIB - Staurolite", "RLIB - Badelaire",  "RLIB - Opal",
                     "RNO4 - Diamond", "RNO4 - Opal", "RNO4 - Garnet", "RNO4 - Osafune katana", "RNO4 - Alucard shield",
                     "RCHI - Alucard sword", "RCAT - Necklace of j", "RCAT - Diamond", "RNO2 - Sword of hador",
                     "RNO2 - Alucard mail", "RARE - Gram", "RARE - Fury plate(Hidden floor)", "Cube of Zoe",
                     "Power of Wolf", "Skill of Wolf", "Bat Card", "Spirit Orb", "Gravity Boots", "Soul of Wolf",
                     "Soul of Bat", "Faerie Scroll", "Jewel of Open", "Faerie Card", "Fire of Bat", "Leap Stone",
                     "Power of Mist", "Ghost Card", "Form of Mist", "Echo of Bat", "Sword Card", "Holy Symbol",
                     "Merman Statue", "Demon Card", "Gas Cloud", "Eye of Vlad", "Heart of Vlad", "Tooth of Vlad",
                     "Rib of Vlad", "Force of Echo", "Ring of Vlad", "ARE - Minotaurus/Werewolf kill",
                     "CAT - Granfaloon kill", "CHI - Cerberos kill", "DAI - Hippogryph kill", "LIB - Lesser Demon kill",
                     "NO1 - Doppleganger 10 kill", "NO2 - Olrox kill", "NO4 - Scylla kill", "NO4 - Succubus kill",
                     "NZ0 - Slogra and Gaibon kill", "NZ1 - Karasuman kill", "RARE - Fake Trevor/Grant/Sypha kill",
                     "RCAT - Galamoth kill", "RCHI - Death kill", "RDAI - Medusa kill", "RNO1 - Creature kill",
                     "RNO2 - Akmodan II kill", "RNO4 - Doppleganger40 kill", "RNZ0 - Beezelbub kill",
                     "RNZ1 - Darkwing bat kill"]


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

            # Duplicate Seed options
            patched_rom[0xf4ce4:0xf4d50] = patched_rom[0x438d47c:0x438d4e8]

            seed_options = patched_rom[0x438d487]

            if seed_options & (1 << 2):
                # Wing smash timer
                write_word(patched_rom, 0x00134990, 0x00000000)

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
        file_name = options["sotn_settings"]["rom_file"]
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
    shop_prog = world.options.prog_shop
    shop_lib = world.options.lib_shop
    prices = world.options.rng_prices
    bosses = world.options.bosses_need
    exp = world.options.exp_need
    candles = world.options.rng_candles
    candles_prog = world.options.prog_candles
    drops = world.options.rng_drops
    drops_prog = world.options.prog_drops
    esanity = world.options.enemysanity
    dsanity = world.options.dropsanity
    difficult = world.options.difficult
    player_xp = world.options.xp_mod
    player_att = world.options.att_mod
    player_hp = world.options.hp_mod
    bonus_luck = world.options.bonus_luck
    goal = world.options.goal
    #tt = world.options.num_talisman
    #talisman = world.options.per_talisman
    wing_smash = world.options.infinite_wing
    rules = world.options.rand_rules

    # Convert exploration to rooms
    exp = int((exp * 10) / 0.107)
    # Normalize Total talismans
    #total_location = 405

    #if rules > 0:
    #    total_location = 100

    # Extra locations Enemy 140 / Drops 109
    #if esanity and rules != 1:
    #    total_location += 140
    #if dsanity and rules != 1:
    #    total_location += 107

    # Max 60% of talisman
    #if rules != 1 and int(total_location * 0.6) < tt:
    #    tt = int(total_location * 0.6)

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

    # 285 Castle locations to be randomized
    if rules > 0:
        # Randomize the game items
        weapon_list = ['Shield rod', 'Sword of dawn', 'Basilard', 'Short sword', 'Combat knife', 'Nunchaku',
                       'Were bane', 'Rapier', 'Red rust', 'Takemitsu', 'Shotel', 'Tyrfing', 'Namakura',
                       'Knuckle duster', 'Gladius', 'Scimitar', 'Cutlass', 'Saber', 'Falchion', 'Broadsword',
                       'Bekatowa', 'Damascus sword', 'Hunter sword', 'Estoc', 'Bastard sword', 'Jewel knuckles',
                       'Claymore', 'Talwar', 'Katana', 'Flamberge', 'Iron fist', 'Zwei hander', 'Sword of hador',
                       'Luminus', 'Harper', 'Obsidian sword', 'Gram', 'Jewel sword', 'Mormegil', 'Firebrand',
                       'Thunderbrand', 'Icebrand', 'Stone sword', 'Holy sword', 'Terminus est', 'Marsil',
                       'Dark blade', 'Heaven sword', 'Fist of tulkas', 'Gurthang', 'Mourneblade', 'Alucard sword',
                       'Mablung sword', 'Badelaire', 'Sword familiar', 'Great sword', 'Mace', 'Morningstar',
                       'Holy rod', 'Star flail', 'Moon rod', 'Chakram', 'Holbein dagger', 'Blue knuckles',
                       'Osafune katana', 'Masamune', 'Muramasa', 'Runesword', 'Vorpal blade', 'Crissaegrim',
                       'Yasutsuna', 'Alucart sword']
        shield_list = ['Leather shield', 'Knight shield', 'Iron shield', 'AxeLord shield', 'Herald shield',
                       'Dark shield', 'Goddess shield', 'Shaman shield', 'Medusa shield', 'Skull shield',
                       'Fire shield', 'Alucard shield', 'Alucart shield']
        helmet_list = ['Sunglasses', 'Ballroom mask', 'Bandanna', 'Felt hat', 'Velvet hat', 'Goggles', 'Leather hat',
                       'Steel helm', 'Stone mask', 'Circlet', 'Gold circlet', 'Ruby circlet', 'Opal circlet',
                       'Topaz circlet', 'Beryl circlet', 'Cat-eye circl.', 'Coral circlet', 'Dragon helm',
                       'Silver crown', 'Wizard hat']
        armor_list = ['Cloth tunic', 'Hide cuirass', 'Bronze cuirass', 'Iron cuirass', 'Steel cuirass', 'Silver plate',
                      'Gold plate', 'Platinum mail', 'Diamond plate', 'Fire mail', 'Lightning mail', 'Ice mail',
                      'Mirror cuirass', 'Alucard mail', 'Dark armor', 'Healing mail', 'Holy mail', 'Walk armor',
                      'Brilliant mail', 'Mojo mail', 'Fury plate', 'Dracula tunic', "God's Garb", 'Axe Lord armor',
                      'Alucart mail']
        cloak_list = ['Cloth cape', 'Reverse cloak', 'Elven cloak', 'Crystal cloak', 'Royal cloak', 'Blood cloak',
                      "Joseph's cloak", 'Twilight cloak']
        accessory_list = ['Moonstone', 'Sunstone', 'Bloodstone', 'Staurolite', 'Ring of pales', 'Lapis lazuli',
                          'Ring of ares', 'Ring of varda', 'Ring of arcana', 'Mystic pendant', 'Heart broach',
                          'Necklace of j', 'Gauntlet', 'Ankh of life', 'Ring of feanor', 'Medal', 'Talisman',
                          'Duplicator', "King's stone", 'Covenant stone', 'Nauglamir', 'Secret boots']
        salable_list = ['Aquamarine', 'Diamond', 'Zircon', 'Turquoise', 'Onyx', 'Garnet', 'Opal']
        usable_list = ['Monster vial 1', 'Monster vial 2', 'Monster vial 3', 'Karma coin', 'Magic missile', 'Orange',
                       'Apple', 'Banana', 'Grapes', 'Strawberry', 'Pineapple', 'Peanuts', 'Toadstool', 'Shiitake',
                       'Cheesecake', 'Shortcake', 'Tart', 'Parfait', 'Pudding', 'Ice cream', 'Frankfurter', 'Hamburger',
                       'Pizza', 'Cheese', 'Ham and eggs', 'Omelette', 'Morning set', 'Lunch A', 'Lunch B', 'Curry rice',
                       'Gyros plate', 'Spaghetti', 'Grape juice', 'Barley tea', 'Green tea', 'Natou', 'Ramen',
                       'Miso soup', 'Sushi', 'Pork bun', 'Red bean bun', 'Chinese bun', 'Dim sum set', 'Pot roast',
                       'Sirloin', 'Turkey', 'Meal ticket', 'Neutron bomb', 'Power of sire', 'Pentagram',
                       'Bat pentagram', 'Shuriken', 'Cross shuriken', 'Buffalo star', 'Flame star', 'TNT',
                       'Bwaka knife', 'Boomerang', 'Javelin', 'Fire boomerang', 'Iron ball', 'Dynamite',
                       'Heart refresh', 'Antivenom', 'Uncurse', 'Life apple', 'Hammer', 'Str. potion', 'Luck potion',
                       'Smart potion', 'Attack potion', 'Shield potion', 'Resist fire', 'Resist thunder', 'Resist ice',
                       'Resist stone', 'Resist holy', 'Resist dark', 'Potion', 'High potion', 'Elixir', 'Manna prism',
                       'Library card']
        total_locations = 285
        added_item = 0
        items_to_add = []

        if goal >= 4:
            accessory_list.remove("Talisman")

        if len(world.not_added_items) > 0:
            for item in world.not_added_items:
                items_to_add += [item]
                added_item += 1

        world.random.shuffle(weapon_list)
        world.random.shuffle(shield_list)
        world.random.shuffle(helmet_list)
        world.random.shuffle(armor_list)
        world.random.shuffle(cloak_list)
        world.random.shuffle(accessory_list)
        world.random.shuffle(salable_list)
        world.random.shuffle(usable_list)

        if difficult == 0:
            items_to_add += [create_item("Life Vessel") for _ in range(40)]
            items_to_add += [create_item("Heart Vessel") for _ in range(40)]
            added_item += 80
            remove_offset = 0
        elif difficult == 1:
            items_to_add += [create_item("Life Vessel") for _ in range(32)]
            items_to_add += [create_item("Heart Vessel") for _ in range(33)]
            added_item += 65
            remove_offset = 20
        elif difficult == 2:
            items_to_add += [create_item("Life Vessel") for _ in range(17)]
            items_to_add += [create_item("Heart Vessel") for _ in range(17)]
            added_item += 34
            remove_offset = 100
        else:
            remove_offset = 200

        remaining = total_locations - added_item - remove_offset

        weapon_num = int(remaining * 0.1254)
        shield_num = int(remaining * 0.0237)
        helmet_num = int(remaining * 0.0372)
        armor_num = int(remaining * 0.0576)
        cloak_num = int(remaining * 0.0169)
        acce_num = int(remaining * 0.0338)
        salable_num = int(remaining * 0.1084)
        usab_num = int(remaining * 0.5966)

        for _ in range(weapon_num + 1):
            if weapon_list:
                item = weapon_list.pop()
                items_to_add += [create_item(item)]
                added_item += 1

        for _ in range(shield_num + 1):
            if shield_list:
                item = shield_list.pop()
                items_to_add += [create_item(item)]
                added_item += 1

        for _ in range(helmet_num + 1):
            if helmet_list:
                item = helmet_list.pop()
                items_to_add += [create_item(item)]
                added_item += 1

        for _ in range(armor_num + 1):
            if armor_list:
                item = armor_list.pop()
                items_to_add += [create_item(item)]
                added_item += 1

        for _ in range(cloak_num + 1):
            if cloak_list:
                item = cloak_list.pop()
                items_to_add += [create_item(item)]
                added_item += 1

        for _ in range(acce_num + 1):
            if accessory_list:
                item = accessory_list.pop()
                items_to_add += [create_item(item)]
                added_item += 1

        for _ in range(salable_num + 1):
            if salable_list and remaining > 0:
                item = world.random.choice(salable_list)
                items_to_add += [create_item(item)]
                added_item += 1

        for _ in range(usab_num + 1):
            if usable_list:
                item = world.random.choice(usable_list)
                items_to_add += [create_item(item)]
                added_item += 1

        junk_list = ["Orange", "Apple", "Banana", "Grapes", "Strawberry", "Pineapple", "Peanuts", "Toadstool"]
        items_to_add += [create_item(world.random.choice(junk_list)) for _ in range(total_locations - added_item)]

        world.random.shuffle(items_to_add)
        pu_backup = []
        for i, (k, v) in enumerate(castle_table.items()):
            if k in limited_locations:
                continue

            if len(pu_backup) > 0:
                item = pu_backup.pop()
            else:
                item = items_to_add.pop()
            item_data = item_table[item.name]
            loc_data = location_table[k]

            # Locations goes from 0 to 404
            if loc_data.no_offset:
                while item_data.type == IType.POWERUP:
                    if len(pu_backup) > 404 - i:
                        # We have leftover vessels for 'no offset locations'
                        print(f"Warning: No item left to place at {k} replacing with Monster vial 1 {pu_backup} / {i}")
                        item_data = item_table["Monster vial 1"]
                        break
                    pu_backup += [item]
                    item = items_to_add.pop()
                    item_data = item_table[item.name]
                for address in loc_data.rom_address:
                    write_short(patched_rom, address, item_data.get_item_id_no_offset())
            else:
                for address in loc_data.rom_address:
                    write_short(patched_rom, address, item_data.get_item_id())

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
    # write_char(patched_rom, 0x04f85ae3, bosses)
    # Write exploration need it on index -3 of RNO0
    # write_short(patched_rom, 0x04f85ae1, exp)
    """
    The instruction that check relics of Vlad is jnz r2, 801c1790 we gonna change to je r0, r0 so it's always 
    branch. ROM is @ 0x4fcf7b4 and RAM is @ 0x801c132c
    """
    if goal == 3 or goal == 5:
        write_word(patched_rom, 0x04fcf7b4, 0x10000118)

    if songs:
        randomize_music(patched_rom)

    if shop:
        randomize_shop(patched_rom, shop_prog, shop_lib, goal)

    if prices != 0 and prices <= 3:
        randomize_prices(patched_rom, prices)

    randomize_candles(patched_rom, candles, candles_prog, goal)

    xp_mod, mon_atk, mon_hp = 1, 1, 1
    if difficult == 0:
        xp_mod = 1.5
        mon_atk = 0.7
        mon_hp = 0.7
    elif difficult == 2:
        xp_mod = 0.8
        mon_atk = 1.3
        mon_hp = 1.3
    elif difficult == 3:
        xp_mod = 0.5
        mon_atk = 1.5
        mon_hp = 2
    if player_xp != 0:
        xp_mod = player_xp / 100
    if player_att != 0:
        mon_atk = player_att / 100
    if player_hp != 0:
        mon_hp = player_hp / 100

    # Replace talisman from Bone Musket on talisman farm mode and rng_drops off for a Magic missile
    if 4 <= goal <= 5 and drops == 0:
        enemy = Enemy_dict["Bone musket"]
        write_short(patched_rom, enemy.drop_addresses[0], item_value(25, 1))

    randomize_enemy(patched_rom, drops, drops_prog, xp_mod, mon_atk, mon_hp, goal)

    sanity = 0

    if esanity and rules != 1:
        sanity |= (1 << 0)
    if dsanity and rules != 1:
        sanity |= (1 << 1)
    if wing_smash:
        sanity |= (1 << 2)

    player_name = world.multiworld.get_player_name(world.player)
    player_num = world.player

    seed_num = world.multiworld.seed_name
    tt = world.total_talisman
    talisman = world.required_talisman
    write_seed(patched_rom, seed_num, player_num, player_name, sanity, bonus_luck, goal, bosses, exp, tt, talisman)

    music_slice = original_rom[0x000affd0:0x000b9ea5]
    music_patched = patched_rom[0x000affd0:0x000b9ea5]

    original_slice = music_slice + original_rom[0x04389c6c:0x06a868a4]
    patched_slice = music_patched + patched_rom[0x04389c6c:0x06a868a4]

    print("Generating patch. Please wait!")

    patch = bsdiff4.diff(bytes(original_slice), bytes(patched_slice))

    patch_path = os.path.join(output_directory, f"{world.multiworld.get_out_file_name_base(world.player)}.apsotn")

    with open(patch_path, 'wb') as outfile:
        outfile.write(patch)


def write_seed(buffer, seed, player_number, player_name, sanity_options, bonus_luck, goal, bosses, exp, tt,
               talisman) -> None:
    byte = 0
    start_address = 0x0438d47c
    seed_text = []

    # Seed number occupies 10 bytes total line have 22 + 0xFF 0x00 at end
    for i, num in enumerate(str(seed)):
        if i % 2 != 0:
            byte = (byte | int(num))
            seed_text.append(byte)
            byte = 0
        else:
            byte = (int(num) << 4)

    seed_text.append(player_number)
    seed_text.append(sanity_options)
    hex_luck = int(bonus_luck).to_bytes(2, "little")
    for b in hex_luck:
        seed_text.append(b)

    seed_text.append(goal)
    seed_text.append(bosses)
    seed_text.append(exp)
    seed_text.append(tt)
    seed_text.append(talisman)
    # Still 3 bytes on this 1st maria meeting text

    options_len = len(seed_text)
    for _ in range(options_len, 22):
        seed_text.append(0x00)

    seed_text.append(0xFF)
    seed_text.append(0x00)

    for b in seed_text:
        write_char(buffer, start_address, b)
        start_address += 1

    utf_name = player_name.encode("utf8")
    sizes = [30, 30, 20]
    first_line = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0x00]
    second_line = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0x00]
    third_line = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0xFF, 0x00]
    # Name MAX SIZE is 16 chars = 64 bytes
    char_count = 0
    line_count = 0
    for c in utf_name:
        if char_count == sizes[line_count]:
            line_count += 1
            char_count = 0

        if line_count == 0:
            first_line[char_count] = c
        elif line_count == 1:
            second_line[char_count] = c
        elif line_count == 2:
            third_line[char_count] = c

        char_count += 1

    # Write a CR+LF 0d 0a
    if char_count == sizes[line_count]:
        line_count += 1
        char_count = 0

    if line_count == 0:
        first_line[char_count] = 0x0d
        first_line[char_count + 1] = 0x0a
    elif line_count == 1:
        second_line[char_count] = 0x0d
        second_line[char_count + 1] = 0x0a
    elif line_count == 2:
        third_line[char_count] = 0x0d
        third_line[char_count + 1] = 0x0a

    # Write to file
    start_address = 0x438d494
    for b in first_line:
        write_char(buffer, start_address, b)
        start_address += 1

    start_address = 0x438d4b4
    for b in second_line:
        write_char(buffer, start_address, b)
        start_address += 1

    start_address = 0x438d4d4
    for b in third_line:
        write_char(buffer, start_address, b)
        start_address += 1


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


def randomize_shop(buffer, prog, lib, goal):
    forbid_items = [169, 183, 195, 203, 217, 226, 241, 242]

    if prog:
        forbid_items = [169, 195, 217, 226]

    if goal >= 4:
        forbid_items.append(252)

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


def randomize_candles(buffer, rng_choice, prog, goal):
    if rng_choice == 0:
        return

    forbid_items = [169, 183, 195, 203, 217, 226, 241, 242]

    if prog:
        forbid_items = [169, 195, 217, 226]

    if goal >= 4:
        forbid_items.append(252)

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


def randomize_enemy(buffer, rng_choice, prog, xp_mod, mon_atk, mon_hp, goal):
    forbid_items = [169, 183, 195, 203, 217, 226, 241, 242]

    if prog:
        forbid_items = [169, 195, 217, 226]

    if goal >= 4:
        forbid_items.append(252)

    rng_item = 0
    rng_type = 0

    for drop in Global_drop:
        if rng_choice == 1:
            if drop.vanilla_drop in ["Heart", "Big heart"]:
                rng_item = random.choice([0, 1])
            elif drop.vanilla_drop in ["$1", "$25", "$50", "$100", "$250", "$400", "$1000", "$2000"]:
                rng_item = random.choice([2, 3, 4, 5, 6, 7, 9, 10])
            elif drop.vanilla_drop in hand_type_table:
                rng_item = random.randrange(1, 169)
                rng_type = 1
            else:
                print(f"DEBUG: Item {drop} not found")

            item_id = item_value(rng_item, rng_type)
            for address in drop.drop_addresses:
                write_short(buffer, address, item_id)
        elif rng_choice == 2:
            rng_type = random.randrange(0, 2)

            if rng_type == 0:
                rng_item = random.choice([i for i in range(2, 12) if i not in [8]])
            elif rng_type == 1:
                rng_item = random.choice([i for i in range(1, 259) if i not in forbid_items])

            item_id = item_value(rng_item, rng_type)
            for address in drop.drop_addresses:
                write_short(buffer, address, item_id)

    for k, v in Enemy_dict.items():
        if k in ["Stone skull", "Slime", "Large slime", "Poltergeist", "Puppet sword", "Shield", "Spear", "Ball"]:
            continue
        # Monster data
        # XP
        cur_value = int.from_bytes(buffer[v.drop_addresses[0] - 2:v.drop_addresses[0]], byteorder='little')
        new_value = int(xp_mod * cur_value)
        new_value = clamp(new_value, 1, 65535)
        write_short(buffer, v.drop_addresses[0] - 2, new_value)
        # Monster attack
        cur_value = int.from_bytes(buffer[v.drop_addresses[0] - 20:v.drop_addresses[0] - 18], byteorder='little')
        new_value = int(mon_atk * cur_value)
        new_value = clamp(new_value, 1, 65535)
        if k != "Galamoth":
            write_short(buffer, v.drop_addresses[0] - 20, new_value)
        # Moster HP
        cur_value = int.from_bytes(buffer[v.drop_addresses[0] - 22:v.drop_addresses[0] - 20], byteorder='little')
        new_value = int(mon_hp * cur_value)
        new_value = clamp(new_value, 1, 65535)
        if k != "Galamoth":
            write_short(buffer, v.drop_addresses[0] - 22, new_value)
        for i, drop in enumerate(v.vanilla_drop):
            if rng_choice == 1:
                if drop == "Axe":
                    continue

                if drop in ["$1", "$25", "$50", "$100", "$250", "$400", "$1000", "$2000"]:
                    rng_item = random.choice([2, 3, 4, 5, 6, 7, 9, 10])
                elif drop in hand_type_table:
                    rng_item = random.randrange(1, 169)
                    rng_type = 1
                elif drop in chest_type_table:
                    chest_table = [x for x in range(170, 195) if x not in forbid_items]
                    chest_table.append(258)
                    rng_item = random.choice(chest_table)
                    rng_type = 1
                elif drop in helmet_type_table:
                    rng_item = random.choice([i for i in range(196, 217) if i not in forbid_items])
                    rng_type = 1
                elif drop in cloak_type_table:
                    rng_item = random.choice([i for i in range(218, 226) if i not in forbid_items])
                    rng_type = 1
                elif drop in acc_type_table:
                    rng_item = random.choice([i for i in range(227, 258) if i not in forbid_items])
                    rng_type = 1
                else:
                    print(f"DEBUG: Item {drop} not found")

                item_id = item_value(rng_item, rng_type)
                write_short(buffer, v.drop_addresses[i], item_id)
                if k == "Blue venus weed":
                    write_short(buffer, v.drop_addresses[i+2], item_id)
            if rng_choice == 2:
                if drop == "Axe":
                    continue

                rng_type = random.randrange(0, 2)

                if rng_type == 0:
                    rng_item = random.choice([i for i in range(2, 12) if i not in [8]])
                else:
                    rng_item = random.choice([i for i in range(1, 259) if i not in forbid_items])

                item_id = item_value(rng_item, rng_type)
                write_short(buffer, v.drop_addresses[i], item_id)


def item_value(rng_item: int, rng_type: int) -> int:
    item_id = rng_item
    if rng_item >= tile_id_offset:
        item_id += tile_id_offset
    else:
        if rng_type == 1:
            item_id += tile_id_offset
    return item_id


def create_item(name: str) -> Item:
    data = item_table[name]
    return SotnItem(name, data.ic, data.index, 0
                    )


# def clamp(n, minn, maxn): return max(min(maxn, n), minn) ????
def clamp(n, minn, maxn):
    if n <= minn:
        return minn
    elif n > maxn:
        return maxn
    else:
        return n
