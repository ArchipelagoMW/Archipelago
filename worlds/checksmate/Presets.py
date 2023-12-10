from typing import Any, Dict

from .Options import *

checksmate_option_presets: Dict[str, Dict[str, Any]] = {
    # Standard Chess pieces, moving in standard Chess ways, allowing many combinations of material.
    # Leaves unique features and mixed material on, but all pieces will be recognizable.
    "No Dumb Pieces": {
        "early_material": EarlyMaterial.option_off,

        "fairy_chess_pieces": ['FIDE'],
        "fairy_chess_pawns": FairyChessPawns.option_vanilla,

        # TODO: Set the rest to defaults. Is this necessary? I feel like they should just be... defaults.
    },

    # A vanilla army with no pockets, comprising 2 Bishops+Knights+Rooks, and 1 Queen (or Rook until upgraded)
    "Strict Traditional": {
        "progression_balancing": 31,

        "early_material": EarlyMaterial.option_pawn, # not counted against locked_items (this may be changed)

        "min_material": 41,
        "max_material": 46, # excludes so many items that it can never get more than 45 material
        "max_engine_penalties": 4,
        "max_pocket": 0,
        "fairy_chess_pieces": ['FIDE'],
        "fairy_chess_pawns": FairyChessPawns.option_vanilla,

        "minor_piece_limit_by_type": 2,
        "major_piece_limit_by_type": 2,
        "queen_piece_limit": 1,
        "locked_items": {
            "Progressive Minor Piece": 4,
            "Progressive Major Piece": 3,
            "Progressive Major To Queen": 1,
        },
        "start_hints": { "Play as White" },
        "death_link": DeathLink.default,
    },

    # Chaos and pocket pieces
    "Sleeved Ace": {
        "progression_balancing": 31,

        "early_material": EarlyMaterial.option_pawn,

        "min_material": 45,
        "max_material": 51,
        "max_engine_penalties": 5,
        "max_pocket": 0,
        "fairy_chess_pieces": ["FIDE", "Rookies", "Clobberers", "Nutty", "Cannon"],
        "fairy_chess_pawns": FairyChessPawns.option_vanilla,

        "minor_piece_limit_by_type": 2,
        "major_piece_limit_by_type": 2,
        "queen_piece_limit": 1,
        "locked_items": {
            "Progressive Pocket": 12,
        },
        "start_hints": { "Play as White" },
        "death_link": DeathLink.default,
    },

    # Weird Fairy Chess with opportunity to study the opening
    "Different Army": {
        "progression_balancing": 31,

        "early_material": EarlyMaterial.option_piece,

        "min_material": 45,
        "max_material": 51,
        "max_engine_penalties": 4,
        "max_pocket": 12,
        "fairy_chess_pieces": ["Rookies", "Clobberers", "Nutty", "Camel"],
        "fairy_chess_pawns": FairyChessPawns.option_berolina,
        "fairy_chess_army": FairyChessArmy.option_stable,

        "minor_piece_limit_by_type": 2,
        "major_piece_limit_by_type": 2,
        "queen_piece_limit": 1,
        "locked_items": {
            "Progressive Minor Piece": 4,
            "Progressive Major Piece": 3,
            "Progressive Major To Queen": 1,
        },
        "start_hints": { "Play as White" },
        "death_link": DeathLink.default,
    },

    # Many exotic royal pieces
    "Power Couples": {
        "progression_balancing": 69,

        "early_material": EarlyMaterial.option_major,

        "min_material": 45,
        "max_material": 51,
        "max_engine_penalties": 4,
        "max_pocket": 12,
        "fairy_chess_pieces": ["FIDE", "Rookies", "Clobberers", "Nutty", "Camel"],
        "fairy_chess_pawns": FairyChessPawns.option_berolina,

        "minor_piece_limit_by_type": 2,
        "major_piece_limit_by_type": 2,
        "queen_piece_limit": 1,
        "locked_items": {
            "Progressive Minor Piece": 4,
            "Progressive Major Piece": 3,
            "Progressive Major To Queen": 1,
        },
        "start_hints": { "Play as White" },
        "death_link": DeathLink.default,
    },
}
