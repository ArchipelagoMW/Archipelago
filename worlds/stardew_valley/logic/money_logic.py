from typing import Iterable

from .region_logic import RegionLogic
from .time_logic import TimeLogic
from ..stardew_rule import StardewRule, And, Or, Reach, Count, True_

MONEY_PER_MONTH = 15000
DISPOSABLE_INCOME_DIVISOR = 5


class MoneyLogic:
    player: int
    starting_money_option: int
    region: RegionLogic
    time: TimeLogic

    def __init__(self, player: int, starting_money_option: int, region: RegionLogic, time: TimeLogic):
        self.player = player
        self.starting_money_option = starting_money_option
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


