from .base_logic import BaseLogic, BaseLogicMixin
from ..options.options import Secretsanity
from ..stardew_rule import StardewRule
from ..strings.craftable_names import Consumable
from ..strings.metal_names import Artifact
from ..strings.region_names import Region
from ..strings.season_names import Season
from ..strings.special_item_names import SpecialItem
from ..strings.villager_names import NPC


class SpecialItemsLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.special_items = SpecialItemsLogic(*args, **kwargs)


class SpecialItemsLogic(BaseLogic):

    def has_purple_shorts(self) -> StardewRule:
        has_first_shorts = self.logic.season.has(Season.summer) & self.logic.relationship.has_hearts(NPC.marnie, 2)
        has_repeatable_shorts = self.logic.region.can_reach(Region.purple_shorts_maze) & self.logic.has(Consumable.warp_totem_farm)
        return has_first_shorts & has_repeatable_shorts
        # can_reach_bedroom = self.logic.region.can_reach(Region.mayor_house) & self.logic.relationship.has_hearts(NPC.lewis, 2)
        # has_repeatable_shorts = can_reach_bedroom & self.logic.has(Craftable.staircase)

    def has_far_away_stone(self) -> StardewRule:
        sacrifice_rule = self.logic.has(Artifact.ancient_doll) & self.logic.region.can_reach_any((Region.mines_floor_100, Region.volcano_floor_10))
        if self.options.secretsanity == Secretsanity.option_none:
            return sacrifice_rule

        return sacrifice_rule & self.logic.received(SpecialItem.far_away_stone)
