
import Utils
import logging

from BaseClasses import Location
from worlds.Files import APDeltaPatch
from typing import List, Dict, Union, Iterable, Collection, TYPE_CHECKING

import hashlib
import os
import pkgutil

# from .data import patches
# from .text import cvcotm_string_to_bytearray, cvcotm_text_truncate, cvcotm_text_wrap
from .locations import get_location_info
from .options import Countdown
from settings import get_settings

if TYPE_CHECKING:
    from . import CVCotMWorld

CVCOTMUSHASH = "50a1089600603a94e15ecf287f8d5a1f"
ROM_PLAYER_LIMIT = 65535


class LocalRom:
    orig_buffer: None
    buffer: bytearray

    def __init__(self, file: str) -> None:
        self.orig_buffer = None

        with open(file, "rb") as stream:
            self.buffer = bytearray(stream.read())

    def read_bit(self, address: int, bit_number: int) -> bool:
        bitflag = (1 << bit_number)
        return (self.buffer[address] & bitflag) != 0

    def read_byte(self, address: int) -> int:
        return self.buffer[address]

    def read_bytes(self, start_address: int, length: int) -> bytearray:
        return self.buffer[start_address:start_address + length]

    def write_byte(self, address: int, value: int) -> None:
        self.buffer[address] = value

    def write_bytes(self, start_address: int, values: Collection[int]) -> None:
        self.buffer[start_address:start_address + len(values)] = values

    def write_int16(self, address: int, value: int) -> None:
        value = value & 0xFFFF
        self.write_bytes(address, [(value >> 8) & 0xFF, value & 0xFF])

    def write_int16s(self, start_address: int, values: List[int]) -> None:
        for i, value in enumerate(values):
            self.write_int16(start_address + (i * 2), value)

    def write_int24(self, address: int, value: int) -> None:
        value = value & 0xFFFFFF
        self.write_bytes(address, [(value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF])

    def write_int24s(self, start_address: int, values: List[int]) -> None:
        for i, value in enumerate(values):
            self.write_int24(start_address + (i * 3), value)

    def write_int32(self, address, value: int) -> None:
        value = value & 0xFFFFFFFF
        self.write_bytes(address, [(value >> 24) & 0xFF, (value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF])

    def write_int32s(self, start_address: int, values: list) -> None:
        for i, value in enumerate(values):
            self.write_int32(start_address + (i * 4), value)

    def write_to_file(self, filepath: str) -> None:
        with open(filepath, "wb") as outfile:
            outfile.write(self.buffer)

    def apply_ips(self, filename: str) -> None:
        ips_file = bytearray(pkgutil.get_data(__name__, "data/ips/" + filename))

        # Verify that the IPS patch is, indeed, an IPS patch.
        if ips_file[0:5].decode("ascii") != "PATCH":
            logging.error(filename + " does not appear to be an IPS patch...")
            return

        # self.write_bytes(22484, b'\x00I\x08G\x01\x00h\x08')

        file_pos = 5
        while True:
            # Get the ROM offset bytes of the current record.
            rom_offset = int.from_bytes(ips_file[file_pos:file_pos + 3], "big")

            # If we've hit the "EOF" codeword (aka 0x454F46), stop iterating because we've hit the end of the file.
            if rom_offset == 0x454F46:
                return

            # Get the size bytes of the current record.
            bytes_size = int.from_bytes(ips_file[file_pos + 3:file_pos + 5], "big")

            if bytes_size != 0:
                # Write the data to the ROM.
                self.write_bytes(rom_offset, ips_file[file_pos + 5:file_pos + 5 + bytes_size])

                # Increase our position in the IPS patch to the start of the next record.
                file_pos += 5 + bytes_size
            else:
                # If the size is 0, we are looking at an RLE record.
                # Get the size of the RLE.
                rle_size = int.from_bytes(ips_file[file_pos + 5:file_pos + 7], "big")

                # Get the byte to be written over and over.
                rle_byte = ips_file[file_pos + 7:file_pos + 8]

                # Write the RLE byte to the ROM the RLE size times over.
                self.write_bytes(rom_offset, [rle_byte for _ in range(rle_size)])

                # Increase our position in the IPS patch to the start of the next record.
                file_pos += 8


def patch_rom(world: "CVCotMWorld", rom: LocalRom, offset_data: Dict[int, int],
              active_locations: Iterable[Location]) -> None:

    multiworld = world.multiworld
    options = world.options
    player = world.player
    required_last_keys = world.required_last_keys
    total_last_keys = world.total_last_keys

    # These patches get applied regardless of settings.
    rom.apply_ips("AutoDashBoots.ips")
    rom.apply_ips("CardUp_v3_Custom.ips")
    rom.apply_ips("NoDSSDrops.ips")
    rom.apply_ips("CardCombosRevealed.ips")
    rom.apply_ips("CandleFix.ips")
    rom.apply_ips("SoftlockBlockFix.ips")
    rom.apply_ips("MPComboFix.ips")
    rom.apply_ips("GameClearBypass.ips")
    rom.apply_ips("MapEdits.ips")
    rom.apply_ips("DemoForceFirst.ips")
    rom.apply_ips("AllowAlwaysDrop.ips")
    # rom.apply_ips("SeedDisplay.ips")

    if options.auto_run:
        rom.apply_ips("PermanentDash.ips")

    if options.dss_patch:
        rom.apply_ips("DSSGlitchFix.ips")

    if options.break_iron_maidens:
        rom.apply_ips("BrokenMaidens.ips")

    if required_last_keys != 1:
        rom.apply_ips("MultiLastKey.ips")
        rom.write_byte(0x96C1E, required_last_keys)
        rom.write_byte(0xDFB4, required_last_keys)
        rom.write_byte(0xCB84, required_last_keys)

    if options.buff_ranged_familiars:
        rom.apply_ips("BuffFamiliars.ips")

    if options.buff_sub_weapons:
        rom.apply_ips("BuffSubweapons.ips")

    if options.buff_shooter_strength:
        rom.apply_ips("ShooterStrength.ips")

    if options.always_allow_speed_dash:
        rom.apply_ips("AllowSpeedDash.ips")

    if options.countdown:
        rom.apply_ips("Countdown.ips")

    if options.disable_battle_arena_mp_drain:
        rom.apply_ips("NoMPDrain.ips")


class CVCotMDeltaPatch(APDeltaPatch):
    hash = CVCOTMUSHASH
    patch_file_ending: str = ".apcvcotm"
    result_file_ending: str = ".gba"

    game = "Castlevania - Circle of the Moon"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(open(file_name, "rb").read())

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if CVCOTMUSHASH != basemd5.hexdigest():
            raise Exception("Supplied Base Rom does not match known MD5 for Castlevania: Circle of the Moon USA."
                            "Get the correct game and version, then dump it.")
        setattr(get_base_rom_bytes, "base_rom_bytes", base_rom_bytes)
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    if not file_name:
        file_name = get_settings()["cvcotm_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
