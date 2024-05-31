from typing import Union

from Utils import cache_self1
from .base_logic import BaseLogic, BaseLogicMixin
from .book_logic import BookLogicMixin
from .has_logic import HasLogicMixin
from .received_logic import ReceivedLogicMixin
from .time_logic import TimeLogicMixin
from ..options import Booksanity
from ..stardew_rule import StardewRule, HasProgressionPercent
from ..strings.book_names import Book
from ..strings.craftable_names import Consumable
from ..strings.currency_names import Currency
from ..strings.fish_names import WaterChest
from ..strings.geode_names import Geode

MIN_ITEMS = 10
MAX_ITEMS = 999
PERCENT_REQUIRED_FOR_MAX_ITEM = 24


class GrindLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grind = GrindLogic(*args, **kwargs)


class GrindLogic(BaseLogic[Union[GrindLogicMixin, HasLogicMixin, ReceivedLogicMixin, BookLogicMixin, TimeLogicMixin]]):

    def can_grind_mystery_boxes(self, quantity: int) -> StardewRule:
        mystery_box_rule = self.logic.has(Consumable.mystery_box)
        book_of_mysteries_rule = self.logic.true_ if self.options.booksanity == Booksanity.option_none else self.logic.book.has_book_power(Book.book_of_mysteries)
        # Assuming one box per day, but halved because we don't know how many months have passed before Mr. Qi's Plane Ride.
        time_rule = self.logic.time.has_lived_months(quantity // 14)
        return self.logic.and_(mystery_box_rule,
                               book_of_mysteries_rule,
                               time_rule)

    def can_grind_artifact_troves(self, quantity: int) -> StardewRule:
        return self.logic.and_(self.logic.has(Geode.artifact_trove),
                               # Assuming one per month if the player does not grind it.
                               self.logic.time.has_lived_months(quantity))

    def can_grind_prize_tickets(self, quantity: int) -> StardewRule:
        return self.logic.and_(self.logic.has(Currency.prize_ticket),
                               # Assuming two per month if the player does not grind it.
                               self.logic.time.has_lived_months(quantity // 2))

    def can_grind_fishing_treasure_chests(self, quantity: int) -> StardewRule:
        return self.logic.and_(self.logic.has(WaterChest.fishing_chest),
                               # Assuming one per week if the player does not grind it.
                               self.logic.time.has_lived_months(quantity // 4))

    @cache_self1
    def can_grind_item(self, quantity: int) -> StardewRule:
        if quantity <= MIN_ITEMS:
            return self.logic.true_

        quantity = min(quantity, MAX_ITEMS)
        price = max(1, quantity * PERCENT_REQUIRED_FOR_MAX_ITEM // MAX_ITEMS)
        return HasProgressionPercent(self.player, price)
