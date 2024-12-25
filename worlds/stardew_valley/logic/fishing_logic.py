from typing import Union

from Utils import cache_self1
from .base_logic import BaseLogicMixin, BaseLogic
from .has_logic import HasLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from .season_logic import SeasonLogicMixin
from .skill_logic import SkillLogicMixin
from .tool_logic import ToolLogicMixin
from ..data import fish_data
from ..data.fish_data import FishItem
from ..options import ExcludeGingerIsland
from ..options import SpecialOrderLocations
from ..stardew_rule import StardewRule, True_, False_
from ..strings.ap_names.mods.mod_items import SVEQuestItem
from ..strings.craftable_names import Fishing
from ..strings.fish_names import SVEFish
from ..strings.machine_names import Machine
from ..strings.quality_names import FishQuality
from ..strings.region_names import Region
from ..strings.skill_names import Skill


class FishingLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fishing = FishingLogic(*args, **kwargs)


class FishingLogic(BaseLogic[Union[HasLogicMixin, FishingLogicMixin, ReceivedLogicMixin, RegionLogicMixin, SeasonLogicMixin, ToolLogicMixin,
SkillLogicMixin]]):
    def can_fish_in_freshwater(self) -> StardewRule:
        return self.logic.skill.can_fish() & self.logic.region.can_reach_any((Region.forest, Region.town, Region.mountain))

    def has_max_fishing(self) -> StardewRule:
        return self.logic.tool.has_fishing_rod(4) & self.logic.skill.has_level(Skill.fishing, 10)

    def can_fish_chests(self) -> StardewRule:
        return self.logic.tool.has_fishing_rod(4) & self.logic.skill.has_level(Skill.fishing, 6)

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
            item_rule = self.logic.received(SVEQuestItem.kittyfish_spell)
        else:
            item_rule = True_()
        return quest_rule & region_rule & season_rule & difficulty_rule & item_rule

    def can_catch_fish_for_fishsanity(self, fish: FishItem) -> StardewRule:
        """ Rule could be different from the basic `can_catch_fish`. Imagine a fishsanity setting where you need to catch every fish with gold quality.
        """
        return self.logic.fishing.can_catch_fish(fish)

    def can_start_extended_family_quest(self) -> StardewRule:
        if self.options.exclude_ginger_island == ExcludeGingerIsland.option_true:
            return False_()
        if not self.options.special_order_locations & SpecialOrderLocations.value_qi:
            return False_()
        return (self.logic.region.can_reach(Region.qi_walnut_room) &
                self.logic.and_(*(self.logic.fishing.can_catch_fish(fish) for fish in fish_data.vanilla_legendary_fish)))

    def can_catch_quality_fish(self, fish_quality: str) -> StardewRule:
        if fish_quality == FishQuality.basic:
            return True_()
        if fish_quality == FishQuality.silver:
            return self.logic.tool.has_fishing_rod(2)
        if fish_quality == FishQuality.gold:
            return self.logic.skill.has_level(Skill.fishing, 4) & self.can_use_tackle(Fishing.quality_bobber)
        if fish_quality == FishQuality.iridium:
            return self.logic.skill.has_level(Skill.fishing, 10) & self.can_use_tackle(Fishing.quality_bobber)

        raise ValueError(f"Quality {fish_quality} is unknown.")

    def can_use_tackle(self, tackle: str) -> StardewRule:
        return self.logic.tool.has_fishing_rod(4) & self.logic.has(tackle)

    def can_catch_every_fish(self) -> StardewRule:
        rules = [self.has_max_fishing()]

        rules.extend(
            self.logic.fishing.can_catch_fish(fish)
            for fish in self.content.fishes.values()
        )

        return self.logic.and_(*rules)

    def has_specific_bait(self, fish: FishItem) -> StardewRule:
        return self.can_catch_fish(fish) & self.logic.has(Machine.bait_maker)
