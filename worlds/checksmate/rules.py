import logging
from typing import cast

from BaseClasses import CollectionState
from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule, forbid_item
from Options import OptionError

from .item_utils import (
    castling_requirement,
    chessmen_count as count_chessmen,
    effective_fundamental_castlers,
)
from .items import ItemizationMode, itemization_mode, progression_items
from .options import CMOptions
from .locations import (
    geometry_unlocks_for_stage,
    location_names_for_stage,
    location_table,
    rule_stage_for_series,
    tactics_mode_for_options,
    uses_expanded_profile,
)
from .geometry_progression import (
    BoardStage,
    GeometryProgression,
    GeometryUnlocks,
    build_geometry_progression,
)


logger = logging.getLogger(__name__)


def has_french_move(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Pawn", player, 7)


def has_pawn(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Pawn", player)


def has_pin(state: CollectionState, player: int) -> bool:
    return state.has_any(("Progressive Minor Piece", "Progressive Major Piece", "Progressive Jack"), player)


def effective_castlers(
    state: CollectionState,
    player: int,
    world: World | None = None,
    stage: BoardStage = BoardStage.Board8x8,
) -> int:
    if world is not None:
        return world.logic_projection.metrics(state, player, stage).castlers
    return effective_fundamental_castlers(
        state.count("Castler", player),
        state.count("Chessmen", player),
        state.count("Material", player),
    )


def has_board_files_unlock(state: CollectionState, player: int) -> bool:
    return state.has("Board Files", player) or state.has("Super-Size Me", player)


def effective_geometry_unlocks(
    state: CollectionState,
    player: int,
    initial_unlocks: GeometryUnlocks | tuple[int, int] = (0, 0),
) -> tuple[int, int]:
    if isinstance(initial_unlocks, GeometryUnlocks):
        initial_files = initial_unlocks.board_files
        initial_ranks = initial_unlocks.board_ranks
    else:
        initial_files, initial_ranks = initial_unlocks
    board_files = initial_files + state.count("Board Files", player)
    if state.has("Super-Size Me", player):
        board_files += 1
    return board_files, initial_ranks + state.count("Board Ranks", player)


def has_board_stage(
    state: CollectionState,
    player: int,
    stage: BoardStage,
    initial_unlocks: GeometryUnlocks | tuple[int, int] = (0, 0),
) -> bool:
    required_files, required_ranks = geometry_unlocks_for_stage(stage)
    board_files, board_ranks = effective_geometry_unlocks(
        state,
        player,
        initial_unlocks,
    )
    return board_files >= required_files and board_ranks >= required_ranks


def has_later_board_stage(
    state: CollectionState,
    player: int,
    stage: BoardStage,
    progression: GeometryProgression,
) -> bool:
    return any(
        metadata.stage > stage
        and has_board_stage(
            state,
            player,
            metadata.stage,
            progression.initial_unlocks,
        )
        for metadata in progression.stages
    )


def determine_difficulty(opts: CMOptions) -> float:
    difficulty = 1.0
    
    # Army composition affects difficulty
    if opts.piece_locations.value == opts.piece_locations.option_stable:
        difficulty *= 1.05

    # Pawn type affects difficulty
    if opts.fairy_chess_pawns.value == opts.fairy_chess_pawns.option_mixed:
        difficulty *= 1.16  # Most complex - all pawn types possible
    elif opts.fairy_chess_pawns.value in [
        opts.fairy_chess_pawns.option_any_pawn,
        opts.fairy_chess_pawns.option_any_fairy,
        opts.fairy_chess_pawns.option_any_classical
    ]:
        difficulty *= 1.12  # Two pawn types to manage
    elif opts.fairy_chess_pawns.value in [
        opts.fairy_chess_pawns.option_berolina,
        opts.fairy_chess_pawns.option_checkers
    ]:
        difficulty *= 1.06  # Single but unusual pawn type
    # Vanilla pawns don't affect difficulty

    fairy_pieces = len(opts.fairy_chess_pieces_configure.value)
    if opts.fairy_chess_pieces.value == opts.fairy_chess_pieces.option_fide:
        fairy_pieces = 1
    elif opts.fairy_chess_pieces.value == opts.fairy_chess_pieces.option_betza:
        fairy_pieces = 4
    elif opts.fairy_chess_pieces.value == opts.fairy_chess_pieces.option_full:
        fairy_pieces = 6
    difficulty *= 0.99 + (0.01 * fairy_pieces)
    if opts.difficulty.value == opts.difficulty.option_daily:
        difficulty *= 1.1  # results in, for example, the 4000 checkmate requirement becoming 4400
    if opts.difficulty.value == opts.difficulty.option_bullet:
        difficulty *= 1.2  # results in, for example, the 4000 checkmate requirement becoming 4800
    if opts.difficulty.value == opts.difficulty.option_relaxed:
        difficulty *= 1.35  # results in, for example, the 4000 checkmate requirement becoming 5400
    return difficulty


def determine_material(opts: CMOptions, base_material: float) -> float:
    difficulty = determine_difficulty(opts)
    material = base_material * 100 * difficulty
    material += progression_items["Play as White"].material * difficulty
    return material + determine_relaxation(opts)


def determine_min_material(
    opts: CMOptions,
    progression: GeometryProgression | None = None,
) -> float:
    base_material = 41
    base_material *= _terminal_material_ratio(opts, progression)
    return determine_material(opts, base_material)


def determine_max_material(
    opts: CMOptions,
    progression: GeometryProgression | None = None,
) -> float:
    base_material = 46
    base_material *= _terminal_material_ratio(opts, progression)
    return determine_material(opts, base_material)


def _terminal_material_ratio(
    opts: CMOptions,
    progression: GeometryProgression | None = None,
) -> float:
    if progression is None:
        try:
            progression = build_geometry_progression(
                opts.min_board_size.value,
                opts.max_board_size.value,
            )
        except ValueError as error:
            raise OptionError(f"ChecksMate board series is invalid: {error}") from error
    terminal = location_table[progression.victory.location_name]
    terminal_material = terminal.material_requirement(True)
    baseline_material = location_table[
        "Checkmate Minima"
    ].material_expectations_grand
    if baseline_material is None or (
        terminal_material is None
        and progression.endpoint.stage is not BoardStage.Board6x8
    ):
        raise OptionError(
            "ChecksMate cannot calculate item-pool material for terminal "
            f"board {progression.endpoint.stage_id}; its calibration is "
            "unsupported."
        )
    if terminal_material is None:
        # Keep 6x8 checkmate uncalibrated without inventing a new pool target.
        terminal_material = baseline_material
    return terminal_material / baseline_material


def determine_relaxation(opts: CMOptions) -> int:
    target = 0
    if opts.difficulty.value == opts.difficulty.option_bullet:
        target += 120
    if opts.difficulty.value == opts.difficulty.option_relaxed:
        target += 240
    if opts.fairy_chess_pawns.value in [
        opts.fairy_chess_pawns.option_checkers,
        opts.fairy_chess_pawns.option_any_fairy,
        opts.fairy_chess_pawns.option_any_classical
    ]:
        target += 120
    return target


def meets_material_expectations(state: CollectionState,
                                material: int, player: int, difficulty: float, absolute_relaxation: int,
                                world: World | None = None,
                                stage: BoardStage = BoardStage.Board8x8) -> bool:
    target = (material * difficulty) + (absolute_relaxation if material > 90 else 0)
    if world is not None:
        current_material = world.logic_projection.metrics(
            state, player, stage
        ).material
        target = min(target, world.logic_projection.maximum_material(stage))
    else:
        raise ValueError(
            "ChecksMate material rules require the world's logic projection"
        )
    logger.debug(
        "Checking material: current=%s, target=%s",
        current_material,
        target,
    )
    return current_material >= target


def meets_chessmen_expectations(state: CollectionState,
                                count: int, player: int, pocket_limit_by_pocket: int,
                                fundamental: bool = False,
                                world: World | None = None,
                                stage: BoardStage = BoardStage.Board8x8) -> bool:
    if world is not None:
        chessmen_count = world.logic_projection.metrics(
            state, player, stage
        ).chessmen
    else:
        mode = (
            ItemizationMode.FUNDAMENTAL
            if fundamental
            else ItemizationMode.LEGACY
        )
        chessmen_count = count_chessmen(
            state.prog_items[player],
            mode,
            pocket_limit_by_pocket,
        )
    return chessmen_count >= count


def set_rules(world: World) -> None:
    opts = cast(CMOptions, world.options)
    progression = world.geometry_progression
    start_stage = progression.stages[0].stage
    endpoint_stage = progression.endpoint.stage
    difficulty = determine_difficulty(opts)
    absolute_relaxation = determine_relaxation(opts)
    mode = itemization_mode(opts)
    fundamental = mode is ItemizationMode.FUNDAMENTAL

    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)

    tactics_mode = tactics_mode_for_options(opts)

    location_names = location_names_for_stage(
        endpoint_stage,
        tactics_mode,
        progression_start=start_stage,
    )
    for name in location_names:
        item = location_table[name]
        expanded = uses_expanded_profile(item, endpoint_stage)
        rule_stage = rule_stage_for_series(
            name,
            start_stage,
            endpoint_stage,
        )

        location = world.multiworld.get_location(name, world.player)

        if rule_stage != start_stage:
            add_rule(location, lambda state, v=rule_stage: has_board_stage(
                state,
                world.player,
                v,
                progression.initial_unlocks,
            ))

        # Material expectations rule
        material_cost = item.material_requirement(
            expanded,
        )
        if material_cost is not None and material_cost > 0:
            add_rule(location, lambda state, v=material_cost, s=rule_stage:
                     has_later_board_stage(
                         state, world.player, s, progression
                     )
                     or meets_material_expectations(
                         state, v, world.player, difficulty, absolute_relaxation,
                         world, s))

        # Chessmen expectations rule
        chessmen_requirement = min(
            item.chessmen_requirement(expanded),
            world.logic_projection.maximum_chessmen(rule_stage),
        )
        if chessmen_requirement > 0:
            add_rule(location, lambda state, v=chessmen_requirement, s=rule_stage:
                     has_later_board_stage(
                         state, world.player, s, progression
                     )
                     or meets_chessmen_expectations(
                         state, v, world.player, opts.pocket_limit_by_pocket.value,
                         fundamental, world, s))

    # Add special move rules
    if opts.enable_tactics.value == opts.enable_tactics.option_all:
        for fork_loc in ["Fork, Sacrificial", "Fork, True", "Fork, Sacrificial Triple", 
                        "Fork, True Triple", "Fork, Sacrificial Royal", "Fork, True Royal"]:
            fork_stage = rule_stage_for_series(
                fork_loc,
                start_stage,
                endpoint_stage,
            )
            add_rule(
                world.multiworld.get_location(fork_loc, world.player),
                (
                    lambda state, stage=fork_stage: world.logic_projection.metrics(
                        state, world.player, stage
                    ).chessmen >= 1
                )
                if fundamental
                else (lambda state: has_pin(state, world.player)),
            )

    for threat_loc in ["Threaten Minor", "Threaten Major", "Threaten Queen", "Threaten King"]:
        threat_stage = rule_stage_for_series(
            threat_loc,
            start_stage,
            endpoint_stage,
        )
        threat_rule = (
            (lambda state, stage=threat_stage: world.logic_projection.metrics(
                state, world.player, stage
            ).chessmen >= 1)
            if fundamental
            else (lambda state: has_pin(state, world.player))
        )
        add_rule(
            world.multiworld.get_location(threat_loc, world.player),
            threat_rule,
        )

    required_castlers = castling_requirement(opts)
    for castle_name in ("O-O Castle", "O-O-O Castle"):
        castle_stage = rule_stage_for_series(
            castle_name,
            start_stage,
            endpoint_stage,
        )
        add_rule(
            world.multiworld.get_location(castle_name, world.player),
            lambda state, required=required_castlers, stage=castle_stage:
            world.logic_projection.metrics(
                state, world.player, stage
            ).castlers >= required,
        )

    for name in location_names:
        location = world.multiworld.get_location(name, world.player)
        forbid_item(location, "Board Files", world.player)
        forbid_item(location, "Board Ranks", world.player)
