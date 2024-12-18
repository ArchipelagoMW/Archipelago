from functools import cached_property
from typing import Union, Tuple

from Utils import cache_self1
from .base_logic import BaseLogicMixin, BaseLogic
from .combat_logic import CombatLogicMixin
from .harvesting_logic import HarvestingLogicMixin
from .has_logic import HasLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from .season_logic import SeasonLogicMixin
from .time_logic import TimeLogicMixin
from .tool_logic import ToolLogicMixin
from ..data.harvest import HarvestCropSource
from ..mods.logic.magic_logic import MagicLogicMixin
from ..mods.logic.mod_skills_levels import get_mod_skill_levels
from ..stardew_rule import StardewRule, true_, True_, False_
from ..strings.craftable_names import Fishing
from ..strings.machine_names import Machine
from ..strings.performance_names import Performance
from ..strings.quality_names import ForageQuality
from ..strings.region_names import Region
from ..strings.skill_names import Skill, all_mod_skills, all_vanilla_skills
from ..strings.tool_names import ToolMaterial, Tool
from ..strings.wallet_item_names import Wallet

fishing_regions = (Region.beach, Region.town, Region.forest, Region.mountain, Region.island_south, Region.island_west)
vanilla_skill_items = ("Farming Level", "Mining Level", "Foraging Level", "Fishing Level", "Combat Level")


class SkillLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.skill = SkillLogic(*args, **kwargs)


