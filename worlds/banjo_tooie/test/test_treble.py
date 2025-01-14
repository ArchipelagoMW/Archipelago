from . import BanjoTooieTestBase
from ..Names import locationName, itemName, regionName
from .. import all_item_table, all_group_table

class Treble(BanjoTooieTestBase):

    def _item_pool(self) -> None:
        treble_amt = 0
        treble_count = 0
        for name, btitem in all_group_table["misc"].items():
            if name == itemName.TREBLE:
                treble_amt = btitem.qty
                break

        for item in self.world.multiworld.itempool:
            if itemName.TREBLE == item.name:
                    treble_count += 1
        assert treble_amt == treble_count

    def _disabled_item_pool(self) -> None:
        adv_count = 0
        for item in self.world.multiworld.itempool:
            if itemName.TREBLE == item.name:
                print(f"Item: {item.name} Should not be here!")
                adv_count += 1
        assert 0 == adv_count

    def _prefills(self) -> None:
        treble_amt = 0
        treble_count = 0
        for name, btitem in all_group_table["misc"].items():
            if name == itemName.TREBLE:
                treble_amt = btitem.qty
                break

        for name, id in self.world.location_name_to_id.items():
            if name.find(itemName.TREBLE) != -1:
                try:
                    location_item = self.multiworld.get_location(name, self.player).item.name
                    if location_item == itemName.TREBLE:
                        treble_count += 1
                except:
                    print(f"Issue with Item: {name} Please Investigate")
                    treble_count += 0
        assert treble_amt == treble_count


class TestTrebleEnabledEasy(Treble):
    options = {
        'randomize_treble': 'true',
        'logic_type': 0
    }
    def test_item_pool(self) -> None:
        super()._item_pool()


class TestTrebleEnabledNormal(Treble):
    options = {
        'randomize_treble': 'true',
        'logic_type': 1
    }
    def test_item_pool(self) -> None:
        super()._item_pool()


class TestTrebleEnabledAdvance(Treble):
    options = {
        'randomize_treble': 'true',
        'logic_type': 2
    }
    def test_item_pool(self) -> None:
        super()._item_pool()


class TestTrebleEnabledGlitch(Treble):
    options = {
        'randomize_treble': 'true',
        'logic_type': 3
    }
    def test_item_pool(self) -> None:
        super()._item_pool()



class TestTrebleDisabledEasy(Treble):
    options = {
        'randomize_treble': 'false',
        'logic_type': 0
    }
    def test_disabled_item_pool(self) -> None:
        super()._disabled_item_pool()

    def test_prefills(self) -> None:
        super()._prefills()


class TestTrebleDisabledNormal(Treble):
    options = {
        'randomize_treble': 'false',
        'logic_type': 1
    }
    def test_disabled_item_pool(self) -> None:
        super()._disabled_item_pool()

    def test_prefills(self) -> None:
        super()._prefills()


class TestTrebleDisabledAdvance(Treble):
    options = {
        'randomize_treble': 'false',
        'logic_type': 2
    }
    def test_disabled_item_pool(self) -> None:
        super()._disabled_item_pool()

    def test_prefills(self) -> None:
        super()._prefills()


class TestTrebleDisabledGlitch(Treble):
    options = {
        'randomize_treble': 'false',
        'logic_type': 3
    }
    def test_disabled_item_pool(self) -> None:
        super()._disabled_item_pool()

    def test_prefills(self) -> None:
        super()._prefills()

