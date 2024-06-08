import pkgutil
from typing import Optional, TYPE_CHECKING, Iterable, Dict, Sequence
import hashlib
import Utils
import os

import settings
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from . import names
from .rules import minimum_weakness_requirement, bosses

#from .text import MM3TextEntry
#from .color import get_colors_for_item, write_palette_shuffle

if TYPE_CHECKING:
    from . import MM3World

MM3LCHASH = "37f2c36ce7592f1e16b3434b3985c497"
PROTEUSHASH = "9ff045a3ca30018b6e874c749abb3ec4"
MM3NESHASH = "4a53b6f58067d62c9a43404fe835dd5c"
MM3VCHASH = "c50008f1ac86fae8d083232cdd3001a5"

enemy_weakness_ptrs: Dict[int, int] = {
    0: 0x14100,
    1: 0x14200,
    2: 0x14300,
    3: 0x14400,
    4: 0x14500,
    5: 0x14600,
    6: 0x14700,
    7: 0x14800,
    8: 0x14900,
}

enemy_addresses: Dict[str, int] = {
    "Snake Man": 0xD4,
    "Gemini Man": 0xD6,
    "Gemini Man (Clone)": 0xD7, # Capcom why
}

# addresses printed when assembling basepatch
consumables_ptr: int = 0x3F2FE
wily_4_ptr: int = 0x3F3A1
energylink_ptr: int = 0x3F46B


class RomData:
    def __init__(self, file: bytes, name: str = "") -> None:
        self.file = bytearray(file)
        self.name = name

    def read_byte(self, offset: int) -> int:
        return self.file[offset]

    def read_bytes(self, offset: int, length: int) -> bytearray:
        return self.file[offset:offset + length]

    def write_byte(self, offset: int, value: int) -> None:
        self.file[offset] = value

    def write_bytes(self, offset: int, values: Sequence[int]) -> None:
        self.file[offset:offset + len(values)] = values

    def write_to_file(self, file: str) -> None:
        with open(file, 'wb') as outfile:
            outfile.write(self.file)


