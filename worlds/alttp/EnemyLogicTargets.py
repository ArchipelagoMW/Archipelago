from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import ALTTPWorld
    from .EnemyShuffle import EffectiveDungeonEnemySprite


@dataclass(frozen=True)
class EnemyClearTarget:
    name: str
    room_name: str
    min_x: int = 0
    max_x: int | None = None
    min_y: int = 0
    max_y: int | None = None

    def contains(self, enemy: "EffectiveDungeonEnemySprite") -> bool:
        if enemy.x_coord_pixels < self.min_x or enemy.y_coord_pixels < self.min_y:
            return False
        if self.max_x is not None and enemy.x_coord_pixels >= self.max_x:
            return False
        if self.max_y is not None and enemy.y_coord_pixels >= self.max_y:
            return False
        return True


@dataclass(frozen=True)
class KeyDropEnemyTarget:
    location_name: str
    room_name: str
    x_coord_pixels: int
    y_coord_pixels: int

    def matches(self, enemy: "EffectiveDungeonEnemySprite") -> bool:
        return (
            enemy.x_coord_pixels == self.x_coord_pixels
            and enemy.y_coord_pixels == self.y_coord_pixels
        )


MIMIC_CAVE_ROOM = "Mimic Cave"
MINI_MOLDORM_CAVE_ROOM = "Mini-Moldorm Cave"
AGA_TOWER_ENTRANCE_TOP_LEFT = "Agahnim's Tower (Second Room)"
AGA_TOWER_CIRCLE_OF_POTS_TOP_HALF = "Agahnim's Tower (Pre-Circle of Pots)"
EASTERN_BIG_KEY_ROOM = "Eastern Palace (Big Key Room)"
EASTERN_PRE_ARMOS_ROOM = "Eastern Palace (Pre-Armos Knights Rooms)"
DESERT_EAST_ENTRANCE_TOP_RIGHT = "Desert Palace (Compass Room)"
DESERT_BEAMOS_HELLWAY_BOTTOM_LEFT = "Desert Palace (4 Statues Room)"
HERA_HARDHAT_BEETLES_BOTTOM_RIGHT = "Tower of Hera (Hardhat Beetles Room)"
TURTLE_ROCK_BIG_CHEST_ROOM_TOP_LEFT = "Turtle Rock (Double Hokku-Bokku Room)"
ICE_PALACE_COMPASS_ROOM = "Ice Palace (Compass Room)"
ICE_PALACE_PENGATORS_ROOM = "Ice Palace (Pengators Room)"
ICE_PALACE_CONVEYOR_HELLWAY_TOP_RIGHT = "Ice Palace (Conveyor Hellway)"
POD_NORTH_MIMICS_BOTTOM_LEFT = "Palace of Darkness (North Mimics Room)"
POD_TURTLE_ROOM_BOTTOM_LEFT = "Palace of Darkness (Turtle Room)"
POD_SOUTH_MIMICS_TOP_LEFT = "Palace of Darkness (South Mimics Room)"
GANONS_TOWER_WIZZROBES_TOP_HALF = "Ganon's Tower (Wizzrobes Rooms)"
HYRULE_CASTLE_PRE_BOOMERANG_CHEST_ROOM = "Hyrule Castle (Pre-Boomerang Chest Room)"
THIEVES_TOWN_JAIL_CELLS_TOP_LEFT = "Thieves Town (Basement)"

HYRULE_CASTLE_MAP_GUARD_KEY_DROP = "Hyrule Castle - Map Guard Key Drop"
HYRULE_CASTLE_BOOMERANG_GUARD_KEY_DROP = "Hyrule Castle - Boomerang Guard Key Drop"
SEWERS_KEY_RAT_KEY_DROP = "Sewers - Key Rat Key Drop"
HYRULE_CASTLE_BIG_KEY_DROP = "Hyrule Castle - Big Key Drop"
EASTERN_DARK_EYEGORE_KEY_DROP = "Eastern Palace - Dark Eyegore Key Drop"
CASTLE_TOWER_DARK_ARCHER_KEY_DROP = "Castle Tower - Dark Archer Key Drop"
CASTLE_TOWER_CIRCLE_OF_POTS_KEY_DROP = "Castle Tower - Circle of Pots Key Drop"
SKULL_WOODS_SPIKE_CORNER_KEY_DROP = "Skull Woods - Spike Corner Key Drop"
ICE_PALACE_JELLY_KEY_DROP = "Ice Palace - Jelly Key Drop"
ICE_PALACE_CONVEYOR_KEY_DROP = "Ice Palace - Conveyor Key Drop"
MISERY_MIRE_CONVEYOR_CRYSTAL_KEY_DROP = "Misery Mire - Conveyor Crystal Key Drop"
TURTLE_ROCK_POKEY_1_KEY_DROP = "Turtle Rock - Pokey 1 Key Drop"
TURTLE_ROCK_POKEY_2_KEY_DROP = "Turtle Rock - Pokey 2 Key Drop"
GANONS_TOWER_MINI_HELMASAUR_KEY_DROP = "Ganons Tower - Mini Helmasaur Key Drop"

