"""Pure semantic roster generation and active/reserve projection for APMW v2."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
from fractions import Fraction
import hashlib
import math
from typing import Any, Iterable

from .contract import ApmwContractV2, GeometryStage


PRIMARY_ROYAL = "primary-royal"
ADDITIONAL_ROYAL = "additional-royal"
LOCKED_CASTLER = "locked-castler"
JACK_SLOT = "jack-slot"
MAJOR_SLOT = "major-slot"
MINOR_SLOT = "minor-slot"
PAWN_SLOT = "pawn-slot"

ROYAL = "royal"
PAWN = "pawn"
MINOR = "minor"
MAJOR = "major"
JACK = "jack"
QUEEN = "queen"
AMAZON = "amazon"

_ROLE_ORDER = (
    PRIMARY_ROYAL,
    ADDITIONAL_ROYAL,
    LOCKED_CASTLER,
    JACK_SLOT,
    MAJOR_SLOT,
    MINOR_SLOT,
    PAWN_SLOT,
)
_FAMILY_ORDER = (ROYAL, PAWN, MINOR, MAJOR, JACK, QUEEN, AMAZON)
_NON_PAWN_ROLES = (ADDITIONAL_ROYAL, LOCKED_CASTLER, JACK_SLOT, MAJOR_SLOT, MINOR_SLOT)
_ORDINARY_NON_PAWN_ROLES = (JACK_SLOT, MAJOR_SLOT, MINOR_SLOT)


class ProjectionError(ValueError):
    """Raised when a semantic projection input violates the accepted contract."""


@dataclass(frozen=True)
class ItemCount:
    name: str
    count: int


@dataclass(frozen=True)
class UnlockCount:
    role_id: str
    count: int


@dataclass(frozen=True)
class UpgradePreference:
    action: str
    priority: int
    proportion_numerator: int = 1
    proportion_denominator: int = 1

    @property
    def proportion(self) -> Fraction:
        if self.proportion_denominator <= 0:
            raise ProjectionError("upgrade proportion denominator must be positive")
        if self.proportion_numerator < 0:
            raise ProjectionError("upgrade proportion numerator must not be negative")
        return Fraction(self.proportion_numerator, self.proportion_denominator)


@dataclass(frozen=True)
class SemanticSeeds:
    pocket_seed: str = "0"
    pawn_seed: str = "0"
    minor_seed: str = "0"
    major_seed: str = "0"
    queen_seed: str = "0"

    @property
    def stable_root(self) -> str:
        return "|".join(
            (
                self.pocket_seed,
                self.pawn_seed,
                self.minor_seed,
                self.major_seed,
                self.queen_seed,
            )
        )


@dataclass(frozen=True)
class ProjectionInput:
    itemization: str
    ordering: str
    seeds: SemanticSeeds = SemanticSeeds()
    item_counts: tuple[ItemCount, ...] = ()
    unlock_counts: tuple[UnlockCount, ...] = ()
    upgrade_preferences: tuple[UpgradePreference, ...] = ()


@dataclass(frozen=True)
class EffectiveCounts:
    items: tuple[ItemCount, ...]
    overcounts: tuple[ItemCount, ...]
    unlocks: tuple[UnlockCount, ...]
    unlock_overcounts: tuple[UnlockCount, ...]

    def count(self, name: str) -> int:
        return next((entry.count for entry in self.items if entry.name == name), 0)


@dataclass(frozen=True)
class OwnedSlot:
    slot_id: str
    source_role: str
    source_ordinal: int
    role_origin_action: str
    final_family: str
    upgrade_path: tuple[str, ...]
    locked_castler: bool
    granted_material: int
    final_expected_material: int
    promotion_entitlement_families: tuple[str, ...]


@dataclass(frozen=True)
class CountByRoleFamily:
    source_role: str
    final_family: str
    count: int


@dataclass(frozen=True)
class MaterialLedgerEntry:
    entry_id: str
    source: str
    amount: int
    slot_id: str | None
    reason: str


@dataclass(frozen=True)
class FormationRankUsage:
    relative_rank: int
    region: str
    capacity: int
    non_pawns: int
    pawns: int
    empty: int


@dataclass(frozen=True)
class SlotPlacement:
    slot_id: str
    file: int
    relative_rank: int
    formation_band: str


@dataclass(frozen=True)
class RegionUsage:
    back_optional_capacity: int
    mixed_capacity: int
    pawn_only_capacity: int
    non_pawn_capacity: int
    gross_pawn_capacity: int
    combined_non_primary_capacity: int
    active_pawn_capacity: int
    back_non_primary: int
    mixed_non_pawns: int
    mixed_pawns: int
    pawn_only_pawns: int
    unused_non_pawn_capacity: int
    unused_pawn_capacity: int
    ranks: tuple[FormationRankUsage, ...]


@dataclass(frozen=True)
class ProjectionResult:
    contract_hash: str
    itemization: str
    ordering: str
    geometry_stage: str
    files: int
    ranks: int
    effective_counts: EffectiveCounts
    owned_slots: tuple[OwnedSlot, ...]
    active_slots: tuple[OwnedSlot, ...]
    reserve_slots: tuple[OwnedSlot, ...]
    active_placements: tuple[SlotPlacement, ...]
    active_counts: tuple[CountByRoleFamily, ...]
    reserve_counts: tuple[CountByRoleFamily, ...]
    active_material_ledger: tuple[MaterialLedgerEntry, ...]
    reserve_material_ledger: tuple[MaterialLedgerEntry, ...]
    dormant_material_ledger: tuple[MaterialLedgerEntry, ...]
    unallocated_material_ledger: tuple[MaterialLedgerEntry, ...]
    owned_expected_material: int
    exact_active_material: int
    active_granted_material: int
    missing_material: int
    dormant_material: int
    unallocated_material: int
    normalized_grant_material: int
    total_accounted_material: int
    active_castlers: tuple[str, ...]
    reserve_castlers: tuple[str, ...]
    castling_eligible_slots: tuple[str, ...]
    available_promotion_families: tuple[str, ...]
    reserve_promotion_families: tuple[str, ...]
    region_usage: RegionUsage
    applied_forwardness: int
    unspent_forwardness: int


@dataclass(frozen=True)
class FundamentalOwnedPlan:
    tier_counts: tuple[tuple[str, int], ...]
    applied_counts: tuple[tuple[str, int], ...]
    spare_material: int
    locked_castlers: int


@dataclass
class _Piece:
    slot_id: str
    source_role: str
    source_ordinal: int
    role_origin_action: str
    origin_family: str
    final_family: str
    upgrade_path: list[str] = field(default_factory=list)
    locked_castler: bool = False
    granted_material: int = 0
    final_expected_material: int = 0
    promotion_entitlement_families: list[str] = field(default_factory=list)
    alive: bool = True

    def freeze(self) -> OwnedSlot:
        return OwnedSlot(
            self.slot_id,
            self.source_role,
            self.source_ordinal,
            self.role_origin_action,
            self.final_family,
            tuple(self.upgrade_path),
            self.locked_castler,
            self.granted_material,
            self.final_expected_material,
            tuple(self.promotion_entitlement_families),
        )


class CounterBasedSeedSeries:
    """Exact Python wire twin of C# CounterBasedSeedSeries."""

    def __init__(self, root: str | None, series_id: str | None):
        self.root = root or ""
        self.series_id = series_id or ""

    def value(self, counter: int) -> int:
        payload = f"{self.root}\n{self.series_id}\n{counter}".encode("utf-8")
        return int.from_bytes(hashlib.sha256(payload).digest()[:8], "big")

    def index(self, counter: int, count: int) -> int:
        if count <= 0:
            raise ProjectionError("series index count must be positive")
        return self.value(counter) % count

    def unit(self, counter: int) -> float:
        return (self.value(counter) >> 11) * (1.0 / (1 << 53))

    def choose(self, counter: int, values: list[Any]) -> Any:
        if not values:
            raise ProjectionError(
                f"cannot choose from empty semantic series {self.series_id}"
            )
        return values[self.index(counter, len(values))]


