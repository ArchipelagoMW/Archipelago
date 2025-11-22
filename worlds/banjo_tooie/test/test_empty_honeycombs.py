from ..Names import itemName
from ..Options import RandomizeHoneycombs
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from ..Locations import all_location_table
from . import BanjoTooieTestBase


class TestRandomizedEmptyHoneycombs(BanjoTooieTestBase):
    options = {
        "randomize_honeycombs": RandomizeHoneycombs.option_true,
    }

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        assert item_pool_names.count(itemName.HONEY) == 25


class TestVanillaEmptyHoneycombs(BanjoTooieTestBase):
    options = {
        "randomize_honeycombs": RandomizeHoneycombs.option_false,
    }

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        assert item_pool_names.count(itemName.HONEY) == 0

    def test_prefills(self) -> None:
        vanilla_locations_names = [location_name for location_name, location_data in all_location_table.items()
                                   if location_data.group == "Honeycomb"]
        vanilla_locations = [location for location in self.world.get_locations()
                             if location.name in vanilla_locations_names]

        assert len(vanilla_locations) == 25
        for location in vanilla_locations:
            assert location.item.name == itemName.HONEY


class TestRandomizedEmptyHoneycombsIntended(TestRandomizedEmptyHoneycombs, IntendedLogic):
    options = {
        **TestRandomizedEmptyHoneycombs.options,
        **IntendedLogic.options,
    }


class TestRandomizedEmptyHoneycombsEasyTricks(TestRandomizedEmptyHoneycombs, EasyTricksLogic):
    options = {
        **TestRandomizedEmptyHoneycombs.options,
        **EasyTricksLogic.options,
    }


class TestRandomizedEmptyHoneycombsHardTricks(TestRandomizedEmptyHoneycombs, HardTricksLogic):
    options = {
        **TestRandomizedEmptyHoneycombs.options,
        **HardTricksLogic.options,
    }


class TestRandomizedEmptyHoneycombsGlitches(TestRandomizedEmptyHoneycombs, GlitchesLogic):
    options = {
        **TestRandomizedEmptyHoneycombs.options,
        **GlitchesLogic.options,
    }


class TestVanillaEmptyHoneycombsIntended(TestVanillaEmptyHoneycombs, IntendedLogic):
    options = {
        **TestVanillaEmptyHoneycombs.options,
        **IntendedLogic.options,
    }


class TestVanillaEmptyHoneycombsEasyTricks(TestVanillaEmptyHoneycombs, EasyTricksLogic):
    options = {
        **TestVanillaEmptyHoneycombs.options,
        **EasyTricksLogic.options,
    }


class TestVanillaEmptyHoneycombsHardTricks(TestVanillaEmptyHoneycombs, HardTricksLogic):
    options = {
        **TestVanillaEmptyHoneycombs.options,
        **HardTricksLogic.options,
    }


class TestVanillaEmptyHoneycombsGlitches(TestVanillaEmptyHoneycombs, GlitchesLogic):
    options = {
        **TestVanillaEmptyHoneycombs.options,
        **GlitchesLogic.options,
    }
