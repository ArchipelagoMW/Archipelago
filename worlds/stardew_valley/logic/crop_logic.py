from typing import Union, Iterable

from .has_logic import HasLogic
from .region_logic import RegionLogic
from .season_logic import SeasonLogic
from .skill_logic import SkillLogic
from .tool_logic import ToolLogic
from ..data import CropItem
from ..stardew_rule import StardewRule, True_
from ..strings.fertilizer_names import Fertilizer
from ..strings.region_names import Region
from ..strings.tool_names import Tool


class CropLogic:
    player: int
    has: HasLogic
    region: RegionLogic
    season: SeasonLogic
    skill: SkillLogic
    tool: ToolLogic

    def __init__(self, player: int, has: HasLogic, region: RegionLogic, season: SeasonLogic, skill: SkillLogic, tool: ToolLogic):
        self.player = player
        self.has = has
        self.region = region
        self.season = season
        self.skill = skill
        self.tool = tool

    def can_grow(self, crop: CropItem) -> StardewRule:
        season_rule = self.season.has_any(crop.farm_growth_seasons)
        seed_rule = self.has(crop.seed.name)
        farm_rule = self.region.can_reach(Region.farm) & season_rule
        tool_rule = self.tool.has_tool(Tool.hoe) & self.tool.has_tool(Tool.watering_can)
        region_rule = farm_rule | self.region.can_reach(Region.greenhouse) | self.region.can_reach(Region.island_west)
        return seed_rule & region_rule & tool_rule

    def can_plant_and_grow_item(self, seasons: Union[str, Iterable[str]]) -> StardewRule:
        if isinstance(seasons, str):
            seasons = [seasons]
        season_rule = self.season.has_any(seasons) | self.region.can_reach(Region.greenhouse) | self.has_island_farm()
        farm_rule = self.region.can_reach(Region.farm) | self.region.can_reach(
            Region.greenhouse) | self.has_island_farm()
        return season_rule & farm_rule

    def has_island_farm(self) -> StardewRule:
        return self.region.can_reach(Region.island_south)

    def has_fertilizer(self, tier: int) -> StardewRule:
        if tier <= 0:
            return True_()
        if tier == 1:
            return self.has(Fertilizer.basic)
        if tier == 2:
            return self.has(Fertilizer.quality)
        if tier >= 3:
            return self.has(Fertilizer.deluxe)

    def can_grow_gold_quality(self, quality: int) -> StardewRule:
        if quality <= 0:
            return True_()
        if quality == 1:
            return self.skill.has_farming_level(5) | (self.has_fertilizer(1) & self.skill.has_farming_level(2)) | (
                    self.has_fertilizer(2) & self.skill.has_farming_level(1)) | self.has_fertilizer(3)
        if quality == 2:
            return self.skill.has_farming_level(10) | (self.has_fertilizer(1) & self.skill.has_farming_level(5)) | (
                    self.has_fertilizer(2) & self.skill.has_farming_level(3)) | (
                           self.has_fertilizer(3) & self.skill.has_farming_level(2))
        if quality >= 3:
            return self.has_fertilizer(3) & self.skill.has_farming_level(4)

