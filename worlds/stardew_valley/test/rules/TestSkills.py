from ... import HasProgressionPercent
from ...options import ToolProgression, SkillProgression
from ...test import SVTestBase


class TestVanillaSkillLogicSimplification(SVTestBase):
    options = {
        SkillProgression.internal_name: SkillProgression.option_vanilla,
        ToolProgression.internal_name: ToolProgression.option_progressive,
    }

    def test_skill_logic_has_level_only_uses_one_has_progression_percent(self):
        rule = self.multiworld.worlds[1].logic.skill.has_level("Farming", 8)
        self.assertEqual(1, sum(1 for i in rule.current_rules if type(i) == HasProgressionPercent))
