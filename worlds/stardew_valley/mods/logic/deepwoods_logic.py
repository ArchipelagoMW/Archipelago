from typing import Union

from ... import options
from ...logic.base_logic import BaseLogicMixin, BaseLogic
from ...logic.combat_logic import CombatLogicMixin
from ...logic.cooking_logic import CookingLogicMixin
from ...logic.has_logic import HasLogicMixin
from ...logic.received_logic import ReceivedLogicMixin
from ...logic.skill_logic import SkillLogicMixin
from ...logic.tool_logic import ToolLogicMixin
from ...mods.mod_data import ModNames
from ...options import ElevatorProgression
from ...stardew_rule import StardewRule, True_, And, true_
from ...strings.ap_names.mods.mod_items import DeepWoodsItem, SkillLevel
from ...strings.ap_names.transport_names import ModTransportation
from ...strings.craftable_names import Bomb
from ...strings.food_names import Meal
from ...strings.performance_names import Performance
from ...strings.skill_names import Skill
from ...strings.tool_names import Tool, ToolMaterial


class DeepWoodsLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deepwoods = DeepWoodsLogic(*args, **kwargs)


class DeepWoodsLogic(BaseLogic[Union[SkillLogicMixin, ReceivedLogicMixin, HasLogicMixin, CombatLogicMixin, ToolLogicMixin, SkillLogicMixin,
CookingLogicMixin]]):

    def can_reach_woods_depth(self, depth: int) -> StardewRule:
        # Assuming you can always do the 10 first floor
        if depth <= 10:
            return true_

        rules = []

        if depth > 10:
            rules.append(self.logic.has(Bomb.bomb) | self.logic.tool.has_tool(Tool.axe, ToolMaterial.iridium))
        if depth > 30:
            rules.append(self.logic.received(ModTransportation.woods_obelisk))
        if depth > 50:
            rules.append(self.logic.combat.can_fight_at_level(Performance.great) & self.logic.cooking.can_cook() &
                         self.logic.received(ModTransportation.woods_obelisk))

        tier = int(depth / 25) + 1
        if self.options.skill_progression == options.SkillProgression.option_progressive:
            combat_tier = min(10, max(0, tier + 5))
            rules.append(self.logic.skill.has_level(Skill.combat, combat_tier))

        return And(*rules)

    def has_woods_rune_to_depth(self, floor: int) -> StardewRule:
        if self.options.elevator_progression == ElevatorProgression.option_vanilla:
            return True_()
        return self.logic.received(DeepWoodsItem.obelisk_sigil, int(floor / 10))

    def can_chop_to_depth(self, floor: int) -> StardewRule:
        previous_elevator = max(floor - 10, 0)
        return (self.has_woods_rune_to_depth(previous_elevator) &
                self.can_reach_woods_depth(previous_elevator))

    def can_pull_sword(self) -> StardewRule:
        rules = [self.logic.received(DeepWoodsItem.pendant_depths) & self.logic.received(DeepWoodsItem.pendant_community) &
                 self.logic.received(DeepWoodsItem.pendant_elder),
                 self.logic.skill.has_total_level(40)]
        if ModNames.luck_skill in self.options.mods:
            rules.append(self.logic.received(SkillLevel.luck, 7))
        else:
            rules.append(
                self.logic.has(Meal.magic_rock_candy))  # You need more luck than this, but it'll push the logic down a ways; you can get the rest there.
        return And(*rules)