@dataclass(frozen=True)
class _Action:
    name: str
    from_family: str
    to_family: str
    source_role_rule: str
    priority: int
    proportion: Fraction


@dataclass(frozen=True)
class _FundamentalPlan:
    tier_counts: dict[str, int]
    applied_counts: dict[str, int]
    spare_material: int
    locked_castlers: int


@dataclass(frozen=True)
class _LegacyPlan:
    direct_counts: dict[str, int]
    planned_actions: tuple[tuple[_Action, int], ...]
    unused_upgrade_counts: dict[str, int]


_FUNDAMENTAL_ACTION_ORDER = (
    "pawn-to-minor",
    "pawn-to-major",
    "minor-to-major",
    "major-to-jack",
    "minor-to-jack",
    "major-to-queen",
    "jack-to-queen",
    "queen-to-amazon",
)
_LEGACY_ACTION_ORDER = (
    "minor-to-major",
    "major-to-jack",
    "minor-to-jack",
    "major-to-queen",
    "jack-to-queen",
    "queen-to-amazon",
)


_DEFAULT_LEGACY_PREFERENCES = (
    UpgradePreference("major-to-queen", 1),
)
_DEFAULT_FUNDAMENTAL_PREFERENCES = (
    UpgradePreference("pawn-to-minor", 1),
    UpgradePreference("minor-to-major", 1),
    UpgradePreference("pawn-to-major", 1),
    UpgradePreference("major-to-queen", 1),
)


