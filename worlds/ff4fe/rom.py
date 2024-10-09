import argparse
import io
import json
import os
import random
import typing

from typing import TYPE_CHECKING, Optional, BinaryIO

import Utils
from BaseClasses import Item, Location
from settings import get_settings
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension
from .FreeEnterpriseForAP.FreeEnt.cmd_make import MakeCommand

if TYPE_CHECKING:
    from . import FF4FEWorld

ROM_NAME = 0x007FC0
sentinel_addresses = [
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
objective_count_location = 0x10F0F9

key_items_found_location = 0xF51578
gp_byte_location = 0xF516A0
gp_byte_size = 3
junk_tier_byte = 0x1FFC00

sell_value_byte = 0x00C951

json_doc_length_location = 0x1FF000
json_doc_location = 0x1FF004

special_flag_key_items = {
    "Hook": (0xF51286, 0b01000000),
    "Darkness Crystal": (0xF5128C, 0b00000001),
    "Earth Crystal": (0xF5128C, 0b00000010),
    "Package": (0xF5128C, 0b00001000),
    "Legend Sword": (0xF5128C, 0b00100000)
}

airship_flyable_flag = (0xF51286, 0b11111011)

def get_base_rom_as_bytes() -> bytes:
    with open(get_settings().ff4fe_options.rom_file, "rb") as infile:
        base_rom_bytes = bytes(Utils.read_snes_rom(infile))
    return base_rom_bytes


class FF4FEPatchExtension(APPatchExtension):
    game = "Final Fantasy IV Free Enterprise"

    @staticmethod
    def call_fe(caller, rom, placement_file):
        placements = json.loads(caller.get_file(placement_file))
        seed = placements["seed"]
        output_file = placements["output_file"]
        rom_name = placements["rom_name"]
        flags = placements["flags"]
        junk_tier = 1
        try:
            junk_tier = placements["junk_tier"]
        except KeyError:
            junk_tier = 1
        placements = json.dumps(json.loads(caller.get_file(placement_file)))
        cmd = MakeCommand()
        parser = argparse.ArgumentParser()
        cmd.add_parser_arguments(parser)
        with open("ff4base.sfc", "wb") as file:
            file.write(rom)
            arguments = [
                "ff4base.sfc",
                f"-s={seed}",
                f"-f={flags}",
                f"-o={output_file}",
                f"-a={placements}"
            ]
            args = parser.parse_args(arguments)
            cmd.execute(args)
        os.unlink("ff4base.sfc")
        with open(output_file, "rb") as file:
            rom_data = bytearray(file.read())
            rom_data[ROM_NAME:ROM_NAME+20] = bytes(rom_name, encoding="utf-8")
            rom_data[junk_tier_byte:junk_tier_byte + 1] = bytes([junk_tier])
        os.unlink(output_file)
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

