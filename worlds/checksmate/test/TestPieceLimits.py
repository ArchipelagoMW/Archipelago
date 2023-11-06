from . import CMTestBase


# I don't like that this generates many entire seeds just to check some global logic.
# TODO(chesslogic): find_piece_limit should accept an army option value. Store piece distribution on some other helper


class PieceLimitTestBase(CMTestBase):
    options = {}


class TestChaosPieceLimits(PieceLimitTestBase):
    options = {
        "fairy_chess_army": "chaos",
        "fairy_chess_pieces": 0
    }

    def test_no_options(self):
        self.assertEquals(0, self.world.find_piece_limit("Progressive Pawn"))
        self.assertEquals(0, self.world.find_piece_limit("Progressive Minor Piece"))
        self.assertEquals(0, self.world.find_piece_limit("Progressive Major Piece"))
        self.assertEquals(0, self.world.find_piece_limit("Progressive Major To Queen"))


class TestChaosPieceLimitsOfVanilla(PieceLimitTestBase):
    options = {
        "fairy_chess_army": "chaos",
        "fairy_chess_pieces": 0,
        "minor_piece_limit_by_type": 2,
        "major_piece_limit_by_type": 2,
        "queen_piece_limit_by_type": 1,
    }

    def test_limit(self):
        self.assertEquals(0, self.world.find_piece_limit("Progressive Pawn"))
        self.assertEquals(18, self.world.find_piece_limit("Progressive Minor Piece"))
        self.assertEquals(14, self.world.find_piece_limit("Progressive Major Piece"))
        self.assertEquals(4, self.world.find_piece_limit("Progressive Major To Queen"))


class TestChaosPieceLimitsOfOne(PieceLimitTestBase):
    options = {
        "fairy_chess_army": "chaos",
        "fairy_chess_pieces": 0,
        "minor_piece_limit_by_type": 1,
        "major_piece_limit_by_type": 1,
        "queen_piece_limit_by_type": 1,
    }

    def test_limit(self):
        self.assertEquals(0, self.world.find_piece_limit("Progressive Pawn"))
        self.assertEquals(9, self.world.find_piece_limit("Progressive Minor Piece"))
        self.assertEquals(9, self.world.find_piece_limit("Progressive Major Piece"))
        self.assertEquals(4, self.world.find_piece_limit("Progressive Major To Queen"))


class TestChaosPieceLimitsOfTwo(PieceLimitTestBase):
    options = {
        "fairy_chess_army": "chaos",
        "fairy_chess_pieces": 0,
        "minor_piece_limit_by_type": 2,
        "major_piece_limit_by_type": 2,
        "queen_piece_limit_by_type": 2,
    }

    def test_limit(self):
        self.assertEquals(0, self.world.find_piece_limit("Progressive Pawn"))
        self.assertEquals(18, self.world.find_piece_limit("Progressive Minor Piece"))
        self.assertEquals(18, self.world.find_piece_limit("Progressive Major Piece"))
        self.assertEquals(8, self.world.find_piece_limit("Progressive Major To Queen"))


class TestChaosPieceLimitsByVariety(PieceLimitTestBase):
    options = {
        "fairy_chess_army": "chaos",
        "fairy_chess_pieces": 0,
        "minor_piece_limit_by_type": 5,
        "major_piece_limit_by_type": 1,
        "queen_piece_limit_by_type": 3,
    }

    def test_limit(self):
        self.assertEquals(0, self.world.find_piece_limit("Progressive Pawn"))
        self.assertEquals(45, self.world.find_piece_limit("Progressive Minor Piece"))
        self.assertEquals(17, self.world.find_piece_limit("Progressive Major Piece"))
        self.assertEquals(12, self.world.find_piece_limit("Progressive Major To Queen"))


class TestLimitedPieceLimits(PieceLimitTestBase):
    options = {
        "fairy_chess_army": "limited",
        "fairy_chess_pieces": 0,
    }

    def test_no_options(self):
        self.assertEquals(0, self.world.find_piece_limit("Progressive Pawn"))
        self.assertEquals(0, self.world.find_piece_limit("Progressive Minor Piece"))
        self.assertEquals(0, self.world.find_piece_limit("Progressive Major Piece"))
        self.assertEquals(0, self.world.find_piece_limit("Progressive Major To Queen"))


class TestLimitedPieceLimitsOfVanilla(PieceLimitTestBase):
    options = {
        "fairy_chess_army": "limited",
        "fairy_chess_pieces": 0,
        "minor_piece_limit_by_type": 2,
        "major_piece_limit_by_type": 2,
        "queen_piece_limit_by_type": 1,
    }

    def test_limit(self):
        self.assertEquals(0, self.world.find_piece_limit("Progressive Pawn"))
        self.assertEquals(4, self.world.find_piece_limit("Progressive Minor Piece"))
        self.assertEquals(3, self.world.find_piece_limit("Progressive Major Piece"))
        self.assertEquals(1, self.world.find_piece_limit("Progressive Major To Queen"))


class TestLimitedPieceLimitsOfThree(PieceLimitTestBase):
    options = {
        "fairy_chess_army": "limited",
        "fairy_chess_pieces": 0,
        "minor_piece_limit_by_type": 3,
        "major_piece_limit_by_type": 3,
        "queen_piece_limit_by_type": 3,
    }

    def test_limit(self):
        self.assertEquals(0, self.world.find_piece_limit("Progressive Pawn"))
        self.assertEquals(6, self.world.find_piece_limit("Progressive Minor Piece"))
        self.assertEquals(6, self.world.find_piece_limit("Progressive Major Piece"))
        self.assertEquals(3, self.world.find_piece_limit("Progressive Major To Queen"))


class TestLimitedPieceLimitsByVariety(PieceLimitTestBase):
    options = {
        "fairy_chess_army": "limited",
        "fairy_chess_pieces": 0,
        "minor_piece_limit_by_type": 4,
        "major_piece_limit_by_type": 1,
        "queen_piece_limit_by_type": 3,
    }

    def test_limit(self):
        self.assertEquals(0, self.world.find_piece_limit("Progressive Pawn"))
        self.assertEquals(8, self.world.find_piece_limit("Progressive Minor Piece"))
        self.assertEquals(4, self.world.find_piece_limit("Progressive Major Piece"))
        self.assertEquals(3, self.world.find_piece_limit("Progressive Major To Queen"))

