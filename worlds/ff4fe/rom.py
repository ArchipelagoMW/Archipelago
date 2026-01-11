import argparse
import json
import logging
import os
import pkgutil
import tempfile

from typing import TYPE_CHECKING

import Utils
from settings import get_settings
from worlds.Files import APProcedurePatch, APTokenMixin, APPatchExtension
from .items import all_items

if TYPE_CHECKING:
    from . import FF4FEWorld


ROM_NAME = 0x007FC0
sentinel_addresses = [ # A list of memory addresses that amounts to "are we in a cutscene or battle or menu".
    0xF506B1, 0xF506D9, 0xF50650, 0xF50140, 0xF50685, 0xE070FD
]
inventory_start_location = 0xF51440
inventory_size = 96
checked_reward_locations_start = 0xF51510
checked_reward_size = 16
treasure_found_locations_start = 0xF512A0
treasure_found_size = 64
key_items_tracker_start_location = 0xF51500
key_items_tracker_size = 3
items_received_location_start = 0xE02FFE
items_received_size = 2
victory_byte_location= 0xE070F2

objective_threshold_start_location = 0x21F820
objective_threshold_size = 32
objective_progress_start_location = 0xF51520
objective_progress_size = 32
objective_count_location = 0x10F0FC
objectives_needed_count_location = 0x10F0F9

key_items_found_location = 0xF51578
gp_byte_location = 0xF516A0
gp_byte_size = 3
junk_tier_byte = 0x1FFC00
junked_items_length_byte = 0x1FFC01
junked_items_array_start = 0x1FFD00
kept_items_length_byte = 0x1FFC02
kept_items_array_start = 0x1FFE00

sell_value_byte = 0x00C951

json_doc_length_location = 0x1FF000
json_doc_location = 0x1FF004

generation_version_byte = 0x001FFC10
patch_version_byte = 0x001FFC11

special_flag_key_items = {
    "Hook": (0xF51286, 0b01000000),
    "Darkness Crystal": (0xF5128C, 0b00000001),
    "Earth Crystal": (0xF5128C, 0b00000010),
    "Package": (0xF5128C, 0b00001000),
    "Legend Sword": (0xF5128C, 0b00100000)
}

airship_flyable_flag = (0xF51286, 0b11111011)
drill_attached_flag = (0xF51287, 0b00100000)

def get_base_rom_as_bytes() -> bytes:
    with open(get_settings().ff4fe_options.rom_file, "rb") as infile:
        base_rom_bytes = bytes(Utils.read_snes_rom(infile))
    return base_rom_bytes


class FF4FEPatchExtension(APPatchExtension):
    game = "Final Fantasy IV Free Enterprise"

    @staticmethod
    def call_fe(caller, rom, placement_file):
        from . import FF4FEWorld
        logging.info(f"FF4FE APWorld version v{FF4FEWorld.version} used for patching.")
        placements = json.loads(caller.get_file(placement_file))
        logging.info(f"Patching using data generated on version v{placements["version"]}.")
        seed = placements["seed"]
        output_file = placements["output_file"]
        rom_name = placements["rom_name"]
        flags = placements["flags"]
        junk_tier = placements["junk_tier"]
        junked_items = placements["junked_items"]
        kept_items = placements["kept_items"]
        data_dir = Utils.user_path("data", "ff4fe")
        placements["data_dir"] = data_dir
        placement_string = json.dumps(placements)
        # We try to fetch FE from the data directory in case of patcher updates...
        try:
            logging.info(f"Loading Free Enterprise from {data_dir}")
            import sys
            sys.path.append(data_dir)
            from FreeEnterprise4.FreeEnt.cmd_make import MakeCommand
        except:
            # ...and if it's not there, we grab the installed packaged version
            try:
                logging.info("Loading Free Enterprise from installed packages")
                from FreeEnt.cmd_make import MakeCommand
            except ImportError:
                # Once part of the frozen build, this shouldn't get hit ever, but it's useful for the standalone APWorld.
                raise ImportError("Free Enterprise not found. Try reinstalling it.")
        cmd = MakeCommand()
        parser = argparse.ArgumentParser()
        cmd.add_parser_arguments(parser)
        directory = tempfile.gettempdir()
        with open(os.path.join(directory, "ff4base.sfc"), "wb") as file:
            file.write(rom)
            arguments = [
                os.path.join(directory, "ff4base.sfc"),
                f"-s={seed}",
                f"-f={flags}",
                f"-o={os.path.join(directory, output_file)}",
                f"-a={placement_string}"
            ]
            args = parser.parse_args(arguments)
            cmd.execute(args)
        with open(os.path.join(directory, output_file), "rb") as file:
            rom_data = bytearray(file.read())
            rom_data[ROM_NAME:ROM_NAME+20] = bytes(rom_name, encoding="utf-8")
            rom_data[junk_tier_byte:junk_tier_byte + 1] = bytes([junk_tier])
            rom_data[junked_items_length_byte] = len(junked_items)
            rom_data[kept_items_length_byte] = len(kept_items)
            for i, item_name in enumerate(junked_items):
                item_id = [item for item in all_items if item.name == item_name].pop().fe_id
                rom_data[junked_items_array_start + i] = item_id
            for i, item_name in enumerate(kept_items):
                item_id = [item for item in all_items if item.name == item_name].pop().fe_id
                rom_data[kept_items_array_start + i] = item_id
            rom_data[generation_version_byte] = placements["version"]
            rom_data[patch_version_byte] = FF4FEWorld.version
        return rom_data


class FF4FEProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Final Fantasy IV Free Enterprise"
    hash = "27D02A4F03E172E029C9B82AC3DB79F7"
    patch_file_ending = ".apff4fe"
    result_file_ending = ".sfc"

    procedure = [
        ("call_fe", ["placement_file.json"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()

