from dataclasses import dataclass, field
from typing import Tuple

from .game_item import ItemSource
from ..strings.season_names import Season


@dataclass(frozen=True)
class ShopSource(ItemSource):
    money_price: int = field(default=0, kw_only=True)
    items_price: Tuple[str, ...] = field(default=(), kw_only=True)
    shop: str = field(kw_only=True)
    seasons: Tuple[str, ...] = field(default=Season.all, kw_only=True)
