from functools import cached_property
from typing import Union

from Utils import cache_self1
from .base_logic import BaseLogic, BaseLogicMixin
from .has_logic import HasLogicMixin
from .received_logic import ReceivedLogicMixin
from ..stardew_rule import StardewRule, HasProgressionPercent, True_

ONE_YEAR = 4
MAX_MONTHS = 3 * ONE_YEAR
PERCENT_REQUIRED_FOR_MAX_MONTHS = 24
MONTH_COEFFICIENT = PERCENT_REQUIRED_FOR_MAX_MONTHS // MAX_MONTHS

MIN_ITEMS = 10
MAX_ITEMS = 999
PERCENT_REQUIRED_FOR_MAX_ITEM = 24
ITEMS_COEFFICIENT = PERCENT_REQUIRED_FOR_MAX_ITEM // MAX_ITEMS


class TimeLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.time = TimeLogic(*args, **kwargs)


class TimeLogic(BaseLogic[Union[TimeLogicMixin, HasLogicMixin, ReceivedLogicMixin]]):

    @cache_self1
    def has_can_grind_item(self, quantity: int) -> StardewRule:
        if quantity <= MIN_ITEMS:
            return self.logic.true_

        quantity = min(quantity, MAX_ITEMS)
        return HasProgressionPercent(self.player, quantity * ITEMS_COEFFICIENT)

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
        return self.logic.time.has_lived_months(2 * ONE_YEAR)

    @cached_property
    def has_year_three(self) -> StardewRule:
        return self.logic.time.has_lived_months(3 * ONE_YEAR)
