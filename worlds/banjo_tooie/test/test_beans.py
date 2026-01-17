from ..Names import itemName
from ..Options import RandomizeBeans
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from . import BanjoTooieTestBase


class TestRandomizedBeans(BanjoTooieTestBase):
    options = {
        "randomize_beans": RandomizeBeans.option_true,
    }

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        assert item_pool_names.count(itemName.BEANS) == 2


class TestVanillaBeans(BanjoTooieTestBase):
    options = {
        "randomize_beans": RandomizeBeans.option_false,
    }

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        assert item_pool_names.count(itemName.BEANS) == 0


class TestRandomizedBeansIntended(TestRandomizedBeans, IntendedLogic):
    options = {
        **TestRandomizedBeans.options,
        **IntendedLogic.options,
    }


class TestRandomizedBeansEasyTricks(TestRandomizedBeans, EasyTricksLogic):
    options = {
        **TestRandomizedBeans.options,
        **EasyTricksLogic.options,
    }


class TestRandomizedBeansHardTricks(TestRandomizedBeans, HardTricksLogic):
    options = {
        **TestRandomizedBeans.options,
        **HardTricksLogic.options,
    }


class TestRandomizedBeansGlitches(TestRandomizedBeans, GlitchesLogic):
    options = {
        **TestRandomizedBeans.options,
        **GlitchesLogic.options,
    }


class TestVanillaBeansIntended(TestVanillaBeans, IntendedLogic):
    options = {
        **TestVanillaBeans.options,
        **IntendedLogic.options,
    }


class TestVanillaBeansEasyTricks(TestVanillaBeans, EasyTricksLogic):
    options = {
        **TestVanillaBeans.options,
        **EasyTricksLogic.options,
    }


class TestVanillaBeansHardTricks(TestVanillaBeans, HardTricksLogic):
    options = {
        **TestVanillaBeans.options,
        **HardTricksLogic.options,
    }


class TestVanillaBeansGlitches(TestVanillaBeans, GlitchesLogic):
    options = {
        **TestVanillaBeans.options,
        **GlitchesLogic.options,
    }
