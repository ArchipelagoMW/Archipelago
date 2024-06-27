from dataclasses import dataclass
from typing import Callable

from Options import Range, Option, Choice, Toggle, NamedRange, ItemDict, PerGameCommonOptions, OptionSet, DeathLink


class Goal(Choice):
    """
    How victory is defined.

    Single: Your opponent starts with an army of 7 pieces and 8 pawns. You have a king. Finding checkmate is your goal.
    To get there, find checks, mate!

    Ordered Progressive: When you deliver checkmate, you instead graduate to a Super-Sized board. Your goal is to
    checkmate again, on that board!

    Progressive: As Ordered Progressive, but the board grows larger when someone sends you your Super-Sized board.
    NOT IMPLEMENTED.
    """
    display_name = "Goal"
    option_single = 0
    option_progressive = 1
    option_ordered_progressive = 2
    default = 0


class Difficulty(Choice):
    """
    Which kinds of checks to expect of the player. In general, this mostly affects later checks (like Checkmate Maxima,
    the victory condition).

    Grandmaster: All checks are baseline. You will generally hope for equal material, and may find yourself struggling.
    You will have about the same material as the AI for Checkmate Maxima to be considered in logic.

    Daily: The player may expect some difficulty with early checks, but complex game states will be relaxed. You will
    have about an extra Bishop and an extra Pawn for Checkmate Maxima to be considered in logic.

    Bullet: All checks are relaxed. Material expectations are raised, so the player will have more material earlier. You
    will have about an extra Rook and an extra Bishop for Checkmate Maxima to be considered in logic.

    Relaxed: Most checks require almost twice as much material, so the player will have overwhelming forces. You will
    have about an extra Queen and an extra Rook and an extra Pawn for Checkmate Maxima to be considered in logic.
    """
    display_name = "Difficulty"
    option_grandmaster = 0
    option_daily = 1
    option_bullet = 2
    option_relaxed = 3
    default = 0


class EnableTactics(Choice):
    """
    When you start a new match, chooses the player's piece types (such as whether a minor piece is a Knight or Bishop).

    All: Allows the Fork positions to contain progression or useful items.

    None: Completely removes the Fork positions from all item pools.
    """
    display_name = "Enable Tactics"
    option_all = 0
    option_none = 1
    default = 1


class PieceLocations(Choice):
    """
    When you start a new match, chooses how to distribute player pieces.

    Chaos: Puts pieces on first rank until it's full, and pawns on second rank until it's full. Changes every match -
    your games won't preserve starting position. Plays more like Chess960.

    Stable: As Chaos, but doesn't change between matches.

    Ordered: Puts pieces as close to king as possible, and pawns as close to center as possible (but never first rank).
    NOT IMPLEMENTED.
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

    Book: Uses the standard Chess army. Adds the King's Bishop, then both Knights, then a Bishop. NOT IMPLEMENTED.
    """
    display_name = "Piece Types"
    option_chaos = 0
    option_stable = 1
    # option_book = 2
    default = 1


class EnemyPieceTypes(Choice):
    """
    When you start a new match, chooses the CPU's piece types (such as whether a minor piece is a Knight or Bishop).

    Chaos: Chooses random valid options.

    Stable: As Chaos, but doesn't change between matches. You'll only ever add pieces. NOT IMPLEMENTED.

    Book: Uses the standard Chess army. Adds pieces inward, then kingside. For example, minor pieces are added in order
    of the King's Bishop, then both Knights, then a Bishop. NOT IMPLEMENTED.
    """
    display_name = "Enemy Piece Types"
    # option_chaos = 0
    # option_stable = 1
    option_book = 2
    default = 2


