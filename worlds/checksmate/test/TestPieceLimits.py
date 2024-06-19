from . import CMTestBase


# I don't like that this generates many entire seeds just to check some global logic.
# TODO(chesslogic): find_piece_limit should accept an army option value. Store piece distribution on some other helper


class PieceLimitTestBase(CMTestBase):

    def world_setup(self):
        super().world_setup()
        self.NO_CHILDREN = self.world.PieceLimitCascade.NO_CHILDREN
        self.ACTUAL_CHILDREN = self.world.PieceLimitCascade.ACTUAL_CHILDREN
        self.POTENTIAL_CHILDREN = self.world.PieceLimitCascade.POTENTIAL_CHILDREN

    def assert_matches(self, expected_minors: int, expected_majors: int, expected_queens: int):
        self.assertTrue(self.options["min_material"] >= 39)
        self.assertEqual(0, self.world.find_piece_limit("Progressive Pawn", self.NO_CHILDREN
                                                        ))
        self.assertEqual(expected_minors, self.world.find_piece_limit("Progressive Minor Piece", self.NO_CHILDREN
                                                                      ))
        self.assertEqual(expected_majors, self.world.find_piece_limit("Progressive Major Piece", self.NO_CHILDREN
                                                                      ))
        self.assertEqual(expected_queens, self.world.find_piece_limit("Progressive Major To Queen", self.NO_CHILDREN
                                                                      ))

    def assert_actuals(self, expected_majors, expected_queens):
        actual_queens = self.world.items_used[self.player].get("Progressive Major To Queen", 0)
        self.assertEqual(expected_majors + actual_queens,
                         self.world.find_piece_limit("Progressive Major Piece", self.ACTUAL_CHILDREN))
        self.assertEqual(expected_majors + expected_queens,
                         self.world.find_piece_limit("Progressive Major Piece", self.POTENTIAL_CHILDREN))


class TestChaosPieceLimits(PieceLimitTestBase):
    def test_no_options(self):
        self.options["fairy_chess_army"] = "chaos"
        expected_minors = 0
        expected_majors = 0
        expected_queens = 0
        self.assert_matches(expected_minors, expected_majors, expected_queens)


class TestChaosPieceLimitsOfVanilla(PieceLimitTestBase):
    options = {
        "accessibility": "minimal",
        "fairy_chess_army": "chaos",
        "fairy_chess_piece_collection": 2,
        "minor_piece_limit_by_type": 2,
        "major_piece_limit_by_type": 2,
        "queen_piece_limit_by_type": 1,
    }

    def test_limit(self):
        expected_minors = 18
        expected_majors = 10
        expected_queens = 4
        self.assert_matches(expected_minors, expected_majors, expected_queens)
        self.assert_actuals(expected_majors, expected_queens)


class TestChaosPieceLimitsOfOne(PieceLimitTestBase):
    options = {
        "accessibility": "minimal",
        "fairy_chess_army": "chaos",
        "fairy_chess_piece_collection": 2,
        "minor_piece_limit_by_type": 1,
        "major_piece_limit_by_type": 1,
        "queen_piece_limit_by_type": 1,
    }

    def test_limit(self):
        expected_minors = 9
        expected_majors = 5
        expected_queens = 4
        self.assert_matches(expected_minors, expected_majors, expected_queens)
        self.assert_actuals(expected_majors, expected_queens)


class TestChaosPieceLimitsOfTwo(PieceLimitTestBase):
    options = {
        "accessibility": "minimal",
        "fairy_chess_army": "chaos",
        "fairy_chess_piece_collection": 2,
        "minor_piece_limit_by_type": 2,
        "major_piece_limit_by_type": 2,
        "queen_piece_limit_by_type": 2,
    }

    def test_limit(self):
        expected_minors = 18
        expected_majors = 10
        expected_queens = 8
        self.assert_matches(expected_minors, expected_majors, expected_queens)
        self.assert_actuals(expected_majors, expected_queens)


class TestChaosPieceLimitsByVariety(PieceLimitTestBase):
    options = {
        "accessibility": "minimal",
        "fairy_chess_army": "chaos",
        "fairy_chess_piece_collection": 2,
        "minor_piece_limit_by_type": 5,
        "major_piece_limit_by_type": 1,
        "queen_piece_limit_by_type": 3,
    }

    def test_limit(self):
        expected_minors = 45
        expected_majors = 5
        expected_queens = 12
        self.assert_matches(expected_minors, expected_majors, expected_queens)
        self.assert_actuals(expected_majors, expected_queens)


class TestLimitedPieceLimits(PieceLimitTestBase):
    options = {
        "accessibility": "minimal",
        "fairy_chess_army": "limited",
        "fairy_chess_piece_collection": 2,
    }

    def test_no_options(self):
        expected_minors = 0
        expected_majors = 0
        expected_queens = 0
        self.assert_matches(expected_minors, expected_majors, expected_queens)


class TestLimitedPieceLimitsOfVanilla(PieceLimitTestBase):
    options = {
        "accessibility": "minimal",
        "fairy_chess_army": "limited",
        "fairy_chess_piece_collection": 2,
        "minor_piece_limit_by_type": 2,
        "major_piece_limit_by_type": 2,
        "queen_piece_limit_by_type": 1,
    }

    def test_limit(self):
        expected_minors = 4
        expected_majors = 2
        expected_queens = 1
        self.assert_matches(expected_minors, expected_majors, expected_queens)
        self.assert_actuals(expected_majors, expected_queens)


class TestLimitedPieceLimitsOfThree(PieceLimitTestBase):
    options = {
        "accessibility": "minimal",
        "fairy_chess_army": "limited",
        "fairy_chess_piece_collection": 0,
        "minor_piece_limit_by_type": 3,
        "major_piece_limit_by_type": 3,
        "queen_piece_limit_by_type": 3,
    }

    def test_limit(self):
        expected_minors = 6
        expected_majors = 3
        expected_queens = 3
        self.assert_matches(expected_minors, expected_majors, expected_queens)
        self.assert_actuals(expected_majors, expected_queens)


class TestLimitedPieceLimitsByVariety(PieceLimitTestBase):
    options = {
        "accessibility": "minimal",
        "fairy_chess_army": "limited",
        "fairy_chess_piece_collection": 0,
        "minor_piece_limit_by_type": 4,
        "major_piece_limit_by_type": 1,
        "queen_piece_limit_by_type": 3,
    }

    def test_limit(self):
        expected_minors = 8
        expected_majors = 1
        expected_queens = 3
        self.assert_matches(expected_minors, expected_majors, expected_queens)
        self.assert_actuals(expected_majors, expected_queens)
