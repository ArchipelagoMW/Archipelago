from dataclasses import dataclass
from typing import Tuple, Optional

from .game_item import ItemSource, source_dataclass_args
from ..strings.season_names import Season

ItemPrice = Tuple[int, str]


@dataclass(**source_dataclass_args)
class ShopSource(ItemSource):
    shop_region: str
    money_price: Optional[int] = None
    items_price: Optional[Tuple[ItemPrice, ...]] = None
    seasons: Tuple[str, ...] = Season.all

    def __post_init__(self):
        assert self.money_price or self.items_price, "At least money price or items price need to be defined."
        assert self.items_price is None or all(type(p) == tuple for p in self.items_price), "Items price should be a tuple."
