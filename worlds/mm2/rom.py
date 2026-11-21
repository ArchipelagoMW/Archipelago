import pkgutil
from typing import Optional, TYPE_CHECKING, Iterable, Dict, Sequence
import hashlib
import Utils
import os

import settings
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from . import names
from .rules import minimum_weakness_requirement
from .text import MM2TextEntry
from .color import get_colors_for_item, write_palette_shuffle
from .options import Consumables, ReduceFlashing, RandomMusic

if TYPE_CHECKING:
    from . import MM2World

MM2LCHASH = "37f2c36ce7592f1e16b3434b3985c497"
PROTEUSHASH = "b69fff40212b80c94f19e786d1efbf61"
MM2NESHASH = "0527a0ee512f69e08b8db6dc97964632"
MM2VCHASH = "0c78dfe8e90fb8f3eed022ff01126ad3"

enemy_weakness_ptrs: Dict[int, int] = {
    0: 0x3E9A8,
    1: 0x3EA24,
    2: 0x3EA9C,
    3: 0x3EB14,
    4: 0x3EB8C,
    5: 0x3EC04,
    6: 0x3EC7C,
    7: 0x3ECF4,
}

enemy_addresses: Dict[str, int] = {
    "Shrink": 0x00,
    "M-445": 0x04,
    "Claw": 0x08,
    "Tanishi": 0x0A,
    "Kerog": 0x0C,
    "Petit Kerog": 0x0D,
    "Anko": 0x0F,
    "Batton": 0x16,
    "Robitto": 0x17,
    "Friender": 0x1C,
    "Monking": 0x1D,
    "Kukku": 0x1F,
    "Telly": 0x22,
    "Changkey Maker": 0x23,
    "Changkey": 0x24,
    "Pierrobot": 0x29,
    "Fly Boy": 0x2C,
    # "Crash Wall": 0x2D
    # "Friender Wall": 0x2E
    "Blocky": 0x31,
    "Neo Metall": 0x34,
    "Matasaburo": 0x36,
    "Pipi": 0x38,
    "Pipi Egg": 0x3A,
    "Copipi": 0x3C,
    "Kaminari Goro": 0x3E,
    "Petit Goblin": 0x45,
    "Springer": 0x46,
    "Mole (Up)": 0x48,
    "Mole (Down)": 0x49,
    "Shotman (Left)": 0x4B,
    "Shotman (Right)": 0x4C,
    "Sniper Armor": 0x4E,
    "Sniper Joe": 0x4F,
    "Scworm": 0x50,
    "Scworm Worm": 0x51,
    "Picopico-kun": 0x6A,
    "Boobeam Trap": 0x6D,
    "Big Fish": 0x71
}

# addresses printed when assembling basepatch
consumables_ptr: int = 0x3F2FE
quickswap_ptr: int = 0x3F363
wily_5_ptr: int = 0x3F3A1
energylink_ptr: int = 0x3F46B
get_equipped_sound_ptr: int = 0x3F384


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


