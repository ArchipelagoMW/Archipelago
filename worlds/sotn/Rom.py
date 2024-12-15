import json
import struct

import Utils
import random
import logging
from sys import platform
from typing import TYPE_CHECKING
from worlds.Files import APDeltaPatch
from Utils import home_path, open_filename, messagebox
from settings import get_settings
from worlds.AutoWorld import World
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension
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

if TYPE_CHECKING:
    from . import SotnWorld

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


# Thanks lil David from AP discord for the info on APProcedurePatch
class SotnProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Symphony of the Night"
    hash = USHASH
    patch_file_ending = ".apsotn"
    result_file_ending = ".cue"

    procedure = [
        ("apply_mods", ["options.json"]),
        ("apply_tokens", ["token_data.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_settings().sotn_settings.rom_file, "rb") as infile:
            return bytes(infile.read())

    def patch(self, target: str) -> None:
        file_name = target[:-4]
        if os.path.exists(file_name + ".bin") and os.path.exists(file_name + ".cue"):
            logger.info("Patched ROM + CUE already exist!")
            return

        super().patch(target)

        os.rename(target, target[:-4] + ".bin")

        audio_name = target[0:target.rfind('/') + 1]
        audio_name += "Castlevania - Symphony of the Night (USA) (Track 2).bin"
        if os.path.exists(audio_name):
            logger.info("Track 2 already exist")
        else:
            logger.info("Copying track 2")
            audio_rom = bytearray(get_base_rom_bytes(audio=True))
            with open(audio_name, "wb") as stream:
                stream.write(audio_rom)

        track1_name = target[target.rfind('/') + 1:-4]

        cue_file = f'FILE "{track1_name}.bin" BINARY\n  TRACK 01 MODE2/2352\n\tINDEX 01 00:00:00\n'
        cue_file += f'FILE "Castlevania - Symphony of the Night (USA) (Track 2).bin" BINARY\n  TRACK 02 AUDIO\n'
        cue_file += f'\tINDEX 00 00:00:00\n\tINDEX 01 00:02:00'

        with open(target[:-4] + ".cue", 'wb') as outfile:
            outfile.write(bytes(cue_file, 'utf-8'))

        # Apply Error Recalculation
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
            subprocess.call([error_recalc_path, target[:-4] + ".bin"])
        else:
            messagebox("Error", "Could not find Error_recalc binary", error=True)


class RomData:
    orig_buffer: None
    buffer: bytearray

    def __init__(self, file: bytes) -> None:
        self.file = bytearray(file)

    def write_char(self, address: int, value: int):
        self.file[address] = (value & 0xFF)

    def write_short(self, address: int, value: int):
        x1, x2 = (value & 0xFFFF).to_bytes(2, "little")
        self.file[address] = x1
        self.file[address + 1] = x2

    def read_short(self, address: int) -> int:
        return int.from_bytes(self.file[address:address+2], byteorder="little")

    def get_bytes(self) -> bytes:
        return bytes(self.file)


class SotnPatchExtension(APPatchExtension):
    game = "Symphony of the Night"

    @staticmethod
    def apply_mods(caller: APProcedurePatch, original_rom: bytes, options_file: str) -> bytes:
        rom = RomData(original_rom)
        options = json.loads(caller.get_file(options_file).decode("utf-8"))
        xp_mod, mon_atk, mon_hp, mon_drp = 1, 1, 1, 1
        difficult = options["difficult"]
        if difficult == 0:
            xp_mod = 1.5
            mon_atk = 0.7
            mon_hp = 0.7
            mon_drp = 2
        elif difficult == 2:
            xp_mod = 0.8
            mon_atk = 1.3
            mon_hp = 1.3
            mon_drp = 0
        elif difficult == 3:
            xp_mod = 0.5
            mon_atk = 1.5
            mon_hp = 2
            mon_drp = 0
        if options["xp_mod"] != 0:
            xp_mod = options["xp_mod"] / 100
        if options["att_mod"] != 0:
            mon_atk = options["att_mod"] / 100
        if options["hp_mod"] != 0:
            mon_hp = options["hp_mod"] / 100

        for k, v in Enemy_dict.items():
            if k in ["Stone skull", "Slime", "Large slime", "Poltergeist", "Puppet sword", "Shield", "Spear", "Ball"]:
                continue
            # Monster data
            # XP
            cur_value = rom.read_short(v.drop_addresses[0] - 2)
            new_value = int(xp_mod * cur_value)
            new_value = clamp(new_value, 1, 65535)
            rom.write_short(v.drop_addresses[0] - 2, new_value)
            # Monster attack
            cur_value = rom.read_short(v.drop_addresses[0] - 20)
            new_value = int(mon_atk * cur_value)
            new_value = clamp(new_value, 1, 65535)
            if k != "Galamoth":
                rom.write_short(v.drop_addresses[0] - 20, new_value)
            # Moster HP
            cur_value = rom.read_short(v.drop_addresses[0] - 22)
            new_value = int(mon_hp * cur_value)
            new_value = clamp(new_value, 1, 65535)
            if k != "Galamoth":
                rom.write_short(v.drop_addresses[0] - 22, new_value)

            for i, drop in enumerate(v.vanilla_drop):
                # Drop increase
                if mon_drp != 0:
                    if mon_drp == 1 or mon_drp == 2:
                        rom.write_char(v.drop_addresses[i] + 5, int(mon_drp))
                    else:
                        cur_value = rom.read_short(v.drop_addresses[i] + 4)
                        new_value = int(mon_drp * cur_value)
                        new_value = clamp(new_value, 2, 65535)
                        rom.write_short(v.drop_addresses[i] + 4, new_value)

        return rom.get_bytes()


def apply_acessibility_patches(patch: SotnProcedurePatch):
    # Researched by MottZilla.
    # Patch Clock Room cutscene
    patch.write_token(APTokenTypes.WRITE, 0x0aeaa0, struct.pack("<B", 0x00))
    patch.write_token(APTokenTypes.WRITE, 0x119af4, struct.pack("<B", 0x00))
    # Patch Alchemy Laboratory cutscene
    patch.write_token(APTokenTypes.WRITE, 0x054f0f44 + 2, (0x1000).to_bytes(2, "little"))
    # Power of Sire flashing
    patch.write_token(APTokenTypes.WRITE, 0x00136580, (0x03e00008).to_bytes(4, "little"))
    # Clock Tower puzzle gate
    patch.write_token(APTokenTypes.WRITE, 0x05574dee, struct.pack("<B", 0x80))
    patch.write_token(APTokenTypes.WRITE, 0x055a110c, struct.pack("<B", 0xe0))
    # Olrox death
    patch.write_token(APTokenTypes.WRITE, 0x05fe6914, struct.pack("<B", 0x80))
    # Scylla door
    patch.write_token(APTokenTypes.WRITE, 0x061ce8ec, struct.pack("<B", 0xce))
    patch.write_token(APTokenTypes.WRITE, 0x061cb734, (0x304200fe).to_bytes(4, "little"))
    # Minotaur & Werewolf
    offset = 0x0613a640
    patch.write_token(APTokenTypes.WRITE, 0x061294dc, (0x0806d732).to_bytes(4, "little"))
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c028007).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34423404).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34030005).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x90420000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x1043000b).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34030018).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x10430008).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34030009).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x10430005).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34030019).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x10430002).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x0806d747).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34020001).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xac82002c).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c028007).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x944233da).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x08069bc3).to_bytes(4, "little"))
    # Softlock when using gold & silver ring
    offset = 0x492df64
    patch.write_token(APTokenTypes.WRITE, offset, (0xa0202ee8).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x080735cc).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x4952454, (0x0806b647).to_bytes(4, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x4952474, (0x0806b647).to_bytes(4, "little"))