def project_semantic_roster(contract: ApmwContractV2, projection_input: ProjectionInput) -> ProjectionResult:
    """Generate an owned roster and project it onto the largest unlocked valid geometry."""
    effective, stage, pieces, dormant, unallocated, normalized_grant = _prepare_projection(
        contract, projection_input
    )
    return _project(
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
    """Project only the exact active material, skipping placement and ledger construction."""
    _, stage, pieces, _, _, _ = _prepare_projection(contract, projection_input)
    active, _ = _select_active_slots(
        contract, stage, [piece.freeze() for piece in pieces]
    )
    return sum(piece.final_expected_material for piece in active)


def project_exact_active_non_primary_count(
    contract: ApmwContractV2, projection_input: ProjectionInput
) -> int:
    """Project only the active roster size, excluding the primary royal."""
    _, stage, pieces, _, _, _ = _prepare_projection(contract, projection_input)
    active, _ = _select_active_slots(
        contract, stage, [piece.freeze() for piece in pieces]
    )
    return sum(piece.source_role != PRIMARY_ROYAL for piece in active)


def _prepare_projection(
    contract: ApmwContractV2, projection_input: ProjectionInput
) -> tuple[
    EffectiveCounts,
    GeometryStage,
    list[_Piece],
    list[MaterialLedgerEntry],
    list[MaterialLedgerEntry],
    int,
]:
    _validate_mode(contract, projection_input)
    effective = _normalize_counts(contract, projection_input)
    stage = _select_geometry(contract, effective.unlocks)
    actions = _resolve_actions(contract, projection_input)
    semantic_root = projection_input.seeds.stable_root

    if projection_input.itemization == "legacy":
        pieces, dormant, unallocated, normalized_grant = _generate_legacy(
            contract, effective, actions, semantic_root
        )
    else:
        pieces, dormant, unallocated, normalized_grant = _generate_fundamental(
            contract, effective, actions, semantic_root
        )
    expected_grant = _expected_normalized_grant_from_effective(
        contract,
        projection_input.itemization,
        effective,
        actions,
        semantic_root,
    )
    if normalized_grant != expected_grant:
        raise ProjectionError(
            f"ownership grant calculation drifted: {normalized_grant} != {expected_grant}"
        )
    return effective, stage, pieces, dormant, unallocated, expected_grant


def projection_to_dict(result: ProjectionResult) -> dict[str, Any]:
    """Return a JSON-compatible representation with deterministic field and tuple ordering."""
    return _json_value(result)


def expected_normalized_grant_material(
    contract: ApmwContractV2, projection_input: ProjectionInput
) -> int:
    """Calculate normalized input grant material without using projected ledgers."""
    _validate_mode(contract, projection_input)
    effective = _normalize_counts(contract, projection_input)
    actions = _resolve_actions(contract, projection_input)
    return _expected_normalized_grant_from_effective(
        contract,
        projection_input.itemization,
        effective,
        actions,
        projection_input.seeds.stable_root,
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
        raise ProjectionError("Fundamental characterization counts must not be negative")
    projection_input = ProjectionInput(
        "fundamental",
        "stable",
        seeds,
        (),
        (),
        upgrade_preferences,
    )
    actions = _resolve_actions(contract, projection_input)
    plan = _simulate_fundamental(
        contract,
        chessmen,
        material_budget,
        min(castlers, contract.castler.maximum),
        actions,
        seeds.stable_root,
    )
    return FundamentalOwnedPlan(
        tuple((family, plan.tier_counts[family]) for family in (PAWN, MINOR, MAJOR, JACK, QUEEN, AMAZON)),
        tuple(sorted(plan.applied_counts.items())),
        plan.spare_material,
        plan.locked_castlers,
    )


def projection_input_from_dict(value: dict[str, Any]) -> ProjectionInput:
    """Parse the fixture/API representation into immutable typed input."""
    return ProjectionInput(
        itemization=str(value["itemization"]),
        ordering=str(value["ordering"]),
        seeds=SemanticSeeds(
            **{
                key: str(seed_value)
                for key, seed_value in value.get("seeds", {}).items()
            }
        ),
        item_counts=tuple(
            ItemCount(str(name), int(count))
            for name, count in sorted(value.get("item_counts", {}).items())
        ),
        unlock_counts=tuple(
            UnlockCount(str(role_id), int(count))
            for role_id, count in sorted(value.get("unlock_counts", {}).items())
        ),
        upgrade_preferences=tuple(
            UpgradePreference(
                str(entry["action"]),
                int(entry["priority"]),
                int(entry.get("proportion_numerator", 1)),
                int(entry.get("proportion_denominator", 1)),
            )
            for entry in value.get("upgrade_preferences", ())
        ),
    )


def _json_value(value: Any) -> Any:
    if is_dataclass(value):
        return {key: _json_value(item) for key, item in asdict(value).items()}
    if isinstance(value, tuple):
        return [_json_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _json_value(item) for key, item in value.items()}
    return value


def _validate_mode(contract: ApmwContractV2, projection_input: ProjectionInput) -> None:
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
            raise ProjectionError(f"item count for {entry.name} must not be negative")
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

    unlock_roles = {role.role_id: role for role in contract.geometry_unlocks.roles}
    raw_unlocks: dict[str, int] = {}
    for entry in projection_input.unlock_counts:
        if entry.role_id not in unlock_roles:
            raise ProjectionError(f"unknown geometry unlock role: {entry.role_id}")
        if entry.count < 0:
            raise ProjectionError(
                f"unlock count for {entry.role_id} must not be negative"
            )
        raw_unlocks[entry.role_id] = raw_unlocks.get(entry.role_id, 0) + entry.count

    unlocks: list[UnlockCount] = []
    unlock_overcounts: list[UnlockCount] = []
    for role_id, role in sorted(unlock_roles.items()):
        maximum_steps = (role.maximum - role.base) // role.increment
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
    contract: ApmwContractV2, unlocks: tuple[UnlockCount, ...]
) -> GeometryStage:
    counts = {entry.role_id: entry.count for entry in unlocks}
    role_by_id = {role.role_id: role for role in contract.geometry_unlocks.roles}
    file_role = role_by_id["board-file-unlock"]
    rank_role = role_by_id["board-rank-unlock"]
    unlocked_files = min(
        file_role.maximum,
        file_role.base + file_role.increment * counts.get(file_role.role_id, 0),
    )
    unlocked_ranks = min(
        rank_role.maximum,
        rank_role.base + rank_role.increment * counts.get(rank_role.role_id, 0),
    )
    candidates = [
        stage
        for stage in contract.stages
        if stage.files <= unlocked_files and stage.ranks <= unlocked_ranks
    ]
    if not candidates:
        raise ProjectionError(
            f"no valid geometry is unlocked by {unlocked_files}x{unlocked_ranks}"
        )
    order = {stage_id: index for index, stage_id in enumerate(contract.stage_order)}
    return max(candidates, key=lambda stage: order[stage.stage_id])


def _resolve_actions(
    contract: ApmwContractV2, projection_input: ProjectionInput
) -> tuple[_Action, ...]:
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
            _Action(
                transition.action,
                transition.from_family,
                transition.to_family,
                transition.source_role_rule,
                preference.priority,
                preference.proportion,
            )
        )
    return tuple(actions)