ENEMY_CLEAR_TARGETS = (
    EnemyClearTarget(name=MIMIC_CAVE_ROOM, room_name="Mimic Cave"),
    EnemyClearTarget(name=MINI_MOLDORM_CAVE_ROOM, room_name="Mini-Moldorm Cave"),
    EnemyClearTarget(name=AGA_TOWER_ENTRANCE_TOP_LEFT, room_name="Agahnim's Tower (Entrance Room)", max_x=256, max_y=256),
    EnemyClearTarget(name=AGA_TOWER_CIRCLE_OF_POTS_TOP_HALF, room_name="Agahnim's Tower (Circle of Pots)", max_y=256),
    EnemyClearTarget(name=EASTERN_BIG_KEY_ROOM, room_name="Eastern Palace (Big Key Room)"),
    EnemyClearTarget(name=EASTERN_PRE_ARMOS_ROOM, room_name="Eastern Palace ('Zeldagamer Room' / Pre-Armos Knights Room)"),
    EnemyClearTarget(name=DESERT_EAST_ENTRANCE_TOP_RIGHT, room_name="Desert Palace (East Entrance Room)", min_x=256, max_y=256),
    EnemyClearTarget(
        name=DESERT_BEAMOS_HELLWAY_BOTTOM_LEFT,
        room_name="Desert Palace (Popos 2 / Beamos Hellway Room)",
        max_x=256,
        min_y=256,
    ),
    EnemyClearTarget(
        name=HERA_HARDHAT_BEETLES_BOTTOM_RIGHT,
        room_name="Tower of Hera (Hardhat Beetles Room)",
        min_x=256,
        min_y=256,
    ),
    EnemyClearTarget(
        name=TURTLE_ROCK_BIG_CHEST_ROOM_TOP_LEFT,
        room_name="Turtle Rock (Double Hokku-Bokku / Big chest Room)",
        max_x=256,
        max_y=256,
    ),
    EnemyClearTarget(name=ICE_PALACE_COMPASS_ROOM, room_name="Ice Palace (Compass Room)"),
    EnemyClearTarget(name=ICE_PALACE_PENGATORS_ROOM, room_name="Ice Palace (Pengators Room)"),
    EnemyClearTarget(
        name=ICE_PALACE_CONVEYOR_HELLWAY_TOP_RIGHT,
        room_name="Ice Palace (Stalfos Knights / Conveyor Hellway)",
        min_x=256,
        max_y=256,
    ),
    EnemyClearTarget(
        name=POD_NORTH_MIMICS_BOTTOM_LEFT,
        room_name="Palace of Darkness (Mimics / Moving Wall Room)",
        max_x=256,
        min_y=256,
    ),
    EnemyClearTarget(
        name=POD_TURTLE_ROOM_BOTTOM_LEFT,
        room_name="Palace of Darkness (Turtle Room)",
        max_x=256,
        min_y=256,
    ),
    EnemyClearTarget(
        name=POD_SOUTH_MIMICS_TOP_LEFT,
        room_name="Palace of Darkness (Warps / South Mimics Room)",
        max_x=256,
        max_y=256,
    ),
    EnemyClearTarget(
        name=THIEVES_TOWN_JAIL_CELLS_TOP_LEFT,
        room_name="Thieves Town (Jail Cells Room)",
        max_x=256,
        max_y=256,
    ),
    EnemyClearTarget(name=GANONS_TOWER_WIZZROBES_TOP_HALF, room_name="Ganon's Tower (Wizzrobes Rooms)", max_y=256),
    EnemyClearTarget(
        name=HYRULE_CASTLE_PRE_BOOMERANG_CHEST_ROOM,
        room_name="Hyrule Castle (Boomerang Chest Room)",
        max_x=256,
        min_y=256,
    ),
)

ENEMY_CLEAR_TARGET_LOOKUP = {target.name: target for target in ENEMY_CLEAR_TARGETS}

