from ...strings.craftable_names import Craftable
from ...strings.performance_names import Performance
from ...strings.skill_names import Skill
from ...strings.tool_names import Tool, ToolMaterial
from ...strings.ap_names.transport_names import ModTransportation
from ...stardew_rule import StardewRule, True_, And
from ... import options


def can_reach_woods_depth(vanilla_logic, depth: int) -> StardewRule:
    tier = int(depth / 25) + 1
    rules = []
    if depth > 10:
        rules.append(vanilla_logic.has(Craftable.bomb) | vanilla_logic.has_tool(Tool.axe, ToolMaterial.iridium))
    if depth > 30:
        rules.append(vanilla_logic.received(ModTransportation.woods_obelisk))
    if depth > 50:
        rules.append(vanilla_logic.can_do_combat_at_level(Performance.great) & vanilla_logic.can_cook() &
                     vanilla_logic.received(ModTransportation.woods_obelisk))
    if vanilla_logic.options.skill_progression == options.SkillProgression.option_progressive:
        combat_tier = min(10, max(0, tier + 5))
        rules.append(vanilla_logic.has_skill_level(Skill.combat, combat_tier))
    return And(rules)


def has_woods_rune_to_depth(vanilla_logic, floor: int) -> StardewRule:
    if vanilla_logic.options.elevator_progression == options.ElevatorProgression.option_vanilla:
        return True_()
    return vanilla_logic.received("Progressive Woods Obelisk Sigils", count=int(floor / 10))


def can_chop_to_depth(vanilla_logic, floor: int) -> StardewRule:
    previous_elevator = max(floor - 10, 0)
    return (has_woods_rune_to_depth(vanilla_logic, previous_elevator) &
            can_reach_woods_depth(vanilla_logic, previous_elevator))
