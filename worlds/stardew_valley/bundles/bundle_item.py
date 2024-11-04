from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..content import StardewContent
from ..options import StardewValleyOptions, ExcludeGingerIsland, FestivalLocations, SkillProgression
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


class MasteryItemSource(BundleItemSource):
    def can_appear(self, options: StardewValleyOptions) -> bool:
        return options.skill_progression == SkillProgression.option_progressive_with_masteries


class ContentItemSource(BundleItemSource):
    """This is meant to be used for items that are managed by the content packs."""

    def can_appear(self, options: StardewValleyOptions) -> bool:
        raise ValueError("This should not be called, check if the item is in the content instead.")


@dataclass(frozen=True, order=True)
class BundleItem:
    class Sources:
        vanilla = VanillaItemSource()
        island = IslandItemSource()
        festival = FestivalItemSource()
        masteries = MasteryItemSource()
        content = ContentItemSource()

    item_name: str
    amount: int = 1
    quality: str = CropQuality.basic
    source: BundleItemSource = Sources.vanilla
    flavor: str = None
    can_have_quality: bool = True

    @staticmethod
    def money_bundle(amount: int) -> BundleItem:
        return BundleItem(Currency.money, amount)

    def get_item(self) -> str:
        if self.flavor is None:
            return self.item_name
        return f"{self.item_name} [{self.flavor}]"

    def as_amount(self, amount: int) -> BundleItem:
        return BundleItem(self.item_name, amount, self.quality, self.source, self.flavor)

    def as_quality(self, quality: str) -> BundleItem:
        if self.can_have_quality:
            return BundleItem(self.item_name, self.amount, quality, self.source, self.flavor)
        return BundleItem(self.item_name, self.amount, self.quality, self.source, self.flavor)

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
        return f"{self.amount} {quality} {self.get_item()}"

    def can_appear(self, content: StardewContent, options: StardewValleyOptions) -> bool:
        if isinstance(self.source, ContentItemSource):
            return self.get_item() in content.game_items

        return self.source.can_appear(options)

