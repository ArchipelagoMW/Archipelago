from math import ceil

from BaseClasses import MultiWorld, CollectionState, Item
from .. import checksmate

from ..generic.Rules import set_rule, add_rule
from .Options import CMOptions


def has_french_move(state: CollectionState, player: int) -> bool:
    return state.count("Progressive Pawn", player) > 6  # and self.has("Play En Passant", player)


def has_pawn(state: CollectionState, player: int) -> bool:
    return state.has_any({"Progressive Pawn"}, player)


def has_pin(state: CollectionState, player: int) -> bool:
    return state.has_any({"Progressive Minor Piece", "Progressive Major Piece"}, player)


# @cache does not work due to "MultiWorld object was not de-allocated"
# TODO: @cache_self1 is very close but needs a 'self' object
def num_items_in_pool(itempool: list[Item], player_and_item: (int, str)):
    return len([item for item in itempool if item.player == player_and_item[0] and item.name == player_and_item[1]])


def count_enemy_pieces(state: CollectionState, player: int) -> int:
    return 7
    # owned_item_ids = [item_id for item_id, item in item_table.items() if state.has(item_id, player)]
    # return sum(1 if x.startswith("Enemy Piece") else 0 for x in owned_item_ids)


def count_enemy_pawns(state: CollectionState, player: int) -> int:
    return 8
    # owned_item_ids = [item_id for item_id, item in item_table.items() if state.has(item_id, player)]
    # return sum(1 if x.startswith("Enemy Pawn") else 0 for x in owned_item_ids)


enemy_locations_to_items: dict[str, str] = {
    "Capture Pawn A": "Enemy Pawn A",
    "Capture Pawn B": "Enemy Pawn B",
    "Capture Pawn C": "Enemy Pawn C",
    "Capture Pawn D": "Enemy Pawn D",
    "Capture Pawn E": "Enemy Pawn E",
    "Capture Pawn F": "Enemy Pawn F",
    "Capture Pawn G": "Enemy Pawn G",
    "Capture Pawn H": "Enemy Pawn H",
    "Capture Piece A": "Enemy Piece A",
    "Capture Piece B": "Enemy Piece B",
    "Capture Piece C": "Enemy Piece C",
    "Capture Piece D": "Enemy Piece D",
    "Capture Piece F": "Enemy Piece F",
    "Capture Piece G": "Enemy Piece G",
    "Capture Piece H": "Enemy Piece H",
}


def has_enemy(state: CollectionState, location_name: str, player: int) -> bool:
    return True
    # return state.has(enemy_locations_to_items[location_name], player)


