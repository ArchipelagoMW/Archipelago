from collections.abc import Iterable
from dataclasses import dataclass

from .game_item import Source, Requirement
from ..strings.currency_names import Currency
from ..strings.season_names import Season

ItemPrice = tuple[int, str]


@dataclass(frozen=True, kw_only=True)
class ShopSource(Source):
    shop_region: str
    price: int | None = None
    items_price: tuple[ItemPrice, ...] | None = None
    seasons: tuple[str, ...] = Season.all
    currency: str = Currency.money
    forbidden_items: tuple[str, ...] | None = tuple()

    def __post_init__(self):
        assert self.price is not None or self.items_price is not None, "At least money price or items price need to be defined."
        assert self.items_price is None or all(isinstance(p, tuple) for p in self.items_price), "Items price should be a tuple."

    def __repr__(self):
        return f"Region: {self.shop_region}, Price: {self.price}, Items: {self.items_price}, Seasons: {self.seasons}, Currency: {self.currency}"

    def __lt__(self, other):
        return self.__repr__() < other.__repr__()


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
    price: int | None = None
    unlock_requirements: tuple[Requirement, ...] | None = None

    @property
    def all_requirements(self) -> Iterable[Requirement]:
        return self.other_requirements + (self.unlock_requirements or ())
