"""Public semantic projection API and itemization orchestration."""

from __future__ import annotations

from .contract import ApmwContractV2, ApmwContractV3, GeometryStage
from .fundamental import (
    characterize_fundamental_owned_plan,
    expected_normalized_grant as expected_fundamental_grant,
    generate_fundamental,
)
from .legacy import (
    expected_normalized_grant as expected_legacy_grant,
    generate_legacy,
)
from .models import (
    ADDITIONAL_ROYAL,
    AMAZON,
    JACK,
    JACK_SLOT,
    LOCKED_CASTLER,
    MAJOR,
    MAJOR_SLOT,
    MINOR,
    MINOR_SLOT,
    PAWN,
    PAWN_SLOT,
    PRIMARY_ROYAL,
    QUEEN,
    ROYAL,
    CountByRoleFamily,
    CounterBasedSeedSeries,
    EffectiveCounts,
    FormationRankUsage,
    FundamentalOwnedPlan,
    GeometryBaseline,
    ItemCount,
    MaterialLedgerEntry,
    OwnedSlot,
    Piece,
    ProjectionError,
    ProjectionInput,
    ProjectionResult,
    RegionUsage,
    SemanticSeeds,
    SlotPlacement,
    UnlockCount,
    UpgradePreference,
    projection_input_from_dict,
    projection_to_dict,
)
from .placement import project_roster, select_active_slots
from .planning import resolve_actions


__all__ = (
    "ADDITIONAL_ROYAL",
    "AMAZON",
    "ApmwContractV2",
    "ApmwContractV3",
    "CountByRoleFamily",
    "CounterBasedSeedSeries",
    "EffectiveCounts",
    "FormationRankUsage",
    "FundamentalOwnedPlan",
    "GeometryBaseline",
    "GeometryStage",
    "ItemCount",
    "JACK",
    "JACK_SLOT",
    "LOCKED_CASTLER",
    "MAJOR",
    "MAJOR_SLOT",
    "MINOR",
    "MINOR_SLOT",
    "MaterialLedgerEntry",
    "OwnedSlot",
    "PAWN",
    "PAWN_SLOT",
    "PRIMARY_ROYAL",
    "ProjectionError",
    "ProjectionInput",
    "ProjectionResult",
    "QUEEN",
    "ROYAL",
    "RegionUsage",
    "SemanticSeeds",
    "SlotPlacement",
    "UnlockCount",
    "UpgradePreference",
    "characterize_fundamental_owned_plan",
    "expected_normalized_grant_material",
    "project_exact_active_material",
    "project_exact_active_non_primary_count",
    "project_semantic_roster",
    "projection_input_from_dict",
    "projection_to_dict",
)


def project_semantic_roster(
    contract: ApmwContractV2, projection_input: ProjectionInput
) -> ProjectionResult:
    """Generate an owned roster and project it onto the unlocked geometry."""
    effective, stage, pieces, dormant, unallocated, normalized_grant = (
        _prepare_projection(contract, projection_input)
    )
    return project_roster(
        contract,
        projection_input,
        effective,
        stage,
        pieces,
        dormant,
        unallocated,
        normalized_grant,
    )


def project_exact_active_material(
    contract: ApmwContractV2, projection_input: ProjectionInput
) -> int:
    """Project only exact active material without placement or ledgers."""
    _, stage, pieces, _, _, _ = _prepare_projection(contract, projection_input)
    active, _ = select_active_slots(
        contract, stage, [piece.freeze() for piece in pieces]
    )
    return sum(piece.final_expected_material for piece in active)


def project_exact_active_non_primary_count(
    contract: ApmwContractV2, projection_input: ProjectionInput
) -> int:
    """Project active roster size while excluding the primary royal."""
    _, stage, pieces, _, _, _ = _prepare_projection(contract, projection_input)
    active, _ = select_active_slots(
        contract, stage, [piece.freeze() for piece in pieces]
    )
    return sum(piece.source_role != PRIMARY_ROYAL for piece in active)


def expected_normalized_grant_material(
    contract: ApmwContractV2, projection_input: ProjectionInput
) -> int:
    """Calculate normalized input grant material without projected ledgers."""
    _validate_mode(contract, projection_input)
    effective = _normalize_counts(contract, projection_input)
    actions = resolve_actions(contract, projection_input)
    if projection_input.itemization == "fundamental":
        return expected_fundamental_grant(contract, effective)
    return expected_legacy_grant(
        contract,
        effective,
        actions,
        projection_input.seeds.stable_root,
    )


def _prepare_projection(
    contract: ApmwContractV2, projection_input: ProjectionInput
) -> tuple[
    EffectiveCounts,
    GeometryStage,
    list[Piece],
    list[MaterialLedgerEntry],
    list[MaterialLedgerEntry],
    int,
]:
    _validate_mode(contract, projection_input)
    effective = _normalize_counts(contract, projection_input)
    stage = _select_geometry(
        contract,
        effective.unlocks,
        projection_input.geometry_baseline,
    )
    actions = resolve_actions(contract, projection_input)
    semantic_root = projection_input.seeds.stable_root

    if projection_input.itemization == "legacy":
        pieces, dormant, unallocated, normalized_grant = generate_legacy(
            contract, effective, actions, semantic_root
        )
        expected_grant = expected_legacy_grant(
            contract, effective, actions, semantic_root
        )
    else:
        pieces, dormant, unallocated, normalized_grant = generate_fundamental(
            contract, effective, actions, semantic_root
        )
        expected_grant = expected_fundamental_grant(contract, effective)
    if normalized_grant != expected_grant:
        raise ProjectionError(
            f"ownership grant calculation drifted: "
            f"{normalized_grant} != {expected_grant}"
        )
    return effective, stage, pieces, dormant, unallocated, expected_grant


