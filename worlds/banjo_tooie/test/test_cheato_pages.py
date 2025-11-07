from ..Names import itemName
from ..Options import RandomizeCheatoPages
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from ..Locations import all_location_table
from . import BanjoTooieTestBase


class TestRandomizedCheatoPages(BanjoTooieTestBase):
    options = {
        "randomize_cheato": RandomizeCheatoPages.option_true,
    }

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        assert item_pool_names.count(itemName.PAGES) == 25


class TestVanillaCheatoPages(BanjoTooieTestBase):
    options = {
        "randomize_cheato": RandomizeCheatoPages.option_false,
    }

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        assert item_pool_names.count(itemName.PAGES) == 0

    def test_prefills(self) -> None:
        vanilla_locations_names = [location_name for location_name, location_data in all_location_table.items()
                                   if location_data.group == "Cheato Page"]
        vanilla_locations = [location for location in self.world.get_locations()
                             if location.name in vanilla_locations_names]

        assert len(vanilla_locations) == 25
        for location in vanilla_locations:
            assert location.item.name == itemName.PAGES


class TestRandomizedCheatoPagesIntended(TestRandomizedCheatoPages, IntendedLogic):
    options = {
        **TestRandomizedCheatoPages.options,
        **IntendedLogic.options,
    }


class TestRandomizedCheatoPagesEasyTricks(TestRandomizedCheatoPages, EasyTricksLogic):
    options = {
        **TestRandomizedCheatoPages.options,
        **EasyTricksLogic.options,
    }


class TestRandomizedCheatoPagesHardTricks(TestRandomizedCheatoPages, HardTricksLogic):
    options = {
        **TestRandomizedCheatoPages.options,
        **HardTricksLogic.options,
    }


class TestRandomizedCheatoPagesGlitches(TestRandomizedCheatoPages, GlitchesLogic):
    options = {
        **TestRandomizedCheatoPages.options,
        **GlitchesLogic.options,
    }


class TestVanillaCheatoPagesIntended(TestVanillaCheatoPages, IntendedLogic):
    options = {
        **TestVanillaCheatoPages.options,
        **IntendedLogic.options,
    }


class TestVanillaCheatoPagesEasyTricks(TestVanillaCheatoPages, EasyTricksLogic):
    options = {
        **TestVanillaCheatoPages.options,
        **EasyTricksLogic.options,
    }


class TestVanillaCheatoPagesHardTricks(TestVanillaCheatoPages, HardTricksLogic):
    options = {
        **TestVanillaCheatoPages.options,
        **HardTricksLogic.options,
    }


class TestVanillaCheatoPagesGlitches(TestVanillaCheatoPages, GlitchesLogic):
    options = {
        **TestVanillaCheatoPages.options,
        **GlitchesLogic.options,
    }
