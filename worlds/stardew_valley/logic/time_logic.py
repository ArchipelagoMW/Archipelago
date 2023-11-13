from .cached_logic import CachedLogic, cache_rule, CachedRules
from .received_logic import ReceivedLogic
from ..stardew_rule import StardewRule
from ..strings.ap_names.event_names import Event

MAX_MONTHS = 12


class TimeLogic(CachedLogic):
    received: ReceivedLogic

    def __init__(self, player: int, cached_rules: CachedRules, received_logic: ReceivedLogic):
        super().__init__(player, cached_rules)
        self.received = received_logic

    @cache_rule
    def has_lived_months(self, number: int) -> StardewRule:
        number = max(0, min(number, MAX_MONTHS))
        return self.received(Event.month_end, number)

    def has_lived_max_months(self) -> StardewRule:
        return self.has_lived_months(MAX_MONTHS)

    def has_year_two(self) -> StardewRule:
        return self.has_lived_months(4)

    def has_year_three(self) -> StardewRule:
        return self.has_lived_months(8)

