from functools import cached_property
from typing import Tuple, Union

from .base_logic import BaseLogicMixin, BaseLogic
from .farming_logic import FarmingLogicMixin
from .has_logic import HasLogicMixin
from .money_logic import MoneyLogicMixin
from .region_logic import RegionLogicMixin
from ..data.bundle_data import BundleItem
from ..stardew_rule import StardewRule
from ..strings.region_names import Region


class BundleLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bundle = BundleLogic(*args, **kwargs)


class BundleLogic(BaseLogic[Union[HasLogicMixin, RegionLogicMixin, MoneyLogicMixin, FarmingLogicMixin]]):
    # Should be cached
    def can_complete_bundle(self, bundle_requirements: Tuple[BundleItem], number_required: int) -> StardewRule:
        item_rules = []
        highest_quality_yet = 0
        can_speak_junimo = self.logic.region.can_reach(Region.wizard_tower)
        for bundle_item in bundle_requirements:
            if bundle_item.item.item_id == -1:
                return can_speak_junimo & self.logic.money.can_spend(bundle_item.amount)
            else:
                item_rules.append(bundle_item.item.name)
                if bundle_item.quality > highest_quality_yet:
                    highest_quality_yet = bundle_item.quality
        return can_speak_junimo & self.logic.has(tuple(item_rules), number_required) & self.logic.farming.can_grow_crop_quality(highest_quality_yet)

    @cached_property
    def can_complete_community_center(self) -> StardewRule:
        return (self.logic.region.can_reach_location("Complete Crafts Room") &
                self.logic.region.can_reach_location("Complete Pantry") &
                self.logic.region.can_reach_location("Complete Fish Tank") &
                self.logic.region.can_reach_location("Complete Bulletin Board") &
                self.logic.region.can_reach_location("Complete Vault") &
                self.logic.region.can_reach_location("Complete Boiler Room"))
