"""Fundamental itemization planning and owned-roster generation."""

from __future__ import annotations

from dataclasses import dataclass

from .contract import ApmwContractV2
from .models import (
    AMAZON,
    JACK,
    LOCKED_CASTLER,
    MAJOR,
    MAJOR_SLOT,
    MINOR,
    MINOR_SLOT,
    PAWN,
    PAWN_SLOT,
    QUEEN,
    CounterBasedSeedSeries,
    EffectiveCounts,
    FundamentalOwnedPlan,
    MaterialLedgerEntry,
    Piece,
    ProjectionError,
    ProjectionInput,
    SemanticSeeds,
    UpgradePreference,
)
from .planning import (
    ResolvedAction,
    append_promotion_entitlement,
    primary_and_common,
    resolve_actions,
    upgrade_credit,
    upgrade_piece,
)


_ACTION_ORDER = (
    "pawn-to-minor",
    "pawn-to-major",
    "minor-to-major",
    "major-to-jack",
    "minor-to-jack",
    "major-to-queen",
    "jack-to-queen",
    "queen-to-amazon",
)


@dataclass(frozen=True)
class FundamentalPlan:
    tier_counts: dict[str, int]
    applied_counts: dict[str, int]
    spare_material: int
    locked_castlers: int


def generate_fundamental(
    contract: ApmwContractV2,
    effective: EffectiveCounts,
    actions: tuple[ResolvedAction, ...],
    semantic_root: str,
) -> tuple[
    list[Piece],
    list[MaterialLedgerEntry],
    list[MaterialLedgerEntry],
    int,
]:
    expected = contract.expected_material
    pieces, unallocated, common_total = primary_and_common(contract, effective)
    chessmen = effective.count("Chessmen")
    plan = plan_fundamental(contract, effective, actions, semantic_root)

    chessmen_pieces = [
        Piece(
            f"chessman:{ordinal:06d}",
            PAWN_SLOT,
            ordinal,
            "chessman",
            PAWN,
            PAWN,
            [],
            False,
            expected[PAWN],
            expected[PAWN],
        )
        for ordinal in range(chessmen)
    ]
    pieces.extend(chessmen_pieces)

    castler_candidates = list(chessmen_pieces)
    gateway_series = CounterBasedSeedSeries(
        semantic_root, "fundamental.gateway.role"
    )
    for ordinal in range(plan.locked_castlers):
        selected_index = gateway_series.index(ordinal, len(castler_candidates))
        piece = castler_candidates.pop(selected_index)
        piece.source_role = LOCKED_CASTLER
        piece.source_ordinal = ordinal
        piece.role_origin_action = "castler"
        piece.final_family = MAJOR
        piece.upgrade_path.append("castler")
        append_promotion_entitlement(piece, MAJOR)
        piece.locked_castler = True
        piece.granted_material += contract.castler.normalized_cost
        piece.final_expected_material = expected[MAJOR]

    minor_ordinal = 0
    major_ordinal = 0
    minor_ordinal = _apply_gateway(
        contract,
        chessmen_pieces,
        semantic_root,
        plan.applied_counts.get("pawn-to-minor", 0),
        "pawn-to-minor",
        MINOR_SLOT,
        MINOR,
        minor_ordinal,
    )
    major_ordinal = _apply_gateway(
        contract,
        chessmen_pieces,
        semantic_root,
        plan.applied_counts.get("pawn-to-major", 0),
        "pawn-to-major",
        MAJOR_SLOT,
        MAJOR,
        major_ordinal,
    )
    del minor_ordinal, major_ordinal

    action_by_name = {action.name: action for action in actions}
    for action_name in (
        "minor-to-major",
        "minor-to-jack",
        "major-to-jack",
        "major-to-queen",
        "jack-to-queen",
        "queen-to-amazon",
    ):
        count = plan.applied_counts.get(action_name, 0)
        if count <= 0:
            continue
        action = action_by_name[action_name]
        candidates = [
            piece
            for piece in chessmen_pieces
            if not piece.locked_castler and piece.final_family == action.from_family
        ]
        source_series = CounterBasedSeedSeries(
            semantic_root, f"upgrade-source.{action_name}"
        )
        for index in range(min(count, len(candidates))):
            selected_index = source_series.index(index, len(candidates))
            piece = candidates.pop(selected_index)
            upgrade_piece(contract, piece, action)

    spare_material = plan.spare_material
    major_to_jack = action_by_name.get("major-to-jack")
    if major_to_jack is not None:
        castler_jack_credit = expected[JACK] - expected["castler"]
        candidates = [
            piece
            for piece in chessmen_pieces
            if piece.locked_castler and piece.final_family == MAJOR
        ]
        upgrade_count = min(
            len(candidates),
            spare_material // castler_jack_credit,
        )
        source_series = CounterBasedSeedSeries(
            semantic_root, "upgrade-source.major-to-jack"
        )
        for index in range(upgrade_count):
            selected_index = source_series.index(index, len(candidates))
            piece = candidates.pop(selected_index)
            piece.upgrade_path.append("major-to-jack")
            piece.final_family = JACK
            append_promotion_entitlement(piece, JACK)
            piece.granted_material += castler_jack_credit
            piece.final_expected_material = expected[JACK]
        spare_material -= upgrade_count * castler_jack_credit

    if spare_material:
        unallocated.append(
            MaterialLedgerEntry(
                "unallocated:Material",
                "Material",
                spare_material,
                None,
                "unspent-fundamental-material",
            )
        )
    for pawn in (
        piece for piece in chessmen_pieces if piece.final_family == PAWN
    ):
        append_promotion_entitlement(pawn, PAWN)
    normalized_grant = (
        common_total
        + chessmen * expected[PAWN]
        + effective.count("Material") * expected["material_item"]
    )
    return pieces, [], unallocated, normalized_grant


