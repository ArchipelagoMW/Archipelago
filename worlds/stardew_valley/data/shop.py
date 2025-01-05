from dataclasses import dataclass
from typing import Tuple, Optional

from .game_item import ItemSource
from ..strings.season_names import Season

ItemPrice = Tuple[int, str]


@dataclass(frozen=True, kw_only=True)
class ShopSource(ItemSource):
    shop_region: str
    money_price: Optional[int] = None
    items_price: Optional[Tuple[ItemPrice, ...]] = None
    seasons: Tuple[str, ...] = Season.all

    def __post_init__(self):
        assert self.money_price is not None or self.items_price is not None, "At least money price or items price need to be defined."
        assert self.items_price is None or all(isinstance(p, tuple) for p in self.items_price), "Items price should be a tuple."


@dataclass(frozen=True, kw_only=True)
class MysteryBoxSource(ItemSource):
    amount: int


@dataclass(frozen=True, kw_only=True)
class ArtifactTroveSource(ItemSource):
    amount: int


@dataclass(frozen=True, kw_only=True)
class PrizeMachineSource(ItemSource):
    amount: int


@dataclass(frozen=True, kw_only=True)
class FishingTreasureChestSource(ItemSource):
    amount: int
