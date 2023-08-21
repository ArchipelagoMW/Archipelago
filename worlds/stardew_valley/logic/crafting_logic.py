from .has_logic import HasLogic
from .money_logic import MoneyLogic
from .received_logic import ReceivedLogic
from .region_logic import RegionLogic
from .relationship_logic import RelationshipLogic
from .skill_logic import SkillLogic
from .time_logic import TimeLogic
from ..data.craftable_data import CraftingRecipe
from ..data.recipe_data import RecipeSource, StarterSource, ShopSource, SkillSource, FriendshipSource
from ..data.recipe_source import CutsceneSource, ShopTradeSource, ArchipelagoSource, LogicSource
from ..stardew_rule import StardewRule, True_, False_, And
from ..strings.region_names import Region


class CraftingLogic:
    player: int
    received: ReceivedLogic
    has: HasLogic
    region: RegionLogic
    time: TimeLogic
    money: MoneyLogic
    relationship: RelationshipLogic
    skill: SkillLogic

    def __init__(self, player: int, received: ReceivedLogic, has: HasLogic, region: RegionLogic, time: TimeLogic, money: MoneyLogic,
                 relationship: RelationshipLogic, skill: SkillLogic):
        self.player = player
        self.received = received
        self.has = has
        self.region = region
        self.time = time
        self.money = money
        self.relationship = relationship
        self.skill = skill

    def can_craft(self, recipe: CraftingRecipe = None) -> StardewRule:
        craft_rule = True_()
        if recipe is None:
            return craft_rule

        learn_rule = self.can_learn_recipe(recipe.source)
        ingredients_rule = And([self.has(ingredient) for ingredient in recipe.ingredients])
        number_ingredients = sum(recipe.ingredients[ingredient] for ingredient in recipe.ingredients) // 10
        time_rule = self.time.has_lived_months(number_ingredients)
        return craft_rule & learn_rule & ingredients_rule & time_rule

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
        if isinstance(source, LogicSource):
            if source.logic_rule == "Cellar":
                return self.region.can_reach(Region.cellar)

        return False_()
