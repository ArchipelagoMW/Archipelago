from .region_logic import RegionLogic
from .skill_logic import SkillLogic
from .tool_logic import ToolLogic
from ..stardew_rule import StardewRule
from ..strings.region_names import Region
from ..strings.skill_names import Skill


class FishingLogic:
    player: int
    region: RegionLogic
    tool: ToolLogic
    skill: SkillLogic

    def __init__(self, player: int, region: RegionLogic, tool: ToolLogic, skill: SkillLogic):
        self.player = player
        self.region = region
        self.tool = tool
        self.skill = skill

    def can_fish_in_freshwater(self) -> StardewRule:
        return self.skill.can_fish() & self.region.can_reach_any([Region.forest, Region.town, Region.mountain])

    def has_max_fishing(self) -> StardewRule:
        skill_rule = self.skill.has_level(Skill.fishing, 10)
        return self.tool.has_fishing_rod(4) & skill_rule

    def can_fish_chests(self) -> StardewRule:
        skill_rule = self.skill.has_level(Skill.fishing, 6)
        return self.tool.has_fishing_rod(4) & skill_rule

    def can_fish_at(self, region: str) -> StardewRule:
        return self.skill.can_fish() & self.region.can_reach(region)
