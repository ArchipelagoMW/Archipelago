from .received_logic import ReceivedLogic
from ..stardew_rule import StardewRule
from ..strings.ap_names.event_names import Event

MAX_MONTHS = 12


class TimeLogic:
    player: int
    received: ReceivedLogic

    def __init__(self, player: int, received_logic: ReceivedLogic):
        self.player = player
        self.received = received_logic

    def has_lived_months(self, number: int) -> StardewRule:
        number = max(0, min(number, MAX_MONTHS))
        return self.received(Event.month_end, number)

    def has_lived_max_months(self) -> StardewRule:
        return self.has_lived_months(MAX_MONTHS)

    def has_year_two(self) -> StardewRule:
        return self.has_lived_months(4)

    def has_year_three(self) -> StardewRule:
        return self.has_lived_months(8)

