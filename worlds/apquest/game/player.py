from collections import Counter
from collections.abc import Callable

from .events import Event, LocationClearedEvent, VictoryEvent
from .gameboard import Gameboard
from .graphics import Graphic
from .inputs import Direction
from .items import Item


class Player:
    current_x: int
    current_y: int
    current_health: int

    has_won: bool = False

    facing: Direction

    inventory: Counter[Item]

    gameboard: Gameboard
    push_event: Callable[[Event], None]

    def __init__(self, gameboard: Gameboard, push_event: Callable[[Event], None]) -> None:
        self.gameboard = gameboard
        self.inventory = Counter()
        self.push_event = push_event
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
        if not self.gameboard.ready:
            return Graphic.EMPTY

        if self.facing == Direction.LEFT:
            return Graphic.PLAYER_LEFT
        if self.facing == Direction.UP:
            return Graphic.PLAYER_UP
        if self.facing == Direction.RIGHT:
            return Graphic.PLAYER_RIGHT
        return Graphic.PLAYER_DOWN

    def receive_item(self, item: Item) -> None:
        assert item != Item.REMOTE_ITEM, "Player should not directly receive the remote item"

        self.inventory[item] += 1
        if item == Item.HEALTH_UPGRADE:
            self.current_health += 2

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
        self.gameboard.respawn_final_boss()
        self.gameboard.heal_alive_enemies()

    def location_cleared(self, location_id: int) -> None:
        event = LocationClearedEvent(location_id)
        self.push_event(event)

    def victory(self) -> None:
        self.has_won = True
        event = VictoryEvent()
        self.push_event(event)
