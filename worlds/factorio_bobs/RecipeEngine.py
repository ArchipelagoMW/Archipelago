from __future__ import annotations

import json
import math
from enum import Enum
from functools import cached_property
from typing import TYPE_CHECKING, TypeVar

import pulp

if TYPE_CHECKING:
    from . import Technology, FactorioModpack

GENERATOR_ENERGY = 1

class DefinitionSource(Enum):
    UNKNOWN = 0
    EXTRACTED = 1
    CUSTOM = 2
    IMPLIED = 3
    WORLD = 4

class RecipeEngineType:
    def __init__(self, ctx: RecipeEngine, name: str, source: DefinitionSource):
        self.name: str = name
        self.ctx: RecipeEngine = ctx
        self.source: DefinitionSource = source
        if source == DefinitionSource.IMPLIED:
            ctx.modpack.logger.warning(f"{repr(self)}: is implied more strictly define")

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self.name}, ctx={self.ctx.name})"

class RecipeEngine:
    def __init__(self, modpack: "FactorioModpack"):
        self.modpack = modpack
        self.name = self.modpack.packName

        self.has_init = False

        self.game_items: dict[str, GameItem] = {}
        self.recipes: dict[str, GameRecipe] = {}

        self.item_catalysts: dict[GameItem, OneItemCatalyst] = {}
        self.categories: dict[str, CategoryCatalyst] = {}
        self.fluid_mining: TechCatalyst | None = None

        self.custom_invalid: set[GameItem] = set()

        self.__dif_entity_to_item: dict[str, str] | None = None

    def full_init(self) -> None:
        if self.has_init:
            return
        self.has_init = True

        self.__register_game_items()
        self.__register_categories()
        self.__register_recipes()
        self.__link_technologies()
        self.__load_settings()
        self.__link_recipes()
        self.__remove_bad_items()

    def __register_game_items(self) -> None:
        invalid_items = {"fluid-unknown"} | {f"parameter-{i}" for i in range(10)}

        with self.modpack.open_file("Extractor/fluids.json") as file:
            fluids: set[str] = set(json.load(file))

        for fluid in fluids:
            ingredient = GameItem(self, fluid, DefinitionSource.EXTRACTED, True)
            self.game_items[fluid] = ingredient
            if fluid in invalid_items:
                ingredient.is_valid_ingredient = False

        with self.modpack.open_file("Extractor/items.json") as file:
            item_stack_sizes: dict[str, int] = json.load(file)

        for item, stack_size in item_stack_sizes.items():
            ingredient = GameItem(self, item, DefinitionSource.EXTRACTED,False)
            self.game_items[item] = ingredient
            if ingredient.name in self.modpack.ordered_science_packs or ingredient.name in invalid_items:
                ingredient.is_valid_ingredient = False

    def __register_categories(self) -> None:

        def get_category(name: str) -> CategoryCatalyst:
            if name not in self.categories:
                self.categories[name] = CategoryCatalyst(self, name, DefinitionSource.EXTRACTED)
            return self.categories[name]

        with self.modpack.open_file("Extractor/machines.json") as file:
            raw_machines = json.load(file)

        for entity, categories in raw_machines.items():
            if entity == "character":
                for category in categories:
                    get_category(category).manual = True
                get_category("basic-crafting").manual = True # somehow this is implied and not exported
                get_category("basic-solid").manual = True # somehow this is implied and not exported
                continue

            item = self.get_item_from_entity(entity)
            if item.name == "assembling-machine-1":
                get_category("crafting-with-fluid").machines.add(item) # mod enables this todo: disable?
            for category in categories:
                get_category(category).machines.add(item)

    def __register_recipes(self):
        self.__recipes: dict[str, GameRecipe] = {}

        with self.modpack.open_file("Extractor/resources.json") as file:  # todo find better method then opening twice
            raw_resources = json.load(file)

        for resource_name, resource_data in raw_resources.items():
            if "required_fluid" in resource_data:
                self.recipes[f"resource_{resource_name}"] = GameRecipe(self, resource_name, DefinitionSource.EXTRACTED,
                                                                       {resource_data["required_fluid"]: resource_data["fluid_amount"]},
                                                                       resource_data["products"], resource_data["mining_time"])
                if resource_data["category"] == "basic-solid":
                    self.recipes[f"resource_{resource_name}"].catalysts.add(self.fluid_mining)
            else:
                self.recipes[f"resource_{resource_name}"] = GameRecipe(self, resource_name, DefinitionSource.EXTRACTED,
                                                                       {},
                                                                       resource_data["products"], resource_data["mining_time"])
            self.recipes[f"resource_{resource_name}"].catalysts.add(self.categories[resource_data["category"]])
        del raw_resources

        with self.modpack.open_file("Extractor/recipes.json") as file:
            raw_recipes = json.load(file)

        for recipe_name, recipe_data in raw_recipes.items():
            # example "wheat-seeds":{"ingredients":{"wood":100},"products":{"wheat-seeds":1},"category":"organic-synth-recipes","energy":30}
            if recipe_data["category"] not in self.categories:
                continue
            self.recipes[recipe_name] = GameRecipe(self, recipe_name, DefinitionSource.EXTRACTED,
                                                   recipe_data["ingredients"], recipe_data["products"],
                                                   recipe_data["energy"])
            self.recipes[recipe_name].catalysts.add(self.categories[recipe_data["category"]])
        del raw_recipes

        with self.modpack.open_file("Extractor/generators.json") as file:
            raw_generators = json.load(file)
        for entity, product in raw_generators.items():
            item = self.get_item_from_entity(entity)
            self.categories[f"generator_{item.name}"] = CategoryCatalyst(self, f"generator_{item.name}",
                                                                         DefinitionSource.EXTRACTED)
            self.categories[f"generator_{item.name}"].machines.add(item)
            self.recipes[f"generator_{item.name}"] = GameRecipe(self, f"generator_{item.name}",
                                                                DefinitionSource.EXTRACTED,
                                                                {}, {product: 1},
                                                                GENERATOR_ENERGY)
        del raw_generators

        if "offshore-pump" in self.categories:
            fluids = set()
            with self.modpack.open_file("Extractor/specialTiles.json") as file:
                raw_tiles = json.load(file)
            for tile, special in raw_tiles.items():
                if "fluid" in special:
                    fluids.add(special["fluid"])
            del raw_tiles
            for fluid in fluids:
                self.recipes[f"pump_{fluid}"] = GameRecipe(self, f"pump_{fluid}", DefinitionSource.EXTRACTED,
                                                           {}, {fluid: 1}, GENERATOR_ENERGY)

        try:
            with self.modpack.open_file("customRecipes.json") as file:
                raw_custom = json.load(file)
        except FileNotFoundError:
            raw_custom = {}

        for recipe_name, recipe_data in raw_custom.items():
            # TODO add optional crafting_machine_tints
            # TODO add group for AP recipes
            # TODO add support for custom techs for recipes
            self.recipes[recipe_name] = GameRecipe(self, recipe_name, DefinitionSource.CUSTOM,
                                                   recipe_data["ingredients"], recipe_data["products"], recipe_data["energy"])
            self.recipes[recipe_name].catalysts.add(self.categories[recipe_data["category"]])

    def __link_technologies(self):
        for technology in self.modpack.base_technology_table.values():
            if "mining-with-fluid" in technology.modifiers:
                self.fluid_mining = TechCatalyst(self, DefinitionSource.EXTRACTED, technology)
            if not technology.unlocks:
                continue
            catalyst = TechCatalyst(self, DefinitionSource.EXTRACTED, technology)
            for recipe_name in technology.unlocks:
                self.recipes[recipe_name].catalysts.add(catalyst)

    def __load_settings(self) -> None:
        with self.modpack.open_file("recipeEngineSettings.json") as file:
            raw_settings = json.load(file)

        if "missed_machines" in raw_settings:
            for name, categories in raw_settings["missed_machines"].items():
                for category in categories:
                    self.categories[category].machines.add(self.get_game_item(name, DefinitionSource.CUSTOM))

        if "invalid_ingredients" in raw_settings:
            for ingredient in raw_settings["invalid_ingredients"]:
                self.custom_invalid.add(self.get_game_item(ingredient, DefinitionSource.CUSTOM))

        if "excluded_first_pool" in raw_settings:
            for ingredient in raw_settings["excluded_first_pool"]:
                self.get_game_item(ingredient, DefinitionSource.CUSTOM).is_valid_first_pool = False

    def __link_recipes(self):
        for recipe in self.recipes.values():
            recipe.link()

    def __remove_bad_items(self):
        for name, item in self.game_items.copy().items():
            if item not in self.custom_invalid:
                if item.crafted_by:
                    continue
                if item.used_in:
                    if item.is_valid_pool:
                        self.modpack.logger.warning(f"{item.name} is used but not method of obtaining it detected.\n"
                                                    "Consider disabling it or adding a custom recipe")
            item.set_invalid()

    def run_pulp_solver(self, goal: GameItem, invalid_catalysts: set[Catalyst]=None, remove_waste=False) \
            -> tuple[int, float, set[GameRecipe], set[GameRecipe], dict[GameItem, float]]:
        if invalid_catalysts is None:
            invalid_catalysts: set[Catalyst] = set()
        probBest = pulp.LpProblem("CraftingOptimization", pulp.LpMinimize)

        recipe_qty = {
            recipe: pulp.LpVariable(f"recipe_{recipe.name}", lowBound=0)
            for recipe in self.recipes.values() if not (recipe.catalysts & invalid_catalysts)
        }
        waste = {
            item: pulp.LpVariable(f"waste_{item.name}", lowBound=0)
            for item in self.game_items.values()
        }
        # todo these are bad and massively slow things down a graph based solution to get bootstrap before hand would be better
        can_get_item = {
            item: pulp.LpVariable(f"cgi_{item.name}", cat="Binary")
            for item in self.game_items.values()
        }
        can_get_recipe = {
            recipe: pulp.LpVariable(f"cgr_{recipe.name}", cat="Binary")
            for recipe in self.recipes.values()
        }
        can_get_category = {
            category: pulp.LpVariable(f"cgc_{category.name}", cat="Binary")
            for category in self.categories.values()
        }

        # goal
        epsilon = 1e-3
        epsilon_2 = 1e-6
        probBest += (pulp.lpSum(
            recipe.energy * recipe_qty[recipe]
            for recipe in recipe_qty.keys()
        ) + epsilon * pulp.lpSum(can_get_recipe.values())
                     + epsilon_2 * pulp.lpSum(waste.values()) + epsilon_2 * pulp.lpSum(recipe_qty.values()))

        # constraint first pass get best
        for item in self.game_items.values():
            produced = [recipe_qty[recipe] * recipe.products[item] for recipe in item.crafted_by]
            consumed = [recipe_qty[recipe] * recipe.ingredients[item] for recipe in item.used_in]

            if item == goal:
                probBest += pulp.lpSum(produced) - pulp.lpSum(consumed) == 1, f"balance_{item.name}"
            else:
                probBest += pulp.lpSum(produced) - pulp.lpSum(consumed) == 0 + waste[item], f"balance_{item.name}"

            probBest += can_get_item[item] <= pulp.lpSum(can_get_recipe[recipe] for recipe in item.crafted_by), f"can_get_{item.name}"

        big_M = 1e5
        for recipe in self.recipes.values():
            rec_qty = recipe_qty[recipe]
            can_rec = can_get_recipe[recipe]

            probBest += rec_qty <= can_rec * big_M
            req = ({can_get_item[cat.item] for cat in recipe.catalysts if isinstance(cat, OneItemCatalyst)}
                   | {can_get_category[cat] for cat in recipe.catalysts if isinstance(cat, CategoryCatalyst)}
                   | {can_get_item[ingredient] for ingredient in recipe.ingredients})
            for catalyst in req:
                probBest += can_rec <= catalyst

        for category in self.categories.values():
            if category.manual:
                continue
            probBest += can_get_category[category] <= pulp.lpSum(can_get_item[item] for item in category.machines)

        status = probBest.solve(pulp.PULP_CBC_CMD(msg=False))
        score = probBest.objective.value()

        req_recipes = set(recipe for recipe, value in can_get_recipe.items() if not math.isclose(value.value(), 0))

        if not remove_waste:
            return status, score, req_recipes, set(), depulp_dict(waste)

        probWaste = pulp.LpProblem("WasteRemove", pulp.LpMinimize)

        removal_force = 1e5
        probWaste += pulp.lpSum(
            recipe.energy * recipe_qty[recipe]
            for recipe in recipe_qty.keys()
        ) + removal_force * pulp.lpSum(waste.values()) + epsilon * pulp.lpSum(recipe_qty.values())

        # constraint second pass remove waste
        for item in self.game_items.values():
            produced = [recipe_qty[recipe] * recipe.products[item] for recipe in item.crafted_by]
            consumed = [recipe_qty[recipe] * recipe.ingredients[item] for recipe in item.used_in]

            if item == goal:
                probWaste += pulp.lpSum(produced) - pulp.lpSum(consumed) == 1, f"balance_{item.name}"
            else:
                probWaste += pulp.lpSum(produced) - pulp.lpSum(consumed) == 0 + waste[item], f"balance_{item.name}"

        # constraint: keep best recipes
        for recipe, pulp_var in recipe_qty.items():
            quantity = pulp_var.value()
            if -epsilon >= quantity or epsilon <= quantity:
                probWaste += pulp_var >= quantity, f"force_{recipe.name}"

        status = probBest.solve(pulp.PULP_CBC_CMD(msg=False))

        if status != pulp.LpStatusOptimal:
            self.modpack.logger.debug(f"{goal}: is wasteable with status {status}\n")

        waste_recipes = set(recipe for recipe, value in recipe_qty.items() if (not math.isclose(value.value(), 0)) and recipe not in req_recipes)

        return status, score, req_recipes, waste_recipes, depulp_dict(waste)

    def get_item_catalyst(self, item: GameItem) -> OneItemCatalyst:
        if item not in self.item_catalysts:
            self.item_catalysts[item] = OneItemCatalyst(DefinitionSource.UNKNOWN, item)
        return self.item_catalysts[item]

    def get_item_from_entity(self, entity: str) -> GameItem:
        if self.__dif_entity_to_item is None:
            with self.modpack.open_file("Extractor/entityToItem.json") as file:
                self.__dif_entity_to_item = json.load(file)

        if entity in self.__dif_entity_to_item:
            entity = self.__dif_entity_to_item[entity]

        return self.game_items[entity]

    def get_game_item(self, item: GameItem | str, source: DefinitionSource = DefinitionSource.IMPLIED) -> GameItem:
        if type(item) is GameItem:
            return item
        if item in self.game_items:
            return self.game_items[item]
        if source != DefinitionSource.EXTRACTED:
            raise RuntimeError(f"{item} is not a valid ingredient")
        self.game_items[item] = GameItem(self, item, DefinitionSource.IMPLIED)
        return self.game_items[item]


