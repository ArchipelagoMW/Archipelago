from __future__ import annotations

import json
from functools import cached_property
from typing import TYPE_CHECKING, Callable

# All of this needs redoing to be more modular

if TYPE_CHECKING:
    from . import Technology, FactorioModpack

from .FactorioUtils import FactorioElement

Category = str

def ingredient_score(ingredients: dict[InternalItem, float]):
    cost = 0

    for ingredient, amount in ingredients.items():
        cost += ingredient.get_score() * amount
    return cost

class RecipeEngine:
    def __init__(self, modpack: "FactorioModpack"):
        self.modpack = modpack
        self.__all_ingredients: dict[str, InternalItem] | None = None
        self.__valid_ingredients: dict[str, InternalItem] | None = None
        self.__fluids: set[str] | None = None
        self.__recipes: dict[str, Recipe] | None = None
        self.__imported_recipes: dict[str, Recipe] | None = None
        self.__pack_custom_recipes: dict[str, Recipe] | None = None
        self.__machines: dict[str, Machine] | None = None

        self.__recipe_sources: dict[str, set[Technology]] | None = None
        self.__mining_with_fluid_sources: set[Technology] | None = None

        self.__root_categories: set[str] | None = None
        self.__missed_machines: dict[str, set[Category]] | None = None
        self.__raw_cost: dict[str, float] | None = None
        self.__invalid_ingredients: set[str] | None = None
        self.__req_machines_for_category: dict[Category, str] | None = None
        self.__excluded_automation_ingredients: set[str] | None = None

        self.__current_recipe_path: list[tuple[InternalItem, Recipe]] = []

    def full_init(self) -> None:
        try:
            with self.modpack.open_file("Cache/precalc.json") as file:
                precalc = json.load(file)
            for item_name, result in precalc.items():
                item = self.all_ingredients[item_name]
                item.set_cache({self.all_ingredients[ingredient_name]: cost for ingredient_name, cost in result["raw_ingredients"].items()},
                               self.recipes[result["best_recipe"]] if result["best_recipe"] else None,
                               {self.modpack.technology_table[tech] for tech in result["technologies"]},
                               set(result["category"]))
        except FileNotFoundError:
            self.modpack.logger.debug("No precalc.json found")

    def __load_settings(self) -> None:
        with self.modpack.open_file("recipeEngineSettings.json") as file:
            raw_settings = json.load(file)
            self.__root_categories: set[str] = raw_settings["root_categories"]
            self.__missed_machines: dict[str, set[Category]] = {name: set(categories)
                                                                for name, categories in raw_settings["missed_machines"].items()}
            self.__raw_cost: dict[str, float] = raw_settings["raw_cost"]
            self.__invalid_ingredients: set[str] = raw_settings["invalid_ingredients"]
            self.__req_machines_for_category: dict[Category, str] = raw_settings["req_machines_for_category"]
            self.__excluded_automation_ingredients: set[str] = raw_settings.get("excluded_automation_ingredients", set())

    def __register_iternal_items(self) -> None:
        invalid_items = {"pistol", "fluid-unknown"} | {f"parameter-{i}" for i in range(10)}

        self.__all_ingredients: dict[str, InternalItem] = {}
        self.__valid_ingredients: dict[str, InternalItem] = {}

        with self.modpack.open_file("fluids.json") as file:
            self.__fluids: set[str] = set(json.load(file))

        for fluid in self.__fluids:
            if fluid in invalid_items:
                continue
            ingredient = InternalItem(fluid, True, self)
            self.__all_ingredients[fluid] = ingredient
            self.__valid_ingredients[fluid] = ingredient

        with self.modpack.open_file("items.json") as file:
            item_stack_sizes: dict[str, int] = json.load(file)

        for item, stack_size in item_stack_sizes.items():
            if item in invalid_items:
                continue
            ingredient = InternalItem(item, False, self)
            self.__all_ingredients[item] = ingredient
            if stack_size > 1 and ingredient.name not in self.modpack.ordered_science_packs:
                self.__valid_ingredients[item] = ingredient

        self.__all_ingredients["rocket-part"] = InternalItem("rocket-part", False, self)

    def __register_recipe_sources(self) -> None:
        self.__recipe_sources: dict[str, set[Technology]] = {}
        mining_with_fluid_sources: set[Technology] = set()
        for technology in self.modpack.base_technology_table.values():
            for recipe_name in technology.unlocks:
                self.__recipe_sources.setdefault(recipe_name, set()).add(technology)
            if "mining-with-fluid" in technology.modifiers:
                mining_with_fluid_sources.add(technology)

        with self.modpack.open_file("resources.json") as file: # todo find better method then opening twice
            raw_resources = json.load(file)

        for resource_name, resource_data in raw_resources.items():
            if "required_fluid" in resource_data:
                self.__recipe_sources[f"mining-{resource_name}"] = mining_with_fluid_sources

    def __register_recipes(self):
        self.__recipes: dict[str, Recipe] = {}

        with self.modpack.open_file("resources.json") as file:  # todo find better method then opening twice
            raw_resources = json.load(file)

        for resource_name, resource_data in raw_resources.items():
            self.__add_recipe(
                f"mining-{resource_name}",
                resource_data["category"],
                {resource_data["required_fluid"]: resource_data["fluid_amount"]}
                if "required_fluid" in resource_data else {},
                {data["name"]: data["amount"] for data in resource_data["products"].values()},
                resource_data["mining_time"]
            )
        del raw_resources

        with self.modpack.open_file("recipes.json") as file:
            raw_recipes = json.load(file)

        for recipe_name, recipe_data in raw_recipes.items():
            # example:
            # "accumulator":{"ingredients":{"iron-plate":2,"battery":5},"products":{"accumulator":1},"category":"crafting"}
            # FIXME: add mining?
            if (("barrel" in recipe_data["products"] and recipe_name != "barrel")
                    or ("bob-gas-canister" in recipe_data["products"] and recipe_name != "bob-gas-canister")
                    or ("bob-empty-canister" in recipe_data["products"] and recipe_name != "bob-empty-canister")
                    or (recipe_data["category"] == "parameters")): # todo add custom canisters somewhere to skip
                continue

            self.__add_recipe(recipe_name, recipe_data["category"],
                              recipe_data["ingredients"], recipe_data["products"],
                              recipe_data.get("energy", 0))

        del raw_recipes
        self.__imported_recipes: dict[str, Recipe] = self.__recipes.copy()

        try:
            with self.modpack.open_file("customRecipes.json") as file:
                raw_custom = json.load(file)
        except FileNotFoundError:
            raw_custom = {}

        self.__pack_custom_recipes: dict[str, Recipe] = {}
        for recipe_name, recipe_data in raw_custom.items():
            # TODO add optional crafting_machine_tints
            # TODO add group for AP recipes
            # TODO add support for custom techs for recipes
            recipe = Recipe(recipe_name, recipe_data["category"],
                              recipe_data["ingredients"], recipe_data["products"],
                              recipe_data.get("energy", 0), self)
            self.__recipes[recipe_name] = recipe
            self.__pack_custom_recipes[recipe_name] = recipe

    def delete_recipe(self, name: str):
        del self.__recipes[name]

    def __add_recipe(self, recipe_name: str, category: Category,
                     ingredients: dict[InternalItem | str, float], products: dict[InternalItem | str, float],
                     energy = 0) -> None:
        self.__recipes[recipe_name] = Recipe(recipe_name, category, ingredients, products, energy, self)

    def add_recipe_path(self, item: InternalItem, recipe: Recipe):
        self.__current_recipe_path.append((item, recipe))

    def pop_recipe_path(self):
        self.__current_recipe_path.pop()

    def get_recipe_path_from(self, ingredient: InternalItem) -> tuple[tuple[InternalItem, Recipe], ...]:
        start_index = 0
        try:
            while self.__current_recipe_path[start_index][0] != ingredient:
                start_index += 1
        except IndexError:
            Exception(f"history: {self.__current_recipe_path}, item: {ingredient}, index: {start_index}")

        return tuple(self.__current_recipe_path[start_index:])

    def get_machine_from_category(self, category: Category) -> Machine:
        return self.machines[self.req_machines_for_category[category]]

    def get_ordered_items(self, key: Callable[[InternalItem], int] = lambda item: item.get_score()) -> tuple[
        set[InternalItem], list[InternalItem]]:
        valid_items: set[InternalItem] = set()
        for ingredient in self.valid_ingredients.values():
            raw_ingredients = ingredient.get_raw_ingredients()
            if any(raw.name in self.invalid_ingredients for raw in raw_ingredients.keys()):
                continue
            valid_items.add(ingredient)

        starting_pool = set()
        for item in valid_items:
            if not item.all_unlocking_technologies() and not item.is_fluid and all(
                    raw.name not in self.excluded_automation_ingredients for raw in item.get_raw_ingredients().keys()):
                starting_pool.add(item)

        valid_items.difference_update(starting_pool)
        ordered_items: list[InternalItem] = list(sorted(valid_items, key=key))
        return starting_pool, ordered_items

    @property
    def all_ingredients(self) -> dict[str, InternalItem]:
        if self.__all_ingredients is None:
            self.__register_iternal_items()
        return self.__all_ingredients

    @property
    def valid_ingredients(self) -> dict[str, InternalItem]:
        if self.__valid_ingredients is None:
            self.__register_iternal_items()
        return self.__valid_ingredients

    @property
    def fluids(self) -> set[str]:
        if self.__fluids is None:
            self.__register_iternal_items()
        return self.__fluids

    @property
    def recipes(self) -> dict[str, Recipe]:
        if self.__recipes is None:
            self.__register_recipes()
        return self.__recipes

    @property
    def pack_custom_recipes(self) -> dict[str, Recipe]:
        if self.__pack_custom_recipes is None:
            self.__register_recipes()
        return self.__pack_custom_recipes

    @property
    def root_categories(self) -> set[str]:
        if self.__root_categories is None:
            self.__load_settings()
        return self.__root_categories

    @property
    def missed_machines(self) -> dict[str, set[Category]]:
        if self.__missed_machines is None:
            self.__load_settings()
        return self.__missed_machines


    @property
    def recipe_sources(self):
        if self.__recipe_sources is None:
            self.__register_recipe_sources()
        return self.__recipe_sources

    @property
    def raw_cost(self) -> dict[str, float]:
        if self.__raw_cost is None:
            self.__load_settings()
        return self.__raw_cost

    @property
    def req_machines_for_category(self) -> dict[Category, str]:
        if self.__req_machines_for_category is None:
            self.__load_settings()
        return self.__req_machines_for_category

    @property
    def excluded_automation_ingredients(self) -> set[str]:
        if self.__excluded_automation_ingredients:
            self.__load_settings()
        return self.__excluded_automation_ingredients

    @cached_property
    def machines(self) -> dict[str, Machine]:
        with self.modpack.open_file("machines.json") as file:
            raw_machines = json.load(file)
        machines: dict[str, Machine] = {}

        for name, categories in raw_machines.items():
            machines[name] = Machine(name, set(categories), self)

        machines["pumpjack"] = Machine("pumpjack", {"basic-fluid"}, self)
        machines["assembling-machine-1"].categories.add("crafting-with-fluid")  # mod enables this
        machines["character"].categories.add("basic-crafting")  # somehow this is implied and not exported
        machines["character"].categories.add("basic-solid")

        for name, categories in self.missed_machines.items():
            if name in machines:
                for category in categories:
                    machines[name].categories.add(category)
            else:
                machines[name] = Machine(name, categories, self)

        return machines

    @property
    def invalid_ingredients(self) -> set[str]:
        if self.__invalid_ingredients is None:
            self.__load_settings()
        return self.__invalid_ingredients


