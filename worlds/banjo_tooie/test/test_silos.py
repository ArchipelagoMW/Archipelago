from ..Options import RandomizeSilos, OpenSilos
from ..Items import silo_table
from ..Locations import all_location_table
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from . import BanjoTooieTestBase


class TestRandomizedClosedSilos(BanjoTooieTestBase):
    options = {
        "randomize_silos": RandomizeSilos.option_true,
        "open_silos": 0
    }

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        for silo_name in silo_table.keys():
            assert silo_name in item_pool_names


class TestRandomizedOpenSilos(BanjoTooieTestBase):
    options = {
        "randomize_silos": RandomizeSilos.option_true,
        "open_silos": OpenSilos.range_end
    }

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        for silo_name in silo_table.keys():
            assert silo_name not in item_pool_names

    def test_starting_inventory(self) -> None:
        precollected_item_names = [item.name for item in self.multiworld.precollected_items[self.world.player]]
        for silo_name in silo_table.keys():
            assert silo_name in precollected_item_names


class TestVanillaClosedSilos(BanjoTooieTestBase):
    options = {
        "randomize_silos": RandomizeSilos.option_false,
        "open_silos": 0
    }

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        for silo_name in silo_table.keys():
            assert silo_name not in item_pool_names

    def test_prefills(self) -> None:
        vanilla_locations_names = [location_name for location_name, location_data in all_location_table.items()
                                   if location_data.group == "Silos"]
        vanilla_locations = [location for location in self.world.get_locations()
                             if location.name in vanilla_locations_names]

        assert len(vanilla_locations) == 0


class TestVanillaOpenSilos(BanjoTooieTestBase):
    options = {
        "randomize_silos": RandomizeSilos.option_false,
        "open_silos": OpenSilos.range_end
    }

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        for silo_name in silo_table.keys():
            assert silo_name not in item_pool_names

    def test_locations(self) -> None:
        vanilla_locations_names = [location_name for location_name, location_data in all_location_table.items()
                                   if location_data.group == "Silos"]
        vanilla_locations = [location for location in self.world.get_locations()
                             if location.name in vanilla_locations_names]
        assert len(vanilla_locations) == 0


class TestRandomizedClosedSilosIntended(TestRandomizedClosedSilos, IntendedLogic):
    options = {
        **TestRandomizedClosedSilos.options,
        **IntendedLogic.options,
    }


class TestRandomizedClosedSilosEasyTricks(TestRandomizedClosedSilos, EasyTricksLogic):
    options = {
        **TestRandomizedClosedSilos.options,
        **EasyTricksLogic.options,
    }


class TestRandomizedClosedSilosHardTricks(TestRandomizedClosedSilos, HardTricksLogic):
    options = {
        **TestRandomizedClosedSilos.options,
        **HardTricksLogic.options,
    }


class TestRandomizedClosedSilosGlitches(TestRandomizedClosedSilos, GlitchesLogic):
    options = {
        **TestRandomizedClosedSilos.options,
        **GlitchesLogic.options,
    }


class TestVanillaClosedSilosIntended(TestVanillaClosedSilos, IntendedLogic):
    options = {
        **TestVanillaClosedSilos.options,
        **IntendedLogic.options,
    }


class TestVanillaClosedSilosEasyTricks(TestVanillaClosedSilos, EasyTricksLogic):
    options = {
        **TestVanillaClosedSilos.options,
        **EasyTricksLogic.options,
    }


class TestVanillaClosedSilosHardTricks(TestVanillaClosedSilos, HardTricksLogic):
    options = {
        **TestVanillaClosedSilos.options,
        **HardTricksLogic.options,
    }


class TestVanillaClosedSilosGlitches(TestVanillaClosedSilos, GlitchesLogic):
    options = {
        **TestVanillaClosedSilos.options,
        **GlitchesLogic.options,
    }


class TestRandomizedOpenSilosIntended(TestRandomizedOpenSilos, IntendedLogic):
    options = {
        **TestRandomizedOpenSilos.options,
        **IntendedLogic.options,
    }


class TestRandomizedOpenSilosEasyTricks(TestRandomizedOpenSilos, EasyTricksLogic):
    options = {
        **TestRandomizedOpenSilos.options,
        **EasyTricksLogic.options,
    }


class TestRandomizedOpenSilosHardTricks(TestRandomizedOpenSilos, HardTricksLogic):
    options = {
        **TestRandomizedOpenSilos.options,
        **HardTricksLogic.options,
    }


class TestRandomizedOpenSilosGlitches(TestRandomizedOpenSilos, GlitchesLogic):
    options = {
        **TestRandomizedOpenSilos.options,
        **GlitchesLogic.options,
    }


class TestVanillaOpenSilosIntended(TestVanillaOpenSilos, IntendedLogic):
    options = {
        **TestVanillaOpenSilos.options,
        **IntendedLogic.options,
    }


class TestVanillaOpenSilosEasyTricks(TestVanillaOpenSilos, EasyTricksLogic):
    options = {
        **TestVanillaOpenSilos.options,
        **EasyTricksLogic.options,
    }


class TestVanillaOpenSilosHardTricks(TestVanillaOpenSilos, HardTricksLogic):
    options = {
        **TestVanillaOpenSilos.options,
        **HardTricksLogic.options,
    }


class TestVanillaOpenSilosGlitches(TestVanillaOpenSilos, GlitchesLogic):
    options = {
        **TestVanillaOpenSilos.options,
        **GlitchesLogic.options,
    }