class GameItem(RecipeEngineType):
    def __init__(self, ctx: RecipeEngine, name: str, source: DefinitionSource,
                 is_fluid: bool = False):
        super().__init__(ctx, name, source)
        self.is_fluid = is_fluid

        self.has_calculated_raw: bool = False
        self.best_recipes: set[GameRecipe] = set()
        self.score: float = float("inf")
        self.req_techs: set[TechCatalyst] | None = None

        self.is_valid: bool = True
        self.__is_valid_first_pool: bool = True
        self.is_valid_pool: bool = True

        self.used_in: set[GameRecipe] = set()
        self.crafted_by: set[GameRecipe] = set()

    @property
    def is_valid_first_pool(self) -> bool:
        return self.is_valid_pool and self.__is_valid_first_pool

    @is_valid_first_pool.setter
    def is_valid_first_pool(self, is_valid_first_pool: bool) -> None:
        self.__is_valid_first_pool = is_valid_first_pool

    def raw_calculate(self) -> None:
        if self.has_calculated_raw:
            return
        self.has_calculated_raw = True

        status, score, best_recipes, waste_recipes, waste = self.ctx.run_pulp_solver(self)
        if status != pulp.LpStatusOptimal:
            self.ctx.modpack.logger.warn(f"{self}: is uncraftable with status {status}\n"
                                     f"removing {self}")
            self.set_invalid()
        self.score = score
        self.best_recipes = best_recipes
        self.req_techs = {tech for recipe in self.best_recipes for tech in recipe.catalysts if isinstance(tech, TechCatalyst)}

    def get_best_recipes(self):
        if not self.best_recipes:
            self.__eval_best()
        return self.best_recipes

    def __eval_best(self):
        status, score, best_recipes, waste_recipes, waste = self.ctx.run_pulp_solver(self)
        if status != pulp.LpStatusOptimal:
            self.ctx.modpack.logger.warn(f"{self}: is uncraftable with status {status}\n"
                                     f"removing {self}")
            self.set_invalid()
        self.score = score
        self.best_recipes = best_recipes

    def set_invalid(self):
        self.is_valid = False
        for recipe in self.used_in.copy():
            recipe.set_invalid()
        if self.name in self.ctx.game_items:
            del self.ctx.game_items[self.name]


