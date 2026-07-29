from functools import cached_property
from typing import List

from .base_logic import BaseLogicMixin, BaseLogic
from ..bundles.bundle import Bundle
from ..stardew_rule import StardewRule, True_
from ..strings.ap_names.community_upgrade_names import CommunityUpgrade
from ..strings.building_names import Building
from ..strings.bundle_names import MemeBundleName
from ..strings.currency_names import Currency
from ..strings.machine_names import Machine
from ..strings.quality_names import CropQuality, ForageQuality, FishQuality, ArtisanQuality
from ..strings.quest_names import Quest
from ..strings.region_names import Region


class BundleLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bundle = BundleLogic(*args, **kwargs)


class BundleLogic(BaseLogic):
    # Should be cached
    def can_complete_bundle(self, bundle: Bundle) -> StardewRule:
        item_rules = []
        qualities = []
        time_to_grind = 0
        building_rule = self.logic.true_
        can_speak_junimo = self.logic.action.can_speak_junimo()
        number_items_required = bundle.number_required
        for bundle_item in bundle.items:
            item = bundle_item.get_item()
            if Currency.is_currency(item):
                return can_speak_junimo & self.logic.money.can_trade(item, bundle_item.amount)
            if item == Building.well:
                building_rule = self.logic.building.has_building(item)
                number_items_required -= 1
            else:
                item_rules.append(item)
            if bundle_item.amount > 50:
                time_to_grind = bundle_item.amount // 50
            qualities.append(bundle_item.quality)
        quality_rules = self.get_quality_rules(qualities)
        item_rules = self.logic.has_n(*item_rules, count=number_items_required)
        time_rule = self.logic.time.has_lived_months(time_to_grind)
        special_rule = self.get_special_bundle_requirement(bundle)
        return can_speak_junimo & item_rules & quality_rules & time_rule & building_rule & special_rule

    def get_special_bundle_requirement(self, bundle: Bundle) -> StardewRule:
        if bundle.name == MemeBundleName.pomnut:
            return self.logic.building.has_building(Building.stable)
        return self.logic.true_

    def get_quality_rules(self, qualities: List[str]) -> StardewRule:
        crop_quality = CropQuality.get_highest(qualities)
        fish_quality = FishQuality.get_highest(qualities)
        forage_quality = ForageQuality.get_highest(qualities)
        artisan_quality = ArtisanQuality.get_highest(qualities)
        quality_rules = []
        if crop_quality != CropQuality.basic:
            quality_rules.append(self.logic.quality.can_grow_crop_quality(crop_quality))
        if fish_quality != FishQuality.basic:
            quality_rules.append(self.logic.fishing.can_catch_quality_fish(fish_quality))
        if forage_quality != ForageQuality.basic:
            quality_rules.append(self.logic.skill.can_forage_quality(forage_quality))
        if artisan_quality != ArtisanQuality.basic:
            quality_rules.append(self.logic.has(Machine.cask))
        if not quality_rules:
            return True_()
        return self.logic.and_(*quality_rules)

    @cached_property
    def can_complete_community_center(self) -> StardewRule:
        return (self.logic.region.can_reach_location("Complete Crafts Room") &
                self.logic.region.can_reach_location("Complete Pantry") &
                self.logic.region.can_reach_location("Complete Fish Tank") &
                self.logic.region.can_reach_location("Complete Bulletin Board") &
                self.logic.region.can_reach_location("Complete Vault") &
                self.logic.region.can_reach_location("Complete Boiler Room"))

    def can_access_raccoon_bundles(self) -> StardewRule:
        if self.options.quest_locations.has_no_story_quests():
            return self.logic.received(CommunityUpgrade.raccoon, 1) & self.logic.quest.can_complete_quest(Quest.giant_stump)

        # 1 - Break the tree
        # 2 - Build the house, which summons the bundle racoon. This one is done manually if quests are turned off
        return self.logic.received(CommunityUpgrade.raccoon, 2)

    def can_feed_trash_bear(self, *items: str) -> StardewRule:
        return (self.logic.received("Trash Bear Arrival") &
                self.logic.region.can_reach(Region.forest) &
                self.logic.has_all(*items))
