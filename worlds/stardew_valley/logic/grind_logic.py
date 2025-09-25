from typing import Union, TYPE_CHECKING

from Utils import cache_self1
from .base_logic import BaseLogic, BaseLogicMixin
from .book_logic import BookLogicMixin
from .has_logic import HasLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from .time_logic import TimeLogicMixin
from ..stardew_rule import StardewRule, HasProgressionPercent
from ..strings.book_names import Book
from ..strings.craftable_names import Consumable
from ..strings.currency_names import Currency
from ..strings.fish_names import WaterChest
from ..strings.geode_names import Geode
from ..strings.material_names import Material
from ..strings.region_names import Region
from ..strings.tool_names import Tool

if TYPE_CHECKING:
    from .tool_logic import ToolLogicMixin
else:
    ToolLogicMixin = object

MIN_MEDIUM_ITEMS = 10
MAX_MEDIUM_ITEMS = 999
PERCENT_REQUIRED_FOR_MAX_MEDIUM_ITEM = 24

EASY_ITEMS = {Material.wood, Material.stone, Material.fiber, Material.sap}
MIN_EASY_ITEMS = 300
MAX_EASY_ITEMS = 2997
PERCENT_REQUIRED_FOR_MAX_EASY_ITEM = 6


class GrindLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grind = GrindLogic(*args, **kwargs)


class GrindLogic(BaseLogic):

    def can_grind_mystery_boxes(self, quantity: int) -> StardewRule:
        opening_rule = self.logic.region.can_reach(Region.blacksmith)
        mystery_box_rule = self.logic.has(Consumable.mystery_box)
        book_of_mysteries_rule = self.logic.true_ \
            if not self.content.features.booksanity.is_enabled \
            else self.logic.book.has_book_power(Book.book_of_mysteries)
        # Assuming one box per day, but halved because we don't know how many months have passed before Mr. Qi's Plane Ride.
        time_rule = self.logic.time.has_lived_months(quantity // 14)
        return self.logic.and_(opening_rule, mystery_box_rule,
                               book_of_mysteries_rule, time_rule, )

    def can_grind_artifact_troves(self, quantity: int) -> StardewRule:
        opening_rule = self.logic.region.can_reach(Region.blacksmith)
        return self.logic.and_(opening_rule, self.logic.has(Geode.artifact_trove),
                               # Assuming one per month if the player does not grind it.
                               self.logic.time.has_lived_months(quantity))

    def can_grind_prize_tickets(self, quantity: int) -> StardewRule:
        claiming_rule = self.logic.region.can_reach(Region.mayor_house)
        return self.logic.and_(claiming_rule, self.logic.has(Currency.prize_ticket),
                               # Assuming two per month if the player does not grind it.
                               self.logic.time.has_lived_months(quantity // 2))

    def can_grind_fishing_treasure_chests(self, quantity: int) -> StardewRule:
        return self.logic.and_(self.logic.has(WaterChest.fishing_chest),
                               # Assuming one per week if the player does not grind it.
                               self.logic.time.has_lived_months(quantity // 4))

    def can_grind_artifact_spots(self, quantity: int) -> StardewRule:
        return self.logic.and_(self.logic.tool.has_tool(Tool.hoe),
                               # Assuming twelve per month if the player does not grind it.
                               self.logic.time.has_lived_months(quantity // 12))

    def can_grind_item(self, quantity: int, item: str | None = None) -> StardewRule:
        if item in EASY_ITEMS:
            return self.logic.grind.can_grind_easy_item(quantity)
        else:
            return self.logic.grind.can_grind_medium_item(quantity)

    @cache_self1
    def can_grind_medium_item(self, quantity: int) -> StardewRule:
        if quantity <= MIN_MEDIUM_ITEMS:
            return self.logic.true_

        quantity = min(quantity, MAX_MEDIUM_ITEMS)
        price = max(1, quantity * PERCENT_REQUIRED_FOR_MAX_MEDIUM_ITEM // MAX_MEDIUM_ITEMS)
        return HasProgressionPercent(self.player, price)

    @cache_self1
    def can_grind_easy_item(self, quantity: int) -> StardewRule:
        if quantity <= MIN_EASY_ITEMS:
            return self.logic.true_

        quantity = min(quantity, MAX_EASY_ITEMS)
        price = max(1, quantity * PERCENT_REQUIRED_FOR_MAX_EASY_ITEM // MAX_EASY_ITEMS)
        return HasProgressionPercent(self.player, price)