class GameRecipe(RecipeEngineType):
    def __init__(self, ctx: RecipeEngine, name: str, source: DefinitionSource,
                 ingredients: dict[GameItem | str, float], products: dict[GameItem | str, float], energy: float):
        super().__init__(ctx, name, source)

        self.has_calculated_raw: bool = False
        self.req_techs: set[TechCatalyst] | None = None
        self.is_valid: bool = True

        self.ingredients: dict[GameItem, float] = {ctx.get_game_item(ingredient, source): amount
                                                   for ingredient, amount in ingredients.items()}
        self.products: dict[GameItem, float] = {ctx.get_game_item(product, source): amount
                                                for product, amount in products.items()}
        self.energy = energy
        self.catalysts: set[Catalyst] = set()

        if not self.ingredients:
            self.cost: float = self.energy
        else:
            self.cost: float = float("inf")

        for ingredient, amount in self.ingredients.copy().items():
            if not ingredient.is_valid:
                self.is_valid = False
            if ingredient not in self.products:
                continue
            new_amount = self.products[ingredient] - amount
            if new_amount >= 0:
                del self.ingredients[ingredient]
                self.catalysts.add(ctx.get_item_catalyst(ingredient))
                self.products[ingredient] = new_amount
            else:
                del self.products[ingredient]
                self.ingredients[ingredient] = -new_amount

    @cached_property
    def category(self) -> str | None:
        for cat in self.catalysts:
            if type(cat) is CategoryCatalyst:
                return cat.name
        return None

    def link(self) -> None:
        for ingredient in self.ingredients:
            ingredient.used_in.add(self)
        for product in self.products:
            product.crafted_by.add(self)

    def set_invalid(self):
        self.is_valid = False
        for product in self.products:
            if self in product.crafted_by:
                product.crafted_by.remove(self)
                if not product.crafted_by:
                    product.set_invalid()
        for ingredient in self.ingredients:
            if self in ingredient.used_in:
                ingredient.used_in.remove(self)
        if self.name in self.ctx.recipes:
            del self.ctx.recipes[self.name]

    def raw_calculate(self) -> None:
        if self.has_calculated_raw:
            return
        self.has_calculated_raw = True

        self.req_techs = set()
        for catalyst in self.catalysts:
            catalyst.raw_calculate()
            if not catalyst.is_valid:
                self.set_invalid()
                return
            self.req_techs |= catalyst.req_techs



