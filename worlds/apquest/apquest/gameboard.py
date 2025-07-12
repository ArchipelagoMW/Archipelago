from collections.abc import Iterable
from typing import TYPE_CHECKING

from entities import (
    Bush,
    Button,
    ButtonDoor,
    Chest,
    Empty,
    Enemy,
    EnemyWithLoot,
    Entity,
    FinalBoss,
    KeyDoor,
    LocationMixin,
    Wall,
)
from graphics import Graphic
from locations import DEFAULT_CONTENT, Location

if TYPE_CHECKING:
    from game import Player

class Gameboard:
    gameboard: tuple[tuple[Entity, ...], ...]

    def __init__(self, gameboard: tuple[tuple[Entity, ...], ...]) -> None:
        assert gameboard, "Gameboard is empty"
        assert all(len(row) == len(gameboard[0]) for row in gameboard), "Not all rows have the same size"

        self.gameboard = gameboard

    def fill_default_location_content(self) -> None:
        for entity in self.iterate_entities():
            if isinstance(entity, LocationMixin):
                if entity.location in DEFAULT_CONTENT:
                    entity.content = DEFAULT_CONTENT[entity.location]

    def get_entity_at(self, x: int, y: int) -> Entity:
        if x < 0 or x >= len(self.gameboard[0]):
            return Wall()
        if y < 0 or y >= len(self.gameboard):
            return Wall()

        return self.gameboard[y][x]

    def iterate_entities(self) -> Iterable[Entity]:
        for row in self.gameboard:
            yield from row

    def respawn_enemies(self) -> None:
        for entity in self.iterate_entities():
            if isinstance(entity, Enemy):
                entity.respawn()

    def render(self, player: "Player") -> tuple[tuple[Graphic, ...], ...]:
        graphics = []

        for y, row in enumerate(self.gameboard):
            graphics_row = []
            for x, entity in enumerate(row):
                if player.current_x == x and player.current_y == y:
                    graphics_row.append(player.render())
                else:
                    graphics_row.append(entity.graphic)

            graphics.append(tuple(graphics_row))

        return tuple(graphics)


def create_gameboard() -> Gameboard:
    boss_door = ButtonDoor()
    boss_door_button = Button(boss_door)

    key_door = KeyDoor()

    top_middle_chest = Chest(Location.TOP_MIDDLE_CHEST)
    left_room_chest = Chest(Location.TOP_LEFT_CHEST)
    bottom_left_chest = Chest(Location.BOTTOM_LEFT_CHEST)
    bottom_right_chest = Chest(Location.BOTTOM_RIGHT_CHEST)

    normal_enemy = EnemyWithLoot(Location.ENEMY_DROP)
    boss = FinalBoss()

    gameboard = (
        (Empty(), Empty(), Empty(), Wall(), Empty(), Empty(), Empty(), Wall(), Empty(), Empty(), Empty()),
        (
            Empty(),
            boss_door_button,
            Empty(),
            Wall(),
            Empty(),
            top_middle_chest,
            Empty(),
            Wall(),
            Empty(),
            boss,
            Empty(),
        ),
        (Empty(), Empty(), Empty(), Wall(), Empty(), Empty(), Empty(), Wall(), Empty(), Empty(), Empty()),
        (Empty(), left_room_chest, Empty(), Wall(), Empty(), Empty(), Empty(), Wall(), Wall(), boss_door, Wall()),
        (Empty(), Empty(), Empty(), Wall(), Empty(), Empty(), Empty(), Wall(), Empty(), Empty(), Empty()),
        (Wall(), key_door, Wall(), Wall(), Empty(), Empty(), Empty(), Empty(), Empty(), normal_enemy, Empty()),
        (Empty(), Empty(), Empty(), Empty(), Empty(), Empty(), Empty(), Wall(), Empty(), Empty(), Empty()),
        (Empty(), Empty(), Empty(), Empty(), Empty(), Empty(), Empty(), Wall(), Wall(), Wall(), Wall()),
        (Empty(), Empty(), Empty(), Empty(), Empty(), Empty(), Empty(), Wall(), Empty(), Empty(), Empty()),
        (
            Empty(),
            bottom_left_chest,
            Empty(),
            Empty(),
            Empty(),
            Empty(),
            Empty(),
            Bush(),
            Empty(),
            bottom_right_chest,
            Empty(),
        ),
        (Empty(), Empty(), Empty(), Empty(), Empty(), Empty(), Empty(), Wall(), Empty(), Empty(), Empty()),
    )

    return Gameboard(gameboard)
