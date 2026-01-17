from ..Names import itemName
from ..Options import RandomizeGreenRelics
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from . import BanjoTooieTestBase


class TestRandomizedGreenRelics(BanjoTooieTestBase):
    options = {
        "randomize_green_relics": RandomizeGreenRelics.option_true,
    }

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        assert item_pool_names.count(itemName.GRRELIC) == 25


class TestVanillaGreenRelics(BanjoTooieTestBase):
    options = {
        "randomize_green_relics": RandomizeGreenRelics.option_false,
    }

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        assert item_pool_names.count(itemName.GRRELIC) == 0


class TestRandomizedGreenRelicsIntended(TestRandomizedGreenRelics, IntendedLogic):
    options = {
        **TestRandomizedGreenRelics.options,
        **IntendedLogic.options,
    }


class TestRandomizedGreenRelicsEasyTricks(TestRandomizedGreenRelics, EasyTricksLogic):
    options = {
        **TestRandomizedGreenRelics.options,
        **EasyTricksLogic.options,
    }


class TestRandomizedGreenRelicsHardTricks(TestRandomizedGreenRelics, HardTricksLogic):
    options = {
        **TestRandomizedGreenRelics.options,
        **HardTricksLogic.options,
    }


class TestRandomizedGreenRelicsGlitches(TestRandomizedGreenRelics, GlitchesLogic):
    options = {
        **TestRandomizedGreenRelics.options,
        **GlitchesLogic.options,
    }


class TestVanillaGreenRelicsIntended(TestVanillaGreenRelics, IntendedLogic):
    options = {
        **TestVanillaGreenRelics.options,
        **IntendedLogic.options,
    }


class TestVanillaGreenRelicsEasyTricks(TestVanillaGreenRelics, EasyTricksLogic):
    options = {
        **TestVanillaGreenRelics.options,
        **EasyTricksLogic.options,
    }


class TestVanillaGreenRelicsHardTricks(TestVanillaGreenRelics, HardTricksLogic):
    options = {
        **TestVanillaGreenRelics.options,
        **HardTricksLogic.options,
    }


class TestVanillaGreenRelicsGlitches(TestVanillaGreenRelics, GlitchesLogic):
    options = {
        **TestVanillaGreenRelics.options,
        **GlitchesLogic.options,
    }