class Catalyst(RecipeEngineType):
    def __init__(self, ctx: RecipeEngine, name: str, source: DefinitionSource):
        super().__init__(ctx, name, source)
        self.has_calculated_raw: bool = False
        self.is_valid: bool = True
        self.req_techs: set[TechCatalyst] | None = None

    def raw_calculate(self):
        pass


class ItemCatalyst(Catalyst):
    def __init__(self, ctx: RecipeEngine, name: str, source: DefinitionSource):
        super().__init__(ctx, name, source)
        self.item: GameItem | None = None

    def calculate_tech(self, invalid_cat: set[Catalyst] | None = None) -> set[TechCatalyst] | None:
        # if self.has_calculated_raw: # TODO optimise this could do with some caching
        #     return
        # self.has_calculated_raw = True

        self.item.raw_calculate()
        if invalid_cat:
            invalid_cat: set[Catalyst] = {self} | invalid_cat
        else:
            invalid_cat: set[Catalyst] = {self}

        status, _, recipes, _, _ = self.ctx.run_pulp_solver(self.item, invalid_catalysts=invalid_cat)
        if status != pulp.LpStatusOptimal:
            self.ctx.modpack.logger.debug(f"{self}: {status}, {recipes}")
            return None  # critically failed
        req_cat: set[Catalyst] = set(cat for recipe in recipes for cat in recipe.catalysts)
        item_cat: set[ItemCatalyst] = set(cat for cat in req_cat if isinstance(cat, ItemCatalyst))
        tech_cat: set[Catalyst] = set(cat for cat in req_cat if isinstance(cat, TechCatalyst))
        for cat in item_cat:
            ret = cat.calculate_tech(invalid_cat=invalid_cat)
            if ret is None:
                invalid_cat.add(cat)
                return self.calculate_tech(invalid_cat=invalid_cat)
            tech_cat |= ret
        return tech_cat


