from ..Names import itemName
from ..Options import RandomizeDoubloons
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from .test_fillers_and_traps import ONLY_BIG_O_PANTS_FILLER
from ..Locations import all_location_table
from . import BanjoTooieTestBase


class TestRandomizedDoubloons(BanjoTooieTestBase):
    options = {
        "randomize_doubloons": RandomizeDoubloons.option_true,
        **ONLY_BIG_O_PANTS_FILLER
    }

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        assert item_pool_names.count(itemName.DOUBLOON) == 30


class TestVanillaDoubloons(BanjoTooieTestBase):
    options = {
        "randomize_doubloons": RandomizeDoubloons.option_false,
        **ONLY_BIG_O_PANTS_FILLER
    }

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        assert item_pool_names.count(itemName.DOUBLOON) == 0

    def test_prefills(self) -> None:
        vanilla_locations_names = [location_name for location_name, location_data in all_location_table.items()
                                   if location_data.group == "Doubloon"]
        vanilla_locations = [location for location in self.world.get_locations()
                             if location.name in vanilla_locations_names]

        assert len(vanilla_locations) == 30
        for location in vanilla_locations:
            assert location.item.name == itemName.DOUBLOON


class TestRandomizedDoubloonsIntended(TestRandomizedDoubloons, IntendedLogic):
    options = {
        **TestRandomizedDoubloons.options,
        **IntendedLogic.options,
    }


class TestRandomizedDoubloonsEasyTricks(TestRandomizedDoubloons, EasyTricksLogic):
    options = {
        **TestRandomizedDoubloons.options,
        **EasyTricksLogic.options,
    }


class TestRandomizedDoubloonsHardTricks(TestRandomizedDoubloons, HardTricksLogic):
    options = {
        **TestRandomizedDoubloons.options,
        **HardTricksLogic.options,
    }


class TestRandomizedDoubloonsGlitches(TestRandomizedDoubloons, GlitchesLogic):
    options = {
        **TestRandomizedDoubloons.options,
        **GlitchesLogic.options,
    }


class TestVanillaDoubloonsIntended(TestVanillaDoubloons, IntendedLogic):
    options = {
        **TestVanillaDoubloons.options,
        **IntendedLogic.options,
    }


class TestVanillaDoubloonsEasyTricks(TestVanillaDoubloons, EasyTricksLogic):
    options = {
        **TestVanillaDoubloons.options,
        **EasyTricksLogic.options,
    }


class TestVanillaDoubloonsHardTricks(TestVanillaDoubloons, HardTricksLogic):
    options = {
        **TestVanillaDoubloons.options,
        **HardTricksLogic.options,
    }


class TestVanillaDoubloonsGlitches(TestVanillaDoubloons, GlitchesLogic):
    options = {
        **TestVanillaDoubloons.options,
        **GlitchesLogic.options,
    }
