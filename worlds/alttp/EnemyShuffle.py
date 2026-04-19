from __future__ import annotations

from dataclasses import dataclass
import pkgutil
from typing import Optional

from Utils import snes_to_pc

from .Rom import get_base_rom_bytes


DUNGEON_HEADER_POINTER_TABLE_BASE = 0x271E2
DUNGEON_SPRITE_POINTER_TABLE_BASE = 0x4D62E
TOTAL_DUNGEON_ROOMS = 0x128

SPRITE_OVERLORD_MASK = 0xE0
SPRITE_OVERLORD_REMOVE_MASK = 0x1F
SPRITE_SUBTYPE_BYTE_0_MASK = 0x60
KEY_SPRITE_ID = 0xE4
BIG_KEY_SPRITE_ID = 0xE5
WALLMASTER_SPRITE_ID = 0x90

SHUTTER_ROOM_IDS = frozenset({
    11, 14, 27, 36, 40, 46, 49, 61, 62, 68, 69, 75, 83, 93, 107, 110, 113, 117, 123, 125, 133, 135, 141, 150, 165,
    168, 176, 178, 182, 184, 192, 210, 216, 224, 239, 268, 291, 4,
})
WATER_ROOM_IDS = frozenset({22, 40, 52, 54, 56, 70, 102})
DONT_RANDOMIZE_ROOM_IDS = frozenset({0, 1, 3, 13, 20, 32, 48, 127})
NO_SPECIAL_ENEMIES_STANDARD_ROOM_IDS = frozenset({
    1, 2, 17, 33, 34, 50, 65, 66, 80, 81, 82, 85, 96, 97, 98, 112, 113, 114, 128, 129, 130,
})


@dataclass(frozen=True)
class DungeonEnemySprite:
    address: int
    byte_0: int
    byte_1: int
    sprite_id: int
    is_overlord: bool
    has_key: bool

    @property
    def is_on_bg2(self) -> bool:
        return bool(self.byte_0 & 0x80)

    @property
    def hm_param(self) -> int:
        return ((self.byte_0 & 0x60) >> 2) | ((self.byte_1 & 0xE0) >> 5)

    @property
    def y_coord_pixels(self) -> int:
        return (self.byte_0 & 0x1F) * 16

    @property
    def x_coord_pixels(self) -> int:
        return (self.byte_1 & 0x1F) * 16


@dataclass(frozen=True)
class DungeonEnemyRoom:
    room_id: int
    room_header_address: int
    sprite_table_address: int
    graphics_block_id: int
    tag_1: int
    tag_2: int
    sort_sprites_value: int
    sprites: tuple[DungeonEnemySprite, ...]
    is_shutter_room: bool
    is_water_room: bool
    do_not_randomize: bool
    no_special_enemies_standard: bool


@dataclass(frozen=True)
class EnemyShuffleState:
    dungeon_rooms: dict[int, DungeonEnemyRoom]


def generate_enemy_shuffle_state() -> EnemyShuffleState:
    rom_bytes = get_base_rom_bytes()
    moved_header_bank = _get_enemizer_symbol("moved_room_header_bank_value_address")
    return EnemyShuffleState(
        dungeon_rooms={
            room.room_id: room
            for room in _read_dungeon_rooms(rom_bytes, moved_header_bank)
        }
    )


def _read_dungeon_rooms(rom_bytes: bytes, moved_header_bank_address: int) -> list[DungeonEnemyRoom]:
    rooms: list[DungeonEnemyRoom] = []
    room_header_bank = rom_bytes[moved_header_bank_address]

    for room_id in range(TOTAL_DUNGEON_ROOMS):
        room_header_address = _read_room_header_address(rom_bytes, room_id, room_header_bank)
        sprite_table_address = _read_room_sprite_table_address(rom_bytes, room_id)
        rooms.append(
            DungeonEnemyRoom(
                room_id=room_id,
                room_header_address=room_header_address,
                sprite_table_address=sprite_table_address,
                graphics_block_id=rom_bytes[room_header_address + 3],
                tag_1=rom_bytes[room_header_address + 5],
                tag_2=rom_bytes[room_header_address + 6],
                sort_sprites_value=rom_bytes[sprite_table_address],
                sprites=_read_room_sprites(rom_bytes, sprite_table_address),
                is_shutter_room=room_id in SHUTTER_ROOM_IDS,
                is_water_room=room_id in WATER_ROOM_IDS,
                do_not_randomize=room_id in DONT_RANDOMIZE_ROOM_IDS,
                no_special_enemies_standard=room_id in NO_SPECIAL_ENEMIES_STANDARD_ROOM_IDS,
            )
        )

    return rooms


def _read_room_header_address(rom_bytes: bytes, room_id: int, room_header_bank: int) -> int:
    pointer_address = DUNGEON_HEADER_POINTER_TABLE_BASE + (room_id * 2)
    snes_address = (
        rom_bytes[pointer_address]
        | (rom_bytes[pointer_address + 1] << 8)
        | (room_header_bank << 16)
    )
    return snes_to_pc(snes_address)


def _read_room_sprite_table_address(rom_bytes: bytes, room_id: int) -> int:
    pointer_address = DUNGEON_SPRITE_POINTER_TABLE_BASE + (room_id * 2)
    snes_address = (
        rom_bytes[pointer_address]
        | (rom_bytes[pointer_address + 1] << 8)
        | (0x09 << 16)
    )
    return snes_to_pc(snes_address)


def _read_room_sprites(rom_bytes: bytes, sprite_table_address: int) -> tuple[DungeonEnemySprite, ...]:
    sprites: list[DungeonEnemySprite] = []
    index = sprite_table_address + 1  # byte 0 is sort-sprites metadata

    while rom_bytes[index] != 0xFF:
        byte_0 = rom_bytes[index]
        byte_1 = rom_bytes[index + 1]
        sprite_id = rom_bytes[index + 2]
        is_overlord = (byte_1 & SPRITE_OVERLORD_MASK) == SPRITE_OVERLORD_MASK and (
            (byte_0 & SPRITE_SUBTYPE_BYTE_0_MASK) != SPRITE_SUBTYPE_BYTE_0_MASK
        )
        if not is_overlord and sprite_id not in {KEY_SPRITE_ID, WALLMASTER_SPRITE_ID}:
            byte_0 &= 0x9F
            byte_1 &= SPRITE_OVERLORD_REMOVE_MASK
        has_key = bool(
            rom_bytes[index + 3] != 0xFF
            and rom_bytes[index + 5] in {KEY_SPRITE_ID, BIG_KEY_SPRITE_ID}
        )
        sprites.append(
            DungeonEnemySprite(
                address=index,
                byte_0=byte_0,
                byte_1=byte_1,
                sprite_id=sprite_id + (0x100 if is_overlord else 0),
                is_overlord=is_overlord,
                has_key=has_key,
            )
        )
        index += 3

    return tuple(sprites)


def _get_enemizer_symbol(symbol_name: str) -> int:
    raw_symbols = pkgutil.get_data(__package__, "data/enemizer/exported_symbols.txt")
    if raw_symbols is None:
        raise FileNotFoundError("Missing vendored Enemizer symbols required by ALTTP enemy state generation")

    for line in raw_symbols.decode("utf-8").splitlines():
        parts = line.split(maxsplit=1)
        if len(parts) != 2 or parts[1] != symbol_name:
            continue
        return snes_to_pc(int(parts[0].replace(":", ""), 16))
    raise KeyError(symbol_name)
