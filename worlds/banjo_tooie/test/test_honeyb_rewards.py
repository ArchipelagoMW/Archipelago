from ..Names import locationName
from ..Options import EnableHoneyBRewards
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from . import BanjoTooieTestBase


class TestRandomizedHoneyBRewards(BanjoTooieTestBase):
    options = {
        "honeyb_rewards": EnableHoneyBRewards.option_true,
    }

    def test_locations(self) -> None:
        location_names = [
            locationName.HONEYBR1,
            locationName.HONEYBR2,
            locationName.HONEYBR3,
            locationName.HONEYBR4,
            locationName.HONEYBR5
        ]
        world_location_names = [location.name for location in self.world.get_locations()]
        for name in location_names:
            assert name in world_location_names


class TestVanillaHoneyBRewards(BanjoTooieTestBase):
    options = {
        "honeyb_rewards": EnableHoneyBRewards.option_false,
    }

    def test_locations(self) -> None:
        location_names = [
            locationName.HONEYBR1,
            locationName.HONEYBR2,
            locationName.HONEYBR3,
            locationName.HONEYBR4,
            locationName.HONEYBR5
        ]
        world_location_names = [location.name for location in self.world.get_locations()]
        for name in location_names:
            assert name not in world_location_names


class TestRandomizedHoneyBRewardsIntended(TestRandomizedHoneyBRewards, IntendedLogic):
    options = {
        **TestRandomizedHoneyBRewards.options,
        **IntendedLogic.options,
    }


class TestRandomizedHoneyBRewardsEasyTricks(TestRandomizedHoneyBRewards, EasyTricksLogic):
    options = {
        **TestRandomizedHoneyBRewards.options,
        **EasyTricksLogic.options,
    }


class TestRandomizedHoneyBRewardsHardTricks(TestRandomizedHoneyBRewards, HardTricksLogic):
    options = {
        **TestRandomizedHoneyBRewards.options,
        **HardTricksLogic.options,
    }


class TestRandomizedHoneyBRewardsGlitches(TestRandomizedHoneyBRewards, GlitchesLogic):
    options = {
        **TestRandomizedHoneyBRewards.options,
        **GlitchesLogic.options,
    }


class TestVanillaHoneyBRewardsIntended(TestVanillaHoneyBRewards, IntendedLogic):
    options = {
        **TestVanillaHoneyBRewards.options,
        **IntendedLogic.options,
    }


class TestVanillaHoneyBRewardsEasyTricks(TestVanillaHoneyBRewards, EasyTricksLogic):
    options = {
        **TestVanillaHoneyBRewards.options,
        **EasyTricksLogic.options,
    }


class TestVanillaHoneyBRewardsHardTricks(TestVanillaHoneyBRewards, HardTricksLogic):
    options = {
        **TestVanillaHoneyBRewards.options,
        **HardTricksLogic.options,
    }


class TestVanillaHoneyBRewardsGlitches(TestVanillaHoneyBRewards, GlitchesLogic):
    options = {
        **TestVanillaHoneyBRewards.options,
        **GlitchesLogic.options,
    }
