from ..Options import WorldRequirements
from ..Names import itemName
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from . import BanjoTooieTestBase
from math import ceil


class WorldRequirementTest(BanjoTooieTestBase):
    expected_world_costs = [1, 4, 8, 14, 20, 28, 36, 45, 55]

    def test_check_world_costs(self) -> None:
        assert list(self.world.world_requirements.values()) == self.expected_world_costs

    def test_jiggies(self) -> None:
        expected_progression_jiggies = min(max(self.expected_world_costs) + 5, 90)
        expected_useful_jiggies = max(0, ceil((90 - expected_progression_jiggies - 5) / 2))

        assert sum(
            1 for item in self.multiworld.itempool
            if item.name == itemName.JIGGY and item.advancement
        ) == expected_progression_jiggies - 1  # jingaling's

        assert sum(
            1 for item in self.multiworld.itempool
            if item.name == itemName.JIGGY and item.useful
        ) == expected_useful_jiggies


class WorldRequirementMinTest(WorldRequirementTest):
    expected_world_costs = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    options = {
        "world_requirements": WorldRequirements.option_custom,
        "custom_worlds": "1,1,1,1,1,1,1,1,1"
    }


class WorldRequirementQuickTest(WorldRequirementTest):
    expected_world_costs = [1, 3, 6, 10, 15, 21, 28, 35, 44]
    options = {
        "world_requirements": WorldRequirements.option_quick
    }


class WorldRequirementNormalTest(WorldRequirementTest):
    expected_world_costs = [1, 4, 8, 14, 20, 28, 36, 45, 55]
    options = {
        "world_requirements": WorldRequirements.option_normal
    }


class WorldRequirementLongTest(WorldRequirementTest):
    expected_world_costs = [1, 8, 16, 25, 34, 43, 52, 60, 70]
    options = {
        "world_requirements": WorldRequirements.option_long
    }


class WorldRequirementMaxTest(WorldRequirementTest):
    expected_world_costs = [1, 10, 20, 30, 50, 60, 70, 80, 90]
    options = {
        "world_requirements": WorldRequirements.option_custom,
        "custom_worlds": "1,10,20,30,50,60,70,80,90"
    }


class WorldRequirementMinIntendedTest(WorldRequirementMinTest, IntendedLogic):
    options = {
        **WorldRequirementMinTest.options,
        **IntendedLogic.options
    }


class WorldRequirementMinEasyTricksTest(WorldRequirementMinTest, EasyTricksLogic):
    options = {
        **WorldRequirementMinTest.options,
        **EasyTricksLogic.options
    }


class WorldRequirementMinHardTricksTest(WorldRequirementMinTest, HardTricksLogic):
    options = {
        **WorldRequirementMinTest.options,
        **HardTricksLogic.options
    }


class WorldRequirementMinGlitchesTest(WorldRequirementMinTest, GlitchesLogic):
    options = {
        **WorldRequirementMinTest.options,
        **GlitchesLogic.options
    }


class WorldRequirementQuickIntendedTest(WorldRequirementQuickTest, IntendedLogic):
    options = {
        **WorldRequirementQuickTest.options,
        **IntendedLogic.options
    }


class WorldRequirementQuickEasyTricksTest(WorldRequirementQuickTest, EasyTricksLogic):
    options = {
        **WorldRequirementQuickTest.options,
        **EasyTricksLogic.options
    }


class WorldRequirementQuickHardTricksTest(WorldRequirementQuickTest, HardTricksLogic):
    options = {
        **WorldRequirementQuickTest.options,
        **HardTricksLogic.options
    }


class WorldRequirementQuickGlitchesTest(WorldRequirementQuickTest, GlitchesLogic):
    options = {
        **WorldRequirementQuickTest.options,
        **GlitchesLogic.options
    }


class WorldRequirementNormalIntendedTest(WorldRequirementNormalTest, IntendedLogic):
    options = {
        **WorldRequirementNormalTest.options,
        **IntendedLogic.options
    }


class WorldRequirementNormalEasyTricksTest(WorldRequirementNormalTest, EasyTricksLogic):
    options = {
        **WorldRequirementNormalTest.options,
        **EasyTricksLogic.options
    }


class WorldRequirementNormalHardTricksTest(WorldRequirementNormalTest, HardTricksLogic):
    options = {
        **WorldRequirementNormalTest.options,
        **HardTricksLogic.options
    }


class WorldRequirementNormalGlitchesTest(WorldRequirementNormalTest, GlitchesLogic):
    options = {
        **WorldRequirementNormalTest.options,
        **GlitchesLogic.options
    }


class WorldRequirementLongIntendedTest(WorldRequirementLongTest, IntendedLogic):
    options = {
        **WorldRequirementLongTest.options,
        **IntendedLogic.options
    }


class WorldRequirementLongEasyTricksTest(WorldRequirementLongTest, EasyTricksLogic):
    options = {
        **WorldRequirementLongTest.options,
        **EasyTricksLogic.options
    }


class WorldRequirementLongHardTricksTest(WorldRequirementLongTest, HardTricksLogic):
    options = {
        **WorldRequirementLongTest.options,
        **HardTricksLogic.options
    }


class WorldRequirementLongGlitchesTest(WorldRequirementLongTest, GlitchesLogic):
    options = {
        **WorldRequirementLongTest.options,
        **GlitchesLogic.options
    }


class WorldRequirementMaxIntendedTest(WorldRequirementMaxTest, IntendedLogic):
    options = {
        **WorldRequirementMaxTest.options,
        **IntendedLogic.options
    }


class WorldRequirementMaxEasyTricksTest(WorldRequirementMaxTest, EasyTricksLogic):
    options = {
        **WorldRequirementMaxTest.options,
        **EasyTricksLogic.options
    }


class WorldRequirementMaxHardTricksTest(WorldRequirementMaxTest, HardTricksLogic):
    options = {
        **WorldRequirementMaxTest.options,
        **HardTricksLogic.options
    }


class WorldRequirementMaxGlitchesTest(WorldRequirementMaxTest, GlitchesLogic):
    options = {
        **WorldRequirementMaxTest.options,
        **GlitchesLogic.options
    }
