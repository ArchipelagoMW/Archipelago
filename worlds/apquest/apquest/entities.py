from abc import abstractmethod
from typing import TYPE_CHECKING, ClassVar

from graphics import Graphic
from items import ITEM_TO_GRAPHIC, Item
from locations import Location

if TYPE_CHECKING:
    from game import Player


class Entity:
    solid: bool
    graphic: Graphic


class InteractableMixin:
    @abstractmethod
    def interact(self, player: "Player") -> None:
        pass


class ActivatableMixin:
    @abstractmethod
    def activate(self, player: "Player") -> None:
        pass


class LocationMixin:
    location: Location
    content: Item | None = None
    has_given_content: bool = False

    def give_content(self, player: "Player") -> None:
        if self.has_given_content:
            return

        if self.content is None:
            self.content_failure()
            return

        self.has_given_content = True
        player.receive_item(self.content)
        self.content_success()

    def content_success(self) -> None:
        pass

    def content_failure(self) -> None:
        pass


class Empty(Entity):
    solid = False
    graphic = Graphic.EMPTY


class Wall(Entity):
    solid = True
    graphic = Graphic.WALL


class Chest(Entity, InteractableMixin, LocationMixin):
    solid = True

    open: bool = False

    def __init__(self, location: Location) -> None:
        self.location = location

    def update_solidity(self) -> None:
        self.solid = not self.has_given_content

    def interact(self, player: "Player") -> None:
        self.give_content(player)

    def content_success(self) -> None:
        self.update_solidity()

    def content_failure(self) -> None:
        self.update_solidity()

    @property
    def graphic(self) -> Graphic:
        if self.has_given_content:
            return Graphic.EMPTY
        return Graphic.CHEST


class Door(Entity):
    solid = True

    is_open: bool = False

    closed_graphic: ClassVar[Graphic]

    def open(self) -> None:
        self.is_open = True
        self.solid = False

    @property
    def graphic(self) -> Graphic:
        if self.is_open:
            return Graphic.EMPTY
        return self.closed_graphic


class KeyDoor(Door, InteractableMixin):
    closed_graphic = Graphic.KEY_DOOR

    def interact(self, player: "Player") -> None:
        if self.is_open:
            return

        if not player.has_item(Item.KEY):
            return

        player.remove_item(Item.KEY)

        self.open()


class Bush(Door, InteractableMixin):
    closed_graphic = Graphic.BUSH

    def interact(self, player: "Player") -> None:
        if self.is_open:
            return

        if not player.has_item(Item.SWORD):
            return

        self.open()


class Button(Entity, InteractableMixin):
    solid = True

    activates: ActivatableMixin
    activated = False

    def __init__(self, activates: ActivatableMixin) -> None:
        self.activates = activates

    def interact(self, player: "Player") -> None:
        if self.activated:
            return

        self.activated = True
        self.activates.activate(player)

    @property
    def graphic(self) -> Graphic:
        if self.activated:
            return Graphic.BUTTON_ACTIVATED
        return Graphic.BUTTON_NOT_ACTIVATED


class ButtonDoor(Door, ActivatableMixin):
    closed_graphic = Graphic.BUTTON_DOOR

    def activate(self, player: "Player") -> None:
        self.is_open = True
        self.solid = False


class Enemy(Entity, InteractableMixin):
    solid = True

    current_health: int

    max_health: ClassVar[int] = 2
    dead: bool = False

    enemy_graphic: ClassVar[Graphic] = Graphic.NORMAL_ENEMY

    def __init__(self) -> None:
        self.respawn()

    def die(self) -> None:
        self.dead = True
        self.solid = False

    def respawn(self) -> None:
        self.current_health = self.max_health
        self.dead = False
        self.solid = True

    def interact(self, player: "Player") -> None:
        if self.dead:
            return

        self.current_health = max(0, self.current_health - 1)

        if self.current_health == 0:
            if not self.dead:
                self.die()
            return

        player.damage(2)

    @property
    def graphic(self) -> Graphic:
        if self.dead:
            return Graphic.EMPTY
        return self.enemy_graphic


class EnemyWithLoot(Enemy, LocationMixin):
    def __init__(self, location: Location) -> None:
        super().__init__()
        self.location = location

    def die(self) -> None:
        self.dead = True
        self.solid = not self.has_given_content

    def interact(self, player: "Player") -> None:
        if self.dead:
            if not self.has_given_content:
                self.give_content(player)
            return

        super().interact(player)

    @property
    def graphic(self) -> Graphic:
        if self.dead and not self.has_given_content:
            return ITEM_TO_GRAPHIC[self.content]
        return super().graphic

    def content_success(self) -> None:
        self.die()

    def content_failure(self) -> None:
        self.die()


class FinalBoss(Enemy):
    max_health = 5

    enemy_graphic = Graphic.BOSS

    def interact(self, player: "Player") -> None:
        dead_before = self.dead

        super().interact(player)

        if not dead_before and self.dead:
            player.victory()
