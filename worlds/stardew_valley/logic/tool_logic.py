from typing import Union, Iterable

from Utils import cache_self1
from .base_logic import BaseLogicMixin, BaseLogic
from .has_logic import HasLogicMixin
from .money_logic import MoneyLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from .season_logic import SeasonLogicMixin
from ..mods.logic.magic_logic import MagicLogicMixin
from ..options import ToolProgression
from ..stardew_rule import StardewRule, True_, False_
from ..strings.ap_names.skill_level_names import ModSkillLevel
from ..strings.region_names import Region
from ..strings.skill_names import ModSkill
from ..strings.spells import MagicSpell
from ..strings.tool_names import ToolMaterial, Tool

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


class ToolLogic(BaseLogic[Union[ToolLogicMixin, HasLogicMixin, ReceivedLogicMixin, RegionLogicMixin, SeasonLogicMixin, MoneyLogicMixin, MagicLogicMixin]]):
    # Should be cached
    def has_tool(self, tool: str, material: str = ToolMaterial.basic) -> StardewRule:
        if material == ToolMaterial.basic or tool == Tool.scythe:
            return True_()

        if self.options.tool_progression & ToolProgression.option_progressive:
            return self.logic.received(f"Progressive {tool}", tool_materials[material])

        return self.logic.has(f"{material} Bar") & self.logic.money.can_spend(tool_upgrade_prices[material])

    def can_use_tool_at(self, tool: str, material: str, region: str) -> StardewRule:
        return self.has_tool(tool, material) & self.logic.region.can_reach(region)

    @cache_self1
    def has_fishing_rod(self, level: int) -> StardewRule:
        if self.options.tool_progression & ToolProgression.option_progressive:
            return self.logic.received(f"Progressive {Tool.fishing_rod}", level)

        if level <= 1:
            return self.logic.region.can_reach(Region.beach)
        prices = {2: 500, 3: 1800, 4: 7500}
        level = min(level, 4)
        return self.logic.money.can_spend_at(Region.fish_shop, prices[level])

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