class CategoryCatalyst(ItemCatalyst):
    def __init__(self, ctx: RecipeEngine, name: str, source: DefinitionSource):
        super().__init__(ctx, name, source)
        self.machines: set[GameItem] = set()
        self.manual = False

    def raw_calculate(self):
        if self.has_calculated_raw:
            return
        self.has_calculated_raw: bool = True
        if self.manual:
            self.has_calculated_raw: bool = True
            self.req_techs = set() # todo check is not manual early
            return

        ordered_machines = sorted(self.machines, key=lambda x: x.score)
        for machine in ordered_machines:
            self.item = machine
            self.req_techs = self.calculate_tech()
            if self.req_techs is not None:
                return

        self.ctx.modpack.logger.warning(f"{self}: unable to bootstrap")
        self.is_valid = False # todo better is invalid

    def calculate_tech(self, invalid_cat: set[Catalyst] | None = None) -> set[TechCatalyst] | None:
        if self.manual:
            return set()
        store_best = self.item

        ordered_machines = sorted(self.machines, key=lambda x: x.score)
        calc_tech: set[TechCatalyst] = set()
        for machine in ordered_machines:
            self.item = machine
            calc_tech = super().calculate_tech(invalid_cat)
            if calc_tech is not None:
                break

        if self.has_calculated_raw:
            self.item = store_best
        return calc_tech


class OneItemCatalyst(ItemCatalyst):
    def __init__(self, source: DefinitionSource,
                 item: GameItem):
        super().__init__(item.ctx, item.name, source)
        self.item = item

    def raw_calculate(self):
        if self.has_calculated_raw or not self.item.is_valid:
            return
        self.has_calculated_raw = True

        self.req_techs = self.calculate_tech()
        if self.req_techs is None:
            self.ctx.modpack.logger.warning(f"{self}: unable to bootstrap")
            self.is_valid = False # todo better is invalid


class TechCatalyst(Catalyst):
    def __init__(self, ctx: RecipeEngine, source: DefinitionSource, tech: Technology):
        super().__init__(ctx, tech.name, source)
        self.tech = tech
        self.req_techs = {self}


T = TypeVar("T")
def depulp_dict(dictionary: dict[T, pulp.LpVariable]) -> dict[T, float]:
    out: dict[T, float] = {}
    for key, value in dictionary.items():
        qty = value.value()
        epsilon = 1e-6
        if -epsilon >= value or epsilon <= value:
            out[key] = qty
    return out