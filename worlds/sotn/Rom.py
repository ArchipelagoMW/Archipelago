import json
import struct
import math
import sys

import logging
from sys import platform
from typing import TYPE_CHECKING, List
from Utils import home_path, open_filename, messagebox
from settings import get_settings
from worlds.AutoWorld import World
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension
from BaseClasses import Item, ItemClassification
from .Items import tile_id_offset, relic_id_to_name, items, relic_table
from .Locations import locations, LOCATION_TO_ABREV
from .data.Constants import RELIC_NAMES, SLOT, slots, equip_id_offset, equip_inv_id_offset, CURRENT_VERSION, EXTENSIONS
from .data.Zones import zones, ZONE
import hashlib
import os
import subprocess

if TYPE_CHECKING:
    from . import SotnWorld

USHASH = "acbb3a2e4a8f865f363dc06df147afa2"
AUDIOHASH = "8f4b1df20c0173f7c2e6a30bd3109ac8"
logger = logging.getLogger("Client")


# Thanks lil David from AP discord for the info on APProcedurePatch
class SotnProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Symphony of the Night"
    hash = USHASH
    patch_file_ending = ".apsotn"
    result_file_ending = ".cue"

    procedure = [
        ("apply_tokens", ["token_data.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_settings().sotn_settings.rom_file, "rb") as infile:
            return bytes(infile.read())

    def patch(self, target: str) -> None:
        error_message = ""
        try:
            options = json.loads(self.get_file("options.json"))
            gen_version = options["version"]
            if gen_version != CURRENT_VERSION:
                error_message = f"Version mismatch. Gen: {gen_version} - Cur: {CURRENT_VERSION}"
        except KeyError:
            error_message = f"Could not find version on option.json! Generated version too old?"
        except:
            error_message = "Something went really wrong!!!"

        if len(error_message):
            messagebox("Error", error_message, error=True)
            sys.exit()

        file_name = target[:-4]
        if os.path.exists(file_name + ".bin") and os.path.exists(file_name + ".cue"):
            logger.info("Patched ROM + CUE already exist!")
            audio_name = target[0:target.rfind('/') + 1]
            audio_name += "Castlevania - Symphony of the Night (USA) (Track 2).bin"
            if os.path.exists(audio_name):
                logger.info("Track 2 already exist")
            else:
                logger.info("Copying track 2")
                audio_rom = bytearray(get_base_rom_bytes(audio=True))
                with open(audio_name, "wb") as stream:
                    stream.write(audio_rom)
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


class SotnPatchExtension(APPatchExtension):
    game = "Symphony of the Night"


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
    # Always have Clear Game Status. - MottZilla
    patch.write_token(APTokenTypes.WRITE, 0x04397122, struct.pack("<B", 0x22))


def rom_offset(zone: dict, address: int) -> int:
    return zone["pos"] + address + math.floor(address / 0x800) * 0x130


def item_slots(item: dict) -> list:
    if item["type"] in ["WEAPON1", "WEAPON2", "SHIELD", "USABLE"]:
        return [slots[SLOT["LEFT_HAND"]], slots[SLOT["RIGHT_HAND"]]]
    elif item["type"] == "HELMET":
        return [slots[SLOT["HEAD"]]]
    elif item["type"] == "ARMOR":
        return [slots[SLOT["BODY"]]]
    elif item["type"] == "CLOAK":
        return [slots[SLOT["CLOAK"]]]
    elif item["type"] == "ACCESSORY":
        return [slots[SLOT["OTHER"]], slots[SLOT["OTHER2"]]]


def shop_item_type(item: dict) -> int:
    if item["type"] == "HELMET":
        return 0x01
    elif item["type"] == "ARMOR":
        return 0x02
    elif item["type"] == "CLOAK":
        return 0x03
    elif item["type"] == "ACCESSORY":
        return 0x04
    else:
        return 0x00


def tile_value(item: dict, tile: dict) -> int:
    item_id = item["id"]

    if "no_offset" in tile:
        return item_id

    if "shop" in tile:
        if item["type"] in ["HELMET", "ARMOR", "CLOAK", "ACCESSORY"]:
            item_id += equip_id_offset
    else:
        if item["type"] == "RELIC":
            item_id -= 300
        elif item["type"] == "POWERUP":
            item_id -= 400
        elif item["type"] not in ["HEART", "GOLD", "SUBWEAPON"]:
            item_id += tile_id_offset

    return item_id


def write_entity(entity: dict, opts: dict, patch: SotnProcedurePatch) -> None:
    for index, e in enumerate(entity["entities"]):
        zone = zones[entity["zones"][index >> 1]]
        if "x" in opts:
            address = rom_offset(zone, e + 0x00)
            patch.write_token(APTokenTypes.WRITE, address, opts["x"].to_bytes(2, "little"))
        if "y" in opts:
            address = rom_offset(zone, e + 0x02)
            patch.write_token(APTokenTypes.WRITE, address, opts["y"].to_bytes(2, "little"))
        if "id" in opts:
            address = rom_offset(zone, e + 0x04)
            patch.write_token(APTokenTypes.WRITE, address, opts["id"].to_bytes(2, "little"))
        if "slots" in opts:
            address = rom_offset(zone, e + 0x06)
            patch.write_token(APTokenTypes.WRITE, address, opts["slots"][index].to_bytes(2, "little"))
        if "state" in opts:
            address = rom_offset(zone, e + 0x08)
            patch.write_token(APTokenTypes.WRITE, address, opts["state"].to_bytes(2, "little"))


def write_tile_id(zones_list: list, index: int, item_id: int, patch: SotnProcedurePatch) -> None:
    for z in zones_list:
        zone = zones[z]
        addr = rom_offset(zone, zone["items"] + 0x02 * index)
        patch.write_token(APTokenTypes.WRITE, addr, item_id.to_bytes(2, "little"))


def replace_holy_glasses_with_relic(instructions: list, relic: int, patch: SotnProcedurePatch):
    zone = zones[ZONE["CEN"]]
    # Erase Holy glasses
    patch.write_token(APTokenTypes.WRITE,
                      instructions[0]["addresses"][0],
                      instructions[0]["instruction"].to_bytes(4, "little"))
    # Replace entity with relic
    for addr in [0x1328, 0x13be]:
        offset = rom_offset(zone, addr + 0x00)
        patch.write_token(APTokenTypes.WRITE, offset, (0x0180).to_bytes(2, "little"))
        offset = rom_offset(zone, addr + 0x02)
        patch.write_token(APTokenTypes.WRITE, offset, (0x022c).to_bytes(2, "little"))
        offset = rom_offset(zone, addr + 0x04)
        patch.write_token(APTokenTypes.WRITE, offset, (0x000b).to_bytes(2, "little"))
        offset = rom_offset(zone, addr + 0x06)
        patch.write_token(APTokenTypes.WRITE, offset, (0x0000).to_bytes(2, "little"))
        offset = rom_offset(zone, addr + 0x08)
        patch.write_token(APTokenTypes.WRITE, offset, relic.to_bytes(2, "little"))


def replace_shop_relic_with_relic(jewel_address: int, relic_id: int, patch: SotnProcedurePatch):
    relic_name_address = 0x047d5650
    relic_id_address = 0x047dbde0
    relic_id_offset = 0x64
    # Write relic id
    patch.write_token(APTokenTypes.WRITE,
                      jewel_address,
                      struct.pack("<B", relic_id))
    # Fix shop menu check
    patch.write_token(APTokenTypes.WRITE,
                      relic_id_address,
                      struct.pack("<B", (relic_id + relic_id_offset)))
    # Change shop menu name
    relic_name = relic_id_to_name[relic_id + 300]
    ord_string = [0 for _ in range(16)]
    for i in range(16):
        if i < len(relic_name):
            if ord(relic_name[i]) == ' ':
                ord_string[i] = ord(' ')
            else:
                ord_string[i] = ord(relic_name[i]) - 0x20
        elif i == len(relic_name):
            ord_string[i] = 0xff
        else:
            ord_string[i] = 0x00

    ord_string[len(relic_name) + 0] = 0xff
    ord_string[len(relic_name) + 1] = 0x00

    for ch in ord_string:
        patch.write_token(APTokenTypes.WRITE, relic_name_address, struct.pack("<B", ch))
        relic_name_address += 1


def replace_shop_relic_with_item(item: dict, patch: SotnProcedurePatch):
    item_id = item["id"]
    zone = zones[ZONE["LIB"]]
    i_slots = item_slots(item)
    # Write item type
    i_type = shop_item_type(item)
    patch.write_token(APTokenTypes.WRITE, rom_offset(zone, 0x134c), struct.pack("<B", i_type))
    # Write item id
    i_tile = tile_value(item, {"shop": True})
    patch.write_token(APTokenTypes.WRITE, rom_offset(zone, 0x134e), i_tile.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, rom_offset(zone, 0x14d4), i_tile.to_bytes(2, "little"))
    # Write short item type
    offset = rom_offset(zone, 0x032b80)
    patch.write_token(APTokenTypes.WRITE, offset, (0x96220000).to_bytes(4, "little"))  # lhu v0, 0x0000 (s1)
    # Load byte item type
    offset = rom_offset(zone, 0x033050)
    patch.write_token(APTokenTypes.WRITE, offset, (0x90a30000).to_bytes(4, "little"))  # lbu v1, 0x0000 (al)
    offset = rom_offset(zone, 0x033638)
    patch.write_token(APTokenTypes.WRITE, offset, (0x90234364).to_bytes(4, "little"))  # lbu v1, 0x4364 (at)
    offset = rom_offset(zone, 0x03369c)
    patch.write_token(APTokenTypes.WRITE, offset, (0x90224364).to_bytes(4, "little"))  # lbu v0, 0x4364 (at)
    offset = rom_offset(zone, 0x033730)
    patch.write_token(APTokenTypes.WRITE, offset, (0x90234364).to_bytes(4, "little"))  # lbu v1, 0x4364 (at)
    offset = rom_offset(zone, 0x03431c)
    patch.write_token(APTokenTypes.WRITE, offset, (0x92620000).to_bytes(4, "little"))  # lbu v0, 0x0000 (s3)
    offset = rom_offset(zone, 0x0343c0)
    patch.write_token(APTokenTypes.WRITE, offset, (0x92630000).to_bytes(4, "little"))  # lbu v1, 0x0000 (s3)
    offset = rom_offset(zone, 0x034f10)
    patch.write_token(APTokenTypes.WRITE, offset, (0x90430000).to_bytes(4, "little"))  # lbu v1, 0x0000 (v0)
    offset = rom_offset(zone, 0x0359f4)
    patch.write_token(APTokenTypes.WRITE, offset, (0x92a30000).to_bytes(4, "little"))  # lbu v1, 0x0000 (s5)
    # Load relic icon
    offset = rom_offset(zone, 0x034fb4)
    patch.write_token(APTokenTypes.WRITE, offset, (0x00801021).to_bytes(4, "little"))  # addu v0, a0, r0
    # Load relic id for purchase
    offset = rom_offset(zone, 0x033750)
    patch.write_token(APTokenTypes.WRITE, offset, (0x00402021).to_bytes(4, "little"))  # addu a0, v0, r0
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    # Entry point
    offset = rom_offset(zone, 0x032b08)
    patch.write_token(APTokenTypes.WRITE, offset, (0x08075180).to_bytes(4, "little"))  # j 0x801d4600
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    # Equipped check
    offset = rom_offset(zone, 0x054600)
    # ori v1, r0, id
    patch.write_token(APTokenTypes.WRITE, offset, (0x34030000 + item_id + equip_id_offset).to_bytes(4, "little"))
    offset += 4
    for i, slot in enumerate(i_slots):
        # lui v0, 0x8009
        patch.write_token(APTokenTypes.WRITE, offset, (0x3c028000 + (slot >> 16)).to_bytes(4, "little"))
        offset += 4
        # lbu v0, slot (v0)
        patch.write_token(APTokenTypes.WRITE, offset, (0x90420000 + (slot & 0xffff)).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
        offset += 4
        next_slot = 4 + 5 * (len(i_slots) - i - 1)
        # beq v0, v1, pc + next
        patch.write_token(APTokenTypes.WRITE, offset, (0x10430000 + next_slot).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
        offset += 4
    # Inventory check
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c028009).to_bytes(4, "little"))  # lui v0, 0x8009
    offset += 4
    # lbu v0, 0x798a + id (v0)
    patch.write_token(APTokenTypes.WRITE, offset, (0x90420000 + item_id + equip_inv_id_offset).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    # Return
    patch.write_token(APTokenTypes.WRITE, offset, (0x0806cac7).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    # Entry point
    offset = rom_offset(zone, 0x033050)
    patch.write_token(APTokenTypes.WRITE, offset, (0x08075190).to_bytes(4, "little"))  # j 0x801d4640
    # Load base address
    offset = rom_offset(zone, 0x054640)
    patch.write_token(APTokenTypes.WRITE, offset, (0x90a20001).to_bytes(4, "little"))  # lbu v0, 0x0001 (a1)
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x2c4200ff).to_bytes(4, "little"))  # sltiu v0, v0, 0x00ff
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x14400003).to_bytes(4, "little"))  # bne v0, r0, pc + 0x10
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x90a30000).to_bytes(4, "little"))  # lbu v1, 0x0000 (a1)
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34030005).to_bytes(4, "little"))  # ori v1, r0, 0x0005
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x0806cc16).to_bytes(4, "little"))  # j 0x801b3058
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    # Patch checker
    offset = rom_offset(zone, 0x03317c)
    patch.write_token(APTokenTypes.WRITE, offset, (0x080751a0).to_bytes(4, "little"))  # j 0x801d4680
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    # Injection
    offset = rom_offset(zone, 0x054680)
    for i, slot in enumerate(i_slots):
        # lui v0, 0x8009
        patch.write_token(APTokenTypes.WRITE, offset, (0x3c028000 + (slot >> 16)).to_bytes(4, "little"))
        offset += 4
        # lbu v0, slot (v0)
        patch.write_token(APTokenTypes.WRITE, offset, (0x90420000 + (slot & 0xffff)).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
        offset += 4
        next_slot = 5 + 5 * (len(i_slots) - i - 1)
        # beq v0, s3, pc + next
        patch.write_token(APTokenTypes.WRITE, offset, (0x10530000 + next_slot).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
        offset += 4
    # Inventory check
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c028009).to_bytes(4, "little"))  # lui v0, 0x8009
    offset += 4
    # lbu v0, 0x798a + id (v0)
    patch.write_token(APTokenTypes.WRITE, offset, (0x90420000 + item_id + equip_inv_id_offset).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    # Return
    patch.write_token(APTokenTypes.WRITE, offset, (0x10400003).to_bytes(4, "little"))  # beq v0, r0, pc + 0x10
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x0806cc1f).to_bytes(4, "little"))  # j 0x801b307c
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x0806cc69).to_bytes(4, "little"))  # j 0x801b31a4
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    # Entry point
    offset = rom_offset(zone, 0x03431c)
    patch.write_token(APTokenTypes.WRITE, offset, (0x080751c0).to_bytes(4, "little"))  # j 0x801d4700
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    # Quantity check
    offset = rom_offset(zone, 0x054700)
    patch.write_token(APTokenTypes.WRITE, offset, (0x92620001).to_bytes(4, "little"))  # lbu v0, 0x0001 (s3)
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x2c4200ff).to_bytes(4, "little"))  # sltiu v0, v0, 0x00ff
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x14400003).to_bytes(4, "little"))  # bne v0, r0, pc + 0x10
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x0806d0d9).to_bytes(4, "little"))  # j 0x801b4364
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x92620000).to_bytes(4, "little"))  # lbu v0, 0x0000 (s3)
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x0806d0c9).to_bytes(4, "little"))  # j 0x801b4324
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop


def replace_boss_relic_with_item(opts: dict, patch: SotnProcedurePatch) -> None:
    relic = opts["relic"]
    boss = zones[relic["reward"]["zones"]]
    index = relic["index"]
    item = opts["item"]
    zone = zones[relic["zones"][0]]
    slots_list = item_slots(item)
    # Patch item table
    offset = rom_offset(zone, zone["items"] + 0x02 * index)
    item_id = tile_value(item, relic)
    patch.write_token(APTokenTypes.WRITE, offset, item_id.to_bytes(2, "little"))
    # Patch entities table
    for entity in relic["entities"]:
        if "as_item" in relic:
            if "x" in relic["as_item"]:
                offset = rom_offset(zone, entity + 0x00)
                patch.write_token(APTokenTypes.WRITE, offset, relic["as_item"]["x"].to_bytes(2, "little"))
            if "y" in relic["as_item"]:
                offset = rom_offset(zone, entity + 0x02)
                patch.write_token(APTokenTypes.WRITE, offset, relic["as_item"]["y"].to_bytes(2, "little"))
        offset = rom_offset(zone, entity + 0x04)
        patch.write_token(APTokenTypes.WRITE, offset, (0x000c).to_bytes(2, "little"))
        offset = rom_offset(zone, entity + 0x08)
        patch.write_token(APTokenTypes.WRITE, offset, index.to_bytes(2, "little"))
    # Patch instructions that load a relic
    patch.write_token(APTokenTypes.WRITE,
                      relic["erase"]["instructions"][0]["addresses"][0],
                      relic["erase"]["instructions"][0]["instruction"].to_bytes(4, "little"))
    # Patch boss rewards
    offset = rom_offset(boss, boss["rewards"])
    item_id = tile_value(item, relic)
    patch.write_token(APTokenTypes.WRITE, offset, item_id.to_bytes(2, "little"))
    # Entry point
    offset = rom_offset(zone, opts["entry"])
    # j inj
    patch.write_token(APTokenTypes.WRITE, offset, (0x08060000 + (opts["inj"] >> 2)).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00041400).to_bytes(4, "little"))  # sll v0, a0, 10
    # Zero tile function if item is equipped
    offset = rom_offset(zone, opts["inj"])
    # ori t1, r0, id
    patch.write_token(APTokenTypes.WRITE, offset, (0x34090000 + item["id"] + equip_id_offset).to_bytes(4, "little"))
    offset += 4
    for i, slot in enumerate(slots_list):
        # lui t0, 0x8009
        patch.write_token(APTokenTypes.WRITE, offset, (0x3c080000 + (slot >> 16)).to_bytes(4, "little"))
        offset += 4
        # lbu t0, slot (t0)
        patch.write_token(APTokenTypes.WRITE, offset, (0x91080000 + (slot & 0xffff)).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
        offset += 4
        next_slot = 5 + 5 * (len(slots_list) - i - 1)
        # beq t0, t1, pc + next
        patch.write_token(APTokenTypes.WRITE, offset, (0x11090000 + next_slot).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
        offset += 4
    # Inventory check
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c088009).to_bytes(4, "little"))  # lui t0, 0x8009
    offset += 4
    # lbu t0, 0x798a + id (v0)
    patch.write_token(APTokenTypes.WRITE, offset, (0x91080000 + item["id"] + equip_inv_id_offset).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x11000004).to_bytes(4, "little"))  # beq t0, r0, pc + 0x14
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3409000f).to_bytes(4, "little"))  # ori t1 ro, 0x000f
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c088018).to_bytes(4, "little"))  # lui t0, 0x8018
    offset += 4
    for addr in relic["entities"]:
        # sh t1, entity + 4 (t0)
        patch.write_token(APTokenTypes.WRITE, offset, (0xa5090000 + addr + 0x04).to_bytes(4, "little"))
        offset += 4
    # Return
    patch.write_token(APTokenTypes.WRITE, offset, (0x03e00008).to_bytes(4, "little"))  # jr ra
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4


