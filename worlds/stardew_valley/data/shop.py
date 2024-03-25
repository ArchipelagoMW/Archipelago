from dataclasses import dataclass, field
from typing import Tuple

from .game_item import ItemSource, source_dataclass_args
from ..strings.season_names import Season


@dataclass(**source_dataclass_args)
class ShopSource(ItemSource):
    shop: str
    money_price: int = field(default=0)
    items_price: Tuple[str, ...] = field(default=())
    seasons: Tuple[str, ...] = field(default=Season.all)

    def __post_init__(self):
        assert self.money_price or self.items_price, "At least money price or items price need to be defined."
