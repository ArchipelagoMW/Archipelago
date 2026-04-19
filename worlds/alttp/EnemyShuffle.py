from __future__ import annotations

from dataclasses import dataclass
import json
import pkgutil
from typing import Optional, TYPE_CHECKING

from Utils import snes_to_pc

from .Rom import get_base_rom_bytes

if TYPE_CHECKING:
    from . import ALTTPWorld


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
STAL_SPRITE_ID = 0xD3

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
class EnemySpriteRequirement:
    sprite_name: str
    sprite_id: int
    boss: bool
    overlord: bool
    do_not_randomize: bool
    killable: bool
    npc: bool
    never_use_dungeon: bool
    never_use_overworld: bool
    cannot_have_key: bool
    is_object: bool
    absorbable: bool
    is_water_sprite: bool
    is_enemy_sprite: bool
    group_ids: tuple[int, ...]
    subgroup_0: tuple[int, ...]
    subgroup_1: tuple[int, ...]
    subgroup_2: tuple[int, ...]
    subgroup_3: tuple[int, ...]
    parameters: Optional[int]
    special_glitched: bool
    excluded_rooms: tuple[int, ...]
    dont_randomize_rooms: tuple[int, ...]
    spawnable_rooms: tuple[int, ...]


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
class RandomizedDungeonEnemySprite:
    address: int
    byte_0: int
    byte_1: int
    original_sprite_id: int
    sprite_id: int
    is_overlord: bool
    has_key: bool


@dataclass(frozen=True)
class RandomizedDungeonEnemyRoom:
    room_id: int
    room_header_address: int
    sprite_table_address: int
    original_graphics_block_id: int
    graphics_block_id: int
    tag_1: int
    tag_2: int
    sort_sprites_value: int
    sprites: tuple[RandomizedDungeonEnemySprite, ...]
    skipped_randomization: bool


@dataclass(frozen=True)
class EnemyShuffleState:
    dungeon_rooms: dict[int, DungeonEnemyRoom]
    sprite_groups: dict[int, DungeonSpriteGroup]
    sprite_requirements: tuple[EnemySpriteRequirement, ...]
    room_group_requirements: tuple[RoomGroupRequirement, ...]
    shutter_room_ids: frozenset[int]
    water_room_ids: frozenset[int]
    dont_randomize_room_ids: frozenset[int]
    no_special_enemies_standard_room_ids: frozenset[int]
    boss_room_ids: frozenset[int]
    randomized_dungeon_rooms: dict[int, RandomizedDungeonEnemyRoom]