class InternalItem(FactorioElement):
    evaluating: set[InternalItem] = set()
    __req_categories: set[Category]
    def __init__(self, name: str, is_fluid: bool, recipeEngine: RecipeEngine):
        self.name = name
        self.recipeEngine = recipeEngine
        self.is_fluid = is_fluid
        self.recipes: set[Recipe] = set()
        self.is_used_in: set[Recipe] = set()

        self.best_recipe: Recipe | None = None
        self.root_item = False

        self.non_recursive_raw_ingredients: dict[InternalItem, float] = {}
        self.non_recursive_best_recipe: Recipe | None = None
        self.recursive_loops: set[RecursiveRecipeLoop] = set()
        self.has_recursive_recipe = False
        self.best_loop = None

        self.__raw_ingredients: dict[InternalItem, float] = {}
        self.__ingredient_unlocking_technologies: set[Technology] = set()
        self.__req_categories: set[Category] = set()

    def get_raw_ingredients(self) -> dict[InternalItem, float]:
        return self.eval()[0]

    def eval(self) -> tuple[dict[InternalItem, float], Recipe | None, set[Technology], set[Category]]:
        if (self.__raw_ingredients
                and not any(loop.entry and loop.get_recipe(self) == self.best_recipe for loop in self.recursive_loops)): #  and loop.get_recipe(self) == self.best_recipe
            return (self.__raw_ingredients, self.best_recipe,
                    self.__ingredient_unlocking_technologies, self.__req_categories)
        # no cache calculate

        if len(self.recipes) == 0:
            # must be an unknown method for item to spontaneously exist
            if self.name not in self.recipeEngine.raw_cost:
                self.recipeEngine.modpack.logger.warning(f"spontaneously existing item ({self.name}) doesn't have a cost, defaulting to 1")
            self.non_recursive_raw_ingredients = {self: 1}
            self.__raw_ingredients = {self: 1}
            return self.__raw_ingredients, None, set(), set()

        InternalItem.evaluating.add(self)
        for loop in self.recursive_loops:
            loop.enter_loop(self)

        if self.root_item:
            self.recipeEngine.add_recipe_path(self, self.best_recipe)
            (self.__raw_ingredients, self.__ingredient_unlocking_technologies,
             self.__req_categories) = self.best_recipe.eval()
            self.recipeEngine.pop_recipe_path()

            if not self.__raw_ingredients:
                self.__raw_ingredients = {self: 1}

            self.non_recursive_best_recipe = self.best_recipe
            self.non_recursive_raw_ingredients = self.__raw_ingredients
            InternalItem.evaluating.remove(self)
            return (self.__raw_ingredients, self.best_recipe,
                    self.__ingredient_unlocking_technologies, self.__req_categories)


        lowest_score = float('inf')
        best_recipe = None
        best_tech = set()
        best_categories = set()
        best_raw_ingredients = {}
        for recipe in self.recipes:
            self.recipeEngine.add_recipe_path(self, recipe)
            raw_ingredients, tech, cat = recipe.eval()
            self.recipeEngine.pop_recipe_path()

            if not raw_ingredients:
                continue

            recipe_score = ingredient_score(raw_ingredients) / recipe.products[self]
            if recipe_score < lowest_score:
                lowest_score = recipe_score
                best_recipe = recipe
                best_tech = tech
                best_categories = cat
                best_raw_ingredients = {ingredient: cost / recipe.products[self] for ingredient, cost in raw_ingredients.items()}

        for loop in self.recursive_loops:
            loop.exit_loop(self)

        if any(loop.entry for loop in self.recursive_loops):
            # in loop, calculation not valid for cache or recursive calculation
            InternalItem.evaluating.remove(self)
            return best_raw_ingredients, best_recipe, best_tech, best_categories

        if not best_raw_ingredients:
            # initial item must have unknown generation
            best_raw_ingredients = {self: 1}
            if self.name not in self.recipeEngine.raw_cost:
                print(f"spontaneously existing sample item ({self.name}) doesn't have a cost, defaulting to 1")

        self.non_recursive_raw_ingredients = best_raw_ingredients
        self.non_recursive_best_recipe = best_recipe
        # todo non_recursive_tech

        if not self.recursive_loops or True: # todo fix recursion
            self.__raw_ingredients = best_raw_ingredients
            self.best_recipe = best_recipe
            self.__ingredient_unlocking_technologies = best_tech
            self.__req_categories = best_categories
            InternalItem.evaluating.remove(self)
            return (self.__raw_ingredients, self.best_recipe,
                    self.__ingredient_unlocking_technologies, self.__req_categories)

        # recursive calculate
        raise NotImplementedError("recursion takes too long and should be implemented yet. How did you get here?")
        # todo recursive tech handling & categories

        for loop in self.recursive_loops:
            loop.enter_loop(self)

        non_recursive_score = lowest_score
        best_loop = None
        for loop in self.recursive_loops:
            loop_ingredients = loop.get_cost(self)

            if loop_ingredients[self] >= 1: # costs more for the loop
                continue

            discount = loop_ingredients[self]
            del loop_ingredients[self]

            raw_loop_ingredients = {}
            for loop_ingredient, loop_amount in loop_ingredients.items():
                raw_ingredients = loop_ingredient.get_raw_ingredients()

                for ingredient, amount in raw_ingredients.items():
                    if ingredient in raw_loop_ingredients:
                        raw_loop_ingredients[ingredient] += amount * loop_amount
                    else:
                        raw_loop_ingredients[ingredient] = amount * loop_amount

            self.has_recursive_recipe = True

            recipe_score = ingredient_score(raw_loop_ingredients) + non_recursive_score * discount

            if recipe_score < lowest_score:
                lowest_score = recipe_score
                best_loop = loop
                best_raw_ingredients = raw_loop_ingredients
                for ingredient, amount in self.non_recursive_raw_ingredients.items():
                    if ingredient in best_raw_ingredients:
                        best_raw_ingredients[ingredient] += amount * discount
                    else:
                        best_raw_ingredients[ingredient] = amount * discount

        for loop in self.recursive_loops:
            loop.exit_loop(self)

        self.__raw_ingredients = best_raw_ingredients
        self.best_loop = best_loop
        if best_loop is None:
            self.best_recipe = best_recipe
        else:
            self.best_recipe = best_loop.get_recipe(self)

        InternalItem.evaluating.remove(self)
        return self.__raw_ingredients

    def get_score(self) -> float:
        if self.name in self.recipeEngine.raw_cost:
            return self.recipeEngine.raw_cost[self.name]
        raw_ingredients = self.get_raw_ingredients()
        if len(raw_ingredients) == 1 and self in raw_ingredients:
            return 1
        return ingredient_score(self.get_raw_ingredients())

    def all_unlocking_technologies(self) -> set[Technology]:
        if self in InternalItem.evaluating:
            return set()

        _,_,all_unlocking_technologies, categories = self.eval()
        all_unlocking_technologies = all_unlocking_technologies.copy()
        categories = categories.copy()

        for category in categories:
            all_unlocking_technologies |= self.recipeEngine.get_machine_from_category(category).all_unlocking_technologies()

        return all_unlocking_technologies

    def invalidate_cache(self):
        self.__raw_ingredients = set()
        self.best_recipe = None
        self.__ingredient_unlocking_technologies = set()
        self.__req_categories = set()

    def set_cache(self, raw_ingredients: dict[InternalItem, float], best_recipe : Recipe | None,
                  ingredient_tech: set[Technology], req_categories: set[Category]):
        self.__raw_ingredients = raw_ingredients
        self.best_recipe = best_recipe
        self.__ingredient_unlocking_technologies = ingredient_tech
        self.__req_categories = req_categories


