from dataclasses import dataclass

from ..strings.crop_names import Fruit
from ..strings.currency_names import Currency
from ..strings.quality_names import CropQuality, FishQuality, ForageQuality


@dataclass(frozen=True, order=True)
class BundleItem:
    item_name: str
    amount: int = 1
    quality: str = CropQuality.basic
    requires_island: bool = False

    @staticmethod
    def money_bundle(amount: int):
        return BundleItem(Currency.money, amount)

    def as_amount(self, amount: int):
        return BundleItem(self.item_name, amount, self.quality, requires_island=self.requires_island)

    def as_quality(self, quality: str):
        return BundleItem(self.item_name, self.amount, quality, requires_island=self.requires_island)

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


def IslandBundleItem(*args, **kwargs):
    return BundleItem(*args, requires_island=True, **kwargs)