def expected_normalized_grant(
    contract: ApmwContractV2,
    effective: EffectiveCounts,
) -> int:
    expected = contract.expected_material
    _, _, common_total = primary_and_common(contract, effective)
    return (
        common_total
        + effective.count("Chessmen") * expected[PAWN]
        + effective.count("Material") * expected["material_item"]
    )


def characterize_fundamental_owned_plan(
    contract: ApmwContractV2,
    chessmen: int,
    material_budget: int,
    castlers: int,
    seeds: SemanticSeeds,
    upgrade_preferences: tuple[UpgradePreference, ...],
) -> FundamentalOwnedPlan:
    """Expose raw-budget PlanOwned characterization for cross-language vectors."""
    if min(chessmen, material_budget, castlers) < 0:
        raise ProjectionError(
            "Fundamental characterization counts must not be negative"
        )
    projection_input = ProjectionInput(
        "fundamental",
        "stable",
        seeds,
        (),
        (),
        upgrade_preferences,
    )
    actions = resolve_actions(contract, projection_input)
    plan = simulate_fundamental(
        contract,
        chessmen,
        material_budget,
        min(castlers, contract.castler.maximum),
        actions,
        seeds.stable_root,
    )
    return FundamentalOwnedPlan(
        tuple(
            (family, plan.tier_counts[family])
            for family in (PAWN, MINOR, MAJOR, JACK, QUEEN, AMAZON)
        ),
        tuple(sorted(plan.applied_counts.items())),
        plan.spare_material,
        plan.locked_castlers,
    )


def plan_fundamental(
    contract: ApmwContractV2,
    effective: EffectiveCounts,
    actions: tuple[ResolvedAction, ...],
    semantic_root: str,
) -> FundamentalPlan:
    expected = contract.expected_material
    return simulate_fundamental(
        contract,
        effective.count("Chessmen"),
        effective.count("Material") * expected["material_item"],
        effective.count("Castler"),
        actions,
        semantic_root,
    )


