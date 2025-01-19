from typing import Tuple, List, Optional, Set, Iterable
from BaseClasses import CollectionState
from .GameLogic import GameLogic, Recipe, PowerInfrastructureLevel
from .Options import SatisfactoryOptions

EventId: Optional[int] = None

part_event_prefix = "Can Produce: "
building_event_prefix = "Can Build: "

class StateLogic:
    player: int
    options: SatisfactoryOptions
    initial_unlocked_items: Set[str]

    def __init__(self, player: int, options: SatisfactoryOptions):
        self.player = player
        self.options = options

    def has_recipe(self, state: CollectionState, recipe: Recipe):
        return recipe.implicitly_unlocked or state.has(recipe.name, self.player)
    
    def can_build(self, state: CollectionState, building_name: Optional[str]) -> bool:
        return building_name is None or state.has(building_event_prefix + building_name, self.player)
    
    def can_build_any(self, state: CollectionState, building_names: Optional[Iterable[str]]) -> bool:
        return building_names is None or \
            state.has_any(map(self.to_building_event, building_names), self.player)
    
    def can_build_all(self, state: CollectionState, building_names: Optional[Iterable[str]]) -> bool:
        return building_names is None or \
            state.has_all(map(self.to_building_event, building_names), self.player)

    def can_produce(self, state: CollectionState, part_name: Optional[str]) -> bool:
        return part_name is None or state.has(part_event_prefix + part_name, self.player)
    
    def can_power(self, state: CollectionState, power_level: Optional[PowerInfrastructureLevel]) -> bool:
        return power_level is None or state.has(building_event_prefix + power_level.to_name(), self.player)

    def can_produce_all(self, state: CollectionState, parts: Optional[Iterable[str]]) -> bool:
        if parts and "SAM" in parts:
            debug = "Now"

        return parts is None or \
            state.has_all(map(self.to_part_event, parts), self.player)

    def can_produce_all_allowing_handcrafting(self, state: CollectionState, logic: GameLogic, 
            parts: Optional[Tuple[str, ...]]) -> bool:
        
        def can_handcraft_part(part: str) -> bool:
            if self.can_produce(state, part):
                return True
            elif part not in logic.handcraftable_recipes:
                return False

            recipes: List[Recipe] = logic.handcraftable_recipes[part]

            return any(
                self.has_recipe(state, recipe) 
                    and (not recipe.inputs or self.can_produce_all_allowing_handcrafting(state, logic, recipe.inputs))
                for recipe in recipes)

        return not parts or all(can_handcraft_part(part) for part in parts)

    def can_produce_specific_recipe_for_part(self, state: CollectionState, recipe: Recipe) -> bool:
        if recipe.needs_pipes and (
                not self.can_build_any(state, ("Pipes Mk.1", "Pipes Mk.2")) or
                not self.can_build_any(state, ("Pipeline Pump Mk.1", "Pipeline Pump Mk.2"))):
            return False
        
        if recipe.is_radio_active and not self.can_produce_all(state, ("Hazmat Suit", "Iodine Infused Filter")): 
            return False
        
        if not self.options.experimental_generation and recipe.minimal_belt_speed and \
                not self.can_build_any(state, map(self.to_belt_name, range(recipe.minimal_belt_speed, 6))):
            return False

        return self.has_recipe(state, recipe) \
            and self.can_build(state, recipe.building) \
            and self.can_produce_all(state, recipe.inputs)
    
    def is_game_phase(self, state: CollectionState, phase: int) -> bool:
        return state.has(f"Elevator Tier {phase}", self.player)
    
    @staticmethod
    def to_part_event(part: str) -> str:
        return part_event_prefix + part

    @staticmethod
    def to_building_event(part: str) -> str:
        return building_event_prefix + part
    
    @staticmethod
    def to_belt_name(power_level: int) -> str:
        return "Conveyor Mk." + str(power_level)
