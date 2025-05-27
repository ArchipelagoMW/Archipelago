from dataclasses import dataclass
from typing import Tuple, Optional

from .game_item import Source, Requirement
from ..strings.currency_names import Currency
from ..strings.season_names import Season

ItemPrice = Tuple[int, str]


@dataclass(frozen=True, kw_only=True)
class ShopSource(Source):
    shop_region: str
    price: Optional[int] = None
    items_price: Optional[Tuple[ItemPrice, ...]] = None
    seasons: Tuple[str, ...] = Season.all
    currency: str = Currency.money

    def __post_init__(self):
        assert self.price is not None or self.items_price is not None, "At least money price or items price need to be defined."
        assert self.items_price is None or all(isinstance(p, tuple) for p in self.items_price), "Items price should be a tuple."


@dataclass(frozen=True, kw_only=True)
class MysteryBoxSource(Source):
    amount: int


@dataclass(frozen=True, kw_only=True)
class ArtifactTroveSource(Source):
    amount: int


@dataclass(frozen=True, kw_only=True)
class PrizeMachineSource(Source):
    amount: int


@dataclass(frozen=True, kw_only=True)
class FishingTreasureChestSource(Source):
    amount: int


@dataclass(frozen=True, kw_only=True)
class HatMouseSource(Source):
    price: Optional[int] = None
    unlock_requirements: Optional[Tuple[Requirement, ...]] = None
