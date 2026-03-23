from typing import Union, Iterable

from Utils import cache_self1
from .base_logic import BaseLogicMixin, BaseLogic
from ..stardew_rule import StardewRule, False_
from ..strings.ap_names.skill_level_names import ModSkillLevel
from ..strings.region_names import Region, LogicRegion
from ..strings.skill_names import Skill
from ..strings.spells import MagicSpell
from ..strings.tool_names import ToolMaterial, Tool, FishingRod

fishing_rod_prices = {
    FishingRod.training: 25,
    FishingRod.bamboo: 500,
    FishingRod.fiberglass: 1800,
    FishingRod.iridium: 7500,
    FishingRod.advanced_iridium: 25000,
}

tool_materials = {
    ToolMaterial.basic: 1,
    ToolMaterial.copper: 2,
    ToolMaterial.iron: 3,
    ToolMaterial.gold: 4,
    ToolMaterial.iridium: 5
}

tool_upgrade_prices = {
    ToolMaterial.copper: 2000,
    ToolMaterial.iron: 5000,
    ToolMaterial.gold: 10000,
    ToolMaterial.iridium: 25000
}


class ToolLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tool = ToolLogic(*args, **kwargs)


class ToolLogic(BaseLogic):

    def has_all_tools(self, tools: Iterable[tuple[str, str]]):
        return self.logic.and_(*(self.logic.tool.has_tool(tool, material) for tool, material in tools))

    def has_tool_generic(self, tool: str, material: str) -> StardewRule:
        """I hope you know what you're doing..."""
        if tool == Tool.fishing_rod:
            return self.has_fishing_rod(material)
        if tool == Tool.scythe:
            return self.has_scythe(material)
        if tool == Tool.pan:
            return self.has_pan(material)
        return self.has_tool(tool, material)

    # Should be cached
    def has_tool(self, tool: str, material: str = ToolMaterial.basic) -> StardewRule:
        assert tool != Tool.fishing_rod, "Use has_fishing_rod instead of has_tool for fishing rods."
        assert tool != Tool.scythe, "Use has_scythe instead of has_tool for scythes."
        assert tool != Tool.pan, "Use has_pan instead of has_tool for pans."

        if self.content.features.tool_progression.is_progressive:
            return self.logic.tool._has_progressive_tool(tool, tool_materials[material])

        if material == ToolMaterial.basic:
            return self.logic.true_

        return self.logic.tool._can_purchase_upgrade(material)

    @cache_self1
    def can_mine_using(self, material: str) -> StardewRule:
        return self.logic.tool.has_tool(Tool.pickaxe, material)

    @cache_self1
    def _can_purchase_upgrade(self, material: str) -> StardewRule:
        return self.logic.region.can_reach(LogicRegion.blacksmith_upgrade(material))

    def can_use_tool_at(self, tool: str, material: str, region: str) -> StardewRule:
        return self.has_tool(tool, material) & self.logic.region.can_reach(region)

    @cache_self1
    def has_pan(self, material: str = ToolMaterial.copper) -> StardewRule:
        assert material != ToolMaterial.basic, "The basic pan does not exist."

        if self.content.features.tool_progression.is_progressive:
            # The is no basic tier for the pan, so copper is level 1 instead of 2
            level = tool_materials[material] - 1
            return self.logic.tool._has_progressive_tool(Tool.pan, level)

        pan_cutscene_rule = self.logic.received("Glittering Boulder Removed") & self.logic.region.can_reach(Region.mountain)
        if material == ToolMaterial.copper:
            return pan_cutscene_rule

        return pan_cutscene_rule & self.logic.tool._can_purchase_upgrade(material)

    @cache_self1
    def has_scythe(self, material: str = ToolMaterial.basic) -> StardewRule:
        if self.content.features.tool_progression.is_progressive:
            if material == ToolMaterial.basic:
                return self._has_progressive_tool(Tool.scythe, 1)
            if material == ToolMaterial.gold:
                return self._has_progressive_tool(Tool.scythe, 2)
            if material == ToolMaterial.iridium:
                return self._has_progressive_tool(Tool.scythe, 3)
            raise ValueError(f"Scythe material [{material}] is not valid.")

        if material == ToolMaterial.basic:
            return self.logic.true_
        if material == ToolMaterial.gold:
            return self.logic.tool._has_progressive_tool(Tool.scythe, 1)
        if material == ToolMaterial.iridium:
            return self.logic.skill.has_mastery(Skill.farming)

        return self.has_tool(Tool.scythe, material)

    @cache_self1
    def has_fishing_rod(self, material: str = FishingRod.training) -> StardewRule:
        level = FishingRod.material_to_tier[material]
        tool_progression = self.content.features.tool_progression

        rebuy_rule = self.logic.money.can_spend_at(Region.fish_shop, fishing_rod_prices[material])

        if tool_progression.is_progressive:
            return self.logic.tool._has_progressive_tool(Tool.fishing_rod, level) & rebuy_rule

        if material == FishingRod.bamboo:
            return self.logic.region.can_reach(Region.beach) & rebuy_rule
        if material == FishingRod.fiberglass:
            return self.logic.skill.has_level(Skill.fishing, 2) & rebuy_rule
        if material == FishingRod.iridium:
            return self.logic.skill.has_level(Skill.fishing, 6) & rebuy_rule
        if material == FishingRod.advanced_iridium:
            return self.logic.skill.has_mastery(Skill.fishing) & rebuy_rule
        return rebuy_rule

    def _has_progressive_tool(self, tool: str, amount: int) -> StardewRule:
        tool_progression = self.content.features.tool_progression
        amount -= tool_progression.starting_tools[tool]

        # Meaning you started with the tool
        if amount <= 0:
            return self.logic.true_

        return self.logic.received(tool_progression.to_progressive_item_name(tool), amount)

    @cache_self1
    def _can_purchase_upgrade(self, material: str) -> StardewRule:
        return self.logic.region.can_reach(LogicRegion.blacksmith_upgrade(material))

    # Should be cached
    def can_forage(self, season: Union[str, Iterable[str]], region: str = Region.forest, need_hoe: bool = False) -> StardewRule:
        season_rule = False_()
        if isinstance(season, str):
            season_rule = self.logic.season.has(season)
        elif isinstance(season, Iterable):
            season_rule = self.logic.season.has_any(season)
        region_rule = self.logic.region.can_reach(region)
        if need_hoe:
            return season_rule & region_rule & self.logic.tool.has_tool(Tool.hoe)
        return season_rule & region_rule

    @cache_self1
    def can_water(self, level: int = 1) -> StardewRule:
        tool_rule = self.logic.tool.has_tool(Tool.watering_can, ToolMaterial.tiers[level])
        spell_rule = self.logic.received(MagicSpell.water) & self.logic.magic.can_use_altar() & self.logic.received(ModSkillLevel.magic_level, level)
        return tool_rule | spell_rule
