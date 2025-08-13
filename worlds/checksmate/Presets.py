from typing import Any

from .Options import *

checksmate_option_presets: dict[str, dict[str, Any]] = {
    # Standard Chess pieces, moving in standard Chess ways, allowing many combinations of material.
    # Leaves unique features and mixed material on, but all pieces will be recognizable.
    "No Dumb Pieces": {
        "fairy_chess_pieces": FairyChessPieces.option_fide,
        "fairy_chess_pawns": FairyChessPawns.option_vanilla,
        "goal": 0,

        "locked_items": {},
    },

    # A vanilla army with no pockets, comprising 2 Bishops+Knights+Rooks, and 1 Queen (or Rook until upgraded)
    "Strict Traditional": {
        "difficulty": 0,  # excludes so many items that it can never get more than 45 material
        "goal": 0,
        "early_material": EarlyMaterial.option_pawn,  # not counted against locked_items (this may be changed)

        "max_engine_penalties": 5,
        "max_pocket": 0,
        "fairy_chess_pieces": FairyChessPieces.option_fide,
        "fairy_chess_pawns": FairyChessPawns.option_vanilla,
        "asymmetric_trades": 0,

        "minor_piece_limit_by_type": 2,
        "major_piece_limit_by_type": 2,
        "queen_piece_limit": 1,
        "locked_items": {
            "Progressive Minor Piece": 4,
            "Progressive Major Piece": 3,
            "Progressive Major To Queen": 1,
        },
        "start_hints": {"Play as White"},
    },

    # Chaos and pocket pieces
    "Sleeved Ace": {
        "difficulty": 2,
        "goal": 1,
        "early_material": EarlyMaterial.option_pawn,

        "max_engine_penalties": 5,
        "max_pocket": 12,
        "fairy_chess_pieces": FairyChessPieces.option_betza,
        "fairy_chess_pawns": FairyChessPawns.option_vanilla,
        "fairy_chess_army": FairyChessArmy.option_chaos,
        "asymmetric_trades": 1,

        "minor_piece_limit_by_type": 2,
        "major_piece_limit_by_type": 2,
        "queen_piece_limit": 1,
        "locked_items": {
            "Progressive Pocket": 12,
        },
        "start_hints": {"Play as White"},
    },

    # Weird Fairy Chess with opportunity to study the opening
    "Different Army": {
        "difficulty": 2,
        "goal": 1,
        "early_material": EarlyMaterial.option_piece,

        "max_engine_penalties": 5,
        "max_pocket": 12,
        "fairy_chess_pieces": FairyChessPieces.option_betza,
        "fairy_chess_pawns": FairyChessPawns.option_vanilla,
        "fairy_chess_army": FairyChessArmy.option_stable,
        "asymmetric_trades": 0,

        "minor_piece_limit_by_type": 2,
        "major_piece_limit_by_type": 2,
        "queen_piece_limit": 1,
        "locked_items": {
            "Progressive Minor Piece": 4,
            "Progressive Major Piece": 3,
            "Progressive Major To Queen": 1,
        },
        "start_hints": {"Play as White"},
    },

    # Many exotic royal pieces
    "Power Couples": {
        "difficulty": 2,
        "goal": 1,
        "early_material": EarlyMaterial.option_major,

        "max_engine_penalties": 5,
        "max_pocket": 12,
        "fairy_chess_pieces": FairyChessPieces.option_betza,
        "fairy_chess_pawns": FairyChessPawns.option_vanilla,
        "fairy_chess_army": FairyChessArmy.option_chaos,
        "asymmetric_trades": 1,

        "minor_piece_limit_by_type": 1,
        "major_piece_limit_by_type": 1,
        "queen_piece_limit_by_type": 1,
        "queen_piece_limit": 5,
        "locked_items": {
            "Progressive Consul": 2,
            "Progressive King Promotion": 1,
            "Progressive Jack": 1,
            "Progressive Major Piece": 2,  # the 3rd is granted as Early Material!
            "Progressive Major To Queen": 3
        },
        "start_hints": {"Play as White"},
    },
}
