from functools import cached_property
from typing import Union

from Utils import cache_self1
from .base_logic import BaseLogic, BaseLogicMixin
from .received_logic import ReceivedLogicMixin
from ..stardew_rule import StardewRule, HasProgressionPercent, True_

MAX_MONTHS = 12
MONTH_COEFFICIENT = 24 // MAX_MONTHS


class TimeLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.time = TimeLogic(*args, **kwargs)


class TimeLogic(BaseLogic[Union[TimeLogicMixin, ReceivedLogicMixin]]):

    @cache_self1
    def has_lived_months(self, number: int) -> StardewRule:
        if number <= 0:
            return True_()
        number = min(number, MAX_MONTHS)
        return HasProgressionPercent(self.player, number * MONTH_COEFFICIENT)

    @cached_property
    def has_lived_max_months(self) -> StardewRule:
        return self.logic.time.has_lived_months(MAX_MONTHS)

    @cached_property
    def has_year_two(self) -> StardewRule:
        return self.logic.time.has_lived_months(4)

    @cached_property
    def has_year_three(self) -> StardewRule:
        return self.logic.time.has_lived_months(8)
