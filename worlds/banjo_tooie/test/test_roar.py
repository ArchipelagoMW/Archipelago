from ..Names import itemName
from ..Options import RandomizeWorldDinoRoar
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from . import BanjoTooieTestBase


class TestRandomizedDinoRoarRewards(BanjoTooieTestBase):
    options = {
        "randomize_dino_roar": RandomizeWorldDinoRoar.option_true,
    }

    def test_item_pool(self) -> None:
        assert itemName.ROAR in [item.name for item in self.multiworld.itempool]


class TestVanillaDinoRoarRewards(BanjoTooieTestBase):
    options = {
        "randomize_dino_roar": RandomizeWorldDinoRoar.option_false,
    }

    def test_item_pool(self) -> None:
        assert itemName.ROAR not in [item.name for item in self.multiworld.itempool]


class TestRandomizedDinoRoarRewardsIntended(TestRandomizedDinoRoarRewards, IntendedLogic):
    options = {
        **TestRandomizedDinoRoarRewards.options,
        **IntendedLogic.options,
    }


class TestRandomizedDinoRoarRewardsEasyTricks(TestRandomizedDinoRoarRewards, EasyTricksLogic):
    options = {
        **TestRandomizedDinoRoarRewards.options,
        **EasyTricksLogic.options,
    }


class TestRandomizedDinoRoarRewardsHardTricks(TestRandomizedDinoRoarRewards, HardTricksLogic):
    options = {
        **TestRandomizedDinoRoarRewards.options,
        **HardTricksLogic.options,
    }


class TestRandomizedDinoRoarRewardsGlitches(TestRandomizedDinoRoarRewards, GlitchesLogic):
    options = {
        **TestRandomizedDinoRoarRewards.options,
        **GlitchesLogic.options,
    }


class TestVanillaDinoRoarRewardsIntended(TestVanillaDinoRoarRewards, IntendedLogic):
    options = {
        **TestVanillaDinoRoarRewards.options,
        **IntendedLogic.options,
    }


class TestVanillaDinoRoarRewardsEasyTricks(TestVanillaDinoRoarRewards, EasyTricksLogic):
    options = {
        **TestVanillaDinoRoarRewards.options,
        **EasyTricksLogic.options,
    }


class TestVanillaDinoRoarRewardsHardTricks(TestVanillaDinoRoarRewards, HardTricksLogic):
    options = {
        **TestVanillaDinoRoarRewards.options,
        **HardTricksLogic.options,
    }


class TestVanillaDinoRoarRewardsGlitches(TestVanillaDinoRoarRewards, GlitchesLogic):
    options = {
        **TestVanillaDinoRoarRewards.options,
        **GlitchesLogic.options,
    }
