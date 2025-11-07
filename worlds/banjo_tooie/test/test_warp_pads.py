from ..Options import RandomizeWarpPads
from ..Items import warp_pad_table
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from . import BanjoTooieTestBase


class TestRandomizedWarpPads(BanjoTooieTestBase):
    options = {
        "randomize_warp_pads": RandomizeWarpPads.option_true,
    }

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        for warp_pad_name in warp_pad_table.keys():
            assert warp_pad_name in item_pool_names

    def test_locations(self) -> None:
        world_location_names = [location.name for location in self.world.get_locations()]
        for warp_pad_data in warp_pad_table.values():
            assert warp_pad_data.default_location in world_location_names


class TestVanillaWarpPads(BanjoTooieTestBase):
    options = {
        "randomize_warp_pads": RandomizeWarpPads.option_false,
    }

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        for warp_pad_name in warp_pad_table.keys():
            assert warp_pad_name not in item_pool_names

    def test_locations(self) -> None:
        world_location_names = [location.name for location in self.world.get_locations()]
        for warp_pad_data in warp_pad_table.values():
            assert warp_pad_data.default_location not in world_location_names


class TestRandomizedWarpPadsIntended(TestRandomizedWarpPads, IntendedLogic):
    options = {
        **TestRandomizedWarpPads.options,
        **IntendedLogic.options,
    }


class TestRandomizedWarpPadsEasyTricks(TestRandomizedWarpPads, EasyTricksLogic):
    options = {
        **TestRandomizedWarpPads.options,
        **EasyTricksLogic.options,
    }


class TestRandomizedWarpPadsHardTricks(TestRandomizedWarpPads, HardTricksLogic):
    options = {
        **TestRandomizedWarpPads.options,
        **HardTricksLogic.options,
    }


class TestRandomizedWarpPadsGlitches(TestRandomizedWarpPads, GlitchesLogic):
    options = {
        **TestRandomizedWarpPads.options,
        **GlitchesLogic.options,
    }


class TestVanillaWarpPadsIntended(TestVanillaWarpPads, IntendedLogic):
    options = {
        **TestVanillaWarpPads.options,
        **IntendedLogic.options,
    }


class TestVanillaWarpPadsEasyTricks(TestVanillaWarpPads, EasyTricksLogic):
    options = {
        **TestVanillaWarpPads.options,
        **EasyTricksLogic.options,
    }


class TestVanillaWarpPadsHardTricks(TestVanillaWarpPads, HardTricksLogic):
    options = {
        **TestVanillaWarpPads.options,
        **HardTricksLogic.options,
    }


class TestVanillaWarpPadsGlitches(TestVanillaWarpPads, GlitchesLogic):
    options = {
        **TestVanillaWarpPads.options,
        **GlitchesLogic.options,
    }
