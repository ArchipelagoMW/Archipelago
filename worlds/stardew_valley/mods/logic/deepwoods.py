from ...strings.building_names import ModBuilding
from ...strings.craftable_names import Craftable
from ...strings.performance_names import Performance
from ...strings.skill_names import Skill
from ...strings.tool_names import Tool, ToolMaterial
from ...strings.ap_names.transport_names import ModTransportation
from ...stardew_rule import StardewRule, True_, And
from ... import options


def can_reach_woods_depth(self, depth: int) -> StardewRule:
    tier = int(depth / 25) + 1
    rules = []
    if depth > 10:
        rules.append(self.has(Craftable.bomb) | self.has_tool(Tool.axe, ToolMaterial.iridium))
    if depth > 30:
        rules.append(self.received(ModTransportation.woods_obelisk))
    if depth > 50:
        rules.append(self.can_do_combat_at_level(Performance.great) & self.can_cook())
    if self.options[options.SkillProgression] == options.SkillProgression.option_progressive:
        combat_tier = min(10, max(0, tier + 5))
        rules.append(self.has_skill_level(Skill.combat, combat_tier))
    return And(rules)


def has_woods_rune_to_depth(self, floor: int) -> StardewRule:
    if (self.options[options.TheMinesElevatorsProgression] ==
            options.TheMinesElevatorsProgression.option_progressive or
            self.options[options.TheMinesElevatorsProgression] ==
            options.TheMinesElevatorsProgression.option_progressive_from_previous_floor):
        return self.received("Progressive Wood Obelisk Sigils", count=int(floor / 10))
    return True_()


def can_chop_to_depth(self, floor: int) -> StardewRule:
    previous_elevator = max(floor - 10, 0)
    previous_previous_elevator = max(floor - 20, 0)
    return ((has_woods_rune_to_depth(self, previous_elevator) &
             can_reach_woods_depth(self, previous_elevator)) |
            (has_woods_rune_to_depth(self, previous_previous_elevator) &
             can_reach_woods_depth(self, previous_previous_elevator)))
