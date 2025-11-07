from ..Options import LogicType, RandomizeBKMoveList, RandomizeNotes
from . import BanjoTooieTestBase
from .. import all_group_table


class BKMovesAll(BanjoTooieTestBase):
    options = {
        "randomize_bk_moves": RandomizeBKMoveList.option_all,
        "randomize_notes": RandomizeNotes(True)
    }

    def test_item_pool(self) -> None:
        bk_moves_count = len(all_group_table["bk_moves"])
        bk_count = 0
        for name, move in all_group_table["bk_moves"].items():
            if move.btid == self.world.starting_egg or move.btid == self.world.starting_attack:
                bk_count += 1
                continue
            for item in self.world.multiworld.itempool:
                if name == item.name:
                    bk_count += 1
        assert bk_moves_count == bk_count


class BKMovesMcJiggy(BanjoTooieTestBase):
    options = {
        "randomize_bk_moves": RandomizeBKMoveList.option_mcjiggy_special,
        "randomize_notes": RandomizeNotes(True)
    }

    def test_item_pool(self) -> None:
        bk_moves_count = len(all_group_table["bk_moves"])
        bk_count = 0
        for name, move in all_group_table["bk_moves"].items():
            if move.btid == 1230815 or move.btid == 1230816:  # Talon Trot and Tall Jump
                bk_moves_count -= 1  # Not in the pool
            if move.btid == self.world.starting_egg or move.btid == self.world.starting_attack:
                bk_count += 1
                continue
            for item in self.world.multiworld.itempool:
                if name == item.name:
                    bk_count += 1
        assert bk_moves_count == bk_count


class BKMovesDisabled(BanjoTooieTestBase):
    options = {
        "randomize_bk_moves": RandomizeBKMoveList.option_none
    }

    def test_not_in_pool(self) -> None:
        bk_count = 0
        for name, move in all_group_table["bk_moves"].items():
            for item in self.world.multiworld.itempool:
                if name == item.name:
                    bk_count += 1
        assert 0 == bk_count


class TestBKMovesAllIntended(BKMovesAll):
    options = {
        **BKMovesAll.options,
        "logic_type": LogicType.option_intended,
    }


class TestBKMovesAllEasyTricks(BKMovesAll):
    options = {
        **BKMovesAll.options,
        "logic_type": LogicType.option_easy_tricks,
    }


class TestBKMovesAllHardTricks(BKMovesAll):
    options = {
        **BKMovesAll.options,
        "logic_type": LogicType.option_hard_tricks,
    }


class TestBKMovesAllGlitchesTricks(BKMovesAll):
    options = {
        **BKMovesAll.options,
        "logic_type": LogicType.option_glitches
    }


class TestBKMovesMcJiggyIntended(BKMovesMcJiggy):
    options = {
        **BKMovesMcJiggy.options,
        "logic_type": LogicType.option_intended
    }


class TestBKMovesMcJiggyEasyTricks(BKMovesMcJiggy):
    options = {
        **BKMovesMcJiggy.options,
        "logic_type": LogicType.option_easy_tricks,
    }


class TestBKMovesMcJiggyHardTricks(BKMovesMcJiggy):
    options = {
        **BKMovesMcJiggy.options,
        "logic_type": LogicType.option_hard_tricks
    }


class TestBKMovesMcJiggyGlitchesTricks(BKMovesMcJiggy):
    options = {
        **BKMovesMcJiggy.options,
        "logic_type": LogicType.option_glitches
    }


class TestBKMovesDisabledIntended(BKMovesDisabled):
    options = {
        **BKMovesDisabled.options,
        "logic_type": LogicType.option_intended,
    }


class TestBKMovesDisabledEasyTricks(BKMovesDisabled):
    options = {
        **BKMovesDisabled.options,
        "logic_type": LogicType.option_easy_tricks,
    }


class TestBKMovesDisabledHardTricks(BKMovesDisabled):
    options = {
        **BKMovesDisabled.options,
        "logic_type": LogicType.option_hard_tricks
    }


class TestBKMovesDisabledGlitchesTricks(BKMovesDisabled):
    options = {
        **BKMovesDisabled.options,
        "logic_type": LogicType.option_glitches
    }