class SkillLogic(BaseLogic[Union[HasLogicMixin, ReceivedLogicMixin, RegionLogicMixin, SeasonLogicMixin, TimeLogicMixin, ToolLogicMixin, SkillLogicMixin,
CombatLogicMixin, MagicLogicMixin, HarvestingLogicMixin]]):

    # Should be cached
    def can_earn_level(self, skill: str, level: int) -> StardewRule:
        if level <= 0:
            return True_()

        tool_level = min(4, (level - 1) // 2)
        tool_material = ToolMaterial.tiers[tool_level]

        previous_level_rule = self.logic.skill.has_previous_level(skill, level)

        if skill == Skill.fishing:
            xp_rule = self.logic.tool.has_fishing_rod(max(tool_level, 3))
        elif skill == Skill.farming:
            xp_rule = self.can_get_farming_xp & self.logic.tool.has_tool(Tool.hoe, tool_material) & self.logic.tool.can_water(tool_level)
        elif skill == Skill.foraging:
            xp_rule = (self.can_get_foraging_xp & self.logic.tool.has_tool(Tool.axe, tool_material)) | \
                      self.logic.magic.can_use_clear_debris_instead_of_tool_level(tool_level)
        elif skill == Skill.mining:
            xp_rule = self.logic.tool.has_tool(Tool.pickaxe, tool_material) | \
                      self.logic.magic.can_use_clear_debris_instead_of_tool_level(tool_level)
            xp_rule = xp_rule & self.logic.region.can_reach(Region.mines_floor_5)
        elif skill == Skill.combat:
            combat_tier = Performance.tiers[tool_level]
            xp_rule = self.logic.combat.can_fight_at_level(combat_tier)
            xp_rule = xp_rule & self.logic.region.can_reach(Region.mines_floor_5)
        elif skill in all_mod_skills:
            # Ideal solution would be to add a logic registry, but I'm too lazy.
            return previous_level_rule & self.logic.mod.skill.can_earn_mod_skill_level(skill, level)
        else:
            raise Exception(f"Unknown skill: {skill}")

        return previous_level_rule & xp_rule

    # Should be cached
    def has_level(self, skill: str, level: int) -> StardewRule:
        assert level >= 0, f"There is no level before level 0."
        if level == 0:
            return true_

        if self.content.features.skill_progression.is_progressive:
            return self.logic.received(f"{skill} Level", level)

        return self.logic.skill.can_earn_level(skill, level)

    def has_previous_level(self, skill: str, level: int) -> StardewRule:
        assert level > 0, f"There is no level before level 0."
        if level == 1:
            return true_

        if self.content.features.skill_progression.is_progressive:
            return self.logic.received(f"{skill} Level", level - 1)

        months = max(1, level - 1)
        return self.logic.time.has_lived_months(months)

    @cache_self1
    def has_farming_level(self, level: int) -> StardewRule:
        return self.logic.skill.has_level(Skill.farming, level)

    # Should be cached
    def has_total_level(self, level: int, allow_modded_skills: bool = False) -> StardewRule:
        if level <= 0:
            return True_()

        if self.content.features.skill_progression.is_progressive:
            skills_items = vanilla_skill_items
            if allow_modded_skills:
                skills_items += get_mod_skill_levels(self.options.mods)
            return self.logic.received_n(*skills_items, count=level)

        months_with_4_skills = max(1, (level // 4) - 1)
        months_with_5_skills = max(1, (level // 5) - 1)
        rule_with_fishing = self.logic.time.has_lived_months(months_with_5_skills) & self.logic.skill.can_get_fishing_xp
        if level > 40:
            return rule_with_fishing
        return self.logic.time.has_lived_months(months_with_4_skills) | rule_with_fishing

    def has_any_skills_maxed(self, included_modded_skills: bool = True) -> StardewRule:
        skills = self.content.skills.keys() if included_modded_skills else sorted(all_vanilla_skills)
        return self.logic.or_(*(self.logic.skill.has_level(skill, 10) for skill in skills))

    @cached_property
    def can_get_farming_xp(self) -> StardewRule:
        sources = self.content.find_sources_of_type(HarvestCropSource)
        crop_rules = []
        for crop_source in sources:
            crop_rules.append(self.logic.harvesting.can_harvest_crop_from(crop_source))
        return self.logic.or_(*crop_rules)

    @cached_property
    def can_get_foraging_xp(self) -> StardewRule:
        tool_rule = self.logic.tool.has_tool(Tool.axe)
        tree_rule = self.logic.region.can_reach(Region.forest) & self.logic.season.has_any_not_winter()
        stump_rule = self.logic.region.can_reach(Region.secret_woods) & self.logic.tool.has_tool(Tool.axe, ToolMaterial.copper)
        return tool_rule & (tree_rule | stump_rule)

    @cached_property
    def can_get_mining_xp(self) -> StardewRule:
        tool_rule = self.logic.tool.has_tool(Tool.pickaxe)
        stone_rule = self.logic.region.can_reach_any((Region.mines_floor_5, Region.quarry, Region.skull_cavern_25, Region.volcano_floor_5))
        return tool_rule & stone_rule

    @cached_property
    def can_get_combat_xp(self) -> StardewRule:
        tool_rule = self.logic.combat.has_any_weapon()
        enemy_rule = self.logic.region.can_reach_any((Region.mines_floor_5, Region.skull_cavern_25, Region.volcano_floor_5))
        return tool_rule & enemy_rule

    @cached_property
    def can_get_fishing_xp(self) -> StardewRule:
        if self.content.features.skill_progression.is_progressive:
            return self.logic.skill.can_fish() | self.logic.skill.can_crab_pot

        return self.logic.skill.can_fish()

    # Should be cached
    def can_fish(self, regions: Union[str, Tuple[str, ...]] = None, difficulty: int = 0) -> StardewRule:
        if isinstance(regions, str):
            regions = regions,

        if regions is None or len(regions) == 0:
            regions = fishing_regions

        skill_required = min(10, max(0, int((difficulty / 10) - 1)))
        if difficulty <= 40:
            skill_required = 0

        skill_rule = self.logic.skill.has_level(Skill.fishing, skill_required)
        region_rule = self.logic.region.can_reach_any(regions)
        # Training rod only works with fish < 50. Fiberglass does not help you to catch higher difficulty fish, so it's skipped in logic.
        number_fishing_rod_required = 1 if difficulty < 50 else (2 if difficulty < 80 else 4)
        return self.logic.tool.has_fishing_rod(number_fishing_rod_required) & skill_rule & region_rule

    @cache_self1
    def can_crab_pot_at(self, region: str) -> StardewRule:
        return self.logic.skill.can_crab_pot & self.logic.region.can_reach(region)

    @cached_property
    def can_crab_pot(self) -> StardewRule:
        crab_pot_rule = self.logic.has(Fishing.bait)

        # We can't use the same rule if skills are vanilla, because fishing levels are required to crab pot, which is required to get fishing levels...
        if self.content.features.skill_progression.is_progressive:
            crab_pot_rule = crab_pot_rule & self.logic.has(Machine.crab_pot)
        else:
            crab_pot_rule = crab_pot_rule & self.logic.skill.can_get_fishing_xp

        water_region_rules = self.logic.region.can_reach_any(fishing_regions)
        return crab_pot_rule & water_region_rules

    def can_forage_quality(self, quality: str) -> StardewRule:
        if quality == ForageQuality.basic:
            return True_()
        if quality == ForageQuality.silver:
            return self.has_level(Skill.foraging, 5)
        if quality == ForageQuality.gold:
            return self.has_level(Skill.foraging, 9)
        return False_()

    def can_earn_mastery(self, skill: str) -> StardewRule:
        # Checking for level 11, so it includes having level 10 and being able to earn xp.
        return self.logic.skill.can_earn_level(skill, 11) & self.logic.region.can_reach(Region.mastery_cave)

    def has_mastery(self, skill: str) -> StardewRule:
        if self.content.features.skill_progression.are_masteries_shuffled:
            return self.logic.received(f"{skill} Mastery")

        return self.logic.skill.can_earn_mastery(skill)

    @cached_property
    def can_enter_mastery_cave(self) -> StardewRule:
        if self.content.features.skill_progression.are_masteries_shuffled:
            return self.logic.received(Wallet.mastery_of_the_five_ways)

        return self.has_any_skills_maxed(included_modded_skills=False)
