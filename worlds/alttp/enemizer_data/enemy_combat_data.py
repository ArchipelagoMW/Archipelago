from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple


DAMAGE_SOURCE_TABLE_ADDRESS = 0x06B8F1
DAMAGE_SOURCE_TABLE_SIZE = 0x80
ENEMY_HP_TABLE_ADDRESS = 0x06B173
ENEMY_HEALTH_TABLE_SIZE = 0xF3
SPRITE_DAMAGE_SUBCLASS_TABLE_SNES_ADDRESS = 0x31C800
SPRITE_DAMAGE_SUBCLASS_TABLE_SIZE = 0x800
REACHABLE_SPRITE_DAMAGE_SUBCLASS_COUNT = 0xD8
MOTHULA_SPRITE_ID = 0x88
THIEF_SPRITE_ID = 0xC4
THIEF_DEFAULT_HP = 4
YELLOW_SLIME_SPRITE_ID = 0x8F
FAIRY_TRANSFORM_EFFECT = 0xF9
BLOB_TRANSFORM_EFFECT = 0xFA
STUN_32_FRAMES_EFFECT = 0xFB
STUN_128_FRAMES_EFFECT = 0xFC
INCINERATE_EFFECT = 0xFD
FREEZE_EFFECT = 0xFE
STUN_255_FRAMES_EFFECT = 0xFF
FIGHTER_SWORD_DAMAGE_CLASSES = frozenset((1, 2))
MASTER_SWORD_DAMAGE_CLASSES = frozenset((1, 2, 3))
TEMPERED_SWORD_DAMAGE_CLASSES = frozenset((2, 3, 4))
GOLDEN_SWORD_DAMAGE_CLASSES = frozenset((3, 4, 5))
KEY_DROP_KILL_DAMAGE_CLASS_OVERRIDES = {
    "RedBariSprite": (11, 13),
}
EXCLUDED_ENEMY_TABLE_SPRITE_IDS = frozenset({
    0x09, 0x53, 0x54, 0x70, 0x7A, 0x7B, 0x88, 0x89, 0x8C, 0x8D, 0x92,
    0xA2, 0xA3, 0xA4, 0xBD, 0xBE, 0xBF, 0xCB, 0xCC, 0xCD, 0xCE, 0xD6, 0xD7,
})
ENEMY_HEALTH_RANGE_BY_KEY = {
    "easy": (1, 4),
    "normal": (2, 15),
    "hard": (2, 25),
    "expert": (4, 50),
}
VANILLA_ENEMY_HEALTH = bytes.fromhex(
    "0c06ff0303030303020c04ff00030c020014040400ff00020308000000000000"
    "08030802020003ff0003030303030303030003000303030003000000000302ff"
    "02060408060806040808080404020202ff08ff30100808ff020000ffffffffff"
    "ffffffff0404ffffffff100300020401ff04ff00000000ff000060ff18ffffff"
    "0304ff10080800ff2020202020080804084030ff02ffffffff10040204040808"
    "081040400804080404080c1000000000000000000000000000000000008030ff"
    "ffffff08000000200008052828285a10184000040000ffff0000000000000000"
    "00000000000000000000000000000000000000"
)


class CombatDeliveryOverride(NamedTuple):
    items: tuple[str, ...]
    abilities: tuple[str, ...] = tuple()


DIRECT_KILL_DELIVERY_OVERRIDES = {
    # Damage class 1 includes both safe Cane hits and unsafe sword contact shocks.
    "BuzzblobSprite": CombatDeliveryOverride(
        ("Cane of Somaria", "Cane of Byrna", "Golden Sword", "Bow", "Silver Bow", "Fire Rod", "Bombos"),
        ("bombs",),
    ),
    # Most positive table hits only knock both actors back; only stun/contact tools are logical.
    "FloatingStalfosHeadSprite": CombatDeliveryOverride(
        ("Blue Boomerang", "Red Boomerang", "Cane of Somaria", "Cane of Byrna"),
    ),
}


