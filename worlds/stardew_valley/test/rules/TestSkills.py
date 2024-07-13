from ... import HasProgressionPercent
from ...options import ToolProgression, SkillProgression, Mods
from ...strings.skill_names import all_skills, all_vanilla_skills
from ...test import SVTestBase, get_minsanity_options


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
                location = self.multiworld.get_location(location_name, self.player)

                with self.subTest(location_name):
                    if level > 1:
                        self.assert_reach_location_false(location, self.multiworld.state)
                        self.collect(f"{skill} Level")

                    self.assert_reach_location_true(location, self.multiworld.state)

            self.reset_collection()


class TestMasteryRequireSkillBeingMaxed(SVTestBase):
    #  Using minsanity so collecting everything is faster
    options = get_minsanity_options() | {
        SkillProgression.internal_name: SkillProgression.option_progressive_with_masteries,
        Mods.internal_name: frozenset(Mods.valid_keys),
    }

    def test_given_one_level_missing_when_can_earn_mastery_then_cannot(self):
        for skill in all_vanilla_skills:
            with self.subTest(skill):
                self.collect_everything()
                self.remove_one_by_name(f"{skill} Level")

                location = self.multiworld.get_location(f"{skill} Mastery", self.player)
                self.assert_reach_location_false(location, self.multiworld.state)

                self.reset_collection()

    def test_given_all_levels_when_can_earn_mastery_then_can(self):
        self.collect_everything()

        for skill in all_vanilla_skills:
            with self.subTest(skill):
                location = self.multiworld.get_location(f"{skill} Mastery", self.player)
                self.assert_reach_location_true(location, self.multiworld.state)

        self.reset_collection()