def simulate_fundamental(
    contract: ApmwContractV2,
    chessmen: int,
    material_budget: int,
    castlers: int,
    actions: tuple[ResolvedAction, ...],
    semantic_root: str,
) -> FundamentalPlan:
    spare_material = material_budget
    locked = min(
        castlers,
        contract.castler.maximum,
        chessmen,
        spare_material // contract.castler.normalized_cost,
    )
    spare_material -= locked * contract.castler.normalized_cost
    tiers = {
        family: 0
        for family in (PAWN, MINOR, MAJOR, JACK, QUEEN, AMAZON)
    }
    tiers[PAWN] = chessmen - locked
    tiers[MAJOR] = locked

    action_by_name = {action.name: action for action in actions}
    ordered = [
        action_by_name[name]
        for name in _ACTION_ORDER
        if name in action_by_name
    ]
    priorities = sorted({action.priority for action in ordered}, reverse=True)
    groups = {
        priority: [action for action in ordered if action.priority == priority]
        for priority in priorities
    }
    applied: dict[str, int] = {}
    tie_counters: dict[int, int] = {}
    while True:
        did_apply = False
        for priority in priorities:
            viable: list[ResolvedAction] = []
            weights: list[float] = []
            for action in groups[priority]:
                eligible = tiers[action.from_family]
                if action.from_family == MAJOR:
                    eligible -= locked
                credit = upgrade_credit(contract, action)
                if eligible <= 0 or credit > spare_material:
                    continue
                viable.append(action)
                weights.append(eligible * float(action.proportion))
            if not viable:
                continue

            if len(viable) == 1:
                chosen = viable[0]
            else:
                counter = tie_counters.get(priority, 0)
                chosen = _weighted_choice(
                    semantic_root, priority, counter, viable, weights
                )
                tie_counters[priority] = counter + 1
            credit = upgrade_credit(contract, chosen)
            spare_material -= credit
            tiers[chosen.from_family] -= 1
            tiers[chosen.to_family] += 1
            applied[chosen.name] = applied.get(chosen.name, 0) + 1
            did_apply = True
            break
        if not did_apply:
            break
    return FundamentalPlan(tiers, applied, spare_material, locked)


def _weighted_choice(
    semantic_root: str,
    priority: int,
    counter: int,
    actions: list[ResolvedAction],
    weights: list[float],
) -> ResolvedAction:
    series = CounterBasedSeedSeries(
        semantic_root, f"fundamental.wave.tie.{priority}"
    )
    total = sum(weights)
    if total <= 0:
        return actions[series.index(counter, len(actions))]
    draw = series.unit(counter) * total
    cumulative = 0.0
    for action, weight in zip(actions, weights):
        cumulative += weight
        if draw < cumulative:
            return action
    return actions[-1]


def _apply_gateway(
    contract: ApmwContractV2,
    pieces: list[Piece],
    semantic_root: str,
    count: int,
    action_name: str,
    role: str,
    family: str,
    role_ordinal: int,
) -> int:
    candidates = [
        piece
        for piece in pieces
        if not piece.locked_castler and piece.final_family == PAWN
    ]
    series = CounterBasedSeedSeries(
        semantic_root, f"upgrade-source.{action_name}"
    )
    for index in range(min(count, len(candidates))):
        selected_index = series.index(index, len(candidates))
        piece = candidates.pop(selected_index)
        piece.source_role = role
        piece.source_ordinal = role_ordinal
        piece.role_origin_action = action_name
        role_ordinal += 1
        piece.upgrade_path.append(action_name)
        piece.final_family = family
        append_promotion_entitlement(piece, family)
        credit = (
            contract.expected_material[family]
            - contract.expected_material[PAWN]
        )
        piece.granted_material += credit
        piece.final_expected_material = contract.expected_material[family]
    return role_ordinal
