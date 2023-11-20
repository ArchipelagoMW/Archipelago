from functools import cached_property

from Utils import cache_self1
from .action_logic import ActionLogicMixin
from .building_logic import BuildingLogicMixin
from .has_logic import HasLogicMixin
from .money_logic import MoneyLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from .relationship_logic import RelationshipLogic
from .season_logic import SeasonLogicMixin
from .skill_logic import SkillLogic
from .time_logic import TimeLogicMixin
from ..data.recipe_data import RecipeSource, StarterSource, ShopSource, SkillSource, FriendshipSource, \
    QueenOfSauceSource, CookingRecipe, \
    all_cooking_recipes_by_name
from ..data.recipe_source import CutsceneSource, ShopTradeSource
from ..locations import locations_by_tag, LocationTags
from ..options import Chefsanity
from ..options import ExcludeGingerIsland, Mods
from ..stardew_rule import StardewRule, True_, False_, And
from ..strings.region_names import Region
from ..strings.skill_names import Skill
from ..strings.tv_channel_names import Channel


class CookingLogic:
    chefsanity_option: Chefsanity
    exclude_ginger_island: ExcludeGingerIsland
    mods: Mods
    received: ReceivedLogicMixin
    has: HasLogicMixin
    region: RegionLogicMixin
    season: SeasonLogicMixin
    time: TimeLogicMixin
    money: MoneyLogicMixin
    action: ActionLogicMixin
    buildings: BuildingLogicMixin
    relationship: RelationshipLogic
    skill: SkillLogic

    def __init__(self, player: int, chefsanity_option: Chefsanity, exclude_ginger_island: ExcludeGingerIsland, mods: Mods, received: ReceivedLogicMixin,
                 has: HasLogicMixin, region: RegionLogicMixin, season: SeasonLogicMixin, time: TimeLogicMixin, money: MoneyLogicMixin, action: ActionLogicMixin,
                 buildings: BuildingLogicMixin,
                 relationship: RelationshipLogic, skill: SkillLogic):
        self.player = player
        self.chefsanity_option = chefsanity_option
        self.exclude_ginger_island = exclude_ginger_island
        self.mods = mods
        self.received = received
        self.has = has
        self.region = region
        self.season = season
        self.time = time
        self.money = money
        self.action = action
        self.buildings = buildings
        self.relationship = relationship
        self.skill = skill

    @cached_property
    def can_cook_in_kitchen(self) -> StardewRule:
        return self.buildings.has_house(1) | self.skill.has_level(Skill.foraging, 9)

    # Should be cached
    def can_cook(self, recipe: CookingRecipe = None) -> StardewRule:
        cook_rule = self.region.can_reach(Region.kitchen)
        if recipe is None:
            return cook_rule

        recipe_rule = self.knows_recipe(recipe.source, recipe.meal)
        ingredients_rule = And(*(self.has(ingredient) for ingredient in recipe.ingredients))
        return cook_rule & recipe_rule & ingredients_rule

    # Should be cached
    def knows_recipe(self, source: RecipeSource, meal_name: str) -> StardewRule:
        if self.chefsanity_option == Chefsanity.option_none:
            return self.can_learn_recipe(source)
        if isinstance(source, StarterSource):
            return self.received_recipe(meal_name)
        if isinstance(source, ShopTradeSource) and self.chefsanity_option & Chefsanity.option_purchases:
            return self.received_recipe(meal_name)
        if isinstance(source, ShopSource) and self.chefsanity_option & Chefsanity.option_purchases:
            return self.received_recipe(meal_name)
        if isinstance(source, SkillSource) and self.chefsanity_option & Chefsanity.option_skills:
            return self.received_recipe(meal_name)
        if isinstance(source, CutsceneSource) and self.chefsanity_option & Chefsanity.option_friendship:
            return self.received_recipe(meal_name)
        if isinstance(source, FriendshipSource) and self.chefsanity_option & Chefsanity.option_friendship:
            return self.received_recipe(meal_name)
        if isinstance(source, QueenOfSauceSource) and self.chefsanity_option & Chefsanity.option_queen_of_sauce:
            return self.received_recipe(meal_name)
        return self.can_learn_recipe(source)

    @cache_self1
    def can_learn_recipe(self, source: RecipeSource) -> StardewRule:
        if isinstance(source, StarterSource):
            return True_()
        if isinstance(source, ShopTradeSource):
            return self.money.can_trade_at(source.region, source.currency, source.price)
        if isinstance(source, ShopSource):
            return self.money.can_spend_at(source.region, source.price)
        if isinstance(source, SkillSource):
            return self.skill.has_level(source.skill, source.level)
        if isinstance(source, CutsceneSource):
            return self.region.can_reach(source.region) & self.relationship.has_hearts(source.friend, source.hearts)
        if isinstance(source, FriendshipSource):
            return self.relationship.has_hearts(source.friend, source.hearts)
        if isinstance(source, QueenOfSauceSource):
            return self.action.can_watch(Channel.queen_of_sauce) & self.season.has(source.season)
        return False_()

    @cache_self1
    def received_recipe(self, meal_name: str):
        return self.received(f"{meal_name} Recipe")

    @cached_property
    def can_cook_everything(self) -> StardewRule:
        cooksanity_prefix = "Cook "
        all_recipes_names = []
        exclude_island = self.exclude_ginger_island == ExcludeGingerIsland.option_true
        for location in locations_by_tag[LocationTags.COOKSANITY]:
            if exclude_island and LocationTags.GINGER_ISLAND in location.tags:
                continue
            if location.mod_name and location.mod_name not in self.mods:
                continue
            all_recipes_names.append(location.name[len(cooksanity_prefix):])
        all_recipes = [all_cooking_recipes_by_name[recipe_name] for recipe_name in all_recipes_names]
        return And(*(self.can_cook(recipe) for recipe in all_recipes))
