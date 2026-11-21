from .base_logic import BaseLogic, BaseLogicMixin
from ..content.vanilla.ginger_island import ginger_island_content_pack
from ..stardew_rule import StardewRule
from ..strings.ap_names.ap_option_names import SecretsanityOptionName
from ..strings.craftable_names import Consumable
from ..strings.forageable_names import Forageable
from ..strings.metal_names import Artifact
from ..strings.quest_names import Quest
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
        has_first_shorts = self.logic.season.has(Season.summer) &\
                           self.logic.region.can_reach(Region.ranch) &\
                           self.logic.relationship.has_hearts(NPC.marnie, 2)
        has_repeatable_shorts = self.logic.region.can_reach(Region.purple_shorts_maze) & self.logic.has(Consumable.warp_totem_farm)
        return has_first_shorts & has_repeatable_shorts

    def has_far_away_stone(self) -> StardewRule:
        sacrifice_rule = self.logic.has(Artifact.ancient_doll) & self.logic.region.can_reach_any(Region.mines_floor_100, Region.volcano_floor_10)
        if SecretsanityOptionName.easy in self.options.secretsanity:
            return sacrifice_rule & self.logic.received(SpecialItem.far_away_stone)
        return sacrifice_rule

    def has_solid_gold_lewis(self) -> StardewRule:
        if SecretsanityOptionName.secret_notes in self.options.secretsanity:
            return self.logic.received(SpecialItem.solid_gold_lewis) & self.logic.region.can_reach(Region.town)
        return self.logic.has(Forageable.secret_note) & self.logic.region.can_reach(Region.town)

    def has_advanced_tv_remote(self) -> StardewRule:
        george_rule = self.logic.relationship.has_hearts(NPC.george, 10)
        if ginger_island_content_pack.name in self.content.registered_packs:
            return george_rule
        return self.logic.quest.can_complete_quest(Quest.the_pirates_wife) & george_rule
