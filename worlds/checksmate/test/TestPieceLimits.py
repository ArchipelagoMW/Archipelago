from copy import copy

from . import CMTestBase
from .. import Options
from ..PieceLimitCascade import PieceLimitCascade


# I don't like that this generates many entire seeds just to check some global logic.
# TODO(chesslogic): Convert as much of this as possible to use test.bases, not WorldTestBase.

# TODO(chesslogic): find_piece_limit should accept an army option value. Store piece distribution on some other helper


class PieceLimitTestBase(CMTestBase):
    NO_CHILDREN = PieceLimitCascade.NO_CHILDREN
    ACTUAL_CHILDREN = PieceLimitCascade.ACTUAL_CHILDREN
    POTENTIAL_CHILDREN = PieceLimitCascade.POTENTIAL_CHILDREN

    def world_setup(self, *args, **kwargs) -> None:
        self.options = copy(self.options)
        super().world_setup(*args, **kwargs)

    def assert_matches(self, expected_minors: int, expected_majors: int, expected_queens: int) -> None:
        self.assertEqual(0, self.world.find_piece_limit("Progressive Pawn", self.NO_CHILDREN
                                                        ))
        self.assertEqual(expected_minors, self.world.find_piece_limit("Progressive Minor Piece", self.NO_CHILDREN
                                                                      ))
        self.assertEqual(expected_majors, self.world.find_piece_limit("Progressive Major Piece", self.NO_CHILDREN
                                                                      ))
        self.assertEqual(expected_queens, self.world.find_piece_limit("Progressive Major To Queen", self.NO_CHILDREN
                                                                      ))

    def assert_actuals(self, expected_majors, expected_queens) -> None:
        actual_queens = self.world.items_used[self.player].get("Progressive Major To Queen", 0)
        self.assertEqual(expected_majors + actual_queens,
                         self.world.find_piece_limit("Progressive Major Piece", self.ACTUAL_CHILDREN))
        self.assertEqual(expected_majors + expected_queens,
                         self.world.find_piece_limit("Progressive Major Piece", self.POTENTIAL_CHILDREN))


class TestChaosPieceLimits(PieceLimitTestBase):
    def world_setup(self, *args, **kwargs) -> None:
        self.options = copy(self.options)
        self.options["fairy_chess_army"] = Options.FairyChessArmy.option_chaos
        super().world_setup(*args, **kwargs)

    def test_no_options(self) -> None:
        # self.options["fairy_chess_army"] = "chaos"
        expected_minors = 0
        expected_majors = 0
        expected_queens = 0
        self.assert_matches(expected_minors, expected_majors, expected_queens)


class TestChaosPieceLimitsOfVanilla(PieceLimitTestBase):
    def world_setup(self, *args, **kwargs) -> None:
        self.options = copy(self.options)
        self.options["fairy_chess_pieces"] = Options.FairyChessPieces.option_full
        self.options["fairy_chess_army"] = Options.FairyChessArmy.option_chaos
        self.options["minor_piece_limit_by_type"] = 2
        self.options["major_piece_limit_by_type"] = 2
        self.options["queen_piece_limit_by_type"] = 1
        super().world_setup(*args, **kwargs)

    def test_limit(self) -> None:
        expected_minors = 22
        expected_majors = 14
        expected_queens = 6
        self.assert_matches(expected_minors, expected_majors, expected_queens)
        self.assert_actuals(expected_majors, expected_queens)


class TestChaosPieceLimitsOfOne(PieceLimitTestBase):
    def world_setup(self, *args, **kwargs) -> None:
        self.options = copy(self.options)
        self.options["fairy_chess_pieces"] = Options.FairyChessPieces.option_full
        self.options["fairy_chess_army"] = Options.FairyChessArmy.option_chaos
        self.options["minor_piece_limit_by_type"] = 1
        self.options["major_piece_limit_by_type"] = 1
        self.options["queen_piece_limit_by_type"] = 1
        super().world_setup(*args, **kwargs)

    def test_limit(self) -> None:
        expected_minors = 11
        expected_majors = 7
        expected_queens = 6
        self.assert_matches(expected_minors, expected_majors, expected_queens)
        self.assert_actuals(expected_majors, expected_queens)


