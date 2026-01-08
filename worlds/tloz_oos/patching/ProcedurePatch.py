import json
import pkgutil

import yaml

from worlds.Files import APProcedurePatch, APTokenMixin, APPatchExtension
from .Functions import *
from .RomData import RomData
from .data_manager.text import get_text_data
from .text.encoding import write_text_data
from .z80asm.Assembler import Z80Assembler, Z80Block


class OoSPatchExtensions(APPatchExtension):
    game = "The Legend of Zelda - Oracle of Seasons"

    @staticmethod
    def apply_patches(caller: APProcedurePatch, rom: bytes, patch_file: str) -> bytes:
        from .. import OracleOfSeasonsWorld
        rom_data = RomData(rom)
        patch_data = json.loads(caller.get_file(patch_file).decode("utf-8"))

        version = patch_data["version"].split(".")
        world_version = OracleOfSeasonsWorld.world_version
        if int(version[0]) != world_version.major or int(version[1]) > world_version.minor:
            raise Exception(f"Invalid version: this patch was generated on v{patch_data['version']}, "
                            f"you are currently using v{world_version.as_simple_string()}")

        if patch_data["options"]["cross_items"]:
            file_name = get_settings().tloz_oos_options.ages_rom_file
            file_path = Utils.user_path(file_name)
            rom_file = open(file_path, "rb")
            ages_rom = bytes(rom_file.read())
            rom_file.close()

            for bank in range(0x40, 0x80):
                bank = 0xdd  # TODO: this is an invalid instruction that hangs the game, it's easier to debug but looks worse, remove/comment out once stable
                rom_data.add_bank(bank)
            rom_data.update_rom_size()
        else:
            ages_rom = bytes()

        # Initialize random seed with the one used for generation + the player ID, so that cosmetic stuff set
        # to "random" always generate the same for successive patchings for a given slot
        random.seed(patch_data["seed"] + caller.player)

        assembler = Z80Assembler(CAVE_DATA, DEFINES, rom, ages_rom)
        dictionary, texts = get_text_data(rom_data, True)

        # Define assembly constants & floating chunks
        define_location_constants(assembler, patch_data)
        define_option_constants(assembler, patch_data)
        define_season_constants(assembler, patch_data)
        make_text_data(assembler, texts, patch_data)
        define_compass_rooms_table(assembler, patch_data)
        define_collect_properties_table(assembler, patch_data)
        define_additional_tile_replacements(assembler, patch_data)
        define_samasa_combination(assembler, patch_data)
        define_dungeon_items_text_constants(texts, patch_data)
        define_essence_sparkle_constants(assembler, patch_data)
        define_lost_woods_sequences(assembler, texts, patch_data)
        define_tree_sprites(assembler, patch_data)
        set_file_select_text(assembler, caller.player_name)
        set_player_start_inventory(assembler, patch_data)

        # Parse assembler files, compile them and write the result in the ROM
        print("Compiling ASM files...")
        write_text_data(rom_data, dictionary, texts, True)
        for file_path in get_asm_files(patch_data):
            data_loaded = yaml.safe_load(pkgutil.get_data(__name__, file_path))
            for metalabel, contents in data_loaded.items():
                assembler.add_block(Z80Block(metalabel, contents))
        assembler.compile_all()
        for block in assembler.blocks:
            rom_data.write_bytes(block.addr.address_in_rom(), block.byte_array)

        # Perform direct edits on the ROM
        alter_treasure_types(rom_data)
        write_chest_contents(rom_data, patch_data)
        set_old_men_rupee_values(rom_data, patch_data)
        set_dungeon_warps(rom_data, patch_data)
        set_portal_warps(rom_data, patch_data)
        apply_miscellaneous_options(rom_data, patch_data)
        set_fixed_subrosia_seaside_location(rom_data, patch_data)
        if patch_data["options"]["randomize_ai"]:
            randomize_ai_for_april_fools(rom_data, patch_data["seed"] + caller.player)

        # Apply cosmetic settings
        set_heart_beep_interval_from_settings(rom_data)
        set_character_sprite_from_settings(rom_data)
        inject_slot_name(rom_data, caller.player_name)

        rom_data.update_header_checksum()
        rom_data.update_checksum(0x14e)
        return rom_data.output()


class OoSProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = [ROM_HASH]
    patch_file_ending: str = ".apoos"
    result_file_ending: str = ".gbc"

    game = "The Legend of Zelda - Oracle of Seasons"
    procedure = [
        ("apply_patches", ["patch.dat"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        base_rom_bytes = getattr(cls, "base_rom_bytes", None)
        if not base_rom_bytes:
            file_name = get_settings().tloz_oos_options.rom_file
            file_name = Utils.user_path(file_name)

            rom_file = open(file_name, "rb")
            base_rom_bytes = bytes(rom_file.read())
            rom_file.close()

            setattr(cls, "base_rom_bytes", base_rom_bytes)
        return base_rom_bytes
