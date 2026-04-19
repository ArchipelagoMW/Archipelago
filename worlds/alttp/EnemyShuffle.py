from __future__ import annotations

from dataclasses import dataclass
import json
import pkgutil
from typing import Optional

from Utils import snes_to_pc

from .Rom import get_base_rom_bytes


DUNGEON_HEADER_POINTER_TABLE_BASE = 0x271E2
DUNGEON_SPRITE_POINTER_TABLE_BASE = 0x4D62E
SPRITE_GROUP_BASE_ADDRESS = 0x5B97
TOTAL_SPRITE_GROUPS = 144
TOTAL_DUNGEON_ROOMS = 0x128

SPRITE_OVERLORD_MASK = 0xE0
SPRITE_OVERLORD_REMOVE_MASK = 0x1F
SPRITE_SUBTYPE_BYTE_0_MASK = 0x60
KEY_SPRITE_ID = 0xE4
BIG_KEY_SPRITE_ID = 0xE5
WALLMASTER_SPRITE_ID = 0x90

@dataclass(frozen=True)
class RoomGroupRequirement:
    group_id: Optional[int]
    subgroup_0: Optional[int]
    subgroup_1: Optional[int]
    subgroup_2: Optional[int]
    subgroup_3: Optional[int]
    rooms: tuple[int, ...]


@dataclass(frozen=True)
class DungeonSpriteGroup:
    group_id: int
    dungeon_group_id: int
    subgroup_0: int
    subgroup_1: int
    subgroup_2: int
    subgroup_3: int


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
    required_group_id: Optional[int]
    required_subgroup_0: tuple[int, ...]
    required_subgroup_1: tuple[int, ...]
    required_subgroup_2: tuple[int, ...]
    required_subgroup_3: tuple[int, ...]
    is_shutter_room: bool
    is_water_room: bool
    do_not_randomize: bool
    no_special_enemies_standard: bool


@dataclass(frozen=True)
class EnemyShuffleState:
    dungeon_rooms: dict[int, DungeonEnemyRoom]
    sprite_groups: dict[int, DungeonSpriteGroup]
    room_group_requirements: tuple[RoomGroupRequirement, ...]
    shutter_room_ids: frozenset[int]
    water_room_ids: frozenset[int]
    dont_randomize_room_ids: frozenset[int]
    no_special_enemies_standard_room_ids: frozenset[int]
    boss_room_ids: frozenset[int]


def generate_enemy_shuffle_state() -> EnemyShuffleState:
    rom_bytes = get_base_rom_bytes()
    moved_header_bank = _get_enemizer_symbol("moved_room_header_bank_value_address")
    metadata = _load_enemy_room_metadata()
    return EnemyShuffleState(
        dungeon_rooms={
            room.room_id: room
            for room in _read_dungeon_rooms(rom_bytes, moved_header_bank, metadata)
        },
        sprite_groups={
            group.group_id: group
            for group in _read_sprite_groups(rom_bytes)
        },
        room_group_requirements=metadata["room_requirements"],
        shutter_room_ids=metadata["shutter_room_ids"],
        water_room_ids=metadata["water_room_ids"],
        dont_randomize_room_ids=metadata["dont_randomize_room_ids"],
        no_special_enemies_standard_room_ids=metadata["no_special_enemies_standard_room_ids"],
        boss_room_ids=metadata["boss_room_ids"],
    )


def _read_dungeon_rooms(rom_bytes: bytes, moved_header_bank_address: int, metadata: dict[str, object]) -> list[DungeonEnemyRoom]:
    rooms: list[DungeonEnemyRoom] = []
    room_header_bank = rom_bytes[moved_header_bank_address]
    shutter_room_ids = metadata["shutter_room_ids"]
    water_room_ids = metadata["water_room_ids"]
    dont_randomize_room_ids = metadata["dont_randomize_room_ids"]
    no_special_enemies_standard_room_ids = metadata["no_special_enemies_standard_room_ids"]
    room_requirements = metadata["room_requirements"]

    for room_id in range(TOTAL_DUNGEON_ROOMS):
        room_header_address = _read_room_header_address(rom_bytes, room_id, room_header_bank)
        sprite_table_address = _read_room_sprite_table_address(rom_bytes, room_id)
        merged_requirement = _merge_room_requirements(room_id, room_requirements)
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
                required_group_id=merged_requirement.group_id,
                required_subgroup_0=merged_requirement.subgroup_0,
                required_subgroup_1=merged_requirement.subgroup_1,
                required_subgroup_2=merged_requirement.subgroup_2,
                required_subgroup_3=merged_requirement.subgroup_3,
                is_shutter_room=room_id in shutter_room_ids,
                is_water_room=room_id in water_room_ids,
                do_not_randomize=room_id in dont_randomize_room_ids,
                no_special_enemies_standard=room_id in no_special_enemies_standard_room_ids,
            )
        )

    return rooms


