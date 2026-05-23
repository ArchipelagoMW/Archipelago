from functools import cached_property

from Utils import cache_self1
from .base_logic import BaseLogicMixin, BaseLogic
from ..data.cooking_recipe import CookingRecipe
from ..data.game_item import Source
from ..data.recipe_source import CutsceneSource, StarterSource, SkillSource, FriendshipSource, QueenOfSauceSource
from ..data.shop import ShopSource
from ..options import Chefsanity
from ..stardew_rule import StardewRule
from ..strings.ap_names.ap_option_names import ChefsanityOptionName
from ..strings.building_names import Building
from ..strings.craftable_names import Craftable
from ..strings.region_names import LogicRegion


class CookingLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cooking = CookingLogic(*args, **kwargs)


class CookingLogic(BaseLogic):
    @cached_property
    def can_cook_in_kitchen(self) -> StardewRule:
        return self.logic.building.has_building(Building.kitchen) | self.logic.has(Craftable.cookout_kit)

    # Should be cached
    def can_cook(self, recipe: CookingRecipe | str = None) -> StardewRule:
        cook_rule = self.logic.region.can_reach(LogicRegion.kitchen)
        if recipe is None:
            return cook_rule
        if isinstance(recipe, str):
            recipe = self.content.cooking_recipes[recipe]

        recipe_rule = self.knows_recipe(recipe)
        items = [ingredient for ingredient, amount in recipe.ingredients]
        ingredients_rule = self.logic.has_all(*sorted(items))
        return cook_rule & recipe_rule & ingredients_rule

    @cache_self1
    def knows_recipe(self, recipe: CookingRecipe) -> StardewRule:
        if self.options.chefsanity == Chefsanity.preset_none:
            return self.logic.cooking.can_learn_recipe(recipe)
        rules = []
        for source in recipe.sources:
            rules.append(self.knows_recipe_source(source, recipe.name))
        return self.logic.or_(*rules)

    # Should be cached
    def knows_recipe_source(self, source: Source, meal_name: str) -> StardewRule:
        if isinstance(source, StarterSource):
            return self.logic.cooking.received_recipe(meal_name)
        if isinstance(source, ShopSource) and ChefsanityOptionName.purchases in self.options.chefsanity:
            return self.logic.cooking.received_recipe(meal_name)
        if isinstance(source, SkillSource) and ChefsanityOptionName.skills in self.options.chefsanity:
            return self.logic.cooking.received_recipe(meal_name)
        if isinstance(source, CutsceneSource) and ChefsanityOptionName.friendship in self.options.chefsanity:
            return self.logic.cooking.received_recipe(meal_name)
        if isinstance(source, FriendshipSource) and ChefsanityOptionName.friendship in self.options.chefsanity:
            return self.logic.cooking.received_recipe(meal_name)
        if isinstance(source, QueenOfSauceSource) and ChefsanityOptionName.queen_of_sauce in self.options.chefsanity:
            return self.logic.cooking.received_recipe(meal_name)
        return self.logic.cooking.can_learn_recipe(source)

    @cache_self1
    def can_learn_recipe(self, recipe: CookingRecipe) -> StardewRule:
        return self.logic.source.has_access_to_any(recipe.sources)

    @cache_self1
    def can_learn_recipe_source(self, source: Source) -> StardewRule:
        return self.logic.source.has_access_to(source)

    @cache_self1
    def received_recipe(self, meal_name: str):
        return self.logic.received(f"{meal_name} Recipe")

    def can_have_cooked_recipes(self, number: int) -> StardewRule:
        if number <= 0:
            return self.logic.true_
        recipe_rules = []
        for recipe in self.content.cooking_recipes.values():
            recipe_rules.append(self.can_cook(recipe))
        number = min(len(recipe_rules), number)
        return self.logic.count(number, *recipe_rules)
