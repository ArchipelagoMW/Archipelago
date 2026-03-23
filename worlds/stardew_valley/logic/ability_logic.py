from .base_logic import BaseLogicMixin, BaseLogic
from ..options import FarmType
from ..stardew_rule import StardewRule, False_, True_
from ..strings.ap_names.ap_option_names import CustomLogicOptionName
from ..strings.region_names import Region
from ..strings.skill_names import Skill, ModSkill
from ..strings.tool_names import ToolMaterial, Tool, FishingRod


class AbilityLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ability = AbilityLogic(*args, **kwargs)


class AbilityLogic(BaseLogic):

    def can_mine_stone(self) -> StardewRule:
        can_reach_any_mining_region = self.logic.region.can_reach_any(Region.mines, Region.skull_cavern, Region.volcano, Region.quarry_mine)
        if self.options.farm_type in [FarmType.option_hill_top, FarmType.option_four_corners]:
            can_reach_any_mining_region = can_reach_any_mining_region | self.logic.region.can_reach(Region.farm)
        return self.logic.tool.has_tool(Tool.pickaxe) & can_reach_any_mining_region

    def can_mine_perfectly(self) -> StardewRule:
        return self.logic.mine.can_progress_in_the_mines_from_floor(160)

    def can_mine_perfectly_in_the_skull_cavern(self) -> StardewRule:
        return (self.logic.ability.can_mine_perfectly() &
                self.logic.region.can_reach(Region.skull_cavern))

    def can_farm_perfectly(self) -> StardewRule:
        tool_rule = self.logic.tool.has_tool(Tool.hoe, ToolMaterial.iridium) & self.logic.tool.can_water(5)
        return tool_rule & self.logic.skill.has_farming_level(10)

    def can_fish_perfectly(self) -> StardewRule:
        skill_rule = self.logic.skill.has_level(Skill.fishing, 10)
        return skill_rule & self.logic.tool.has_fishing_rod(FishingRod.iridium)

    def can_chop_trees(self) -> StardewRule:
        can_reach_any_tree_region = self.logic.region.can_reach_any(Region.forest, Region.backwoods, Region.bus_stop, Region.mountain, Region.desert,
                                                                    Region.island_west, Region.island_north)
        return self.logic.tool.has_tool(Tool.axe) & can_reach_any_tree_region

    def can_chop_perfectly(self) -> StardewRule:
        magic_rule = (self.logic.magic.can_use_clear_debris_instead_of_tool_level(3)) & self.logic.mod.skill.has_mod_level(ModSkill.magic, 10)
        tool_rule = self.logic.tool.has_tool(Tool.axe, ToolMaterial.iridium)
        foraging_rule = self.logic.skill.has_level(Skill.foraging, 10)
        region_rule = self.logic.region.can_reach(Region.forest)
        return region_rule & ((tool_rule & foraging_rule) | magic_rule)

    def can_scythe_vines(self) -> StardewRule:
        can_reach_any_vine_region = self.logic.region.can_reach_any(Region.forest, Region.railroad)
        return self.logic.tool.has_scythe() & can_reach_any_vine_region & self.logic.season.has_any_not_winter()

    def can_chair_skip(self) -> StardewRule:
        if CustomLogicOptionName.chair_skips not in self.options.custom_logic:
            return False_()

        if CustomLogicOptionName.critical_free_samples in self.options.custom_logic:
            if self.options.farm_type == FarmType.option_standard or \
                    self.options.farm_type == FarmType.option_riverland or \
                    self.options.farm_type == FarmType.option_forest or \
                    self.options.farm_type == FarmType.option_beach:
                return True_()

        return self.logic.money.can_spend_at(Region.carpenter, 350)
