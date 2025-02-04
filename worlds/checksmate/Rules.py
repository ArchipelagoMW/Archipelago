from math import ceil
from typing import cast
from BaseClasses import CollectionState
from worlds.AutoWorld import World
from .Items import progression_items
from worlds.generic.Rules import set_rule, add_rule
from .Options import CMOptions
from .Locations import location_table, Tactic
import logging


def has_french_move(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Pawn", player, 7)  # and self.has("Play En Passant", player)


def has_pawn(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Pawn", player)


def has_pin(state: CollectionState, player: int) -> bool:
    return state.has_any(("Progressive Minor Piece", "Progressive Major Piece"), player)


def determine_difficulty(opts: CMOptions):
    difficulty = 1.0
    if opts.fairy_chess_army.value == opts.fairy_chess_army.option_stable:
        difficulty *= 1.05
    if opts.fairy_chess_pawns.value != opts.fairy_chess_pawns.option_vanilla:
        difficulty *= 1.05
    if opts.fairy_chess_pawns.value == opts.fairy_chess_pawns.option_mixed:
        difficulty *= 1.05
    fairy_pieces = len(opts.fairy_chess_pieces_configure.value)
    if opts.fairy_chess_pieces.value == opts.fairy_chess_pieces.option_fide:
        fairy_pieces = 1
    elif opts.fairy_chess_pieces.value == opts.fairy_chess_pieces.option_betza:
        fairy_pieces = 4
    elif opts.fairy_chess_pieces.value == opts.fairy_chess_pieces.option_full:
        fairy_pieces = 6
    difficulty *= 0.99 + (0.01 * fairy_pieces)
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


def determine_relaxation(opts: CMOptions) -> int:
    if opts.difficulty.value == opts.difficulty.option_bullet:
        return 120
    if opts.difficulty.value == opts.difficulty.option_relaxed:
        return 240
    return 0


def meets_material_expectations(state: CollectionState,
                                material: int, player: int, difficulty: float, absolute_relaxation: int) -> bool:
    target = (material * difficulty) + (absolute_relaxation if material > 90 else 0)
    current_material = state.prog_items[player]["Material"]
    logging.debug(f"Checking material: current={current_material}, target={target}")
    return current_material >= target


def meets_chessmen_expectations(state: CollectionState,
                                count: int, player: int, pocket_limit_by_pocket: int) -> bool:
    chessmen_count = state.count_group("Chessmen", player)
    if pocket_limit_by_pocket == 0:
        return chessmen_count >= count
    pocket_count = ceil(state.count("Progressive Pocket", player) / pocket_limit_by_pocket)
    return chessmen_count + pocket_count >= count


def set_rules(world: World):
    opts = cast(CMOptions, world.options)
    difficulty = determine_difficulty(opts)
    absolute_relaxation = determine_relaxation(opts)
    super_sized = opts.goal.value != opts.goal.option_single
    always_super_sized = opts.goal.value == opts.goal.option_super

    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)

    # Calculate minimum queens for castle requirements
    max_queens = world._item_pool.calculate_possible_queens()

    for name, item in location_table.items():
        if not super_sized and item.material_expectations == -1:
            continue
        if item.is_tactic is not None:
            if opts.enable_tactics.value == opts.enable_tactics.option_none:
                continue
            elif opts.enable_tactics.value == opts.enable_tactics.option_turns and \
                    item.is_tactic == Tactic.Fork:
                continue

        location = world.multiworld.get_location(name, world.player)
        rule_set = []

        # Material expectations rule
        material_cost = item.material_expectations if not super_sized else (
            item.material_expectations_grand if always_super_sized or item.material_expectations == -1 else min(
                item.material_expectations, item.material_expectations_grand
            ))
        if material_cost > 0:
            rule_set.append(lambda state, v=material_cost: meets_material_expectations(
                state, v, world.player, difficulty, absolute_relaxation))

        # Chessmen expectations rule
        if item.chessmen_expectations == -1:
            # this is used for items which change between grand and not... currently only 1 location
            assert item.code == 4_902_039, f"Unknown location code for custom chessmen: {str(item.code)}"
            rule_set.append(lambda state: meets_chessmen_expectations(
                state, 18 if super_sized else 14, world.player, opts.pocket_limit_by_pocket.value))
        elif item.chessmen_expectations > 0:
            rule_set.append(lambda state, v=item.chessmen_expectations: meets_chessmen_expectations(
                state, v, world.player, opts.pocket_limit_by_pocket.value))

        if item.material_expectations == -1:
            rule_set.append(lambda state: state.has("Super-Size Me", world.player))

        # Combine all rules with AND logic
        if rule_set:
            set_rule(location, lambda state, v=rule_set: all(rule(state) for rule in v))

    # Add special move rules
    if opts.enable_tactics.value == opts.enable_tactics.option_all:
        for fork_loc in ["Fork, Sacrificial", "Fork, True", "Fork, Sacrificial Triple", 
                        "Fork, True Triple", "Fork, Sacrificial Royal", "Fork, True Royal"]:
            add_rule(world.multiworld.get_location(fork_loc, world.player), 
                    lambda state: has_pin(state, world.player))

    for threat_loc in ["Threaten Minor", "Threaten Major", "Threaten Queen", "Threaten King"]:
        add_rule(world.multiworld.get_location(threat_loc, world.player), 
                lambda state: has_pin(state, world.player))

    # Castle rules
    add_rule(world.multiworld.get_location("O-O Castle", world.player),
             lambda state: state.has("Progressive Major Piece", world.player,
                                     2 + max(max_queens, state.count("Progressive Major To Queen", world.player))))
    add_rule(world.multiworld.get_location("O-O-O Castle", world.player),
             lambda state: state.has("Progressive Major Piece", world.player,
                                     2 + max(max_queens, state.count("Progressive Major To Queen", world.player))))