class TestChaosPieceLimitsOfTwo(PieceLimitTestBase):
    def world_setup(self, *args, **kwargs) -> None:
        self.options = copy(self.options)
        self.options["fairy_chess_pieces"] = Options.FairyChessPieces.option_full
        self.options["fairy_chess_army"] = Options.FairyChessArmy.option_chaos
        self.options["minor_piece_limit_by_type"] = 2
        self.options["major_piece_limit_by_type"] = 2
        self.options["queen_piece_limit_by_type"] = 2
        super().world_setup(*args, **kwargs)

    def test_limit(self) -> None:
        expected_minors = 22
        expected_majors = 14
        expected_queens = 12
        self.assert_matches(expected_minors, expected_majors, expected_queens)
        self.assert_actuals(expected_majors, expected_queens)


class TestChaosPieceLimitsByVariety(PieceLimitTestBase):
    def world_setup(self, *args, **kwargs) -> None:
        self.options = copy(self.options)
        self.options["fairy_chess_pieces"] = Options.FairyChessPieces.option_full
        self.options["fairy_chess_army"] = Options.FairyChessArmy.option_chaos
        self.options["minor_piece_limit_by_type"] = 5
        self.options["major_piece_limit_by_type"] = 1
        self.options["queen_piece_limit_by_type"] = 3
        super().world_setup(*args, **kwargs)

    def test_limit(self) -> None:
        expected_minors = 55
        expected_majors = 7
        expected_queens = 18
        self.assert_matches(expected_minors, expected_majors, expected_queens)
        self.assert_actuals(expected_majors, expected_queens)


class TestStablePieceLimits(PieceLimitTestBase):
    def world_setup(self, *args, **kwargs) -> None:
        self.options = copy(self.options)
        self.options["fairy_chess_pieces"] = Options.FairyChessPieces.option_full
        super().world_setup(*args, **kwargs)

    def test_no_options(self) -> None:
        expected_minors = 0
        expected_majors = 0
        expected_queens = 0
        self.assert_matches(expected_minors, expected_majors, expected_queens)


class TestStablePieceLimitsOfVanilla(PieceLimitTestBase):
    def world_setup(self, *args, **kwargs) -> None:
        self.options = copy(self.options)
        self.options["fairy_chess_pieces"] = Options.FairyChessPieces.option_fide
        self.options["fairy_chess_army"] = Options.FairyChessArmy.option_stable
        self.options["minor_piece_limit_by_type"] = 2
        self.options["major_piece_limit_by_type"] = 2
        self.options["queen_piece_limit_by_type"] = 1
        super().world_setup(*args, **kwargs)

    def test_limit(self) -> None:
        expected_minors = 4
        expected_majors = 2
        expected_queens = 1
        self.assert_matches(expected_minors, expected_majors, expected_queens)
        self.assert_actuals(expected_majors, expected_queens)


class TestStablePieceLimitsOfThree(PieceLimitTestBase):
    def world_setup(self, *args, **kwargs) -> None:
        self.options = copy(self.options)
        self.options["fairy_chess_pieces"] = Options.FairyChessPieces.option_fide
        self.options["fairy_chess_army"] = Options.FairyChessArmy.option_stable
        self.options["minor_piece_limit_by_type"] = 3
        self.options["major_piece_limit_by_type"] = 3
        self.options["queen_piece_limit_by_type"] = 3
        super().world_setup(*args, **kwargs)

    def test_limit(self) -> None:
        expected_minors = 6
        expected_majors = 3
        expected_queens = 3
        self.assert_matches(expected_minors, expected_majors, expected_queens)
        self.assert_actuals(expected_majors, expected_queens)


class TestStablePieceLimitsByVariety(PieceLimitTestBase):
    def world_setup(self, *args, **kwargs) -> None:
        self.options = copy(self.options)
        self.options["fairy_chess_pieces"] = Options.FairyChessPieces.option_fide
        self.options["fairy_chess_army"] = Options.FairyChessArmy.option_stable
        self.options["minor_piece_limit_by_type"] = 4
        self.options["major_piece_limit_by_type"] = 2
        self.options["queen_piece_limit_by_type"] = 3
        super().world_setup(*args, **kwargs)

    def test_limit(self) -> None:
        expected_minors = 8
        expected_majors = 2
        expected_queens = 3
        self.assert_matches(expected_minors, expected_majors, expected_queens)
        self.assert_actuals(expected_majors, expected_queens)