def _build_yellow_slime_follow_up_override(
    *,
    boomerangs: bool = False,
    hookshot: bool = False,
    fire_rod: bool = True,
    ice_rod: bool = True,
    ether: bool = True,
) -> CombatDeliveryOverride:
    items: list[str] = []
    if boomerangs:
        items.extend(("Blue Boomerang", "Red Boomerang"))
    items.extend(
        (
            "Cane of Somaria",
            "Cane of Byrna",
            "Fighter Sword",
            "Master Sword",
            "Hammer",
            "Tempered Sword",
            "Golden Sword",
            "Bow",
        )
    )
    if hookshot:
        items.append("Hookshot")
    items.append("Silver Bow")
    if fire_rod:
        items.append("Fire Rod")
    if ice_rod:
        items.append("Ice Rod")
    items.append("Bombos")
    if ether:
        items.append("Ether")
    return CombatDeliveryOverride(tuple(items), ("bombs",))


# Blob-transform damage classes come from the ROM damage tables. These overrides
# only describe the logical follow-up tools needed to finish the spawned yellow slime.
YELLOW_SLIME_FOLLOW_UP_DELIVERY_OVERRIDES = {
    8: _build_yellow_slime_follow_up_override(),
    10: _build_yellow_slime_follow_up_override(),
    13: _build_yellow_slime_follow_up_override(hookshot=True, ice_rod=False, ether=False),
    14: _build_yellow_slime_follow_up_override(),
    17: _build_yellow_slime_follow_up_override(boomerangs=True),
    18: _build_yellow_slime_follow_up_override(),
    19: _build_yellow_slime_follow_up_override(fire_rod=False, ice_rod=False),
    23: _build_yellow_slime_follow_up_override(boomerangs=True),
    34: _build_yellow_slime_follow_up_override(),
    39: _build_yellow_slime_follow_up_override(hookshot=True, ice_rod=False, ether=False),
    65: _build_yellow_slime_follow_up_override(),
    66: _build_yellow_slime_follow_up_override(),
    67: _build_yellow_slime_follow_up_override(ice_rod=False),
    68: _build_yellow_slime_follow_up_override(ice_rod=False),
    69: _build_yellow_slime_follow_up_override(ice_rod=False),
    70: _build_yellow_slime_follow_up_override(),
    71: _build_yellow_slime_follow_up_override(),
    72: _build_yellow_slime_follow_up_override(ice_rod=False),
    73: _build_yellow_slime_follow_up_override(ice_rod=False),
    74: _build_yellow_slime_follow_up_override(),
    75: _build_yellow_slime_follow_up_override(),
    78: _build_yellow_slime_follow_up_override(hookshot=True),
    79: _build_yellow_slime_follow_up_override(hookshot=True),
    88: _build_yellow_slime_follow_up_override(),
    106: _build_yellow_slime_follow_up_override(boomerangs=True, ice_rod=False),
    109: _build_yellow_slime_follow_up_override(hookshot=True),
    110: _build_yellow_slime_follow_up_override(hookshot=True),
    167: _build_yellow_slime_follow_up_override(boomerangs=True),
    201: _build_yellow_slime_follow_up_override(boomerangs=True),
}


class DamageSource(NamedTuple):
    name: str
    damage_class: int
    subclasses: tuple[int, ...]


@dataclass(frozen=True)
class EnemyCombatModel:
    damage_sources: tuple[DamageSource, ...]
    sprite_damage_subclasses: tuple[tuple[int, ...], ...]
    enemy_health_table: bytes


