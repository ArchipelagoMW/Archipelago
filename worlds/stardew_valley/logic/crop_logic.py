from functools import lru_cache
from typing import Union, Iterable

from .cached_logic import CachedLogic
from .has_logic import HasLogic, CachedRules
from .money_logic import MoneyLogic
from .received_logic import ReceivedLogic
from .region_logic import RegionLogic
from .season_logic import SeasonLogic
from .tool_logic import ToolLogic
from .traveling_merchant_logic import TravelingMerchantLogic
from ..data import CropItem, SeedItem
from ..options import Cropsanity
from ..stardew_rule import StardewRule, True_
from ..strings.forageable_names import Forageable
from ..strings.metal_names import Fossil
from ..strings.region_names import Region
from ..strings.seed_names import Seed
from ..strings.tool_names import Tool


class CropLogic(CachedLogic):
    player: int
    cropsanity_option: Cropsanity
    received: ReceivedLogic
    has: HasLogic
    region: RegionLogic
    traveling_merchant: TravelingMerchantLogic
    season: SeasonLogic
    money: MoneyLogic
    tool: ToolLogic

    def __init__(self, player: int, cached_rules: CachedRules, cropsanity_option: Cropsanity, received: ReceivedLogic, has: HasLogic, region: RegionLogic,
                 traveling_merchant: TravelingMerchantLogic, season: SeasonLogic, money: MoneyLogic, tool: ToolLogic):
        super().__init__(player, cached_rules)
        self.cropsanity_option = cropsanity_option
        self.received = received
        self.has = has
        self.region = region
        self.traveling_merchant = traveling_merchant
        self.season = season
        self.money = money
        self.tool = tool

    @lru_cache(maxsize=None)
    def can_grow(self, crop: CropItem) -> StardewRule:
        season_rule = self.season.has_any(crop.farm_growth_seasons)
        seed_rule = self.has(crop.seed.name)
        farm_rule = self.region.can_reach(Region.farm) & season_rule
        tool_rule = self.tool.has_tool(Tool.hoe) & self.tool.has_tool(Tool.watering_can)
        region_rule = farm_rule | self.region.can_reach(Region.greenhouse) | self.region.can_reach(Region.island_west)
        return seed_rule & region_rule & tool_rule

    def can_plant_and_grow_item(self, seasons: Union[str, Iterable[str]]) -> StardewRule:
        if isinstance(seasons, str):
            seasons = [seasons]
        season_rule = self.season.has_any(seasons) | self.region.can_reach(Region.greenhouse) | self.has_island_farm()
        farm_rule = self.region.can_reach(Region.farm) | self.region.can_reach(
            Region.greenhouse) | self.has_island_farm()
        return season_rule & farm_rule

    def has_island_farm(self) -> StardewRule:
        return self.region.can_reach(Region.island_south)

    @lru_cache(maxsize=None)
    def can_buy_seed(self, seed: SeedItem) -> StardewRule:
        if self.cropsanity_option == Cropsanity.option_disabled or seed.name == Seed.qi_bean:
            item_rule = True_()
        else:
            item_rule = self.received(seed.name)
        if seed.name == Seed.coffee:
            item_rule = item_rule & self.traveling_merchant.has_days(3)
        season_rule = self.season.has_any(seed.seasons)
        region_rule = self.region.can_reach_all(seed.regions)
        currency_rule = self.money.can_spend(1000)
        if seed.name == Seed.pineapple:
            currency_rule = self.has(Forageable.magma_cap)
        if seed.name == Seed.taro:
            currency_rule = self.has(Fossil.bone_fragment)
        return season_rule & region_rule & item_rule & currency_rule
