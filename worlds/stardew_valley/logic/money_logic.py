import typing
from typing import Union

from Utils import cache_self1
from .base_logic import BaseLogicMixin, BaseLogic
from .grind_logic import GrindLogicMixin
from .has_logic import HasLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from .season_logic import SeasonLogicMixin
from .time_logic import TimeLogicMixin
from ..data.shop import ShopSource
from ..options import SpecialOrderLocations
from ..stardew_rule import StardewRule, True_, HasProgressionPercent, False_, true_
from ..strings.currency_names import Currency
from ..strings.region_names import Region, LogicRegion

if typing.TYPE_CHECKING:
    from .shipping_logic import ShippingLogicMixin

    assert ShippingLogicMixin

qi_gem_rewards = ("100 Qi Gems", "50 Qi Gems", "40 Qi Gems", "35 Qi Gems", "25 Qi Gems",
                  "20 Qi Gems", "15 Qi Gems", "10 Qi Gems")


class MoneyLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.money = MoneyLogic(*args, **kwargs)


class MoneyLogic(BaseLogic[Union[RegionLogicMixin, MoneyLogicMixin, TimeLogicMixin, RegionLogicMixin, ReceivedLogicMixin, HasLogicMixin, SeasonLogicMixin,
GrindLogicMixin, 'ShippingLogicMixin']]):

    @cache_self1
    def can_have_earned_total(self, amount: int) -> StardewRule:
        if amount < 1000:
            return True_()

        pierre_rule = self.logic.region.can_reach_all((Region.pierre_store, Region.forest))
        willy_rule = self.logic.region.can_reach_all((Region.fish_shop, LogicRegion.fishing))
        clint_rule = self.logic.region.can_reach_all((Region.blacksmith, Region.mines_floor_5))
        robin_rule = self.logic.region.can_reach_all((Region.carpenter, Region.secret_woods))
        shipping_rule = self.logic.shipping.can_use_shipping_bin

        if amount < 2000:
            selling_any_rule = pierre_rule | willy_rule | clint_rule | robin_rule | shipping_rule
            return selling_any_rule

        if amount < 5000:
            selling_all_rule = (pierre_rule & willy_rule & clint_rule & robin_rule) | shipping_rule
            return selling_all_rule

        if amount < 10000:
            return shipping_rule

        seed_rules = self.logic.region.can_reach(Region.pierre_store)
        if amount < 40000:
            return shipping_rule & seed_rules

        percent_progression_items_needed = min(90, amount // 20000)
        return shipping_rule & seed_rules & HasProgressionPercent(self.player, percent_progression_items_needed)

    @cache_self1
    def can_spend(self, amount: int) -> StardewRule:
        if self.options.starting_money == -1:
            return True_()
        return self.logic.money.can_have_earned_total(amount * 5)

    # Should be cached
    def can_spend_at(self, region: str, amount: int) -> StardewRule:
        return self.logic.region.can_reach(region) & self.logic.money.can_spend(amount)

    @cache_self1
    def can_shop_from(self, source: ShopSource) -> StardewRule:
        season_rule = self.logic.season.has_any(source.seasons)
        money_rule = self.logic.money.can_spend(source.money_price) if source.money_price is not None else true_

        item_rules = []
        if source.items_price is not None:
            for price, item in source.items_price:
                item_rules.append(self.logic.has(item) & self.logic.grind.can_grind_item(price))

        region_rule = self.logic.region.can_reach(source.shop_region)

        return self.logic.and_(season_rule, money_rule, *item_rules, region_rule)

    # Should be cached
    def can_trade(self, currency: str, amount: int) -> StardewRule:
        if amount == 0:
            return True_()
        if currency == Currency.money:
            return self.can_spend(amount)
        if currency == Currency.star_token:
            return self.logic.region.can_reach(LogicRegion.fair)
        if currency == Currency.qi_coin:
            return self.logic.region.can_reach(Region.casino) & self.logic.time.has_lived_months(amount // 1000)
        if currency == Currency.qi_gem:
            if self.options.special_order_locations & SpecialOrderLocations.value_qi:
                number_rewards = min(len(qi_gem_rewards), max(1, (amount // 10)))
                return self.logic.received_n(*qi_gem_rewards, count=number_rewards)
            number_rewards = 2
            return self.logic.received_n(*qi_gem_rewards, count=number_rewards) & self.logic.region.can_reach(Region.qi_walnut_room) & \
                self.logic.region.can_reach(Region.saloon) & self.can_have_earned_total(5000)
        if currency == Currency.golden_walnut:
            return self.can_spend_walnut(amount)

        return self.logic.has(currency) & self.logic.grind.can_grind_item(amount)

    # Should be cached
    def can_trade_at(self, region: str, currency: str, amount: int) -> StardewRule:
        if amount == 0:
            return True_()
        if currency == Currency.money:
            return self.logic.money.can_spend_at(region, amount)

        return self.logic.region.can_reach(region) & self.can_trade(currency, amount)

    def can_spend_walnut(self, amount: int) -> StardewRule:
        return False_()
