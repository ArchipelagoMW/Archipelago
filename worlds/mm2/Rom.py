from typing import Optional
import hashlib
import Utils
import os
from BaseClasses import MultiWorld

MM2LCHASH = ""


class RomData:
    def __init__(self, file, name=None):
        self.file = bytearray()
        self.read_from_file(file)
        self.name = name

    def read_byte(self, offset):
        return self.file[offset]

    def read_bytes(self, offset, length):
        return self.file[offset:offset + length]

    def write_byte(self, offset, value):
        self.file[offset] = value

    def write_bytes(self, offset, values):
        self.file[offset:offset + len(values)] = values

    def write_to_file(self, file):
        with open(file, 'wb') as outfile:
            outfile.write(self.file)

    def read_from_file(self, file):
        with open(file, 'rb') as stream:
            self.file = bytearray(stream.read())


def patch_rom(multiworld: MultiWorld, player: int, rom: RomData):
    rom.write_byte(0x3403C, 0x8A)  # Read for setting robot master face tiles
    rom.write_byte(0x34083, 0x8A)  # Read for setting robot master face sprites
    rom.write_bytes(0x340DD, [0x9B, 0xC9, 0x07])   # Dr. Wily checking for Items
    rom.write_byte(0x340ED, 0x8A)   # Check for allowing access to stage
    rom.write_bytes(0x3806C, [0xFC, 0x85, 0x8A])  # placeholder, replace first with starting robot master
    rom.write_bytes(0x38076, [0xA9, 0x00])  # Block auto-Wily
    rom.write_bytes(0x3C264, [0xA9, 0x00])  # Block auto-Wily
    rom.write_bytes(0x3C24D, [0x8B, 0x85, 0x8B])  # Write stage completion to $8B


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes: Optional[bytes] = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name: str = get_base_rom_path(file_name)
        base_rom_bytes = bytes(open(file_name, "rb").read())

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in {MM2LCHASH}:
            raise Exception("Supplied Base Rom does not match known MD5 for US LC release. "
                            "Get the correct game and version, then dump it")
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options: Utils.OptionsType = Utils.get_options()
    if not file_name:
        file_name = options["mm2_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name