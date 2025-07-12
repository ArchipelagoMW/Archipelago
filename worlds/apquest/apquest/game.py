from collections import Counter
from enum import Enum

from entities import InteractableMixin
from events import ConfettiFired, Event
from gameboard import Gameboard, create_gameboard
from graphics import Graphic
from items import Item


class Direction(Enum):
    LEFT = (-1, 0)
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)


class Input(Enum):
    LEFT = 1
    UP = 2
    RIGHT = 3
    DOWN = 4
    ACTION = 5
    CONFETTI = 6


class Player:
    current_x: int
    current_y: int
    current_health: int

    has_won: bool = False

    facing: Direction

    inventory: Counter[Item]

    gameboard: Gameboard

    def __init__(self, gameboard: Gameboard) -> None:
        self.gameboard = gameboard
        self.inventory = Counter()
        self.respawn()

    def respawn(self) -> None:
        self.current_x = 4
        self.current_y = 9
        self.current_health = self.max_health
        self.facing = Direction.DOWN

    @property
    def max_health(self) -> int:
        return 2 + 2 * self.inventory[Item.HEALTH_UPGRADE]

    def render(self) -> Graphic:
        if self.facing == Direction.LEFT:
            return Graphic.PLAYER_LEFT
        if self.facing == Direction.UP:
            return Graphic.PLAYER_UP
        if self.facing == Direction.RIGHT:
            return Graphic.PLAYER_RIGHT
        return Graphic.PLAYER_DOWN

    def receive_item(self, item: Item) -> None:
        self.inventory[item] += 1

    def has_item(self, item: Item) -> bool:
        return self.inventory[item] > 0

    def remove_item(self, item: Item) -> None:
        self.inventory[item] -= 1

    def damage(self, damage: int) -> None:
        if self.has_item(Item.SHIELD):
            damage = damage // 2

        self.current_health = max(0, self.current_health - damage)

        if self.current_health <= 0:
            self.die()

    def die(self) -> None:
        self.respawn()
        self.gameboard.respawn_enemies()

    def victory(self) -> None:
        self.has_won = True


class Game:
    player: Player
    gameboard: Gameboard

    queued_events: list[Event]

    def __init__(self, hard_mode: bool) -> None:
        self.queued_events = []
        self.gameboard = create_gameboard(hard_mode)
        self.player = Player(self.gameboard)

    def render(self) -> tuple[tuple[Graphic, ...], ...]:
        return self.gameboard.render(self.player)

    def attempt_player_movement(self, direction: Direction) -> None:
        self.player.facing = direction

        delta_x, delta_y = direction.value
        new_x, new_y = self.player.current_x + delta_x, self.player.current_y + delta_y

        if not self.gameboard.get_entity_at(new_x, new_y).solid:
            self.player.current_x = new_x
            self.player.current_y = new_y

    def attempt_interact(self) -> None:
        delta_x, delta_y = self.player.facing.value
        entity_x, entity_y = self.player.current_x + delta_x, self.player.current_y + delta_y

        entity = self.gameboard.get_entity_at(entity_x, entity_y)

        if isinstance(entity, InteractableMixin):
            entity.interact(self.player)

    def attempt_fire_confetti_cannon(self) -> None:
        if self.player.has_item(Item.CONFETTI_CANNON):
            self.player.remove_item(Item.CONFETTI_CANNON)
            self.queued_events.append(ConfettiFired(self.player.current_x, self.player.current_y))

    def input(self, input_key: Input) -> None:
        if input_key == Input.LEFT:
            self.attempt_player_movement(Direction.LEFT)
            return

        if input_key == Input.UP:
            self.attempt_player_movement(Direction.UP)
            return

        if input_key == Input.RIGHT:
            self.attempt_player_movement(Direction.RIGHT)
            return

        if input_key == Input.DOWN:
            self.attempt_player_movement(Direction.DOWN)
            return

        if input_key == Input.ACTION:
            self.attempt_interact()
            return

        if input_key == Input.CONFETTI:
            self.attempt_fire_confetti_cannon()
            return

        raise ValueError(f"Don't know input {input_key}")
