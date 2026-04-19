from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
import os
from typing import TYPE_CHECKING, Optional

from Utils import local_path, pc_to_snes, snes_to_pc

if TYPE_CHECKING:
    from . import ALTTPWorld
    from .Rom import LocalRom


@dataclass(frozen=True)
class BossPatchData:
    pointer: tuple[int, int]
    graphics: int
    sprite_array: tuple[int, ...]


@dataclass(frozen=True)
class DungeonBossPatchData:
    room_id: int
    sprite_pointer_address: int
    shell_x: int
    shell_y: int
    clear_layer2: bool = False
    extra_sprites: tuple[int, ...] = ()
    gt_sprite_write_address: Optional[int] = None


@dataclass
class RoomObjectTable:
    header_byte_0: int
    header_byte_1: int
    layer_1_objects: list[bytes] = field(default_factory=list)
    layer_1_doors: list[bytes] = field(default_factory=list)
    layer_2_objects: list[bytes] = field(default_factory=list)
    layer_2_doors: list[bytes] = field(default_factory=list)
    layer_3_objects: list[bytes] = field(default_factory=list)
    layer_3_doors: list[bytes] = field(default_factory=list)

    @classmethod
    def from_rom(cls, rom: "LocalRom", start_address: int) -> "RoomObjectTable":
        table = cls(rom.read_byte(start_address), rom.read_byte(start_address + 1))
        layers = (
            (table.layer_1_objects, table.layer_1_doors),
            (table.layer_2_objects, table.layer_2_doors),
            (table.layer_3_objects, table.layer_3_doors),
        )
        index = start_address + 2

        for objects, doors in layers:
            is_door = False
            while True:
                if rom.read_bytes(index, 2) == bytearray((0xF0, 0xFF)):
                    is_door = True
                    index += 2
                    continue
                if rom.read_bytes(index, 2) == bytearray((0xFF, 0xFF)):
                    index += 2
                    break
                if is_door:
                    doors.append(bytes(rom.read_bytes(index, 2)))
                    index += 2
                else:
                    objects.append(bytes(rom.read_bytes(index, 3)))
                    index += 3

        return table

    def add_shell(self, x: int, y: int, clear_layer_2: bool, shell_id: int) -> None:
        self.header_byte_0 = 0xF0
        if clear_layer_2:
            self.layer_2_objects.clear()
        self.layer_2_objects.append(_build_subtype_3_object(x, y, shell_id))

    def remove_shell(self, shell_id: int) -> None:
        self.layer_2_objects = [obj for obj in self.layer_2_objects if _object_id(obj) != shell_id]

    def to_bytes(self) -> bytes:
        output = bytearray((self.header_byte_0, self.header_byte_1))
        output.extend(self._serialize_layer(self.layer_1_objects, self.layer_1_doors, is_last_layer=False))
        output.extend(self._serialize_layer(self.layer_2_objects, self.layer_2_doors, is_last_layer=False))
        output.extend(self._serialize_layer(self.layer_3_objects, self.layer_3_doors, is_last_layer=True))
        return bytes(output)

    @staticmethod
    def _serialize_layer(objects: list[bytes], doors: list[bytes], is_last_layer: bool) -> bytes:
        output = bytearray()
        for obj in objects:
            output.extend(obj)
        if is_last_layer or doors:
            output.extend((0xF0, 0xFF))
        for door in doors:
            output.extend(door)
        output.extend((0xFF, 0xFF))
        return bytes(output)


