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


class BundleItemSources:
    vanilla = VanillaItemSource()
    island = IslandItemSource()
    festival = FestivalItemSource()


@dataclass(frozen=True, order=True)
class BundleItem:
    item_name: str
    amount: int = 1
    quality: str = CropQuality.basic
    source: BundleItemSource = BundleItemSources.vanilla

    @staticmethod
    def money_bundle(amount: int):
        return BundleItem(Currency.money, amount)

    def as_amount(self, amount: int):
        return BundleItem(self.item_name, amount, self.quality, self.source)

    def as_quality(self, quality: str):
        return BundleItem(self.item_name, self.amount, quality, self.source)

    def as_quality_crop(self):
        amount = 5
        difficult_crops = [Fruit.sweet_gem_berry, Fruit.ancient_fruit]
        if self.item_name in difficult_crops:
            amount = 1
        return self.as_quality(CropQuality.gold).as_amount(amount)

    def as_quality_fish(self):
        return self.as_quality(FishQuality.gold)

    def as_quality_forage(self):
        return self.as_quality(ForageQuality.gold)

    def __repr__(self):
        quality = "" if self.quality == CropQuality.basic else self.quality
        return f"{self.amount} {quality} {self.item_name}"

    def can_appear(self, options: StardewValleyOptions) -> bool:
        return self.source.can_appear(options)


def IslandBundleItem(*args, **kwargs):
    return BundleItem(*args, source=BundleItemSources.island, **kwargs)


def FestivalBundleItem(*args, **kwargs):
    return BundleItem(*args, source=BundleItemSources.festival, **kwargs)
