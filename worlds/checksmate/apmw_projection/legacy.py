"""Legacy itemization planning and owned-roster generation."""

from __future__ import annotations

from dataclasses import dataclass
import math

from .contract import ApmwContractV2
from .models import (
    AMAZON,
    JACK,
    JACK_SLOT,
    MAJOR,
    MAJOR_SLOT,
    MINOR,
    MINOR_SLOT,
    PAWN,
    PAWN_SLOT,
    QUEEN,
    CounterBasedSeedSeries,
    EffectiveCounts,
    MaterialLedgerEntry,
    Piece,
)
from .planning import (
    ResolvedAction,
    primary_and_common,
    stable_id,
    upgrade_credit,
    upgrade_piece,
)


_ACTION_ORDER = (
    "minor-to-major",
    "major-to-jack",
    "minor-to-jack",
    "major-to-queen",
    "jack-to-queen",
    "queen-to-amazon",
)


@dataclass(frozen=True)
class LegacyPlan:
    direct_counts: dict[str, int]
    planned_actions: tuple[tuple[ResolvedAction, int], ...]
    unused_upgrade_counts: dict[str, int]


def generate_legacy(
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
    plan = plan_legacy(effective, actions, semantic_root)

    for family, role in (
        (MINOR, MINOR_SLOT),
        (MAJOR, MAJOR_SLOT),
        (JACK, JACK_SLOT),
    ):
        for ordinal in range(plan.direct_counts[family]):
            pieces.append(
                Piece(
                    stable_id(role, ordinal),
                    role,
                    ordinal,
                    f"direct-{family}",
                    family,
                    family,
                    [],
                    False,
                    expected[family],
                    expected[family],
                    [family],
                )
            )

    for action, count in plan.planned_actions:
        candidates = [
            piece
            for piece in pieces
            if not piece.locked_castler and piece.final_family == action.from_family
        ]
        source_series = CounterBasedSeedSeries(
            semantic_root, f"upgrade-source.{action.name}"
        )
        for index in range(min(count, len(candidates))):
            candidate_index = source_series.index(index, len(candidates))
            piece = candidates.pop(candidate_index)
            upgrade_piece(contract, piece, action)

    pawn_count = effective.count("Progressive Pawn")
    for ordinal in range(pawn_count):
        pieces.append(
            Piece(
                stable_id(PAWN_SLOT, ordinal),
                PAWN_SLOT,
                ordinal,
                "new-pawn",
                PAWN,
                PAWN,
                [],
                False,
                expected[PAWN],
                expected[PAWN],
                [PAWN],
            )
        )

    dormant: list[MaterialLedgerEntry] = []
    unused_queen = plan.unused_upgrade_counts[QUEEN]
    if unused_queen:
        dormant.append(
            MaterialLedgerEntry(
                "dormant:Progressive Major To Queen",
                "Progressive Major To Queen",
                unused_queen * (expected[QUEEN] - expected[MAJOR]),
                None,
                "parentless-upgrade",
            )
        )
    normalized_grant = (
        common_total
        + pawn_count * expected[PAWN]
        + sum(
            plan.direct_counts[family] * expected[family]
            for family in (MINOR, MAJOR, JACK)
        )
        + sum(
            count * upgrade_credit(contract, action)
            for action, count in plan.planned_actions
        )
        + sum(entry.amount for entry in dormant)
    )
    return pieces, dormant, unallocated, normalized_grant


def expected_normalized_grant(
    contract: ApmwContractV2,
    effective: EffectiveCounts,
    actions: tuple[ResolvedAction, ...],
    semantic_root: str,
) -> int:
    expected = contract.expected_material
    _, _, common_total = primary_and_common(contract, effective)
    plan = plan_legacy(effective, actions, semantic_root)
    return (
        common_total
        + effective.count("Progressive Pawn") * expected[PAWN]
        + sum(
            plan.direct_counts[family] * expected[family]
            for family in (MINOR, MAJOR, JACK)
        )
        + sum(
            count * upgrade_credit(contract, action)
            for action, count in plan.planned_actions
        )
        + plan.unused_upgrade_counts[QUEEN]
        * (expected[QUEEN] - expected[MAJOR])
        + plan.unused_upgrade_counts[AMAZON]
        * (expected[AMAZON] - expected[QUEEN])
    )


def plan_legacy(
    effective: EffectiveCounts,
    actions: tuple[ResolvedAction, ...],
    semantic_root: str,
) -> LegacyPlan:
    found = {
        MINOR: effective.count("Progressive Minor Piece"),
        MAJOR: effective.count("Progressive Major Piece"),
        JACK: effective.count("Progressive Jack"),
        QUEEN: effective.count("Progressive Major To Queen"),
        AMAZON: 0,
    }
    families = (MINOR, MAJOR, JACK, QUEEN, AMAZON)
    current = {(family, origin): 0 for family in families for origin in families}
    for family in (MINOR, MAJOR, JACK):
        current[(family, family)] = found[family]
    remaining = dict(found)
    direct = {
        MINOR: found[MINOR],
        MAJOR: found[MAJOR],
        JACK: found[JACK],
        QUEEN: 0,
        AMAZON: 0,
    }

    action_by_name = {action.name: action for action in actions}
    ordered_actions = [
        action_by_name[name]
        for name in _ACTION_ORDER
        if name in action_by_name
    ]
    priorities = sorted({action.priority for action in ordered_actions}, reverse=True)
    grouped = [
        [action for action in ordered_actions if action.priority == priority]
        for priority in priorities
    ]
    applied: dict[str, int] = {}
    counters: dict[str, int] = {}

    while True:
        did_apply = False
        for group in grouped:
            viable: list[ResolvedAction] = []
            weights: list[float] = []
            for action in group:
                target = action.to_family
                has_target = remaining[target] > 0
                if target not in (QUEEN, AMAZON):
                    has_target = has_target and current[(target, target)] > 0
                eligible = sum(
                    current[(action.from_family, origin)] for origin in families
                )
                if has_target and eligible > 0:
                    viable.append(action)
                    weights.append(eligible * float(action.proportion))
            if not viable:
                continue

            if len(viable) == 1:
                chosen = viable[0]
            else:
                chosen = _weighted_choice(
                    semantic_root, viable, weights, counters
                )
                for candidate in viable:
                    counters[candidate.name] = counters.get(candidate.name, 0) + 1

            target = chosen.to_family
            remaining[target] -= 1
            if target in direct:
                direct[target] = max(0, direct[target] - 1)
            if target not in (QUEEN, AMAZON):
                current[(target, target)] = max(0, current[(target, target)] - 1)
            _move_planned_source(current, families, chosen.from_family, target)
            applied[chosen.name] = applied.get(chosen.name, 0) + 1
            did_apply = True
            break
        if not did_apply:
            break

    planned = tuple(
        (action, applied[action.name])
        for group in grouped
        for action in group
        if action.name in applied
    )
    return LegacyPlan(
        direct,
        planned,
        {QUEEN: remaining[QUEEN], AMAZON: remaining[AMAZON]},
    )


def _weighted_choice(
    semantic_root: str,
    actions: list[ResolvedAction],
    weights: list[float],
    counters: dict[str, int],
) -> ResolvedAction:
    has_positive = any(weight > 0 for weight in weights)
    chosen_index = 0
    chosen_score = math.inf
    chosen_uniform = (1 << 64) - 1
    for index, (action, weight) in enumerate(zip(actions, weights)):
        counter = counters.get(action.name, 0)
        series = CounterBasedSeedSeries(
            semantic_root, f"upgrade-source.{action.name}"
        )
        if has_positive:
            if weight <= 0:
                continue
            unit = max(5e-324, series.unit(counter))
            score = -math.log(unit) / weight
            if score < chosen_score:
                chosen_score = score
                chosen_index = index
        else:
            uniform = series.value(counter)
            if uniform < chosen_uniform:
                chosen_uniform = uniform
                chosen_index = index
    return actions[chosen_index]


def _move_planned_source(
    current: dict[tuple[str, str], int],
    families: tuple[str, ...],
    source: str,
    target: str,
) -> None:
    for origin in (source,) + tuple(
        family for family in families if family != source
    ):
        if current[(source, origin)] <= 0:
            continue
        current[(source, origin)] -= 1
        current[(target, origin)] += 1
        return
