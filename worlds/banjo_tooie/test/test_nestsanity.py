from ..Regions import NEST_REGIONS
from ..Names import itemName
from ..Options import EnableNestsanity
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from .test_fillers_and_traps import ONLY_BIG_O_PANTS_FILLER
from . import BanjoTooieTestBase


class TestNestsanityEnabled(BanjoTooieTestBase):
    options = {
        "nestsanity": EnableNestsanity.option_true,
    }
    tested_locations = []
    for locations in NEST_REGIONS.values():
        tested_locations.extend(locations)

    def test_locations(self) -> None:
        assert len(self.tested_locations) == 473
        world_location_names = [location.name for location in self.world.get_locations()]
        for name in self.tested_locations:
            assert name in world_location_names


class TestNestsanityDisabled(BanjoTooieTestBase):
    options = {
        **ONLY_BIG_O_PANTS_FILLER
    }
    tested_locations = []
    for locations in NEST_REGIONS.values():
        tested_locations.extend(locations)

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        assert itemName.ENEST not in item_pool_names
        assert itemName.FNEST not in item_pool_names
        assert itemName.GNEST not in item_pool_names

    def test_locations(self) -> None:
        world_location_names = [location.name for location in self.world.get_locations()]
        for name in self.tested_locations:
            assert name not in world_location_names


class TestNestsanityEnabledIntended(TestNestsanityEnabled, IntendedLogic):
    options = {
        **TestNestsanityEnabled.options,
        **IntendedLogic.options,
    }


class TestNestsanityEnabledEasyTricks(TestNestsanityEnabled, EasyTricksLogic):
    options = {
        **TestNestsanityEnabled.options,
        **EasyTricksLogic.options,
    }


class TestNestsanityEnabledHardTricks(TestNestsanityEnabled, HardTricksLogic):
    options = {
        **TestNestsanityEnabled.options,
        **HardTricksLogic.options,
    }


class TestNestsanityEnabledGlitches(TestNestsanityEnabled, GlitchesLogic):
    options = {
        **TestNestsanityEnabled.options,
        **GlitchesLogic.options,
    }


class TestNestsanityDisabledIntended(TestNestsanityDisabled, IntendedLogic):
    options = {
        **TestNestsanityDisabled.options,
        **IntendedLogic.options,
    }


class TestNestsanityDisabledEasyTricks(TestNestsanityDisabled, EasyTricksLogic):
    options = {
        **TestNestsanityDisabled.options,
        **EasyTricksLogic.options,
    }


class TestNestsanityDisabledHardTricks(TestNestsanityDisabled, HardTricksLogic):
    options = {
        **TestNestsanityDisabled.options,
        **HardTricksLogic.options,
    }


class TestNestsanityDisabledGlitches(TestNestsanityDisabled, GlitchesLogic):
    options = {
        **TestNestsanityDisabled.options,
        **GlitchesLogic.options,
    }
