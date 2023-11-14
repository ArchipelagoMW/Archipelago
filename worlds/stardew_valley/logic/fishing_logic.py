from .cached_logic import cache_rule, CachedLogic, CachedRules, profile_rule
from .received_logic import ReceivedLogic
from .region_logic import RegionLogic
from .season_logic import SeasonLogic
from .skill_logic import SkillLogic
from .tool_logic import ToolLogic
from ..options import ExcludeGingerIsland
from ..data import FishItem
from ..data.fish_data import legendary_fish
from ..options import SpecialOrderLocations
from ..stardew_rule import StardewRule, True_, False_, And
from ..strings.fish_names import SVEFish
from ..strings.region_names import Region
from ..strings.skill_names import Skill


class FishingLogic(CachedLogic):
    exclude_ginger_island: ExcludeGingerIsland
    special_order_locations: SpecialOrderLocations
    received: ReceivedLogic
    region: RegionLogic
    season: SeasonLogic
    tool: ToolLogic
    skill: SkillLogic

    def __init__(self, player: int, cached_rules: CachedRules, exclude_ginger_island: ExcludeGingerIsland, special_order_locations: SpecialOrderLocations,
                 received: ReceivedLogic, region: RegionLogic, season: SeasonLogic, tool: ToolLogic, skill: SkillLogic):
        super().__init__(player, cached_rules)
        self.exclude_ginger_island = exclude_ginger_island
        self.special_order_locations = special_order_locations
        self.received = received
        self.region = region
        self.season = season
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

    @cache_rule
    def can_catch_fish(self, fish: FishItem) -> StardewRule:
        quest_rule = True_()
        if fish.extended_family:
            quest_rule = self.can_start_extended_family_quest()
        region_rule = self.region.can_reach_any(fish.locations)
        season_rule = self.season.has_any(fish.seasons)
        if fish.difficulty == -1:
            difficulty_rule = self.skill.can_crab_pot()
        else:
            difficulty_rule = self.skill.can_fish([], 120 if fish.legendary else fish.difficulty)
        if fish.name == SVEFish.kittyfish:
            item_rule = self.received("Kittyfish Spell")
        else:
            item_rule = True_()
        return quest_rule & region_rule & season_rule & difficulty_rule & item_rule

    def can_start_extended_family_quest(self) -> StardewRule:
        if self.exclude_ginger_island == ExcludeGingerIsland.option_true:
            return False_()
        if self.special_order_locations != SpecialOrderLocations.option_board_qi:
            return False_()
        return self.region.can_reach(Region.qi_walnut_room) & And([self.can_catch_fish(fish) for fish in legendary_fish])
