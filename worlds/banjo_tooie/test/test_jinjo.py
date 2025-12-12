from ..Items import all_item_table
from ..Options import RandomizeJinjos
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from . import BanjoTooieTestBase
from ..Names import locationName, itemName


class JinjosEnabled(BanjoTooieTestBase):
    options = {
        "randomize_jinjos": RandomizeJinjos.option_true,
        "world_requirements": "custom",
        "custom_worlds": "1,1,1,1,1,1,1,1,51",  # add jingaling's jiggy
    }

    def test_item_pool_jinjos(self) -> None:
        jinjo_count = 0
        jinjo_counter = 0

        for jinjo in self.world.item_name_groups["Jinjo"]:
            banjoItem = all_item_table[jinjo]
            jinjo_count += banjoItem.qty
            for item in self.world.multiworld.itempool:
                if jinjo == item.name:
                    jinjo_counter += 1

        assert jinjo_count == jinjo_counter

    def test_item_pool_jiggies(self) -> None:
        assert [item.name for item in self.multiworld.itempool if item.advancement].count(itemName.JIGGY) == 55
        assert [item.name for item in self.multiworld.itempool if item.useful].count(itemName.JIGGY) == 15


class JinjosDisabled(BanjoTooieTestBase):
    options = {
        "randomize_jinjos": RandomizeJinjos.option_false,
        "world_requirements": "custom",
        "custom_worlds": "1,1,1,1,1,1,1,1,51",  # add jingaling's jiggy
    }

    def test_disabled_item_pool(self) -> None:
        jinjo_counter = 0

        for jinjo in self.world.item_name_groups["Jinjo"]:
            for item in self.world.multiworld.itempool:
                if jinjo == item.name:
                    print(f"Item: {jinjo} Should be here!")
                    jinjo_counter += 1

        assert 0 == jinjo_counter

    def test_prefills(self) -> None:
        def check_jinjo_locations(location_names: list[str], jinjo_name: str) -> bool:
            for location_name in location_names:
                location_item = self.multiworld.get_location(location_name, self.player).item.name
                if location_item != jinjo_name:
                    return False
            return True

        white_jinjo_locations = [locationName.JINJOJR5]
        orange_jinjo_locations = [locationName.JINJOWW4, locationName.JINJOHP2]
        yellow_jinjo_locations = [locationName.JINJOWW3, locationName.JINJOHP4, locationName.JINJOHP3]
        brown_jinjo_locations = [
            locationName.JINJOGM1,
            locationName.JINJOJR2,
            locationName.JINJOTL2,
            locationName.JINJOTL5,
        ]
        green_jinjo_locations = [
            locationName.JINJOWW5,
            locationName.JINJOJR1,
            locationName.JINJOTL4,
            locationName.JINJOGI2,
            locationName.JINJOHP1,
        ]
        red_jinjo_locations = [
            locationName.JINJOMT2,
            locationName.JINJOMT3,
            locationName.JINJOMT5,
            locationName.JINJOJR3,
            locationName.JINJOJR4,
            locationName.JINJOWW2,
        ]
        blue_jinjo_locations = [
            locationName.JINJOGM3,
            locationName.JINJOTL1,
            locationName.JINJOHP5,
            locationName.JINJOCC2,
            locationName.JINJOIH1,
            locationName.JINJOIH4,
            locationName.JINJOIH5,
        ]
        purple_jinjo_locations = [
            locationName.JINJOMT1,
            locationName.JINJOGM5,
            locationName.JINJOCC1,
            locationName.JINJOCC3,
            locationName.JINJOCC5,
            locationName.JINJOIH2,
            locationName.JINJOIH3,
            locationName.JINJOGI4,
        ]
        black_jinjo_locations = [
            locationName.JINJOMT4,
            locationName.JINJOGM2,
            locationName.JINJOGM4,
            locationName.JINJOWW1,
            locationName.JINJOTL3,
            locationName.JINJOGI1,
            locationName.JINJOGI5,
            locationName.JINJOCC4,
            locationName.JINJOGI3,
        ]
        assert check_jinjo_locations(white_jinjo_locations, itemName.WJINJO)
        assert check_jinjo_locations(orange_jinjo_locations, itemName.OJINJO)
        assert check_jinjo_locations(yellow_jinjo_locations, itemName.YJINJO)
        assert check_jinjo_locations(brown_jinjo_locations, itemName.BRJINJO)
        assert check_jinjo_locations(green_jinjo_locations, itemName.GJINJO)
        assert check_jinjo_locations(red_jinjo_locations, itemName.RJINJO)
        assert check_jinjo_locations(blue_jinjo_locations, itemName.BLJINJO)
        assert check_jinjo_locations(purple_jinjo_locations, itemName.PJINJO)
        assert check_jinjo_locations(black_jinjo_locations, itemName.BKJINJO)

    def test_item_pool_jiggies(self) -> None:
        assert [item.name for item in self.multiworld.itempool if item.advancement].count(itemName.JIGGY) == 46
        assert [item.name for item in self.multiworld.itempool if item.useful].count(itemName.JIGGY) == 15


class TestJinjosEnabledIntended(JinjosEnabled, IntendedLogic):
    options = {
        **JinjosEnabled.options,
        **IntendedLogic.options,
    }


class TestJinjosEnabledEasyTricks(JinjosEnabled, EasyTricksLogic):
    options = {
        **JinjosEnabled.options,
        **EasyTricksLogic.options,
    }


class TestJinjosEnabledHardTricks(JinjosEnabled, HardTricksLogic):
    options = {
        **JinjosEnabled.options,
        **HardTricksLogic.options,
    }


class TestJinjosEnabledGlitchesTricks(JinjosEnabled, GlitchesLogic):
    options = {
        **JinjosEnabled.options,
        **GlitchesLogic.options,
    }


class TestJinjosDisabledIntended(JinjosDisabled, IntendedLogic):
    options = {
        **JinjosDisabled.options,
        **IntendedLogic.options,
    }


class TestJinjosDisabledEasyTricks(JinjosDisabled, EasyTricksLogic):
    options = {
        **JinjosDisabled.options,
        **EasyTricksLogic.options,
    }


class TestJinjosDisabledHardTricks(JinjosDisabled, HardTricksLogic):
    options = {
        **JinjosDisabled.options,
        **HardTricksLogic.options,
    }


class TestJinjosDisabledGlitchesTricks(JinjosDisabled, GlitchesLogic):
    options = {
        **JinjosDisabled.options,
        **GlitchesLogic.options,
    }