BOSS_PATCH_DATA: dict[str, BossPatchData] = {
    "Armos": BossPatchData((0x87, 0xE8), 9, (0x05, 0x04, 0x53, 0x05, 0x07, 0x53, 0x05, 0x0A, 0x53,
                                              0x08, 0x0A, 0x53, 0x08, 0x07, 0x53, 0x08, 0x04, 0x53,
                                              0x08, 0xE7, 0x19)),
    "Arrghus": BossPatchData((0x97, 0xD9), 20, (0x07, 0x07, 0x8C, 0x07, 0x07, 0x8D, 0x07, 0x07, 0x8D,
                                                0x07, 0x07, 0x8D, 0x07, 0x07, 0x8D, 0x07, 0x07, 0x8D,
                                                0x07, 0x07, 0x8D, 0x07, 0x07, 0x8D, 0x07, 0x07, 0x8D,
                                                0x07, 0x07, 0x8D, 0x07, 0x07, 0x8D, 0x07, 0x07, 0x8D,
                                                0x07, 0x07, 0x8D, 0x07, 0x07, 0x8D)),
    "Blind": BossPatchData((0x54, 0xE6), 32, (0x05, 0x09, 0xCE)),
    "Helmasaur": BossPatchData((0x49, 0xE0), 21, (0x06, 0x07, 0x92)),
    "Kholdstare": BossPatchData((0x01, 0xEA), 22, (0x05, 0x07, 0xA3, 0x05, 0x07, 0xA4, 0x05, 0x07, 0xA2)),
    "Lanmola": BossPatchData((0xCB, 0xDC), 11, (0x07, 0x06, 0x54, 0x07, 0x09, 0x54, 0x09, 0x07, 0x54)),
    "Moldorm": BossPatchData((0xC3, 0xD9), 12, (0x09, 0x09, 0x09)),
    "Mothula": BossPatchData((0x31, 0xDC), 26, (0x06, 0x08, 0x88)),
    "Trinexx": BossPatchData((0xBA, 0xE5), 23, (0x05, 0x07, 0xCB, 0x05, 0x07, 0xCC, 0x05, 0x07, 0xCD)),
    "Vitreous": BossPatchData((0x57, 0xE4), 22, (0x05, 0x07, 0xBD)),
}

DUNGEON_BOSS_PATCH_DATA: dict[tuple[str, Optional[str]], DungeonBossPatchData] = {
    ("Eastern Palace", None): DungeonBossPatchData(200, 0x04D7BE, 0x2B, 0x28),
    ("Desert Palace", None): DungeonBossPatchData(51, 0x04D694, 0x0B, 0x28),
    ("Tower of Hera", None): DungeonBossPatchData(7, 0x04D63C, 0x18, 0x16),
    ("Palace of Darkness", None): DungeonBossPatchData(90, 0x04D6E2, 0x2B, 0x28),
    ("Swamp Palace", None): DungeonBossPatchData(6, 0x04D63A, 0x0B, 0x28),
    ("Skull Woods", None): DungeonBossPatchData(41, 0x04D680, 0x2B, 0x28),
    ("Thieves Town", None): DungeonBossPatchData(172, 0x04D786, 0x2B, 0x28, clear_layer2=True),
    ("Ice Palace", None): DungeonBossPatchData(222, 0x04D7EA, 0x2B, 0x08, clear_layer2=True),
    ("Misery Mire", None): DungeonBossPatchData(144, 0x04D74E, 0x0B, 0x28, clear_layer2=True),
    ("Turtle Rock", None): DungeonBossPatchData(164, 0x04D776, 0x0B, 0x28, clear_layer2=True),
    ("Ganons Tower", "bottom"): DungeonBossPatchData(
        28, 0x04D666, 0x2B, 0x28, extra_sprites=(0x07, 0x07, 0xE3, 0x07, 0x08, 0xE3, 0x08, 0x07, 0xE3, 0x08, 0x08, 0xE3),
        gt_sprite_write_address=0x04D87E,
    ),
    ("Ganons Tower", "middle"): DungeonBossPatchData(
        108, 0x04D706, 0x0B, 0x28, extra_sprites=(0x18, 0x17, 0xD1, 0x1C, 0x03, 0xC5), gt_sprite_write_address=0x04D8B6,
    ),
    ("Ganons Tower", "top"): DungeonBossPatchData(77, 0x04D6C8, 0x18, 0x16),
}