KEY_DROP_ENEMY_TARGETS = (
    KeyDropEnemyTarget(
        location_name=HYRULE_CASTLE_MAP_GUARD_KEY_DROP,
        room_name="Hyrule Castle (Map Chest Room)",
        x_coord_pixels=272,
        y_coord_pixels=96,
    ),
    KeyDropEnemyTarget(
        location_name=HYRULE_CASTLE_BOOMERANG_GUARD_KEY_DROP,
        room_name="Hyrule Castle (Boomerang Chest Room)",
        x_coord_pixels=416,
        y_coord_pixels=384,
    ),
    KeyDropEnemyTarget(
        location_name=SEWERS_KEY_RAT_KEY_DROP,
        room_name="Hyrule Castle (Key-rat Room)",
        x_coord_pixels=80,
        y_coord_pixels=96,
    ),
    KeyDropEnemyTarget(
        location_name=HYRULE_CASTLE_BIG_KEY_DROP,
        room_name="Hyrule Castle (Jail Cell Room)",
        x_coord_pixels=416,
        y_coord_pixels=144,
    ),
    KeyDropEnemyTarget(
        location_name=EASTERN_DARK_EYEGORE_KEY_DROP,
        room_name="Eastern Palace (Eyegore Key Room)",
        x_coord_pixels=272,
        y_coord_pixels=368,
    ),
    KeyDropEnemyTarget(
        location_name=CASTLE_TOWER_DARK_ARCHER_KEY_DROP,
        room_name="Agahnim's Tower (Dark Bridge Room)",
        x_coord_pixels=320,
        y_coord_pixels=176,
    ),
    KeyDropEnemyTarget(
        location_name=CASTLE_TOWER_CIRCLE_OF_POTS_KEY_DROP,
        room_name="Agahnim's Tower (Circle of Pots)",
        x_coord_pixels=128,
        y_coord_pixels=384,
    ),
    KeyDropEnemyTarget(
        location_name=SKULL_WOODS_SPIKE_CORNER_KEY_DROP,
        room_name="Skull Woods (Gibdo Key / Mothula Hole Room)",
        x_coord_pixels=80,
        y_coord_pixels=336,
    ),
    KeyDropEnemyTarget(
        location_name=ICE_PALACE_JELLY_KEY_DROP,
        room_name="Ice Palace (Entrance Room)",
        x_coord_pixels=80,
        y_coord_pixels=416,
    ),
    KeyDropEnemyTarget(
        location_name=ICE_PALACE_CONVEYOR_KEY_DROP,
        room_name="Ice Palace (Stalfos Knights / Conveyor Hellway)",
        x_coord_pixels=272,
        y_coord_pixels=384,
    ),
    KeyDropEnemyTarget(
        location_name=MISERY_MIRE_CONVEYOR_CRYSTAL_KEY_DROP,
        room_name="Misery Mire (Compass Chest / Tile Room)",
        x_coord_pixels=304,
        y_coord_pixels=432,
    ),
    KeyDropEnemyTarget(
        location_name=TURTLE_ROCK_POKEY_1_KEY_DROP,
        room_name="Turtle Rock (Chain Chomps Room)",
        x_coord_pixels=112,
        y_coord_pixels=336,
    ),
    KeyDropEnemyTarget(
        location_name=TURTLE_ROCK_POKEY_2_KEY_DROP,
        room_name="Turtle Rock (Hokku-Bokku Key Room 2)",
        x_coord_pixels=352,
        y_coord_pixels=384,
    ),
    KeyDropEnemyTarget(
        location_name=GANONS_TOWER_MINI_HELMASAUR_KEY_DROP,
        room_name="Ganon's Tower (Torch Room 2)",
        x_coord_pixels=368,
        y_coord_pixels=112,
    ),
)

KEY_DROP_ENEMY_TARGET_LOOKUP = {
    target.location_name: target
    for target in KEY_DROP_ENEMY_TARGETS
}


def get_enemy_clear_target(target_name: str) -> EnemyClearTarget:
    return ENEMY_CLEAR_TARGET_LOOKUP[target_name]


def get_key_drop_enemy_target(location_name: str) -> KeyDropEnemyTarget:
    return KEY_DROP_ENEMY_TARGET_LOOKUP[location_name]


def get_enemy_clear_target_enemies(
    world: "ALTTPWorld",
    target_name: str,
) -> tuple["EffectiveDungeonEnemySprite", ...]:
    from .EnemyShuffle import get_effective_dungeon_room_enemies, get_room_id

    target = get_enemy_clear_target(target_name)
    room_id = get_room_id(target.room_name)
    if room_id is None:
        raise ValueError(f"Unknown ALTTP room {target.room_name!r}")

    return tuple(
        enemy
        for enemy in get_effective_dungeon_room_enemies(world, room_id)
        if target.contains(enemy)
    )


def get_key_drop_enemy(
    world: "ALTTPWorld",
    location_name: str,
) -> "EffectiveDungeonEnemySprite | None":
    from .EnemyShuffle import get_effective_dungeon_room_enemies, get_room_id

    target = get_key_drop_enemy_target(location_name)
    room_id = get_room_id(target.room_name)
    if room_id is None:
        raise ValueError(f"Unknown ALTTP room {target.room_name!r}")

    for enemy in get_effective_dungeon_room_enemies(world, room_id):
        if target.matches(enemy):
            return enemy
    return None
