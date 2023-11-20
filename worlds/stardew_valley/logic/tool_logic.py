from Utils import cache_self1
from .has_logic import HasLogicMixin
from .money_logic import MoneyLogic
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from .season_logic import SeasonLogic
from ..mods.logic.magic_logic import MagicLogic
from ..options import ToolProgression
from ..stardew_rule import StardewRule, True_
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


class ToolLogic:
    tool_option = ToolProgression
    received: ReceivedLogicMixin
    has: HasLogicMixin
    region: RegionLogicMixin
    season: SeasonLogic
    money: MoneyLogic
    magic: MagicLogic

    def __init__(self, player: int, tool_option: ToolProgression, received: ReceivedLogicMixin, has: HasLogicMixin, region: RegionLogicMixin,
                 season: SeasonLogic,
                 money: MoneyLogic):
        self.player = player
        self.tool_option = tool_option
        self.received = received
        self.has = has
        self.region = region
        self.season = season
        self.money = money

    def set_magic(self, magic: MagicLogic):
        self.magic = magic

    # Should be cached
    def has_tool(self, tool: str, material: str = ToolMaterial.basic) -> StardewRule:
        if material == ToolMaterial.basic or tool == Tool.scythe:
            return True_()

        if self.tool_option & ToolProgression.option_progressive:
            return self.received(f"Progressive {tool}", tool_materials[material])

        return self.has(f"{material} Bar") & self.money.can_spend(tool_upgrade_prices[material])

    @cache_self1
    def has_fishing_rod(self, level: int) -> StardewRule:
        if self.tool_option & ToolProgression.option_progressive:
            return self.received(f"Progressive {Tool.fishing_rod}", level)

        if level <= 1:
            return self.region.can_reach(Region.beach)
        prices = {2: 500, 3: 1800, 4: 7500}
        level = min(level, 4)
        return self.money.can_spend_at(Region.fish_shop, prices[level])

    # Should be cached
    def can_forage(self, season: str, region: str = Region.forest, need_hoe: bool = False) -> StardewRule:
        season_rule = self.season.has(season)
        region_rule = self.region.can_reach(region)
        if need_hoe:
            return season_rule & region_rule & self.has_tool(Tool.hoe)
        return season_rule & region_rule

    @cache_self1
    def can_water(self, level: int) -> StardewRule:
        tool_rule = self.has_tool(Tool.watering_can, ToolMaterial.tiers[level])
        spell_rule = self.received(MagicSpell.water) & self.magic.can_use_altar() & self.received(
            f"{ModSkill.magic} Level", level)
        return tool_rule | spell_rule
