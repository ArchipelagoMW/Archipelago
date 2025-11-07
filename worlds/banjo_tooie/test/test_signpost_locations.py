from ..Regions import SIGNPOST_REGIONS
from ..Options import RandomizeSignposts
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from . import BanjoTooieTestBase


class TestRandomizedSignposts(BanjoTooieTestBase):
    options = {
        "randomize_signposts": RandomizeSignposts.option_true,
    }

    tested_locations = []
    for locations in SIGNPOST_REGIONS.values():
        tested_locations.extend(locations)

    def test_locations(self) -> None:
        assert len(self.tested_locations) == 61
        world_location_names = [location.name for location in self.world.get_locations()]
        for name in self.tested_locations:
            assert name in world_location_names


class TestNonRandomizedSignposts(BanjoTooieTestBase):
    options = {
        "randomize_signposts": RandomizeSignposts.option_false,
    }
    tested_locations = []
    for locations in SIGNPOST_REGIONS.values():
        tested_locations.extend(locations)

    def test_locations(self) -> None:
        assert len(self.tested_locations) == 61
        world_location_names = self.world.get_locations()
        for name in self.tested_locations:
            assert name not in world_location_names


class TestRandomizedSignpostsIntended(TestRandomizedSignposts, IntendedLogic):
    options = {
        **TestRandomizedSignposts.options,
        **IntendedLogic.options,
    }


class TestRandomizedSignpostsEasyTricks(TestRandomizedSignposts, EasyTricksLogic):
    options = {
        **TestRandomizedSignposts.options,
        **EasyTricksLogic.options,
    }


class TestRandomizedSignpostsHardTricks(TestRandomizedSignposts, HardTricksLogic):
    options = {
        **TestRandomizedSignposts.options,
        **HardTricksLogic.options,
    }


class TestRandomizedSignpostsGlitches(TestRandomizedSignposts, GlitchesLogic):
    options = {
        **TestRandomizedSignposts.options,
        **GlitchesLogic.options,
    }


class TestNonRandomizedSignpostsIntended(TestNonRandomizedSignposts, IntendedLogic):
    options = {
        **TestNonRandomizedSignposts.options,
        **IntendedLogic.options,
    }


class TestNonRandomizedSignpostsEasyTricks(TestNonRandomizedSignposts, EasyTricksLogic):
    options = {
        **TestNonRandomizedSignposts.options,
        **EasyTricksLogic.options,
    }


class TestNonRandomizedSignpostsHardTricks(TestNonRandomizedSignposts, HardTricksLogic):
    options = {
        **TestNonRandomizedSignposts.options,
        **HardTricksLogic.options,
    }


class TestNonRandomizedSignpostsGlitches(TestNonRandomizedSignposts, GlitchesLogic):
    options = {
        **TestNonRandomizedSignposts.options,
        **GlitchesLogic.options,
    }
