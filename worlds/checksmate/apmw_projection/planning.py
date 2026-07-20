"""Shared action resolution and roster-building primitives."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .contract import ApmwContractV2
from .models import (
    ADDITIONAL_ROYAL,
    MAJOR_SLOT,
    MINOR_SLOT,
    PRIMARY_ROYAL,
    ROYAL,
    EffectiveCounts,
    MaterialLedgerEntry,
    Piece,
    ProjectionError,
    ProjectionInput,
    UpgradePreference,
)


@dataclass(frozen=True)
class ResolvedAction:
    name: str
    from_family: str
    to_family: str
    source_role_rule: str
    priority: int
    proportion: Fraction


_DEFAULT_LEGACY_PREFERENCES = (
    UpgradePreference("major-to-queen", 1),
)
_DEFAULT_FUNDAMENTAL_PREFERENCES = (
    UpgradePreference("pawn-to-minor", 1),
    UpgradePreference("minor-to-major", 1),
    UpgradePreference("pawn-to-major", 1),
    UpgradePreference("major-to-queen", 1),
)


def resolve_actions(
    contract: ApmwContractV2, projection_input: ProjectionInput
) -> tuple[ResolvedAction, ...]:
    preferences = projection_input.upgrade_preferences
    if not preferences:
        preferences = (
            _DEFAULT_LEGACY_PREFERENCES
            if projection_input.itemization == "legacy"
            else _DEFAULT_FUNDAMENTAL_PREFERENCES
        )
    by_name: dict[str, UpgradePreference] = {}
    for preference in preferences:
        if preference.action in by_name:
            raise ProjectionError(
                f"duplicate upgrade preference: {preference.action}"
            )
        by_name[preference.action] = preference
        preference.proportion

    transitions = {
        transition.action: transition
        for transition in contract.upgrade_dag.transitions
    }
    valid_actions = set(transitions) | set(contract.upgrade_dag.pawn_creation_actions)
    unknown = sorted(set(by_name) - valid_actions)
    if unknown:
        raise ProjectionError(f"unknown upgrade actions: {unknown}")
    actions = []
    for transition in contract.upgrade_dag.transitions:
        preference = by_name.get(transition.action)
        if preference is None or preference.priority <= 0:
            continue
        actions.append(
            ResolvedAction(
                transition.action,
                transition.from_family,
                transition.to_family,
                transition.source_role_rule,
                preference.priority,
                preference.proportion,
            )
        )
    return tuple(actions)


def primary_and_common(
    contract: ApmwContractV2,
    effective: EffectiveCounts,
) -> tuple[list[Piece], list[MaterialLedgerEntry], int]:
    expected = contract.expected_material
    king_promotions = effective.count("Progressive King Promotion")
    primary_material = king_promotions * expected["king_promotion"]
    pieces = [
        Piece(
            "primary-royal:000000",
            PRIMARY_ROYAL,
            0,
            "primary-royal",
            ROYAL,
            ROYAL,
            ["king-promotion"] * king_promotions,
            False,
            primary_material,
            primary_material,
            [ROYAL] if king_promotions else [],
        )
    ]
    for ordinal in range(effective.count("Progressive Consul")):
        pieces.append(
            Piece(
                stable_id(ADDITIONAL_ROYAL, ordinal),
                ADDITIONAL_ROYAL,
                ordinal,
                "consul",
                ROYAL,
                ROYAL,
                [],
                False,
                expected["consul"],
                expected["consul"],
                [ROYAL],
            )
        )

    unallocated = []
    common_total = primary_material + sum(
        piece.granted_material
        for piece in pieces
        if piece.source_role == ADDITIONAL_ROYAL
    )
    for item_name, material_key in (
        ("Play as White", "play_as_white"),
        ("Progressive Pocket", "pocket"),
    ):
        amount = effective.count(item_name) * expected[material_key]
        if amount:
            common_total += amount
            unallocated.append(
                MaterialLedgerEntry(
                    f"unallocated:{item_name}",
                    item_name,
                    amount,
                    None,
                    "outside-roster-projection",
                )
            )
    return pieces, unallocated, common_total


def upgrade_piece(
    contract: ApmwContractV2,
    piece: Piece,
    action: ResolvedAction,
) -> None:
    if piece.final_family != action.from_family:
        raise ProjectionError(
            f"{piece.slot_id} is {piece.final_family}, not {action.from_family}"
        )
    if action.source_role_rule == "establish-minor-slot":
        piece.source_role = MINOR_SLOT
        piece.role_origin_action = action.name
    elif action.source_role_rule == "establish-major-slot":
        piece.source_role = MAJOR_SLOT
        piece.role_origin_action = action.name
    elif action.source_role_rule != "preserve":
        raise ProjectionError(
            f"unsupported source role rule: {action.source_role_rule}"
        )
    incremental = max(
        0,
        contract.expected_material[action.to_family]
        - contract.expected_material[action.from_family],
    )
    piece.granted_material += incremental
    piece.final_family = action.to_family
    append_promotion_entitlement(piece, action.to_family)
    piece.final_expected_material = contract.expected_material[action.to_family]
    piece.upgrade_path.append(action.name)


def upgrade_credit(contract: ApmwContractV2, action: ResolvedAction) -> int:
    return max(
        0,
        contract.expected_material[action.to_family]
        - contract.expected_material[action.from_family],
    )


def append_promotion_entitlement(piece: Piece, family: str) -> None:
    if family not in piece.promotion_entitlement_families:
        piece.promotion_entitlement_families.append(family)


def stable_id(role: str, ordinal: int) -> str:
    return f"{role}:{ordinal:06d}"
