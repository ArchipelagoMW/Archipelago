from .action_logic import ActionLogic
from .building_logic import BuildingLogic
from .has_logic import HasLogic
from .money_logic import MoneyLogic
from .received_logic import ReceivedLogic
from .region_logic import RegionLogic
from .relationship_logic import RelationshipLogic
from .season_logic import SeasonLogic
from .skill_logic import SkillLogic
from .time_logic import TimeLogic
from .. import options
from ..data.recipe_data import RecipeSource, StarterSource, ShopSource, SkillSource, FriendshipSource, QueenOfSauceSource, CookingRecipe, \
    all_cooking_recipes_by_name
from ..data.recipe_source import CutsceneSource, ShopTradeSource, ArchipelagoSource
from ..locations import locations_by_tag, LocationTags
from ..stardew_rule import StardewRule, True_, False_, And
from ..strings.region_names import Region
from ..strings.skill_names import Skill
from ..strings.tv_channel_names import Channel


class CookingLogic:
    player: int
    exclude_ginger_island: int
    received: ReceivedLogic
    has: HasLogic
    region: RegionLogic
    season: SeasonLogic
    time: TimeLogic
    money: MoneyLogic
    action: ActionLogic
    buildings: BuildingLogic
    relationship: RelationshipLogic
    skill: SkillLogic

    def __init__(self, player: int, exclude_ginger_island: int, received: ReceivedLogic, has: HasLogic, region: RegionLogic, season: SeasonLogic, time: TimeLogic, money: MoneyLogic,
                 action: ActionLogic, buildings: BuildingLogic, relationship: RelationshipLogic, skill: SkillLogic):
        self.player = player
        self.exclude_ginger_island = exclude_ginger_island
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

    def can_cook_in_kitchen(self) -> StardewRule:
        return self.buildings.has_house(1) | self.skill.has_level(Skill.foraging, 9)

    def can_cook(self, recipe: CookingRecipe = None) -> StardewRule:
        cook_rule = self.region.can_reach(Region.kitchen)
        if recipe is None:
            return cook_rule

        learn_rule = self.can_learn_recipe(recipe.source)
        ingredients_rule = And([self.has(ingredient) for ingredient in recipe.ingredients])
        number_ingredients = sum(recipe.ingredients[ingredient] for ingredient in recipe.ingredients)
        time_rule = self.time.has_lived_months(number_ingredients)
        return cook_rule & learn_rule & ingredients_rule & time_rule

    def can_learn_recipe(self, source: RecipeSource) -> StardewRule:
        if isinstance(source, StarterSource):
            return True_()
        if isinstance(source, ArchipelagoSource):
            return self.received(source.ap_item, len(source.ap_item))
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
            year_rule = self.time.has_year_two() if source.year == 2 else self.time.has_year_three()
            return self.action.can_watch(Channel.queen_of_sauce) & self.season.has(source.season) & year_rule

        return False_()

    def can_cook_everything(self) -> StardewRule:
        cooksanity_prefix = "Cook "
        all_recipes_to_cook = []
        include_island = self.exclude_ginger_island == options.ExcludeGingerIsland.option_false
        for location in locations_by_tag[LocationTags.COOKSANITY]:
            if include_island or LocationTags.GINGER_ISLAND not in location.tags:
                all_recipes_to_cook.append(location.name[len(cooksanity_prefix):])
        return And([self.can_cook(all_cooking_recipes_by_name[recipe_name]) for recipe_name in all_recipes_to_cook])
