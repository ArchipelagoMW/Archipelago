from .received_logic import ReceivedLogicMixin
from ..stardew_rule import True_
from ..strings.calendar_names import Weekday


class TravelingMerchantLogic:
    player: int
    received: ReceivedLogicMixin

    def __init__(self, player: int, received_logic: ReceivedLogicMixin):
        self.player = player
        self.received = received_logic

    def has_days(self, number_days: int = 1):
        if number_days <= 0:
            return True_()
        tier = min(7, max(1, number_days))
        traveling_merchant_days = tuple(f"Traveling Merchant: {day}" for day in Weekday.all_days)
        return self.received(traveling_merchant_days, tier)
