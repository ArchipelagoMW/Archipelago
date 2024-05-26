from functools import cached_property
from typing import Union

from Utils import cache_self1
from .base_logic import BaseLogic, BaseLogicMixin
from .book_logic import BookLogicMixin
from .has_logic import HasLogicMixin
from .received_logic import ReceivedLogicMixin
from ..stardew_rule import StardewRule, HasProgressionPercent
from ..strings.book_names import Book
from ..strings.craftable_names import Consumable

ONE_YEAR = 4
MAX_MONTHS = 3 * ONE_YEAR
PERCENT_REQUIRED_FOR_MAX_MONTHS = 24
MONTH_COEFFICIENT = PERCENT_REQUIRED_FOR_MAX_MONTHS // MAX_MONTHS

MIN_ITEMS = 10
MAX_ITEMS = 999
PERCENT_REQUIRED_FOR_MAX_ITEM = 24


class TimeLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.time = TimeLogic(*args, **kwargs)


class TimeLogic(BaseLogic[Union[TimeLogicMixin, HasLogicMixin, ReceivedLogicMixin, BookLogicMixin]]):

    @cache_self1
    def can_grind_mystery_boxes(self, quantity: int) -> StardewRule:
        return self.logic.and_(self.logic.has(Consumable.mystery_box),
                               self.logic.book.has_book_power(Book.book_of_mysteries),
                               # Assuming 1 box per day, but halved because we don't know how many months have passed before Mr. Qi's Plane Ride
                               self.logic.time.has_lived_months(quantity // 14))

    @cache_self1
    def can_grind_item(self, quantity: int) -> StardewRule:
        if quantity <= MIN_ITEMS:
            return self.logic.true_

        quantity = min(quantity, MAX_ITEMS)
        price = max(1, quantity * PERCENT_REQUIRED_FOR_MAX_ITEM // MAX_ITEMS)
        return HasProgressionPercent(self.player, price)

    @cache_self1
    def has_lived_months(self, number: int) -> StardewRule:
        if number <= 0:
            return self.logic.true_
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
