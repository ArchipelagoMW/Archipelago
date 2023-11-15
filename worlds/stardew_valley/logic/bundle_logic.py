from functools import cached_property
from typing import Tuple

from .cached_logic import CachedLogic, CachedRules
from .farming_logic import FarmingLogic
from .has_logic import HasLogic
from .money_logic import MoneyLogic
from .region_logic import RegionLogic
from ..data.bundle_data import BundleItem
from ..stardew_rule import StardewRule
from ..strings.region_names import Region


class BundleLogic(CachedLogic):
    has: HasLogic
    region: RegionLogic
    money: MoneyLogic
    farming: FarmingLogic

    def __init__(self, player: int, cached_rules: CachedRules, has: HasLogic, region: RegionLogic, money: MoneyLogic,
                 farming: FarmingLogic):
        super().__init__(player, cached_rules)
        self.has = has
        self.region = region
        self.money = money
        self.farming = farming

    # Should be cached
    def can_complete_bundle(self, bundle_requirements: Tuple[BundleItem], number_required: int) -> StardewRule:
        item_rules = []
        highest_quality_yet = 0
        can_speak_junimo = self.region.can_reach(Region.wizard_tower)
        for bundle_item in bundle_requirements:
            if bundle_item.item.item_id == -1:
                return can_speak_junimo & self.money.can_spend(bundle_item.amount)
            else:
                item_rules.append(bundle_item.item.name)
                if bundle_item.quality > highest_quality_yet:
                    highest_quality_yet = bundle_item.quality
        return can_speak_junimo & self.has(tuple(item_rules), number_required) & self.farming.can_grow_crop_quality(
            highest_quality_yet)

    @cached_property
    def can_complete_community_center(self) -> StardewRule:
        return (self.region.can_reach_location("Complete Crafts Room") &
                self.region.can_reach_location("Complete Pantry") &
                self.region.can_reach_location("Complete Fish Tank") &
                self.region.can_reach_location("Complete Bulletin Board") &
                self.region.can_reach_location("Complete Vault") &
                self.region.can_reach_location("Complete Boiler Room"))
