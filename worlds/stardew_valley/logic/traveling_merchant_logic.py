from .cached_logic import profile_rule
from .received_logic import ReceivedLogic
from ..stardew_rule import True_
from ..strings.calendar_names import Weekday


class TravelingMerchantLogic:
    player: int
    received: ReceivedLogic

    def __init__(self, player: int, received_logic: ReceivedLogic):
        self.player = player
        self.received = received_logic

    def has_days(self, number_days: int = 1):
        if number_days <= 0:
            return True_()
        tier = min(7, max(1, number_days))
        traveling_merchant_days = [f"Traveling Merchant: {day}" for day in Weekday.all_days]
        return self.received(traveling_merchant_days, tier)