def _validate_mode(
    contract: ApmwContractV2, projection_input: ProjectionInput
) -> None:
    valid = {
        (mode.itemization, mode.ordering)
        for mode in contract.mode_combinations
    }
    pair = (projection_input.itemization, projection_input.ordering)
    if pair not in valid:
        raise ProjectionError(
            f"unsupported itemization/ordering combination: {pair[0]}/{pair[1]}"
        )


def _normalize_counts(
    contract: ApmwContractV2, projection_input: ProjectionInput
) -> EffectiveCounts:
    raw: dict[str, int] = {}
    for entry in projection_input.item_counts:
        if entry.count < 0:
            raise ProjectionError(
                f"item count for {entry.name} must not be negative"
            )
        raw[entry.name] = raw.get(entry.name, 0) + entry.count

    maxima = dict(contract.effective_item_maxima["common"])
    maxima.update(contract.effective_item_maxima[projection_input.itemization])
    items: list[ItemCount] = []
    overcounts: list[ItemCount] = []
    for name in sorted(maxima):
        count = raw.get(name, 0)
        effective = min(count, maxima[name])
        if effective:
            items.append(ItemCount(name, effective))
        if count > effective:
            overcounts.append(ItemCount(name, count - effective))

    unlock_roles = {
        role.role_id: role for role in contract.geometry_unlocks.roles
    }
    raw_unlocks: dict[str, int] = {}
    for entry in projection_input.unlock_counts:
        if entry.role_id not in unlock_roles:
            raise ProjectionError(
                f"unknown geometry unlock role: {entry.role_id}"
            )
        if entry.count < 0:
            raise ProjectionError(
                f"unlock count for {entry.role_id} must not be negative"
            )
        raw_unlocks[entry.role_id] = (
            raw_unlocks.get(entry.role_id, 0) + entry.count
        )

    unlocks: list[UnlockCount] = []
    unlock_overcounts: list[UnlockCount] = []
    baseline = _geometry_baseline(contract, projection_input.geometry_baseline)
    baseline_by_role = {
        "board-file-unlock": baseline.files,
        "board-rank-unlock": baseline.ranks,
    }
    for role_id, role in sorted(unlock_roles.items()):
        maximum_steps = (
            role.maximum - baseline_by_role[role_id]
        ) // role.increment
        count = min(raw_unlocks.get(role_id, 0), maximum_steps)
        unlocks.append(UnlockCount(role_id, count))
        if raw_unlocks.get(role_id, 0) > count:
            unlock_overcounts.append(
                UnlockCount(role_id, raw_unlocks[role_id] - count)
            )

    return EffectiveCounts(
        tuple(items),
        tuple(overcounts),
        tuple(unlocks),
        tuple(unlock_overcounts),
    )


def _select_geometry(
    contract: ApmwContractV2,
    unlocks: tuple[UnlockCount, ...],
    geometry_baseline: GeometryBaseline | None = None,
) -> GeometryStage:
    counts = {entry.role_id: entry.count for entry in unlocks}
    role_by_id = {
        role.role_id: role for role in contract.geometry_unlocks.roles
    }
    file_role = role_by_id["board-file-unlock"]
    rank_role = role_by_id["board-rank-unlock"]
    baseline = _geometry_baseline(contract, geometry_baseline)
    unlocked_files = min(
        file_role.maximum,
        baseline.files
        + file_role.increment * counts.get(file_role.role_id, 0),
    )
    unlocked_ranks = min(
        rank_role.maximum,
        baseline.ranks
        + rank_role.increment * counts.get(rank_role.role_id, 0),
    )
    candidates = [
        stage
        for stage in contract.stages
        if stage.files <= unlocked_files and stage.ranks <= unlocked_ranks
    ]
    if not candidates:
        raise ProjectionError(
            f"no valid geometry is unlocked by "
            f"{unlocked_files}x{unlocked_ranks}"
        )
    order = {
        stage_id: index
        for index, stage_id in enumerate(contract.stage_order)
    }
    return max(candidates, key=lambda stage: order[stage.stage_id])


def _geometry_baseline(
    contract: ApmwContractV2,
    geometry_baseline: GeometryBaseline | None,
) -> GeometryBaseline:
    baseline = geometry_baseline or GeometryBaseline(
        contract.base_geometry.files,
        contract.base_geometry.ranks,
    )
    if not any(
        (stage.files, stage.ranks) == (baseline.files, baseline.ranks)
        for stage in contract.stages
    ):
        raise ProjectionError(
            f"geometry baseline {baseline.files}x{baseline.ranks} "
            "is not a valid contract stage"
        )
    return baseline
