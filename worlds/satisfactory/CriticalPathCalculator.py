from random import Random
from typing import Optional
from collections.abc import Iterable
from .GameLogic import GameLogic, Recipe
from .Options import SatisfactoryOptions
from .Options import SatisfactoryOptions

class CriticalPathCalculator:
    logic: GameLogic
    random: Random

    potential_required_parts: set[str]
    potential_required_buildings: set[str]
    potential_required_belt_speed: int
    potential_required_pipes: bool
    potential_required_radioactive: bool
    potential_required_power: int
    potential_required_recipes_names: set[str]

    def __init__(self, logic: GameLogic, random: Random, options: SatisfactoryOptions):
        self.logic = logic
        self.random = random
        self.options = options

        self.potential_required_parts = set()
        self.potential_required_buildings = set()
        self.potential_required_belt_speed = 1
        self.potential_required_pipes = False
        self.potential_required_radioactive = False
        self.potential_required_power: int = 1

        selected_power_infrastructure: dict[int, Recipe] = {}

        self.select_minimal_required_parts_for(self.logic.space_elevator_tiers[options.final_elevator_package-1].keys())

        for tree in self.logic.man_trees.values():
            self.select_minimal_required_parts_for(tree.access_items)

            for node in tree.nodes:
                # Bullet Guidance System - Rifle Ammo
                # Stun Rebar - Iron Rebar
                # Radar Technology - Heavy Modular Frame
                # Turbo Rifle Ammo - Packaged Turbofuel, Rifle Ammo
                # Nuclear Deterrent Development - Encased Uranium Cell
                # Rocket Fuel - Packaged Turbofuel
                # Ionized Fuel - Ionized Fuel
                if node.name == "Hostile Organism Detection":
                    Debug = True

                if node.minimal_tier > options.final_elevator_package:
                    continue

                self.select_minimal_required_parts_for(node.unlock_cost.keys())

        self.select_minimal_required_parts_for_building("MAM")
        self.select_minimal_required_parts_for_building("AWESOME Sink")
        self.select_minimal_required_parts_for_building("AWESOME Shop")
        self.select_minimal_required_parts_for_building("Space Elevator")
        self.select_minimal_required_parts_for_building("Conveyor Splitter")
        self.select_minimal_required_parts_for_building("Conveyor Merger")
        self.select_minimal_required_parts_for_building("Equipment Workshop")
        self.select_minimal_required_parts_for_building("Foundation")
        self.select_minimal_required_parts_for_building("Walls Orange")
        self.select_minimal_required_parts_for_building("Power Storage")

        for i in range(1, self.potential_required_belt_speed + 1):
            self.select_minimal_required_parts_for_building(f"Conveyor Mk.{i}")
        if self.potential_required_pipes:
            self.select_minimal_required_parts_for_building("Pipes Mk.1")
            self.select_minimal_required_parts_for_building("Pipeline Pump Mk.1")
        if self.potential_required_radioactive:
            self.select_minimal_required_parts_for(self.logic.recipes["Hazmat Suit"][0].inputs)
            self.select_minimal_required_parts_for(self.logic.recipes["Iodine Infused Filter"][0].inputs)
        for i in range(1, self.potential_required_power + 1):
            power_recipe = random.choice(self.logic.requirement_per_powerlevel[i])
            selected_power_infrastructure[i] = power_recipe
            self.select_minimal_required_parts_for(power_recipe.inputs)
            self.select_minimal_required_parts_for_building(power_recipe.building)

        self.potential_required_recipes_names = set(
            recipe.name 
            for part in self.potential_required_parts
            for recipe in self.logic.recipes[part]
            if recipe.minimal_tier <= self.options.final_elevator_package
        )
        self.potential_required_recipes_names.update(
            "Building: "+ building
            for building in self.potential_required_buildings
        )

        debug = True

    def select_minimal_required_parts_for_building(self, building: str) -> None:
        self.select_minimal_required_parts_for(self.logic.buildings[building].inputs)
        self.potential_required_buildings.add(building)

    def select_minimal_required_parts_for(self, parts: Optional[Iterable[str]]) -> None:
        if parts is None:
            return

        for part in parts:
            if part in self.potential_required_parts:
                continue

            if part == "Radio Control Unit":
                Debug = True

            self.potential_required_parts.add(part)

            for recipe in self.logic.recipes[part]:
                if part == "Fuel":
                    Debug = True

                if recipe.minimal_tier > self.options.final_elevator_package:
                    continue

                if recipe.minimal_belt_speed == 5:
                    Debug = True

                self.potential_required_belt_speed = \
                    max(self.potential_required_belt_speed, recipe.minimal_belt_speed)

                self.select_minimal_required_parts_for(recipe.inputs)

                if recipe.needs_pipes:
                    self.potential_required_pipes = True
                if recipe.is_radio_active:
                    self.potential_required_radioactive = True

                if recipe.building:
                    if recipe.building == "Blender":
                        debug = True

                    self.select_minimal_required_parts_for(self.logic.buildings[recipe.building].inputs)
                    self.potential_required_buildings.add(recipe.building)

                    if self.logic.buildings[recipe.building].power_requirement:
                        self.potential_required_power = \
                            max(self.potential_required_power, 
                                self.logic.buildings[recipe.building].power_requirement)

        debug = True