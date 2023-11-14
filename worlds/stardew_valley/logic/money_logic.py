from functools import lru_cache

from .cached_logic import CachedLogic
from .has_logic import HasLogic, CachedRules
from .received_logic import ReceivedLogic
from .region_logic import RegionLogic
from .time_logic import TimeLogic
from ..options import StartingMoney
from ..stardew_rule import StardewRule, True_
from ..strings.currency_names import Currency

MONEY_PER_MONTH = 15000
DISPOSABLE_INCOME_DIVISOR = 5

qi_gem_rewards = ("100 Qi Gems", "50 Qi Gems", "40 Qi Gems", "40 Qi Gems", "40 Qi Gems", "35 Qi Gems", "25 Qi Gems",
                  "25 Qi Gems", "20 Qi Gems", "10 Qi Gems")


class MoneyLogic(CachedLogic):
    starting_money_option: StartingMoney
    received: ReceivedLogic
    has: HasLogic
    region: RegionLogic
    time: TimeLogic

    def __init__(self, player: int, cached_rules: CachedRules, starting_money_option: StartingMoney,
                 received: ReceivedLogic,
                 has: HasLogic, region: RegionLogic, time: TimeLogic):
        super().__init__(player, cached_rules)
        self.starting_money_option = starting_money_option
        self.received = received
        self.has = has
        self.region = region
        self.time = time

    @lru_cache(maxsize=None)
    def can_have_earned_total(self, amount: int) -> StardewRule:
        if self.starting_money_option == -1:
            return True_()
        return self.time.has_lived_months(amount // MONEY_PER_MONTH)

    @lru_cache(maxsize=None)
    def can_spend(self, amount: int) -> StardewRule:
        if self.starting_money_option == -1:
            return True_()
        return self.time.has_lived_months(amount // (MONEY_PER_MONTH // DISPOSABLE_INCOME_DIVISOR))

    @lru_cache(maxsize=None)
    def can_spend_at(self, region: str, amount: int) -> StardewRule:
        return self.region.can_reach(region) & self.can_spend(amount)

    @lru_cache(maxsize=None)
    def can_trade_at(self, region: str, currency: str, amount: int) -> StardewRule:
        if amount == 0:
            return True_()
        if currency == Currency.money:
            return self.can_spend_at(region, amount)
        if currency == Currency.qi_gem:
            number_rewards = min(10, max(1, (amount // 10) + 2))
            return self.received(qi_gem_rewards, number_rewards)

        return self.region.can_reach(region) & self.has(currency)
