from __future__ import annotations

import json
import math
from enum import Enum
from typing import TYPE_CHECKING, TypeVar

try:
    import pulp
except ImportError:
    pulp_enabled = False
else:
    pulp_enabled = True

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
    invalidate_cache = False

    def __init__(self, modpack: "FactorioModpack"):
        self.modpack = modpack
        self.name = self.modpack.packName

        self.has_init = False

        self.game_items: dict[str, GameItem] = {}
        self.recipes: dict[str, GameRecipe] = {}

        self.item_catalysts: dict[GameItem, OneItemCatalyst] = {}
        self.categories: dict[str, Category] = {}
        self.fluid_mining: set[GameRecipe] = set()

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
        self.__remove_bad_items()

        goal_items = {"rocket-part", "satellite", "rocket-silo"}
        non_randomizable_items = set(self.modpack.ordered_science_packs) | goal_items

        for item_name in non_randomizable_items:
            self.get_game_item(item_name).is_valid_pool = False

        if RecipeEngine.invalidate_cache:
            return

        try:
            with self.modpack.open_file("Cache/precalc.json") as file:
                raw_logic_pre_compute = json.load(file)
            for name, data in raw_logic_pre_compute.items():
                item = self.get_game_item(name)
                item.has_calculated_raw = True
                if "invalid" in data:
                    if item.name not in {"space-science-pack"}:
                        item.set_invalid()
                    continue
                item.best_recipes = {self.recipes[name] for name in data["recipes"]}
                item.score = data["score"]
        except FileNotFoundError:
            pass


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
        def get_category(name: str) -> Category:
            if name not in self.categories:
                self.categories[name] = Category(self, name, DefinitionSource.EXTRACTED)
            return self.categories[name]

        with self.modpack.open_file("Extractor/machines.json") as file:
            raw_machines = json.load(file)

        for entity, categories in raw_machines.items():
            if entity == "character":
                for category in categories:
                    get_category(category).manual = True
                get_category("basic-crafting").manual = True # somehow this is implied and not exported
                get_category("basic-solid").manual = True # this is not a crafting category so not extracted todo look if some ores can't do this
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
                GameRecipe(self, f"resource_{resource_name}", DefinitionSource.EXTRACTED, resource_data["category"],
                           {resource_data["required_fluid"]: resource_data["fluid_amount"]},
                           resource_data["products"], resource_data["mining_time"])
                if resource_data["category"] == "basic-solid":
                    self.fluid_mining.add(self.recipes[f"resource_{resource_name}"])
            else:
                GameRecipe(self, f"resource_{resource_name}", DefinitionSource.EXTRACTED, resource_data["category"],
                           {},
                           resource_data["products"], resource_data["mining_time"])
        del raw_resources

        with self.modpack.open_file("Extractor/recipes.json") as file:
            raw_recipes = json.load(file)

        for recipe_name, recipe_data in raw_recipes.items():
            # example "wheat-seeds":{"ingredients":{"wood":100},"products":{"wheat-seeds":1},"category":"organic-synth-recipes","energy":30}
            if recipe_data["category"] not in self.categories: # No way to craft skip recipe
                self.modpack.logger.debug(f"Recipe {recipe_name} has invalid category {recipe_data['category']}.")
                continue
            GameRecipe(self, recipe_name, DefinitionSource.EXTRACTED, recipe_data["category"],
                       recipe_data["ingredients"], recipe_data["products"], recipe_data["energy"])
        del raw_recipes

        with self.modpack.open_file("Extractor/generators.json") as file:
            raw_generators = json.load(file)
        for entity, product in raw_generators.items():
            item = self.get_item_from_entity(entity)
            self.categories[f"generator_{item.name}"] = Category(self, f"generator_{item.name}",
                                                                 DefinitionSource.EXTRACTED)
            self.categories[f"generator_{item.name}"].machines.add(item)
            GameRecipe(self, f"generator_{item.name}", DefinitionSource.EXTRACTED,
                       f"generator_{item.name}",{}, {product: 1}, GENERATOR_ENERGY)
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
                GameRecipe(self, f"pump_{fluid}", DefinitionSource.EXTRACTED,
                           "offshore-pump",{}, {fluid: 1}, GENERATOR_ENERGY)

        try:
            with self.modpack.open_file("customRecipes.json") as file:
                raw_custom = json.load(file)
        except FileNotFoundError:
            raw_custom = {}

        for recipe_name, recipe_data in raw_custom.items():
            # TODO add optional crafting_machine_tints
            # TODO add group for AP recipes
            # TODO add support for custom techs for recipes
            GameRecipe(self, recipe_name, DefinitionSource.CUSTOM, recipe_data["category"],
                       recipe_data["ingredients"], recipe_data["products"], recipe_data["energy"])

    def __link_technologies(self):
        for technology in self.modpack.base_technology_table.values():
            if "mining-with-fluid" in technology.modifiers:
                fluid_mining_tech = TechCatalyst(self, DefinitionSource.EXTRACTED, technology) # todo Multiple/none?
                for recipe in self.fluid_mining:
                    recipe.technologies.add(fluid_mining_tech)
            if not technology.unlocks:
                continue
            catalyst = TechCatalyst(self, DefinitionSource.EXTRACTED, technology)
            for recipe_name in technology.unlocks:
                if recipe_name in self.recipes:
                    self.recipes[recipe_name].technologies.add(catalyst)
                else:
                    self.modpack.logger.debug(f"Technology {technology.name} unlocked unknown recipe: {recipe_name}")

    def __load_settings(self) -> None:
        with self.modpack.open_file("recipeEngineSettings.json") as file:
            raw_settings = json.load(file)

        if "missed_machines" in raw_settings:
            for name, categories in raw_settings["missed_machines"].items():
                item = self.get_item_from_entity(name)
                for category in categories:
                    self.get_category(category).machines.add(item)
            del raw_settings["missed_machines"]

        if "invalid_ingredients" in raw_settings:
            for ingredient in raw_settings["invalid_ingredients"]:
                self.custom_invalid.add(self.get_game_item(ingredient, DefinitionSource.CUSTOM))
            del raw_settings["invalid_ingredients"]

        if "excluded_first_pool" in raw_settings:
            for ingredient in raw_settings["excluded_first_pool"]:
                self.get_game_item(ingredient, DefinitionSource.CUSTOM).is_valid_first_pool = False
            del raw_settings["excluded_first_pool"]

        for key in raw_settings.keys():
            self.modpack.logger.error(f"Unknown key in recipeEngineSettings.json: {key}")


    def __remove_bad_items(self):
        for name, item in self.game_items.copy().items():
            if item.name in {"space-science-pack"}:
                continue # todo remove this when silo recipes added
            if item not in self.custom_invalid:
                if item.crafted_by:
                    continue
                if item.used_in:
                    if item.is_valid_pool:
                        self.modpack.logger.warning(f"{item.name} is used but not method of obtaining it detected.\n"
                                                    "Consider disabling it or adding a custom recipe")
                self.modpack.logger.warning(f"{item.name} is defined but not used or craftable")
            item.set_invalid()

    def run_pulp_solver(self, goal: GameItem, remove_waste=False) \
            -> tuple[int, float, set[GameRecipe], set[GameRecipe], dict[GameItem, float]]:
        if not pulp_enabled:
            raise Exception("Pulp is not installed. \n"
                            "This means that the pack has not been precalculated. This is currently required.\n"
                            "If you are trying to precalculate then you need to install Pulp.\n"
                            "If the pack has been precalculated and you get this error report it in the discord thread alongside the pack.")

        probBest = pulp.LpProblem("CraftingOptimization", pulp.LpMinimize)

        recipe_qty = {
            recipe: pulp.LpVariable(f"recipe_{recipe.name}", lowBound=0)
            for recipe in self.recipes.values() if recipe.is_valid
        }
        waste = {
            item: pulp.LpVariable(f"waste_{item.name}", lowBound=0)
            for item in self.game_items.values()
        }
        # todo these are bad and massively slow things down a graph based solution to get bootstrap before hand would be better
        can_get_item = {
            item: pulp.LpVariable(f"cgi_{item.name}", cat="Binary")
            for item in self.game_items.values() if item.is_valid
        }
        can_get_recipe = {
            recipe: pulp.LpVariable(f"cgr_{recipe.name}", cat="Binary")
            for recipe in self.recipes.values() if recipe.is_valid
        }
        can_get_category = {
            category: pulp.LpVariable(f"cgc_{category.name}", cat="Binary")
            for category in self.categories.values() if category.is_valid
        }
        # Add a 'ghost' supply for every item with a massive penalty
        slack = {
            item: pulp.LpVariable(f"slack_{item.name}", lowBound=0)
            for item in self.game_items.values() if item.is_valid
        }

        # goal
        epsilon = 1e-3
        epsilon_2 = 1e-6
        probBest += (pulp.lpSum(
            recipe.energy * recipe_qty[recipe]
            for recipe in recipe_qty.keys()
        ) + epsilon * pulp.lpSum(can_get_recipe.values())
                     + epsilon_2 * pulp.lpSum(waste.values()) + epsilon_2 * pulp.lpSum(recipe_qty.values())
                     + pulp.lpSum(slack.values()) * 1e10)

        # constraint first pass get best
        for item in self.game_items.values():
            if not item.is_valid:
                continue
            produced = [recipe_qty[recipe] * recipe.products[item] for recipe in item.crafted_by if recipe.is_valid]
            consumed = [recipe_qty[recipe] * recipe.ingredients[item] for recipe in item.used_in if recipe.is_valid]

            if item == goal:
                probBest += pulp.lpSum(produced) - pulp.lpSum(consumed) + slack[item] == 1, f"balance_{item.name}"
            else:
                probBest += pulp.lpSum(produced) - pulp.lpSum(consumed) + slack[item] == 0 + waste[item], f"balance_{item.name}"

            probBest += can_get_item[item] <= pulp.lpSum(can_get_recipe[recipe] for recipe in item.crafted_by if recipe.is_valid), f"can_get_{item.name}"

        big_M = 1e5
        for recipe in self.recipes.values():
            if not recipe.is_valid:
                continue
            rec_qty = recipe_qty[recipe]
            can_rec = can_get_recipe[recipe]

            probBest += rec_qty <= can_rec * big_M
            req = ({can_get_item[cat.item] for cat in recipe.needed_items if cat.is_valid}
                   | {can_get_category[recipe.category]}
                   | {can_get_item[ingredient] for ingredient in recipe.ingredients if ingredient.is_valid})
            for catalyst in req:
                probBest += can_rec <= catalyst

        for category in self.categories.values():
            if category.manual or not category.is_valid:
                continue
            probBest += can_get_category[category] <= pulp.lpSum(can_get_item[item] for item in category.machines if item.is_valid)

        status = probBest.solve(pulp.PULP_CBC_CMD(msg=False))
        score = probBest.objective.value()

        req_recipes = set(recipe for recipe, value in can_get_recipe.items() if not math.isclose(value.value(), 0))

        spawned_items = {item: var.value() for item, var in slack.items() if not math.isclose(var.value(), 0)}
        if spawned_items:
            status = -1
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
            if item.ctx is self:
                return item
            else:
                item = item.name # should never happen but just in case
        if item in self.game_items:
            return self.game_items[item]
        if source != DefinitionSource.EXTRACTED:
            raise RuntimeError(f"{item} is not a valid ingredient")
        self.game_items[item] = GameItem(self, item, DefinitionSource.IMPLIED)
        return self.game_items[item]

    def get_category(self, category: Category | str, source: DefinitionSource = DefinitionSource.IMPLIED) -> Category:
        if type(category) is Category:
            if category.ctx is self:
                return category
            else:
                category = category.name # should never happen but just in case
        if category in self.categories:
            return self.categories[category]
        if source != DefinitionSource.EXTRACTED:
            raise RuntimeError(f"{category} is not a valid category")
        self.categories[category] = Category(self, category, DefinitionSource.IMPLIED)
        return self.categories[category]

    def get_pool_items(self) -> set[GameItem]:
        for item in self.game_items.values():
            item.raw_calculate()
        valid_ingredients = {x for x in self.game_items.values() if x.is_valid_pool}
        return valid_ingredients