def set_rules(multiworld: MultiWorld, player: int):
    # TODO: cannot import partially initialized CMWorld, is there a simpler way to access params?

    # TODO: handle other goals
    multiworld.completion_condition[player] = lambda state: state.has("Victory", player)

    # AI avoids making trades except where it wins material or secures victory, so require that much material
    for name, item in checksmate.Locations.location_table.items():
        set_rule(multiworld.get_location(name, player),
                 lambda state, v=item.material_expectations: state.prog_items[player]["Material"] >= v)
    # player must have (a king plus) that many chessmen to capture any given number of chessmen
    for name, item in checksmate.Locations.location_table.items():
        add_rule(multiworld.get_location(name, player),
                 lambda state, v=item.chessmen_expectations: (state.count_group("Chessmen", player) + ceil(
                     state.count("Progressive Pocket", player) /
                     state.multiworld.worlds[player].options.pocket_limit_by_pocket)) >= v)

    for i in range(1, 7):
        add_rule(multiworld.get_location("Capture " + str(i + 1) + " Pieces", player),
                 lambda state, v=i: count_enemy_pieces(state, player) > v)
        add_rule(multiworld.get_location("Capture " + str(i + 1) + " Pawns", player),
                 lambda state, v=i: count_enemy_pawns(state, player) > v)
        add_rule(multiworld.get_location("Capture " + str(i + 1) + " Of Each", player),
                 lambda state, v=i: count_enemy_pawns(state, player) > v and count_enemy_pieces(state, player) > v)
    add_rule(multiworld.get_location("Capture 8 Pawns", player),
             lambda state: count_enemy_pawns(state, player) > 7)
    add_rule(multiworld.get_location("Capture Everything", player),
             lambda state: count_enemy_pawns(state, player) > 7 and count_enemy_pieces(state, player) > 6)
    # pieces must exist to be captured
    for letter in ["A", "B", "C", "D", "F", "G", "H"]:  # the E piece is the King
        add_rule(multiworld.get_location("Capture Piece " + str(letter), player),
                 lambda state, v=letter: has_enemy(state, "Capture Piece " + str(v), player))
        add_rule(multiworld.get_location("Capture Pawn " + str(letter), player),
                 lambda state, v=letter: has_enemy(state, "Capture Pawn " + str(v), player))
    add_rule(multiworld.get_location("Capture Pawn E", player),
             lambda state: has_enemy(state, "Capture Pawn E", player))
    # tactics
    # add_rule(multiworld.get_location("Pin", player), lambda state: has_pin(state, player))
    add_rule(multiworld.get_location("Fork, Sacrificial", player), lambda state: has_pin(state, player))
    add_rule(multiworld.get_location("Fork, True", player), lambda state: has_pin(state, player))
    add_rule(multiworld.get_location("Fork, Sacrificial Triple", player), lambda state: has_pin(state, player))
    add_rule(multiworld.get_location("Fork, True Triple", player), lambda state: has_pin(state, player))
    add_rule(multiworld.get_location("Fork, Sacrificial Royal", player), lambda state: has_pin(state, player))
    add_rule(multiworld.get_location("Fork, True Royal", player), lambda state: has_pin(state, player))
    add_rule(multiworld.get_location("Threaten Pawn", player), lambda state: count_enemy_pawns(state, player) > 0)
    add_rule(multiworld.get_location("Threaten Minor", player), lambda state: count_enemy_pieces(state, player) > 3)
    add_rule(multiworld.get_location("Threaten Major", player), lambda state: count_enemy_pieces(state, player) > 5)
    add_rule(multiworld.get_location("Threaten Queen", player), lambda state: count_enemy_pieces(state, player) > 6)
    add_rule(multiworld.get_location("Threaten King", player), lambda state: has_pin(state, player))
    # special moves
    total_queens = multiworld.worlds[player].items_used[player].get("Progressive Major To Queen", 0)
    add_rule(multiworld.get_location("O-O Castle", player),
             lambda state: state.count("Progressive Major Piece", player) >= 2 + total_queens)
    add_rule(multiworld.get_location("O-O-O Castle", player),
             lambda state: state.count("Progressive Major Piece", player) >= 2 + total_queens)
    # add_rule(multiworld.get_location("French Move", player), lambda state: state.has_french_move(player))

    # goal materials
    # add_rule(multiworld.get_location("Checkmate Minima", player), lambda state: has_piece_material(state, player, 2))
    # add_rule(multiworld.get_location("Checkmate One Piece", player), lambda state: has_piece_material(state, player, 5))
    # add_rule(multiworld.get_location("Checkmate 2 Pieces", player), lambda state: has_piece_material(state, player, 9))
    # add_rule(multiworld.get_location("Checkmate 3 Pieces", player), lambda state: has_piece_material(state, player, 13))
    # add_rule(multiworld.get_location("Checkmate 4 Pieces", player), lambda state: has_piece_material(state, player, 18))
    # add_rule(multiworld.get_location("Checkmate 5 Pieces", player), lambda state: has_piece_material(state, player, 20))
    # add_rule(multiworld.get_location("Checkmate 6 Pieces", player), lambda state: has_piece_material(state, player, 22))
    # add_rule(multiworld.get_location("Checkmate 7 Pieces", player), lambda state: has_piece_material(state, player, 24))
    # add_rule(multiworld.get_location("Checkmate 8 Pieces", player), lambda state: has_piece_material(state, player, 26))
    # add_rule(multiworld.get_location("Checkmate 9 Pieces", player), lambda state: has_piece_material(state, player, 28))
    # add_rule(multiworld.get_location("Checkmate 10 Pieces", player), lambda state: has_piece_material(state, player, 30))
    # add_rule(multiworld.get_location("Checkmate 11 Pieces", player), lambda state: has_piece_material(state, player, 32))
    # add_rule(multiworld.get_location("Checkmate 12 Pieces", player), lambda state: has_piece_material(state, player, 34))
    # add_rule(multiworld.get_location("Checkmate 13 Pieces", player), lambda state: has_piece_material(state, player, 36))
    # add_rule(multiworld.get_location("Checkmate 14 Pieces", player), lambda state: has_piece_material(state, player, 38))