class RecursiveRecipeLoop:
    # entered_loops = 0
    existing_loops = set()

    def __init__(self, start: InternalItem, recipeEngine: RecipeEngine) -> None:
        self.recipeEngine = recipeEngine

        self.recipes: tuple[tuple[InternalItem, Recipe], ...] = self.recipeEngine.get_recipe_path_from(start)
        self.entry: InternalItem | None = start
        try:
            self.blocked: Recipe | None = self.recipes[0][1]
        except IndexError:
            Exception(f"recipes: {self.recipes}, item: {start}")
        # RecursiveRecipeLoop.entered_loops += 1

        # make the start of self.recipes stable for hash
        hashed_recipes = tuple(hash(recipe) for recipe in self.recipes)
        first_recipe = min(hashed_recipes)
        first_recipe_index = hashed_recipes.index(first_recipe)
        self.recipes = self.recipes[first_recipe_index:] + self.recipes[:first_recipe_index]

        if self in RecursiveRecipeLoop.existing_loops:
            return
        RecursiveRecipeLoop.existing_loops.add(self)
        if not len(RecursiveRecipeLoop.existing_loops) % 100:
            print(f"recursive loops: {len(RecursiveRecipeLoop.existing_loops)}\n"
                  f"loop: {self.recipes}")

        for item, _ in self.recipes:
            item.recursive_loops.add(self)

    def __hash__(self) -> int:
        return hash(self.recipes)

    def __eq__(self, other) -> bool:
        return hash(self) == hash(other)

    def enter_loop(self, item: InternalItem) -> bool:
        if self.entry:
            return False
        self.entry = item
        # RecursiveRecipeLoop.entered_loops += 1
        for index, (loop_item, _) in enumerate(self.recipes):
            if item == loop_item:
                self.blocked = self.recipes[index-1][1]
                # excluded_recipes.add(self.blocked)
                break

        return True

    def exit_loop(self, item: InternalItem) -> bool:
        if not self.entry:
            raise Exception("exiting_loop called without entry")
        if item != self.entry:
            return False
        self.entry = None
        # excluded_recipes.remove(self.blocked)
        self.blocked = None
        return True

    # what would getting one of the item from the loop cost
    def get_cost(self, item: InternalItem) -> dict[InternalItem, float]:
        item_index = 0
        while self.recipes[item_index][0] != item:
            item_index += 1
        recipes = self.recipes[item_index:] + self.recipes[:item_index]

        loop_ingredients: dict[InternalItem, float] = {}
        ingredients = {item: 1}
        for index, (current_item, recipe) in enumerate(recipes):
            amount_wanted = ingredients[current_item]
            produced = recipe.products[current_item]
            ingredients = {ingredient: (cost/produced) * amount_wanted
                           for ingredient, cost in recipe.ingredients.items()}

            for ingredient, cost in ingredients.items():
                if index + 1 != len(recipes) and ingredient == recipes[index+1][0]:
                    continue
                if ingredient not in loop_ingredients:
                    loop_ingredients[ingredient] = cost
                else:
                    loop_ingredients[ingredient] += cost

        return loop_ingredients

    def get_recipe(self, item: InternalItem):
        item_index = 0
        while self.recipes[item_index][0] != item:
            item_index += 1
        return self.recipes[item_index][1]

