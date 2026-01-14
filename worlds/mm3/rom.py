import pkgutil
from typing import TYPE_CHECKING, Iterable
import hashlib
import Utils
import os

from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from . import names
from .rules import bosses

from .text import MM3TextEntry
from .color import get_colors_for_item, write_palette_shuffle
from .options import Consumables

if TYPE_CHECKING:
    from . import MM3World

MM3LCHASH = "5266687de215e790b2008284402f3917"
PROTEUSHASH = "b69fff40212b80c94f19e786d1efbf61"
MM3NESHASH = "4a53b6f58067d62c9a43404fe835dd5c"
MM3VCHASH = "c50008f1ac86fae8d083232cdd3001a5"

enemy_weakness_ptrs: dict[int, int] = {
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

enemy_addresses: dict[str, int] = {
    "Dada": 0x12,
    "Potton": 0x13,
    "New Shotman": 0x15,
    "Hammer Joe": 0x16,
    "Peterchy": 0x17,
    "Bubukan": 0x18,
    "Vault Pole": 0x19,  # Capcom..., why did you name an enemy Pole?
    "Bomb Flier": 0x1A,
    "Yambow": 0x1D,
    "Metall 2": 0x1E,
    "Cannon": 0x22,
    "Jamacy": 0x25,
    "Jamacy 2": 0x26,  # dunno what this is, but I won't question
    "Jamacy 3": 0x27,
    "Jamacy 4": 0x28,  # tf is this Capcom
    "Mag Fly": 0x2A,
    "Egg": 0x2D,
    "Gyoraibo 2": 0x2E,
    "Junk Golem": 0x2F,
    "Pickelman Bull": 0x30,
    "Nitron": 0x35,
    "Pole": 0x37,
    "Gyoraibo": 0x38,
    "Hari Harry": 0x3A,
    "Penpen Maker": 0x3B,
    "Returning Monking": 0x3C,
    "Have 'Su' Bee": 0x3E,
    "Hive": 0x3F,
    "Bolton-Nutton": 0x40,
    "Walking Bomb": 0x44,
    "Elec'n": 0x45,
    "Mechakkero": 0x47,
    "Chibee": 0x4B,
    "Swimming Penpen": 0x4D,
    "Top": 0x52,
    "Penpen": 0x56,
    "Komasaburo": 0x57,
    "Parasyu": 0x59,
    "Hologran (Static)": 0x5A,
    "Hologran (Moving)": 0x5B,
    "Bomber Pepe": 0x5C,
    "Metall DX": 0x5D,
    "Petit Snakey": 0x5E,
    "Proto Man": 0x62,
    "Break Man": 0x63,
    "Metall": 0x7D,
    "Giant Springer": 0x83,
    "Springer Missile": 0x85,
    "Big Snakey": 0x99,
    "Tama": 0x9A,
    "Doc Robot (Flash)": 0xB0,
    "Doc Robot (Wood)": 0xB1,
    "Doc Robot (Crash)": 0xB2,
    "Doc Robot (Metal)": 0xB3,
    "Doc Robot (Bubble)": 0xC0,
    "Doc Robot (Heat)": 0xC1,
    "Doc Robot (Quick)": 0xC2,
    "Doc Robot (Air)": 0xC3,
    "Snake": 0xCA,
    "Needle Man": 0xD0,
    "Magnet Man": 0xD1,
    "Top Man": 0xD2,
    "Shadow Man": 0xD3,
    "Top Man's Top": 0xD5,
    "Shadow Man (Sliding)": 0xD8,  # Capcom I swear
    "Hard Man": 0xE0,
    "Spark Man": 0xE2,
    "Snake Man": 0xE4,
    "Gemini Man": 0xE6,
    "Gemini Man (Clone)": 0xE7,  # Capcom why
    "Yellow Devil MK-II": 0xF1,
    "Wily Machine 3": 0xF3,
    "Gamma": 0xF8,
    "Kamegoro": 0x101,
    "Kamegoro Shell": 0x102,
    "Holograph Mega Man": 0x105,
    "Giant Metall": 0x10C,  # This is technically FC but we're +16 from the rom header
}

# addresses printed when assembling basepatch
wily_4_ptr: int = 0x7F570
consumables_ptr: int = 0x7FDEA
energylink_ptr: int = 0x7FDF9


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

    base_address = 0x3C000
    color_address = 0x31BC7
    for i, offset, location in zip([0, 8, 1, 2,
                                    3, 4, 5, 6,
                                    7, 9],
                                   [0x10, 0x50, 0x91, 0xD2,
                                    0x113, 0x154, 0x195, 0x1D6,
                                    0x217, 0x257],
                                   [
                                       names.get_needle_cannon,
                                       names.get_rush_jet,
                                       names.get_magnet_missile,
                                       names.get_gemini_laser,
                                       names.get_hard_knuckle,
                                       names.get_top_spin,
                                       names.get_search_snake,
                                       names.get_spark_shock,
                                       names.get_shadow_blade,
                                       names.get_rush_marine,
                                   ]):
        item = world.get_location(location).item
        if item:
            if len(item.name) <= 13:
                # we want to just place it in the center
                first_str = ""
                second_str = item.name
                third_str = ""
            elif len(item.name) <= 26:
                # spread across second and third
                first_str = ""
                second_str = item.name[:13]
                third_str = item.name[13:]
            else:
                # all three
                first_str = item.name[:13]
                second_str = item.name[13:26]
                third_str = item.name[26:]
                if len(third_str) > 13:
                    third_str = third_str[:13]
            player_str = world.multiworld.get_player_name(item.player)
            if len(player_str) > 13:
                player_str = player_str[:13]
            y_coords = 0xA5
            row = 0x21
            if location in [names.get_rush_marine, names.get_rush_jet]:
                y_coords = 0x45
                row = 0x22
            patch.write_bytes(base_address + offset, MM3TextEntry(first_str, y_coords, row).resolve())
            patch.write_bytes(base_address + 16 + offset, MM3TextEntry(second_str, y_coords + 0x20, row).resolve())
            patch.write_bytes(base_address + 32 + offset, MM3TextEntry(third_str, y_coords + 0x40, row).resolve())
            if y_coords + 0x60 > 0xFF:
                row += 1
                y_coords = 0x01
                patch.write_bytes(base_address + 48 + offset, MM3TextEntry(player_str, y_coords, row).resolve())
                colors_high, colors_low = get_colors_for_item(item.name)
                patch.write_bytes(color_address + (i * 8) + 1, colors_high)
                patch.write_bytes(color_address + (i * 8) + 5, colors_low)
            else:
                patch.write_bytes(base_address + 48 + offset, MM3TextEntry(player_str, y_coords + 0x60, row).resolve())

    write_palette_shuffle(world, patch)

    enemy_weaknesses: dict[str, dict[int, int]] = {}

    if world.options.strict_weakness or world.options.random_weakness or world.options.plando_weakness:
        # we need to write boss weaknesses
        for boss in bosses:
            if boss == "Kamegoro Maker":
                enemy_weaknesses["Kamegoro"] = {i: world.weapon_damage[i][bosses[boss]] for i in world.weapon_damage}
                enemy_weaknesses["Kamegoro Shell"] = {i: world.weapon_damage[i][bosses[boss]]
                                                      for i in world.weapon_damage}
            elif boss == "Gemini Man":
                enemy_weaknesses[boss] = {i: world.weapon_damage[i][bosses[boss]] for i in world.weapon_damage}
                enemy_weaknesses["Gemini Man (Clone)"] = {i: world.weapon_damage[i][bosses[boss]]
                                                          for i in world.weapon_damage}
            elif boss == "Shadow Man":
                enemy_weaknesses[boss] = {i: world.weapon_damage[i][bosses[boss]] for i in world.weapon_damage}
                enemy_weaknesses["Shadow Man (Sliding)"] = {i: world.weapon_damage[i][bosses[boss]]
                                                            for i in world.weapon_damage}
            else:
                enemy_weaknesses[boss] = {i: world.weapon_damage[i][bosses[boss]] for i in world.weapon_damage}

    if world.options.enemy_weakness:
        for enemy in enemy_addresses:
            if enemy in [*bosses.keys(), "Kamegoro", "Kamegoro Shell", "Gemini Man (Clone)", "Shadow Man (Sliding)"]:
                continue
            enemy_weaknesses[enemy] = {weapon: world.random.randint(-4, 4) for weapon in enemy_weakness_ptrs}
            if enemy in ["Tama", "Giant Snakey", "Proto Man", "Giant Metall"] and enemy_weaknesses[enemy][0] <= 0:
                enemy_weaknesses[enemy][0] = 1
            elif enemy == "Jamacy 2":
                # bruh
                if not enemy_weaknesses[enemy][8] > 0:
                    enemy_weaknesses[enemy][8] = 1
                if not enemy_weaknesses[enemy][3] > 0:
                    enemy_weaknesses[enemy][3] = 1

    for enemy, damage in enemy_weaknesses.items():
        for weapon in enemy_weakness_ptrs:
            if damage[weapon] < 0:
                damage[weapon] = 256 + damage[weapon]
            patch.write_byte(enemy_weakness_ptrs[weapon] + enemy_addresses[enemy], damage[weapon])

    if world.options.consumables != Consumables.option_all:
        value_a = 0x64
        value_b = 0x6A
        if world.options.consumables in (Consumables.option_none, Consumables.option_1up_etank):
            value_a = 0x68
        if world.options.consumables in (Consumables.option_none, Consumables.option_weapon_health):
            value_b = 0x67
        patch.write_byte(consumables_ptr - 3, value_a)
        patch.write_byte(consumables_ptr + 1, value_b)

    patch.write_byte(wily_4_ptr + 1, world.options.wily_4_requirement.value)

    patch.write_byte(energylink_ptr + 1, world.options.energy_link.value)

    if world.options.reduce_flashing:
        # Spark Man
        patch.write_byte(0x12649, 8)
        patch.write_byte(0x1264E, 8)
        patch.write_byte(0x12653, 8)
        # Shadow Man
        patch.write_byte(0x12658, 0x10)
        # Gemini Man
        patch.write_byte(0x12637, 0x20)
        patch.write_byte(0x1263D, 0x20)
        patch.write_byte(0x12643, 0x20)
        # Gamma
        patch.write_byte(0x7DA4A, 0xF)

    if world.options.music_shuffle:
        if world.options.music_shuffle.current_key == "no_music":
            pool = [0xF0] * 18
        elif world.options.music_shuffle.current_key == "randomized":
            pool = world.random.choices(range(1, 0xC), k=18)
        else:
            pool = [1, 2, 3, 4, 5, 6, 7, 8, 1, 3, 7, 8, 9, 9, 10, 10, 11, 11]
        world.random.shuffle(pool)
        patch.write_bytes(0x7CD1C, pool)

    from Utils import __version__
    patch.name = bytearray(f'MM3{__version__.replace(".", "")[0:3]}_{world.player}_{world.multiworld.seed:11}\0',
                           'utf8')[:21]
    patch.name.extend([0] * (21 - len(patch.name)))
    patch.write_bytes(0x3F330, patch.name)  # We changed this section, but this pointer is still valid!
    deathlink_byte = world.options.death_link.value | (world.options.energy_link.value << 1)
    patch.write_byte(0x3F346, deathlink_byte)

    patch.write_bytes(0x3F34C, world.world_version)

    version_map = {
        "0": 0x00,
        "1": 0x01,
        "2": 0x02,
        "3": 0x03,
        "4": 0x04,
        "5": 0x05,
        "6": 0x06,
        "7": 0x07,
        "8": 0x08,
        "9": 0x09,
        ".": 0x26
    }
    patch.write_token(APTokenTypes.RLE, 0x653B, (11, 0x25))
    patch.write_token(APTokenTypes.RLE, 0x6549, (25, 0x25))

    # BY SILVRIS
    patch.write_bytes(0x653B, [0x0B, 0x22, 0x25, 0x1C, 0x12, 0x15, 0x1F, 0x1B, 0x12, 0x1C])
    # ARCHIPELAGO x.x.x
    patch.write_bytes(0x654D,
                      [0x0A, 0x1B, 0x0C, 0x11, 0x12, 0x19, 0x0E, 0x15, 0x0A, 0x10, 0x18])
    patch.write_bytes(0x6559, list(map(lambda c: version_map[c], __version__)))

    patch.write_file("token_patch.bin", patch.get_token_binary())


header = b"\x4E\x45\x53\x1A\x10\x10\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00"


def read_headerless_nes_rom(rom: bytes) -> bytes:
    if rom[:4] == b"NES\x1A":
        return rom[16:]
    else:
        return rom


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes: bytes | None = getattr(get_base_rom_bytes, "base_rom_bytes", None)
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
    from . import MM3World
    if not file_name:
        file_name = MM3World.settings.rom_file
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


prg_offset = 0xCF1B0
prg_size = 0x40000
chr_offset = 0x10F1B0
chr_size = 0x20000


def extract_mm3(proteus: bytes) -> bytes:
    mm3 = bytearray(proteus[prg_offset:prg_offset + prg_size])
    mm3.extend(proteus[chr_offset:chr_offset + chr_size])
    return bytes(mm3)
