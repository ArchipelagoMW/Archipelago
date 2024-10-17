from math import ceil

from typing import List, Dict

from BaseClasses import MultiWorld, CollectionState, Item
from . import progression_items
from . import Locations

from worlds.generic.Rules import set_rule, add_rule
from .Options import CMOptions
from .Locations import Tactic


def has_french_move(state: CollectionState, player: int) -> bool:
    return state.count("Progressive Pawn", player) > 6  # and self.has("Play En Passant", player)


def has_pawn(state: CollectionState, player: int) -> bool:
    return state.has_any({"Progressive Pawn"}, player)


def has_pin(state: CollectionState, player: int) -> bool:
    return state.has_any({"Progressive Minor Piece", "Progressive Major Piece"}, player)


# @cache does not work due to "MultiWorld object was not de-allocated"
# TODO: @cache_self1 is very close but needs a 'self' object
def num_items_in_pool(itempool: List[Item], player_and_item: (int, str)):
    return len([item for item in itempool if item.player == player_and_item[0] and item.name == player_and_item[1]])


def count_enemy_pieces(state: CollectionState, player: int) -> int:
    return 9
    # owned_item_ids = [item_id for item_id, item in item_table.items() if state.has(item_id, player)]
    # return sum(1 if x.startswith("Enemy Piece") else 0 for x in owned_item_ids)


def count_enemy_pawns(state: CollectionState, player: int) -> int:
    return 10
    # owned_item_ids = [item_id for item_id, item in item_table.items() if state.has(item_id, player)]
    # return sum(1 if x.startswith("Enemy Pawn") else 0 for x in owned_item_ids)