def write_tokens(world: "SotnWorld", patch: SotnProcedurePatch):
    apply_acessibility_patches(patch)

    options_dict = {
        "difficult": world.options.difficult.value,
        "xp_mod": world.options.xp_mod.value,
        "att_mod": world.options.att_mod.value,
        "hp_mod": world.options.hp_mod.value,
        "drop_mod": world.options.drop_mod.value,
        "opened_no4": world.options.opened_no4.value,
        "opened_are": world.options.opened_are.value,
        "opened_no2": world.options.opened_no2.value,
        "goal": world.options.goal.value,
        "num_talisman": world.options.num_talisman.value,
        "per_talisman": world.options.per_talisman.value,
        "bosses_need": world.options.bosses_need.value,
        "rng_songs": world.options.rng_songs.value,
        "rng_shop": world.options.rng_shop.value,
        "prog_shop": world.options.prog_shop.value,
        "lib_shop": world.options.lib_shop.value,
        "rng_prices": world.options.rng_prices.value,
        "exp_need": world.options.exp_need.value,
        "rng_candles": world.options.rng_candles.value,
        "prog_candles": world.options.prog_candles.value,
        "rng_drops": world.options.rng_drops.value,
        "prog_drops": world.options.prog_drops.value,
        "enemysanity": world.options.enemysanity.value,
        "dropsanity": world.options.dropsanity.value,
        "boostqty": world.options.boostqty.value,
        "boostweight": world.options.boostweight.value,
        "trapqty": world.options.trapqty.value,
        "trapweight": world.options.trapweight.value,
        "rand_rules": world.options.rand_rules.value,
        "infinite_wing": world.options.infinite_wing.value,
        "auto_heal": world.options.auto_heal.value,
        "multiple_trap": world.options.multiple_trap.value,
        "extra_pool": world.options.extra_pool.value,
        "seed": int(world.multiworld.seed_name),
        "player": patch.player,
        "player_name": patch.player_name,
    }

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
                            patch.write_token(APTokenTypes.WRITE, address, (0x0000).to_bytes(2, "little"))
                        else:
                            patch.write_token(APTokenTypes.WRITE,
                                              address,
                                              (item_data.get_item_id_no_offset()).to_bytes(2, "little"))
                    else:
                        if loc_data.can_be_relic:
                            if item_data.type == IType.RELIC:
                                patch.write_token(APTokenTypes.WRITE,
                                                  address,
                                                  (item_data.get_item_id()).to_bytes(2, "little"))
                                if loc.name == "Jewel of Open":
                                    replace_shop_text(patch, loc.item.name)
                                    # Fix shop menu check
                                    patch.write_token(APTokenTypes.WRITE,
                                                      0x047dbde0,
                                                      struct.pack("<B", item_data.get_item_id() + 0x64))
                            else:
                                # Skill of wolf, bat card can't be item. Replace with ghost card instead
                                if loc.name == "Skill of Wolf" or loc.name == "Bat Card":
                                    patch.write_token(APTokenTypes.WRITE, address, (0x0013).to_bytes(2, "little"))
                                elif loc.name == "Jewel of Open":
                                    replace_shop_text(patch, "Ghost Card")
                                    patch.write_token(APTokenTypes.WRITE, address, (0x0013).to_bytes(2, "little"))
                                    patch.write_token(APTokenTypes.WRITE,0x047dbde0, struct.pack("<B",  0x77))
                                elif loc.name in relics_vlad:
                                    patch.write_token(APTokenTypes.WRITE, address, (0x0013).to_bytes(2, "little"))
                                else:
                                    patch.write_token(APTokenTypes.WRITE,
                                                      address,
                                                      loc_data.relic_index.to_bytes(2, "little"))
                                    patch.write_token(APTokenTypes.WRITE, address - 4, (0x000c).to_bytes(2, "little"))
                                    for a in loc_data.item_address:
                                        if loc.item.name == "Life Vessel":
                                            patch.write_token(APTokenTypes.WRITE, a, (0x0017).to_bytes(2, "little"))
                                        elif loc.item.name == "Heart Vessel":
                                            patch.write_token(APTokenTypes.WRITE, a, (0x000c).to_bytes(2, "little"))
                                        else:
                                            patch.write_token(APTokenTypes.WRITE, a,
                                                              item_data.get_item_id().to_bytes(2, "little"))
                        else:
                            if item_data.type == IType.RELIC:
                                patch.write_token(APTokenTypes.WRITE, address, (0x0007).to_bytes(2, "little"))
                            else:
                                patch.write_token(APTokenTypes.WRITE, address,
                                                  item_data.get_item_id().to_bytes(2, "little"))
        elif loc.item and loc.item.player != world.player:
            loc_data = location_table[loc.name]
            if loc_data.rom_address:
                for address in loc_data.rom_address:
                    if loc_data.no_offset:
                        patch.write_token(APTokenTypes.WRITE, address, (0x0000).to_bytes(2, "little"))
                    else:
                        if loc_data.can_be_relic:
                            if loc.name == "Skill of Wolf" or loc.name == "Bat Card":
                                patch.write_token(APTokenTypes.WRITE, address, (0x0013).to_bytes(2, "little"))
                            elif loc.name == "Jewel of Open":
                                patch.write_token(APTokenTypes.WRITE, address, (0x0013).to_bytes(2, "little"))
                                replace_shop_text(patch, "Ghost Card")
                                patch.write_token(APTokenTypes.WRITE, 0x047dbde0, struct.pack("<B", 0x77))
                            elif loc.name in relics_vlad:
                                patch.write_token(APTokenTypes.WRITE, address, (0x0013).to_bytes(2, "little"))
                            else:
                                patch.write_token(APTokenTypes.WRITE, address, loc_data.relic_index.to_bytes(2, "little"))
                                patch.write_token(APTokenTypes.WRITE, address - 4, (0x000c).to_bytes(2, "little"))
                                if (loc.item.classification == ItemClassification.filler or
                                        loc.item.classification == ItemClassification.trap):
                                    for a in loc_data.item_address:
                                        patch.write_token(APTokenTypes.WRITE, a, (0x0004).to_bytes(2, "little"))
                                else:
                                    for a in loc_data.item_address:
                                        patch.write_token(APTokenTypes.WRITE, a, (0x0003).to_bytes(2, "little"))
                        else:
                            if loc.item.classification == ItemClassification.filler:
                                patch.write_token(APTokenTypes.WRITE, address, (0x0004).to_bytes(2, "little"))
                            else:
                                patch.write_token(APTokenTypes.WRITE, address, (0x0003).to_bytes(2, "little"))

    if options_dict["rand_rules"] > 0:
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

        if options_dict["goal"] >= 4:
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

        if options_dict["difficult"] == 0:
            items_to_add += [create_item("Life Vessel") for _ in range(40)]
            items_to_add += [create_item("Heart Vessel") for _ in range(40)]
            added_item += 80
            remove_offset = 0
        elif options_dict["difficult"] == 1:
            items_to_add += [create_item("Life Vessel") for _ in range(32)]
            items_to_add += [create_item("Heart Vessel") for _ in range(33)]
            added_item += 65
            remove_offset = 20
        elif options_dict["difficult"] == 2:
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
                    patch.write_token(APTokenTypes.WRITE, address,
                                      item_data.get_item_id_no_offset().to_bytes(2, "little"))
            else:
                for address in loc_data.rom_address:
                    patch.write_token(APTokenTypes.WRITE, address,
                                      item_data.get_item_id().to_bytes(2, "little"))

    offset = 0x0492df64
    patch.write_token(APTokenTypes.WRITE, offset, (0xa0202ee8).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x080735cc).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x4952454, (0x0806b647).to_bytes(4, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x4952474, (0x0806b647).to_bytes(4, "little"))

    """
    The flag that get set on NO4 switch: 0x03be1c and the instruction is jz, r2, 80181230 on 0x5430404 we patched
    to jne r0, r0 so it never branch.

    The flag that get set on ARE switch: 0x03be9d and the instruction is jz, r2, 801b6f84 on 0x440110c we patched
    to jne r0, r0 so it never branch.

    The flag that get set on NO2 switch: 0x03be4c and the instruction is jz, r2, 801c1028 on 0x46c0968 we patched
    to jne r0, r0 so it never branch.
    """
    #  NO3 and NP3 doesn't share instruction.
    if options_dict["opened_no4"]:
        # Open NO4 too soon, make death skippable. Keep close till visit Alchemy Laboratory
        # write_word(patched_rom, 0x4ba8798, 0x14000005)
        patch.write_token(APTokenTypes.WRITE, 0x05430404, (0x14000005).to_bytes(4, "little"))

    if options_dict["opened_are"]:
        patch.write_token(APTokenTypes.WRITE, 0x0440110c, (0x14000066).to_bytes(4, "little"))

    if options_dict["opened_no2"]:
        patch.write_token(APTokenTypes.WRITE, 0x046c0968, (0x1400000b).to_bytes(4, "little"))

    """
    The instruction that check relics of Vlad is jnz r2, 801c1790 we gonna change to je r0, r0 so it's always 
    branch. ROM is @ 0x4fcf7b4 and RAM is @ 0x801c132c
    """
    if options_dict["goal"] == 3 or options_dict["goal"] == 5:
        patch.write_token(APTokenTypes.WRITE, 0x04fcf7b4, (0x10000118).to_bytes(4, "little"))

    if options_dict["rng_songs"]:
        randomize_music(patch)

    if options_dict["rng_shop"]:
        randomize_shop(patch, options_dict["prog_shop"], options_dict["lib_shop"], options_dict["goal"])

    if options_dict["rng_prices"] != 0 and options_dict["rng_prices"] <= 3:
        randomize_prices(patch, options_dict["rng_prices"])

    randomize_candles(patch, options_dict["rng_candles"], options_dict["prog_candles"], options_dict["goal"])

    # Replace talisman from Bone Musket on talisman farm mode and rng_drops off for a Magic missile
    if 4 <= options_dict["goal"] <= 5 and options_dict["rng_drops"] == 0:
        enemy = Enemy_dict["Bone musket"]
        patch.write_token(APTokenTypes.WRITE, enemy.drop_addresses[0],
                          item_value(25, 1).to_bytes(2, "little"))

    randomize_enemy(patch, options_dict["rng_drops"], options_dict["prog_drops"], options_dict["goal"])

    sanity = 0

    if options_dict["enemysanity"] and options_dict["rand_rules"] != 1:
        sanity |= (1 << 0)
    if options_dict["dropsanity"] and options_dict["rand_rules"] != 1:
        sanity |= (1 << 1)
    if options_dict["infinite_wing"]:
        sanity |= (1 << 2)
    if options_dict["auto_heal"]:
        sanity |= (1 << 3)
    if options_dict["multiple_trap"]:
        sanity |= (1 << 4)

    player_name = world.multiworld.get_player_name(world.player)
    player_num = world.player

    seed_num = world.multiworld.seed_name
    tt = world.total_talisman
    talisman = world.required_talisman
    options_dict["game_tt"] = tt.value
    options_dict["game_reqtt"] = talisman

    write_seed(patch, seed_num, player_num, player_name, sanity, 0xffff, options_dict["goal"],
               options_dict["bosses_need"], options_dict["exp_need"], tt, talisman)

    if options_dict["infinite_wing"]:
        # Wing smash timer
        # Thanks Forat Negre for the info on that
        patch.write_token(APTokenTypes.WRITE, 0x00134990, (0x00000000).to_bytes(4, "little"))

    if options_dict["goal"] >= 4:
        # Talisman farm on, remove item quantity limitation
        patch.write_token(APTokenTypes.WRITE, 0x1171f4, struct.pack("<B", 0xff))

    patch.write_file("options.json", json.dumps(options_dict).encode("utf-8"))
    patch.write_file("token_data.bin", patch.get_token_binary())


