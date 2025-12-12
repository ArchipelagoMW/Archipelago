from ..Names import itemName, locationName
from ..Options import RandomizeChuffyTrain, RandomizeTrainStationSwitches
from ..Items import stations_table
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from . import BanjoTooieTestBase


class TestRandomizedChuffy(BanjoTooieTestBase):
    options = {
        "randomize_chuffy": RandomizeChuffyTrain.option_true,
    }

    def test_item_pool(self) -> None:
        assert itemName.CHUFFY in [item.name for item in self.multiworld.itempool]


class TestVanillaChuffy(BanjoTooieTestBase):
    options = {
        "randomize_chuffy": RandomizeChuffyTrain.option_false
    }

    def test_item_pool(self) -> None:
        assert itemName.CHUFFY not in [item.name for item in self.multiworld.itempool]

    def test_prefill(self) -> None:
        chuffy_location = [location for location in self.world.get_locations()
                           if location.name == locationName.CHUFFY][0]
        assert chuffy_location.item.name == itemName.CHUFFY


class TestRandomizedTrainSwitches(BanjoTooieTestBase):
    options = {
        "randomize_stations": RandomizeTrainStationSwitches.option_true,
    }

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        for station_name in stations_table.keys():
            assert station_name in item_pool_names


class TestVanillaTrainSwitches(BanjoTooieTestBase):
    options = {
        "randomize_stations": RandomizeTrainStationSwitches.option_false,
    }

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        for station_name in stations_table.keys():
            assert station_name not in item_pool_names

    def test_prefill(self) -> None:
        vanilla_locations = {item_name: item_data.default_location for item_name, item_data in stations_table.items()}
        for location in self.world.get_locations():
            if location.name in vanilla_locations.values():
                assert vanilla_locations[location.item.name] == location.name

# for this one, the logic is so coupled together that it makes sense to test Chuffy and train switches at the same time.


class TestRandomizedChuffyRandomizedTrainSwitchesIntended(TestRandomizedChuffy,
                                                          TestRandomizedTrainSwitches, IntendedLogic):
    options = {
        **TestRandomizedChuffy.options,
        **TestRandomizedTrainSwitches.options,
        **IntendedLogic.options,
    }


class TestRandomizedChuffyRandomizedTrainSwitchesEasyTricks(TestRandomizedChuffy,
                                                            TestRandomizedTrainSwitches, EasyTricksLogic):
    options = {
        **TestRandomizedChuffy.options,
        **TestRandomizedTrainSwitches.options,
        **EasyTricksLogic.options,
    }


class TestRandomizedChuffyRandomizedTrainSwitchesHardTricks(TestRandomizedChuffy,
                                                            TestRandomizedTrainSwitches, HardTricksLogic):
    options = {
        **TestRandomizedChuffy.options,
        **TestRandomizedTrainSwitches.options,
        **HardTricksLogic.options,
    }


class TestRandomizedChuffyRandomizedTrainSwitchesGlitches(TestRandomizedChuffy,
                                                          TestRandomizedTrainSwitches, GlitchesLogic):
    options = {
        **TestRandomizedChuffy.options,
        **TestRandomizedTrainSwitches.options,
        **GlitchesLogic.options,
    }


class TestVanillaChuffyRandomizedTrainSwitchesIntended(TestVanillaChuffy, TestRandomizedTrainSwitches, IntendedLogic):
    options = {
        **TestVanillaChuffy.options,
        **TestRandomizedTrainSwitches.options,
        **IntendedLogic.options,
    }


class TestVanillaChuffyRandomizedTrainSwitchesEasyTricks(TestVanillaChuffy,
                                                         TestRandomizedTrainSwitches, EasyTricksLogic):
    options = {
        **TestVanillaChuffy.options,
        **TestRandomizedTrainSwitches.options,
        **EasyTricksLogic.options,
    }


class TestVanillaChuffyRandomizedTrainSwitchesHardTricks(TestVanillaChuffy,
                                                         TestRandomizedTrainSwitches, HardTricksLogic):
    options = {
        **TestVanillaChuffy.options,
        **TestRandomizedTrainSwitches.options,
        **HardTricksLogic.options,
    }


class TestVanillaChuffyRandomizedTrainSwitchesGlitches(TestVanillaChuffy, TestRandomizedTrainSwitches, GlitchesLogic):
    options = {
        **TestVanillaChuffy.options,
        **TestRandomizedTrainSwitches.options,
        **GlitchesLogic.options,
    }


class TestVanillaChuffyVanillaTrainSwitchesIntended(TestVanillaChuffy, TestVanillaTrainSwitches, IntendedLogic):
    options = {
        **TestVanillaChuffy.options,
        **TestVanillaTrainSwitches.options,
        **IntendedLogic.options,
    }


class TestVanillaChuffyVanillaTrainSwitchesEasyTricks(TestVanillaChuffy, TestVanillaTrainSwitches, EasyTricksLogic):
    options = {
        **TestVanillaChuffy.options,
        **TestVanillaTrainSwitches.options,
        **EasyTricksLogic.options,
    }


class TestVanillaChuffyVanillaTrainSwitchesHardTricks(TestVanillaChuffy, TestVanillaTrainSwitches, HardTricksLogic):
    options = {
        **TestVanillaChuffy.options,
        **TestVanillaTrainSwitches.options,
        **HardTricksLogic.options,
    }


class TestVanillaChuffyVanillaTrainSwitchesGlitches(TestVanillaChuffy, TestVanillaTrainSwitches, GlitchesLogic):
    options = {
        **TestVanillaChuffy.options,
        **TestVanillaTrainSwitches.options,
        **GlitchesLogic.options,
    }


class TestRandomizedChuffyVanillaTrainSwitchesIntended(TestRandomizedChuffy, TestVanillaTrainSwitches, IntendedLogic):
    options = {
        **TestRandomizedChuffy.options,
        **TestVanillaTrainSwitches.options,
        **IntendedLogic.options,
    }


class TestRandomizedChuffyVanillaTrainSwitchesEasyTricks(TestRandomizedChuffy,
                                                         TestVanillaTrainSwitches, EasyTricksLogic):
    options = {
        **TestRandomizedChuffy.options,
        **TestVanillaTrainSwitches.options,
        **EasyTricksLogic.options,
    }


class TestRandomizedChuffyVanillaTrainSwitchesHardTricks(TestRandomizedChuffy,
                                                         TestVanillaTrainSwitches, HardTricksLogic):
    options = {
        **TestRandomizedChuffy.options,
        **TestVanillaTrainSwitches.options,
        **HardTricksLogic.options,
    }


class TestRandomizedChuffyVanillaTrainSwitchesGlitches(TestRandomizedChuffy, TestVanillaTrainSwitches, GlitchesLogic):
    options = {
        **TestRandomizedChuffy.options,
        **TestVanillaTrainSwitches.options,
        **GlitchesLogic.options,
    }
