from worlds.banjo_tooie.Items import BanjoTooieItem, all_item_table
from . import BanjoTooieTestBase
from ..Names import locationName, itemName, regionName

class Jinjo(BanjoTooieTestBase):

    def _item_pool(self) -> None:
        jinjo_count = 0
        jinjo_counter = 0

        for jinjo in self.world.item_name_groups["Jinjo"]:
            banjoItem = all_item_table.get(jinjo)
            jinjo_count += banjoItem.qty
            for item in self.world.multiworld.itempool:
                if jinjo == item.name:
                    jinjo_counter += 1

        assert jinjo_count == jinjo_counter

    def _disabled_item_pool(self) -> None:
        jinjo_counter = 0

        for jinjo in self.world.item_name_groups["Jinjo"]:
            for item in self.world.multiworld.itempool:
                if jinjo == item.name:
                    print(f"Item: {jinjo} Should be here!")
                    jinjo_counter += 1

        assert 0 == jinjo_counter

    def _prefills(self) -> None:
        jinjos = 0
        placed_correctly = 0
        for name in self.world.item_name_groups["Jinjo"]:
            banjoItem = all_item_table.get(name)
            jinjos += banjoItem.qty
            try:
                location_item = ''
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


class TestJinjoEnabledEasy(Jinjo):
    options = {
        'randomize_jinjos': 'true',
        'logic_type': 0
    }
    def test_item_pool(self) -> None:
        super()._item_pool()


class TestJinjoEnabledNormal(Jinjo):
    options = {
        'randomize_jinjos': 'true',
        'logic_type': 1
    }
    def test_item_pool(self) -> None:
        super()._item_pool()


class TestJinjoEnabledAdvance(Jinjo):
    options = {
        'randomize_jinjos': 'true',
        'logic_type': 2
    }
    def test_item_pool(self) -> None:
        super()._item_pool()


class TestJinjoEnabledGitch(Jinjo):
    options = {
        'randomize_jinjos': 'true',
        'logic_type': 3
    }
    def test_item_pool(self) -> None:
        super()._item_pool()



class TestJinjoDisabledEasy(Jinjo):
    options = {
        'randomize_jinjos': 'false',
        'logic_type': 0
    }
    def test_disabled_item_pool(self) -> None:
        super()._disabled_item_pool()

    def test_prefills(self) -> None:
        super()._prefills()


class TestJinjoDisabledNormal(Jinjo):
    options = {
        'randomize_jinjos': 'false',
        'logic_type': 1
    }
    def test_disabled_item_pool(self) -> None:
        super()._disabled_item_pool()

    def test_prefills(self) -> None:
        super()._prefills()


class TestJinjoDisabledAdvance(Jinjo):
    options = {
        'randomize_jinjos': 'false',
        'logic_type': 2
    }
    def test_disabled_item_pooll(self) -> None:
        super()._disabled_item_pool()

    def test_prefills(self) -> None:
        super()._prefills()


class TestJinjoDisabledGlitch(Jinjo):
    options = {
        'randomize_jinjos': 'false',
        'logic_type': 3
    }
    def test_disabled_item_pool(self) -> None:
        super()._disabled_item_pool()

    def test_prefills(self) -> None:
        super()._prefills()

