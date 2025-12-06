from BaseClasses import ItemClassification
from ..Names import itemName, locationName
from ..Options import RandomizeCheatoRewards
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from . import BanjoTooieTestBase


class TestRandomizedCheatoRewards(BanjoTooieTestBase):
    options = {
        "cheato_rewards": RandomizeCheatoRewards.option_true,
    }

    def test_item_classification(self) -> None:
        items = [item for item in self.multiworld.itempool if item.name == itemName.PAGES]
        for item in items:
            assert item.advancement

    def test_locations(self) -> None:
        location_names = [
            locationName.CHEATOR1,
            locationName.CHEATOR2,
            locationName.CHEATOR3,
            locationName.CHEATOR4,
            locationName.CHEATOR5
        ]
        world_location_names = [location.name for location in self.world.get_locations()]
        for name in location_names:
            assert name in world_location_names


class TestVanillaCheatoRewards(BanjoTooieTestBase):
    options = {
        "cheato_rewards": RandomizeCheatoRewards.option_false,
    }

    def test_item_classification(self) -> None:
        items = [item for item in self.multiworld.itempool if item.name == itemName.PAGES]
        for item in items:
            assert item.classification == ItemClassification.filler


class TestRandomizedCheatoRewardsIntended(TestRandomizedCheatoRewards, IntendedLogic):
    options = {
        **TestRandomizedCheatoRewards.options,
        **IntendedLogic.options,
    }


class TestRandomizedCheatoRewardsEasyTricks(TestRandomizedCheatoRewards, EasyTricksLogic):
    options = {
        **TestRandomizedCheatoRewards.options,
        **EasyTricksLogic.options,
    }


class TestRandomizedCheatoRewardsHardTricks(TestRandomizedCheatoRewards, HardTricksLogic):
    options = {
        **TestRandomizedCheatoRewards.options,
        **HardTricksLogic.options,
    }


class TestRandomizedCheatoRewardsGlitches(TestRandomizedCheatoRewards, GlitchesLogic):
    options = {
        **TestRandomizedCheatoRewards.options,
        **GlitchesLogic.options,
    }


class TestVanillaCheatoRewardsIntended(TestVanillaCheatoRewards, IntendedLogic):
    options = {
        **TestVanillaCheatoRewards.options,
        **IntendedLogic.options,
    }


class TestVanillaCheatoRewardsEasyTricks(TestVanillaCheatoRewards, EasyTricksLogic):
    options = {
        **TestVanillaCheatoRewards.options,
        **EasyTricksLogic.options,
    }


class TestVanillaCheatoRewardsHardTricks(TestVanillaCheatoRewards, HardTricksLogic):
    options = {
        **TestVanillaCheatoRewards.options,
        **HardTricksLogic.options,
    }


class TestVanillaCheatoRewardsGlitches(TestVanillaCheatoRewards, GlitchesLogic):
    options = {
        **TestVanillaCheatoRewards.options,
        **GlitchesLogic.options,
    }
