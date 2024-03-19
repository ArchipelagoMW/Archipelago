from typing import Union

from Utils import cache_self1
from .base_logic import BaseLogicMixin, BaseLogic
from .buff_logic import BuffLogicMixin
from .has_logic import HasLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from .time_logic import TimeLogicMixin
from ..options import SpecialOrderLocations
from ..stardew_rule import StardewRule, True_, HasProgressionPercent, False_
from ..strings.ap_names.event_names import Event
from ..strings.currency_names import Currency
from ..strings.region_names import Region

qi_gem_rewards = ("100 Qi Gems", "50 Qi Gems", "40 Qi Gems", "35 Qi Gems", "25 Qi Gems",
                  "20 Qi Gems", "15 Qi Gems", "10 Qi Gems")


class MoneyLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.money = MoneyLogic(*args, **kwargs)


class MoneyLogic(BaseLogic[Union[RegionLogicMixin, MoneyLogicMixin, TimeLogicMixin, RegionLogicMixin, ReceivedLogicMixin, HasLogicMixin, BuffLogicMixin]]):

    @cache_self1
    def can_have_earned_total(self, amount: int) -> StardewRule:
        if amount < 1000:
            return True_()

        pierre_rule = self.logic.region.can_reach_all((Region.pierre_store, Region.forest))
        willy_rule = self.logic.region.can_reach_all((Region.fish_shop, Region.fishing))
        clint_rule = self.logic.region.can_reach_all((Region.blacksmith, Region.mines_floor_5))
        robin_rule = self.logic.region.can_reach_all((Region.carpenter, Region.secret_woods))
        shipping_rule = self.logic.received(Event.can_ship_items)

        if amount < 2000:
            selling_any_rule = pierre_rule | willy_rule | clint_rule | robin_rule | shipping_rule
            return selling_any_rule

        if amount < 5000:
            selling_all_rule = (pierre_rule & willy_rule & clint_rule & robin_rule) | shipping_rule
            return selling_all_rule

        if amount < 10000:
            return shipping_rule

        seed_rules = self.logic.received(Event.can_shop_at_pierre)
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

    # Should be cached
    def can_trade(self, currency: str, amount: int) -> StardewRule:
        if amount == 0:
            return True_()
        if currency == Currency.money:
            return self.can_spend(amount)
        if currency == Currency.star_token:
            return self.logic.region.can_reach(Region.fair)
        if currency == Currency.qi_coin:
            return self.logic.region.can_reach(Region.casino) & self.logic.buff.has_max_luck()
        if currency == Currency.qi_gem:
            if self.options.special_order_locations == SpecialOrderLocations.option_board_qi:
                number_rewards = min(len(qi_gem_rewards), max(1, (amount // 10)))
                return self.logic.received_n(*qi_gem_rewards, count=number_rewards)
            number_rewards = 2
            return self.logic.received_n(*qi_gem_rewards, count=number_rewards) & self.logic.region.can_reach(Region.qi_walnut_room) & \
                self.logic.region.can_reach(Region.saloon) & self.can_have_earned_total(5000)
        if currency == Currency.golden_walnut:
            return self.can_spend_walnut(amount)

        return self.logic.has(currency) & self.logic.time.has_lived_months(amount)

    # Should be cached
    def can_trade_at(self, region: str, currency: str, amount: int) -> StardewRule:
        if amount == 0:
            return True_()
        if currency == Currency.money:
            return self.logic.money.can_spend_at(region, amount)

        return self.logic.region.can_reach(region) & self.can_trade(currency, amount)

    def can_spend_walnut(self, amount: int) -> StardewRule:
        return False_()
