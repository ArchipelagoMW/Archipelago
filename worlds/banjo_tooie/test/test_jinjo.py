from ..Items import all_item_table
from ..Options import RandomizeJinjos
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from . import BanjoTooieTestBase
from ..Names import locationName, itemName

class JinjosEnabled(BanjoTooieTestBase):
    options = {
        "randomize_jinjos": RandomizeJinjos.option_true,
        "world_requirements": "custom",
        "custom_worlds": "1,1,1,1,1,1,1,1,51", # add jingaling's jiggy
    }
    def test_item_pool_jinjos(self) -> None:
        jinjo_count = 0
        jinjo_counter = 0

        for jinjo in self.world.item_name_groups["Jinjo"]:
            banjoItem = all_item_table.get(jinjo)
            jinjo_count += banjoItem.qty
            for item in self.world.multiworld.itempool:
                if jinjo == item.name:
                    jinjo_counter += 1

        assert jinjo_count == jinjo_counter

    def test_item_pool_jiggies(self) -> None:
        assert [item.name for item in self.multiworld.itempool if item.advancement].count(itemName.JIGGY) == 50
        assert [item.name for item in self.multiworld.itempool if item.useful].count(itemName.JIGGY) == 20

class JinjosDisabled(BanjoTooieTestBase):
    options = {
        "randomize_jinjos": RandomizeJinjos.option_false,
        "world_requirements": "custom",
        "custom_worlds": "1,1,1,1,1,1,1,1,51", # add jingaling's jiggy
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
        jinjos = 0
        placed_correctly = 0
        for name in self.world.item_name_groups["Jinjo"]:
            banjoItem = all_item_table.get(name)
            jinjos += banjoItem.qty
            try:
                location_item = ""
                if name == itemName.WJINJO:
                    location_item = self.multiworld.get_location(locationName.JINJOJR5, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                elif name == itemName.OJINJO:
                    location_item = self.multiworld.get_location(locationName.JINJOWW4, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOHP2, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                elif name == itemName.YJINJO:
                    location_item = self.multiworld.get_location(locationName.JINJOWW3, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOHP4, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOHP3, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                elif name == itemName.BRJINJO:
                    location_item = self.multiworld.get_location(locationName.JINJOGM1, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOJR2, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOTL2, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOTL5, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                elif name == itemName.GJINJO:
                    location_item = self.multiworld.get_location(locationName.JINJOWW5, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOJR1, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOTL4, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOGI2, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOHP1, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                elif name == itemName.RJINJO:
                    location_item = self.multiworld.get_location(locationName.JINJOMT2, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOMT3, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOMT5, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOJR3, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOJR4, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOWW2, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                elif name == itemName.BLJINJO:
                    location_item = self.multiworld.get_location(locationName.JINJOGM3, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOTL1, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOHP5, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOCC2, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOIH1, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOIH4, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOIH5, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                elif name == itemName.PJINJO:
                    location_item = self.multiworld.get_location(locationName.JINJOMT1, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOGM5, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOCC1, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOCC3, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOCC5, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOIH2, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOIH3, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOGI4, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                elif name == itemName.BKJINJO:
                    location_item = self.multiworld.get_location(locationName.JINJOMT4, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOGM2, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOGM4, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOWW1, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOTL3, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOGI1, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOGI5, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOCC4, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
                    location_item = self.multiworld.get_location(locationName.JINJOGI3, self.player).item.name
                    if location_item == name:
                        placed_correctly += 1
            except:
                print(f"Issue with Item: {name} Please Investigate")
                placed_correctly += 0
        assert jinjos == placed_correctly

    def test_item_pool_jiggies(self) -> None:
        assert [item.name for item in self.multiworld.itempool if item.advancement].count(itemName.JIGGY) == 41
        assert [item.name for item in self.multiworld.itempool if item.useful].count(itemName.JIGGY) == 20

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