TRINEXX_SHELL_OBJECT_ID = 0xFF2
KHOLDSTARE_SHELL_OBJECT_ID = 0xF95
TRINEXX_VANILLA_ROOM_ID = 164
KHOLDSTARE_VANILLA_ROOM_ID = 222

_ENEMIZER_SYMBOLS: Optional[dict[str, int]] = None

BOSS_GFX_SHEET_INDEXES = {
    "Agahnim1": 0x8D,
    "Agahnim2": 0xB5,
    "Agahnim3": 0xC8,
    "Agahnim4": 0xB6,
    "ArmosKnight1": 0x90,
    "Ganon1": 0x94,
    "Ganon2": 0xA6,
    "Ganon3": 0xB4,
    "Ganon4": 0xB8,
    "Moldorm1": 0xA3,
    "Lanmola1": 0xA4,
    "Arrghus1": 0xAC,
    "Mothula1": 0xAB,
    "Helmasaure1": 0xAD,
    "Helmasaure2": 0xB1,
    "Blind1": 0xAE,
    "Kholdstare1": 0xAF,
    "Vitreous1": 0xB0,
    "Trinexx1": 0xB2,
    "Trinexx2": 0xB3,
}

def patch_bosses(world: "ALTTPWorld", rom: "LocalRom") -> None:
    _patch_boss_gfx_tables(rom)
    dungeon_header_base = _get_enemizer_symbol("room_header_table")
    moved_room_object_base = _get_enemizer_symbol("modified_room_object_table")
    gt_dungeon_name = "Ganons Tower" if world.options.mode != "inverted" else "Inverted Ganons Tower"
    gt_dungeon = world.dungeons[gt_dungeon_name]

    placements = (
        (world.dungeons["Eastern Palace"].boss.enemizer_name, DUNGEON_BOSS_PATCH_DATA[("Eastern Palace", None)]),
        (world.dungeons["Desert Palace"].boss.enemizer_name, DUNGEON_BOSS_PATCH_DATA[("Desert Palace", None)]),
        (world.dungeons["Tower of Hera"].boss.enemizer_name, DUNGEON_BOSS_PATCH_DATA[("Tower of Hera", None)]),
        (world.dungeons["Palace of Darkness"].boss.enemizer_name, DUNGEON_BOSS_PATCH_DATA[("Palace of Darkness", None)]),
        (world.dungeons["Swamp Palace"].boss.enemizer_name, DUNGEON_BOSS_PATCH_DATA[("Swamp Palace", None)]),
        (world.dungeons["Skull Woods"].boss.enemizer_name, DUNGEON_BOSS_PATCH_DATA[("Skull Woods", None)]),
        (world.dungeons["Thieves Town"].boss.enemizer_name, DUNGEON_BOSS_PATCH_DATA[("Thieves Town", None)]),
        (world.dungeons["Ice Palace"].boss.enemizer_name, DUNGEON_BOSS_PATCH_DATA[("Ice Palace", None)]),
        (world.dungeons["Misery Mire"].boss.enemizer_name, DUNGEON_BOSS_PATCH_DATA[("Misery Mire", None)]),
        (world.dungeons["Turtle Rock"].boss.enemizer_name, DUNGEON_BOSS_PATCH_DATA[("Turtle Rock", None)]),
        (gt_dungeon.bosses["bottom"].enemizer_name, DUNGEON_BOSS_PATCH_DATA[("Ganons Tower", "bottom")]),
        (gt_dungeon.bosses["middle"].enemizer_name, DUNGEON_BOSS_PATCH_DATA[("Ganons Tower", "middle")]),
        (gt_dungeon.bosses["top"].enemizer_name, DUNGEON_BOSS_PATCH_DATA[("Ganons Tower", "top")]),
    )

    modified_room_tables: dict[int, RoomObjectTable] = {}

    for boss_name, dungeon_data in placements:
        boss_data = BOSS_PATCH_DATA[boss_name]
        rom.write_bytes(dungeon_data.sprite_pointer_address, boss_data.pointer)
        rom.write_byte(dungeon_header_base + (dungeon_data.room_id * 14) + 3, boss_data.graphics)

        if boss_name == "Trinexx" and dungeon_data.room_id != TRINEXX_VANILLA_ROOM_ID:
            room_table = _get_room_object_table(rom, modified_room_tables, dungeon_data.room_id)
            room_table.add_shell(
                dungeon_data.shell_x,
                dungeon_data.shell_y - 2,
                dungeon_data.clear_layer2,
                TRINEXX_SHELL_OBJECT_ID,
            )
            rom.write_byte(dungeon_header_base + (dungeon_data.room_id * 14), 0x60)
            rom.write_byte(dungeon_header_base + (dungeon_data.room_id * 14) + 4, 0x04)

        if boss_name == "Kholdstare" and dungeon_data.room_id != KHOLDSTARE_VANILLA_ROOM_ID:
            room_table = _get_room_object_table(rom, modified_room_tables, dungeon_data.room_id)
            room_table.add_shell(
                dungeon_data.shell_x,
                dungeon_data.shell_y,
                dungeon_data.clear_layer2,
                KHOLDSTARE_SHELL_OBJECT_ID,
            )
            rom.write_byte(dungeon_header_base + (dungeon_data.room_id * 14), 0xE0)
            rom.write_byte(dungeon_header_base + (dungeon_data.room_id * 14) + 4, 0x01)

        if boss_name != "Trinexx" and dungeon_data.room_id == TRINEXX_VANILLA_ROOM_ID:
            _get_room_object_table(rom, modified_room_tables, dungeon_data.room_id).remove_shell(TRINEXX_SHELL_OBJECT_ID)

        if boss_name != "Kholdstare" and dungeon_data.room_id == KHOLDSTARE_VANILLA_ROOM_ID:
            _get_room_object_table(rom, modified_room_tables, dungeon_data.room_id).remove_shell(KHOLDSTARE_SHELL_OBJECT_ID)

        if dungeon_data.gt_sprite_write_address is not None:
            _write_gt_boss_sprite_block(rom, dungeon_data, boss_data)

    write_address = moved_room_object_base
    for room_id in sorted(modified_room_tables):
        table_bytes = modified_room_tables[room_id].to_bytes()
        _write_room_object_pointer(rom, room_id, write_address)
        rom.write_bytes(write_address, table_bytes)
        write_address += len(table_bytes)

    rom.write_byte(0x1B0101, 0x01)
    rom.write_byte(0x04DE81, 0x00)
    if world.dungeons["Thieves Town"].boss.enemizer_name == "Blind":
        rom.write_byte(0x04DE81, 0x06)
        rom.write_byte(0x1B0101, 0x00)