def _primary_and_common(
    contract: ApmwContractV2,
    effective: EffectiveCounts,
) -> tuple[list[_Piece], list[MaterialLedgerEntry], int]:
    expected = contract.expected_material
    king_promotions = effective.count("Progressive King Promotion")
    primary_material = king_promotions * expected["king_promotion"]
    pieces = [
        _Piece(
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
            _Piece(
                _stable_id(ADDITIONAL_ROYAL, ordinal),
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


def _expected_normalized_grant_from_effective(
    contract: ApmwContractV2,
    itemization: str,
    effective: EffectiveCounts,
    actions: tuple[_Action, ...],
    semantic_root: str,
) -> int:
    expected = contract.expected_material
    _, _, common_total = _primary_and_common(contract, effective)
    if itemization == "fundamental":
        return (
            common_total
            + effective.count("Chessmen") * expected[PAWN]
            + effective.count("Material") * expected["material_item"]
        )

    plan = _plan_legacy(effective, actions, semantic_root)
    return (
        common_total
        + effective.count("Progressive Pawn") * expected[PAWN]
        + sum(
            plan.direct_counts[family] * expected[family]
            for family in (MINOR, MAJOR, JACK)
        )
        + sum(
            count * _upgrade_credit(contract, action)
            for action, count in plan.planned_actions
        )
        + plan.unused_upgrade_counts[QUEEN]
        * (expected[QUEEN] - expected[MAJOR])
        + plan.unused_upgrade_counts[AMAZON]
        * (expected[AMAZON] - expected[QUEEN])
    )


def _generate_legacy(
    contract: ApmwContractV2,
    effective: EffectiveCounts,
    actions: tuple[_Action, ...],
    semantic_root: str,
) -> tuple[
    list[_Piece],
    list[MaterialLedgerEntry],
    list[MaterialLedgerEntry],
    int,
]:
    expected = contract.expected_material
    pieces, unallocated, common_total = _primary_and_common(contract, effective)
    plan = _plan_legacy(effective, actions, semantic_root)

    for family, role in (
        (MINOR, MINOR_SLOT),
        (MAJOR, MAJOR_SLOT),
        (JACK, JACK_SLOT),
    ):
        for ordinal in range(plan.direct_counts[family]):
            pieces.append(
                _Piece(
                    _stable_id(role, ordinal),
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
            _upgrade_piece(contract, piece, action)

    pawn_count = effective.count("Progressive Pawn")
    for ordinal in range(pawn_count):
        pieces.append(
            _Piece(
                _stable_id(PAWN_SLOT, ordinal),
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
            count * _upgrade_credit(contract, action)
            for action, count in plan.planned_actions
        )
        + sum(entry.amount for entry in dormant)
    )
    return pieces, dormant, unallocated, normalized_grant


def _plan_legacy(
    effective: EffectiveCounts,
    actions: tuple[_Action, ...],
    semantic_root: str,
) -> _LegacyPlan:
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
        for name in _LEGACY_ACTION_ORDER
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
            viable: list[_Action] = []
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
                chosen = _legacy_weighted_choice(
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
    return _LegacyPlan(
        direct,
        planned,
        {QUEEN: remaining[QUEEN], AMAZON: remaining[AMAZON]},
    )


def _legacy_weighted_choice(
    semantic_root: str,
    actions: list[_Action],
    weights: list[float],
    counters: dict[str, int],
) -> _Action:
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
    for origin in (source,) + tuple(family for family in families if family != source):
        if current[(source, origin)] <= 0:
            continue
        current[(source, origin)] -= 1
        current[(target, origin)] += 1
        return


def _generate_fundamental(
    contract: ApmwContractV2,
    effective: EffectiveCounts,
    actions: tuple[_Action, ...],
    semantic_root: str,
) -> tuple[
    list[_Piece],
    list[MaterialLedgerEntry],
    list[MaterialLedgerEntry],
    int,
]:
    expected = contract.expected_material
    pieces, unallocated, common_total = _primary_and_common(contract, effective)
    chessmen = effective.count("Chessmen")
    plan = _plan_fundamental(contract, effective, actions, semantic_root)

    chessmen_pieces = [
        _Piece(
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
        _append_promotion_entitlement(piece, MAJOR)
        piece.locked_castler = True
        piece.granted_material += contract.castler.normalized_cost
        piece.final_expected_material = expected[MAJOR]

    minor_ordinal = 0
    major_ordinal = 0
    minor_ordinal = _apply_fundamental_gateway(
        contract,
        chessmen_pieces,
        semantic_root,
        plan.applied_counts.get("pawn-to-minor", 0),
        "pawn-to-minor",
        MINOR_SLOT,
        MINOR,
        minor_ordinal,
    )
    major_ordinal = _apply_fundamental_gateway(
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
            _upgrade_piece(contract, piece, action)

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
            _append_promotion_entitlement(piece, JACK)
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
        _append_promotion_entitlement(pawn, PAWN)
    normalized_grant = (
        common_total
        + chessmen * expected[PAWN]
        + effective.count("Material") * expected["material_item"]
    )
    return pieces, [], unallocated, normalized_grant


def _plan_fundamental(
    contract: ApmwContractV2,
    effective: EffectiveCounts,
    actions: tuple[_Action, ...],
    semantic_root: str,
) -> _FundamentalPlan:
    expected = contract.expected_material
    return _simulate_fundamental(
        contract,
        effective.count("Chessmen"),
        effective.count("Material") * expected["material_item"],
        effective.count("Castler"),
        actions,
        semantic_root,
    )


def _simulate_fundamental(
    contract: ApmwContractV2,
    chessmen: int,
    material_budget: int,
    castlers: int,
    actions: tuple[_Action, ...],
    semantic_root: str,
) -> _FundamentalPlan:
    expected = contract.expected_material
    spare_material = material_budget
    locked = min(
        castlers,
        contract.castler.maximum,
        chessmen,
        spare_material // contract.castler.normalized_cost,
    )
    spare_material -= locked * contract.castler.normalized_cost
    tiers = {family: 0 for family in (PAWN, MINOR, MAJOR, JACK, QUEEN, AMAZON)}
    tiers[PAWN] = chessmen - locked
    tiers[MAJOR] = locked

    action_by_name = {action.name: action for action in actions}
    ordered = [
        action_by_name[name]
        for name in _FUNDAMENTAL_ACTION_ORDER
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
            viable: list[_Action] = []
            weights: list[float] = []
            for action in groups[priority]:
                eligible = tiers[action.from_family]
                if action.from_family == MAJOR:
                    eligible -= locked
                credit = _upgrade_credit(contract, action)
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
                chosen = _fundamental_weighted_choice(
                    semantic_root, priority, counter, viable, weights
                )
                tie_counters[priority] = counter + 1
            credit = _upgrade_credit(contract, chosen)
            spare_material -= credit
            tiers[chosen.from_family] -= 1
            tiers[chosen.to_family] += 1
            applied[chosen.name] = applied.get(chosen.name, 0) + 1
            did_apply = True
            break
        if not did_apply:
            break
    return _FundamentalPlan(tiers, applied, spare_material, locked)


def _fundamental_weighted_choice(
    semantic_root: str,
    priority: int,
    counter: int,
    actions: list[_Action],
    weights: list[float],
) -> _Action:
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


def _apply_fundamental_gateway(
    contract: ApmwContractV2,
    pieces: list[_Piece],
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
        _append_promotion_entitlement(piece, family)
        credit = contract.expected_material[family] - contract.expected_material[PAWN]
        piece.granted_material += credit
        piece.final_expected_material = contract.expected_material[family]
    return role_ordinal


def _upgrade_piece(
    contract: ApmwContractV2,
    piece: _Piece,
    action: _Action,
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
    _append_promotion_entitlement(piece, action.to_family)
    piece.final_expected_material = contract.expected_material[action.to_family]
    piece.upgrade_path.append(action.name)


def _upgrade_credit(contract: ApmwContractV2, action: _Action) -> int:
    return max(
        0,
        contract.expected_material[action.to_family]
        - contract.expected_material[action.from_family],
    )


def _append_promotion_entitlement(piece: _Piece, family: str) -> None:
    if family not in piece.promotion_entitlement_families:
        piece.promotion_entitlement_families.append(family)


def _stable_id(role: str, ordinal: int) -> str:
    return f"{role}:{ordinal:06d}"


def _project(
    contract: ApmwContractV2,
    projection_input: ProjectionInput,
    effective: EffectiveCounts,
    stage: GeometryStage,
    pieces: list[_Piece],
    dormant: list[MaterialLedgerEntry],
    unallocated: list[MaterialLedgerEntry],
    normalized_grant_material: int,
) -> ProjectionResult:
    frozen = [piece.freeze() for piece in pieces]
    active, reserve = _select_active_slots(contract, stage, frozen)

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
        family for family in _FAMILY_ORDER if family in active_entitlements
    )
    reserve_families = tuple(
        family for family in _FAMILY_ORDER if family in reserve_entitlements
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


def _select_active_slots(
    contract: ApmwContractV2,
    stage: GeometryStage,
    frozen: list[OwnedSlot],
) -> tuple[tuple[OwnedSlot, ...], tuple[OwnedSlot, ...]]:
    by_role = {
        role: [piece for piece in frozen if piece.source_role == role]
        for role in _ROLE_ORDER
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
        if piece.slot_id in active_ids and piece.source_role in _NON_PAWN_ROLES
    )
    remaining_non_pawn = max(0, stage.non_pawn_capacity - active_non_pawn_count)
    for role in _ORDINARY_NON_PAWN_ROLES:
        selected = _activation_order(by_role[role])[:remaining_non_pawn]
        active_ids.update(piece.slot_id for piece in selected)
        remaining_non_pawn -= len(selected)

    active_non_pawn_count = sum(
        1
        for piece in frozen
        if piece.slot_id in active_ids and piece.source_role in _NON_PAWN_ROLES
    )
    active_pawn_capacity = contract.pawn_capacity_formula.active_pawn_capacity(
        stage.files,
        stage.gross_pawn_capacity,
        active_non_pawn_count,
    )
    selected_pawns = _activation_order(by_role[PAWN_SLOT])[:active_pawn_capacity]
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
    return (_ROLE_ORDER.index(piece.source_role), piece.source_ordinal, piece.slot_id)


def _reserve_sort_key(piece: OwnedSlot) -> tuple[int, int, int, int, str]:
    return (
        _ROLE_ORDER.index(piece.source_role),
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
        for role in _ROLE_ORDER
        for family in _FAMILY_ORDER
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
        1 for piece in active if piece.source_role in _NON_PAWN_ROLES
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
    mixed_non_pawns = sum(rank.non_pawns for rank in ranks if rank.region == "mixed")
    mixed_pawns = sum(rank.pawns for rank in ranks if rank.region == "mixed")
    pawn_only_pawns = sum(rank.pawns for rank in ranks if rank.region == "pawn-only")
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
        raise ProjectionError("active projection selected slots that could not be placed")
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
        raise ProjectionError("source role exceeded its assigned placement region")


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
