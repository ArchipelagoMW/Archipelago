from ..bases import SVTestBase
from ... import HasProgressionPercent, StardewLogic
from ...options import ToolProgression, SkillProgression, Mods
from ...strings.skill_names import all_skills, all_vanilla_skills, Skill


class TestSkillProgressionVanilla(SVTestBase):
    options = {
        SkillProgression.internal_name: SkillProgression.option_vanilla,
        ToolProgression.internal_name: ToolProgression.option_progressive,
    }

    def test_skill_logic_has_level_only_uses_one_has_progression_percent(self):
        rule = self.multiworld.worlds[1].logic.skill.has_level(Skill.farming, 8)
        self.assertEqual(1, sum(1 for i in rule.current_rules if type(i) is HasProgressionPercent))

    def test_has_mastery_requires_month_equivalent_to_10_levels(self):
        logic: StardewLogic = self.multiworld.worlds[1].logic
        rule = logic.skill.has_mastery(Skill.farming)
        time_rule = logic.time.has_lived_months(10)

        self.assertIn(time_rule, rule.current_rules)


class TestSkillProgressionProgressive(SVTestBase):
    options = {
        SkillProgression.internal_name: SkillProgression.option_progressive,
        Mods.internal_name: frozenset(Mods.valid_keys),
    }

    def test_all_skill_levels_require_previous_level(self):
        for skill in all_skills:
            self.collect_everything()
            self.remove_by_name(f"{skill} Level")

            for level in range(1, 11):
                location_name = f"Level {level} {skill}"

                with self.subTest(location_name):
                    if level > 1:
                        self.assert_cannot_reach_location(location_name)
                        self.collect(f"{skill} Level")

                    self.assert_can_reach_location(location_name)

            self.reset_collection_state()

    def test_has_level_requires_exact_amount_of_levels(self):
        logic: StardewLogic = self.multiworld.worlds[1].logic
        rule = logic.skill.has_level(Skill.farming, 8)
        level_rule = logic.received("Farming Level", 8)

        self.assertEqual(level_rule, rule)

    def test_has_previous_level_requires_one_less_level_than_requested(self):
        logic: StardewLogic = self.multiworld.worlds[1].logic
        rule = logic.skill.has_previous_level(Skill.farming, 8)
        level_rule = logic.received("Farming Level", 7)

        self.assertEqual(level_rule, rule)

    def test_has_mastery_requires_10_levels(self):
        logic: StardewLogic = self.multiworld.worlds[1].logic
        rule = logic.skill.has_mastery(Skill.farming)
        level_rule = logic.received("Farming Level", 10)

        self.assertIn(level_rule, rule.current_rules)


class TestSkillProgressionProgressiveWithMasteryWithoutMods(SVTestBase):
    options = {
        SkillProgression.internal_name: SkillProgression.option_progressive_with_masteries,
        ToolProgression.internal_name: ToolProgression.option_progressive,
        Mods.internal_name: frozenset(),
    }

    def test_has_mastery_requires_the_item(self):
        logic: StardewLogic = self.multiworld.worlds[1].logic
        rule = logic.skill.has_mastery(Skill.farming)
        received_mastery = logic.received("Farming Mastery")

        self.assertEqual(received_mastery, rule)

    def test_given_all_levels_when_can_earn_mastery_then_can_earn_mastery(self):
        self.collect_everything()

        for skill in all_vanilla_skills:
            with self.subTest(skill):
                self.assert_can_reach_location(f"{skill} Mastery")

        self.reset_collection_state()

    def test_given_one_level_missing_when_can_earn_mastery_then_cannot_earn_mastery(self):
        for skill in all_vanilla_skills:
            with self.subTest(skill):
                self.collect_everything()
                self.remove_one_by_name(f"{skill} Level")

                self.assert_cannot_reach_location(f"{skill} Mastery")

                self.reset_collection_state()

    def test_given_one_tool_missing_when_can_earn_mastery_then_cannot_earn_mastery(self):
        self.collect_everything()

        self.remove_one_by_name(f"Progressive Pickaxe")
        self.assert_cannot_reach_location("Mining Mastery")

        self.reset_collection_state()
