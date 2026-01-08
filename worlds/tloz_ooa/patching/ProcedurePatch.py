import hashlib
import os
import pkgutil

import yaml

import Utils
from worlds.Files import APProcedurePatch, APTokenMixin, APPatchExtension

from .Functions import *
from .Constants import *
from .RomData import RomData
from .z80asm.Assembler import Z80Assembler, Z80Block

from tkinter.filedialog import askopenfilename

ROM_HASH = "c4639cc61c049e5a085526bb6cac03bb"


class OoAPatchExtensions(APPatchExtension):
    game = "The Legend of Zelda - Oracle of Ages"

    @staticmethod
    def apply_patches(caller: APProcedurePatch, rom: bytes, patch_file: str) -> bytes:
        rom_data = RomData(rom)
        patch_data = yaml.safe_load(caller.get_file(patch_file).decode("utf-8"))

        if not (patch_data["version"] in RETRO_COMPAT_VERSION):
            raise Exception(f"Invalid version: this seed was generated on v{patch_data['version']}, "
                            f"and is not compatible with current : v{VERSION}")

        #if patch_data["options"]["enforce_potion_in_shop"]:
        #    patch_data["locations"]["Horon Village: Shop #3"] = "Potion"

        assembler = Z80Assembler()

        # Define static values & data blocks
        for i, offset in enumerate(EOB_ADDR):
            assembler.end_of_banks[i] = offset
        for key, value in DEFINES.items():
            assembler.define(key, value)
        for symbolic_name, price in patch_data["shop_prices"].items():
            assembler.define_byte(f"shopPrices.{symbolic_name}", RUPEE_VALUES[price])
        define_location_constants(assembler, patch_data)
        define_option_constants(assembler, patch_data)
        define_text_constants(assembler, patch_data)
        define_dungeon_items_text_constants(assembler, patch_data)

        # Define dynamic data blocks
        define_compass_rooms_table(assembler, patch_data)
        define_collect_properties_table(assembler, patch_data)
        set_file_select_text(assembler, caller.player_name)

        # Parse assembler files, compile them and write the result in the ROM
        print(f"Compiling ASM files...")
        for file_path in get_asm_files(patch_data):
            data_loaded = yaml.safe_load(pkgutil.get_data(__name__, file_path))
            for metalabel, contents in data_loaded.items():
                assembler.add_block(Z80Block(metalabel, contents))
        assembler.compile_all()
        for block in assembler.blocks:
            rom_data.write_bytes(block.addr.full_address(), block.byte_array)

        alter_treasures(rom_data)
        write_chest_contents(rom_data, patch_data)
        write_seed_tree_content(rom_data, patch_data)
        set_dungeon_warps(rom_data, patch_data)
        #apply_miscellaneous_options(rom_data, patch_data)

        set_heart_beep_interval_from_settings(rom_data)
        set_character_sprite_from_settings(rom_data)
        apply_misc_option(rom_data, patch_data)
        inject_slot_name(rom_data, caller.player_name)

        rom_data.update_checksum(0x14e)
        return rom_data.output()

class OoAProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = [ROM_HASH]
    patch_file_ending: str = ".apooa"
    result_file_ending: str = ".gbc"

    game = "The Legend of Zelda - Oracle of Ages"
    procedure = [
        ("apply_patches", ["patch.dat"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        base_rom_bytes = getattr(cls, "base_rom_bytes", None)
        if not base_rom_bytes:
            file_name = get_settings().tloz_ooa_options["rom_file"]
            if not os.path.exists(file_name):
                file_name = Utils.user_path(file_name)
            if not os.path.exists(file_name):
                file_name = askopenfilename() 
            base_rom_bytes = bytes(open(file_name, "rb").read())

            basemd5 = hashlib.md5()
            basemd5.update(base_rom_bytes)
            if ROM_HASH != basemd5.hexdigest():
                raise Exception("Supplied ROM does not match known MD5 for Oracle of Seasons US version."
                                "Get the correct game and version, then dump it.")
            setattr(cls, "base_rom_bytes", base_rom_bytes)
        return base_rom_bytes