DAMAGE_SOURCES: tuple[DamageSource, ...] = (
    DamageSource('Boomerang', 0x00, (0x00, 0x01, 0x20, 0xFF, 0xFC, 0xFB, 0x00, 0x00)),
    DamageSource('Damage Class 1', 0x01, (0x00, 0x02, 0x40, 0x04, 0x00, 0x00, 0x00, 0x00)),
    DamageSource('Damage Class 2', 0x02, (0x00, 0x04, 0x40, 0x02, 0x03, 0x00, 0x00, 0x00)),
    DamageSource('Damage Class 3', 0x03, (0x00, 0x08, 0x40, 0x04, 0x00, 0x00, 0x00, 0x00)),
    DamageSource('Damage Class 4', 0x04, (0x00, 0x10, 0x40, 0x08, 0x00, 0x00, 0x00, 0x00)),
    DamageSource('Damage Class 5', 0x05, (0x00, 0x10, 0x40, 0x08, 0x00, 0x00, 0x00, 0x00)),
    DamageSource('Arrow', 0x06, (0x00, 0x04, 0x40, 0x10, 0x00, 0x00, 0x00, 0x00)),
    DamageSource('Hookshot', 0x07, (0x00, 0xFF, 0x40, 0xFF, 0xFC, 0xFB, 0x00, 0x00)),
    DamageSource('Bomb', 0x08, (0x00, 0x04, 0x40, 0xFF, 0xFC, 0xFB, 0x20, 0x00)),
    DamageSource('SilverArrow', 0x09, (0x00, 0x64, 0x18, 0x64, 0x00, 0x00, 0x00, 0x00)),
    DamageSource('Powder', 0x0A, (0x00, 0xF9, 0xFA, 0xFF, 0x64, 0x00, 0x00, 0x00)),
    DamageSource('FireRod', 0x0B, (0x00, 0x08, 0x40, 0xFD, 0x04, 0x10, 0x00, 0x00)),
    DamageSource('IceRod', 0x0C, (0x00, 0x08, 0x40, 0xFE, 0x04, 0x00, 0x00, 0x00)),
    DamageSource('Bombos', 0x0D, (0x00, 0x10, 0x40, 0xFD, 0x00, 0x00, 0x00, 0x00)),
    DamageSource('Ether', 0x0E, (0x00, 0xFE, 0x40, 0x10, 0x00, 0x00, 0x00, 0x00)),
    DamageSource('Quake', 0x0F, (0x00, 0x20, 0x40, 0xFF, 0x00, 0x00, 0x00, 0xFA)),
)


