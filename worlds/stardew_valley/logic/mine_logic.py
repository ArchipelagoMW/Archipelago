from typing import Union

from Utils import cache_self1
from .base_logic import BaseLogicMixin, BaseLogic
from .combat_logic import CombatLogicMixin
from .cooking_logic import CookingLogicMixin
from .has_logic import HasLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from .skill_logic import SkillLogicMixin
from .tool_logic import ToolLogicMixin
from .. import options
from ..options import ToolProgression
from ..stardew_rule import StardewRule, True_
from ..strings.performance_names import Performance
from ..strings.region_names import Region
from ..strings.skill_names import Skill
from ..strings.tool_names import Tool, ToolMaterial


class MineLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mine = MineLogic(*args, **kwargs)


class MineLogic(BaseLogic[Union[HasLogicMixin, MineLogicMixin, RegionLogicMixin, ReceivedLogicMixin, CombatLogicMixin, ToolLogicMixin,
SkillLogicMixin, CookingLogicMixin]]):
    # Regions
    def can_mine_in_the_mines_floor_1_40(self) -> StardewRule:
        return self.logic.region.can_reach(Region.mines_floor_5)

    def can_mine_in_the_mines_floor_41_80(self) -> StardewRule:
        return self.logic.region.can_reach(Region.mines_floor_45)

    def can_mine_in_the_mines_floor_81_120(self) -> StardewRule:
        return self.logic.region.can_reach(Region.mines_floor_85)

    def can_mine_in_the_skull_cavern(self) -> StardewRule:
        return (self.logic.mine.can_progress_in_the_mines_from_floor(120) &
                self.logic.region.can_reach(Region.skull_cavern))

    @cache_self1
    def get_weapon_rule_for_floor_tier(self, tier: int):
        if tier >= 4:
            return self.logic.combat.can_fight_at_level(Performance.galaxy)
        if tier >= 3:
            return self.logic.combat.can_fight_at_level(Performance.great)
        if tier >= 2:
            return self.logic.combat.can_fight_at_level(Performance.good)
        if tier >= 1:
            return self.logic.combat.can_fight_at_level(Performance.decent)
        return self.logic.combat.can_fight_at_level(Performance.basic)

    @cache_self1
    def can_progress_in_the_mines_from_floor(self, floor: int) -> StardewRule:
        tier = floor // 40
        rules = []
        weapon_rule = self.logic.mine.get_weapon_rule_for_floor_tier(tier)
        rules.append(weapon_rule)

        if self.options.tool_progression & ToolProgression.option_progressive:
            rules.append(self.logic.tool.has_tool(Tool.pickaxe, ToolMaterial.tiers[tier]))

        # No alternative for vanilla because we assume that you will grind the levels in the mines.
        if self.content.features.skill_progression.is_progressive:
            skill_level = min(10, max(0, tier * 2))
            rules.append(self.logic.skill.has_level(Skill.combat, skill_level))
            rules.append(self.logic.skill.has_level(Skill.mining, skill_level))

        if tier >= 4:
            rules.append(self.logic.cooking.can_cook())

        return self.logic.and_(*rules)

    @cache_self1
    def has_mine_elevator_to_floor(self, floor: int) -> StardewRule:
        if floor < 0:
            floor = 0
        if self.options.elevator_progression != options.ElevatorProgression.option_vanilla:
            return self.logic.received("Progressive Mine Elevator", floor // 5)
        return True_()

    @cache_self1
    def can_progress_in_the_skull_cavern_from_floor(self, floor: int) -> StardewRule:
        tier = floor // 50
        rules = []
        weapon_rule = self.logic.combat.has_great_weapon
        rules.append(weapon_rule)

        if self.options.tool_progression & ToolProgression.option_progressive:
            rules.append(self.logic.received("Progressive Pickaxe", min(4, max(0, tier + 2))))

        # No alternative for vanilla because we assume that you will grind the levels in the mines.
        if self.content.features.skill_progression.is_progressive:
            skill_level = min(10, max(0, tier * 2 + 6))
            rules.extend((self.logic.skill.has_level(Skill.combat, skill_level),
                          self.logic.skill.has_level(Skill.mining, skill_level)))

        return self.logic.and_(*rules)