class MM3ProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = [MM3LCHASH, MM3NESHASH, MM3VCHASH]
    game = "Mega Man 3"
    patch_file_ending = ".apmm3"
    result_file_ending = ".nes"
    name: bytearray
    procedure = [
        ("apply_bsdiff4", ["mm3_basepatch.bsdiff4"]),
        ("apply_tokens", ["token_patch.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_byte(self, offset: int, value: int) -> None:
        self.write_token(APTokenTypes.WRITE, offset, value.to_bytes(1, "little"))

    def write_bytes(self, offset: int, value: Iterable[int]) -> None:
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))


def patch_rom(world: "MM3World", patch: MM3ProcedurePatch) -> None:
    patch.write_file("mm3_basepatch.bsdiff4", pkgutil.get_data(__name__, os.path.join("data", "mm3_basepatch.bsdiff4")))
    # text writing
    #patch.write_bytes(0x37E2A, MM2TextEntry("FOR           ", 0xCB).resolve())
    #patch.write_bytes(0x37EAA, MM2TextEntry("GET EQUIPPED  ", 0x0B).resolve())
    #patch.write_bytes(0x37EBA, MM2TextEntry("WITH          ", 0x2B).resolve())

    base_address = 0x3F650
    color_address = 0x37F6C
    for i, location in zip(range(11), [
        names.get_needle_cannon,
        names.get_magnet_missile,
        names.get_gemini_laser,
        names.get_hard_knuckle,
        names.get_top_spin,
        names.get_search_snake,
        names.get_spark_shot,
        names.get_shadow_blade,
        names.get_rush_marine,
        names.get_rush_jet
    ]):
        continue
        #item = world.multiworld.get_location(location, world.player).item
        #if item:
        #    if len(item.name) <= 14:
        #        # we want to just place it in the center
        #        first_str = ""
        #        second_str = item.name
        #        third_str = ""
        #    elif len(item.name) <= 28:
        #        # spread across second and third
        #        first_str = ""
        #        second_str = item.name[:14]
        #        third_str = item.name[14:]
        #    else:
        #        # all three
        #        first_str = item.name[:14]
        #        second_str = item.name[14:28]
        #        third_str = item.name[28:]
        #        if len(third_str) > 16:
        #            third_str = third_str[:16]
        #    player_str = world.multiworld.get_player_name(item.player)
        #    if len(player_str) > 14:
        #        player_str = player_str[:14]
        #    patch.write_bytes(base_address + (64 * i), MM2TextEntry(first_str, 0x4B).resolve())
        #    patch.write_bytes(base_address + (64 * i) + 16, MM2TextEntry(second_str, 0x6B).resolve())
        #    patch.write_bytes(base_address + (64 * i) + 32, MM2TextEntry(third_str, 0x8B).resolve())
        #    patch.write_bytes(base_address + (64 * i) + 48, MM2TextEntry(player_str, 0xEB).resolve())

        #    colors = get_colors_for_item(item.name)
        #    if i > 7:
        #        patch.write_bytes(color_address + 27 + ((i - 8) * 2), colors)
        #    else:
        #        patch.write_bytes(color_address + (i * 2), colors)

    # write_palette_shuffle(world, patch)

    enemy_weaknesses: Dict[str, Dict[int, int]] = {}

    if world.options.strict_weakness or world.options.random_weakness or world.options.plando_weakness:
        # we need to write boss weaknesses
        output = bytearray()
        pass

    if world.options.enemy_weakness:
        for enemy in enemy_addresses:
            if enemy in bosses:
                continue
            enemy_weaknesses[enemy] = {weapon: world.random.randint(-4, 4) for weapon in enemy_weakness_ptrs}

    for enemy, damage in enemy_weaknesses.items():
        for weapon in enemy_weakness_ptrs:
            if damage[weapon] < 0:
                damage[weapon] = 256 + damage[weapon]
            patch.write_byte(enemy_weakness_ptrs[weapon] + enemy_addresses[enemy], damage[weapon])

    if world.options.consumables != world.options.consumables.option_all:
        pass
        #value_a = 0x7C
        #value_b = 0x76
        #if world.options.consumables == world.options.consumables.option_1up_etank:
        #    value_b = 0x7A
        #else:
        #    value_a = 0x7A
        #patch.write_byte(consumables_ptr - 3, value_a)
        #patch.write_byte(consumables_ptr + 1, value_b)

    #patch.write_byte(wily_4_ptr + 1, world.options.wily_4_requirement.value)

    if world.options.energy_link:
        pass
        #patch.write_byte(energylink_ptr + 1, 1)

    if world.options.reduce_flashing:
        pass

    from Utils import __version__
    patch.name = bytearray(f'MM3{__version__.replace(".", "")[0:3]}_{world.player}_{world.multiworld.seed:11}\0',
                           'utf8')[:21]
    patch.name.extend([0] * (21 - len(patch.name)))
    patch.write_bytes(0x3F300, patch.name)
    deathlink_byte = world.options.death_link.value | (world.options.energy_link.value << 1)
    patch.write_byte(0x3F316, deathlink_byte)

    patch.write_bytes(0x3FF1C, world.world_version)

    version_map = {
        "0": 0x90,
        "1": 0x91,
        "2": 0x92,
        "3": 0x93,
        "4": 0x94,
        "5": 0x95,
        "6": 0x96,
        "7": 0x97,
        "8": 0x98,
        "9": 0x99,
        ".": 0xDC
    }
    #patch.write_token(APTokenTypes.RLE, 0x36EE0, (11, 0))
    #patch.write_token(APTokenTypes.RLE, 0x36EEE, (25, 0))

    # BY SILVRIS
    #patch.write_bytes(0x36EE0, [0xC2, 0xD9, 0xC0, 0xD3, 0xC9, 0xCC, 0xD6, 0xD2, 0xC9, 0xD3])
    # ARCHIPELAGO x.x.x
    #patch.write_bytes(0x36EF2, [0xC1, 0xD2, 0xC3, 0xC8, 0xC9, 0xD0, 0xC5, 0xCC, 0xC1, 0xC7, 0xCF, 0xC0])
    #patch.write_bytes(0x36EFE, list(map(lambda c: version_map[c], __version__)))

    patch.write_file("token_patch.bin", patch.get_token_binary())


header = b"\x4E\x45\x53\x1A\x10\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00"


def read_headerless_nes_rom(rom: bytes) -> bytes:
    if rom[:4] == b"NES\x1A":
        return rom[16:]
    else:
        return rom


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes: Optional[bytes] = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = read_headerless_nes_rom(bytes(open(file_name, "rb").read()))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() == PROTEUSHASH:
            base_rom_bytes = extract_mm3(base_rom_bytes)
            basemd5 = hashlib.md5()
            basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in {MM3LCHASH, MM3NESHASH, MM3VCHASH}:
            print(basemd5.hexdigest())
            raise Exception("Supplied Base Rom does not match known MD5 for US, LC, or US VC release. "
                            "Get the correct game and version, then dump it")
        headered_rom = bytearray(base_rom_bytes)
        headered_rom[0:0] = header
        setattr(get_base_rom_bytes, "base_rom_bytes", bytes(headered_rom))
        return bytes(headered_rom)
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options: settings.Settings = settings.get_settings()
    if not file_name:
        file_name = options["mm2_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


prg_offset = 0xCEDB0
prg_size = 0x40000
chr_offset = 0x10EDB0
chr_size = 0x20000


def extract_mm3(proteus: bytes) -> bytes:
    mm3 = bytearray(proteus[prg_offset:prg_offset + prg_size])
    mm3.extend(proteus[chr_offset:chr_offset + chr_size])
    return bytes(mm3)
