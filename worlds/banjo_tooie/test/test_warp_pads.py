from ..Names import itemName
from ..Options import RandomizeWarpPads
from ..Items import warp_pad_table
from ..Locations import all_location_table
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



class TestVanillaWarpPads(BanjoTooieTestBase):
    options = {
        "randomize_warp_pads": RandomizeWarpPads.option_false,
    }

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        for warp_pad_name in warp_pad_table.keys():
            assert warp_pad_name not in item_pool_names

    def test_prefills(self) -> None:
        vanilla_locations_names = [location_name for location_name, location_data in all_location_table.items()\
                                   if location_data.group == "Warp Pads"]
        vanilla_locations = [location for location in self.world.get_locations()\
                             if location.name in vanilla_locations_names]

        warp_pad_names = warp_pad_table.keys()

        assert len(vanilla_locations) == 39
        for location in vanilla_locations:
            assert location.item.name in warp_pad_names

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
