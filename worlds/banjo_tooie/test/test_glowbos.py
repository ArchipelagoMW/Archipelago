from ..Options import RandomizeGlowbos
from ..Items import glowbo_table
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from . import BanjoTooieTestBase


class TestRandomizedGlowbos(BanjoTooieTestBase):
    options = {
        "randomize_glowbos": RandomizeGlowbos.option_true,
    }

    def test_item_pool(self) -> None:
        item_pool_names = {item.name for item in self.multiworld.itempool}
        for glowbo in glowbo_table.keys():
            assert glowbo in item_pool_names


class TestVanillaGlowbos(BanjoTooieTestBase):
    options = {
        "randomize_glowbos": RandomizeGlowbos.option_false,
    }

    def test_item_pool(self) -> None:
        for glowbo in glowbo_table.keys():
            assert glowbo not in self.multiworld.itempool

    def test_prefills(self) -> None:
        glowbo_location_names = [item_data.default_location for item_data in glowbo_table.values()]
        for location in self.world.get_locations():
            if location.name in glowbo_location_names:
                assert location.name == glowbo_table[location.item.name].default_location


class TestRandomizedGlowbosIntended(TestRandomizedGlowbos, IntendedLogic):
    options = {
        **TestRandomizedGlowbos.options,
        **IntendedLogic.options,
    }


class TestRandomizedGlowbosEasyTricks(TestRandomizedGlowbos, EasyTricksLogic):
    options = {
        **TestRandomizedGlowbos.options,
        **EasyTricksLogic.options,
    }


class TestRandomizedGlowbosHardTricks(TestRandomizedGlowbos, HardTricksLogic):
    options = {
        **TestRandomizedGlowbos.options,
        **HardTricksLogic.options,
    }


class TestRandomizedGlowbosGlitches(TestRandomizedGlowbos, GlitchesLogic):
    options = {
        **TestRandomizedGlowbos.options,
        **GlitchesLogic.options,
    }


class TestVanillaGlowbosIntended(TestVanillaGlowbos, IntendedLogic):
    options = {
        **TestVanillaGlowbos.options,
        **IntendedLogic.options,
    }


class TestVanillaGlowbosEasyTricks(TestVanillaGlowbos, EasyTricksLogic):
    options = {
        **TestVanillaGlowbos.options,
        **EasyTricksLogic.options,
    }


class TestVanillaGlowbosHardTricks(TestVanillaGlowbos, HardTricksLogic):
    options = {
        **TestVanillaGlowbos.options,
        **HardTricksLogic.options,
    }


class TestVanillaGlowbosGlitches(TestVanillaGlowbos, GlitchesLogic):
    options = {
        **TestVanillaGlowbos.options,
        **GlitchesLogic.options,
    }
