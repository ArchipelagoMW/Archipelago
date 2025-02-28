from functools import cached_property
from typing import Union

from Utils import cache_self1
from .base_logic import BaseLogicMixin, BaseLogic
from .has_logic import HasLogicMixin
from .money_logic import MoneyLogicMixin
from .quest_logic import QuestLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from .relationship_logic import RelationshipLogicMixin
from .skill_logic import SkillLogicMixin
from .special_order_logic import SpecialOrderLogicMixin
from .. import options
from ..data.craftable_data import CraftingRecipe, all_crafting_recipes_by_name
from ..data.recipe_source import CutsceneSource, ShopTradeSource, ArchipelagoSource, LogicSource, SpecialOrderSource, \
    FestivalShopSource, QuestSource, StarterSource, ShopSource, SkillSource, MasterySource, FriendshipSource, SkillCraftsanitySource
from ..locations import locations_by_tag, LocationTags
from ..options import Craftsanity, SpecialOrderLocations, ExcludeGingerIsland
from ..stardew_rule import StardewRule, True_, False_
from ..strings.region_names import Region


class CraftingLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.crafting = CraftingLogic(*args, **kwargs)


class CraftingLogic(BaseLogic[Union[ReceivedLogicMixin, HasLogicMixin, RegionLogicMixin, MoneyLogicMixin, RelationshipLogicMixin,
SkillLogicMixin, SpecialOrderLogicMixin, CraftingLogicMixin, QuestLogicMixin]]):
    @cache_self1
    def can_craft(self, recipe: CraftingRecipe = None) -> StardewRule:
        if recipe is None:
            return True_()

        learn_rule = self.logic.crafting.knows_recipe(recipe)
        ingredients_rule = self.logic.has_all(*recipe.ingredients)
        return learn_rule & ingredients_rule

    @cache_self1
    def knows_recipe(self, recipe: CraftingRecipe) -> StardewRule:
        if isinstance(recipe.source, ArchipelagoSource):
            return self.logic.received_all(*recipe.source.ap_item)
        if isinstance(recipe.source, FestivalShopSource):
            if self.options.festival_locations == options.FestivalLocations.option_disabled:
                return self.logic.crafting.can_learn_recipe(recipe)
            else:
                return self.logic.crafting.received_recipe(recipe.item)
        if isinstance(recipe.source, QuestSource):
            if self.options.quest_locations < 0:
                return self.logic.crafting.can_learn_recipe(recipe)
            else:
                return self.logic.crafting.received_recipe(recipe.item)
        if self.options.craftsanity == Craftsanity.option_none:
            return self.logic.crafting.can_learn_recipe(recipe)
        if isinstance(recipe.source, (StarterSource, ShopTradeSource, ShopSource, SkillCraftsanitySource)):
            return self.logic.crafting.received_recipe(recipe.item)
        if isinstance(recipe.source, SpecialOrderSource) and self.options.special_order_locations & SpecialOrderLocations.option_board:
            return self.logic.crafting.received_recipe(recipe.item)
        return self.logic.crafting.can_learn_recipe(recipe)

    @cache_self1
    def can_learn_recipe(self, recipe: CraftingRecipe) -> StardewRule:
        if isinstance(recipe.source, StarterSource):
            return True_()
        if isinstance(recipe.source, ArchipelagoSource):
            return self.logic.received_all(*recipe.source.ap_item)
        if isinstance(recipe.source, ShopTradeSource):
            return self.logic.money.can_trade_at(recipe.source.region, recipe.source.currency, recipe.source.price)
        if isinstance(recipe.source, ShopSource):
            return self.logic.money.can_spend_at(recipe.source.region, recipe.source.price)
        if isinstance(recipe.source, SkillCraftsanitySource):
            return self.logic.skill.has_level(recipe.source.skill, recipe.source.level) & self.logic.skill.can_earn_level(recipe.source.skill, recipe.source.level)
        if isinstance(recipe.source, SkillSource):
            return self.logic.skill.has_level(recipe.source.skill, recipe.source.level)
        if isinstance(recipe.source, MasterySource):
            return self.logic.skill.has_mastery(recipe.source.skill)
        if isinstance(recipe.source, CutsceneSource):
            return self.logic.region.can_reach(recipe.source.region) & self.logic.relationship.has_hearts(recipe.source.friend, recipe.source.hearts)
        if isinstance(recipe.source, FriendshipSource):
            return self.logic.relationship.has_hearts(recipe.source.friend, recipe.source.hearts)
        if isinstance(recipe.source, QuestSource):
            return self.logic.quest.can_complete_quest(recipe.source.quest)
        if isinstance(recipe.source, SpecialOrderSource):
            if self.options.special_order_locations & SpecialOrderLocations.option_board:
                return self.logic.crafting.received_recipe(recipe.item)
            return self.logic.special_order.can_complete_special_order(recipe.source.special_order)
        if isinstance(recipe.source, LogicSource):
            if recipe.source.logic_rule == "Cellar":
                return self.logic.region.can_reach(Region.cellar)

        return False_()

    @cache_self1
    def received_recipe(self, item_name: str):
        return self.logic.received(f"{item_name} Recipe")

    @cached_property
    def can_craft_everything(self) -> StardewRule:
        craftsanity_prefix = "Craft "
        all_recipes_names = []
        exclude_island = self.options.exclude_ginger_island == ExcludeGingerIsland.option_true
        exclude_masteries = not self.content.features.skill_progression.are_masteries_shuffled
        for location in locations_by_tag[LocationTags.CRAFTSANITY]:
            if not location.name.startswith(craftsanity_prefix):
                continue
            if exclude_island and LocationTags.GINGER_ISLAND in location.tags:
                continue
            # FIXME Remove when recipes are in content packs
            if exclude_masteries and LocationTags.REQUIRES_MASTERIES in location.tags:
                continue
            if location.mod_name and location.mod_name not in self.options.mods:
                continue
            all_recipes_names.append(location.name[len(craftsanity_prefix):])
        all_recipes = [all_crafting_recipes_by_name[recipe_name] for recipe_name in all_recipes_names]
        return self.logic.and_(*(self.logic.crafting.can_craft(recipe) for recipe in all_recipes))