class Recipe(FactorioElement):
    name: str
    category: str
    ingredients: dict[InternalItem, float]
    products: dict[InternalItem, float]
    energy: float

    def __init__(self, name: str, category: str, ingredients_raw: dict[InternalItem | str, float],
                 products_raw: dict[InternalItem | str, float], energy: float, recipeEngine: RecipeEngine):
        self.name = name
        self.recipeEngine = recipeEngine
        # TODO add check for category
        self.category = category
        self.energy = energy
        self.productivity = False
        self.__raw_ingredients: dict[InternalItem, float] = {}
        self.__all_unlocking_technologies: set[Technology] = set()
        self.__all_categories: set[Category] = set()

        self.ingredients = {}
        for ingredient, amount in ingredients_raw.items():
            if type(ingredient) is InternalItem:
                self.ingredients[ingredient] = amount
            elif type(ingredient) is str:
                assert ingredient in self.recipeEngine.all_ingredients, (f"Unknown ingredient: {ingredient}", f"In recipe {self.name}")
                self.ingredients[self.recipeEngine.all_ingredients[ingredient]] = amount
            else:
                raise TypeError(f"Unknown ingredient type: {ingredient} \nIn recipe {self.name}")

        self.products = {}
        for product, amount in products_raw.items():
            if type(product) is InternalItem:
                self.products[product] = amount
            elif type(product) is str:
                assert product in self.recipeEngine.all_ingredients, (f"Unknown product: {product}", f"In recipe {self.name}")
                self.products[self.recipeEngine.all_ingredients[product]] = amount
            else:
                raise TypeError(f"Unknown product type: {product} \nIn recipe {self.name}")

        for product in self.products.keys():
            product.recipes.add(self)
            product.invalidate_cache()

        for ingredient in self.ingredients.keys():
            ingredient.is_used_in.add(self)

        if category in self.recipeEngine.root_categories:
            for product, produced in self.products.items():
                product.root_item = True
                product.best_recipe = self
                product.best_non_recursive_recipe = self
                # if ingredients:
                #     for ingredient, cost in ingredients.items():
                #         product.raw_ingredients |= {ingredient: cost/produced}
                # else:
                #     if self.name not in rel_cost:
                #         print(f"spontaneously existing item ({product.name}) doesn't have a cost, default to 1")
                #     product.raw_ingredients = {product: 1}
                #     product.raw_eval = True

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"

    def remove(self):
        self.recipeEngine.delete_recipe(self.name)
        for product in self.products.keys():
            product.recipes.remove(self)
            if self == product.best_recipe:
                product.invalidate_cache()

        for ingredient in self.ingredients.keys():
            ingredient.is_used_in.remove(self)

    @property
    def crafting_machine(self) -> Machine:
        """cheapest crafting machine name able to run this recipe"""
        return self.recipeEngine.get_machine_from_category(self.category)

    @property
    def unlocking_technologies(self) -> set[Technology]:
        """Unlocked by any of the returned technologies. Empty set indicates a starting recipe."""
        return {tech for tech in self.recipeEngine.recipe_sources.get(self.name, ())}

    def all_unlocking_technologies(self) -> set[Technology]:
        _, technologies, all_categories = self.eval()
        for category in all_categories:
            technologies |= self.recipeEngine.get_machine_from_category(category).all_unlocking_technologies()
        return technologies


    @property
    def total_energy(self) -> float:
        """Total required energy (crafting time) for single craft"""
        # TODO: multiply mining energy by 2 since drill has 0.5 speed
        total_energy = self.energy
        for ingredient, cost in self.ingredients.items():
            ingredient.get_raw_ingredients()
            if ingredient.best_recipe:
                total_energy += ingredient.best_recipe.total_energy / ingredient.best_recipe.products[ingredient] * cost
            # if ingredient in craftable:
            #     selected_recipe_energy = float('inf')
            #     for ingredient_recipe in all_product_sources[ingredient]:
            #         craft_count = max((n for name, n in ingredient_recipe.products.items() if name == ingredient))
            #         recipe_energy = ingredient_recipe.total_energy / craft_count * cost
            #         if recipe_energy < selected_recipe_energy:
            #             selected_recipe_energy = recipe_energy
            #     total_energy += selected_recipe_energy
        return total_energy

    def get_raw_ingredients(self) -> dict[InternalItem, float]:
        return self.eval()[0]


    def eval(self) -> tuple[dict[InternalItem, float], set[Technology], set[Category]]:
        invalid_cache = any(loop.entry for ingredient in self.ingredients for loop in ingredient.recursive_loops) # todo less invalidation possible?

        if self.__raw_ingredients and not invalid_cache:
            return self.__raw_ingredients, self.__all_unlocking_technologies, self.__all_categories
        invalid = False

        base_tech = self.unlocking_technologies
        req_categories = {self.category}
        ingredients = {}
        for ingredient, cost in self.ingredients.items():
            if ingredient in InternalItem.evaluating:
                # recursion occured log and bounce
                RecursiveRecipeLoop(ingredient, self.recipeEngine)
                return {}, set(), set() # todo fix recursion
                invalid = True
                continue

            raw_ingredients, _, tech, cat = ingredient.eval()
            if not raw_ingredients:
                # not currently a valid path fail
                return {}, set(), set()

            base_tech |= tech
            req_categories |= cat
            for raw_ingredient, raw_cost in raw_ingredients.items():
                if raw_ingredient not in ingredients:
                    ingredients[raw_ingredient] = raw_cost * cost
                else:
                    ingredients[raw_ingredient] += raw_cost * cost

        if invalid:
            return {}, set(), set()

        if not invalid_cache:
            self.__raw_ingredients = ingredients
            self.__all_unlocking_technologies = base_tech
            self.__all_categories = req_categories

        return ingredients, base_tech, req_categories

class Machine(FactorioElement):
    evaluating: set[Machine] = set()
    def __init__(self, name: str, categories: set[Category], recipeEngine: RecipeEngine):
        self.name: str = name
        self.recipeEngine: RecipeEngine = recipeEngine
        self.item: InternalItem | None
        if self.name != "character":
            self.item = self.recipeEngine.all_ingredients[name]
        else:
            self.item = None
        self.categories: set[Category] = categories

    def all_unlocking_technologies(self) -> set[Technology]:
        if self.item:
            if self in Machine.evaluating:
                return set()
            Machine.evaluating.add(self)
            tech = self.item.all_unlocking_technologies()
            Machine.evaluating.remove(self)
            return tech
        else:
            return set()

