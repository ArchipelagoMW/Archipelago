from . import BanjoTooieTestBase
from ..Names import locationName, itemName, regionName
from .. import all_item_table, all_group_table

class AdvMoves(BanjoTooieTestBase):
    def _item_pool(self) -> None:
        adv_move_count = len(self.world.item_name_groups["Moves"])
        adv_count = 0

        for adv_move in self.world.item_name_groups["Moves"]:
            for item in self.world.multiworld.itempool:
                if adv_move == item.name:
                    adv_count += 1

        assert adv_move_count == adv_count

    def _disabled_item_pool(self) -> None:
        adv_count = 0

        for adv_move in self.world.item_name_groups["Moves"]:
            for item in self.world.multiworld.itempool:
                if adv_move == item.name:
                    print(f"Item: {adv_move} Should be here!")
                    adv_count += 1

        assert 0 == adv_count

    def _prefills(self) -> None:
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
        super()._item_pool()

class TestAdvMovesEnabledNormal(AdvMoves):
    options = {
        'randomized_moves': 'true',
        'logic_type': 1
    }
    def test_item_pool(self) -> None:
        super()._item_pool()

class TestAdvMovesEnabledAdvance(AdvMoves):
    options = {
        'randomized_moves': 'true',
        'logic_type': 2
    }
    def test_item_pool(self) -> None:
        super()._item_pool()

class TestAdvMovesEnabledGitch(AdvMoves):
    options = {
        'randomized_moves': 'true',
        'logic_type': 3
    }
    def test_item_pool(self) -> None:
        super()._item_pool()


class TestAdvMovesDisabledEasy(AdvMoves):
    options = {
        'randomize_moves': 'false',
        'logic_type': 0
    }
    def test_disabled_item_pool(self) -> None:
        super()._disabled_item_pool()
    def test_prefills(self) -> None:
        super()._prefills()

class TestAdvMovesDisabledNormal(AdvMoves):
    options = {
        'randomize_moves': 'false',
        'logic_type': 1
    }
    def test_disabled_item_pool(self) -> None:
        super()._disabled_item_pool()
    def test_prefills(self) -> None:
        super()._prefills()

class TestAdvMovesDisabledAdvance(AdvMoves):
    options = {
        'randomize_moves': 'false',
        'logic_type': 2
    }
    def test_disabled_item_pool(self) -> None:
        super()._disabled_item_pool()
    def test_prefills(self) -> None:
        super()._prefills()

class TestAdvMovesDisabledGlitch(AdvMoves):
    options = {
        'randomize_moves': 'false',
        'logic_type': 3
    }
    def test_disabled_item_pool(self) -> None:
        super()._disabled_item_pool()
    def test_prefills(self) -> None:
        super()._prefills()
