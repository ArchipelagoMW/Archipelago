from math import ceil

from BaseClasses import MultiWorld, CollectionState, Item
from .. import checksmate

from ..generic.Rules import set_rule, add_rule
from .Options import CMOptions


def total_piece_material(state: CollectionState, player: int) -> int:
    return state.prog_items[player]["Material"]


def has_piece_material(state: CollectionState, player: int, amount: int) -> bool:
    return total_piece_material(state, player) >= amount


def has_chessmen(state: CollectionState, player: int, amount: int) -> bool:
    cmoptions: CMOptions = state.multiworld.worlds[player].options  # this is safe. trust me I'm a doctor
    return (state.count_group("Chessmen", player) + ceil(
        state.count("Progressive Pocket", player) / cmoptions.pocket_limit_by_pocket)) >= amount


def has_french_move(state: CollectionState, player: int) -> bool:
    return state.count("Progressive Pawn", player) > 6  # and self.has("Play En Passant", player)


def has_pawn(state: CollectionState, player: int) -> bool:
    return state.has_any({"Progressive Pawn"}, player)


def has_pin(state: CollectionState, player: int) -> bool:
    return state.has_any({"Progressive Minor Piece", "Progressive Major Piece"}, player)


def has_castle(state: CollectionState, player: int) -> bool:
    return (state.count("Progressive Major Piece", player) >=
            2 + num_items_in_pool(state.multiworld.itempool, (player, "Progressive Major To Queen")))


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
    # TODO: handle other goals
    multiworld.completion_condition[player] = lambda state: state.has("Victory", player)

    for name, item in checksmate.Locations.location_table.items():
        set_rule(multiworld.get_location(name, player),
                 lambda state, v=item.material_expectations: has_piece_material(state, player, v))
    for name, item in checksmate.Locations.location_table.items():
        add_rule(multiworld.get_location(name, player),
                 lambda state, v=item.chessmen_expectations: has_chessmen(state, player, v))

    ###
    # inelegance is malleable
    ###

    # pieces must exist to be captured
    # and player must have (a king plus) that many chessmen to capture any given number of chessmen
    add_rule(multiworld.get_location("Capture 2 Pieces", player),
             lambda state: count_enemy_pieces(state, player) > 1)
    add_rule(multiworld.get_location("Capture 3 Pieces", player),
             lambda state: count_enemy_pieces(state, player) > 2)
    add_rule(multiworld.get_location("Capture 4 Pieces", player),
             lambda state: count_enemy_pieces(state, player) > 3)
    add_rule(multiworld.get_location("Capture 5 Pieces", player),
             lambda state: count_enemy_pieces(state, player) > 4)
    add_rule(multiworld.get_location("Capture 6 Pieces", player),
             lambda state: count_enemy_pieces(state, player) > 5)
    add_rule(multiworld.get_location("Capture 7 Pieces", player),
             lambda state: count_enemy_pieces(state, player) > 6)
    add_rule(multiworld.get_location("Capture 2 Pawns", player),
             lambda state: count_enemy_pawns(state, player) > 1)
    add_rule(multiworld.get_location("Capture 3 Pawns", player),
             lambda state: count_enemy_pawns(state, player) > 2)
    add_rule(multiworld.get_location("Capture 4 Pawns", player),
             lambda state: count_enemy_pawns(state, player) > 3)
    add_rule(multiworld.get_location("Capture 5 Pawns", player),
             lambda state: count_enemy_pawns(state, player) > 4)
    add_rule(multiworld.get_location("Capture 6 Pawns", player),
             lambda state: count_enemy_pawns(state, player) > 5)
    add_rule(multiworld.get_location("Capture 7 Pawns", player),
             lambda state: count_enemy_pawns(state, player) > 6)
    add_rule(multiworld.get_location("Capture 8 Pawns", player),
             lambda state: count_enemy_pawns(state, player) > 7)
    add_rule(multiworld.get_location("Capture 2 Of Each", player),
             lambda state: count_enemy_pawns(state, player) > 1 and count_enemy_pieces(state, player) > 1)
    add_rule(multiworld.get_location("Capture 3 Of Each", player),
             lambda state: count_enemy_pawns(state, player) > 2 and count_enemy_pieces(state, player) > 2)
    add_rule(multiworld.get_location("Capture 4 Of Each", player),
             lambda state: count_enemy_pawns(state, player) > 3 and count_enemy_pieces(state, player) > 3)
    add_rule(multiworld.get_location("Capture 5 Of Each", player),
             lambda state: count_enemy_pawns(state, player) > 4 and count_enemy_pieces(state, player) > 4)
    add_rule(multiworld.get_location("Capture 6 Of Each", player),
             lambda state: count_enemy_pawns(state, player) > 5 and count_enemy_pieces(state, player) > 5)
    add_rule(multiworld.get_location("Capture 7 Of Each", player),
             lambda state: count_enemy_pawns(state, player) > 6 and count_enemy_pieces(state, player) > 6)
    add_rule(multiworld.get_location("Capture Everything", player),
             lambda state: count_enemy_pawns(state, player) > 7 and count_enemy_pieces(state, player) > 6)
    add_rule(multiworld.get_location("Capture Piece A", player),
             lambda state: has_enemy(state, "Capture Piece A", player))
    add_rule(multiworld.get_location("Capture Piece B", player),
             lambda state: has_enemy(state, "Capture Piece B", player))
    add_rule(multiworld.get_location("Capture Piece C", player),
             lambda state: has_enemy(state, "Capture Piece C", player))
    add_rule(multiworld.get_location("Capture Piece D", player),
             lambda state: has_enemy(state, "Capture Piece D", player))
    add_rule(multiworld.get_location("Capture Piece F", player),
             lambda state: has_enemy(state, "Capture Piece F", player))
    add_rule(multiworld.get_location("Capture Piece G", player),
             lambda state: has_enemy(state, "Capture Piece G", player))
    add_rule(multiworld.get_location("Capture Piece H", player),
             lambda state: has_enemy(state, "Capture Piece H", player))
    add_rule(multiworld.get_location("Capture Pawn A", player),
             lambda state: has_enemy(state, "Capture Pawn A", player))
    add_rule(multiworld.get_location("Capture Pawn B", player),
             lambda state: has_enemy(state, "Capture Pawn B", player))
    add_rule(multiworld.get_location("Capture Pawn C", player),
             lambda state: has_enemy(state, "Capture Pawn C", player))
    add_rule(multiworld.get_location("Capture Pawn D", player),
             lambda state: has_enemy(state, "Capture Pawn D", player))
    add_rule(multiworld.get_location("Capture Pawn E", player),
             lambda state: has_enemy(state, "Capture Pawn E", player))
    add_rule(multiworld.get_location("Capture Pawn F", player),
             lambda state: has_enemy(state, "Capture Pawn F", player))
    add_rule(multiworld.get_location("Capture Pawn G", player),
             lambda state: has_enemy(state, "Capture Pawn G", player))
    add_rule(multiworld.get_location("Capture Pawn H", player),
             lambda state: has_enemy(state, "Capture Pawn H", player))
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
    add_rule(multiworld.get_location("O-O Castle", player), lambda state: has_castle(state, player))
    add_rule(multiworld.get_location("O-O-O Castle", player), lambda state: has_castle(state, player))
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
