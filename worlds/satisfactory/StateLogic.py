from typing import Optional, Callable, ClassVar, Tuple
from collections.abc import Iterable
from BaseClasses import CollectionState
from .GameLogic import Recipe, PowerInfrastructureLevel
from .Options import SatisfactoryOptions
from .CriticalPathCalculator import CriticalPathCalculator

EventId: Optional[int] = None

part_event_prefix = "Can Produce: "
building_event_prefix = "Can Build: "


def true_rule(_: CollectionState) -> bool:
    return True


def to_part_event(part: str) -> str:
    return part_event_prefix + part


def to_building_event(part: str) -> str:
    return building_event_prefix + part


def to_belt_name(power_level: int) -> str:
    return "Conveyor Mk." + str(power_level)


class StateLogic:
    player: int
    options: SatisfactoryOptions
    critical_path: CriticalPathCalculator
    initial_unlocked_items: set[str]

    pipe_events: ClassVar[tuple[str, str]] = \
        tuple(to_building_event(building) for building in ("Pipes Mk.1", "Pipes Mk.2"))
    pump_events: ClassVar[tuple[str, str]] = \
        tuple(to_building_event(building) for building in ("Pipeline Pump Mk.1", "Pipeline Pump Mk.2"))
    hazmat_events: ClassVar[tuple[str, str]] = \
        tuple(to_part_event(part) for part in ("Hazmat Suit", "Iodine-Infused Filter"))
    belt_events: ClassVar[tuple[tuple[str, ...], ...]] = tuple(
        tuple(map(to_building_event, map(to_belt_name, range(speed, 6))))
        for speed in range(1, 6)
    )

    pipes_rule: Callable[[CollectionState], bool]
    radio_active_rule: Callable[[CollectionState], bool]
    belt_rules: Tuple[Callable[[CollectionState], bool], ...]

    def __init__(self, player: int, options: SatisfactoryOptions, critical_path: CriticalPathCalculator):
        self.player = player
        self.options = options
        self.critical_path = critical_path

        self.pipes_rule = self.get_requires_pipes_rule()
        self.radio_active_rule = self.get_requires_hazmat_rule()
        self.belt_rule = tuple(self.get_belt_speed_rule(speed) for speed in range(1, 6))

    def has_recipe(self, state: CollectionState, recipe: Recipe) -> bool:
        return state.has(recipe.name, self.player) or recipe.name in self.critical_path.implicitly_unlocked

    def can_build(self, state: CollectionState, building_name: Optional[str]) -> bool:
        return building_name is None or state.has(building_event_prefix + building_name, self.player)

    def can_build_any(self, state: CollectionState, building_names: Optional[Iterable[str]]) -> bool:
        return building_names is None or \
            state.has_any(map(to_building_event, building_names), self.player)

    def can_build_all(self, state: CollectionState, building_names: Optional[Iterable[str]]) -> bool:
        return building_names is None or \
            state.has_all(map(to_building_event, building_names), self.player)

    def can_produce(self, state: CollectionState, part_name: Optional[str]) -> bool:
        return part_name is None or state.has(part_event_prefix + part_name, self.player)

    def can_power(self, state: CollectionState, power_level: Optional[PowerInfrastructureLevel]) -> bool:
        return power_level is None or state.has(building_event_prefix + power_level.to_name(), self.player)

    def can_produce_all(self, state: CollectionState, parts: Optional[Iterable[str]]) -> bool:
        return parts is None or \
            state.has_all(map(to_part_event, parts), self.player)

    def has_obtained_all(self, state: CollectionState, items: Optional[Iterable[str]]) -> bool:
        if not items:
            return True
        else:
            return state.has_all(items, self.player)

    def can_handcraft_single_part(self, state: CollectionState, part: str) -> bool:
        if self.can_produce(state, part):
            return True

        if part not in self.critical_path.handcraftable_parts:
            return False

        recipes: list[Recipe] = self.critical_path.handcraftable_parts[part]
        return any(
            self.has_recipe(state, recipe)
            and (not recipe.inputs or all(
                self.can_handcraft_single_part(state, recipe_part)
                for recipe_part in recipe.inputs))
            for recipe in recipes)

    def get_can_produce_all_allowing_handcrafting_rule(self, parts: Optional[Iterable[str]]) \
            -> Callable[[CollectionState], bool]:
        if not parts:
            return true_rule

        return lambda state: all(self.can_handcraft_single_part(state, part) for part in parts)

    def get_requires_pipes_rule(self) -> Callable[[CollectionState], bool]:
        return lambda state: \
            state.has_any(self.pipe_events, self.player) and state.has_any(self.pump_events, self.player)

    def get_requires_hazmat_rule(self) -> Callable[[CollectionState], bool]:
        return lambda state: state.has_all(self.hazmat_events, self.player)

    def get_belt_speed_rule(self, belt_speed: int) -> Callable[[CollectionState], bool]:
        return lambda state: state.has_any(self.belt_events[belt_speed], self.player)

    def is_recipe_producible(self, state: CollectionState, recipe: Recipe) -> bool:
        return self.has_recipe(state, recipe) \
               and self.can_build(state, recipe.building) \
               and self.can_produce_all(state, recipe.inputs)

    def get_can_produce_specific_recipe_for_part_rule(self, recipe: Recipe) -> Callable[[CollectionState], bool]:
        if recipe.needs_pipes:
            if recipe.is_radio_active:
                if recipe.minimal_belt_speed:
                    return lambda state: \
                        self.is_recipe_producible(state, recipe) \
                        and self.pipes_rule(state) \
                        and self.radio_active_rule(state) \
                        and self.belt_rule[recipe.minimal_belt_speed - 1]
                else:
                    return lambda state: \
                        self.is_recipe_producible(state, recipe) \
                        and self.pipes_rule(state) \
                        and self.radio_active_rule(state)
            else:
                if recipe.minimal_belt_speed:
                    return lambda state: \
                        self.is_recipe_producible(state, recipe) \
                        and self.pipes_rule(state) \
                        and self.belt_rule[recipe.minimal_belt_speed - 1]
                else:
                    return lambda state: \
                        self.is_recipe_producible(state, recipe) \
                        and self.pipes_rule(state)
        else:
            if recipe.is_radio_active:
                if recipe.minimal_belt_speed:
                    return lambda state: \
                        self.is_recipe_producible(state, recipe) \
                        and self.radio_active_rule(state) \
                        and self.belt_rule[recipe.minimal_belt_speed - 1]
                else:
                    return lambda state: \
                        self.is_recipe_producible(state, recipe) \
                        and self.radio_active_rule(state)
            else:
                if recipe.minimal_belt_speed:
                    return lambda state: \
                        self.is_recipe_producible(state, recipe) \
                        and self.belt_rule[recipe.minimal_belt_speed - 1]
                else:
                    return lambda state: \
                        self.is_recipe_producible(state, recipe)

    def is_elevator_phase(self, state: CollectionState, phase: int) -> bool:
        limited_phase = min(self.options.final_elevator_phase - 1, phase)

        if limited_phase != 0:
            return state.has(f"Elevator Phase {limited_phase}", self.player)
        else:
            return True
