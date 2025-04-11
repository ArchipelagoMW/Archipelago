from random import Random
from typing import Optional
from collections.abc import Iterable
from .GameLogic import GameLogic, Recipe
from .Options import SatisfactoryOptions
from .Options import SatisfactoryOptions

class CriticalPathCalculator:
    logic: GameLogic
    random: Random
    options: SatisfactoryOptions

    required_parts: set[str]
    required_buildings: set[str]
    required_item_names: set[str]
    required_power_level: int

    __potential_required_belt_speed: int

    parts_to_exclude: set[str]
    recipes_to_exclude: set[str]
    buildings_to_exclude: set[str]

    implicitly_unlocked: set[str]
    handcraftable_parts: dict[str, list[Recipe]]

    def __init__(self, logic: GameLogic, random: Random, options: SatisfactoryOptions):
        self.logic = logic
        self.random = random
        self.options = options

        self.required_parts = set()
        self.required_buildings = set()
        self.required_power_level: int = 1

        self.__potential_required_belt_speed = 1

        selected_power_infrastructure: dict[int, Recipe] = {}
        

        self.configure_implicitly_unlocked_and_handcraftable_parts()

        self.select_minimal_required_parts_for(self.logic.space_elevator_tiers[options.final_elevator_package-1].keys())

        for tree in self.logic.man_trees.values():
            self.select_minimal_required_parts_for(tree.access_items)

            for node in tree.nodes:
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
        self.select_minimal_required_parts_for_building("Miner Mk.2")
        self.select_minimal_required_parts_for_building("Pipes Mk.1")
        self.select_minimal_required_parts_for_building("Pipes Mk.2")
        self.select_minimal_required_parts_for_building("Pipeline Pump Mk.1")
        self.select_minimal_required_parts_for_building("Pipeline Pump Mk.2")

        if self.logic.recipes["Uranium"][0].minimal_tier <= options.final_elevator_package:
            self.select_minimal_required_parts_for(("Hazmat Suit", "Iodine-Infused Filter"))

        for i in range(1, self.__potential_required_belt_speed + 1):
            self.select_minimal_required_parts_for_building(f"Conveyor Mk.{i}")

        for i in range(1, self.required_power_level + 1):
            power_recipe = random.choice(self.logic.requirement_per_powerlevel[i])
            selected_power_infrastructure[i] = power_recipe
            self.select_minimal_required_parts_for(power_recipe.inputs)
            self.select_minimal_required_parts_for_building(power_recipe.building)

        self.required_item_names = {
            recipe.name 
            for part in self.required_parts
            for recipe in self.logic.recipes[part]
            if recipe.minimal_tier <= self.options.final_elevator_package
        }
        self.required_item_names.update({"Building: "+ building for building in self.required_buildings})

        self.calculate_excluded_things()


    def select_minimal_required_parts_for_building(self, building: str) -> None:
        self.select_minimal_required_parts_for(self.logic.buildings[building].inputs)
        self.required_buildings.add(building)


    def select_minimal_required_parts_for(self, parts: Optional[Iterable[str]]) -> None:
        if parts is None:
            return

        for part in parts:
            if part in self.required_parts:
                continue

            self.required_parts.add(part)

            for recipe in self.logic.recipes[part]:
                if recipe.minimal_tier > self.options.final_elevator_package:
                    continue

                self.__potential_required_belt_speed = \
                    max(self.__potential_required_belt_speed, recipe.minimal_belt_speed)

                self.select_minimal_required_parts_for(recipe.inputs)

                if recipe.building:
                    self.select_minimal_required_parts_for(self.logic.buildings[recipe.building].inputs)
                    self.required_buildings.add(recipe.building)

                    if self.logic.buildings[recipe.building].power_requirement:
                        self.required_power_level = \
                            max(self.required_power_level, 
                                self.logic.buildings[recipe.building].power_requirement)


    def calculate_excluded_things(self) -> None:
        self.parts_to_exclude = set()
        self.buildings_to_exclude = set()
        self.recipes_to_exclude = {
            recipe.name
            for part in self.logic.recipes
            for recipe in self.logic.recipes[part]
            if recipe.minimal_tier > self.options.final_elevator_package
        }

        excluded_count = len(self.recipes_to_exclude)
        while True:
            for part in self.logic.recipes:
                if part in self.parts_to_exclude:
                    continue

                for recipe in self.logic.recipes[part]:
                    if recipe.name in self.recipes_to_exclude:
                        continue

                    if recipe.inputs and any(input in self.parts_to_exclude for input in recipe.inputs):
                        self.recipes_to_exclude.add(recipe.name)

                if all(r.name in self.recipes_to_exclude for r in self.logic.recipes[part]):
                    self.parts_to_exclude.add(part)

                new_buildings_to_exclude = {
                    building_name
                    for building_name, building in self.logic.buildings.items()
                    if building_name not in self.buildings_to_exclude 
                        and building.inputs and any(input in self.parts_to_exclude for input in building.inputs)
                }

                self.recipes_to_exclude.update({
                    recipe_per_part.name
                    for building_to_exclude in new_buildings_to_exclude
                    for recipes_per_part in self.logic.recipes.values()
                    for recipe_per_part in recipes_per_part
                    if recipe_per_part.building == building_to_exclude
                })

                self.buildings_to_exclude.update(new_buildings_to_exclude)

            new_length = len(self.recipes_to_exclude)
            if new_length == excluded_count:
                break
            excluded_count = new_length


    def configure_implicitly_unlocked_and_handcraftable_parts(self) -> None:
        self.implicitly_unlocked: set[str] = { 
            recipe.name
            for recipes_per_part in self.logic.recipes.values()
            for recipe in recipes_per_part if recipe.implicitly_unlocked 
        }
        self.implicitly_unlocked.update({ 
            building.name
            for building in self.logic.buildings.values() if building.implicitly_unlocked 
        })

        self.handcraftable_parts: dict[str, list[Recipe]] = {}
        for part, recipes_per_part in self.logic.recipes.items():
            for recipe in recipes_per_part:
                if recipe.handcraftable:
                    self.handcraftable_parts.setdefault(part, []).append(recipe)

        if self.options.randomize_tier_0:
            pass
            #decide what to re-randomize, like smelter / iron ingot etc
            #self.implicitly_unlocked.remove("") 