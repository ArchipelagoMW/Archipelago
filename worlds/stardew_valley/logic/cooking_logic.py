from functools import cached_property
from typing import Union

from Utils import cache_self1
from .action_logic import ActionLogicMixin
from .base_logic import BaseLogicMixin, BaseLogic
from .building_logic import BuildingLogicMixin
from .has_logic import HasLogicMixin
from .money_logic import MoneyLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from .relationship_logic import RelationshipLogicMixin
from .season_logic import SeasonLogicMixin
from .skill_logic import SkillLogicMixin
from ..data.recipe_data import RecipeSource, StarterSource, ShopSource, SkillSource, FriendshipSource, \
    QueenOfSauceSource, CookingRecipe, ShopFriendshipSource
from ..data.recipe_source import CutsceneSource, ShopTradeSource
from ..options import Chefsanity
from ..stardew_rule import StardewRule, True_, False_
from ..strings.region_names import LogicRegion
from ..strings.skill_names import Skill
from ..strings.tv_channel_names import Channel


class CookingLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cooking = CookingLogic(*args, **kwargs)


class CookingLogic(BaseLogic[Union[HasLogicMixin, ReceivedLogicMixin, RegionLogicMixin, SeasonLogicMixin, MoneyLogicMixin, ActionLogicMixin,
BuildingLogicMixin, RelationshipLogicMixin, SkillLogicMixin, CookingLogicMixin]]):
    @cached_property
    def can_cook_in_kitchen(self) -> StardewRule:
        return self.logic.building.has_house(1) | self.logic.skill.has_level(Skill.foraging, 9)

    # Should be cached
    def can_cook(self, recipe: CookingRecipe = None) -> StardewRule:
        cook_rule = self.logic.region.can_reach(LogicRegion.kitchen)
        if recipe is None:
            return cook_rule

        recipe_rule = self.logic.cooking.knows_recipe(recipe.source, recipe.meal)
        ingredients_rule = self.logic.has_all(*sorted(recipe.ingredients))
        return cook_rule & recipe_rule & ingredients_rule

    # Should be cached
    def knows_recipe(self, source: RecipeSource, meal_name: str) -> StardewRule:
        if self.options.chefsanity == Chefsanity.option_none:
            return self.logic.cooking.can_learn_recipe(source)
        if isinstance(source, StarterSource):
            return self.logic.cooking.received_recipe(meal_name)
        if isinstance(source, ShopTradeSource) and self.options.chefsanity & Chefsanity.option_purchases:
            return self.logic.cooking.received_recipe(meal_name)
        if isinstance(source, ShopSource) and self.options.chefsanity & Chefsanity.option_purchases:
            return self.logic.cooking.received_recipe(meal_name)
        if isinstance(source, SkillSource) and self.options.chefsanity & Chefsanity.option_skills:
            return self.logic.cooking.received_recipe(meal_name)
        if isinstance(source, CutsceneSource) and self.options.chefsanity & Chefsanity.option_friendship:
            return self.logic.cooking.received_recipe(meal_name)
        if isinstance(source, FriendshipSource) and self.options.chefsanity & Chefsanity.option_friendship:
            return self.logic.cooking.received_recipe(meal_name)
        if isinstance(source, QueenOfSauceSource) and self.options.chefsanity & Chefsanity.option_queen_of_sauce:
            return self.logic.cooking.received_recipe(meal_name)
        if isinstance(source, ShopFriendshipSource) and self.options.chefsanity & Chefsanity.option_purchases:
            return self.logic.cooking.received_recipe(meal_name)
        return self.logic.cooking.can_learn_recipe(source)

    @cache_self1
    def can_learn_recipe(self, source: RecipeSource) -> StardewRule:
        if isinstance(source, StarterSource):
            return True_()
        if isinstance(source, ShopTradeSource):
            return self.logic.money.can_trade_at(source.region, source.currency, source.price)
        if isinstance(source, ShopSource):
            return self.logic.money.can_spend_at(source.region, source.price)
        if isinstance(source, SkillSource):
            return self.logic.skill.has_level(source.skill, source.level)
        if isinstance(source, CutsceneSource):
            return self.logic.region.can_reach(source.region) & self.logic.relationship.has_hearts(source.friend, source.hearts)
        if isinstance(source, FriendshipSource):
            return self.logic.relationship.has_hearts(source.friend, source.hearts)
        if isinstance(source, QueenOfSauceSource):
            return self.logic.action.can_watch(Channel.queen_of_sauce) & self.logic.season.has(source.season)
        if isinstance(source, ShopFriendshipSource):
            return self.logic.money.can_spend_at(source.region, source.price) & self.logic.relationship.has_hearts(source.friend, source.hearts)
        return False_()

    @cache_self1
    def received_recipe(self, meal_name: str):
        return self.logic.received(f"{meal_name} Recipe")
