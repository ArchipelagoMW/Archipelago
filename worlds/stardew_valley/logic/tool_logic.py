from typing import Union, Iterable, Tuple

from Utils import cache_self1
from .base_logic import BaseLogicMixin, BaseLogic
from ..stardew_rule import StardewRule, True_, False_
from ..strings.ap_names.skill_level_names import ModSkillLevel
from ..strings.region_names import Region, LogicRegion
from ..strings.spells import MagicSpell
from ..strings.tool_names import ToolMaterial, Tool, APTool

fishing_rod_prices = {
    3: 1800,
    4: 7500,
}

tool_materials = {
    ToolMaterial.copper: 1,
    ToolMaterial.iron: 2,
    ToolMaterial.gold: 3,
    ToolMaterial.iridium: 4
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

    def has_all_tools(self, tools: Iterable[Tuple[str, str]]):
        return self.logic.and_(*(self.logic.tool.has_tool(tool, material) for tool, material in tools))

    # Should be cached
    def has_tool(self, tool: str, material: str = ToolMaterial.basic) -> StardewRule:
        if tool == Tool.fishing_rod:
            return self.logic.tool.has_fishing_rod(tool_materials[material])

        if tool == Tool.pan and material == ToolMaterial.basic:
            material = ToolMaterial.copper  # The first Pan is the copper one, so the basic one does not exist

        if material == ToolMaterial.basic or tool == Tool.scythe:
            return True_()

        if self.content.features.tool_progression.is_progressive:
            return self.logic.received(f"Progressive {tool}", tool_materials[material])

        can_upgrade_rule = self.logic.tool._can_purchase_upgrade(material)
        if tool == Tool.pan:
            has_base_pan = self.logic.received("Glittering Boulder Removed") & self.logic.region.can_reach(Region.mountain)
            if material == ToolMaterial.copper:
                return has_base_pan
            return has_base_pan & can_upgrade_rule

        return can_upgrade_rule

    @cache_self1
    def can_mine_using(self, material: str) -> StardewRule:
        if material == ToolMaterial.basic:
            return self.logic.true_

        if self.content.features.tool_progression.is_progressive:
            return self.logic.received(APTool.pickaxe, tool_materials[material])
        else:
            return self.logic.tool._can_purchase_upgrade(material)

    @cache_self1
    def _can_purchase_upgrade(self, material: str) -> StardewRule:
        return self.logic.region.can_reach(LogicRegion.blacksmith_upgrade(material))

    def can_use_tool_at(self, tool: str, material: str, region: str) -> StardewRule:
        return self.has_tool(tool, material) & self.logic.region.can_reach(region)

    @cache_self1
    def has_fishing_rod(self, level: int) -> StardewRule:
        assert 1 <= level <= 4, "Fishing rod 0 isn't real, it can't hurt you. Training is 1, Bamboo is 2, Fiberglass is 3 and Iridium is 4."

        if self.content.features.tool_progression.is_progressive:
            return self.logic.received(APTool.fishing_rod, level)

        if level <= 2:
            # We assume you always have access to the Bamboo pole, because mod side there is a builtin way to get it back.
            return self.logic.region.can_reach(Region.beach)

        return self.logic.money.can_spend_at(Region.fish_shop, fishing_rod_prices[level])

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
    def can_water(self, level: int) -> StardewRule:
        tool_rule = self.logic.tool.has_tool(Tool.watering_can, ToolMaterial.tiers[level])
        spell_rule = self.logic.received(MagicSpell.water) & self.logic.magic.can_use_altar() & self.logic.received(ModSkillLevel.magic_level, level)
        return tool_rule | spell_rule
