from typing import Union

from .base_logic import BaseLogicMixin, BaseLogic
from .cooking_logic import CookingLogicMixin
from .mine_logic import MineLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from .skill_logic import SkillLogicMixin
from .tool_logic import ToolLogicMixin
from ..mods.logic.magic_logic import MagicLogicMixin
from ..stardew_rule import StardewRule
from ..strings.region_names import Region
from ..strings.skill_names import Skill, ModSkill
from ..strings.tool_names import ToolMaterial, Tool


class AbilityLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ability = AbilityLogic(*args, **kwargs)


class AbilityLogic(BaseLogic[Union[AbilityLogicMixin, RegionLogicMixin, ReceivedLogicMixin, ToolLogicMixin, SkillLogicMixin, MineLogicMixin, MagicLogicMixin]]):
    def can_mine_perfectly(self) -> StardewRule:
        return self.logic.mine.can_progress_in_the_mines_from_floor(160)

    def can_mine_perfectly_in_the_skull_cavern(self) -> StardewRule:
        return (self.logic.ability.can_mine_perfectly() &
                self.logic.region.can_reach(Region.skull_cavern))

    def can_farm_perfectly(self) -> StardewRule:
        tool_rule = self.logic.tool.has_tool(Tool.hoe, ToolMaterial.iridium) & self.logic.tool.can_water(4)
        return tool_rule & self.logic.skill.has_farming_level(10)

    def can_fish_perfectly(self) -> StardewRule:
        skill_rule = self.logic.skill.has_level(Skill.fishing, 10)
        return skill_rule & self.logic.tool.has_fishing_rod(4)

    def can_chop_trees(self) -> StardewRule:
        return self.logic.tool.has_tool(Tool.axe) & self.logic.region.can_reach(Region.forest)

    def can_chop_perfectly(self) -> StardewRule:
        magic_rule = (self.logic.magic.can_use_clear_debris_instead_of_tool_level(3)) & self.logic.mod.skill.has_mod_level(ModSkill.magic, 10)
        tool_rule = self.logic.tool.has_tool(Tool.axe, ToolMaterial.iridium)
        foraging_rule = self.logic.skill.has_level(Skill.foraging, 10)
        region_rule = self.logic.region.can_reach(Region.forest)
        return region_rule & ((tool_rule & foraging_rule) | magic_rule)
