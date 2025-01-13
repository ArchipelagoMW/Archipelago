from . import BanjoTooieTestBase
from ..Names import locationName, itemName, regionName
from .. import all_item_table, all_group_table

class AdvMoves(BanjoTooieTestBase):
    def item_pool(self) -> None:
        adv_move_count = len(self.world.item_name_groups["Moves"])
        adv_count = 0

        for adv_move in self.world.item_name_groups["Moves"]:
            for item in self.world.multiworld.itempool:
                if adv_move == item.name:
                    adv_count += 1

        assert adv_move_count == adv_count

    def disabled_item_pool(self) -> None:
        adv_count = 0

        for adv_move in self.world.item_name_groups["Moves"]:
            for item in self.world.multiworld.itempool:
                if adv_move == item.name:
                    print(f"Item: {adv_move} Should be here!")
                    adv_count += 1

        assert 0 == adv_count

    def prefills(self) -> None:
        adv_items = 0
        placed_correctly = 0
        for name in self.world.item_name_groups["Moves"]:
            adv_items += 1
            banjoItem = all_item_table.get(name)
            try:
                location_item = self.multiworld.get_location(banjoItem.default_location, self.player).item.name
                if location_item == name:
                    placed_correctly += 1
            except:
                print(f"Issue with Item: {name} Please Investigate")
                placed_correctly += 0
        assert adv_items == placed_correctly


class TestAdvMovesEnabledEasy(AdvMoves):
    options = {
        'randomized_moves': 'true',
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

class TestAdvMovesEnabledNormal(AdvMoves):
    options = {
        'randomized_moves': 'true',
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

class TestAdvMovesEnabledAdvance(AdvMoves):
    options = {
        'randomized_moves': 'true',
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

class TestAdvMovesEnabledGitch(AdvMoves):
    options = {
        'randomized_moves': 'true',
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


class TestAdvMovesDisabledEasy(AdvMoves):
    options = {
        'randomize_moves': 'false',
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

class TestAdvMovesDisabledNormal(AdvMoves):
    options = {
        'randomize_moves': 'false',
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

class TestAdvMovesDisabledAdvance(AdvMoves):
    options = {
        'randomize_moves': 'false',
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

class TestAdvMovesDisabledGlitch(AdvMoves):
    options = {
        'randomize_moves': 'false',
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