def get_base_rom_bytes(audio: bool = False) -> bytes:
    if not audio:
        file_name = get_settings().sotn_settings.rom_file
        with open(file_name, "rb") as infile:
            base_rom_bytes = bytes(infile.read())

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if USHASH != basemd5.hexdigest():
            raise Exception('Supplied Track 1 Base Rom does not match known MD5 for SLU067 release. '
                            'Get the correct game and version, then dump it')
    else:
        file_name = get_settings().sotn_settings.audio_file
        with open(file_name, "rb") as infile:
            base_rom_bytes = bytes(infile.read())

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if AUDIOHASH != basemd5.hexdigest():
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


def replace_shop_text(patch: SotnProcedurePatch, new_text):
    start_address = 0x047d5650

    for c in new_text:
        if c == " ":
            patch.write_token(APTokenTypes.WRITE, start_address, struct.pack("<B", 0x00))
        else:
            patch.write_token(APTokenTypes.WRITE, start_address, struct.pack("<B", ord(c) - 0x20))
        start_address += 1

    patch.write_token(APTokenTypes.WRITE, start_address, struct.pack("<B", 0xff))
    patch.write_token(APTokenTypes.WRITE, start_address + 1, struct.pack("<B", 0x00))


def write_seed(patch: SotnProcedurePatch, seed, player_number, player_name, sanity_options, bonus_luck, goal, bosses, exp, tt,
               talisman) -> None:
    byte = 0
    start_address = 0x0438d47c
    duplicate_offset = 0x4298798
    seed_text = []

    # Seed number occupies 10 bytes total line have 22 + 0xFF 0x00 at end
    # There are 2 unused bytes from bonus luck
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
        patch.write_token(APTokenTypes.WRITE, start_address, struct.pack("<B", b))
        patch.write_token(APTokenTypes.WRITE, start_address - duplicate_offset, struct.pack("<B", b))
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
        patch.write_token(APTokenTypes.WRITE, start_address, struct.pack("<B", b))
        patch.write_token(APTokenTypes.WRITE, start_address - duplicate_offset, struct.pack("<B", b))
        start_address += 1

    start_address = 0x438d4b4
    for b in second_line:
        patch.write_token(APTokenTypes.WRITE, start_address, struct.pack("<B", b))
        patch.write_token(APTokenTypes.WRITE, start_address - duplicate_offset, struct.pack("<B", b))
        start_address += 1

    start_address = 0x438d4d4
    for b in third_line:
        patch.write_token(APTokenTypes.WRITE, start_address, struct.pack("<B", b))
        patch.write_token(APTokenTypes.WRITE, start_address - duplicate_offset, struct.pack("<B", b))
        start_address += 1