def _get_room_object_table(rom: "LocalRom", cache: dict[int, RoomObjectTable], room_id: int) -> RoomObjectTable:
    room_table = cache.get(room_id)
    if room_table is not None:
        return room_table

    pointer_address = 0xF8000 + (room_id * 3)
    snes_address_bytes = rom.read_bytes(pointer_address, 3)
    snes_address = (snes_address_bytes[2] << 16) | (snes_address_bytes[1] << 8) | snes_address_bytes[0]
    room_table = RoomObjectTable.from_rom(rom, snes_to_pc(snes_address))
    cache[room_id] = room_table
    return room_table


def _write_gt_boss_sprite_block(rom: "LocalRom", dungeon_data: DungeonBossPatchData, boss_data: BossPatchData) -> None:
    assert dungeon_data.gt_sprite_write_address is not None
    rom.write_int16(dungeon_data.sprite_pointer_address, dungeon_data.gt_sprite_write_address)

    sprite_block = bytearray((0x00,))
    sprite_block.extend(boss_data.sprite_array)
    if dungeon_data.room_id == 28 and boss_data.pointer == BOSS_PATCH_DATA["Arrghus"].pointer:
        sprite_block.extend(dungeon_data.extra_sprites[:6])
    else:
        sprite_block.extend(dungeon_data.extra_sprites)
    sprite_block.append(0xFF)
    rom.write_bytes(dungeon_data.gt_sprite_write_address, sprite_block)


