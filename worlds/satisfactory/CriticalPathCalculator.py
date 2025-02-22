from random import Random
from typing import Set, Tuple
from .GameLogic import GameLogic, Recipe
from .Options import SatisfactoryOptions
from .Options import SatisfactoryOptions

class CriticalPathCalculator:
    logic: GameLogic
    random: Random

    potential_required_parts: Set[str]
    potential_required_buildings: Set[str]
    potential_required_belt_speed: int
    potential_required_pipes: bool
    potential_required_radioactive: bool
    potential_required_power: int
    potential_required_recipes_names: Set[str]

    def __init__(self, logic: GameLogic, random: Random, options: SatisfactoryOptions):
        self.logic = logic
        self.random = random

        self.potential_required_parts = set()
        self.potential_required_buildings = set()
        self.potential_required_belt_speed = 1
        self.potential_required_pipes = False
        self.potential_required_radioactive = False
        self.potential_required_power: int = 1

        self.select_minimal_required_parts_for(
            tuple(self.logic.space_elevator_tiers[options.final_elevator_package - 1].keys())
        )
        for i in range(self.potential_required_belt_speed, 1):
            self.select_minimal_required_parts_for(self.logic.buildings[f"Conveyor Mk.{i}"].inputs)
        if self.potential_required_pipes:
            self.select_minimal_required_parts_for(self.logic.buildings["Pipeline Pump Mk.1"].inputs)
            self.select_minimal_required_parts_for(self.logic.buildings["Pipeline Pump Mk.2"].inputs)
        if self.potential_required_radioactive:
            self.select_minimal_required_parts_for(self.logic.recipes["Hazmat Suit"][0].inputs)
            self.select_minimal_required_parts_for(self.logic.recipes["Iodine Infused Filter"][0].inputs)
        for i in range(self.potential_required_belt_speed, 1):
            power_recipe = random.choice(self.logic.requirement_per_powerlevel[i])
            self.select_minimal_required_parts_for(power_recipe.inputs)
            self.potential_required_buildings.add(power_recipe.building)
        

        self.potential_required_recipes_names = set(
            recipe.name 
            for part in self.potential_required_parts
            for recipe in self.logic.recipes[part]
        )
        self.potential_required_recipes_names.update(
            "Building: "+ building
            for building in self.potential_required_buildings
        )

        debug = True


    def select_minimal_required_parts_for(self, parts: Tuple[str]) -> None:
        if parts:
            for part in parts:
                if part in self.potential_required_parts:
                    continue

                self.potential_required_parts.add(part)

                for recipe in self.logic.recipes[part]:
                    self.potential_required_belt_speed = \
                        max(self.potential_required_belt_speed, recipe.minimal_belt_speed)

                    self.select_minimal_required_parts_for(recipe.inputs)
                    self.select_minimal_required_parts_for(self.logic.buildings[recipe.building].inputs)

                    self.potential_required_buildings.add(recipe.building)

                    if self.logic.buildings[recipe.building].power_requirement:
                        self.potential_required_power = \
                            max(self.potential_required_power, self.logic.buildings[recipe.building].power_requirement)