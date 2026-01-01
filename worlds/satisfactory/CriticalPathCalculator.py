from random import Random
from typing import Optional
from collections.abc import Iterable
from .GameLogic import GameLogic, Recipe
from .Options import SatisfactoryOptions


class CriticalPathCalculator:
    logic: GameLogic
    random: Random
    final_elevator_phase: int
    randomize_starter_recipes: bool

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
    tier_0_recipes: set[str]

    def __init__(self, logic: GameLogic, seed: float, options: SatisfactoryOptions):
        self.logic = logic
        self.random = Random(seed)
        self.final_elevator_phase = options.final_elevator_phase.value
        self.randomize_starter_recipes = bool(options.randomize_starter_recipes.value)

    def calculate(self) -> None:
        self.required_parts = set[str]()
        self.required_buildings = set[str]()
        self.required_power_level: int = 1

        self.__potential_required_belt_speed = 1

        self.configure_implicitly_unlocked_and_handcraftable_parts()

        self.select_minimal_required_parts_for(
            self.logic.space_elevator_phases[self.final_elevator_phase-1].keys())

        for tree in self.logic.man_trees.values():
            self.select_minimal_required_parts_for(tree.access_items)

            for node in tree.nodes:
                if node.minimal_phase > self.final_elevator_phase:
                    continue

                self.select_minimal_required_parts_for(node.unlock_cost)

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

        if self.logic.recipes["Uranium"][0].minimal_phase <= self.final_elevator_phase:
            self.select_minimal_required_parts_for(("Hazmat Suit", "Iodine-Infused Filter"))

        for i in range(1, self.__potential_required_belt_speed + 1):
            self.select_minimal_required_parts_for_building(f"Conveyor Mk.{i}")

        for i in range(1, self.required_power_level + 1):
            power_recipe = self.random.choice(self.logic.requirement_per_powerlevel[i])
            self.select_minimal_required_parts_for(power_recipe.inputs)
            self.select_minimal_required_parts_for_building(power_recipe.building)

        self.required_item_names = {
            recipe.name
            for part in self.required_parts
            for recipe in self.logic.recipes[part]
            if recipe.minimal_phase <= self.final_elevator_phase
        }
        self.required_item_names.update({"Building: " + building for building in self.required_buildings})

        self.calculate_excluded_things()
        self.select_starter_recipes()

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
                if recipe.minimal_phase > self.final_elevator_phase:
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
        self.parts_to_exclude = set[str]()
        self.buildings_to_exclude = set[str]()
        self.recipes_to_exclude = {
            recipe.name
            for part in self.logic.recipes
            for recipe in self.logic.recipes[part]
            if recipe.minimal_phase > self.final_elevator_phase
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
                    for recipes_per_part in self.logic.recipes.values()
                    for recipe_per_part in recipes_per_part
                    if recipe_per_part.building in new_buildings_to_exclude
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

    def select_starter_recipes(self) -> None:
        # cable is left unaffected as all its alternative recipes require refinery
        if not self.randomize_starter_recipes:
            self.tier_0_recipes = {
                "Recipe: Iron Ingot",
                "Recipe: Iron Plate",
                "Recipe: Iron Rod",
                "Recipe: Copper Ingot",
                "Recipe: Wire",
                "Recipe: Concrete",
                "Recipe: Screw",
                "Recipe: Reinforced Iron Plate"
            }
        else:
            # we only allow basic parts to be made without the need of refineries
            # could be made more based of GameLogic rather than hardcoded but this is likely faster
            # would likely need to be based of GameLogic when we add mod support
            self.tier_0_recipes = set()

            self.tier_0_recipes.add(self.random.choice(
                ("Recipe: Iron Ingot", "Recipe: Basic Iron Ingot", "Recipe: Iron Alloy Ingot")))

            selected_recipe = self.random.choice(
                ("Recipe: Iron Plate", "Recipe: Iron Plate", "Recipe: Iron Plate", "Recipe: Steel Cast Plate"))
            self.tier_0_recipes.add(selected_recipe)
            if selected_recipe == "Recipe: Steel Cast Plate":
                self.add_steel_ingot_to_starter_recipes()

            selected_recipe = self.random.choice(
                ("Recipe: Iron Rod", "Recipe: Iron Rod", "Recipe: Iron Rod", "Recipe: Steel Rod"))
            self.tier_0_recipes.add(selected_recipe)
            if selected_recipe == "Recipe: Steel Rod":
                self.add_steel_ingot_to_starter_recipes()

            self.tier_0_recipes.add(self.random.choice(("Recipe: Copper Ingot", "Recipe: Copper Alloy Ingot")))

            selected_recipe = self.random.choice(
                ("Recipe: Wire", "Recipe: Caterium Wire", "Recipe: Fused Wire", "Recipe: Iron Wire"))
            self.tier_0_recipes.add(selected_recipe)
            if selected_recipe in {"Recipe: Caterium Wire", "Recipe: Fused Wire"}:
                # add Caterium Ingot
                self.tier_0_recipes.add("Recipe: Caterium Ingot")

            selected_recipe = self.random.choice(("Recipe: Concrete", "Recipe: Fine Concrete"))
            self.tier_0_recipes.add(selected_recipe)
            if selected_recipe == "Recipe: Fine Concrete":
                # add Silica
                self.tier_0_recipes.add(self.random.choice(("Recipe: Silica", "Recipe: Cheap Silica")))

            selected_recipe = self.random.choice(
                ("Recipe: Screw", "Recipe: Screw", "Recipe: Cast Screw", "Recipe: Cast Screw", "Recipe: Steel Screw"))

            self.tier_0_recipes.add(selected_recipe)
            if selected_recipe == "Recipe: Steel Screw":
                # add Steel Beam and steel Ingot
                self.add_steel_ingot_to_starter_recipes()
                self.tier_0_recipes.add(self.random.choice(("Recipe: Steel Beam", "Recipe: Molded Beam")))

            self.tier_0_recipes.add(self.random.choice(
                ("Recipe: Reinforced Iron Plate", "Recipe: Bolted Iron Plate", "Recipe: Stitched Iron Plate")))

        for part, recipes in self.logic.recipes.items():
            for recipe in recipes:
                if recipe.name in self.tier_0_recipes:
                    if part in self.handcraftable_parts:
                        self.handcraftable_parts[part].append(recipe)
                    else:
                        self.handcraftable_parts[part] = [recipe]
                    self.tier_0_recipes.add(self.logic.buildings[recipe.building].name)

        self.implicitly_unlocked.update(self.tier_0_recipes)

    def add_steel_ingot_to_starter_recipes(self) -> None:
        if "Recipe: Steel Ingot" not in self.tier_0_recipes \
                and "Recipe: Compacted Steel Ingot" not in self.tier_0_recipes \
                and "Recipe: Solid Steel Ingot" not in self.tier_0_recipes:

            selected_recipe = self.random.choice(
                ("Recipe: Steel Ingot", "Recipe: Compacted Steel Ingot", "Recipe: Solid Steel Ingot"))

            self.tier_0_recipes.add(selected_recipe)

            if selected_recipe == "Recipe: Compacted Steel Ingot":
                self.tier_0_recipes.add("Recipe: Compacted Coal")
