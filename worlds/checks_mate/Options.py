from typing import Dict, Union, List, FrozenSet

from BaseClasses import MultiWorld
from Options import Range, Option, Choice

"""
These are not implemented yet
"""


class Goal(Choice):
    """
    How victory is defined.

    Single: Your opponent starts with an army of 7 pieces and 8 pawns. You have a king. Finding checkmate is your goal.
    To get there, find checks, mate!

    Progressive: Your goal is to checkmate a full army, but their army is scattered across the multiworld. When you
    deliver checkmate, send a check, and add a sent enemy chessman. Progressively add each enemy pawn and piece by
    checkmating the opponent 15 times. See also ChecksFinder rows and columns.

    Ordered Progressive: As Progressive, but the enemy chessmen are always in the progressive locations.
    """
    display_name = "Goal"
    option_single = 0
    # option_progressive = 1
    # option_ordered_progressive = 2
    default = 0


class PieceLocations(Choice):
    """
    When you start a new match, chooses how to distribute player pieces.

    Chaos: Puts pieces on first rank until it's full, and pawns on second rank until it's full. Changes every match -
    your games won't preserve starting position. Plays more like Chess960.

    Stable: As Chaos, but doesn't change between matches.

    Ordered: Puts pieces as close to king as possible, and pawns as close to center as possible (but never first rank).
    """
    display_name = "Piece Locations"
    option_chaos = 0
    # option_stable = 1
    # option_ordered = 2
    default = 0


class PieceTypes(Choice):
    """
    When you start a new match, chooses the player's piece types (such as whether a minor piece is a Knight or Bishop).

    Chaos: Chooses random valid options.

    Stable: As Chaos, but doesn't change between matches. You'll only ever add or upgrade pieces.

    Book: Uses the standard Chess army. Adds the King's Bishop, then both Knights, then a Bishop.
    """
    display_name = "Piece Types"
    option_chaos = 0
    # option_stable = 1
    # option_book = 2
    default = 0


class EnemyPieceTypes(Choice):
    """
    When you start a new match, chooses the CPU's piece types (such as whether a minor piece is a Knight or Bishop).

    Chaos: Chooses random valid options.

    Stable: As Chaos, but doesn't change between matches. You'll only ever add or upgrade pieces.

    Book: Uses the standard Chess army. Adds the King's Bishop, then both Knights, then a Bishop.
    """
    display_name = "Enemy Piece Types"
    # option_chaos = 0
    # option_stable = 1
    option_book = 2
    default = 2


class EarlyMaterial(Choice):
    """
    Guarantees that the first few King moves will provide a piece or pawn (chessman).

    This location gets overridden over any exclusion. It's guaranteed to be reachable with an empty inventory.
    """
    display_name = "Early Material"
    option_off = 0
    option_pawn = 1
    option_minor = 2
    #option_major = 3
    #option_piece = 4
    option_any = 5
    default = 1


class MaterialMinLimit(Choice):
    """
    The minimum material value of your army, once all items are collected. A FIDE army has value 39 (8+6+6+10+9). (If
    you want consistent access to material, consider using Starting Inventory or Starting Hints in your YAML.)
    """
    display_name = "Minimum Material"
    range_start = 30
    range_end = 90
    default = 39


class MaterialMaxLimit(Choice):
    """
    The maximum material value of your army, once all items are collected. A FIDE army has value 39 (8+6+6+10+9).
    """
    display_name = "Maximum Material"
    range_start = 30
    range_end = 100
    default = 49


class FairyChessArmy(Choice):
    """
    Whether to mix pieces between the Different Armies. No effect if Pieces is Vanilla. Does not affect pawns.

    Chaos: Chooses random enabled options.

    Limited: Chooses within your army, but in any distribution.

    Fair: Chooses within your army, to a maximum of 2 of any given piece.
    """
    display_name = "Fairy Chess Army"
    option_chaos = 0
    # option_limited = 1
    # option_fair = 2
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
    # option_vanilla = 0
    option_full = 1
    # option_cw_d_a = 2
    # option_cannon = 3
    # option_eurasian = 4
    default = 1


class FairyChessPawns(Choice):
    """
    Whether to use fairy chess pawns.

    Vanilla: Only use the standard pawn.

    Mixed: Adds all implemented fairy chess pawns to the pool. You may receive a mix of different types of pawns.

    Berolina: Only use the Berolina pawn (may appear to be a Ferz), which moves diagonally and captures forward.
    """
    display_name = "Fairy Chess Pawns"
    # option_vanilla = 0
    option_mixed = 1
    # option_berolina = 2
    default = 1


class MinorPieceTypeLimit(Range):
    """
    How many of any given type of minor piece you might play with. If set to 1, you will never start with more than 1
    Knight, nor 1 Bishop, but you may have both 1 Knight and 1 Bishop. If set to -1, this setting is disabled.
    """
    display_name = "Minor Piece Limit by Type"
    range_start = -1
    range_end = 15
    default = -1


class MajorPieceTypeLimit(Range):
    """
    How many of any given type of major piece you might play with. If set to 1, you will never start with more than 1
    Rook. If set to -1, this setting is disabled.
    """
    display_name = "Major Piece Limit by Type"
    range_start = -1
    range_end = 15
    default = -1


class QueenPieceTypeLimit(Range):
    """
    How many of any given type of Queen-equivalent piece you might play with. If set to 1, you will never start with
    more than 1 Queen. You may have both 1 Queen and 1 Amazon. If set to -1, this setting is disabled.
    """
    display_name = "Queen Piece Limit by Type"
    range_start = -1
    range_end = 15
    default = -1


class QueenPieceLimit(Range):
    """
    How many Queen-equivalent pieces you might play with. If set to 1, you will never start with more than 1 piece
    upgraded to a Queen. (This does nothing when greater than 'Queen Piece Limit by Type'.) You may still promote pawns
    during a game. If set to -1, this setting is disabled.
    """
    display_name = "Queen Piece Limit"
    range_start = -1
    range_end = 15
    default = -1


cm_options: Dict[str, type(Option)] = {
    "goal": Goal,
    "piece_locations": PieceLocations,
    "piece_types": PieceTypes,
    "enemy_piece_types": EnemyPieceTypes,
    "early_material": EarlyMaterial,
    "max_material": MaterialMaxLimit,
    "min_material": MaterialMinLimit,
    "fairy_chess_army": FairyChessArmy,
    "fairy_chess_pieces": FairyChessPieces,
    "fairy_chess_pawns": FairyChessPawns,
    "minor_piece_limit_by_type": MinorPieceTypeLimit,
    "major_piece_limit_by_type": MajorPieceTypeLimit,
    "queen_piece_limit_by_type": QueenPieceTypeLimit,
    "queen_piece_limit": QueenPieceLimit,
}


def is_option_enabled(world: MultiWorld, player: int, name: str) -> bool:
    return get_option_value(world, player, name) > 0


def get_option_value(world: MultiWorld, player: int, name: str) -> Union[int, Dict, List, FrozenSet]:
    if world is None:
        return cm_options[name].default
    option = getattr(world, name, None)
    if option is None:
        return 0

    return option[player].value
