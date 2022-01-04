import Utils
from Patch import read_rom

SMJAP10HASH = '21f3e98df4780ee1c667b84e57d88675'
LTTPJAP10HASH = '03a63945398191337e896e5771f77173'
ROM_PLAYER_LIMIT = 256

import hashlib
import os


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        sm_file_name = get_sm_base_rom_path()
        sm_base_rom_bytes = bytes(read_rom(open(sm_file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(sm_base_rom_bytes)
        if SMJAP10HASH != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for JAP(1.0) release. '
                            'Get the correct game and version, then dump it')
        lttp_file_name = get_lttp_base_rom_path()
        lttp_base_rom_bytes = bytes(read_rom(open(lttp_file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(lttp_base_rom_bytes)
        if LTTPJAP10HASH != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for JAP(1.0) release. '
                            'Get the correct game and version, then dump it')
    
        get_base_rom_bytes.base_rom_bytes = bytes(combine_smz3_rom(sm_base_rom_bytes, lttp_base_rom_bytes))
    return get_base_rom_bytes.base_rom_bytes

def get_sm_base_rom_path(file_name: str = "") -> str:
    options = Utils.get_options()
    if not file_name:
        file_name = options["smz3_options"]["sm_rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.local_path(file_name)
    return file_name

def get_lttp_base_rom_path(file_name: str = "") -> str:
    options = Utils.get_options()
    if not file_name:
        file_name = options["smz3_options"]["lttp_rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.local_path(file_name)
    return file_name

def combine_smz3_rom(sm_rom: bytes, lttp_rom: bytes):
    combined = bytearray(0x600000)
    # SM hi bank
    pos = 0
    srcpos = 0
    for i in range(0x40):
        combined[pos + 0x8000:pos + 0x8000 + 0x8000] = sm_rom[srcpos:srcpos + 0x8000]
        srcpos += 0x8000
        pos += 0x10000

    # SM lo bank
    pos = 0
    for i in range(0x20):
        combined[pos:pos + 0x8000] = sm_rom[srcpos:srcpos + 0x8000]
        srcpos += 0x8000
        pos += 0x10000

    # Z3 hi bank
    pos = 0x400000
    srcpos = 0
    for i in range(0x20):
        combined[pos + 0x8000:pos + 0x8000 + 0x8000] = lttp_rom[srcpos:srcpos + 0x8000]
        srcpos += 0x8000
        pos += 0x10000

    return combined
