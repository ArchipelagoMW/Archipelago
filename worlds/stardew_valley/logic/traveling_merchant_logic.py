from typing import Union

from .base_logic import BaseLogic, BaseLogicMixin
from .received_logic import ReceivedLogicMixin
from ..stardew_rule import True_
from ..strings.calendar_names import Weekday


class TravelingMerchantLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.traveling_merchant = TravelingMerchantLogic(*args, **kwargs)


class TravelingMerchantLogic(BaseLogic):

    def has_days(self, number_days: int = 1):
        if number_days <= 0:
            return True_()

        traveling_merchant_days = tuple(f"Traveling Merchant: {day}" for day in Weekday.all_days)
        if number_days == 1:
            return self.logic.received_any(*traveling_merchant_days)

        tier = min(7, max(1, number_days))
        return self.logic.received_n(*traveling_merchant_days, count=tier)