# Sprite damage subclasses are indexed by sprite id, then damage class.
# Each value selects one entry from the matching row in DAMAGE_SOURCES.
# This table is vanilla JP 1.0 through sprite 0xD7, with Mothula (0x88)
# damage classes 4 and 5 changed from subclass 0 to subclass 1 so the
# Gold Sword uses the same 16-damage behavior as the GBA release.
SPRITE_DAMAGE_SUBCLASSES: tuple[tuple[int, ...], ...] = (
    (1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 3, 1, 3, 1, 1),  # 0x00
    (1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 3, 1, 3, 1, 1),  # 0x01
    (1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x02
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x03
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x04
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x05
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x06
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x07
    (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 3, 3, 1, 7),  # 0x08
    (0, 1, 3, 3, 3, 3, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0),  # 0x09
    (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 3, 3, 1, 7),  # 0x0A
    (1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 0, 0, 0),  # 0x0B
    (1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 3, 1),  # 0x0C
    (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 1, 3),  # 0x0D
    (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 3, 3, 2, 7),  # 0x0E
    (1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 3, 1, 3, 3, 2),  # 0x0F
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 3, 1),  # 0x10
    (4, 1, 1, 1, 1, 2, 1, 0, 2, 1, 0, 1, 3, 3, 1, 7),  # 0x11
    (3, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 3, 3, 3, 1, 7),  # 0x12
    (0, 1, 1, 1, 1, 1, 1, 3, 2, 3, 2, 0, 0, 3, 2, 7),  # 0x13
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x14
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0),  # 0x15
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x16
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 7),  # 0x17
    (0, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 3, 1, 3, 3, 7),  # 0x18
    (1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 0, 1, 1, 3, 2, 3),  # 0x19
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x1A
    (2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 3, 2),  # 0x1B
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x1C
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x1D
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x1E
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x1F
    (3, 1, 1, 1, 1, 1, 1, 1, 0, 1, 2, 3, 3, 3, 1, 7),  # 0x20
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x21
    (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 3, 3, 2, 7),  # 0x22
    (0, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 3, 2, 3, 2, 3),  # 0x23
    (0, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 3, 2, 3, 2, 3),  # 0x24
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x25
    (0, 1, 1, 1, 1, 1, 0, 3, 3, 1, 0, 0, 0, 3, 1, 3),  # 0x26
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 7),  # 0x27
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x28
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x29
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0),  # 0x2A
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x2B
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x2C
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x2D
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x2E
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x2F
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x30
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x31
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x32
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x33
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x34
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x35
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x36
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x37
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x38
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x39
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x3A
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x3B
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x3C
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x3D
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 2, 7),  # 0x3E
    (0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1),  # 0x3F
    (0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x40
    (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 3, 1, 3, 1, 7),  # 0x41
    (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 3, 3, 1, 7),  # 0x42
    (3, 1, 4, 3, 1, 1, 1, 1, 1, 1, 0, 3, 0, 3, 1, 7),  # 0x43
    (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 3, 0, 3, 1, 7),  # 0x44
    (3, 1, 4, 3, 1, 1, 1, 1, 1, 1, 0, 3, 0, 3, 1, 7),  # 0x45
    (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 3, 3, 3, 1, 7),  # 0x46
    (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 3, 1, 3, 2, 7),  # 0x47
    (3, 1, 4, 3, 1, 1, 1, 1, 1, 1, 0, 3, 0, 3, 1, 7),  # 0x48
    (3, 1, 4, 3, 1, 1, 1, 1, 1, 1, 0, 3, 0, 3, 2, 7),  # 0x49
    (3, 1, 4, 3, 1, 1, 1, 1, 1, 1, 0, 3, 3, 3, 1, 7),  # 0x4A
    (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 3, 3, 1, 7),  # 0x4B
    (1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 0, 1, 1, 3, 3, 3),  # 0x4C
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 3, 2, 3, 2, 3),  # 0x4D
    (3, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 3, 3, 3, 1, 7),  # 0x4E
    (3, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 3, 3, 3, 1, 7),  # 0x4F
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x50
    (3, 1, 1, 1, 1, 1, 2, 1, 1, 1, 0, 1, 3, 3, 3, 3),  # 0x51
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x52
    (1, 3, 3, 3, 3, 3, 3, 0, 1, 1, 0, 1, 1, 0, 0, 0),  # 0x53
    (0, 1, 3, 3, 3, 3, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0),  # 0x54
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 3, 1, 3, 2, 1),  # 0x55
    (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 3, 1, 3, 2, 1),  # 0x56
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x57
    (3, 1, 1, 1, 1, 1, 1, 3, 1, 1, 2, 1, 3, 3, 1, 7),  # 0x58
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x59
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x5A
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 3),  # 0x5B
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 3),  # 0x5C
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x5D
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x5E
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x5F
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x60
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x61
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x62
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x63
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 3, 3, 3),  # 0x64
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x65
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x66
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x67
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x68
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x69
    (5, 1, 3, 1, 1, 1, 1, 1, 1, 1, 0, 3, 0, 3, 1, 7),  # 0x6A
    (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1),  # 0x6B
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x6C
    (3, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 3, 3, 3, 1, 7),  # 0x6D
    (3, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 3, 3, 3, 1, 7),  # 0x6E
    (1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 3, 3, 3, 1, 3),  # 0x6F
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x70
    (3, 1, 1, 1, 1, 1, 1, 3, 1, 1, 0, 3, 3, 3, 1, 3),  # 0x71
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x72
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x73
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x74
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x75
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x76
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x77
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x78
    (1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 3, 1),  # 0x79
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x7A
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x7B
    (0, 1, 1, 1, 1, 1, 1, 0, 2, 1, 0, 3, 3, 3, 3, 3),  # 0x7C
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x7D
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x7E
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x7F
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x80
    (0, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 3, 3, 2, 3, 2),  # 0x81
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x82
    (0, 1, 1, 2, 2, 1, 2, 0, 1, 2, 0, 0, 0, 0, 0, 0),  # 0x83
    (0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0),  # 0x84
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 2, 3, 2, 3),  # 0x85
    (0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 3, 3, 1, 7),  # 0x86
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x87
    (0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0),  # 0x88
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x89
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x8A
    (3, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 3, 3, 3, 2, 3),  # 0x8B
    (0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0),  # 0x8C
    (0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0),  # 0x8D
    (1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0, 1, 3, 2, 2, 3),  # 0x8E
    (3, 1, 1, 1, 1, 1, 1, 2, 2, 1, 0, 3, 3, 3, 1, 2),  # 0x8F
    (1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 3, 3, 2),  # 0x90
    (1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x91
    (0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0),  # 0x92
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x93
    (1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 3, 1, 3, 2, 3),  # 0x94
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x95
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x96
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x97
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x98
    (1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 0, 1, 0, 3, 1, 2),  # 0x99
    (1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 2, 3, 2, 1, 1),  # 0x9A
    (0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 2, 3, 2),  # 0x9B
    (0, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 3, 2, 3, 2, 2),  # 0x9C
    (0, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 3, 2, 3, 2, 2),  # 0x9D
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x9E
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x9F
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xA0
    (0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0),  # 0xA1
    (0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0),  # 0xA2
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0),  # 0xA3
    (0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 3, 0, 1, 3, 1),  # 0xA4
    (3, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0, 3, 3, 3, 1, 3),  # 0xA5
    (3, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0, 3, 3, 3, 1, 3),  # 0xA6
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 3, 2, 7),  # 0xA7
    (0, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 3, 3, 3, 1, 1),  # 0xA8
    (0, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 3, 3, 3, 1, 1),  # 0xA9
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 3, 1, 3, 1, 3),  # 0xAA
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0),  # 0xAB
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xAC
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xAD
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xAE
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xAF
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xB0
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xB1
    (1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 3, 1),  # 0xB2
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xB3
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xB4
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xB5
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xB6
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xB7
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xB8
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xB9
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xBA
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xBB
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xBC
    (0, 0, 1, 1, 1, 1, 3, 0, 1, 1, 0, 0, 0, 0, 0, 0),  # 0xBD
    (0, 0, 1, 1, 1, 1, 3, 0, 1, 1, 0, 0, 0, 0, 0, 0),  # 0xBE
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xBF
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xC0
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xC1
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xC2
    (0, 1, 1, 1, 1, 1, 3, 0, 1, 1, 0, 0, 0, 0, 0, 0),  # 0xC3
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xC4
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 1),  # 0xC5
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 1),  # 0xC6
    (0, 1, 1, 1, 1, 1, 1, 0, 1, 2, 0, 3, 1, 3, 1, 3),  # 0xC7
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xC8
    (5, 1, 1, 1, 1, 1, 3, 0, 2, 1, 0, 3, 3, 1, 3, 1),  # 0xC9
    (5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xCA
    (0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xCB
    (0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0),  # 0xCC
    (0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0),  # 0xCD
    (0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xCE
    (1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 2, 1),  # 0xCF
    (0, 0, 0, 1, 1, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0),  # 0xD0
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2, 2, 2),  # 0xD1
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 7),  # 0xD2
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 7),  # 0xD3
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xD4
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xD5
    (0, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xD6
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0),  # 0xD7
)


