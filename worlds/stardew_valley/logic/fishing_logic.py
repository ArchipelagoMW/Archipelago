from functools import cached_property

from Utils import cache_self1
from .base_logic import BaseLogicMixin, BaseLogic
from ..content.vanilla.qi_board import qi_board_content_pack
from ..data import fish_data
from ..data.fish_data import FishItem
from ..stardew_rule import StardewRule, True_
from ..strings.ap_names.ap_option_names import CustomLogicOptionName
from ..strings.ap_names.mods.mod_items import SVEQuestItem
from ..strings.craftable_names import Fishing
from ..strings.fish_names import SVEFish
from ..strings.machine_names import Machine
from ..strings.quality_names import FishQuality
from ..strings.region_names import Region
from ..strings.skill_names import Skill
from ..strings.tool_names import FishingRod


class FishingLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fishing = FishingLogic(*args, **kwargs)


class FishingLogic(BaseLogic):

    @cached_property
    def can_reach_any_fishing_regions(self) -> StardewRule:
        return self.logic.region.can_reach_any(Region.beach, Region.town, Region.forest, Region.mountain, Region.island_south, Region.island_west)

    @cache_self1
    def can_fish_anywhere(self, difficulty: int = 0) -> StardewRule:
        return self.logic.fishing.can_fish(difficulty) & self.logic.fishing.can_reach_any_fishing_regions

    def can_fish_in_freshwater(self) -> StardewRule:
        return self.logic.fishing.can_fish() & self.logic.region.can_reach_any(Region.forest, Region.town, Region.mountain)

    @cached_property
    def has_max_fishing(self) -> StardewRule:
        # Advanced Iridium is not necessary for max fishing
        return self.logic.tool.has_fishing_rod(FishingRod.iridium) & self.logic.skill.has_level(Skill.fishing, 10)

    @cached_property
    def can_fish_chests(self) -> StardewRule:
        return self.logic.tool.has_fishing_rod(FishingRod.iridium) & self.logic.skill.has_level(Skill.fishing, 6)

    @cache_self1
    def can_fish_at(self, region: str) -> StardewRule:
        return self.logic.fishing.can_fish() & self.logic.region.can_reach(region)

    def can_fish_with_cast_distance(self, region: str, distance: int) -> StardewRule:
        if distance >= 7:
            required_levels = 15
        elif distance >= 6:
            required_levels = 8
        elif distance >= 5:
            required_levels = 4
        elif distance >= 4:
            required_levels = 1
        else:
            required_levels = 0
        return self.logic.fishing.can_fish_at(region) & self.logic.skill.has_level(Skill.fishing, required_levels)

    def can_fish(self, difficulty: int = 0, minimum_level: int = 0) -> StardewRule:
        skill_required = int((difficulty / 10) - 1)
        if difficulty <= 40:
            skill_required = 0

        if CustomLogicOptionName.extreme_fishing in self.options.custom_logic:
            skill_required -= 4
        elif CustomLogicOptionName.hard_fishing in self.options.custom_logic:
            skill_required -= 2
        elif CustomLogicOptionName.easy_fishing in self.options.custom_logic and difficulty > 20:
            skill_required += 2

        skill_required = min(10, max(minimum_level, skill_required))

        skill_rule = self.logic.skill.has_level(Skill.fishing, skill_required)
        # Training rod only works with fish < 50. Fiberglass does not help you to catch higher difficulty fish, so it's skipped in logic.
        if difficulty < 50:
            fishing_rod_required = FishingRod.training
        elif difficulty < 80:
            fishing_rod_required = FishingRod.bamboo
        else:
            fishing_rod_required = FishingRod.iridium
        return self.logic.tool.has_fishing_rod(fishing_rod_required) & skill_rule

    @cache_self1
    def can_catch_fish(self, fish: FishItem) -> StardewRule:
        quest_rule = True_()
        if fish.extended_family:
            quest_rule = self.logic.fishing.can_start_extended_family_quest()
        region_rule = self.logic.region.can_reach_any(*fish.locations)
        season_rule = self.logic.season.has_any(fish.seasons)

        if fish.difficulty == -1:
            difficulty_rule = self.logic.fishing.can_crab_pot
        else:
            difficulty_rule = self.logic.fishing.can_fish(120 if fish.legendary else fish.difficulty, fish.minimum_level)

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
        if self.content.is_enabled(qi_board_content_pack):
            return (self.logic.region.can_reach(Region.qi_walnut_room) &
                    self.logic.and_(*(self.logic.fishing.can_catch_fish(fish) for fish in fish_data.vanilla_legendary_fish)))

        return self.logic.false_

    def can_catch_quality_fish(self, fish_quality: str) -> StardewRule:
        if fish_quality == FishQuality.basic:
            return self.logic.true_
        if fish_quality == FishQuality.silver:
            return self.logic.tool.has_fishing_rod(FishingRod.bamboo)
        if fish_quality == FishQuality.gold:
            return self.logic.skill.has_level(Skill.fishing, 4) & self.can_use_tackle(Fishing.quality_bobber)
        if fish_quality == FishQuality.iridium:
            return self.logic.skill.has_level(Skill.fishing, 10) & self.can_use_tackle(Fishing.quality_bobber)

        raise ValueError(f"Quality {fish_quality} is unknown.")

    def can_use_tackle(self, tackle: str) -> StardewRule:
        return self.logic.tool.has_fishing_rod(FishingRod.iridium) & self.logic.has(tackle)

    def can_catch_every_fish(self) -> StardewRule:
        rules = [self.has_max_fishing]

        rules.extend(
            self.logic.fishing.can_catch_fish(fish)
            for fish in self.content.fishes.values()
        )

        return self.logic.and_(*rules)

    def can_catch_many_fish(self, number: int) -> StardewRule:
        rules = [
            self.logic.fishing.can_catch_fish(fish)
            for fish in self.content.fishes.values()
        ]
        if number > len(rules):
            number = len(rules)
        return self.logic.count(number, *rules)

    def has_specific_bait(self, fish: FishItem) -> StardewRule:
        return self.can_catch_fish(fish) & self.logic.has(Machine.bait_maker)

    def can_use_specific_bait(self, fish_name: str) -> StardewRule:
        return self.has_specific_bait(self.content.fishes[fish_name]) & self.logic.tool.has_fishing_rod(FishingRod.fiberglass)

    def can_use_any_bait(self) -> StardewRule:
        return self.logic.has(Fishing.bait) & self.logic.tool.has_fishing_rod(FishingRod.fiberglass)

    @cached_property
    def can_crab_pot_anywhere(self) -> StardewRule:
        return self.logic.fishing.can_crab_pot & self.can_reach_any_fishing_regions

    @cache_self1
    def can_crab_pot_at(self, region: str) -> StardewRule:
        return self.logic.fishing.can_crab_pot & self.logic.region.can_reach(region)

    @cached_property
    def can_crab_pot(self) -> StardewRule:
        return self.logic.has(Machine.crab_pot) & self.logic.has(Fishing.bait)