def generate_enemy_shuffle_state(world: "ALTTPWorld") -> EnemyShuffleState:
    rom_bytes = get_base_rom_bytes()
    moved_header_bank = _get_enemizer_symbol("moved_room_header_bank_value_address")
    metadata = _load_enemy_room_metadata()
    sprite_requirements = _load_enemy_sprite_requirements()
    dungeon_rooms = {
        room.room_id: room
        for room in _read_dungeon_rooms(rom_bytes, moved_header_bank, metadata)
    }
    sprite_groups = {
        group.group_id: group
        for group in _read_sprite_groups(rom_bytes)
    }
    return EnemyShuffleState(
        dungeon_rooms=dungeon_rooms,
        sprite_groups=sprite_groups,
        sprite_requirements=sprite_requirements,
        room_group_requirements=metadata["room_requirements"],
        shutter_room_ids=metadata["shutter_room_ids"],
        water_room_ids=metadata["water_room_ids"],
        dont_randomize_room_ids=metadata["dont_randomize_room_ids"],
        no_special_enemies_standard_room_ids=metadata["no_special_enemies_standard_room_ids"],
        boss_room_ids=metadata["boss_room_ids"],
        randomized_dungeon_rooms=_randomize_dungeon_rooms(
            world,
            dungeon_rooms,
            sprite_groups,
            sprite_requirements,
        ),
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


def _load_enemy_sprite_requirements() -> tuple[EnemySpriteRequirement, ...]:
    raw_metadata = pkgutil.get_data(__package__, "data/enemizer/enemy_sprite_requirements.json")
    if raw_metadata is None:
        raise FileNotFoundError("Missing vendored Enemizer enemy sprite metadata required by ALTTP enemy state generation")

    payload = json.loads(raw_metadata.decode("utf-8"))
    return tuple(
        EnemySpriteRequirement(
            sprite_name=entry["sprite_name"],
            sprite_id=entry["sprite_id"],
            boss=entry["boss"],
            overlord=entry["overlord"],
            do_not_randomize=entry["do_not_randomize"],
            killable=entry["killable"],
            npc=entry["npc"],
            never_use_dungeon=entry["never_use_dungeon"],
            never_use_overworld=entry["never_use_overworld"],
            cannot_have_key=entry["cannot_have_key"],
            is_object=entry["is_object"],
            absorbable=entry["absorbable"],
            is_water_sprite=entry["is_water_sprite"],
            is_enemy_sprite=entry["is_enemy_sprite"],
            group_ids=tuple(entry["group_ids"]),
            subgroup_0=tuple(entry["subgroup_0"]),
            subgroup_1=tuple(entry["subgroup_1"]),
            subgroup_2=tuple(entry["subgroup_2"]),
            subgroup_3=tuple(entry["subgroup_3"]),
            parameters=entry["parameters"],
            special_glitched=entry["special_glitched"],
            excluded_rooms=tuple(entry["excluded_rooms"]),
            dont_randomize_rooms=tuple(entry["dont_randomize_rooms"]),
            spawnable_rooms=tuple(entry["spawnable_rooms"]),
        )
        for entry in payload["requirements"]
    )


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


def get_room_do_not_update_requirements(state: EnemyShuffleState, room: DungeonEnemyRoom) -> tuple[EnemySpriteRequirement, ...]:
    room_sprite_ids = {sprite.sprite_id for sprite in room.sprites}
    return tuple(
        requirement for requirement in state.sprite_requirements
        if requirement.do_not_randomize
        and requirement.sprite_id in room_sprite_ids
        and can_spawn_in_room(requirement, room)
    )


def get_possible_dungeon_sprite_groups(state: EnemyShuffleState, room: DungeonEnemyRoom) -> tuple[DungeonSpriteGroup, ...]:
    do_not_update = get_room_do_not_update_requirements(state, room)
    usable_groups = tuple(group for group in state.sprite_groups.values() if 0 < group.dungeon_group_id < 60)
    needs_key = any(sprite.has_key for sprite in room.sprites)
    needs_killable = room.is_shutter_room
    needs_water = room.is_water_room
    room_requirements = _get_requirements_for_usable_dungeon_enemies(state)
    water_requirements = tuple(requirement for requirement in room_requirements if requirement.is_water_sprite)
    killable_requirements = tuple(
        requirement for requirement in state.sprite_requirements
        if requirement.killable and requirement.sprite_id != STAL_SPRITE_ID
    )
    key_requirements = tuple(requirement for requirement in killable_requirements if not requirement.cannot_have_key)

    if (
        not needs_key and not needs_killable and not needs_water
        and not do_not_update
        and room.required_group_id is None
        and not room.required_subgroup_0
        and not room.required_subgroup_1
        and not room.required_subgroup_2
        and not room.required_subgroup_3
    ):
        return _get_unconstrained_possible_dungeon_sprite_groups(usable_groups, room_requirements, water_requirements)

    do_not_update_matcher = _build_requirement_group_matcher(do_not_update)
    killable_matcher = _build_requirement_group_matcher(killable_requirements)
    key_matcher = _build_requirement_group_matcher(key_requirements)
    water_matcher = _build_requirement_group_matcher(water_requirements)

    return tuple(
        group for group in usable_groups
        if do_not_update_matcher(group)
        and _group_matches_room_requirement(group, room)
        and (not needs_killable or killable_matcher(group))
        and (not needs_key or key_matcher(group))
        and (not needs_water or water_matcher(group))
    )


def can_spawn_in_room(requirement: EnemySpriteRequirement, room: DungeonEnemyRoom) -> bool:
    return (
        room.room_id not in requirement.excluded_rooms
        and (not requirement.spawnable_rooms or room.room_id in requirement.spawnable_rooms)
        and (requirement.sprite_id != WALLMASTER_SPRITE_ID or room.room_id < 0x100)
    )


def _get_requirements_for_usable_dungeon_enemies(state: EnemyShuffleState) -> tuple[EnemySpriteRequirement, ...]:
    return tuple(
        requirement for requirement in state.sprite_requirements
        if not requirement.npc
        and requirement.is_enemy_sprite
        and not requirement.boss
        and not requirement.overlord
        and not requirement.is_object
        and not requirement.never_use_dungeon
    )


def _get_unconstrained_possible_dungeon_sprite_groups(
    usable_groups: tuple[DungeonSpriteGroup, ...],
    room_requirements: tuple[EnemySpriteRequirement, ...],
    water_requirements: tuple[EnemySpriteRequirement, ...],
) -> tuple[DungeonSpriteGroup, ...]:
    water_subgroup_3 = set(_flatten_requirement_values(water_requirements, "subgroup_3"))
    included_group_ids = set(_flatten_requirement_values(room_requirements, "group_ids"))
    included_subgroup_0 = set(_flatten_requirement_values(room_requirements, "subgroup_0"))
    included_subgroup_1 = set(_flatten_requirement_values(room_requirements, "subgroup_1"))
    included_subgroup_2 = set(_flatten_requirement_values(room_requirements, "subgroup_2"))
    included_subgroup_3 = {
        subgroup for subgroup in _flatten_requirement_values(room_requirements, "subgroup_3")
        if subgroup not in water_subgroup_3 and subgroup not in {54, 80}
    }

    return tuple(
        group for group in usable_groups
        if group.group_id in included_group_ids
        or group.subgroup_0 in included_subgroup_0
        or group.subgroup_1 in included_subgroup_1
        or group.subgroup_2 in included_subgroup_2
        or group.subgroup_3 in included_subgroup_3
    )


def _build_requirement_group_matcher(requirements: tuple[EnemySpriteRequirement, ...]):
    allowed_group_ids = set(_flatten_requirement_values(requirements, "group_ids"))
    allowed_subgroup_0 = set(_flatten_requirement_values(requirements, "subgroup_0"))
    allowed_subgroup_1 = set(_flatten_requirement_values(requirements, "subgroup_1"))
    allowed_subgroup_2 = set(_flatten_requirement_values(requirements, "subgroup_2"))
    allowed_subgroup_3 = set(_flatten_requirement_values(requirements, "subgroup_3"))

    def matches(group: DungeonSpriteGroup) -> bool:
        return (
            not allowed_group_ids or group.group_id in allowed_group_ids
        ) and (
            not allowed_subgroup_0 or group.subgroup_0 in allowed_subgroup_0
        ) and (
            not allowed_subgroup_1 or group.subgroup_1 in allowed_subgroup_1
        ) and (
            not allowed_subgroup_2 or group.subgroup_2 in allowed_subgroup_2
        ) and (
            not allowed_subgroup_3 or group.subgroup_3 in allowed_subgroup_3
        )

    return matches


def _flatten_requirement_values(requirements: tuple[EnemySpriteRequirement, ...], attribute: str) -> tuple[int, ...]:
    return tuple(
        value
        for requirement in requirements
        for value in getattr(requirement, attribute)
    )


def _group_matches_room_requirement(group: DungeonSpriteGroup, room: DungeonEnemyRoom) -> bool:
    return (
        (room.required_group_id is None or room.required_group_id == group.dungeon_group_id)
        and (not room.required_subgroup_0 or group.subgroup_0 in room.required_subgroup_0)
        and (not room.required_subgroup_1 or group.subgroup_1 in room.required_subgroup_1)
        and (not room.required_subgroup_2 or group.subgroup_2 in room.required_subgroup_2)
        and (not room.required_subgroup_3 or group.subgroup_3 in room.required_subgroup_3)
    )
def _get_possible_enemy_requirements_for_group(
    state: EnemyShuffleState,
    room: DungeonEnemyRoom,
    group: DungeonSpriteGroup,
) -> tuple[EnemySpriteRequirement, ...]:
    dungeon_requirements = _get_requirements_for_usable_dungeon_enemies(state)
    return tuple(
        requirement for requirement in dungeon_requirements
        if can_spawn_in_room(requirement, room)
        and (
            not requirement.group_ids or group.dungeon_group_id in requirement.group_ids
        )
        and (not requirement.subgroup_0 or group.subgroup_0 in requirement.subgroup_0)
        and (not requirement.subgroup_1 or group.subgroup_1 in requirement.subgroup_1)
        and (not requirement.subgroup_2 or group.subgroup_2 in requirement.subgroup_2)
        and (not requirement.subgroup_3 or group.subgroup_3 in requirement.subgroup_3)
    )


def _get_randomizable_sprites_in_room(
    state: EnemyShuffleState,
    room: DungeonEnemyRoom,
) -> tuple[DungeonEnemySprite, ...]:
    randomizable_sprite_ids = {
        requirement.sprite_id for requirement in state.sprite_requirements
        if not requirement.do_not_randomize
    }
    return tuple(sprite for sprite in room.sprites if sprite.sprite_id in randomizable_sprite_ids)


def _randomize_dungeon_rooms(
    world: "ALTTPWorld",
    dungeon_rooms: dict[int, DungeonEnemyRoom],
    sprite_groups: dict[int, DungeonSpriteGroup],
    sprite_requirements: tuple[EnemySpriteRequirement, ...],
) -> dict[int, RandomizedDungeonEnemyRoom]:
    state = EnemyShuffleState(
        dungeon_rooms=dungeon_rooms,
        sprite_groups=sprite_groups,
        sprite_requirements=sprite_requirements,
        room_group_requirements=tuple(),
        shutter_room_ids=frozenset(room.room_id for room in dungeon_rooms.values() if room.is_shutter_room),
        water_room_ids=frozenset(room.room_id for room in dungeon_rooms.values() if room.is_water_room),
        dont_randomize_room_ids=frozenset(room.room_id for room in dungeon_rooms.values() if room.do_not_randomize),
        no_special_enemies_standard_room_ids=frozenset(
            room.room_id for room in dungeon_rooms.values() if room.no_special_enemies_standard
        ),
        boss_room_ids=boss_room_ids,
        randomized_dungeon_rooms={},
    )
    randomized_rooms: dict[int, RandomizedDungeonEnemyRoom] = {}

    for room_id in sorted(dungeon_rooms):
        room = dungeon_rooms[room_id]
        skip_randomization = room.do_not_randomize or (
            world.options.mode == "standard" and room.no_special_enemies_standard
        )

        selected_group = sprite_groups.get(room.graphics_block_id + 0x40)
        if not skip_randomization:
            possible_groups = get_possible_dungeon_sprite_groups(state, room)
            if possible_groups:
                selected_group = world.random.choice(possible_groups)

        if selected_group is None:
            selected_group = sprite_groups[room.graphics_block_id + 0x40]

        randomized_rooms[room_id] = _randomize_room_sprites(
            world,
            state,
            room,
            selected_group,
            skip_randomization,
        )

    return randomized_rooms


def _randomize_room_sprites(
    world: "ALTTPWorld",
    state: EnemyShuffleState,
    room: DungeonEnemyRoom,
    selected_group: DungeonSpriteGroup,
    skip_randomization: bool,
) -> RandomizedDungeonEnemyRoom:
    randomized_sprites = list(_clone_room_sprites(room))

    if not skip_randomization:
        possible_requirements = _get_possible_enemy_requirements_for_group(state, room, selected_group)
        possible_sprite_ids = [requirement.sprite_id for requirement in possible_requirements]
        sprites_to_update = _get_randomizable_sprites_in_room(state, room)
        sprites_to_update_addresses = {sprite.address for sprite in sprites_to_update}

        if possible_sprite_ids:
            killable_sprite_ids = [
                requirement.sprite_id for requirement in possible_requirements
                if requirement.killable and requirement.sprite_id != STAL_SPRITE_ID
            ]
            killable_key_sprite_ids = [
                requirement.sprite_id for requirement in possible_requirements
                if requirement.killable and not requirement.cannot_have_key and requirement.sprite_id != STAL_SPRITE_ID
            ]
            water_sprite_ids = [
                requirement.sprite_id for requirement in possible_requirements
                if requirement.is_water_sprite
            ]

            if room.is_water_room:
                if water_sprite_ids:
                    for sprite in randomized_sprites:
                        if sprite.address in sprites_to_update_addresses:
                            _set_randomized_sprite_id(randomized_sprites, sprite.address, world.random.choice(water_sprite_ids))
                return _build_randomized_room(room, selected_group, randomized_sprites, False)

            possible_sprite_ids = [sprite_id for sprite_id in possible_sprite_ids if sprite_id not in water_sprite_ids]
            if not possible_sprite_ids:
                return _build_randomized_room(room, selected_group, randomized_sprites, False)
            stal_count = 0

            for sprite in sprites_to_update:
                replacement_sprite_id: int
                if not room.is_shutter_room and world.random.randrange(100) < 5:
                    replacement_sprite_id = STAL_SPRITE_ID
                else:
                    replacement_sprite_id = world.random.choice(possible_sprite_ids)

                _set_randomized_sprite_id(randomized_sprites, sprite.address, replacement_sprite_id)

                if replacement_sprite_id == STAL_SPRITE_ID:
                    stal_count += 1
                    if stal_count > 2:
                        possible_sprite_ids = [sprite_id for sprite_id in possible_sprite_ids if sprite_id != STAL_SPRITE_ID]

            for sprite in (candidate for candidate in sprites_to_update if candidate.has_key):
                if killable_key_sprite_ids:
                    _set_randomized_sprite_id(randomized_sprites, sprite.address, world.random.choice(killable_key_sprite_ids))

            if room.is_shutter_room:
                for sprite in (candidate for candidate in sprites_to_update if not candidate.has_key):
                    if killable_sprite_ids:
                        _set_randomized_sprite_id(randomized_sprites, sprite.address, world.random.choice(killable_sprite_ids))

    return _build_randomized_room(room, selected_group, randomized_sprites, skip_randomization)


def _clone_room_sprites(room: DungeonEnemyRoom) -> list[RandomizedDungeonEnemySprite]:
    return [
        RandomizedDungeonEnemySprite(
            address=sprite.address,
            byte_0=sprite.byte_0,
            byte_1=sprite.byte_1,
            original_sprite_id=sprite.sprite_id,
            sprite_id=sprite.sprite_id,
            is_overlord=sprite.is_overlord,
            has_key=sprite.has_key,
        )
        for sprite in room.sprites
    ]


def _set_randomized_sprite_id(
    randomized_sprites: list[RandomizedDungeonEnemySprite],
    address: int,
    sprite_id: int,
) -> None:
    for index, sprite in enumerate(randomized_sprites):
        if sprite.address != address:
            continue
        randomized_sprites[index] = RandomizedDungeonEnemySprite(
            address=sprite.address,
            byte_0=sprite.byte_0,
            byte_1=sprite.byte_1,
            original_sprite_id=sprite.original_sprite_id,
            sprite_id=sprite_id,
            is_overlord=sprite.is_overlord,
            has_key=sprite.has_key,
        )
        return


def _build_randomized_room(
    room: DungeonEnemyRoom,
    selected_group: DungeonSpriteGroup,
    sprites: list[RandomizedDungeonEnemySprite],
    skipped_randomization: bool,
) -> RandomizedDungeonEnemyRoom:
    return RandomizedDungeonEnemyRoom(
        room_id=room.room_id,
        room_header_address=room.room_header_address,
        sprite_table_address=room.sprite_table_address,
        original_graphics_block_id=room.graphics_block_id,
        graphics_block_id=selected_group.dungeon_group_id,
        tag_1=room.tag_1,
        tag_2=room.tag_2,
        sort_sprites_value=room.sort_sprites_value,
        sprites=tuple(sprites),
        skipped_randomization=skipped_randomization,
    )
