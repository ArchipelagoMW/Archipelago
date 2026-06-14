from Utils import cache_self1
from .base_logic import BaseLogicMixin, BaseLogic
from .. import options
from ..data.craftable_data import CraftingRecipe
from ..data.game_item import Source
from ..data.recipe_source import ArchipelagoSource, SpecialOrderSource, QuestSource, StarterSource, SkillCraftsanitySource
from ..data.shop import ShopSource
from ..options import Craftsanity, SpecialOrderLocations
from ..stardew_rule import StardewRule, True_


class CraftingLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.crafting = CraftingLogic(*args, **kwargs)


class CraftingLogic(BaseLogic):
    @cache_self1
    def can_craft(self, recipe: CraftingRecipe | str = None) -> StardewRule:
        if recipe is None:
            return True_()

        if isinstance(recipe, str):
            recipe = self.content.crafting_recipes[recipe]

        recipe_rule = self.knows_recipe(recipe)
        items = [ingredient for ingredient, amount in recipe.ingredients]
        if all(isinstance(item, str) for item in items):
            ingredients_rule = self.logic.has_all(*sorted(items))
        else:
            item_rules = []
            for ingredient, amount in recipe.ingredients:
                if isinstance(ingredient, str):
                    item_rules.append(self.logic.has(ingredient))
                else:
                    item_rules.append(self.logic.has_any(*ingredient))
            ingredients_rule = self.logic.and_(*item_rules)
        return recipe_rule & ingredients_rule

    @cache_self1
    def knows_recipe(self, recipe: CraftingRecipe) -> StardewRule:
        rules = []
        for source in recipe.sources:
            rules.append(self.knows_recipe_source(source, recipe.name))
        return self.logic.or_(*rules)

    def knows_recipe_source(self, source: Source, item_name: str) -> StardewRule:
        if isinstance(source, ArchipelagoSource):
            return self.logic.received_all(*source.ap_items)
        if isinstance(source, ShopSource):
            shop_suffix = " - Shop"
            shop_name = source.shop_region
            is_festival_recipe = shop_name in self.content.festivals or (shop_name.endswith(shop_suffix) and shop_name[:-len(shop_suffix)] in self.content.festivals)
            if is_festival_recipe:
                if self.options.festival_locations == options.FestivalLocations.option_disabled:
                    return self.logic.crafting.can_learn_recipe_source(source)
                else:
                    return self.logic.crafting.received_recipe(item_name)
        if isinstance(source, QuestSource):
            if self.options.quest_locations.has_no_story_quests():
                return self.logic.crafting.can_learn_recipe_source(source)
            else:
                return self.logic.crafting.received_recipe(item_name)
        if self.options.craftsanity == Craftsanity.option_none:
            return self.logic.crafting.can_learn_recipe_source(source)
        if isinstance(source, (StarterSource, ShopSource, SkillCraftsanitySource)):
            return self.logic.crafting.received_recipe(item_name)
        if isinstance(source, SpecialOrderSource) and self.options.special_order_locations & SpecialOrderLocations.option_board:
            return self.logic.crafting.received_recipe(item_name)
        return self.logic.crafting.can_learn_recipe_source(source)

    @cache_self1
    def can_learn_recipe(self, recipe: CraftingRecipe) -> StardewRule:
        return self.logic.source.has_access_to_any(recipe.sources)

    @cache_self1
    def can_learn_recipe_source(self, source: Source) -> StardewRule:
        return self.logic.source.has_access_to(source)

    @cache_self1
    def received_recipe(self, item_name: str):
        return self.logic.received(f"{item_name} Recipe")

    def can_have_crafted_recipes(self, number: int) -> StardewRule:
        if number <= 0:
            return self.logic.true_
        recipe_rules = []
        for recipe in self.content.crafting_recipes.values():
            recipe_rules.append(self.can_craft(recipe))
        number = min(len(recipe_rules), number)
        return self.logic.count(number, *recipe_rules)
