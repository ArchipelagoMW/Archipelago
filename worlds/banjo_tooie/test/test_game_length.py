from ..Options import GameLength
from ..Names import itemName
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from . import BanjoTooieTestBase
from math import ceil

class GameLengthTest(BanjoTooieTestBase):
    expected_world_costs = [1, 4, 8, 14, 20, 28, 36, 45, 55]
    def test_check_world_costs(self) -> None:
        assert list(self.world.randomize_worlds.values()) == self.expected_world_costs

    def test_jiggies(self) -> None:
        expected_progression_jiggies = max(self.expected_world_costs)
        expected_useful_jiggies = ceil((90 - expected_progression_jiggies) / 2)

        assert sum(1 for item in self.multiworld.itempool
                       if item.name == itemName.JIGGY and item.advancement) \
                 == expected_progression_jiggies - 1 # jingaling's

        assert sum(1 for item in self.multiworld.itempool
                      if item.name == itemName.JIGGY and item.useful) \
                 == expected_useful_jiggies


class GameLengthMinTest(GameLengthTest):
    expected_world_costs = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    options = {
        "game_length": GameLength.option_custom,
        "custom_worlds": "1,1,1,1,1,1,1,1,1"
    }

class GameLengthQuickTest(GameLengthTest):
    expected_world_costs = [1,3,6,10,15,21,28,35,44]
    options = {
        "game_length": GameLength.option_quick
    }

class GameLengthNormalTest(GameLengthTest):
    expected_world_costs = [1,4,8,14,20,28,36,45,55]
    options = {
        "game_length": GameLength.option_normal
    }

class GameLengthLongTest(GameLengthTest):
    expected_world_costs = [1,8,16,25,34,43,52,60,70]
    options = {
        "game_length": GameLength.option_long
    }

class GameLengthMaxTest(GameLengthTest):
    expected_world_costs = [1,10,20,30,50,60,70,80,90]
    options = {
        "game_length": GameLength.option_custom,
        "custom_worlds": "1,10,20,30,50,60,70,80,90"
    }

class GameLengthMinIntendedTest(GameLengthMinTest, IntendedLogic):
    options = {
        **GameLengthMinTest.options,
        **IntendedLogic.options
    }

class GameLengthMinEasyTricksTest(GameLengthMinTest, EasyTricksLogic):
    options = {
        **GameLengthMinTest.options,
        **EasyTricksLogic.options
    }

class GameLengthMinHardTricksTest(GameLengthMinTest, HardTricksLogic):
    options = {
        **GameLengthMinTest.options,
        **HardTricksLogic.options
    }

class GameLengthMinGlitchesTest(GameLengthMinTest, GlitchesLogic):
    options = {
        **GameLengthMinTest.options,
        **GlitchesLogic.options
    }

class GameLengthQuickIntendedTest(GameLengthQuickTest, IntendedLogic):
    options = {
        **GameLengthQuickTest.options,
        **IntendedLogic.options
    }

class GameLengthQuickEasyTricksTest(GameLengthQuickTest, EasyTricksLogic):
    options = {
        **GameLengthQuickTest.options,
        **EasyTricksLogic.options
    }

class GameLengthQuickHardTricksTest(GameLengthQuickTest, HardTricksLogic):
    options = {
        **GameLengthQuickTest.options,
        **HardTricksLogic.options
    }

class GameLengthQuickGlitchesTest(GameLengthQuickTest, GlitchesLogic):
    options = {
        **GameLengthQuickTest.options,
        **GlitchesLogic.options
    }

class GameLengthNormalIntendedTest(GameLengthNormalTest, IntendedLogic):
    options = {
        **GameLengthNormalTest.options,
        **IntendedLogic.options
    }

class GameLengthNormalEasyTricksTest(GameLengthNormalTest, EasyTricksLogic):
    options = {
        **GameLengthNormalTest.options,
        **EasyTricksLogic.options
    }

class GameLengthNormalHardTricksTest(GameLengthNormalTest, HardTricksLogic):
    options = {
        **GameLengthNormalTest.options,
        **HardTricksLogic.options
    }

class GameLengthNormalGlitchesTest(GameLengthNormalTest, GlitchesLogic):
    options = {
        **GameLengthNormalTest.options,
        **GlitchesLogic.options
    }

class GameLengthLongIntendedTest(GameLengthLongTest, IntendedLogic):
    options = {
        **GameLengthLongTest.options,
        **IntendedLogic.options
    }

class GameLengthLongEasyTricksTest(GameLengthLongTest, EasyTricksLogic):
    options = {
        **GameLengthLongTest.options,
        **EasyTricksLogic.options
    }

class GameLengthLongHardTricksTest(GameLengthLongTest, HardTricksLogic):
    options = {
        **GameLengthLongTest.options,
        **HardTricksLogic.options
    }

class GameLengthLongGlitchesTest(GameLengthLongTest, GlitchesLogic):
    options = {
        **GameLengthLongTest.options,
        **GlitchesLogic.options
    }

class GameLengthMaxIntendedTest(GameLengthMaxTest, IntendedLogic):
    options = {
        **GameLengthMaxTest.options,
        **IntendedLogic.options
    }

class GameLengthMaxEasyTricksTest(GameLengthMaxTest, EasyTricksLogic):
    options = {
        **GameLengthMaxTest.options,
        **EasyTricksLogic.options
    }

class GameLengthMaxHardTricksTest(GameLengthMaxTest, HardTricksLogic):
    options = {
        **GameLengthMaxTest.options,
        **HardTricksLogic.options
    }

class GameLengthMaxGlitchesTest(GameLengthMaxTest, GlitchesLogic):
    options = {
        **GameLengthMaxTest.options,
        **GlitchesLogic.options
    }
