from typing import Union, List

from Utils import cache_self1
from .base_logic import BaseLogicMixin, BaseLogic
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from .season_logic import SeasonLogicMixin
from .skill_logic import SkillLogicMixin
from .tool_logic import ToolLogicMixin
from ..data import FishItem, fish_data
from ..locations import LocationTags, locations_by_tag
from ..options import ExcludeGingerIsland, Fishsanity
from ..options import SpecialOrderLocations
from ..stardew_rule import StardewRule, True_, False_, And
from ..strings.fish_names import SVEFish
from ..strings.quality_names import FishQuality
from ..strings.region_names import Region
from ..strings.skill_names import Skill


class FishingLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fishing = FishingLogic(*args, **kwargs)


class FishingLogic(BaseLogic[Union[FishingLogicMixin, ReceivedLogicMixin, RegionLogicMixin, SeasonLogicMixin, ToolLogicMixin, SkillLogicMixin]]):
    def can_fish_in_freshwater(self) -> StardewRule:
        return self.logic.skill.can_fish() & self.logic.region.can_reach_any((Region.forest, Region.town, Region.mountain))

    def has_max_fishing(self) -> StardewRule:
        skill_rule = self.logic.skill.has_level(Skill.fishing, 10)
        return self.logic.tool.has_fishing_rod(4) & skill_rule

    def can_fish_chests(self) -> StardewRule:
        skill_rule = self.logic.skill.has_level(Skill.fishing, 6)
        return self.logic.tool.has_fishing_rod(4) & skill_rule

    def can_fish_at(self, region: str) -> StardewRule:
        return self.logic.skill.can_fish() & self.logic.region.can_reach(region)

    @cache_self1
    def can_catch_fish(self, fish: FishItem) -> StardewRule:
        quest_rule = True_()
        if fish.extended_family:
            quest_rule = self.logic.fishing.can_start_extended_family_quest()
        region_rule = self.logic.region.can_reach_any(fish.locations)
        season_rule = self.logic.season.has_any(fish.seasons)
        if fish.difficulty == -1:
            difficulty_rule = self.logic.skill.can_crab_pot
        else:
            difficulty_rule = self.logic.skill.can_fish(difficulty=(120 if fish.legendary else fish.difficulty))
        if fish.name == SVEFish.kittyfish:
            item_rule = self.logic.received("Kittyfish Spell")
        else:
            item_rule = True_()
        return quest_rule & region_rule & season_rule & difficulty_rule & item_rule

    def can_start_extended_family_quest(self) -> StardewRule:
        if self.options.exclude_ginger_island == ExcludeGingerIsland.option_true:
            return False_()
        if self.options.special_order_locations != SpecialOrderLocations.option_board_qi:
            return False_()
        return self.logic.region.can_reach(Region.qi_walnut_room) & And(*(self.logic.fishing.can_catch_fish(fish) for fish in fish_data.legendary_fish))

    def can_catch_quality_fish(self, fish_quality: str) -> StardewRule:
        if fish_quality == FishQuality.basic:
            return True_()
        rod_rule = self.logic.tool.has_fishing_rod(2)
        if fish_quality == FishQuality.silver:
            return rod_rule
        if fish_quality == FishQuality.gold:
            return rod_rule & self.logic.skill.has_level(Skill.fishing, 4)
        if fish_quality == FishQuality.iridium:
            return rod_rule & self.logic.skill.has_level(Skill.fishing, 10)

        raise ValueError(f"Quality {fish_quality} is unknown.")

    def can_catch_every_fish(self) -> StardewRule:
        rules = [self.has_max_fishing()]
        exclude_island = self.options.exclude_ginger_island == ExcludeGingerIsland.option_true
        exclude_extended_family = self.options.special_order_locations != SpecialOrderLocations.option_board_qi
        for fish in fish_data.get_fish_for_mods(self.options.mods.value):
            if exclude_island and fish in fish_data.island_fish:
                continue
            if exclude_extended_family and fish in fish_data.extended_family:
                continue
            rules.append(self.logic.fishing.can_catch_fish(fish))
        return And(*rules)

    def can_catch_every_fish_in_slot(self, all_location_names_in_slot: List[str]) -> StardewRule:
        if self.options.fishsanity == Fishsanity.option_none:
            return self.can_catch_every_fish()

        rules = [self.has_max_fishing()]

        for fishsanity_location in locations_by_tag[LocationTags.FISHSANITY]:
            if fishsanity_location.name not in all_location_names_in_slot:
                continue
            rules.append(self.logic.region.can_reach_location(fishsanity_location.name))
        return And(*rules)
