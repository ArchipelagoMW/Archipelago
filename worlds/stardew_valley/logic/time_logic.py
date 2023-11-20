from functools import cached_property

from Utils import cache_self1
from .base_logic import LogicRegistry
from .received_logic import ReceivedLogicMixin
from ..stardew_rule import StardewRule, CountPercent, True_
from ..strings.ap_names.event_names import Event

MAX_MONTHS = 12
MONTH_COEFFICIENT = 100 // MAX_MONTHS


class TimeLogicMixin(ReceivedLogicMixin):
    def __init__(self, player: int, registry: LogicRegistry):
        super().__init__(player, registry)
        self.time = self

    @cache_self1
    def has_lived_months(self, number: int) -> StardewRule:
        if number <= 0:
            return True_()
        number = min(number, MAX_MONTHS)
        return CountPercent(self.player, number * MONTH_COEFFICIENT)

    @cached_property
    def has_lived_max_months(self) -> StardewRule:
        return self.has_lived_months(MAX_MONTHS)

    @cached_property
    def has_year_two(self) -> StardewRule:
        return self.has_lived_months(4)

    @cached_property
    def has_year_three(self) -> StardewRule:
        return self.has_lived_months(8)
