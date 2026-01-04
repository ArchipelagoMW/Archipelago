from __future__ import annotations

import random
from collections.abc import Iterable
from typing import TYPE_CHECKING

from .entities import (
    BreakableBlock,
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
from .generate_math_problem import MathProblem
from .graphics import DIGIT_TO_GRAPHIC, DIGIT_TO_GRAPHIC_ZERO_EMPTY, MATH_PROBLEM_TYPE_TO_GRAPHIC, Graphic
from .items import Item
from .locations import DEFAULT_CONTENT, Location

if TYPE_CHECKING:
    from .player import Player


class Gameboard:
    gameboard: tuple[tuple[Entity, ...], ...]

    hammer_exists: bool
    content_filled: bool

    remote_entity_by_location_id: dict[Location, LocationMixin]

    def __init__(self, gameboard: tuple[tuple[Entity, ...], ...], hammer_exists: bool) -> None:
        assert gameboard, "Gameboard is empty"
        assert all(len(row) == len(gameboard[0]) for row in gameboard), "Not all rows have the same size"

        self.gameboard = gameboard
        self.hammer_exists = hammer_exists
        self.content_filled = False
        self.remote_entity_by_location_id = {}

    def fill_default_location_content(self, trap_percentage: int = 0) -> None:
        for entity in self.iterate_entities():
            if isinstance(entity, LocationMixin):
                if entity.location in DEFAULT_CONTENT:
                    content = DEFAULT_CONTENT[entity.location]
                    if content == Item.HAMMER and not self.hammer_exists:
                        content = Item.CONFETTI_CANNON

                    if content == Item.CONFETTI_CANNON:
                        if random.randrange(100) < trap_percentage:
                            content = Item.MATH_TRAP

                    entity.content = content

        self.content_filled = True

    def fill_remote_location_content(self, graphic_overrides: dict[Location, Item]) -> None:
        for entity in self.iterate_entities():
            if isinstance(entity, LocationMixin):
                entity.content = graphic_overrides.get(entity.location, Item.REMOTE_ITEM)
                entity.remote = True
                self.remote_entity_by_location_id[entity.location] = entity

        self.content_filled = True

    def get_entity_at(self, x: int, y: int) -> Entity:
        if x < 0 or x >= len(self.gameboard[0]):
            return Wall()
        if y < 0 or y >= len(self.gameboard):
            return Wall()

        return self.gameboard[y][x]

    def iterate_entities(self) -> Iterable[Entity]:
        for row in self.gameboard:
            yield from row

    def respawn_final_boss(self) -> None:
        for entity in self.iterate_entities():
            if isinstance(entity, FinalBoss):
                entity.respawn()

    def heal_alive_enemies(self) -> None:
        for entity in self.iterate_entities():
            if isinstance(entity, Enemy):
                entity.heal_if_not_dead()

    def render(self, player: Player) -> tuple[tuple[Graphic, ...], ...]:
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

    def render_math_problem(
        self, problem: MathProblem, current_input_digits: list[int], current_input_int: int | None
    ) -> tuple[tuple[Graphic, ...], ...]:
        rows = len(self.gameboard)
        columns = len(self.gameboard[0])

        def pad_row(row: list[Graphic]) -> tuple[Graphic, ...]:
            row = row.copy()
            while len(row) < columns:
                row = [Graphic.EMPTY, *row, Graphic.EMPTY]
            while len(row) > columns:
                row.pop()

            return tuple(row)

        empty_row = tuple([Graphic.EMPTY] * columns)

        math_time_row = pad_row(
            [
                Graphic.LETTER_M,
                Graphic.LETTER_A,
                Graphic.LETTER_T,
                Graphic.LETTER_H,
                Graphic.EMPTY,
                Graphic.LETTER_T,
                Graphic.LETTER_I,
                Graphic.LETTER_M,
                Graphic.LETTER_E,
            ]
        )

        num_1_first_digit = problem.num_1 // 10
        num_1_second_digit = problem.num_1 % 10
        num_2_first_digit = problem.num_2 // 10
        num_2_second_digit = problem.num_2 % 10

        math_problem_row = pad_row(
            [
                DIGIT_TO_GRAPHIC_ZERO_EMPTY[num_1_first_digit],
                DIGIT_TO_GRAPHIC[num_1_second_digit],
                Graphic.EMPTY,
                MATH_PROBLEM_TYPE_TO_GRAPHIC[problem.problem_type],
                Graphic.EMPTY,
                DIGIT_TO_GRAPHIC_ZERO_EMPTY[num_2_first_digit],
                DIGIT_TO_GRAPHIC[num_2_second_digit],
            ]
        )

        display_digit_1 = None
        display_digit_2 = None
        if current_input_digits:
            display_digit_1 = current_input_digits[0]
        if len(current_input_digits) == 2:
            display_digit_2 = current_input_digits[1]

        result_row = pad_row(
            [
                Graphic.EQUALS,
                Graphic.EMPTY,
                DIGIT_TO_GRAPHIC[display_digit_1],
                DIGIT_TO_GRAPHIC[display_digit_2],
                Graphic.EMPTY,
                Graphic.NO if len(current_input_digits) == 2 and current_input_int != problem.result else Graphic.EMPTY,
            ]
        )

        output = [math_time_row, empty_row, math_problem_row, result_row]

        while len(output) < rows:
            output = [empty_row, *output, empty_row]
        while len(output) > columns:
            output.pop(0)

        return tuple(output)

    def force_clear_location(self, location: Location) -> None:
        entity = self.remote_entity_by_location_id[location]
        entity.force_clear()

    @property
    def ready(self) -> bool:
        return self.content_filled

    @property
    def size(self) -> tuple[int, int]:
        return len(self.gameboard[0]), len(self.gameboard)


def create_gameboard(hard_mode: bool, hammer_exists: bool, extra_chest: bool) -> Gameboard:
    boss_door = ButtonDoor()
    boss_door_button = Button(boss_door)

    key_door = KeyDoor()

    top_middle_chest = Chest(Location.TOP_MIDDLE_CHEST)
    left_room_chest = Chest(Location.TOP_LEFT_CHEST)
    bottom_left_chest = Chest(Location.BOTTOM_LEFT_CHEST)
    bottom_right_room_left_chest = Chest(Location.BOTTOM_RIGHT_ROOM_LEFT_CHEST)
    bottom_right_room_right_chest = Chest(Location.BOTTOM_RIGHT_ROOM_RIGHT_CHEST)

    bottom_left_extra_chest = Chest(Location.BOTTOM_LEFT_EXTRA_CHEST) if extra_chest else Empty()
    wall_if_hammer = Wall() if hammer_exists else Empty()
    breakable_block = BreakableBlock() if hammer_exists else Empty()

    normal_enemy = EnemyWithLoot(2 if hard_mode else 1, Location.ENEMY_DROP)
    boss = FinalBoss(5 if hard_mode else 3)

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
        (
            Empty(),
            left_room_chest,
            Empty(),
            Wall(),
            wall_if_hammer,
            breakable_block,
            wall_if_hammer,
            Wall(),
            Wall(),
            boss_door,
            Wall(),
        ),
        (Empty(), Empty(), Empty(), Wall(), Empty(), Empty(), Empty(), Wall(), Empty(), Empty(), Empty()),
        (Wall(), key_door, Wall(), Wall(), Empty(), Empty(), Empty(), Empty(), Empty(), normal_enemy, Empty()),
        (Empty(), Empty(), Empty(), Empty(), Empty(), Empty(), Empty(), Wall(), Empty(), Empty(), Empty()),
        (Empty(), bottom_left_extra_chest, Empty(), Empty(), Empty(), Empty(), Wall(), Wall(), Wall(), Wall(), Wall()),
        (Empty(), Empty(), Empty(), Empty(), Empty(), Empty(), Wall(), Empty(), Empty(), Empty(), Empty()),
        (
            Empty(),
            bottom_left_chest,
            Empty(),
            Empty(),
            Empty(),
            Empty(),
            Bush(),
            Empty(),
            bottom_right_room_left_chest,
            bottom_right_room_right_chest,
            Empty(),
        ),
        (Empty(), Empty(), Empty(), Empty(), Empty(), Empty(), Wall(), Empty(), Empty(), Empty(), Empty()),
    )

    return Gameboard(gameboard, hammer_exists)