class EarlyMaterial(Choice):
    """
    Guarantees that a King move directly onto the second rank within the first few moves will provide a piece or pawn
    (chessman). When this option is set, this location (Bongcloud Once) gets overridden over any exclusion.

    The other Bongcloud moves also involve the King, but are not altered by this setting. (A File: Move to the leftmost
    File; Capture: Any capturing move; Center: Move to any of the center 4 squares; Promotion: Move to enemy back rank)

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
    default = 0


class MaterialMinLimit(Range):
    """
    The minimum material value of your army, once all items are collected. A FIDE army has value 40 (8+6.5+6.5+10+9).

    If you want consistent access to material, consider using Starting Inventory or Starting Hints in your YAML.
    """
    display_name = "Minimum Material"
    range_start = 40
    range_end = 90
    default = 41


class MaterialMaxLimit(Range):
    """
    The maximum material value of your army, once all items are collected. A FIDE army has value 40 (8+6.5+6.5+10+9).

    Due to an ongoing issue, you may go over this maximum (by one piece) if your minimum and maximum are very close
    (within 4).
    """
    display_name = "Maximum Material"
    range_start = 40
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


class MaximumPocket(Range):
    """
    The number of Progressive Pocket Pieces the game is allowed to add to the multiworld.

    Each Progressive Pocket Piece will improve your 1st, 2nd, or 3rd pocket slot up to 4 times, from Nothing to Pawn, to
    Minor Piece (like a pocket Knight), to Major Piece (like a pocket Rook), to Queen.

    This setting does not alter filler item distribution. (Even if you have 0 Progressive Pockets, the item pool may
    contain Progressive Pocket Gems and Progressive Pocket Range.)

    Pocket Pieces are inspired by the Dutch game of paard in de zak (pocket knight).
    """
    display_name = "Maximum Pocket"
    range_start = 0
    range_end = 12
    default = 12


class MaximumKings(Range):
    """
    How many Royal pieces (Kings) to place, which must all be captured before one experiences defeat.

    The player always starts with 1 King, but may find Progressive Consuls if this is set higher than 1. Progressive
    Consuls add additional Kings to the player's starting board.
    """
    display_name = "Maximum Kings"
    range_start = 1
    range_end = 3
    default = 1


class FairyKings(Range):
    """
    Whether to use fairy king upgrades, such as the Knight's moves. Adding multiple upgrades to the pool will allow your
    King to become a hyper-powerful invented piece if all upgrades are collected.
    """
    display_name = "Fairy Kings"
    range_start = 0
    range_end = 2
    default = 0


class FairyChessPieceCollection(Choice):
    """
    Which collection of fairy pieces to allow, if any. Choose FIDE to disable fairy chess pieces. Choose Configure to
    disable this option in favor of the more precise FairyChessPieces option.

    FIDE: The default, which only allows the standard pieces defined by FIDE (Queen, Rook, Knight, Bishop).

    Betza: Adds the pieces from Ralph Betza's Chess With Different Armies, being the Remarkable Rookies, Colorbound
    Clobberers, and Nutty Knights.

    Full: Adds every implemented army, including Eurasian and custom pieces. The Cannon and Vao capture by jumping over
    an intervening chessman.

    Configure: Allows you to specify your own pieces using the FairyChessPieces option. See also FairyChessPieces (an
    OptionSet, which is not typically visible on the Archipelago Settings UI) for advanced, specific configuration.
    """
    display_name = "Fairy Chess Piece Types"
    option_fide = 0
    option_betza = 1
    option_full = 2
    option_configure = 3
    default = 0


class FairyChessPieces(OptionSet):
    """
    Whether to use fairy chess pieces. Most pieces below are from Ralph Betza's Chess with Different Armies. If omitted,
    the default allows for all following fairy chess pieces, as well as the standard pieces defined by FIDE.

    FIDE: Contains the standard chess pieces, consisting of the Bishop, Knight, Rook, and Queen.

    Rookies: Adds the CwDA army inspired by Rooks, the Remarkable Rookies. The Half-Duck castles rather than the Short
    Rook.

    Clobberers: Adds the CwDA army inspired by Bishops, the Colorbound Clobberers. Fad and Bede may both castle.

    Nutty: Adds the CwDA army inspired by Knights, the Nutty Knights.

    Cannon: Adds the Rook-like Cannon, which captures a distal chessman by leaping over an intervening chessman, and the
    Vao, a Bishop-like Cannon, in that it moves and captures diagonally.

    Camel: Adds a custom army themed after 3,x leapers like the Camel (3,1) and Tribbabah (3,0). (The Knight is a 2,1
    leaper.)
    """
    display_name = "Fairy Chess Pieces"
    valid_keys = frozenset([
        "FIDE",
        "Rookies",
        "Clobberers",
        "Nutty",
        "Cannon",
        "Camel",
    ])
    default = valid_keys


# TODO: Rename to ...Mixed/Mercs
class FairyChessArmy(Choice):
    """
    Whether to mix pieces between the Different Armies. Does not affect pawns. Note that the Cannon pieces, which
    replace the Bishop and Knight with a Vao and Cannon, constitute a very powerful yet flawed Different Army.

    Chaos: Chooses random enabled options. (You can disable armies by setting fairy_chess_pieces, which defaults to {
    FIDE, Rookies, Clobberers, Nutty, Cannon, Camel }.)

    Stable: Chooses within one army. (If you want at most 2 Bishops, 2 Knights, 2 Rooks, and 1 Queen, add Piece Type
    Limits below: 2 Minor, 2 Major, and 1 Queen.)
    """
    display_name = "Fairy Chess Army"
    option_chaos = 0
    option_stable = 1
    # TODO: will select within one army but that army will change between games - clobberers issue with major pieces
    # option_limited = 2
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
    default = 0


class MinorPieceLimitByType(NamedRange):
    """
    How many of any given type of minor piece you might play with. If set to 1, you will never start with more than 1
    Knight, nor 1 Bishop, but you may have both 1 Knight and 1 Bishop. If set to 0, this setting is disabled.
    """
    display_name = "Minor Piece Limit by Type"
    range_start = 1
    range_end = 9
    default = 0
    special_range_names = {
        "disabled": 0,
    }


class MajorPieceLimitByType(NamedRange):
    """
    How many of any given type of major piece you might play with. If set to 1, you will never start with more than 1
    Rook. If set to 0, this setting is disabled.
    """
    display_name = "Major Piece Limit by Type"
    range_start = 1
    range_end = 9
    default = 0
    special_range_names = {
        "disabled": 0,
    }


class QueenPieceLimitByType(NamedRange):
    """
    How many of any given type of Queen-equivalent piece you might play with. If set to 1, you will never start with
    more than 1 Queen. You may have both 1 Queen and 1 Amazon. If set to 0, this setting is disabled.
    """
    display_name = "Queen Piece Limit by Type"
    range_start = 1
    range_end = 5
    default = 0
    special_range_names = {
        "disabled": 0,
    }


class PocketLimitByPocket(NamedRange):
    """
    How many Progressive Pocket items might be allocated to any given pocket. If this is set to 1, any given Pocket will
    never hold anything more substantial than a Pawn. If this is set to 3, any given Pocket will never hold a Queen.

    The default of 4 allows each of the 3 spaces to hold between 0-4 progressive items.
    """
    display_name = "Pocket Limit by Pocket"
    range_start = 1
    range_end = 4
    default = 4
    special_range_names = {
        "disabled": 0,
    }


class QueenPieceLimit(NamedRange):
    """
    How many Queen-equivalent pieces you might play with. If set to 1, you will never have more than 1 piece upgraded to
    a Queen. (This does nothing when greater than 'Queen Piece Limit by Type'.) You may still promote pawns during a
    game. If set to 0, this setting is disabled.
    """
    display_name = "Queen Piece Limit"
    range_start = 1
    range_end = 7
    default = 0
    special_range_names = {
        "disabled": 0,
    }


class LockedItems(ItemDict):
    """
    Guarantees that these progression and filler items will be unlockable.

    Implementation note: Currently forces this many items into the item pool before distribution begins. This behaviour
    is not guaranteed - a future version may simply validate the pool contains these items.
    """
    display_name = "Locked Items"


class Deathlink(DeathLink):
    """
    Whenever you are checkmated or resign (close the game window), everyone who is also on Death Link dies. Whenever
    you receive a Death Link event, your game window closes. (You cannot undo or review.)
    """


@dataclass
class CMOptions(PerGameCommonOptions):
    goal: Goal
    difficulty: Difficulty
    enable_tactics: EnableTactics
    piece_locations: PieceLocations
    piece_types: PieceTypes
    enemy_piece_types: EnemyPieceTypes
    early_material: EarlyMaterial
    min_material: MaterialMinLimit
    max_material: MaterialMaxLimit
    max_engine_penalties: MaximumEnginePenalties
    max_pocket: MaximumPocket
    max_kings: MaximumKings
    fairy_kings: FairyKings
    fairy_chess_piece_collection: FairyChessPieceCollection
    fairy_chess_pieces: FairyChessPieces
    fairy_chess_army: FairyChessArmy
    fairy_chess_pawns: FairyChessPawns
    minor_piece_limit_by_type: MinorPieceLimitByType
    major_piece_limit_by_type: MajorPieceLimitByType
    queen_piece_limit_by_type: QueenPieceLimitByType
    queen_piece_limit: QueenPieceLimit
    pocket_limit_by_pocket: PocketLimitByPocket
    locked_items: LockedItems
    death_link: Deathlink


piece_type_limit_options: dict[str, Callable[[CMOptions], Option]] = {
    "Progressive Minor Piece": lambda cmoptions: cmoptions.minor_piece_limit_by_type,
    "Progressive Major Piece": lambda cmoptions: cmoptions.major_piece_limit_by_type,
    "Progressive Major To Queen": lambda cmoptions: cmoptions.queen_piece_limit_by_type,
}


piece_limit_options: dict[str, Callable[[CMOptions], Option]] = {
    "Progressive Major To Queen": lambda cmoptions: cmoptions.queen_piece_limit,
}
