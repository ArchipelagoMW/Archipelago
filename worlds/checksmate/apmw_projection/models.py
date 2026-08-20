"""Shared immutable models and wire serialization for APMW projection."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
from fractions import Fraction
import hashlib
from typing import Any, Sequence, TypeVar


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

ROLE_ORDER = (
    PRIMARY_ROYAL,
    ADDITIONAL_ROYAL,
    LOCKED_CASTLER,
    JACK_SLOT,
    MAJOR_SLOT,
    MINOR_SLOT,
    PAWN_SLOT,
)
FAMILY_ORDER = (ROYAL, PAWN, MINOR, MAJOR, JACK, QUEEN, AMAZON)
NON_PAWN_ROLES = (
    ADDITIONAL_ROYAL,
    LOCKED_CASTLER,
    JACK_SLOT,
    MAJOR_SLOT,
    MINOR_SLOT,
)
ORDINARY_NON_PAWN_ROLES = (JACK_SLOT, MAJOR_SLOT, MINOR_SLOT)


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
class Piece:
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


_Choice = TypeVar("_Choice")


class CounterBasedSeedSeries:
    """Exact Python wire twin of C# CounterBasedSeedSeries."""

    def __init__(self, root: str | None, series_id: str | None) -> None:
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

    def choose(self, counter: int, values: Sequence[_Choice]) -> _Choice:
        if not values:
            raise ProjectionError(
                f"cannot choose from empty semantic series {self.series_id}"
            )
        return values[self.index(counter, len(values))]


def projection_to_dict(result: ProjectionResult) -> dict[str, Any]:
    """Return a JSON-compatible representation with deterministic field ordering."""
    return _json_value(result)


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
