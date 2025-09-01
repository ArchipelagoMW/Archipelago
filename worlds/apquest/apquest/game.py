from math import ceil

from .entities import InteractableMixin
from .events import ConfettiFired, Event
from .gameboard import Gameboard, create_gameboard
from .graphics import Graphic
from .inputs import Direction, Input
from .items import ITEM_TO_GRAPHIC, Item, RemotelyReceivedItem
from .locations import Location
from .player import Player


class Game:
    player: Player
    gameboard: Gameboard

    queued_events: list[Event]

    remotely_received_items: set[tuple[int, int, int]]

    def __init__(self, hard_mode: bool, hammer_exists: bool, extra_chest: bool) -> None:
        self.queued_events = []
        self.gameboard = create_gameboard(hard_mode, hammer_exists, extra_chest)
        self.player = Player(self.gameboard, self.queued_events.append)
        self.remotely_received_items = set()

    def render(self) -> tuple[tuple[Graphic, ...], ...]:
        return self.gameboard.render(self.player)

    def render_health_and_inventory(self, vertical: bool = False) -> tuple[Graphic, ...]:
        size = self.gameboard.size[1] if vertical else self.gameboard.size[0]

        graphics_array = [Graphic.EMPTY] * size

        item_back_index = size - 1
        for item, amount in sorted(self.player.inventory.items(), key=lambda sort_item: sort_item[0].value):
            for _ in range(amount):
                if item_back_index == 3:
                    break
                if item == Item.HEALTH_UPGRADE:
                    continue
                graphics_array[item_back_index] = ITEM_TO_GRAPHIC[item]
                item_back_index -= 1
            else:
                continue
            break

        remaining_health = self.player.current_health
        for i in range(min(item_back_index, ceil(self.player.max_health / 2))):
            new_remaining_health = max(0, remaining_health - 2)
            change = remaining_health - new_remaining_health
            remaining_health = new_remaining_health

            if change == 2:
                graphics_array[i] = Graphic.HEART
            elif change == 1:
                graphics_array[i] = Graphic.HALF_HEART
            elif change == 0:
                graphics_array[i] = Graphic.EMPTY_HEART

        return tuple(graphics_array)

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
        if not self.gameboard.ready:
            return

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

    def receive_item(self, remote_item_id: int, remote_location_id: int, remote_location_player: int) -> None:
        remotely_received_item = RemotelyReceivedItem(remote_item_id, remote_location_id, remote_location_player)
        if remotely_received_item in self.remotely_received_items:
            return

        self.player.receive_item(Item(remote_item_id))

    def force_clear_location(self, location_id: int) -> None:
        location = Location(location_id)
        self.gameboard.force_clear_location(location)