class GameItem(RecipeEngineType):
    def __init__(self, ctx: RecipeEngine, name: str, source: DefinitionSource,
                 is_fluid: bool = False):
        super().__init__(ctx, name, source)
        self.is_fluid = is_fluid

        self.has_calculated_raw: bool = False
        self.best_recipes: set[GameRecipe] = set()
        self.score: float = float("inf")
        # self.req_techs: set[TechCatalyst] | None = None

        self.is_valid: bool = True
        self.__is_valid_first_pool: bool = True
        self.__is_valid_pool: bool = source != DefinitionSource.IMPLIED

        self.used_in: set[GameRecipe] = set()
        self.crafted_by: set[GameRecipe] = set()

    @property
    def is_valid_first_pool(self) -> bool:
        return self.is_valid_pool and self.__is_valid_first_pool

    @is_valid_first_pool.setter
    def is_valid_first_pool(self, is_valid_first_pool: bool) -> None:
        self.__is_valid_first_pool = is_valid_first_pool

    @property
    def is_valid_pool(self) -> bool:
        return self.__is_valid_pool and self.is_valid

    @is_valid_pool.setter
    def is_valid_pool(self, is_valid_pool: bool) -> None:
        self.__is_valid_pool = is_valid_pool

    def raw_calculate(self) -> None:
        if self.has_calculated_raw or not self.is_valid:
            return
        self.has_calculated_raw = True

        status, score, best_recipes, waste_recipes, waste = self.ctx.run_pulp_solver(self)
        if status != pulp.LpStatusOptimal:
            if self.name not in {"space-science-pack"}:
                self.ctx.modpack.logger.warn(f"{self}: is uncraftable with status {pulp.LpStatus[status]}")
                self.set_invalid()
            return
        self.score = score
        self.best_recipes = best_recipes
        # self.req_techs = {tech for recipe in self.best_recipes for tech in recipe.catalysts if isinstance(tech, TechCatalyst)}

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
        # if self.name in self.ctx.game_items:
        #     del self.ctx.game_items[self.name]

    def get_req_techs(self) -> set[Technology]:
        techs = set()
        for recipe in self.best_recipes:
            if recipe.name in self.ctx.modpack.start_unlocked_recipes:
                continue
            for tech_cat in recipe.technologies:
                techs.add(tech_cat.tech)
        return techs


