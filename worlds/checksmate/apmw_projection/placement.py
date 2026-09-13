"""Active/reserve selection, placement, and material ledger projection."""

from __future__ import annotations

from typing import Iterable

from .contract import ApmwContractV2, GeometryStage
from .models import (
    ADDITIONAL_ROYAL,
    FAMILY_ORDER,
    JACK,
    JACK_SLOT,
    LOCKED_CASTLER,
    MAJOR,
    MAJOR_SLOT,
    MINOR_SLOT,
    NON_PAWN_ROLES,
    ORDINARY_NON_PAWN_ROLES,
    PAWN_SLOT,
    PRIMARY_ROYAL,
    ROLE_ORDER,
    CountByRoleFamily,
    CounterBasedSeedSeries,
    EffectiveCounts,
    FormationRankUsage,
    MaterialLedgerEntry,
    OwnedSlot,
    Piece,
    ProjectionError,
    ProjectionInput,
    ProjectionResult,
    RegionUsage,
    SemanticSeeds,
    SlotPlacement,
)


def project_roster(
    contract: ApmwContractV2,
    projection_input: ProjectionInput,
    effective: EffectiveCounts,
    stage: GeometryStage,
    pieces: list[Piece],
    dormant: list[MaterialLedgerEntry],
    unallocated: list[MaterialLedgerEntry],
    normalized_grant_material: int,
) -> ProjectionResult:
    frozen = [piece.freeze() for piece in pieces]
    active, reserve = select_active_slots(contract, stage, frozen)

    coordinates = _place_active_slots(
        stage,
        active,
        projection_input.seeds,
    )
    forwardness = effective.count("Progressive Pawn Forwardness")
    unspent_forwardness = _apply_forwardness(
        active,
        coordinates,
        stage,
        forwardness,
        projection_input.seeds,
    )
    applied_forwardness = forwardness - unspent_forwardness
    home_ids, region = _region_usage(stage, active, coordinates)
    castling_eligible = tuple(
        piece.slot_id
        for piece in active
        if piece.slot_id in home_ids and piece.final_family in (MAJOR, JACK)
    )
    active_placements = tuple(
        SlotPlacement(
            piece.slot_id,
            coordinates[piece.slot_id][0],
            coordinates[piece.slot_id][1],
            _formation_band(stage, coordinates[piece.slot_id][1]),
        )
        for piece in active
    )

    active_ledger = tuple(
        MaterialLedgerEntry(
            f"active:{piece.slot_id}",
            piece.role_origin_action,
            piece.granted_material,
            piece.slot_id,
            "active-slot",
        )
        for piece in active
        if piece.granted_material
    )
    reserve_ledger = tuple(
        MaterialLedgerEntry(
            f"reserve:{piece.slot_id}",
            piece.role_origin_action,
            piece.granted_material,
            piece.slot_id,
            "reserve-slot",
        )
        for piece in reserve
        if piece.granted_material
    )
    owned_expected_material = sum(
        piece.final_expected_material
        for piece in frozen
        if piece.source_role != PRIMARY_ROYAL
    )
    active_material = sum(piece.final_expected_material for piece in active)
    active_granted = sum(entry.amount for entry in active_ledger)
    missing = sum(entry.amount for entry in reserve_ledger)
    dormant_material = sum(entry.amount for entry in dormant)
    unallocated_material = sum(entry.amount for entry in unallocated)
    total_accounted = (
        active_granted + missing + dormant_material + unallocated_material
    )
    if total_accounted != normalized_grant_material:
        raise ProjectionError(
            "normalized grant material is not conserved: "
            f"expected {normalized_grant_material}, accounted {total_accounted}"
        )

    active_entitlements = {
        family
        for piece in active
        for family in piece.promotion_entitlement_families
    }
    reserve_entitlements = {
        family
        for piece in reserve
        for family in piece.promotion_entitlement_families
    }
    active_families = tuple(
        family for family in FAMILY_ORDER if family in active_entitlements
    )
    reserve_families = tuple(
        family for family in FAMILY_ORDER if family in reserve_entitlements
    )
    return ProjectionResult(
        contract.manifest_sha256,
        projection_input.itemization,
        projection_input.ordering,
        stage.stage_id,
        stage.files,
        stage.ranks,
        effective,
        tuple(sorted(frozen, key=_slot_output_key)),
        active,
        reserve,
        active_placements,
        _count_by_role_family(active),
        _count_by_role_family(reserve),
        active_ledger,
        reserve_ledger,
        tuple(dormant),
        tuple(unallocated),
        owned_expected_material,
        active_material,
        active_granted,
        missing,
        dormant_material,
        unallocated_material,
        normalized_grant_material,
        total_accounted,
        tuple(piece.slot_id for piece in active if piece.locked_castler),
        tuple(piece.slot_id for piece in reserve if piece.locked_castler),
        castling_eligible,
        active_families,
        reserve_families,
        region,
        applied_forwardness,
        unspent_forwardness,
    )


