from ...logic.base_logic import BaseLogicMixin, BaseLogic
from ...options import ElevatorProgression
from ...stardew_rule import StardewRule, True_, true_
from ...strings.ap_names.mods.mod_items import DeepWoodsItem
from ...strings.ap_names.transport_names import ModTransportation
from ...strings.craftable_names import Bomb
from ...strings.food_names import Meal
from ...strings.performance_names import Performance
from ...strings.skill_names import Skill, ModSkill
from ...strings.tool_names import Tool, ToolMaterial


class DeepWoodsLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deepwoods = DeepWoodsLogic(*args, **kwargs)


class DeepWoodsLogic(BaseLogic):

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
        if self.content.features.skill_progression.is_progressive:
            combat_level = min(10, max(0, tier + 5))
            rules.append(self.logic.skill.has_level(Skill.combat, combat_level))

        return self.logic.and_(*rules)

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
        if ModSkill.luck in self.content.skills:
            rules.append(self.logic.skill.has_level(ModSkill.luck, 7))
        else:
            # You need more luck than this, but it'll push the logic down a ways; you can get the rest there.
            rules.append(self.logic.has(Meal.magic_rock_candy))
        return self.logic.and_(*rules)
