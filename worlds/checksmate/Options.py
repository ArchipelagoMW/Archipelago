from typing import Dict, Union, List, FrozenSet

from BaseClasses import MultiWorld
from Options import Range, Option, Choice, Toggle, SpecialRange

"""
Most of these are not implemented yet
"""


class Goal(Choice):
    """
    How victory is defined.

    Single: Your opponent starts with an army of 7 pieces and 8 pawns. You have a king. Finding checkmate is your goal.
    To get there, find checks, mate!

    Progressive: Your goal is to checkmate a full army, but their army is scattered across the multiworld. When you
    deliver checkmate, send a check, and add a sent enemy chessman. Progressively add each enemy pawn and piece by
    checkmating the opponent 15 times. See also ChecksFinder rows and columns.

    Ordered Progressive: As Progressive, but the enemy chessmen are always in the progressive checkmate locations.
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
    option_stable = 1
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
    option_stable = 1
    # option_book = 2
    default = 0


class EnemyPieceTypes(Choice):
    """
    When you start a new match, chooses the CPU's piece types (such as whether a minor piece is a Knight or Bishop).

    Chaos: Chooses random valid options.

    Stable: As Chaos, but doesn't change between matches. You'll only ever add pieces.

    Book: Uses the standard Chess army. Adds pieces inward, then kingside. For example, minor pieces are added in order
    of the King's Bishop, then both Knights, then a Bishop.
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

    Pawn, Minor, Major: You will get an early chessman of the specified type (i.e. a pawn, minor piece, or major piece).

    Piece: You will get an early minor or major piece.

    Any: You will get an early chessman.
    """
    display_name = "Early Material"
    option_off = 0
    option_pawn = 1
    option_minor = 2
    option_major = 3
    option_piece = 4
    option_any = 5
    default = 1


class MaterialMinLimit(Range):
    """
    The minimum material value of your army, once all items are collected. A FIDE army has value 39 (8+6+6+10+9).

    If you want consistent access to material, consider using Starting Inventory or Starting Hints in your YAML.
    """
    display_name = "Minimum Material"
    range_start = 39
    range_end = 90
    default = 39


class MaterialMaxLimit(Range):
    """
    The maximum material value of your army, once all items are collected. A FIDE army has value 39 (8+6+6+10+9).

    Due to an ongoing issue, you may go over this maximum (by one piece) if your minimum and maximum are very close
    (within 4).
    """
    display_name = "Maximum Material"
    range_start = 39
    range_end = 100
    default = 46


class MaximumEnginePenalties(Range):
    """
    The number of times the engine will receive a reduction to their skill level. These reductions are currently named
    "Progressive ELO Engine Lobotomy," and each level reduces the AI's access to both analysis and information.

    Before calculation penalties are applied, the current supported engines have an approximate ELO of ...

    ChessV: 2030. See: https://www.computerchess.org.uk/ccrl/404/
    """
    display_name = "Maximum Engine Penalties"
    range_start = 0
    range_end = 5
    default = 5


class FairyChessPieces(Choice):
    """
    Whether to use fairy chess pieces.

    Vanilla: Disables fairy chess pieces completely.

    Full: Adds the 12 Chess With Different Armies pieces, the Cannon, and the Vao.

    CwDA: Adds the pieces from Ralph Betza's 12 Chess With Different Armies. Note that some castling rules are changed:
    The Rookies' Half-Duck castles rather than the Short Rook, and the Clobberers' Fad and Bede may both castle.

    Cannon: Adds a Rook-like piece, which captures a distal chessman by leaping over an intervening chessman.

    Eurasian: Adds the Cannon and the Vao, a Bishop-like Cannon, in that it moves and captures diagonally.
    """
    display_name = "Fairy Chess Pieces"
    option_vanilla = 0
    option_full = 1
    option_cw_d_a = 2
    option_cannon = 3
    option_eurasian = 4
    default = 1


class FairyChessArmy(Choice):
    """
    Whether to mix pieces between the Different Armies. Does not affect pawns. Note that the Eurasian pieces, which
    replace the Bishop and Knight with a Vao and Cannon, constitute a very powerful yet flawed Different Army.

    Chaos: Chooses random enabled options.

    Limited: Chooses within your army. (If you want at most 2 Bishops, 2 Knights, 2 Rooks, and 1 Queen, add Piece Type
    Limits below: 2 Minor, 2 Major, and 1 Queen.)
    """
    display_name = "Fairy Chess Army"
    option_chaos = 0
    option_limited = 1
    default = 0


class FairyChessPawns(Choice):
    """
    Whether to use fairy chess pawns.

    Vanilla: Only use the standard pawn.

    Mixed: Adds all implemented fairy chess pawns to the pool. You may receive a mix of different types of pawns.

    Berolina: Only use the Berolina pawn (may appear to be a Ferz), which moves diagonally and captures forward.
    """
    display_name = "Fairy Chess Pawns"
    option_vanilla = 0
    option_mixed = 1
    option_berolina = 2
    default = 1


class FairyKings(Range):
    """
    Whether to use fairy king upgrades, such as the Knight's moves.
    """
    display_name = "Fairy Kings"
    range_start = 0
    range_end = 2
    default = 0


class RomanKings(Range):
    """
    How many additional Royal pieces to add, which must all be captured before one experiences defeat.
    """
    display_name = "Roman Kings"
    range_start = 0
    range_end = 2
    default = 0


class MinorPieceLimitByType(SpecialRange):
    """
    How many of any given type of minor piece you might play with. If set to 1, you will never start with more than 1
    Knight, nor 1 Bishop, but you may have both 1 Knight and 1 Bishop. If set to 0, this setting is disabled.
    """
    display_name = "Minor Piece Limit by Type"
    range_start = 0
    range_end = 9
    default = 0
    special_range_cutoff = 1


class MajorPieceLimitByType(SpecialRange):
    """
    How many of any given type of major piece you might play with. If set to 1, you will never start with more than 1
    Rook. If set to 0, this setting is disabled.
    """
    display_name = "Major Piece Limit by Type"
    range_start = 0
    range_end = 9
    default = 0
    special_range_cutoff = 1


class QueenPieceLimitByType(SpecialRange):
    """
    How many of any given type of Queen-equivalent piece you might play with. If set to 1, you will never start with
    more than 1 Queen. You may have both 1 Queen and 1 Amazon. If set to 0, this setting is disabled.
    """
    display_name = "Queen Piece Limit by Type"
    range_start = 0
    range_end = 5
    default = 0
    special_range_cutoff = 1


class QueenPieceLimit(SpecialRange):
    """
    How many Queen-equivalent pieces you might play with. If set to 1, you will never have more than 1 piece upgraded to
    a Queen. (This does nothing when greater than 'Queen Piece Limit by Type'.) You may still promote pawns during a
    game. If set to 0, this setting is disabled.
    """
    display_name = "Queen Piece Limit"
    range_start = 0
    range_end = 7
    default = 0
    special_range_cutoff = 1


class DeathLink(Toggle):
    """If on: Whenever you are checkmated or resign (close the game window), everyone who is also on Death Link dies."""
    display_name = "Death Link"


cm_options: Dict[str, type(Option)] = {
    "goal": Goal,
    "piece_locations": PieceLocations,
    "piece_types": PieceTypes,
    "enemy_piece_types": EnemyPieceTypes,
    "early_material": EarlyMaterial,
    "min_material": MaterialMinLimit,
    "max_material": MaterialMaxLimit,
    "max_engine_penalties": MaximumEnginePenalties,
    "fairy_kings": FairyKings,
    "fairy_chess_pieces": FairyChessPieces,
    "fairy_chess_army": FairyChessArmy,
    "fairy_chess_pawns": FairyChessPawns,
    "roman_kings": RomanKings,
    "minor_piece_limit_by_type": MinorPieceLimitByType,
    "major_piece_limit_by_type": MajorPieceLimitByType,
    "queen_piece_limit_by_type": QueenPieceLimitByType,
    "queen_piece_limit": QueenPieceLimit,
    "death_link": DeathLink,
}


def is_option_enabled(world: MultiWorld, player: int, name: str) -> bool:
    return get_option_value(world, player, name) > 0


def get_option_value(world: MultiWorld, player: int, name: str) -> Union[int, Dict, List, FrozenSet]:
    if world is None:
        return cm_options[name].default
    option = getattr(world, name, None)
    if option is None:
        # TODO(chesslogic): is this necessary when the default for my class isn't 0?
        if name in cm_options:
            return cm_options[name].default
        return 0

    return option[player].value
