from .action_logic import ActionLogic
from .building_logic import BuildingLogic
from .has_logic import HasLogic
from .money_logic import MoneyLogic
from .relationship_logic import RelationshipLogic
from .season_logic import SeasonLogic
from .skill_logic import SkillLogic
from .time_logic import TimeLogic
from ..data.recipe_data import RecipeSource, StarterSource, ShopSource, SkillSource, FriendshipSource, QueenOfSauceSource, CookingRecipe
from ..stardew_rule import StardewRule, True_, False_, And
from ..strings.skill_names import Skill
from ..strings.tv_channel_names import Channel


class CookingLogic:
    player: int
    has: HasLogic
    season: SeasonLogic
    time: TimeLogic
    money: MoneyLogic
    action: ActionLogic
    buildings: BuildingLogic
    relationship: RelationshipLogic
    skill: SkillLogic

    def __init__(self, player: int, has: HasLogic, season: SeasonLogic, time: TimeLogic, money: MoneyLogic, action: ActionLogic, buildings: BuildingLogic,
                 relationship: RelationshipLogic, skill: SkillLogic):
        self.player = player
        self.has = has
        self.season = season
        self.time = time
        self.money = money
        self.action = action
        self.buildings = buildings
        self.relationship = relationship
        self.skill = skill

    def can_cook(self, recipe: CookingRecipe = None) -> StardewRule:
        cook_rule = self.buildings.has_house(1) | self.skill.has_level(Skill.foraging, 9)
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
        if isinstance(source, ShopSource):
            return self.money.can_spend_at(source.region, source.price)
        if isinstance(source, SkillSource):
            return self.skill.has_level(source.skill, source.level)
        if isinstance(source, FriendshipSource):
            return self.relationship.has_hearts(source.friend, source.hearts)
        if isinstance(source, QueenOfSauceSource):
            year_rule = self.time.has_year_two() if source.year == 2 else self.time.has_year_three()
            return self.action.can_watch(Channel.queen_of_sauce) & self.season.has(source.season) & year_rule

        return False_()
