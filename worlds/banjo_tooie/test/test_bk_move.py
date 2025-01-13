from . import BanjoTooieTestBase
from ..Names import locationName, itemName, regionName
from .. import all_item_table, all_group_table

class BKMoves(BanjoTooieTestBase):

    def item_pool(self) -> None:
        bk_moves_count = len(all_group_table["bk_moves"])
        bk_count = 0
        for name, move in all_group_table["bk_moves"].items():
            if (move.btid == 1230815 or move.btid == 1230816) and self.world.options.randomize_bk_moves == 1:
                bk_moves_count -= 1 #Not in the pool
            if move.btid == self.world.starting_egg or move.btid == self.world.starting_attack:
                bk_count += 1
                continue
            for item in self.world.multiworld.itempool:
                if name == item.name:
                    bk_count += 1
        assert bk_moves_count == bk_count

    def not_in_pool(self) -> None:
        bk_count = 0
        for name, move in all_group_table["bk_moves"].items():
            for item in self.world.multiworld.itempool:
                if name == item.name:
                    bk_count += 1
        assert 0 == bk_count


class TestBKMovesALLEnabledEasy(BKMoves):
    options = {
        'randomize_bk_moves': 2,
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

class TestBKMovesALLEnabledNormal(BKMoves):
    options = {
        'randomize_bk_moves': 2,
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

class TestBKMovesALLEnabledAdvance(BKMoves):
    options = {
        'randomize_bk_moves': 2,
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

class TestBKMovesALLEnabledGlitch(BKMoves):
    options = {
        'randomize_bk_moves': 2,
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


class TestBKMovesMcJiggyEnabledEasy(BKMoves):
    options = {
        'randomize_bk_moves': 1,
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

class TestBKMovesMcJiggyEnabledNormal(BKMoves):
    options = {
        'randomize_bk_moves': 1,
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

class TestBKMovesMcJiggyEnabledAdvance(BKMoves):
    options = {
        'randomize_bk_moves': 1,
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

class TestBKMovesMcJiggyEnabledGlitch(BKMoves):
    options = {
        'randomize_bk_moves': 1,
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


class TestBKMovesDisabledEasy(BKMoves):
    options = {
        'randomize_bk_moves': 0,
        'logic_type': 0
    }
    def test_item_pool(self) -> None:
        super().not_in_pool()
    def test_all_state_can_reach_everything(self):
        return super().test_all_state_can_reach_everything()
    def test_empty_state_can_reach_something(self):
        return super().test_empty_state_can_reach_something()
    def test_fill(self):
        return super().test_fill()

class TestBKMovesDisabledNormal(BKMoves):
    options = {
        'randomize_bk_moves': 0,
        'logic_type': 1
    }
    def test_item_pool(self) -> None:
        super().not_in_pool()
    def test_all_state_can_reach_everything(self):
        return super().test_all_state_can_reach_everything()
    def test_empty_state_can_reach_something(self):
        return super().test_empty_state_can_reach_something()
    def test_fill(self):
        return super().test_fill()

class TestBKMovesDisabledAdvance(BKMoves):
    options = {
        'randomize_bk_moves': 0,
        'logic_type': 2
    }
    def test_item_pool(self) -> None:
        super().not_in_pool()
    def test_all_state_can_reach_everything(self):
        return super().test_all_state_can_reach_everything()
    def test_empty_state_can_reach_something(self):
        return super().test_empty_state_can_reach_something()
    def test_fill(self):
        return super().test_fill()

class TestBKMovesDisabledGlitch(BKMoves):
    options = {
        'randomize_bk_moves': 0,
        'logic_type': 3
    }
    def test_item_pool(self) -> None:
        super().not_in_pool()
    def test_all_state_can_reach_everything(self):
        return super().test_all_state_can_reach_everything()
    def test_empty_state_can_reach_something(self):
        return super().test_empty_state_can_reach_something()
    def test_fill(self):
        return super().test_fill()