VANILLA_COMBAT_MODEL = EnemyCombatModel(
    damage_sources=DAMAGE_SOURCES,
    sprite_damage_subclasses=SPRITE_DAMAGE_SUBCLASSES,
    enemy_health_table=VANILLA_ENEMY_HEALTH,
)


def build_damage_source_table_bytes(damage_sources: tuple[DamageSource, ...] = DAMAGE_SOURCES) -> bytes:
    if len(damage_sources) != 16:
        raise ValueError(f"Expected 16 damage sources, got {len(damage_sources)}")

    output = bytearray()
    for expected_class, source in enumerate(damage_sources):
        if source.damage_class != expected_class:
            raise ValueError(f"Damage source {source.name} has class {source.damage_class}, expected {expected_class}")
        if len(source.subclasses) != 8:
            raise ValueError(f"Damage source {source.name} has {len(source.subclasses)} subclasses, expected 8")
        output.extend(source.subclasses)

    return bytes(output)


def build_packed_sprite_damage_subclass_table(
    subclass_table: tuple[tuple[int, ...], ...] = SPRITE_DAMAGE_SUBCLASSES,
    table_size: int = SPRITE_DAMAGE_SUBCLASS_TABLE_SIZE,
) -> bytes:
    if len(subclass_table) > table_size // 8:
        raise ValueError(f"Sprite subclass table has {len(subclass_table)} rows, but only {table_size // 8} fit")

    output = bytearray()
    for sprite_id, row in enumerate(subclass_table):
        if len(row) != 16:
            raise ValueError(f"Sprite 0x{sprite_id:02X} has {len(row)} subclasses, expected 16")
        for index in range(0, 16, 2):
            upper = row[index]
            lower = row[index + 1]
            if not 0 <= upper <= 0x0F or not 0 <= lower <= 0x0F:
                raise ValueError(f"Sprite 0x{sprite_id:02X} has subclass outside nibble range")
            output.append((upper << 4) | lower)

    output.extend(b"\x00" * (table_size - len(output)))
    return bytes(output)