enemy_locations_to_items: Dict[str, str] = {
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


def determine_difficulty(opts: CMOptions):
    difficulty = 1.0
    if opts.fairy_chess_army.value == opts.fairy_chess_army.option_stable:
        difficulty *= 1.05
    if opts.fairy_chess_pawns.value != opts.fairy_chess_pawns.option_vanilla:
        difficulty *= 1.05
    if opts.fairy_chess_pawns.value == opts.fairy_chess_pawns.option_mixed:
        difficulty *= 1.05
    fairy_pieces = opts.fairy_chess_pieces_configure.value
    if opts.fairy_chess_pieces.value == opts.fairy_chess_pieces.option_fide:
        fairy_pieces = [0]
    elif opts.fairy_chess_pieces.value == opts.fairy_chess_pieces.option_betza:
        fairy_pieces = [0, 1, 2, 3]
    elif opts.fairy_chess_pieces.value == opts.fairy_chess_pieces.option_full:
        fairy_pieces = [0, 1, 2, 3, 4, 5]
    difficulty *= 0.99 + (0.01 * len(fairy_pieces))
    # difficulty *= 1 + (0.025 * (5 - self.options.max_engine_penalties))

    if opts.difficulty.value == opts.difficulty.option_daily:
        difficulty *= 1.1  # results in, for example, the 4000 checkmate requirement becoming 4400
    if opts.difficulty.value == opts.difficulty.option_bullet:
        difficulty *= 1.2  # results in, for example, the 4000 checkmate requirement becoming 4800
    if opts.difficulty.value == opts.difficulty.option_relaxed:
        difficulty *= 1.35  # results in, for example, the 4000 checkmate requirement becoming 5400
    return difficulty


def determine_material(opts: CMOptions, base_material: int):
    difficulty = determine_difficulty(opts)
    material = base_material * 100 * difficulty
    material += progression_items["Play as White"].material * difficulty
    return material + determine_relaxation(opts)


def determine_min_material(opts: CMOptions):
    return determine_material(opts, 41)


def determine_max_material(opts: CMOptions):
    return determine_material(opts, 46)


def determine_relaxation(opts: CMOptions):
    if opts.difficulty.value == opts.difficulty.option_bullet:
        return 120
    if opts.difficulty.value == opts.difficulty.option_relaxed:
        return 240
    return 0


def meets_material_expectations(state: CollectionState,
                                material: int, player: int, difficulty: float, absolute_relaxation: int) -> bool:
    # TODO: handle other goals
    target = (material * difficulty) + (absolute_relaxation if material > 90 else 0)
    return state.prog_items[player]["Material"] >= target


def meets_chessmen_expectations(state: CollectionState,
                                count: int, player: int, pocket_limit_by_pocket: int) -> bool:
    chessmen_count = state.count_group("Chessmen", player)
    pocket_count = ceil(state.count("Progressive Pocket", player) / pocket_limit_by_pocket)
    return chessmen_count + pocket_count >= count


def set_rules(multiworld: MultiWorld, player: int, opts: CMOptions):
    difficulty = determine_difficulty(opts)
    absolute_relaxation = determine_relaxation(opts)
    super_sized = opts.goal.value != opts.goal.option_single
    always_super_sized = opts.goal.value == opts.goal.option_super

    # TODO: handle other goals
    multiworld.completion_condition[player] = lambda state: state.has("Victory", player)

    for name, item in Locations.location_table.items():
        if not super_sized and item.material_expectations == -1:
            continue
        if item.is_tactic is not None:
            if opts.enable_tactics.value == opts.enable_tactics.option_none:
                continue
            elif opts.enable_tactics.value == opts.enable_tactics.option_turns and item.is_tactic == Tactic.Fork:
                continue
        # AI avoids making trades except where it wins material or secures victory, so require that much material
        material_cost = item.material_expectations if not super_sized else (
            item.material_expectations_grand if always_super_sized else max(
                item.material_expectations, item.material_expectations_grand
            ))
        if material_cost > 0:
            set_rule(multiworld.get_location(name, player),
                     lambda state, v=material_cost: v <= 0 or meets_material_expectations(
                         state, v, player, difficulty, absolute_relaxation))
        # player must have (a king plus) that many chessmen to capture any given number of chessme
        if item.chessmen_expectations == -1:
            # this is used for items which change between grand and not... currently only 1 location
            if item.code == 4_902_039:  # Capture Everything
                add_rule(multiworld.get_location(name, player),
                         lambda state: meets_chessmen_expectations(
                             state, 18 if super_sized else 14, player, opts.pocket_limit_by_pocket.value))
            else:
                raise RuntimeError("Unknown location code for custom chessmen: " + str(item.code))
        elif item.chessmen_expectations > 0:
            add_rule(multiworld.get_location(name, player),
                     lambda state, v=item.chessmen_expectations: meets_chessmen_expectations(
                         state, v, player, opts.pocket_limit_by_pocket.value))
        if item.material_expectations == -1:
            add_rule(multiworld.get_location(name, player),
                     lambda state: state.count("Super-Size Me", player) > 0)

    # add_rule(multiworld.get_location("Capture 2 Pawns", player),
    #          lambda state: count_enemy_pawns(state, player) > 1)
    # piece_files = 9 if super_sized else 7
    # for i in range(1, piece_files):
    #     add_rule(multiworld.get_location("Capture " + str(i + 2) + " Pawns", player),
    #              lambda state, v=i: count_enemy_pawns(state, player) > v + 1)
    #     add_rule(multiworld.get_location("Capture " + str(i + 1) + " Pieces", player),
    #              lambda state, v=i: count_enemy_pieces(state, player) > v)
    #     add_rule(multiworld.get_location("Capture " + str(i + 1) + " Of Each", player),
    #              lambda state, v=i: count_enemy_pawns(state, player) > v and count_enemy_pieces(state, player) > v)
    # add_rule(multiworld.get_location("Capture Everything", player),
    #          lambda state: count_enemy_pawns(state, player) > \
    #          piece_files and count_enemy_pieces(state, player) >= piece_files)

    # pieces must exist to be captured
    # for letter in ["A", "B", "C", "D", "E", "F", "G", "H"]:  # the E piece is the King
    #     add_rule(multiworld.get_location("Capture Pawn " + str(letter), player),
    #              lambda state, v=letter: has_enemy(state, "Capture Pawn " + str(v), player))
    # names_to_capture = piece_names
    # if not super_sized:
    #     names_to_capture = piece_names_small
    # for piece_name in names_to_capture:
    #     add_rule(multiworld.get_location("Capture Piece " + piece_name, player),
    #              lambda state, v=piece_name: has_enemy(state, "Capture Piece " + v, player))

    # tactics
    # add_rule(multiworld.get_location("Pin", player), lambda state: has_pin(state, player))
    if opts.enable_tactics.value == opts.enable_tactics.option_all:
        add_rule(multiworld.get_location("Fork, Sacrificial", player), lambda state: has_pin(state, player))
        add_rule(multiworld.get_location("Fork, True", player), lambda state: has_pin(state, player))
        add_rule(multiworld.get_location("Fork, Sacrificial Triple", player), lambda state: has_pin(state, player))
        add_rule(multiworld.get_location("Fork, True Triple", player), lambda state: has_pin(state, player))
        add_rule(multiworld.get_location("Fork, Sacrificial Royal", player), lambda state: has_pin(state, player))
        add_rule(multiworld.get_location("Fork, True Royal", player), lambda state: has_pin(state, player))
    add_rule(multiworld.get_location("Threaten Pawn", player), lambda state: count_enemy_pawns(state, player) > 0)
    add_rule(multiworld.get_location("Threaten Minor", player), lambda state: count_enemy_pieces(state, player) > 3)
    add_rule(multiworld.get_location("Threaten Minor", player), lambda state: has_pin(state, player))
    add_rule(multiworld.get_location("Threaten Major", player), lambda state: count_enemy_pieces(state, player) > 5)
    add_rule(multiworld.get_location("Threaten Major", player), lambda state: has_pin(state, player))
    add_rule(multiworld.get_location("Threaten Queen", player), lambda state: count_enemy_pieces(state, player) > 6)
    add_rule(multiworld.get_location("Threaten Queen", player), lambda state: has_pin(state, player))
    add_rule(multiworld.get_location("Threaten King", player), lambda state: has_pin(state, player))
    # special moves
    total_queens = multiworld.worlds[player].items_used[player].get("Progressive Major To Queen", 0)
    add_rule(multiworld.get_location("O-O Castle", player),
             lambda state: state.count("Progressive Major Piece", player) >= 2 + total_queens)
    add_rule(multiworld.get_location("O-O-O Castle", player),
             lambda state: state.count("Progressive Major Piece", player) >= 2 + total_queens)
    # add_rule(multiworld.get_location("French Move", player), lambda state: state.has_french_move(player))

    # state cannot have super-size me for small checkmate
    # todo: remove from the pool if non-ordered progressive
    add_rule(multiworld.get_location("Checkmate Minima", player),
             lambda state: not state.has("Super Size Me", player))

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