class GameRecipe(RecipeEngineType):
    def __init__(self, ctx: RecipeEngine, name: str, source: DefinitionSource, category: Category | str,
                 ingredients: dict[GameItem | str, float], products: dict[GameItem | str, float], energy: float):
        super().__init__(ctx, name, source)

        self.has_calculated_raw: bool = False
        self.is_valid: bool = True

        self.is_starter: bool = name in ctx.modpack.start_unlocked_recipes

        self.ingredients: dict[GameItem, float] = {ctx.get_game_item(ingredient, source): amount
                                                   for ingredient, amount in ingredients.items()}
        self.products: dict[GameItem, float] = {ctx.get_game_item(product, source): amount
                                                for product, amount in products.items()}
        self.energy = energy
        self.technologies: set[TechCatalyst] = set()
        self.categories: set[Category] = set([ctx.get_category(category)])
        self.needed_items: set[ItemCatalyst] = set()

        self.productivity: bool | None = None # ternary set to override default

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
                self.needed_items.add(ctx.get_item_catalyst(ingredient))
                self.products[ingredient] = new_amount
            else:
                del self.products[ingredient]
                self.ingredients[ingredient] = -new_amount

        if self.source == DefinitionSource.WORLD:
            for ingredient in self.ingredients:
                if ingredient.source == DefinitionSource.WORLD:
                    ingredient.used_in.add(self)
            for product in self.products:
                if product.source == DefinitionSource.WORLD:
                    product.crafted_by.add(self)
        elif self.is_valid: # link
            ctx.recipes[self.name] = self
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
        # if self.name in self.ctx.recipes:
        #     del self.ctx.recipes[self.name]

    def get_req_techs(self) -> set[Technology]:
        techs = set()
        for item in self.ingredients.keys():
            techs.update(item.get_req_techs())
        for cat in self.needed_items:
            techs.update(cat.item.get_req_techs())
        if self.name not in self.ctx.modpack.start_unlocked_recipes:
            for tech in self.technologies:
                techs.add(tech.tech)
        return techs




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


class Category(ItemCatalyst):
    def __init__(self, ctx: RecipeEngine, name: str, source: DefinitionSource):
        super().__init__(ctx, name, source)
        self.machines: set[GameItem] = set()
        self.manual = False


class OneItemCatalyst(ItemCatalyst):
    def __init__(self, source: DefinitionSource,
                 item: GameItem):
        super().__init__(item.ctx, item.name, source)
        self.item = item

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