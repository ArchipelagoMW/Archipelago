import hashlib
import os

import json
import Utils
from Utils import read_snes_rom
from worlds.Files import APDeltaPatch

SMJUHASH = '21f3e98df4780ee1c667b84e57d88675'
SM_ROM_MAX_PLAYERID = 65535
SM_ROM_PLAYERDATA_COUNT = 202

class SMDeltaPatch(APDeltaPatch):
    hash = SMJUHASH
    game = "Super Metroid"
    patch_file_ending = ".apsm"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if SMJUHASH != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for Japan+US release. '
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options = Utils.get_options()
    if not file_name:
        file_name = options["sm_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name

def get_sm_symbols(sym_json_path) -> dict:
    with open(sym_json_path, "r") as stream:
        symbols = json.load(stream)
        symboltable = {}
        for name, sixdigitaddr in symbols.items():
            (bank, addr_within_bank) = sixdigitaddr.split(":")
            bank = int(bank, 16)
            addr_within_bank = int(addr_within_bank, 16)
            # categorize addresses using snes lorom mapping:
            # (reference: https://en.wikibooks.org/wiki/Super_NES_Programming/SNES_memory_map)
            if (bank >= 0x70 and bank <= 0x7d):
                offset_within_rom_file = None
                # SRAM is not continuous, but callers may want it in continuous terms
                # SRAM @ data bank $70-$7D, addr_within_bank $0000-$7FFF
                #
                # symbol aka snes    offestwithincontinuousSRAM
                # ---------------    --------------------------
                # $70:0000-7FFF   ->  0x0000- 7FFF
                # $71:0000-7FFF   ->  0x8000- FFFF
                # $72:0000-7FFF   -> 0x10000-17FFF
                # etc...
                offset_within_continuous_sram = (bank - 0x70) * 0x8000 + addr_within_bank
                offset_within_wram = None
            elif bank == 0x7e or bank == 0x7f or (bank == 0x00 and addr_within_bank <= 0x1fff):
                offset_within_rom_file = None
                offset_within_continuous_sram = None
                offset_within_wram = addr_within_bank
                if bank == 0x7f:
                    offset_within_wram += 0x10000
            elif bank >= 0x80:
                offset_within_rom_file = ((bank - 0x80) * 0x8000) + (addr_within_bank % 0x8000)
                offset_within_continuous_sram = None
                offset_within_wram = None
            else:
                offset_within_rom_file = None
                offset_within_continuous_sram = None
                offset_within_wram = None
            symboltable[name] = {"bank": bank,
                                 "addr_within_bank": addr_within_bank,
                                 "offset_within_rom_file": offset_within_rom_file,
                                 "offset_within_continuous_sram": offset_within_continuous_sram,
                                 "offset_within_wram": offset_within_wram
                                }
        return symboltable