def select_active_slots(
    contract: ApmwContractV2,
    stage: GeometryStage,
    frozen: list[OwnedSlot],
) -> tuple[tuple[OwnedSlot, ...], tuple[OwnedSlot, ...]]:
    by_role = {
        role: [piece for piece in frozen if piece.source_role == role]
        for role in ROLE_ORDER
    }
    active_ids = {piece.slot_id for piece in by_role[PRIMARY_ROYAL]}
    back_remaining = stage.files - 1

    for role in (ADDITIONAL_ROYAL, LOCKED_CASTLER):
        selected = _activation_order(by_role[role])[:back_remaining]
        active_ids.update(piece.slot_id for piece in selected)
        back_remaining -= len(selected)

    active_non_pawn_count = sum(
        1
        for piece in frozen
        if piece.slot_id in active_ids and piece.source_role in NON_PAWN_ROLES
    )
    remaining_non_pawn = max(
        0, stage.non_pawn_capacity - active_non_pawn_count
    )
    for role in ORDINARY_NON_PAWN_ROLES:
        selected = _activation_order(by_role[role])[:remaining_non_pawn]
        active_ids.update(piece.slot_id for piece in selected)
        remaining_non_pawn -= len(selected)

    active_non_pawn_count = sum(
        1
        for piece in frozen
        if piece.slot_id in active_ids and piece.source_role in NON_PAWN_ROLES
    )
    active_pawn_capacity = contract.pawn_capacity_formula.active_pawn_capacity(
        stage.files,
        stage.gross_pawn_capacity,
        active_non_pawn_count,
    )
    selected_pawns = _activation_order(by_role[PAWN_SLOT])[
        :active_pawn_capacity
    ]
    active_ids.update(piece.slot_id for piece in selected_pawns)

    active = tuple(
        sorted(
            (piece for piece in frozen if piece.slot_id in active_ids),
            key=_slot_output_key,
        )
    )
    reserve = tuple(
        sorted(
            (piece for piece in frozen if piece.slot_id not in active_ids),
            key=_reserve_sort_key,
        )
    )
    return active, reserve


def _activation_order(pieces: Iterable[OwnedSlot]) -> list[OwnedSlot]:
    return sorted(
        pieces,
        key=lambda piece: (
            -piece.final_expected_material,
            -piece.granted_material,
            piece.source_ordinal,
            piece.slot_id,
        ),
    )


def _slot_output_key(piece: OwnedSlot) -> tuple[int, int, str]:
    return (
        ROLE_ORDER.index(piece.source_role),
        piece.source_ordinal,
        piece.slot_id,
    )


def _reserve_sort_key(piece: OwnedSlot) -> tuple[int, int, int, int, str]:
    return (
        ROLE_ORDER.index(piece.source_role),
        piece.final_expected_material,
        piece.granted_material,
        -piece.source_ordinal,
        piece.slot_id,
    )


