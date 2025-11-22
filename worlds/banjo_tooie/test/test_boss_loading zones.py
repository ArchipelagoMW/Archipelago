from ..Options import RandomizeBossLoadingZones
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from . import BanjoTooieTestBase

# There isn't much to test here other than the fact that it can successfully generate.


class TestRandomizedLoadingZones(BanjoTooieTestBase):
    options = {
        "randomize_boss_loading_zones": RandomizeBossLoadingZones.option_true
    }


class TestVanillaLoadingZones(BanjoTooieTestBase):
    options = {
        "randomize_boss_loading_zones": RandomizeBossLoadingZones.option_false
    }


class TestRandomizedLoadingZonesIntended(TestRandomizedLoadingZones, IntendedLogic):
    options = {
        **TestRandomizedLoadingZones.options,
        **IntendedLogic.options,
    }


class TestRandomizedLoadingZonesEasyTricks(TestRandomizedLoadingZones, EasyTricksLogic):
    options = {
        **TestRandomizedLoadingZones.options,
        **EasyTricksLogic.options,
    }


class TestRandomizedLoadingZonesHardTricks(TestRandomizedLoadingZones, HardTricksLogic):
    options = {
        **TestRandomizedLoadingZones.options,
        **HardTricksLogic.options,
    }


class TestRandomizedLoadingZonesGlitches(TestRandomizedLoadingZones, GlitchesLogic):
    options = {
        **TestRandomizedLoadingZones.options,
        **GlitchesLogic.options,
    }


class TestVanillaLoadingZonesIntended(TestVanillaLoadingZones, IntendedLogic):
    options = {
        **TestVanillaLoadingZones.options,
        **IntendedLogic.options,
    }


class TestVanillaLoadingZonesEasyTricks(TestVanillaLoadingZones, EasyTricksLogic):
    options = {
        **TestVanillaLoadingZones.options,
        **EasyTricksLogic.options,
    }


class TestVanillaLoadingZonesHardTricks(TestVanillaLoadingZones, HardTricksLogic):
    options = {
        **TestVanillaLoadingZones.options,
        **HardTricksLogic.options,
    }


class TestVanillaLoadingZonesGlitches(TestVanillaLoadingZones, GlitchesLogic):
    options = {
        **TestVanillaLoadingZones.options,
        **GlitchesLogic.options,
    }
