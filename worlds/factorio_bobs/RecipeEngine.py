from __future__ import annotations

import json
from enum import Enum
from functools import cached_property
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Technology, FactorioModpack

GENERATOR_ENERGY = 0

class DefinitionSource(Enum):
    UNKNOWN = 0
    EXTRACTED = 1
    CUSTOM = 2
    IMPLIED = 3

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

        self.item_catalysts: dict[GameItem, ItemCatalyst] = {}
        self.categories: dict[str, CategoryCatalyst] = {}
        self.fluid_mining: OrTechsCatalyst = OrTechsCatalyst(self, "FluidMining", DefinitionSource.EXTRACTED)

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
            if ingredient.name in self.modpack.ordered_science_packs or invalid_items:
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
                    self.categories[category].manual = True
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
                self.fluid_mining.techs.add(technology)
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
                self.get_game_item(ingredient, DefinitionSource.CUSTOM).is_valid_ingredient = False

        if "excluded_automation_ingredients" in raw_settings:
            for ingredient in raw_settings["excluded_automation_ingredients"]:
                self.get_game_item(ingredient, DefinitionSource.CUSTOM).is_valid_first_pool = False

    def __link_recipes(self):
        for recipe in self.recipes.values():
            recipe.link()

    def __remove_bad_items(self):
        for item in self.game_items.values():
            if item.crafted_by:
                continue
            if item.used_in:
                if item.is_valid_pool:
                    self.modpack.logger.warning(f"{item.name} is used but not method of obtaining it detected.\n"
                                                "Consider disabling it or adding a custom recipe")
                continue
            item.is_valid_ingredient = False

    def get_item_catalyst(self, item: GameItem) -> ItemCatalyst:
        if item not in self.item_catalysts:
            self.item_catalysts[item] = ItemCatalyst(DefinitionSource.IMPLIED, item)
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

        self.is_valid_ingredient: bool = True
        self.__is_valid_first_pool: bool = True
        self.__is_valid_pool: bool = True

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
        return self.is_valid_ingredient and self.__is_valid_pool

    @is_valid_pool.setter
    def is_valid_pool(self, is_valid_pool: bool) -> None:
        self.__is_valid_pool = is_valid_pool


class GameRecipe(RecipeEngineType):
    def __init__(self, ctx: RecipeEngine, name: str, source: DefinitionSource,
                 ingredients: dict[GameItem | str, float], products: dict[GameItem | str, float], energy: float):
        super().__init__(ctx, name, source)

        self.has_calculated_raw: bool = False
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
            if not ingredient.is_valid_ingredient:
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


class Catalyst(RecipeEngineType):
    pass

class CategoryCatalyst(Catalyst):
    def __init__(self, ctx: RecipeEngine, name: str, source: DefinitionSource):
        super().__init__(ctx, name, source)
        self.machines: set[GameItem] = set()

class OrTechsCatalyst(Catalyst):
    def __init__(self, ctx: RecipeEngine, name: str, source: DefinitionSource):
        super().__init__(ctx, name, source)
        self.techs: set[Technology] = set()

class ItemCatalyst(Catalyst):
    def __init__(self, source: DefinitionSource,
                 item: GameItem):
        super().__init__(item.ctx, item.name, source)
        self.item = item

class TechCatalyst(Catalyst):
    def __init__(self, ctx: RecipeEngine, source: DefinitionSource, tech: Technology):
        super().__init__(ctx, tech.name, source)
        self.tech = tech
