import settings
import worlds.Files
import hashlib
import Utils
import os
LADX_HASH = "07c211479386825042efb4ad31bb525f"

class LADXDeltaPatch(worlds.Files.APDeltaPatch):
    hash = LADX_HASH
    game = "Links Awakening DX"
    patch_file_ending = ".apladx"
    result_file_ending: str = ".gbc"

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
        if LADX_HASH != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for USA release. '
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options = settings.get_settings()
    if not file_name:
        file_name = options["ladx_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
