import typing
import bsdiff4
import Utils
import hashlib
import os
from pkgutil import get_data

from worlds.AutoWorld import World
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes

HASH_US = '98458530599b9dff8a7414a7f20b777a'
HASH_US_REV_1 = 'd323e6bb4ccc85fd7b416f58350bc1a2'

STARTING_ID = 0xBF0000

class DKC2ProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = [HASH_US, HASH_US_REV_1]
    game = "Donkey Kong Country 2"
    patch_file_ending = ".apdkc2"
    result_file_ending = ".sfc"
    name: bytearray
    procedure = [
        ("apply_tokens", ["token_patch.bin"]),
        ("apply_bsdiff4", ["dkc2_basepatch.bsdiff4"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_byte(self, offset, value):
        self.write_token(APTokenTypes.WRITE, offset, value.to_bytes(1, "little"))

    def write_bytes(self, offset, value: typing.Iterable[int]):
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))


def patch_rom(world: World, patch: DKC2ProcedurePatch):
    # Edit the ROM header
    from Utils import __version__
    patch.name = bytearray(f'DKC2{__version__.replace(".", "")[0:3]}_{world.player}_{world.multiworld.seed:11}\0', 'utf8')[:21]
    patch.name.extend([0] * (21 - len(patch.name)))
    patch.write_bytes(0x7FC0, patch.name)

    patch.write_file("token_patch.bin", patch.get_token_binary())

    
def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in {HASH_US, HASH_US_REV_1}:
            raise Exception('Supplied Base Rom does not match known MD5 for US 1.0 or 1.1 release. '
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options = Utils.get_options()
    if not file_name:
        file_name = options["dkc2_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
