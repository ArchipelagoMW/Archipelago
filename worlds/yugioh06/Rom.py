import hashlib
import os

import Utils
from Patch import APDeltaPatch

MD5Europe = '020411d3b08f5639eb8cb878283f84bf'
MD5America = 'b8a7c976b28172995fe9e465d654297a'


class YGO06DeltaPatch(APDeltaPatch):
    game = "Yu-Gi-Oh! 2006"
    hash = MD5America
    patch_file_ending = ".apygo06"
    result_file_ending = ".gba"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        md5hash = basemd5.hexdigest()
        if MD5Europe != md5hash and MD5America != md5hash:
            raise Exception('Supplied Base Rom does not match known MD5 for'
                            'Yu-Gi-Oh! World Championship 2006 America or Europe '
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options = Utils.get_options()
    if not file_name:
        file_name = "Yu-Gi-Oh06.gba"
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