def get_damage_effect(
    sprite_id: int,
    damage_class: int,
    combat_model: EnemyCombatModel = VANILLA_COMBAT_MODEL,
) -> int:
    subclass = combat_model.sprite_damage_subclasses[sprite_id][damage_class]
    return combat_model.damage_sources[damage_class].subclasses[subclass]


def is_killing_damage_effect(effect: int) -> bool:
    return 0 < effect < FAIRY_TRANSFORM_EFFECT or effect == INCINERATE_EFFECT


def get_killing_damage_classes(
    sprite_id: int,
    combat_model: EnemyCombatModel = VANILLA_COMBAT_MODEL,
) -> tuple[int, ...]:
    return tuple(
        damage_class
        for damage_class in range(len(combat_model.damage_sources))
        if is_killing_damage_effect(get_damage_effect(sprite_id, damage_class, combat_model))
    )


def get_blob_transform_damage_classes(
    sprite_id: int,
    combat_model: EnemyCombatModel = VANILLA_COMBAT_MODEL,
) -> tuple[int, ...]:
    return tuple(
        damage_class
        for damage_class in range(len(combat_model.damage_sources))
        if get_damage_effect(sprite_id, damage_class, combat_model) == BLOB_TRANSFORM_EFFECT
    )


def get_yellow_slime_follow_up_delivery_override(sprite_id: int) -> CombatDeliveryOverride | None:
    return YELLOW_SLIME_FOLLOW_UP_DELIVERY_OVERRIDES.get(sprite_id)


def get_enemy_health_for_logic(
    sprite_id: int,
    enemy_health_key: str,
    *,
    killable_thieves: bool = False,
    combat_model: EnemyCombatModel = VANILLA_COMBAT_MODEL,
) -> int | None:
    hp = combat_model.enemy_health_table[sprite_id]
    if sprite_id == THIEF_SPRITE_ID and killable_thieves:
        hp = THIEF_DEFAULT_HP

    if enemy_health_key != "default" and hp != 0xFF and sprite_id not in EXCLUDED_ENEMY_TABLE_SPRITE_IDS:
        hp = ENEMY_HEALTH_RANGE_BY_KEY[enemy_health_key][1] - 1

    if hp == 0xFF:
        return None
    return hp


def get_hits_to_kill(
    sprite_id: int,
    damage_class: int,
    enemy_health_key: str,
    *,
    killable_thieves: bool = False,
    combat_model: EnemyCombatModel = VANILLA_COMBAT_MODEL,
) -> int | None:
    effect = get_damage_effect(sprite_id, damage_class, combat_model)
    if effect == INCINERATE_EFFECT:
        return 1
    if not 0 < effect < FAIRY_TRANSFORM_EFFECT:
        return None

    hp = get_enemy_health_for_logic(
        sprite_id,
        enemy_health_key,
        killable_thieves=killable_thieves,
        combat_model=combat_model,
    )
    if hp is None:
        return None
    return (hp + effect - 1) // effect