def randomize_music(patch: SotnProcedurePatch):
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
            patch.write_token(APTokenTypes.WRITE, address, struct.pack("<B", rng_value))
        music.pop(rng_song)


def randomize_shop(patch: SotnProcedurePatch, prog, lib, goal):
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
        patch.write_token(APTokenTypes.WRITE, value, struct.pack("<B", type_value))
        patch.write_token(APTokenTypes.WRITE, value + 2, (rng_item + offset).to_bytes(2, "little"))


def randomize_prices(patch: SotnProcedurePatch, prices):
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
        patch.write_token(APTokenTypes.WRITE, value + 4, rng_price.to_bytes(4, "little"))


def randomize_candles(patch: SotnProcedurePatch, rng_choice, prog, goal):
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
            patch.write_token(APTokenTypes.WRITE, a, item_id.to_bytes(2, "little"))


def randomize_enemy(patch: SotnProcedurePatch, rng_choice, prog, goal):
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
                patch.write_token(APTokenTypes.WRITE, address, item_id.to_bytes(2, "little"))
        elif rng_choice == 2:
            rng_type = random.randrange(0, 2)

            if rng_type == 0:
                rng_item = random.choice([i for i in range(2, 12) if i not in [8]])
            elif rng_type == 1:
                rng_item = random.choice([i for i in range(1, 259) if i not in forbid_items])

            item_id = item_value(rng_item, rng_type)
            for address in drop.drop_addresses:
                patch.write_token(APTokenTypes.WRITE, address, item_id.to_bytes(2, "little"))

    for k, v in Enemy_dict.items():
        if k in ["Stone skull", "Slime", "Large slime", "Poltergeist", "Puppet sword", "Shield", "Spear", "Ball"]:
            continue

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
                patch.write_token(APTokenTypes.WRITE, v.drop_addresses[i], item_id.to_bytes(2, "little"))
                if k == "Blue venus weed":
                    patch.write_token(APTokenTypes.WRITE, v.drop_addresses[i + 2], item_id.to_bytes(2, "little"))
            if rng_choice == 2:
                if drop == "Axe":
                    continue

                rng_type = random.randrange(0, 2)

                if rng_type == 0:
                    rng_item = random.choice([i for i in range(2, 12) if i not in [8]])
                else:
                    rng_item = random.choice([i for i in range(1, 259) if i not in forbid_items])

                item_id = item_value(rng_item, rng_type)
                patch.write_token(APTokenTypes.WRITE, v.drop_addresses[i], item_id.to_bytes(2, "little"))


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

