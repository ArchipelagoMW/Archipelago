from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..options import StardewValleyOptions, ExcludeGingerIsland, FestivalLocations
from ..strings.crop_names import Fruit
from ..strings.currency_names import Currency
from ..strings.quality_names import CropQuality, FishQuality, ForageQuality


class BundleItemSource(ABC):
    @abstractmethod
    def can_appear(self, options: StardewValleyOptions) -> bool:
        ...


class VanillaItemSource(BundleItemSource):
    def can_appear(self, options: StardewValleyOptions) -> bool:
        return True


class IslandItemSource(BundleItemSource):
    def can_appear(self, options: StardewValleyOptions) -> bool:
        return options.exclude_ginger_island == ExcludeGingerIsland.option_false


class FestivalItemSource(BundleItemSource):
    def can_appear(self, options: StardewValleyOptions) -> bool:
        return options.festival_locations != FestivalLocations.option_disabled


@dataclass(frozen=True, order=True)
class BundleItem:
    class Sources:
        vanilla = VanillaItemSource()
        island = IslandItemSource()
        festival = FestivalItemSource()

    item_name: str
    amount: int = 1
    quality: str = CropQuality.basic
    source: BundleItemSource = Sources.vanilla

    @staticmethod
    def money_bundle(amount: int) -> BundleItem:
        return BundleItem(Currency.money, amount)

    def as_amount(self, amount: int) -> BundleItem:
        return BundleItem(self.item_name, amount, self.quality, self.source)

    def as_quality(self, quality: str) -> BundleItem:
        return BundleItem(self.item_name, self.amount, quality, self.source)

    def as_quality_crop(self) -> BundleItem:
        amount = 5
        difficult_crops = [Fruit.sweet_gem_berry, Fruit.ancient_fruit]
        if self.item_name in difficult_crops:
            amount = 1
        return self.as_quality(CropQuality.gold).as_amount(amount)

    def as_quality_fish(self) -> BundleItem:
        return self.as_quality(FishQuality.gold)

    def as_quality_forage(self) -> BundleItem:
        return self.as_quality(ForageQuality.gold)

    def __repr__(self):
        quality = "" if self.quality == CropQuality.basic else self.quality
        return f"{self.amount} {quality} {self.item_name}"

    def can_appear(self, options: StardewValleyOptions) -> bool:
        return self.source.can_appear(options)
