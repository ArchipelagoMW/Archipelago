from ..Items import world_unlock_table
from ..Options import RandomizeWorldOrder, SkipPuzzles
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from . import BanjoTooieTestBase

# There isn't much to test here other than the fact that it can successfully generate.


class TestRandomizedWorlds(BanjoTooieTestBase):
    options = {
        "skip_puzzles": SkipPuzzles.option_true,
        "randomize_worlds": RandomizeWorldOrder.option_true
    }


class TestVanillaWorlds(BanjoTooieTestBase):
    options = {
        "skip_puzzles": SkipPuzzles.option_true,
        "randomize_worlds": RandomizeWorldOrder.option_false
    }

    def test_vanilla_order(self) -> None:
        vanilla_locations = {item_name: item_data.default_location
                             for item_name, item_data in world_unlock_table.items()}
        for location in self.world.get_locations():
            if location.name in vanilla_locations.values():
                assert vanilla_locations[location.item.name] == location.name


class TestRandomizedWorldsEasyTricks(TestRandomizedWorlds, EasyTricksLogic):
    options = {
        **TestRandomizedWorlds.options,
        **EasyTricksLogic.options,
    }


class TestRandomizedWorldsHardTricks(TestRandomizedWorlds, HardTricksLogic):
    options = {
        **TestRandomizedWorlds.options,
        **HardTricksLogic.options,
    }


class TestRandomizedWorldsGlitches(TestRandomizedWorlds, GlitchesLogic):
    options = {
        **TestRandomizedWorlds.options,
        **GlitchesLogic.options,
    }


class TestVanillaWorldsIntended(TestVanillaWorlds, IntendedLogic):
    options = {
        **TestVanillaWorlds.options,
        **IntendedLogic.options,
    }


class TestVanillaWorldsEasyTricks(TestVanillaWorlds, EasyTricksLogic):
    options = {
        **TestVanillaWorlds.options,
        **EasyTricksLogic.options,
    }


class TestVanillaWorldsHardTricks(TestVanillaWorlds, HardTricksLogic):
    options = {
        **TestVanillaWorlds.options,
        **HardTricksLogic.options,
    }


class TestVanillaWorldsGlitches(TestVanillaWorlds, GlitchesLogic):
    options = {
        **TestVanillaWorlds.options,
        **GlitchesLogic.options,
    }
