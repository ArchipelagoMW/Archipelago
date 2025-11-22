from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, ClassVar

from .graphics import Graphic
from .items import ITEM_TO_GRAPHIC, Item
from .locations import Location

if TYPE_CHECKING:
    from .player import Player


class Entity:
    solid: bool
    graphic: Graphic


class InteractableMixin:
    @abstractmethod
    def interact(self, player: Player) -> None:
        pass


class ActivatableMixin:
    @abstractmethod
    def activate(self, player: Player) -> None:
        pass


class LocationMixin:
    location: Location
    content: Item | None = None
    remote: bool = False
    has_given_content: bool = False

    def force_clear(self) -> None:
        if self.has_given_content:
            return

        self.has_given_content = True
        self.content_success()

    def give_content(self, player: Player) -> None:
        if self.has_given_content:
            return

        if self.content is None:
            self.content_failure()
            return

        if self.remote:
            player.location_cleared(self.location.value)
        else:
            player.receive_item(self.content)

        self.has_given_content = True
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

    is_open: bool = False

    def __init__(self, location: Location) -> None:
        self.location = location

    def update_solidity(self) -> None:
        self.solid = not self.has_given_content

    def open(self) -> None:
        self.is_open = True
        self.update_solidity()

    def interact(self, player: Player) -> None:
        if self.has_given_content:
            return

        if self.is_open:
            self.give_content(player)
            return

        self.open()

    def content_success(self) -> None:
        self.update_solidity()

    def content_failure(self) -> None:
        self.update_solidity()

    @property
    def graphic(self) -> Graphic:
        if self.has_given_content:
            return Graphic.EMPTY
        if self.is_open:
            if self.content is None:
                return Graphic.EMPTY
            return ITEM_TO_GRAPHIC[self.content]
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

    def interact(self, player: Player) -> None:
        if self.is_open:
            return

        if not player.has_item(Item.KEY):
            return

        player.remove_item(Item.KEY)

        self.open()


class BreakableBlock(Door, InteractableMixin):
    closed_graphic = Graphic.BREAKABLE_BLOCK

    def interact(self, player: Player) -> None:
        if self.is_open:
            return

        if not player.has_item(Item.HAMMER):
            return

        player.remove_item(Item.HAMMER)

        self.open()


class Bush(Door, InteractableMixin):
    closed_graphic = Graphic.BUSH

    def interact(self, player: Player) -> None:
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

    def interact(self, player: Player) -> None:
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

    def activate(self, player: Player) -> None:
        self.is_open = True
        self.solid = False


class Enemy(Entity, InteractableMixin):
    solid = True

    current_health: int
    max_health: int

    dead: bool = False

    enemy_graphic_by_health: ClassVar[dict[int, Graphic]] = {
        2: Graphic.NORMAL_ENEMY_2_HEALTH,
        1: Graphic.NORMAL_ENEMY_1_HEALTH,
    }
    enemy_default_graphic = Graphic.NORMAL_ENEMY_1_HEALTH

    def __init__(self, max_health: int) -> None:
        self.max_health = max_health
        self.respawn()

    def die(self) -> None:
        self.dead = True
        self.solid = False

    def respawn(self) -> None:
        self.dead = False
        self.solid = True
        self.heal_if_not_dead()

    def heal_if_not_dead(self) -> None:
        if self.dead:
            return
        self.current_health = self.max_health

    def interact(self, player: Player) -> None:
        if self.dead:
            return

        if player.has_item(Item.SWORD):
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
        return self.enemy_graphic_by_health.get(self.current_health, self.enemy_default_graphic)


class EnemyWithLoot(Enemy, LocationMixin):
    def __init__(self, max_health: int, location: Location) -> None:
        super().__init__(max_health)
        self.location = location

    def die(self) -> None:
        self.dead = True
        self.solid = not self.has_given_content

    def interact(self, player: Player) -> None:
        if self.dead:
            if not self.has_given_content:
                self.give_content(player)
            return

        super().interact(player)

    @property
    def graphic(self) -> Graphic:
        if self.dead and not self.has_given_content:
            if self.content is None:
                return Graphic.EMPTY
            return ITEM_TO_GRAPHIC[self.content]
        return super().graphic

    def content_success(self) -> None:
        self.die()

    def content_failure(self) -> None:
        self.die()


class FinalBoss(Enemy):
    enemy_graphic_by_health: ClassVar[dict[int, Graphic]] = {
        5: Graphic.BOSS_5_HEALTH,
        4: Graphic.BOSS_4_HEALTH,
        3: Graphic.BOSS_3_HEALTH,
        2: Graphic.BOSS_2_HEALTH,
        1: Graphic.BOSS_1_HEALTH,
    }
    enemy_default_graphic = Graphic.BOSS_1_HEALTH

    def interact(self, player: Player) -> None:
        dead_before = self.dead

        super().interact(player)

        if not dead_before and self.dead:
            player.victory()
