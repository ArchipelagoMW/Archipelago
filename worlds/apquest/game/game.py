from math import ceil
from random import Random

from .entities import InteractableMixin
from .events import ConfettiFired, Event, MathProblemSolved, MathProblemStarted
from .gameboard import Gameboard, create_gameboard
from .generate_math_problem import MathProblem, generate_math_problem
from .graphics import Graphic
from .inputs import DIGIT_INPUTS_TO_DIGITS, Direction, Input
from .items import ITEM_TO_GRAPHIC, Item, RemotelyReceivedItem
from .locations import Location
from .player import Player


class Game:
    player: Player
    gameboard: Gameboard

    random: Random

    queued_events: list[Event]

    active_math_problem: MathProblem | None
    active_math_problem_input: list[int] | None

    auto_target_path: list[tuple[int, int]] = []

    remotely_received_items: set[tuple[int, int, int]]

    def __init__(
        self, hard_mode: bool, hammer_exists: bool, extra_chest: bool, random_object: Random | None = None
    ) -> None:
        self.queued_events = []
        self.gameboard = create_gameboard(hard_mode, hammer_exists, extra_chest)
        self.player = Player(self.gameboard, self.queued_events.append)
        self.active_math_problem = None
        self.remotely_received_items = set()

        if random_object is None:
            self.random = Random()
        else:
            self.random = random_object

    def render(self) -> tuple[tuple[Graphic, ...], ...]:
        if self.active_math_problem is None and self.player.inventory[Item.MATH_TRAP]:
            self.active_math_problem = generate_math_problem(self.random)
            self.active_math_problem_input = []
            self.player.remove_item(Item.MATH_TRAP)
            self.queued_events.append(MathProblemStarted())
            return self.gameboard.render_math_problem(
                self.active_math_problem,
                self.active_math_problem_input,
                self.currently_typed_in_math_result,
            )

        if self.active_math_problem is not None and self.active_math_problem_input is not None:
            return self.gameboard.render_math_problem(
                self.active_math_problem, self.active_math_problem_input, self.currently_typed_in_math_result
            )

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
                if item == Item.MATH_TRAP:
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

    def attempt_player_movement(self, direction: Direction, cancel_auto_move: bool = True) -> bool:
        if cancel_auto_move:
            self.cancel_auto_move()

        self.player.facing = direction

        delta_x, delta_y = direction.value
        new_x, new_y = self.player.current_x + delta_x, self.player.current_y + delta_y

        if self.gameboard.get_entity_at(new_x, new_y).solid:
            return False

        self.player.current_x = new_x
        self.player.current_y = new_y
        return True

    def attempt_interact(self) -> bool:
        delta_x, delta_y = self.player.facing.value
        entity_x, entity_y = self.player.current_x + delta_x, self.player.current_y + delta_y

        entity = self.gameboard.get_entity_at(entity_x, entity_y)

        if isinstance(entity, InteractableMixin):
            return entity.interact(self.player)

        return False

    def attempt_fire_confetti_cannon(self) -> bool:
        if not self.player.has_item(Item.CONFETTI_CANNON):
            return False

        self.player.remove_item(Item.CONFETTI_CANNON)
        self.queued_events.append(ConfettiFired(self.player.current_x, self.player.current_y))
        return True

    def math_problem_success(self) -> None:
        self.active_math_problem = None
        self.active_math_problem_input = None
        self.queued_events.append(MathProblemSolved())

    @property
    def currently_typed_in_math_result(self) -> int | None:
        if not self.active_math_problem_input:
            return None

        number = self.active_math_problem_input[-1]
        if len(self.active_math_problem_input) == 2:
            number += self.active_math_problem_input[0] * 10

        return number

    def check_math_problem_result(self) -> None:
        if self.active_math_problem is None:
            return

        if self.currently_typed_in_math_result == self.active_math_problem.result:
            self.math_problem_success()

    def math_problem_input(self, input: int) -> None:
        if self.active_math_problem_input is None or len(self.active_math_problem_input) >= 2:
            return

        self.active_math_problem_input.append(input)
        self.check_math_problem_result()

    def math_problem_delete(self) -> None:
        if self.active_math_problem_input is None or len(self.active_math_problem_input) == 0:
            return
        self.active_math_problem_input.pop()
        self.check_math_problem_result()

    def math_problem_replace(self, input: list[int]) -> None:
        if self.active_math_problem_input is None:
            return
        self.active_math_problem_input = input[:2]
        self.check_math_problem_result()

    def input(self, input_key: Input) -> None:
        if not self.gameboard.ready:
            return

        if input_key in DIGIT_INPUTS_TO_DIGITS:
            self.math_problem_input(DIGIT_INPUTS_TO_DIGITS[input_key])
            return
        if input_key == Input.BACKSPACE:
            self.math_problem_delete()
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

    def cancel_auto_move(self) -> None:
        self.auto_target_path = []

    def queue_auto_move(self, target_x: int, target_y: int) -> None:
        self.cancel_auto_move()
        path = self.gameboard.calculate_shortest_path(self.player.current_x, self.player.current_y, target_x, target_y)
        self.auto_target_path = path

    def do_auto_move(self) -> bool:
        if not self.auto_target_path:
            return False

        target_x, target_y = self.auto_target_path.pop(0)
        movement = target_x - self.player.current_x, target_y - self.player.current_y
        direction = Direction(movement)
        moved = self.attempt_player_movement(direction, cancel_auto_move=False)

        if moved:
            return True

        # We are attempting to interact with something on the path.
        # First, make the player face it.
        if self.player.facing != direction:
            self.player.facing = direction
            self.auto_target_path.insert(0, (target_x, target_y))
            return True

        # If we are facing it, attempt to interact with it.
        changed = self.attempt_interact()

        if not changed:
            self.cancel_auto_move()
            return False

        # If the interaction was successful, and this was the end of the path, stop
        # (i.e. don't try to attack the attacked enemy over and over until it's dead)
        if not self.auto_target_path:
            self.cancel_auto_move()
            return True

        # If there is more to go, keep going along the path
        self.auto_target_path.insert(0, (target_x, target_y))
        return True
