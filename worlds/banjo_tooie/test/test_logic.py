from ..Options import LogicType, RandomizeBKMoveList, RandomizeBTMoveList, RandomizeNotes

# Many tests inherit from logic tests, to make sure that the logic of all collectibles works.


class IntendedLogic:
    options = {
        "logic_type": LogicType.option_intended,
        "randomize_bt_moves": RandomizeBTMoveList.option_true,
        "randomize_bk_moves": RandomizeBKMoveList.option_all,
        "randomize_notes": RandomizeNotes.option_true,
    }


class IntendedLogicNoBKShuffle:
    options = {
        "logic_type": LogicType.option_intended,
        "randomize_bt_moves": RandomizeBTMoveList.option_true,
    }


class EasyTricksLogic:
    options = {
        "logic_type": LogicType.option_easy_tricks,
        "randomize_bt_moves": RandomizeBTMoveList.option_true,
        "randomize_bk_moves": RandomizeBKMoveList.option_all,
        "randomize_notes": RandomizeNotes.option_true,
    }


class EasyTricksLogicNoBKShuffle:
    options = {
        "logic_type": LogicType.option_easy_tricks,
        "randomize_bt_moves": RandomizeBTMoveList.option_true,
    }


class HardTricksLogic:
    options = {
        "logic_type": LogicType.option_hard_tricks,
        "randomize_bt_moves": RandomizeBTMoveList.option_true,
        "randomize_bk_moves": RandomizeBKMoveList.option_all,
        "randomize_notes": RandomizeNotes.option_true,
    }


class HardTricksLogicNoBKShuffle:
    options = {
        "logic_type": LogicType.option_hard_tricks,
        "randomize_bt_moves": RandomizeBTMoveList.option_true,
    }


class GlitchesLogic:
    options = {
        "logic_type": LogicType.option_glitches,
        "randomize_bt_moves": RandomizeBTMoveList.option_true,
        "randomize_bk_moves": RandomizeBKMoveList.option_all,
        "randomize_notes": RandomizeNotes.option_true,
    }


class GlitchesLogicNoBKShuffle:
    options = {
        "logic_type": LogicType.option_glitches,
        "randomize_bt_moves": RandomizeBTMoveList.option_true,
    }
