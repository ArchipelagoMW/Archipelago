from typing import Any

from .Options import *

checksmate_option_presets: Dict[str, Dict[str, Any]] = {
    # Standard Chess pieces, moving in standard Chess ways, allowing many combinations of material.
    # Leaves unique features and mixed material on, but all pieces will be recognizable.
    "No Dumb Pieces": {
        "fairy_chess_pieces": FairyChessPieces.option_fide,
        "fairy_chess_pawns": FairyChessPawns.option_vanilla,
    },

    # A vanilla army with no pockets, comprising 2 Bishops+Knights+Rooks, and 1 Queen (or Rook until upgraded)
    "Strict Traditional": {
        "early_material": EarlyMaterial.option_pawn,  # not counted against locked_items (this may be changed)

        "difficulty": 0,  # excludes so many items that it can never get more than 45 material
        "max_engine_penalties": 5,
        "max_pocket": 0,
        "fairy_chess_pieces": FairyChessPieces.option_fide,
        "fairy_chess_pawns": FairyChessPawns.option_vanilla,

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
        "early_material": EarlyMaterial.option_pawn,

        "difficulty": 2,
        "max_engine_penalties": 5,
        "max_pocket": 12,
        "fairy_chess_pieces": FairyChessPieces.option_betza,
        "fairy_chess_pawns": FairyChessPawns.option_vanilla,
        "fairy_chess_army": FairyChessArmy.option_chaos,

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
        "early_material": EarlyMaterial.option_piece,

        "difficulty": 2,
        "max_engine_penalties": 5,
        "max_pocket": 12,
        "fairy_chess_pieces": FairyChessPieces.option_betza,
        "fairy_chess_pawns": FairyChessPawns.option_vanilla,
        "fairy_chess_army": FairyChessArmy.option_stable,

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
        "progression_balancing": 69,

        "early_material": EarlyMaterial.option_major,

        "difficulty": 2,
        "max_engine_penalties": 5,
        "max_pocket": 12,
        "fairy_chess_pieces": FairyChessPieces.option_betza,
        "fairy_chess_pawns": FairyChessPawns.option_berolina,
        "fairy_chess_army": FairyChessArmy.option_chaos,

        "minor_piece_limit_by_type": 1,
        "major_piece_limit_by_type": 1,
        "queen_piece_limit_by_type": 1,
        "queen_piece_limit": 5,
        "locked_items": {
            "Progressive Consul": 2,
            "Progressive King Promotion": 2,
            "Progressive Major Piece": 2,  # the 3rd is granted as Early Material!
            "Progressive Major To Queen": 3
        },
        "start_hints": {"Play as White"},
    },
}