class MM2ProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = [MM2LCHASH, MM2NESHASH, MM2VCHASH]
    game = "Mega Man 2"
    patch_file_ending = ".apmm2"
    result_file_ending = ".nes"
    name: bytearray
    procedure = [
        ("apply_bsdiff4", ["mm2_basepatch.bsdiff4"]),
        ("apply_tokens", ["token_patch.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_byte(self, offset: int, value: int) -> None:
        self.write_token(APTokenTypes.WRITE, offset, value.to_bytes(1, "little"))

    def write_bytes(self, offset: int, value: Iterable[int]) -> None:
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))


def patch_rom(world: "MM2World", patch: MM2ProcedurePatch) -> None:
    patch.write_file("mm2_basepatch.bsdiff4", pkgutil.get_data(__name__, "data/mm2_basepatch.bsdiff4"))
    # text writing
    patch.write_bytes(0x37E2A, MM2TextEntry("FOR           ", 0xCB).resolve())
    patch.write_bytes(0x37EAA, MM2TextEntry("GET EQUIPPED  ", 0x0B).resolve())
    patch.write_bytes(0x37EBA, MM2TextEntry("WITH          ", 0x2B).resolve())

    base_address = 0x3F650
    color_address = 0x37F6C
    for i, location in zip(range(11), [
        names.atomic_fire_get,
        names.air_shooter_get,
        names.leaf_shield_get,
        names.bubble_lead_get,
        names.quick_boomerang_get,
        names.time_stopper_get,
        names.metal_blade_get,
        names.crash_bomber_get,
        names.item_1_get,
        names.item_2_get,
        names.item_3_get
    ]):
        item = world.multiworld.get_location(location, world.player).item
        if item:
            if len(item.name) <= 14:
                # we want to just place it in the center
                first_str = ""
                second_str = item.name
                third_str = ""
            elif len(item.name) <= 28:
                # spread across second and third
                first_str = ""
                second_str = item.name[:14]
                third_str = item.name[14:]
            else:
                # all three
                first_str = item.name[:14]
                second_str = item.name[14:28]
                third_str = item.name[28:]
                if len(third_str) > 16:
                    third_str = third_str[:16]
            player_str = world.multiworld.get_player_name(item.player)
            if len(player_str) > 14:
                player_str = player_str[:14]
            patch.write_bytes(base_address + (64 * i), MM2TextEntry(first_str, 0x4B).resolve())
            patch.write_bytes(base_address + (64 * i) + 16, MM2TextEntry(second_str, 0x6B).resolve())
            patch.write_bytes(base_address + (64 * i) + 32, MM2TextEntry(third_str, 0x8B).resolve())
            patch.write_bytes(base_address + (64 * i) + 48, MM2TextEntry(player_str, 0xEB).resolve())

            colors = get_colors_for_item(item.name)
            if i > 7:
                patch.write_bytes(color_address + 27 + ((i - 8) * 2), colors)
            else:
                patch.write_bytes(color_address + (i * 2), colors)

    write_palette_shuffle(world, patch)

    enemy_weaknesses: Dict[str, Dict[int, int]] = {}

    if world.options.strict_weakness or world.options.random_weakness or world.options.plando_weakness:
        # we need to write boss weaknesses
        output = bytearray()
        for weapon in world.weapon_damage:
            if weapon == 8:
                continue  # Time Stopper is a special case
            weapon_damage = [world.weapon_damage[weapon][i]
                             if world.weapon_damage[weapon][i] >= 0
                             else 256 + world.weapon_damage[weapon][i]
                             for i in range(14)]
            output.extend(weapon_damage)
        patch.write_bytes(0x2E952, bytes(output))
        time_stopper_damage = world.weapon_damage[8]
        time_offset = 0x2C03B
        damage_table = {
            4: 0xF,
            3: 0x17,
            2: 0x1E,
            1: 0x25
        }
        for boss, damage in enumerate(time_stopper_damage):
            if damage > 4:
                damage = 4  # 4 is a guaranteed kill, no need to exceed
            if damage <= 0:
                patch.write_byte(time_offset + 14 + boss, 0)
            else:
                patch.write_byte(time_offset + 14 + boss, 1)
                patch.write_byte(time_offset + boss, damage_table[damage])
        if world.options.random_weakness:
            wily_5_weaknesses = [i for i in range(8) if world.weapon_damage[i][12] > minimum_weakness_requirement[i]]
            world.random.shuffle(wily_5_weaknesses)
            if len(wily_5_weaknesses) >= 3:
                weak1 = wily_5_weaknesses.pop()
                weak2 = wily_5_weaknesses.pop()
                weak3 = wily_5_weaknesses.pop()
            elif len(wily_5_weaknesses) == 2:
                weak1 = weak2 = wily_5_weaknesses.pop()
                weak3 = wily_5_weaknesses.pop()
            else:
                weak1 = weak2 = weak3 = 0
            patch.write_byte(0x2DA2E, weak1)
            patch.write_byte(0x2DA32, weak2)
            patch.write_byte(0x2DA3A, weak3)
        enemy_weaknesses["Picopico-kun"] = {weapon: world.weapon_damage[weapon][9] for weapon in range(8)}
        enemy_weaknesses["Boobeam Trap"] = {weapon: world.weapon_damage[weapon][11] for weapon in range(8)}

    if world.options.enemy_weakness:
        for enemy in enemy_addresses:
            if enemy in ("Picopico-kun", "Boobeam Trap"):
                continue
            enemy_weaknesses[enemy] = {weapon: world.random.randint(-4, 4) for weapon in enemy_weakness_ptrs}
            if enemy == "Friender":
                # Friender has to be killed, need buster damage to not break logic
                enemy_weaknesses[enemy][0] = max(enemy_weaknesses[enemy][0], 1)

    for enemy, damage_table in enemy_weaknesses.items():
        for weapon in enemy_weakness_ptrs:
            if damage_table[weapon] < 0:
                damage_table[weapon] = 256 + damage_table[weapon]
            patch.write_byte(enemy_weakness_ptrs[weapon] + enemy_addresses[enemy], damage_table[weapon])

    if world.options.quickswap:
        patch.write_byte(quickswap_ptr + 1, 0x01)

    if world.options.consumables != Consumables.option_all:
        value_a = 0x7C
        value_b = 0x76
        if world.options.consumables == Consumables.option_1up_etank:
            value_b = 0x7A
        else:
            value_a = 0x7A
        patch.write_byte(consumables_ptr - 3, value_a)
        patch.write_byte(consumables_ptr + 1, value_b)

    patch.write_byte(wily_5_ptr + 1, world.options.wily_5_requirement.value)

    if world.options.energy_link:
        patch.write_byte(energylink_ptr + 1, 1)

    if world.options.reduce_flashing:
        if world.options.reduce_flashing.value == ReduceFlashing.option_virtual_console:
            color = 0x2D  # Dark Gray
            speed = -1
        elif world.options.reduce_flashing.value == ReduceFlashing.option_minor:
            color = 0x2D
            speed = 0x08
        else:
            color = 0x0F
            speed = 0x00
        patch.write_byte(0x2D1B0, color)  # Change white to a dark gray, Mecha Dragon
        patch.write_byte(0x2D397, 0x0F)  # Longer flash time, Mecha Dragon kill
        patch.write_byte(0x2D3A0, color)  # Change white to a dark gray, Picopico-kun/Boobeam Trap
        patch.write_byte(0x2D65F, color)  # Change white to a dark gray, Guts Tank
        patch.write_byte(0x2DA94, color)  # Change white to a dark gray, Wily Machine
        patch.write_byte(0x2DC97, color)  # Change white to a dark gray, Alien
        patch.write_byte(0x2DD68, 0x10)  # Longer flash time, Alien kill
        patch.write_bytes(0x2DF14, [0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA])  # Reduce final Alien flash to 1 big flash
        patch.write_byte(0x34132, 0x08)  # Longer flash time, Stage Select

        if world.options.reduce_flashing.value == ReduceFlashing.option_full:
            # reduce color of stage flashing
            patch.write_bytes(0x344C9, [0x2D, 0x10, 0x00, 0x2D,
                                        0x0F, 0x10, 0x2D, 0x00,
                                        0x0F, 0x10, 0x2D, 0x00,
                                        0x0F, 0x10, 0x2D, 0x00,
                                        0x2D, 0x10, 0x2D, 0x00,
                                        0x0F, 0x10, 0x2D, 0x00,
                                        0x0F, 0x10, 0x2D, 0x00,
                                        0x0F, 0x10, 0x2D, 0x00])
            # remove wily castle flash
            patch.write_byte(0x3596D, 0x0F)

        if speed != -1:
            patch.write_byte(0xFE01, speed)  # Bubble Man Stage
            patch.write_byte(0x1BE01, speed)  # Metal Man Stage

    if world.options.random_music:
        if world.options.random_music == RandomMusic.option_none:
            pool = [0xFF] * 20
            # A couple of additional mutes we want here
            patch.write_byte(0x37819, 0xFF)  # Credits
            patch.write_byte(0x378A4, 0xFF)  # Credits #2
            patch.write_byte(0x37149, 0xFF)  # Game Over Jingle
            patch.write_byte(0x341BA, 0xFF)  # Robot Master Jingle
            patch.write_byte(0x2E0B4, 0xFF)  # Robot Master Defeated
            patch.write_byte(0x35B78, 0xFF)  # Wily Castle
            patch.write_byte(0x2DFA5, 0xFF)  # Wily Defeated

        elif world.options.random_music == RandomMusic.option_shuffled:
            pool = [0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 9, 9, 9, 0x10, 0xC, 0xB, 0x17, 0x13, 0xE, 0xD]
            world.random.shuffle(pool)
        else:
            pool = world.random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0xB, 0xC, 0xD, 0xE, 0x10, 0x13, 0x17], k=20)
        patch.write_bytes(0x381E0, pool[:13])
        patch.write_byte(0x36318, pool[13])  # Game Start
        patch.write_byte(0x37181, pool[13])  # Game Over
        patch.write_byte(0x340AE, pool[14])  # RBM Select
        patch.write_byte(0x39005, pool[15])  # Robot Master Battle
        patch.write_byte(get_equipped_sound_ptr + 1, pool[16])  # Get Equipped, we actually hook this already lmao
        patch.write_byte(0x3775A, pool[17])  # Epilogue
        patch.write_byte(0x36089, pool[18])  # Intro
        patch.write_byte(0x361F1, pool[19])  # Title

    from Utils import __version__
    patch.name = bytearray(f'MM2{__version__.replace(".", "")[0:3]}_{world.player}_{world.multiworld.seed:11}\0',
                           'utf8')[:21]
    patch.name.extend([0] * (21 - len(patch.name)))
    patch.write_bytes(0x3FFC0, patch.name)
    deathlink_byte = world.options.death_link.value | (world.options.energy_link.value << 1)
    patch.write_byte(0x3FFD5, deathlink_byte)

    patch.write_bytes(0x3FFD8, world.world_version)

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
    patch.write_token(APTokenTypes.RLE, 0x36EE0, (11, 0))
    patch.write_token(APTokenTypes.RLE, 0x36EEE, (25, 0))

    # BY SILVRIS
    patch.write_bytes(0x36EE0, [0xC2, 0xD9, 0xC0, 0xD3, 0xC9, 0xCC, 0xD6, 0xD2, 0xC9, 0xD3])
    # ARCHIPELAGO x.x.x
    patch.write_bytes(0x36EF2, [0xC1, 0xD2, 0xC3, 0xC8, 0xC9, 0xD0, 0xC5, 0xCC, 0xC1, 0xC7, 0xCF, 0xC0])
    patch.write_bytes(0x36EFE, list(map(lambda c: version_map[c], __version__)))

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
            base_rom_bytes = extract_mm2(base_rom_bytes)
            basemd5 = hashlib.md5()
            basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in {MM2LCHASH, MM2NESHASH, MM2VCHASH}:
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


PRG_OFFSET = 0x8F170
PRG_SIZE = 0x40000


def extract_mm2(proteus: bytes) -> bytes:
    mm2 = bytearray(proteus[PRG_OFFSET:PRG_OFFSET + PRG_SIZE])
    return bytes(mm2)
