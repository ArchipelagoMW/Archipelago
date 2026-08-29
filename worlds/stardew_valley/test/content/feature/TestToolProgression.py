import unittest

from ....content import choose_tool_progression
from ....options import ToolProgression, SkillProgression, StartWithout
from ....strings.tool_names import Tool


class TestToolDistribution(unittest.TestCase):

    def test_given_vanilla_tool_progression_when_create_feature_then_only_one_scythe_is_randomized(self):
        tool_progression = ToolProgression(ToolProgression.option_vanilla)
        skill_progression = SkillProgression.from_text("random")
        start_without = StartWithout(StartWithout.preset_none)

        feature = choose_tool_progression(tool_progression, skill_progression, start_without)

        self.assertEqual(feature.tool_distribution, {
            Tool.scythe: 1,
        })

    def test_given_progressive_tool_when_create_feature_then_all_tool_upgrades_are_randomized(self):
        tool_progression = ToolProgression(ToolProgression.option_progressive)
        skill_progression = SkillProgression(SkillProgression.option_progressive)
        start_without = StartWithout(StartWithout.preset_none)

        feature = choose_tool_progression(tool_progression, skill_progression, start_without)

        self.assertEqual(feature.tool_distribution, {
            Tool.scythe: 1,
            Tool.pickaxe: 4,
            Tool.axe: 4,
            Tool.hoe: 4,
            Tool.watering_can: 4,
            Tool.trash_can: 4,
            Tool.pan: 4,
            Tool.fishing_rod: 4,
        })

    def test_given_progressive_tool_and_skill_masteries_when_create_feature_then_additional_scythe_and_fishing_rod_are_randomized(self):
        tool_progression = ToolProgression(ToolProgression.option_progressive)
        skill_progression = SkillProgression(SkillProgression.option_progressive_with_masteries)
        start_without = StartWithout(StartWithout.preset_none)

        feature = choose_tool_progression(tool_progression, skill_progression, start_without)

        self.assertEqual(feature.tool_distribution, {
            Tool.scythe: 2,
            Tool.pickaxe: 4,
            Tool.axe: 4,
            Tool.hoe: 4,
            Tool.watering_can: 4,
            Tool.trash_can: 4,
            Tool.pan: 4,
            Tool.fishing_rod: 5,
        })
