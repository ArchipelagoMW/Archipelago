import json
import logging
import os
import tempfile
import typing
import Utils
from settings import get_settings
from worlds.Files import APProcedurePatch, APTokenMixin, APPatchExtension
from .data import memory

def get_base_rom_as_bytes() -> bytes:
    with open(get_settings().metroidfusion_options.rom_file, "rb") as infile:
        base_rom_bytes = bytes(Utils.read_snes_rom(infile))
    return base_rom_bytes


class MetroidFusionPatchExtension(APPatchExtension):
    game = "Metroid Fusion"

    @staticmethod
    def call_mars(caller, rom, placement_file):
        from . import MetroidFusionWorld
        patch_dict = json.loads(caller.get_file(placement_file))
        logging.info(f"Metroid Fusion APWorld v{patch_dict.get('GenerationVersion', 0)} was used for generation.")
        logging.info(f"Metroid Fusion APWorld v{MetroidFusionWorld.version} used for patching.")
        from .mars_patcher import patcher
        patcher.validate_patch_data_mf(patch_dict)
        output_file = patch_dict["OutputFile"]
        directory = tempfile.gettempdir()
        with open(os.path.join(directory, "temp.gba"), "wb") as file:
            file.write(rom)
        patcher.patch(
            os.fspath(os.path.join(directory, "temp.gba")),
            os.fspath(os.path.join(directory, output_file)),
            typing.cast("patcher.MarsSchema", patch_dict),
            lambda message, progress: print(f"{message} -- {progress}"),
        )
        with open(os.path.join(directory, output_file), "rb") as file:
            rom_data = bytearray(file.read())
            rom_name_text = patch_dict["RomName"]
            rom_name = bytearray(rom_name_text, 'utf-8')
            rom_name.extend([0] * (20 - len(rom_name)))
            rom_data[memory.rom_name_location:memory.rom_name_location + 20] = bytes(rom_name)
            rom_data[memory.generation_version_location] = patch_dict.get("GenerationVersion", 0)
            rom_data[memory.patching_version_location] = MetroidFusionWorld.version
        return rom_data


class MetroidFusionProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Metroid Fusion"
    hash = "27D02A4F03E172E029C9B82AC3DB79F7"
    patch_file_ending = ".apmetfus"
    result_file_ending = ".gba"

    procedure = [
        ("call_mars", ["patch_file.json"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()

