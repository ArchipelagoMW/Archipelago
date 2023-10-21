from typing import Dict

from Options import Range, Option, Choice


class PieceLocations(Choice):
    """
    When you start a new match, chooses how to distribute player pieces.
    Chaos: Puts pieces on first rank until it's full, and pawns between second and third rank randomly. Changes
    every match - your games won't preserve starting position. Plays more like Chess960.
    Stable: As Chaos, but doesn't change between matches.
    Ordered: Puts pieces as close to king as possible, and pawns as close to center as possible (but never first rank).
    """
    display_name = "Piece Locations"
    chaos = 0
    # stable = 1
    # ordered = 2
    default = 0


class PieceTypes(Choice):
    """
    When you start a new match, chooses the player's piece types (such as whether a minor piece is a Knight or Bishop).
    Chaos: Chooses random valid options.
    Stable: As Chaos, but doesn't change between matches. You'll only ever add or upgrade pieces.
    Book: Uses the standard Chess army. Adds the King's Bishop, then both Knights, then a Bishop.
    """
    display_name = "Piece Types"
    chaos = 0
    # stable = 1
    # book = 2
    default = 0


class EnemyPieceTypes(Choice):
    """
    When you start a new match, chooses the CPU's piece types (such as whether a minor piece is a Knight or Bishop).
    Chaos: Chooses random valid options.
    Stable: As Chaos, but doesn't change between matches. You'll only ever add or upgrade pieces.
    Book: Uses the standard Chess army. Adds the King's Bishop, then both Knights, then a Bishop.
    """
    display_name = "Enemy Piece Types"
    # chaos = 0
    # stable = 1
    book = 2
    default = 2


class FairyChessArmy(Choice):
    """
    Whether to mix pieces between the Different Armies. No effect if Pieces is Vanilla. Does not affect pawns.
    Chaos: Chooses random enabled options.
    Limited: Chooses within your army, but in any distribution.
    Fair: Chooses within your army, to a maximum of 2 of any given piece.
    """
    display_name = "Fairy Chess Army"
    chaos = 0
    # limited = 1
    # fair = 2
    default = 0


class FairyChessPieces(Choice):
    """
    Whether to use fairy chess pieces.
    Vanilla: Disables fairy chess pieces completely.
    Full: Adds the 12 Chess With Different Armies pieces, the Cannon, and the Vao.
    CwDA: Adds the pieces from Ralph Betza's 12 Chess With Different Armies.
    Cannon: Adds a Rook-like piece, which captures a distal chessman by leaping over an intervening chessman.
    Eurasian: Adds the Cannon and the Vao, a Bishop-like Cannon, in that it moves and captures diagonally.
    """
    display_name = "Fairy Chess Pieces"
    vanilla = 0
    full = 1
    cw_d_a = 2
    cannon = 3
    eurasian = 4
    default = 1


class FairyChessPawns(Choice):
    """
    Whether to use fairy chess pawns.
    Vanilla: Only use the standard pawn.
    Mixed: Adds all implemented fairy chess pawns to the pool. You may receive a mix of different types of pawns.
    Berolina: Only use the Berolina pawn (may appear to be a Ferz), which moves diagonally and captures forward.
    """
    display_name = "Fairy Chess Pawns"
    # vanilla = 0
    mixed = 1
    # berolina = 2
    default = 1


class MinorPieceTypeLimit(Range):
    """
    How many of any given type of minor piece you might play with. If set to 1, you will never start with more than 1
    Knight, nor 1 Bishop. You may have both 1 Knight and 1 Bishop.
    """
    display_name = "Minor Piece Limit by Type"
    range_start = 1
    range_end = 15
    default = 2


class MajorPieceTypeLimit(Range):
    """
    How many of any given type of major piece you might play with. If set to 1, you will never start with more than 1
    Rook.
    """
    display_name = "Major Piece Limit by Type"
    range_start = 1
    range_end = 15
    default = 2


class QueenPieceTypeLimit(Range):
    """
    How many of any given type of Queen-equivalent piece you might play with. If set to 1, you will never start with
    more than 1 Queen. You may have both 1 Queen and 1 Amazon.
    """
    display_name = "Queen Piece Limit by Type"
    range_start = 1
    range_end = 15
    default = 2


class QueenPieceLimit(Range):
    """
    How many Queen-equivalent pieces you might play with. If set to 1, you will never start with more than 1 piece
    upgraded to a Queen. You may still promote pawns to any piece during a game by moving them to the distant rank.
    """
    display_name = "Queen Piece Limit"
    range_start = 1
    range_end = 15
    default = 1


cm_options: Dict[str, type(Option)] = {
    "piece_locations": PieceLocations,
    "piece_types": PieceTypes,
    "enemy_piece_types": EnemyPieceTypes,
    "fairy_chess_army": FairyChessArmy,
    "fairy_chess_pieces": FairyChessPieces,
    "fairy_chess_pawns": FairyChessPawns,
    "minor_piece_limit_by_type": MinorPieceTypeLimit,
    "major_piece_limit_by_type": MajorPieceTypeLimit,
    "queen_piece_limit_by_type": QueenPieceTypeLimit,
    "queen_piece_limit": QueenPieceLimit,
}


