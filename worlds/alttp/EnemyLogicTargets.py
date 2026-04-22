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


AGA_TOWER_ENTRANCE_TOP_LEFT = "Agahnim's Tower (Entrance Room) - Top Left"
AGA_TOWER_CIRCLE_OF_POTS_TOP_HALF = "Agahnim's Tower (Circle of Pots) - Top Half"
DESERT_EAST_ENTRANCE_TOP_RIGHT = "Desert Palace (East Entrance Room) - Top Right"
DESERT_BEAMOS_HELLWAY_BOTTOM_LEFT = "Desert Palace (Popos 2 / Beamos Hellway Room) - Bottom Left"
HERA_HARDHAT_BEETLES_BOTTOM_RIGHT = "Tower of Hera (Hardhat Beetles Room) - Bottom Right"
TURTLE_ROCK_BIG_KEY_ROOM_TOP_LEFT = "Turtle Rock (Big Key Room) - Top Left"
POD_SOUTH_MIMICS_TOP_LEFT = "Palace of Darkness (Warps / South Mimics Room) - Top Left"
GANONS_TOWER_WIZZROBES_TOP_HALF = "Ganon's Tower (Wizzrobes Rooms) - Top Half"
HYRULE_CASTLE_BOOMERANG_CHEST_BOTTOM_RIGHT = "Hyrule Castle (Boomerang Chest Room) - Bottom Right"

ENEMY_CLEAR_TARGETS = (
    EnemyClearTarget(name="Mimic Cave", room_name="Mimic Cave"),
    EnemyClearTarget(name="Mini-Moldorm Cave", room_name="Mini-Moldorm Cave"),
    EnemyClearTarget(name=AGA_TOWER_ENTRANCE_TOP_LEFT, room_name="Agahnim's Tower (Entrance Room)", max_x=256, max_y=256),
    EnemyClearTarget(name=AGA_TOWER_CIRCLE_OF_POTS_TOP_HALF, room_name="Agahnim's Tower (Circle of Pots)", max_y=256),
    EnemyClearTarget(name="Eastern Palace (Big Key Room)", room_name="Eastern Palace (Big Key Room)"),
    EnemyClearTarget(
        name="Eastern Palace ('Zeldagamer Room' / Pre-Armos Knights Room)",
        room_name="Eastern Palace ('Zeldagamer Room' / Pre-Armos Knights Room)",
    ),
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
    EnemyClearTarget(name=TURTLE_ROCK_BIG_KEY_ROOM_TOP_LEFT, room_name="Turtle Rock (Big Key Room)", max_x=256, max_y=256),
    EnemyClearTarget(
        name=POD_SOUTH_MIMICS_TOP_LEFT,
        room_name="Palace of Darkness (Warps / South Mimics Room)",
        max_x=256,
        max_y=256,
    ),
    EnemyClearTarget(name=GANONS_TOWER_WIZZROBES_TOP_HALF, room_name="Ganon's Tower (Wizzrobes Rooms)", max_y=256),
    EnemyClearTarget(name="Hyrule Castle (Boomerang Chest Room)", room_name="Hyrule Castle (Boomerang Chest Room)"),
    EnemyClearTarget(
        name=HYRULE_CASTLE_BOOMERANG_CHEST_BOTTOM_RIGHT,
        room_name="Hyrule Castle (Boomerang Chest Room)",
        min_x=256,
        min_y=256,
    ),
)

ENEMY_CLEAR_TARGET_LOOKUP = {target.name: target for target in ENEMY_CLEAR_TARGETS}

KEY_DROP_ENEMY_TARGETS = (
    KeyDropEnemyTarget(
        location_name="Hyrule Castle - Map Guard Key Drop",
        room_name="Hyrule Castle (Map Chest Room)",
        x_coord_pixels=272,
        y_coord_pixels=96,
    ),
    KeyDropEnemyTarget(
        location_name="Hyrule Castle - Boomerang Guard Key Drop",
        room_name="Hyrule Castle (Boomerang Chest Room)",
        x_coord_pixels=416,
        y_coord_pixels=384,
    ),
    KeyDropEnemyTarget(
        location_name="Sewers - Key Rat Key Drop",
        room_name="Hyrule Castle (Key-rat Room)",
        x_coord_pixels=80,
        y_coord_pixels=96,
    ),
    KeyDropEnemyTarget(
        location_name="Hyrule Castle - Big Key Drop",
        room_name="Hyrule Castle (Jail Cell Room)",
        x_coord_pixels=416,
        y_coord_pixels=144,
    ),
    KeyDropEnemyTarget(
        location_name="Eastern Palace - Dark Eyegore Key Drop",
        room_name="Eastern Palace (Eyegore Key Room)",
        x_coord_pixels=272,
        y_coord_pixels=368,
    ),
    KeyDropEnemyTarget(
        location_name="Castle Tower - Dark Archer Key Drop",
        room_name="Agahnim's Tower (Dark Bridge Room)",
        x_coord_pixels=320,
        y_coord_pixels=176,
    ),
    KeyDropEnemyTarget(
        location_name="Castle Tower - Circle of Pots Key Drop",
        room_name="Agahnim's Tower (Circle of Pots)",
        x_coord_pixels=128,
        y_coord_pixels=384,
    ),
    KeyDropEnemyTarget(
        location_name="Skull Woods - Spike Corner Key Drop",
        room_name="Skull Woods (Gibdo Key / Mothula Hole Room)",
        x_coord_pixels=80,
        y_coord_pixels=336,
    ),
    KeyDropEnemyTarget(
        location_name="Ice Palace - Jelly Key Drop",
        room_name="Ice Palace (Entrance Room)",
        x_coord_pixels=80,
        y_coord_pixels=416,
    ),
    KeyDropEnemyTarget(
        location_name="Ice Palace - Conveyor Key Drop",
        room_name="Ice Palace (Stalfos Knights / Conveyor Hellway)",
        x_coord_pixels=272,
        y_coord_pixels=384,
    ),
    KeyDropEnemyTarget(
        location_name="Misery Mire - Conveyor Crystal Key Drop",
        room_name="Misery Mire (Compass Chest / Tile Room)",
        x_coord_pixels=304,
        y_coord_pixels=432,
    ),
    KeyDropEnemyTarget(
        location_name="Turtle Rock - Pokey 1 Key Drop",
        room_name="Turtle Rock (Chain Chomps Room)",
        x_coord_pixels=112,
        y_coord_pixels=336,
    ),
    KeyDropEnemyTarget(
        location_name="Turtle Rock - Pokey 2 Key Drop",
        room_name="Turtle Rock (Hokku-Bokku Key Room 2)",
        x_coord_pixels=352,
        y_coord_pixels=384,
    ),
    KeyDropEnemyTarget(
        location_name="Ganons Tower - Mini Helmasaur Key Drop",
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
