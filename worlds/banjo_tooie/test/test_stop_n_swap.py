from ..Options import RandomizeStopnSwap
from ..Items import stop_n_swap_table
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from . import BanjoTooieTestBase


class TestRandomizedStopnSwap(BanjoTooieTestBase):
    options = {
        "randomize_stop_n_swap": RandomizeStopnSwap.option_true,
    }

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        for glowbo in stop_n_swap_table.keys():
            assert glowbo in item_pool_names


class TestVanillaStopnSwap(BanjoTooieTestBase):
    options = {
        "randomize_stop_n_swap": RandomizeStopnSwap.option_false,
    }

    def test_item_pool(self) -> None:
        for glowbo in stop_n_swap_table.keys():
            assert glowbo not in self.multiworld.itempool

    def test_prefills(self) -> None:
        glowbo_location_names = [item_data.default_location for item_data in stop_n_swap_table.values()]
        for location in self.world.get_locations():
            if location.name in glowbo_location_names:
                assert location.name == stop_n_swap_table[location.item.name].default_location


class TestRandomizedStopnSwapIntended(TestRandomizedStopnSwap, IntendedLogic):
    options = {
        **TestRandomizedStopnSwap.options,
        **IntendedLogic.options,
    }


class TestRandomizedStopnSwapEasyTricks(TestRandomizedStopnSwap, EasyTricksLogic):
    options = {
        **TestRandomizedStopnSwap.options,
        **EasyTricksLogic.options,
    }


class TestRandomizedStopnSwapHardTricks(TestRandomizedStopnSwap, HardTricksLogic):
    options = {
        **TestRandomizedStopnSwap.options,
        **HardTricksLogic.options,
    }


class TestRandomizedStopnSwapGlitches(TestRandomizedStopnSwap, GlitchesLogic):
    options = {
        **TestRandomizedStopnSwap.options,
        **GlitchesLogic.options,
    }


class TestVanillaStopnSwapIntended(TestVanillaStopnSwap, IntendedLogic):
    options = {
        **TestVanillaStopnSwap.options,
        **IntendedLogic.options,
    }


class TestVanillaStopnSwapEasyTricks(TestVanillaStopnSwap, EasyTricksLogic):
    options = {
        **TestVanillaStopnSwap.options,
        **EasyTricksLogic.options,
    }


class TestVanillaStopnSwapHardTricks(TestVanillaStopnSwap, HardTricksLogic):
    options = {
        **TestVanillaStopnSwap.options,
        **HardTricksLogic.options,
    }


class TestVanillaStopnSwapGlitches(TestVanillaStopnSwap, GlitchesLogic):
    options = {
        **TestVanillaStopnSwap.options,
        **GlitchesLogic.options,
    }