def _count_by_role_family(
    pieces: Iterable[OwnedSlot],
) -> tuple[CountByRoleFamily, ...]:
    counts: dict[tuple[str, str], int] = {}
    for piece in pieces:
        key = (piece.source_role, piece.final_family)
        counts[key] = counts.get(key, 0) + 1
    return tuple(
        CountByRoleFamily(role, family, counts[(role, family)])
        for role in ROLE_ORDER
        for family in FAMILY_ORDER
        if (role, family) in counts
    )


def _region_usage(
    stage: GeometryStage,
    active: tuple[OwnedSlot, ...],
    coordinates: dict[str, tuple[int, int]],
) -> tuple[set[str], RegionUsage]:
    home_ids = {
        piece.slot_id
        for piece in active
        if coordinates[piece.slot_id][1] == 0
    }
    active_non_primary_non_pawns = sum(
        1 for piece in active if piece.source_role in NON_PAWN_ROLES
    )
    active_pawns = sum(
        1 for piece in active if piece.source_role == PAWN_SLOT
    )

    ranks: list[FormationRankUsage] = []
    mixed_count = stage.ranks - 7
    for relative_rank in range(stage.ranks - 3):
        rank_pieces = [
            piece
            for piece in active
            if coordinates[piece.slot_id][1] == relative_rank
        ]
        non_pawns = sum(
            1 for piece in rank_pieces if piece.source_role != PAWN_SLOT
        )
        pawns = len(rank_pieces) - non_pawns
        region = (
            "back"
            if relative_rank == 0
            else "mixed"
            if relative_rank <= mixed_count
            else "pawn-only"
        )
        ranks.append(
            FormationRankUsage(
                relative_rank,
                region,
                stage.files,
                non_pawns,
                pawns,
                stage.files - non_pawns - pawns,
            )
        )

    back_non_primary = ranks[0].non_pawns - 1
    mixed_non_pawns = sum(
        rank.non_pawns for rank in ranks if rank.region == "mixed"
    )
    mixed_pawns = sum(
        rank.pawns for rank in ranks if rank.region == "mixed"
    )
    pawn_only_pawns = sum(
        rank.pawns for rank in ranks if rank.region == "pawn-only"
    )
    active_pawn_capacity = stage.gross_pawn_capacity - max(
        0, active_non_primary_non_pawns - (stage.files - 1)
    )
    region = RegionUsage(
        stage.files - 1,
        stage.files * mixed_count,
        stage.files * 3,
        stage.non_pawn_capacity,
        stage.gross_pawn_capacity,
        stage.combined_non_primary_capacity,
        active_pawn_capacity,
        back_non_primary,
        mixed_non_pawns,
        mixed_pawns,
        pawn_only_pawns,
        stage.non_pawn_capacity - active_non_primary_non_pawns,
        active_pawn_capacity - active_pawns,
        tuple(ranks),
    )
    return home_ids, region


