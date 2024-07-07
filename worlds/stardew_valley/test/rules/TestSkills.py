from ... import HasProgressionPercent
from ...options import ToolProgression, SkillProgression, Mods
from ...strings.skill_names import all_skills
from ...test import SVTestBase


class TestVanillaSkillLogicSimplification(SVTestBase):
    options = {
        SkillProgression.internal_name: SkillProgression.option_vanilla,
        ToolProgression.internal_name: ToolProgression.option_progressive,
    }

    def test_skill_logic_has_level_only_uses_one_has_progression_percent(self):
        rule = self.multiworld.worlds[1].logic.skill.has_level("Farming", 8)
        self.assertEqual(1, sum(1 for i in rule.current_rules if type(i) == HasProgressionPercent))


class TestAllSkillsRequirePrevious(SVTestBase):
    options = {
        SkillProgression.internal_name: SkillProgression.option_progressive_with_masteries,
        Mods.internal_name: frozenset(Mods.valid_keys),
    }

    def test_all_skill_levels_require_previous_level(self):
        for skill in all_skills:
            self.collect_everything()
            self.remove_by_name(f"{skill} Level")
            for level in range(1, 11):
                location_name = f"Level {level} {skill}"
                with self.subTest(location_name):
                    can_reach = self.can_reach_location(location_name)
                    if level > 1:
                        self.assertFalse(can_reach)
                        self.collect(f"{skill} Level")
                        can_reach = self.can_reach_location(location_name)
                    self.assertTrue(can_reach)
            self.multiworld.state = self.original_state.copy()



