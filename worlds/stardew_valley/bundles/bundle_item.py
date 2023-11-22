from dataclasses import dataclass

from ..strings.crop_names import Fruit
from ..strings.quality_names import Quality


@dataclass(frozen=True)
class BundleItem:
    item: str
    amount: int = 1
    quality: str = Quality.basic

    @staticmethod
    def money_bundle(amount: int):
        return BundleItem("Money", amount)

    def as_amount(self, amount: int):
        return BundleItem(self.item, amount, self.quality)

    def as_quality(self, quality: str):
        return BundleItem(self.item, self.amount, quality)

    def as_silver_quality(self):
        return self.as_quality(Quality.silver)

    def as_gold_quality(self):
        return self.as_quality(Quality.gold)

    def as_quality_crop(self):
        amount = 5
        difficult_crops = [Fruit.sweet_gem_berry, Fruit.ancient_fruit]
        if self.item in difficult_crops:
            amount = 1
        return self.as_gold_quality().as_amount(amount)

    def is_gold_quality(self) -> bool:
        return self.quality == Quality.gold or self.quality == Quality.iridium

    def __repr__(self):
        quality = "" if self.quality == Quality.basic else self.quality
        return f"{self.amount} {quality} {self.item}"

    @property
    def requires_island(self) -> bool:
        return False


class IslandBundleItem(BundleItem):

    @property
    def requires_island(self) -> bool:
        return True