def replace_ring_of_vlad_with_item(opts: dict, patch: SotnProcedurePatch) -> None:
    zone = zones[ZONE["RNZ1"]]
    relic = opts["relic"]
    item = opts["item"]
    item_id = tile_value(item, relic)
    slots_list = item_slots(item)
    # Patch instructions that load a relic
    patch.write_token(APTokenTypes.WRITE,
                      relic["erase"]["instructions"][0]["addresses"][0],
                      relic["erase"]["instructions"][0]["instruction"].to_bytes(4, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x059ee2c8, (0x3402000c).to_bytes(4, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x059ee2d4, (0x24423a54).to_bytes(4, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x059ee2e4, relic["index"].to_bytes(2, "little"))
    offset = rom_offset(zone, 0x2dd6)
    patch.write_token(APTokenTypes.WRITE, offset, relic["index"].to_bytes(2, "little"))
    # Replace item in rewards table
    offset = rom_offset(zone, zone["rewards"])
    patch.write_token(APTokenTypes.WRITE, offset, item_id.to_bytes(2, "little"))
    # Replace item in items table
    offset = rom_offset(zone, zone["items"] + 0x02 * relic["index"])
    patch.write_token(APTokenTypes.WRITE, offset, item_id.to_bytes(2, "little"))
    # Injection point
    offset = rom_offset(zone, 0x02c860)
    patch.write_token(APTokenTypes.WRITE, offset, (0x0806fbb4).to_bytes(4, "little"))  # j 0x801beed0
    offset = rom_offset(zone, 0x02c868)
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    # Get Bat defeat time
    offset = rom_offset(zone, 0x3eed0)
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c020003).to_bytes(4, "little"))  # lui v0, 0x0003
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3442ca78).to_bytes(4, "little"))  # ori v0, v0, 0xca78
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x8c420000).to_bytes(4, "little"))  # lw v0, 0x0000 (v0)
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    # Branch if zero
    patch.write_token(APTokenTypes.WRITE, offset, (0x10400005).to_bytes(4, "little"))  # beq v0, r0, pc + 0x18
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    # Change entity's position and slot
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c088018).to_bytes(4, "little"))  # lui t0, 0x8018
    offset += 4
    # ori t1, r0, y
    patch.write_token(APTokenTypes.WRITE, offset, (0x34090000 + relic["as_item"]["y"]).to_bytes(4, "little"))
    offset += 4
    for addr in relic["entities"]:
        # sh t1, entity + 0x02 (t0)
        patch.write_token(APTokenTypes.WRITE, offset, (0xa5090000 + addr + 0x02).to_bytes(4, "little"))
        offset += 4
    # Zero out tile function pointer if item is in inventory
    # ori v0, r0, id
    patch.write_token(APTokenTypes.WRITE,
                      offset,
                      (0x34020000 + item["id"] + equip_id_offset).to_bytes(4, "little"))
    offset += 4
    for i, slot in enumerate(slots_list):
        # lui s0, 0x8009
        patch.write_token(APTokenTypes.WRITE, offset, (0x3c108000 + (slot >> 16)).to_bytes(4, "little"))
        offset += 4
        # lbu s0, slot (s0)
        patch.write_token(APTokenTypes.WRITE, offset, (0x92100000 + (slot & 0xffff)).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
        offset += 4
        next_slot = 5 + 5 * (len(slots_list) - i - 1)
        # beq s0, v0, pc + next
        patch.write_token(APTokenTypes.WRITE, offset, (0x12020000 + next_slot).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
        offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c108009).to_bytes(4, "little"))  # lui s0, 0x8009
    offset += 4
    # lbu s0, 0x798a + id (s0)
    patch.write_token(APTokenTypes.WRITE,
                      offset,
                      (0x92100000 + item["id"] + equip_inv_id_offset).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x12000002).to_bytes(4, "little"))  # beq s0, r0, pc + 0x0c
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c108007).to_bytes(4, "little"))  # lui s0, 0x8007
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xae0065f0).to_bytes(4, "little"))  # sw r0, 0x65f0 (s0)
    offset += 4
    # return
    patch.write_token(APTokenTypes.WRITE, offset, (0x0806b21a).to_bytes(4, "little"))  # j 0x801ac868
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop


def replace_gold_ring_with_relic(relic_id: int, patch: SotnProcedurePatch) -> None:
    zone = zones[ZONE["NO4"]]
    # Put relic in entity table
    gold_ring = locations["Underground Caverns Succubus Side - Succubus item"]
    for addr in gold_ring["entities"]:
        offset = rom_offset(zone, addr + 8)
        patch.write_token(APTokenTypes.WRITE, offset, relic_id.to_bytes(2, "little"))
    # injection point
    offset = rom_offset(zone, 0x04c590)
    patch.write_token(APTokenTypes.WRITE, offset, (0x08077aed).to_bytes(4, "little"))  # j 0x801debb4
    # Branch
    offset = rom_offset(zone, 0x05ebb4)
    patch.write_token(APTokenTypes.WRITE, offset, (0x10400003).to_bytes(4, "little"))  # beq v0, r0, pc + 0x10
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    # Return
    patch.write_token(APTokenTypes.WRITE, offset, (0x08073166).to_bytes(4, "little"))  # j 0x801cc598
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    # Get Succubus defeat time
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c020003).to_bytes(4, "little"))  # lui v0, 0x0003
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3442ca4c).to_bytes(4, "little"))  # ori v0, v0, 0xca4c
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x8c420000).to_bytes(4, "little"))  # lw v0, 0x0000 (v0)
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    # Branch if zero
    patch.write_token(APTokenTypes.WRITE, offset, (0x10400006).to_bytes(4, "little"))  # beq v0, r0, pc + 0x1c
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    # Patch entity type
    patch.write_token(APTokenTypes.WRITE, offset, (0x3403000b).to_bytes(4, "little"))  # ori v1, r0, 0x000b
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c028018).to_bytes(4, "little"))  # lui v0, 0x8018
    offset += 4
    for addr in gold_ring["entities"]:
        # sh v1, addr + 4 (v0)
        patch.write_token(APTokenTypes.WRITE, offset, (0xa4430000 + addr + 4).to_bytes(4, "little"))
        offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34020000).to_bytes(4, "little"))  # ori v0, r0, 0x0000
    offset += 4
    # Return
    patch.write_token(APTokenTypes.WRITE, offset, (0x0807316f).to_bytes(4, "little"))  # j 0x801cc5bc
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop


def replace_trio_with_relic(relic_id: int, patch: SotnProcedurePatch) -> None:
    trio = locations["Reverse Colosseum - Trio item"]
    # Boss zone patches
    boss = zones[ZONE["RBO0"]]
    # Patch rewards
    offset = rom_offset(boss, boss["rewards"] + 0x02 * trio["reward"]["index"])
    patch.write_token(APTokenTypes.WRITE, offset, relic_id.to_bytes(2, "little"))
    # Remove the condition for writing an item tile
    offset = rom_offset(boss, 0x026088)
    patch.write_token(APTokenTypes.WRITE, offset, (0x34020000).to_bytes(4, "little"))  # ori v0, r0, 0x0000
    # Regular zone patches
    zone = zones[ZONE["RARE"]]
    # Replace entities
    for entity in trio["entities"]:
        addr = rom_offset(zone, entity + 0x04)
        patch.write_token(APTokenTypes.WRITE, addr, (0x000b).to_bytes(2, "little"))
        addr += 2
        patch.write_token(APTokenTypes.WRITE, addr, (0x0010).to_bytes(2, "little"))
        addr += 2
        patch.write_token(APTokenTypes.WRITE, addr, relic_id.to_bytes(2, "little"))


def replace_trio_relic_with_item(opts: dict, patch: SotnProcedurePatch) -> None:
    replace_boss_relic_with_item(opts, patch)

    zone = zones[ZONE["RARE"]]
    trio = opts["relic"]
    for entity in trio["entities"]:
        addr = rom_offset(zone, entity + 0x06)
        patch.write_token(APTokenTypes.WRITE, addr, (0x0010).to_bytes(2, "little"))


