from functools import cached_property
from typing import Union, List

from .base_logic import BaseLogicMixin, BaseLogic
from .farming_logic import FarmingLogicMixin
from .fishing_logic import FishingLogicMixin
from .has_logic import HasLogicMixin
from .money_logic import MoneyLogicMixin
from .region_logic import RegionLogicMixin
from .skill_logic import SkillLogicMixin
from ..bundles.bundle import Bundle
from ..stardew_rule import StardewRule, And, True_
from ..strings.currency_names import Currency
from ..strings.machine_names import Machine
from ..strings.quality_names import CropQuality, ForageQuality, FishQuality, ArtisanQuality
from ..strings.region_names import Region


class BundleLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bundle = BundleLogic(*args, **kwargs)


class BundleLogic(BaseLogic[Union[HasLogicMixin, RegionLogicMixin, MoneyLogicMixin, FarmingLogicMixin, FishingLogicMixin, SkillLogicMixin]]):
    # Should be cached
    def can_complete_bundle(self, bundle: Bundle) -> StardewRule:
        item_rules = []
        qualities = []
        can_speak_junimo = self.logic.region.can_reach(Region.wizard_tower)
        for bundle_item in bundle.items:
            if Currency.is_currency(bundle_item.item_name):
                return can_speak_junimo & self.logic.money.can_trade(bundle_item.item_name, bundle_item.amount)

            item_rules.append(bundle_item.item_name)
            qualities.append(bundle_item.quality)
        quality_rules = self.get_quality_rules(qualities)
        item_rules = self.logic.has_n(*item_rules, count=bundle.number_required)
        return can_speak_junimo & item_rules & quality_rules

    def get_quality_rules(self, qualities: List[str]) -> StardewRule:
        crop_quality = CropQuality.get_highest(qualities)
        fish_quality = FishQuality.get_highest(qualities)
        forage_quality = ForageQuality.get_highest(qualities)
        artisan_quality = ArtisanQuality.get_highest(qualities)
        quality_rules = []
        if crop_quality != CropQuality.basic:
            quality_rules.append(self.logic.farming.can_grow_crop_quality(crop_quality))
        if fish_quality != FishQuality.basic:
            quality_rules.append(self.logic.fishing.can_catch_quality_fish(fish_quality))
        if forage_quality != ForageQuality.basic:
            quality_rules.append(self.logic.skill.can_forage_quality(forage_quality))
        if artisan_quality != ArtisanQuality.basic:
            quality_rules.append(self.logic.has(Machine.cask))
        if not quality_rules:
            return True_()
        return And(*quality_rules)

    @cached_property
    def can_complete_community_center(self) -> StardewRule:
        return (self.logic.region.can_reach_location("Complete Crafts Room") &
                self.logic.region.can_reach_location("Complete Pantry") &
                self.logic.region.can_reach_location("Complete Fish Tank") &
                self.logic.region.can_reach_location("Complete Bulletin Board") &
                self.logic.region.can_reach_location("Complete Vault") &
                self.logic.region.can_reach_location("Complete Boiler Room"))