def _place_active_slots(
    stage: GeometryStage,
    active: tuple[OwnedSlot, ...],
    seeds: SemanticSeeds,
) -> dict[str, tuple[int, int]]:
    coordinates = {
        piece.slot_id: (stage.files // 2, 0)
        for piece in active
        if piece.source_role == PRIMARY_ROYAL
    }
    available = {
        rank: list(range(stage.files))
        for rank in range(stage.ranks - 3)
    }
    available[0].remove(stage.files // 2)
    mixed_count = stage.ranks - 7

    for role in (
        ADDITIONAL_ROYAL,
        LOCKED_CASTLER,
        JACK_SLOT,
        MAJOR_SLOT,
        MINOR_SLOT,
    ):
        pieces = sorted(
            (piece for piece in active if piece.source_role == role),
            key=lambda piece: (piece.source_ordinal, piece.slot_id),
        )
        ranks = (
            (0,)
            if role in (ADDITIONAL_ROYAL, LOCKED_CASTLER)
            else tuple(range(0, mixed_count + 1))
        )
        _place_across_ranks(
            pieces, ranks, available, stage, seeds, coordinates
        )

    pawns = sorted(
        (piece for piece in active if piece.source_role == PAWN_SLOT),
        key=lambda piece: (piece.source_ordinal, piece.slot_id),
    )
    _place_across_ranks(
        pawns,
        tuple(range(1, stage.ranks - 3)),
        available,
        stage,
        seeds,
        coordinates,
    )
    if len(coordinates) != len(active):
        raise ProjectionError(
            "active projection selected slots that could not be placed"
        )
    return coordinates


def _place_across_ranks(
    pieces: list[OwnedSlot],
    ranks: tuple[int, ...],
    available: dict[int, list[int]],
    stage: GeometryStage,
    seeds: SemanticSeeds,
    coordinates: dict[str, tuple[int, int]],
) -> None:
    remaining = list(pieces)
    for rank in ranks:
        files = available[rank]
        if not remaining:
            break
        if not files:
            continue
        role = remaining[0].source_role
        band = _formation_band(stage, rank)
        series_id = f"placement.{role}.{band}"
        series = CounterBasedSeedSeries(
            _presentation_root(seeds, series_id), series_id
        )
        count = min(len(remaining), len(files))
        for index in range(count):
            piece = remaining.pop(0)
            file_index = series.index(index, len(files))
            file = files.pop(file_index)
            coordinates[piece.slot_id] = (file, rank)
    if remaining:
        raise ProjectionError(
            "source role exceeded its assigned placement region"
        )


def _apply_forwardness(
    active: tuple[OwnedSlot, ...],
    coordinates: dict[str, tuple[int, int]],
    stage: GeometryStage,
    requested: int,
    seeds: SemanticSeeds,
) -> int:
    remaining = max(0, requested)
    edge_count = stage.ranks - 5
    for wave_length in range(edge_count, 0, -1):
        for edge in range(wave_length):
            if remaining <= 0:
                return 0
            source_rank = edge + 1
            target_rank = source_rank + 1
            occupied = set(coordinates.values())
            movable = sorted(
                (
                    piece
                    for piece in active
                    if piece.source_role == PAWN_SLOT
                    and coordinates[piece.slot_id][1] == source_rank
                    and (
                        coordinates[piece.slot_id][0],
                        target_rank,
                    )
                    not in occupied
                ),
                key=lambda piece: piece.slot_id,
            )
            series_id = (
                f"placement.{PAWN_SLOT}.forwardness-"
                f"{source_rank}-{target_rank}"
            )
            series = CounterBasedSeedSeries(
                _presentation_root(seeds, series_id), series_id
            )
            counter = 0
            while remaining > 0 and movable:
                selected_index = series.index(counter, len(movable))
                counter += 1
                piece = movable.pop(selected_index)
                file, _ = coordinates[piece.slot_id]
                target = (file, target_rank)
                if target in coordinates.values():
                    continue
                coordinates[piece.slot_id] = target
                remaining -= 1
    return remaining


def _formation_band(stage: GeometryStage, relative_rank: int) -> str:
    if relative_rank == 0:
        return "back-rank"
    mixed_count = stage.ranks - 7
    if relative_rank <= mixed_count:
        return f"mixed-{relative_rank}"
    return f"pawn-only-{relative_rank - mixed_count}"


def _presentation_root(seeds: SemanticSeeds, series_id: str) -> str:
    if "pawn" in series_id:
        return seeds.pawn_seed
    if "minor" in series_id:
        return seeds.minor_seed
    if "queen" in series_id or "amazon" in series_id:
        return seeds.queen_seed
    if (
        "major" in series_id
        or "jack" in series_id
        or "castler" in series_id
    ):
        return seeds.major_seed
    return seeds.stable_root