def write_tokens(world: "SotnWorld", patch: SotnProcedurePatch):
    apply_acessibility_patches(patch)

    option_names: List[str] = [option_name for option_name in world.options_dataclass.type_hints]
    options_dict = world.options.as_dict(*option_names)

    options_dict["seed"] = int(world.multiworld.seed_name)
    options_dict["player"] = patch.player
    options_dict["player_name"] = patch.player_name

    relics_vlad = ["Heart of vlad", "Tooth of vlad", "Rib of vlad", "Ring of vlad", "Eye of vlad"]
    local_relics = {}

    for loc in world.multiworld.get_locations(world.player):
        if loc.item and loc.item.player == world.player:
            if loc.item.name == "Victory":
                continue
            item_data = items[loc.item.name]
            item_id = tile_value(item_data, {})
            loc_data = locations[loc.name]
            # Save relic locations
            if item_data["type"] == "RELIC":
                local_relics[item_id] = loc_data["ap_id"]

            # Relic locations
            if loc_data["vanilla_item"] in RELIC_NAMES:
                if loc_data["vanilla_item"] == "Jewel of open":
                    jewel_item = item_data["id"]
                    patch.write_token(APTokenTypes.WRITE, 0xf4f3a, jewel_item.to_bytes(2))
                    patch.write_token(APTokenTypes.WRITE, 0x438d6d2, jewel_item.to_bytes(2, "little"))
                # Change relic for a relic
                if item_data["type"] == "RELIC":
                    if loc_data["vanilla_item"] == "Jewel of open":
                        for address in loc_data["addresses"]:
                            replace_shop_relic_with_relic(address, item_id, patch)
                    elif loc_data["vanilla_item"] in ["Bat card", "Skill of wolf"]:
                        for add in loc_data["addresses"]:
                            patch.write_token(APTokenTypes.WRITE, add, item_id.to_bytes(2, "little"))
                    else:
                        write_entity(loc_data, {"state": item_id}, patch)
                        if loc_data["vanilla_item"] in relics_vlad:
                            if loc_data["vanilla_item"] == "Ring of vlad":
                                for address in loc_data["ids"][0]["addresses"]:
                                    patch.write_token(APTokenTypes.WRITE, address, item_id.to_bytes(2, "little"))
                            # Patch Vlad relics boss area
                            else:
                                zone = zones[loc_data["reward"]["zones"]]
                                index = loc_data["reward"]["index"]
                                address = rom_offset(zone, zone["rewards"] + 0x02 * index)
                                patch.write_token(APTokenTypes.WRITE, address, item_id.to_bytes(2, "little"))
                # Change relic for an item
                else:
                    vanilla = loc_data["vanilla_item"]
                    if vanilla == "Jewel of open":
                        replace_shop_relic_with_item(item_data, patch)
                    elif vanilla == "Heart of vlad":
                        opts = {"relic": loc_data, "item": item_data, "entry": 0x034950, "inj": 0x047900}
                        replace_boss_relic_with_item(opts, patch)
                    elif vanilla == "Tooth of vlad":
                        opts = {"relic": loc_data, "item": item_data, "entry": 0x029fc0, "inj": 0x037500}
                        replace_boss_relic_with_item(opts, patch)
                    elif vanilla == "Rib of vlad":
                        opts = {"relic": loc_data, "item": item_data, "entry": 0x037014, "inj": 0x04bf00}
                        replace_boss_relic_with_item(opts, patch)
                    elif vanilla == "Ring of vlad":
                        opts = {"relic": loc_data, "item": item_data}
                        replace_ring_of_vlad_with_item(opts, patch)
                    elif vanilla == "Eye of vlad":
                        opts = {"relic": loc_data, "item": item_data, "entry": 0x01af18, "inj": 0x02a000}
                        replace_boss_relic_with_item(opts, patch)
                    else:
                        as_item = {}
                        if "as_item" in loc_data:
                            as_item = loc_data["as_item"]

                        if "index" in loc_data:
                            write_entity(loc_data, {"id": 0x000c, "state": loc_data["index"]} | as_item, patch)
                            write_tile_id(loc_data["zones"], loc_data["index"], item_id, patch)
                        else:
                            print(f"ERROR on {loc_data}")
            # Item locations
            else:
                if "no_offset" in loc_data:
                    # Relics are forbid on no offset locations
                    if item_data["type"] == "RELIC":
                        as_relic = {}
                        if "as_relic" in loc_data:
                            as_relic = loc_data["as_relic"]
                        write_entity(loc_data, {"id": 0x000b, "state": item_id} | as_relic, patch)
                    elif item_data["type"] == "POWERUP":
                        for add in loc_data["addresses"]:
                            patch.write_token(APTokenTypes.WRITE, add, (0x0000).to_bytes(2, "little"))
                    else:
                        # TODO In the future add traps and boosts
                        new_value = tile_value(item_data, {"no_offset": True})
                        for add in loc_data["addresses"]:
                            patch.write_token(APTokenTypes.WRITE, add, new_value.to_bytes(2, "little"))
                    # Write no offset location on the ROM
                    for address in loc_data["bin_addresses"]:
                        patch.write_token(APTokenTypes.WRITE, address, item_id.to_bytes(2))
                elif loc_data["vanilla_item"] == "Holy glasses":
                    if item_data["type"] == "RELIC":
                        replace_holy_glasses_with_relic(loc_data["erase"]["instructions"], item_id, patch)
                    else:
                        for address in loc_data["addresses"]:
                            # Holy glasses is no-offset item
                            item_id = tile_value(item_data, {"no_offset": True})
                            patch.write_token(APTokenTypes.WRITE, address, item_id.to_bytes(2, "little"))
                elif "trio" in loc_data:
                    opts = {"relic": loc_data, "item": item_data, "entry": 0x026e64, "inj": 0x038a00}
                    if item_data["type"] == "RELIC":
                        replace_trio_with_relic(item_id, patch)
                    else:
                        replace_trio_relic_with_item(opts, patch)
                elif "index" in loc_data:
                    if loc_data["vanilla_item"] == "Gold ring":
                        if item_data["type"] == "RELIC":
                            replace_gold_ring_with_relic(item_id, patch)
                        else:
                            # TODO In the future add traps and boosts
                            for address in loc_data["addresses"]:
                                patch.write_token(APTokenTypes.WRITE, address, item_id.to_bytes(2, "little"))
                    else:
                        # Change item to relic
                        if item_data["type"] == "RELIC":
                            as_relic = {}
                            if "as_relic" in loc_data:
                                as_relic = loc_data["as_relic"]

                            write_entity(loc_data, {"id": 0x000b, "state": item_id} | as_relic, patch)
                        # Change item to item
                        else:
                            write_tile_id(loc_data["zones"], loc_data["index"], item_id, patch)
                else:
                    # Turkey on breakable wall isn't no_offset
                    if loc_data["ap_id"] == 39:
                        for address in loc_data["bin_addresses"]:
                            patch.write_token(APTokenTypes.WRITE, address, item_id.to_bytes(2))
                        if item_data["type"] == "RELIC":
                            as_relic = {}
                            if "as_relic" in loc_data:
                                as_relic = loc_data["as_relic"]
                            write_entity(loc_data, {"id": 0x000b, "state": item_id} | as_relic, patch)
                        else:
                            for address in loc_data["addresses"]:
                                patch.write_token(APTokenTypes.WRITE, address, item_id.to_bytes(2, "little"))
                    else:
                        print(f"ERROR in {loc_data}")
        # Off world items
        elif loc.item and loc.item.player != world.player:
            loc_data = locations[loc.name]
            item_data = items["Secret boots"]
            item_id = tile_value(item_data, {})
            gold_value = 0x04  # 04 -> Yellow bag of gold
            if (loc.item.classification == ItemClassification.progression or
                    loc.item.classification == ItemClassification.progression_skip_balancing):
                gold_value = 0x07  # 07 -> Blue bag of gold
            elif loc.item.classification == ItemClassification.useful:
                gold_value = 0x03  # 03 -> Red bag of gold
            # Relic locations
            if loc_data["vanilla_item"] in RELIC_NAMES:
                vanilla = loc_data["vanilla_item"]
                if vanilla == "Jewel of open":
                    patch.write_token(APTokenTypes.WRITE, 0xf4f3a, (257).to_bytes(2))
                    patch.write_token(APTokenTypes.WRITE, 0x438d6d2, (257).to_bytes(2, "little"))
                    replace_shop_relic_with_item(item_data, patch)
                elif vanilla == "Heart of vlad":
                    opts = {"relic": loc_data, "item": item_data, "entry": 0x034950, "inj": 0x047900}
                    replace_boss_relic_with_item(opts, patch)
                elif vanilla == "Tooth of vlad":
                    opts = {"relic": loc_data, "item": item_data, "entry": 0x029fc0, "inj": 0x037500}
                    replace_boss_relic_with_item(opts, patch)
                elif vanilla == "Rib of vlad":
                    opts = {"relic": loc_data, "item": item_data, "entry": 0x037014, "inj": 0x04bf00}
                    replace_boss_relic_with_item(opts, patch)
                elif vanilla == "Ring of vlad":
                    opts = {"relic": loc_data, "item": item_data}
                    replace_ring_of_vlad_with_item(opts, patch)
                elif vanilla == "Eye of vlad":
                    opts = {"relic": loc_data, "item": item_data, "entry": 0x01af18, "inj": 0x02a000}
                    replace_boss_relic_with_item(opts, patch)
                else:
                    as_item = {}
                    if "as_item" in loc_data:
                        as_item = loc_data["as_item"]

                    if "index" in loc_data:
                        write_entity(loc_data, {"id": 0x000c, "state": loc_data["index"]} | as_item, patch)
                        write_tile_id(loc_data["zones"], loc_data["index"], gold_value, patch)
                    else:
                        print(f"ERROR on {loc_data}")
            # Items locations
            else:
                # 06 -> Green bag of gold
                # 08 -> Purple bag of gold
                # 09 -> Gray bag of gold
                # 0A -> Black bag of gold
                # 0B -> Chest of gold
                if "no_offset" in loc_data:
                    for add in loc_data["addresses"]:
                        patch.write_token(APTokenTypes.WRITE, add, (0x0000).to_bytes(2, "little"))
                elif loc_data["vanilla_item"] == "Holy glasses":
                    # Holy glasses can't be gold bag replace with secret boots
                    for address in loc_data["addresses"]:
                        patch.write_token(APTokenTypes.WRITE, address, item_data.to_bytes(2, "little"))
                elif "trio" in loc_data:
                    opts = {"relic": loc_data, "item": item_data, "entry": 0x026e64, "inj": 0x038a00}
                    replace_trio_relic_with_item(opts, patch)
                elif "index" in loc_data:
                    if loc_data["vanilla_item"] == "Gold ring":
                        for address in loc_data["addresses"]:
                            patch.write_token(APTokenTypes.WRITE, address, gold_value.to_bytes(2, "little"))
                    else:
                        write_tile_id(loc_data["zones"], loc_data["index"], gold_value, patch)
                else:
                    # Turkey on breakable wall isn't no_offset
                    if loc_data["ap_id"] == 39:
                        for address in loc_data["addresses"]:
                            patch.write_token(APTokenTypes.WRITE, address, item_id.to_bytes(2, "little"))
                    else:
                        print(f"ERROR in {loc_data}")

        # Write relic location in time-attack menu
        for r in relic_table.values():
            relic_id = r["id"] - 300
            addresses = [relic_id * 2 + 0xf4f08, relic_id * 2 + 0x438d6a0]

            if 11 <= relic_id <= 17:
                new_relic = relic_id - 11
                addresses = [new_relic * 2 + 0xf4f20, new_relic * 2 + 0x438d6b8]
            elif 18 <= relic_id <= 29:
                new_relic = relic_id - 18
                addresses = [new_relic * 2 + 0xf4f30, new_relic * 2 + 0x438d6c8]

            for address in addresses:
                if relic_id in local_relics:
                    patch.write_token(APTokenTypes.WRITE, address, local_relics[relic_id].to_bytes(2))
                else:
                    patch.write_token(APTokenTypes.WRITE, address, (0xffff).to_bytes(2))

        # Terminate time-attack texts
        # Relics placement
        # Doppleganger10 not need it
        # Olrox 0 bytes remaining
        patch.write_token(APTokenTypes.WRITE, 0xf4f2e, (0xff00).to_bytes(2))
        patch.write_token(APTokenTypes.WRITE, 0x438d6c6, (0xff00).to_bytes(2))
        # Dracula 2 bytes remaining
        patch.write_token(APTokenTypes.WRITE, 0xf4f48, (0xff00).to_bytes(2))
        patch.write_token(APTokenTypes.WRITE, 0x438d6e0, (0xff00).to_bytes(2))
        # No offset placements
        # Minotaur and Werewolf not need it

    # Randomize items
    non_locations = {}
    offset_locations = {}
    vanilla_list = []
    extension = options_dict["extension"]

    for k, v in locations.items():
        loc = LOCATION_TO_ABREV[k]
        if loc not in EXTENSIONS[extension]:
            if "no_offset" in v or v["ap_id"] == 39:
                offset_locations[k] = v
            else:
                non_locations[k] = v
            vanilla_list.append(v["vanilla_item"])

    if world.options.extra_pool.value:
        while len(vanilla_list) and len(world.extra_add):
            vanilla_list.pop(world.random.randrange(len(vanilla_list)))
            vanilla_list.append(world.extra_add.pop(world.random.randrange(len(world.extra_add))))

    # Place no_offset locations first
    while len(offset_locations):
        placed = False
        while not placed:
            item = world.random.choice(vanilla_list)
            if item not in ["Life Vessel", "Heart Vessel"]:
                loc = offset_locations.popitem()
                new_value = tile_value(items[item], {"no_offset": True})
                # Abandoned Mine Demon Side - Item on Breakable Wall is not no_offset
                if loc[1]["ap_id"] == 39:
                    new_value = tile_value(items[item], {})
                for add in loc[1]["addresses"]:
                    patch.write_token(APTokenTypes.WRITE, add, new_value.to_bytes(2, "little"))
                vanilla_list.remove(item)
                placed = True

    # Place non-randomized items
    while len(non_locations):
        loc = non_locations.popitem()
        item = vanilla_list.pop(world.random.randrange(len(vanilla_list)))
        item_id = tile_value(items[item], {})
        write_tile_id(loc[1]["zones"], loc[1]["index"], item_id, patch)

    """
    The flag that get set on NO4 switch: 0x03be1c and the instruction is jz, r2, 80181230 on 0x5430404 we patched
    to jne r0, r0 so it never branch.

    The flag that get set on ARE switch: 0x03be9d and the instruction is jz, r2, 801b6f84 on 0x440110c we patched
    to jne r0, r0 so it never branch.

    The flag that get set on NO2 switch: 0x03be4c and the instruction is jz, r2, 801c1028 on 0x46c0968 we patched
    to jne r0, r0 so it never branch.
    """
    if options_dict["open_no4"]:
        if options_dict["early_open_no4"]:
            patch.write_token(APTokenTypes.WRITE, 0x4ba8798, (0x14000005).to_bytes(4, "little"))
        patch.write_token(APTokenTypes.WRITE, 0x05430404, (0x14000005).to_bytes(4, "little"))

    if options_dict["open_are"]:
        patch.write_token(APTokenTypes.WRITE, 0x0440110c, (0x14000066).to_bytes(4, "little"))

    """
    The instruction that check relics of Vlad is jnz r2, 801c1790 we gonna change to je r0, r0 so it's always 
    branch. ROM is @ 0x4fcf7b4 and RAM is @ 0x801c132c
    """
    #if options_dict["goal"] == 3 or options_dict["goal"] == 5:
    #    patch.write_token(APTokenTypes.WRITE, 0x04fcf7b4, (0x10000118).to_bytes(4, "little"))

    sanity = 0

    player_name = world.multiworld.get_player_name(world.player)
    player_num = world.player

    seed_num = world.multiworld.seed_name

    write_seed(patch, seed_num, player_num, player_name, sanity)

    if options_dict["infinite_wing"]:
        # Wing smash timer
        # Thanks Forat Negre for the info on that
        # @ RAM 1173c8
        patch.write_token(APTokenTypes.WRITE, 0x00134990, (0x00000000).to_bytes(4, "little"))

    options_dict["version"] = CURRENT_VERSION

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


def write_seed(patch: SotnProcedurePatch, seed, player_number, player_name, sanity_options) -> None:
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

    # Still space on 1st maria meeting text

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
    # Player name on meeting with librarian, get holy glasses, meeting with death
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
