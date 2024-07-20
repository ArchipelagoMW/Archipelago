from functools import cached_property
from typing import Union

from Utils import cache_self1
from .base_logic import BaseLogic, BaseLogicMixin
from .has_logic import HasLogicMixin
from ..stardew_rule import StardewRule, HasProgressionPercent

ONE_YEAR = 4
MAX_MONTHS = 3 * ONE_YEAR
PERCENT_REQUIRED_FOR_MAX_MONTHS = 48
MONTH_COEFFICIENT = PERCENT_REQUIRED_FOR_MAX_MONTHS // MAX_MONTHS

MIN_ITEMS = 10
MAX_ITEMS = 999
PERCENT_REQUIRED_FOR_MAX_ITEM = 24


class TimeLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.time = TimeLogic(*args, **kwargs)


class TimeLogic(BaseLogic[Union[TimeLogicMixin, HasLogicMixin]]):

    @cache_self1
    def has_lived_months(self, number: int) -> StardewRule:
        assert isinstance(number, int), "Can't have lived a fraction of a month. Use // instead of / when dividing."
        if number <= 0:
            return self.logic.true_

        number = min(number, MAX_MONTHS)
        return HasProgressionPercent(self.player, number * MONTH_COEFFICIENT)

    @cached_property
    def has_lived_max_months(self) -> StardewRule:
        return self.logic.time.has_lived_months(MAX_MONTHS)

    @cache_self1
    def has_lived_year(self, number: int) -> StardewRule:
        return self.logic.time.has_lived_months(number * ONE_YEAR)

    @cache_self1
    def has_year(self, number: int) -> StardewRule:
        return self.logic.time.has_lived_year(number - 1)

    @cached_property
    def has_year_two(self) -> StardewRule:
        return self.logic.time.has_year(2)

    @cached_property
    def has_year_three(self) -> StardewRule:
        return self.logic.time.has_year(3)