def _write_room_object_pointer(rom: "LocalRom", room_id: int, pc_address: int) -> None:
    snes_address = pc_to_snes(pc_address)
    pointer_address = 0xF8000 + (room_id * 3)
    rom.write_bytes(pointer_address, (
        snes_address & 0xFF,
        (snes_address >> 8) & 0xFF,
        (snes_address >> 16) & 0xFF,
    ))


def _build_subtype_3_object(x: int, y: int, object_id: int) -> bytes:
    return bytes((
        ((x << 2) & 0xFC) | (object_id & 0x03),
        ((y << 2) & 0xFC) | ((object_id >> 2) & 0x03),
        0xF0 | ((object_id >> 4) & 0x0F),
    ))


def _object_id(object_bytes: bytes) -> Optional[int]:
    if len(object_bytes) != 3:
        return None
    if object_bytes[0] >= 0xFC:
        return (object_bytes[2] & 0x3F) + 0x100
    if object_bytes[2] >= 0xF8:
        return 0xF00 | ((object_bytes[2] & 0x0F) << 4) | ((object_bytes[1] & 0x03) << 2) | (object_bytes[0] & 0x03)
    return object_bytes[2]


def _get_enemizer_symbol(symbol_name: str) -> int:
    global _ENEMIZER_SYMBOLS
    if _ENEMIZER_SYMBOLS is None:
        _ENEMIZER_SYMBOLS = _load_enemizer_symbols()
    return _ENEMIZER_SYMBOLS[symbol_name]


def _load_enemizer_symbols() -> dict[str, int]:
    raw_symbols = pkgutil.get_data(__package__, "data/enemizer/exported_symbols.txt")
    if raw_symbols is None:
        raise FileNotFoundError("Missing vendored Enemizer symbols required by ALTTP native boss patching")

    symbols: dict[str, int] = {}
    for line in raw_symbols.decode("utf-8").splitlines():
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            continue
        snes_address = int(parts[0].replace(":", ""), 16)
        symbols[parts[1]] = snes_to_pc(snes_address)
    return symbols


def _patch_boss_gfx_tables(rom: "LocalRom") -> None:
    boss_gfx_table = _load_cached_boss_gfx_table()
    for sheet_name, table_index in BOSS_GFX_SHEET_INDEXES.items():
        bank, high, low = boss_gfx_table[sheet_name]
        rom.write_byte(0x4FC0 + table_index, bank)
        rom.write_byte(0x509F + table_index, high)
        rom.write_byte(0x517E + table_index, low)


def _load_cached_boss_gfx_table() -> dict[str, tuple[int, int, int]]:
    cache_dir = local_path("data", "enemizer_cache")
    cache_path = os.path.join(cache_dir, "boss_gfx_table_v1.json")

    from .Rom import LTTPJPN10HASH, get_base_rom_bytes

    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as cache_file:
            payload = json.load(cache_file)
        if payload.get("base_rom_md5") == LTTPJPN10HASH and payload.get("version") == 1:
            return {name: tuple(values) for name, values in payload["table"].items()}

    base_rom_bytes = get_base_rom_bytes()
    table = {
        sheet_name: (
            base_rom_bytes[0x4FC0 + table_index],
            base_rom_bytes[0x509F + table_index],
            base_rom_bytes[0x517E + table_index],
        )
        for sheet_name, table_index in BOSS_GFX_SHEET_INDEXES.items()
    }

    os.makedirs(cache_dir, exist_ok=True)
    with open(cache_path, "w", encoding="utf-8") as cache_file:
        json.dump(
            {
                "version": 1,
                "base_rom_md5": hashlib.md5(base_rom_bytes).hexdigest(),
                "table": {name: list(values) for name, values in table.items()},
            },
            cache_file,
            separators=(",", ":"),
        )

    return table
