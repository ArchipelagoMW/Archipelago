from . import BanjoTooieTestBase
from ..Names import locationName, itemName, regionName
from .. import all_item_table, all_group_table

class Treble(BanjoTooieTestBase):
    
    def item_pool(self) -> None:
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
    
    def disabled_item_pool(self) -> None:
        adv_count = 0
        for item in self.world.multiworld.itempool:
            if itemName.TREBLE == item.name:
                print(f"Item: {item.name} Should not be here!")
                adv_count += 1
        assert 0 == adv_count
    
    def prefills(self) -> None:
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
        super().item_pool()
    def test_all_state_can_reach_everything(self):
        return super().test_all_state_can_reach_everything()
    def test_empty_state_can_reach_something(self):
        return super().test_empty_state_can_reach_something()
    def test_fill(self):
        return super().test_fill()
    
class TestTrebleEnabledNormal(Treble):
    options = {
        'randomize_treble': 'true',
        'logic_type': 1
    }
    def test_item_pool(self) -> None:
        super().item_pool()
    def test_all_state_can_reach_everything(self):
        return super().test_all_state_can_reach_everything()
    def test_empty_state_can_reach_something(self):
        return super().test_empty_state_can_reach_something()
    def test_fill(self):
        return super().test_fill()
    
class TestTrebleEnabledAdvance(Treble):
    options = {
        'randomize_treble': 'true',
        'logic_type': 2
    }
    def test_item_pool(self) -> None:
        super().item_pool()
    def test_all_state_can_reach_everything(self):
        return super().test_all_state_can_reach_everything()
    def test_empty_state_can_reach_something(self):
        return super().test_empty_state_can_reach_something()
    def test_fill(self):
        return super().test_fill()
    
class TestTrebleEnabledGlitch(Treble):
    options = {
        'randomize_treble': 'true',
        'logic_type': 3
    }
    def test_item_pool(self) -> None:
        super().item_pool()
    def test_all_state_can_reach_everything(self):
        return super().test_all_state_can_reach_everything()
    def test_empty_state_can_reach_something(self):
        return super().test_empty_state_can_reach_something()
    def test_fill(self):
        return super().test_fill()
    

class TestTrebleDisabledEasy(Treble):
    options = {
        'randomize_treble': 'false',
        'logic_type': 0
    }
    def test_item_pool(self) -> None:
        super().disabled_item_pool()

    def test_prefills(self) -> None:
        super().prefills()
    def test_all_state_can_reach_everything(self):
        return super().test_all_state_can_reach_everything()
    def test_empty_state_can_reach_something(self):
        return super().test_empty_state_can_reach_something()
    def test_fill(self):
        return super().test_fill()
    
class TestTrebleDisabledNormal(Treble):
    options = {
        'randomize_treble': 'false',
        'logic_type': 1
    }
    def test_item_pool(self) -> None:
        super().disabled_item_pool()

    def test_prefills(self) -> None:
        super().prefills()
    def test_all_state_can_reach_everything(self):
        return super().test_all_state_can_reach_everything()
    def test_empty_state_can_reach_something(self):
        return super().test_empty_state_can_reach_something()
    def test_fill(self):
        return super().test_fill()
    
class TestTrebleDisabledAdvance(Treble):
    options = {
        'randomize_treble': 'false',
        'logic_type': 2
    }
    def test_item_pool(self) -> None:
        super().disabled_item_pool()

    def test_prefills(self) -> None:
        super().prefills()
    def test_all_state_can_reach_everything(self):
        return super().test_all_state_can_reach_everything()
    def test_empty_state_can_reach_something(self):
        return super().test_empty_state_can_reach_something()
    def test_fill(self):
        return super().test_fill()

class TestTrebleDisabledGlitch(Treble):
    options = {
        'randomize_treble': 'false',
        'logic_type': 3
    }
    def test_item_pool(self) -> None:
        super().disabled_item_pool()

    def test_prefills(self) -> None:
        super().prefills()
    def test_all_state_can_reach_everything(self):
        return super().test_all_state_can_reach_everything()
    def test_empty_state_can_reach_something(self):
        return super().test_empty_state_can_reach_something()
    def test_fill(self):
        return super().test_fill()