def _read_sprite_groups(rom_bytes: bytes) -> tuple[DungeonSpriteGroup, ...]:
    groups = []
    for group_id in range(TOTAL_SPRITE_GROUPS):
        groups.append(
            DungeonSpriteGroup(
                group_id=group_id,
                dungeon_group_id=group_id - 0x40,
                subgroup_0=rom_bytes[SPRITE_GROUP_BASE_ADDRESS + (group_id * 4)],
                subgroup_1=rom_bytes[SPRITE_GROUP_BASE_ADDRESS + (group_id * 4) + 1],
                subgroup_2=rom_bytes[SPRITE_GROUP_BASE_ADDRESS + (group_id * 4) + 2],
                subgroup_3=rom_bytes[SPRITE_GROUP_BASE_ADDRESS + (group_id * 4) + 3],
            )
        )
    return tuple(groups)


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


def _load_enemy_room_metadata() -> dict[str, object]:
    raw_metadata = pkgutil.get_data(__package__, "data/enemizer/enemy_room_metadata.json")
    if raw_metadata is None:
        raise FileNotFoundError("Missing vendored Enemizer enemy room metadata required by ALTTP enemy state generation")

    payload = json.loads(raw_metadata.decode("utf-8"))
    return {
        "shutter_room_ids": frozenset(payload["shutter_rooms"]),
        "water_room_ids": frozenset(payload["water_rooms"]),
        "dont_randomize_room_ids": frozenset(payload["dont_randomize_rooms"]),
        "no_special_enemies_standard_room_ids": frozenset(payload["no_special_enemies_standard_rooms"]),
        "boss_room_ids": frozenset(payload["boss_rooms"]),
        "room_requirements": tuple(
            RoomGroupRequirement(
                group_id=requirement["group_id"],
                subgroup_0=requirement["subgroup_0"],
                subgroup_1=requirement["subgroup_1"],
                subgroup_2=requirement["subgroup_2"],
                subgroup_3=requirement["subgroup_3"],
                rooms=tuple(requirement["rooms"]),
            )
            for requirement in payload["room_requirements"]
        ),
    }


@dataclass(frozen=True)
class MergedRoomRequirement:
    group_id: Optional[int]
    subgroup_0: tuple[int, ...]
    subgroup_1: tuple[int, ...]
    subgroup_2: tuple[int, ...]
    subgroup_3: tuple[int, ...]


def _merge_room_requirements(room_id: int, room_requirements: tuple[RoomGroupRequirement, ...]) -> MergedRoomRequirement:
    group_id: Optional[int] = None
    subgroup_0: list[int] = []
    subgroup_1: list[int] = []
    subgroup_2: list[int] = []
    subgroup_3: list[int] = []

    for requirement in room_requirements:
        if room_id not in requirement.rooms:
            continue
        if requirement.group_id is not None:
            group_id = requirement.group_id
        if requirement.subgroup_0 is not None:
            subgroup_0.append(requirement.subgroup_0)
        if requirement.subgroup_1 is not None:
            subgroup_1.append(requirement.subgroup_1)
        if requirement.subgroup_2 is not None:
            subgroup_2.append(requirement.subgroup_2)
        if requirement.subgroup_3 is not None:
            subgroup_3.append(requirement.subgroup_3)

    return MergedRoomRequirement(
        group_id=group_id,
        subgroup_0=tuple(subgroup_0),
        subgroup_1=tuple(subgroup_1),
        subgroup_2=tuple(subgroup_2),
        subgroup_3=tuple(subgroup_3),
    )
