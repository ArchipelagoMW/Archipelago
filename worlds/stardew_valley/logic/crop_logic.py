from typing import Union, Iterable

from Utils import cache_self1
from .base_logic import BaseLogicMixin, BaseLogic
from .has_logic import HasLogicMixin
from .money_logic import MoneyLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from .season_logic import SeasonLogicMixin
from .tool_logic import ToolLogicMixin
from .traveling_merchant_logic import TravelingMerchantLogicMixin
from ..data import CropItem, SeedItem
from ..options import Cropsanity, ExcludeGingerIsland
from ..stardew_rule import StardewRule, True_, False_
from ..strings.craftable_names import Craftable
from ..strings.forageable_names import Forageable
from ..strings.machine_names import Machine
from ..strings.metal_names import Fossil
from ..strings.region_names import Region
from ..strings.seed_names import Seed
from ..strings.tool_names import Tool


class CropLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.crop = CropLogic(*args, **kwargs)


class CropLogic(BaseLogic[Union[HasLogicMixin, ReceivedLogicMixin, RegionLogicMixin, TravelingMerchantLogicMixin, SeasonLogicMixin, MoneyLogicMixin,
                                ToolLogicMixin, CropLogicMixin]]):
    @cache_self1
    def can_grow(self, crop: CropItem) -> StardewRule:
        season_rule = self.logic.season.has_any(crop.farm_growth_seasons)
        seed_rule = self.logic.has(crop.seed.name)
        farm_rule = self.logic.region.can_reach(Region.farm) & season_rule
        tool_rule = self.logic.tool.has_tool(Tool.hoe) & self.logic.tool.has_tool(Tool.watering_can)
        region_rule = farm_rule | self.logic.region.can_reach(Region.greenhouse) | self.logic.crop.has_island_farm()
        if crop.name == Forageable.cactus_fruit:
            region_rule = self.logic.region.can_reach(Region.greenhouse) | self.logic.has(Craftable.garden_pot)
        return seed_rule & region_rule & tool_rule

    def can_plant_and_grow_item(self, seasons: Union[str, Iterable[str]]) -> StardewRule:
        if isinstance(seasons, str):
            seasons = [seasons]
        season_rule = self.logic.season.has_any(seasons) | self.logic.region.can_reach(Region.greenhouse) | self.logic.crop.has_island_farm()
        farm_rule = self.logic.region.can_reach(Region.farm) | self.logic.region.can_reach(Region.greenhouse) | self.logic.crop.has_island_farm()
        return season_rule & farm_rule

    def has_island_farm(self) -> StardewRule:
        if self.options.exclude_ginger_island == ExcludeGingerIsland.option_false:
            return self.logic.region.can_reach(Region.island_west)
        return False_()

    @cache_self1
    def can_buy_seed(self, seed: SeedItem) -> StardewRule:
        if seed.requires_island and self.options.exclude_ginger_island == ExcludeGingerIsland.option_true:
            return False_()
        if self.options.cropsanity == Cropsanity.option_disabled or seed.name == Seed.qi_bean:
            item_rule = True_()
        else:
            item_rule = self.logic.received(seed.name)
        if seed.name == Seed.coffee:
            item_rule = item_rule & self.logic.traveling_merchant.has_days(3)
        season_rule = self.logic.season.has_any(seed.seasons)
        region_rule = self.logic.region.can_reach_all(seed.regions)
        currency_rule = self.logic.money.can_spend(1000)
        if seed.name == Seed.pineapple:
            currency_rule = self.logic.has(Forageable.magma_cap)
        if seed.name == Seed.taro:
            currency_rule = self.logic.has(Fossil.bone_fragment)
        return season_rule & region_rule & item_rule & currency_rule
