from typing import Iterable

from .has_logic import HasLogic
from .received_logic import ReceivedLogic
from .region_logic import RegionLogic
from .time_logic import TimeLogic
from ..stardew_rule import StardewRule, And, Or, Reach, Count, True_
from ..strings.currency_names import Currency

MONEY_PER_MONTH = 15000
DISPOSABLE_INCOME_DIVISOR = 5

qi_gem_rewards = ["100 Qi Gems", "50 Qi Gems", "40 Qi Gems", "40 Qi Gems", "40 Qi Gems", "35 Qi Gems", "25 Qi Gems", "25 Qi Gems", "20 Qi Gems", "10 Qi Gems"]


class MoneyLogic:
    player: int
    starting_money_option: int
    received: ReceivedLogic
    has: HasLogic
    region: RegionLogic
    time: TimeLogic

    def __init__(self, player: int, starting_money_option: int, received: ReceivedLogic, has: HasLogic, region: RegionLogic, time: TimeLogic):
        self.player = player
        self.starting_money_option = starting_money_option
        self.received = received
        self.has = has
        self.region = region
        self.time = time

    def can_have_earned_total(self, amount: int) -> StardewRule:
        if self.starting_money_option == -1:
            return True_()
        return self.time.has_lived_months(amount // MONEY_PER_MONTH)

    def can_spend(self, amount: int) -> StardewRule:
        if self.starting_money_option == -1:
            return True_()
        return self.time.has_lived_months(amount // (MONEY_PER_MONTH // DISPOSABLE_INCOME_DIVISOR))

    def can_spend_at(self, region: str, amount: int) -> StardewRule:
        return self.region.can_reach(region) & self.can_spend(amount)

    def can_trade_at(self, region: str, currency: str, amount: int) -> StardewRule:
        if amount == 0:
            return True_()
        if currency == Currency.money:
            return self.can_spend_at(region, amount)
        if currency == Currency.qi_gem:
            number_rewards = min(10, max(1, (amount // 10) + 2))
            return self.received(qi_gem_rewards, number_rewards)

        return self.region.can_reach(region) & self.has(currency)


