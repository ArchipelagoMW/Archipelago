"""Strict parser for the shared, non-live APMW contract v2 manifest.

Canonical hashing decodes JSON while rejecting duplicate keys, replaces the
root ``manifest_sha256`` value with ``""``, sorts every object by ordinal key,
preserves array order, emits printable ASCII without insignificant whitespace,
and hashes the resulting UTF-8 bytes with SHA-256. Only integers, booleans,
printable ASCII strings, arrays, and objects are allowed.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
from types import MappingProxyType
from typing import Any, Mapping


SUPPORTED_MAJOR = 2
SUPPORTED_MINOR = 0

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_SEMVER_RE = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")
_STAGE_RE = re.compile(r"^([1-9][0-9]*)x([1-9][0-9]*)$")

_ITEMIZATION_MODES = ("legacy", "fundamental")
_ORDERING_MODES = ("stable", "chaos")
_MODE_COMBINATIONS = (
    ("legacy", "stable", "stable-legacy", True, True, False, True, True, True),
    ("legacy", "chaos", "chaos-legacy", True, True, False, False, True, True),
    ("fundamental", "stable", "stable-fundamental", True, True, False, False, True, True),
)
_FILE_LADDER = (8, 10, 12)
_RANK_LADDER = (8, 10, 12)
_STAGE_ORDER = ("8x8", "10x8", "10x10", "12x10", "12x12")
_ALGORITHMS = {
    "capacity": "expanded-formation-v2",
    "projection": "placement-role-material-v2",
    "overflow": "material-first-reserve-v2",
    "ordering": "independent-semantic-series-v1",
    "series_prf": "sha256-counter-v1",
}
_EXPECTED_MATERIAL = {
    "weak": 75,
    "pawn": 100,
    "minor": 300,
    "major": 485,
    "castler": 500,
    "jack": 700,
    "queen": 900,
    "amazon": 1300,
    "material_item": 400,
    "play_as_white": 50,
    "pocket": 110,
    "consul": 325,
    "king_promotion": 425,
}
_SOURCE_ROLES = (
    "primary-royal",
    "additional-royal",
    "locked-castler",
    "jack-slot",
    "major-slot",
    "minor-slot",
    "pawn-slot",
)
_FINAL_FAMILIES = ("pawn", "minor", "major", "jack", "queen", "amazon")
_PAWN_CREATION_ACTIONS = ("new-pawn", "more-pawn")
_UPGRADE_TRANSITIONS = (
    ("better-pawn", "pawn", "pawn", ("pawn-slot",), "preserve"),
    ("pool-pawn-upgrade", "pawn", "pawn", ("pawn-slot",), "preserve"),
    ("pawn-to-minor", "pawn", "minor", ("pawn-slot",), "establish-minor-slot"),
    ("pawn-to-major", "pawn", "major", ("pawn-slot",), "establish-major-slot"),
    ("minor-to-major", "minor", "major", ("minor-slot",), "preserve"),
    ("minor-to-jack", "minor", "jack", ("minor-slot",), "preserve"),
    ("major-to-jack", "major", "jack", ("major-slot", "minor-slot"), "preserve"),
    ("major-to-queen", "major", "queen", ("major-slot", "minor-slot"), "preserve"),
    (
        "jack-to-queen",
        "jack",
        "queen",
        ("jack-slot", "major-slot", "minor-slot"),
        "preserve",
    ),
    (
        "queen-to-amazon",
        "queen",
        "amazon",
        ("jack-slot", "major-slot", "minor-slot"),
        "preserve",
    ),
)
_SEMANTIC_SERIES_IDS = (
    "fundamental.wave.tie.{priority}",
    "fundamental.gateway.role",
    "fundamental.omission.{source-role}",
    "upgrade-source.{action}",
)
_PRESENTATION_SERIES_IDS = (
    "placement.{source-role}.{formation-band}",
    "piece-type.{final-family}",
    "upgrade-target.{action}",
    "pocket.choice",
)
_COMMON_MAXIMA = {
    "Play as White": 1,
    "Progressive AI Intelligence Malus": 5,
    "Progressive Pocket": 12,
    "Progressive Pocket Range": 6,
    "Progressive King Promotion": 2,
    "Progressive Consul": 2,
}
_LEGACY_MAXIMA = {
    "Progressive Pawn": 60,
    "Progressive Pawn Forwardness": 13,
    "Progressive Minor Piece": 15,
    "Progressive Major Piece": 11,
    "Progressive Major To Queen": 9,
    "Progressive Jack": 9,
}
_FUNDAMENTAL_MAXIMA = {
    "Chessmen": 107,
    "Material": 321,
    "Castler": 2,
}


class ApmwContractError(ValueError):
    """Raised when an APMW contract manifest is not valid for this parser."""


@dataclass(frozen=True)
class ContractVersion:
    major: int
    minor: int


@dataclass(frozen=True)
class Geometry:
    files: int
    ranks: int

    @property
    def stage_id(self) -> str:
        return f"{self.files}x{self.ranks}"


@dataclass(frozen=True)
class GeometryStage:
    stage_id: str
    files: int
    ranks: int
    deployment_depth: int
    combined_non_primary_capacity: int
    gross_pawn_capacity: int
    forwardness_capacity: int
    non_pawn_capacity: int
    cpu_pawn_count: int
    cpu_non_king_count: int
    all_tactics_locations: int
    turns_locations: int
    no_tactics_locations: int


@dataclass(frozen=True)
class ModeCombination:
    itemization: str
    ordering: str
    semantic_id: str
    permanent: bool
    semantic_snapshot_deterministic: bool
    experiential_prefix_stable: bool
    planned_series_prefix_stable: bool
    semantic_series_isolated: bool
    aggregate_semantics_presentation_independent: bool


@dataclass(frozen=True)
class GeometryUnlockRole:
    role_id: str
    base: int
    increment: int
    maximum: int


@dataclass(frozen=True)
class GeometryUnlocks:
    roles: tuple[GeometryUnlockRole, ...]
    selection_policy: str


@dataclass(frozen=True)
class PawnCapacityFormula:
    gross_pawn_capacity_algorithm: str
    non_pawns_beyond_back_algorithm: str
    active_pawn_capacity_algorithm: str
    back_rank_primary_royal_slots: int

    def non_pawns_beyond_back(self, width: int, active_non_primary_non_pawns: int) -> int:
        return max(0, active_non_primary_non_pawns - (width - self.back_rank_primary_royal_slots))

    def active_pawn_capacity(
        self,
        width: int,
        gross_pawn_capacity: int,
        active_non_primary_non_pawns: int,
    ) -> int:
        return gross_pawn_capacity - self.non_pawns_beyond_back(
            width, active_non_primary_non_pawns
        )


@dataclass(frozen=True)
class UpgradeTransition:
    action: str
    from_family: str
    to_family: str
    allowed_source_roles: tuple[str, ...]
    source_role_rule: str


@dataclass(frozen=True)
class UpgradeDag:
    final_families: tuple[str, ...]
    pawn_creation_actions: tuple[str, ...]
    pawn_creation_source_role: str
    transitions: tuple[UpgradeTransition, ...]


@dataclass(frozen=True)
class CastlerSemantics:
    source_role: str
    reclassifies_existing_chessman: bool
    source_role_immutable: bool
    normalized_material: int
    normalized_cost: int
    maximum: int
    adds_chessman: bool
    requires_existing_chessman: bool
    occupies_board_slot: bool
    target_families: tuple[str, ...]
    upgrade_ceiling: str
    protected_from_higher_upgrades: bool
    ordinary_omission_protection: str
    castling_eligibility: str


@dataclass(frozen=True)
class OverflowPolicy:
    policy_id: str
    role_priority: tuple[str, ...]
    within_role_activation_order: tuple[str, ...]
    reserve_entry_order: tuple[str, ...]
    missing_material_accounting: str
    material_first_activation: bool
    larger_geometry_reactivates_reserves: bool
    ordinary_omission_protected_roles: tuple[str, ...]
    aggregate_semantics_ignore_presentation: bool
    chaos_nonce_scope: str


@dataclass(frozen=True)
class CpuProfiles:
    layout_version: str
    location_profile_version: str
    army_ids: tuple[str, ...]


@dataclass(frozen=True)
class ApmwContractV2:
    version: ContractVersion
    manifest_sha256: str
    minimum_client_version: str
    minor_compatibility: str
    itemization_modes: tuple[str, ...]
    ordering_modes: tuple[str, ...]
    mode_combinations: tuple[ModeCombination, ...]
    base_geometry: Geometry
    file_ladder: tuple[int, ...]
    rank_ladder: tuple[int, ...]
    stage_order: tuple[str, ...]
    stages: tuple[GeometryStage, ...]
    geometry_unlocks: GeometryUnlocks
    pawn_capacity_formula: PawnCapacityFormula
    algorithms: Mapping[str, str]
    expected_material: Mapping[str, int]
    source_roles: tuple[str, ...]
    upgrade_dag: UpgradeDag
    castler: CastlerSemantics
    semantic_series_ids: tuple[str, ...]
    presentation_series_ids: tuple[str, ...]
    overflow_policy: OverflowPolicy
    cpu_profiles: CpuProfiles
    effective_item_maxima: Mapping[str, Mapping[str, int]]


def _reject_float(value: str) -> None:
    raise ApmwContractError(f"JSON numbers must be integers, not {value}")


def _pairs_to_dict(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ApmwContractError(f"duplicate JSON property: {key}")
        result[key] = value
    return result


def _decode_json(text: str) -> dict[str, Any]:
    try:
        value = json.loads(
            text,
            object_pairs_hook=_pairs_to_dict,
            parse_float=_reject_float,
            parse_constant=_reject_float,
        )
    except (json.JSONDecodeError, TypeError) as exc:
        raise ApmwContractError(f"invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ApmwContractError("manifest root must be an object")
    return value


def _validate_ascii(value: str, path: str) -> None:
    if any(ord(char) < 0x20 or ord(char) > 0x7E for char in value):
        raise ApmwContractError(f"{path} must be printable ASCII")


def _canonical_string(value: str, path: str) -> str:
    _validate_ascii(value, path)
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _canonical_json(value: Any, path: str = "$") -> str:
    if isinstance(value, dict):
        parts = []
        for key in sorted(value):
            if not isinstance(key, str):
                raise ApmwContractError(f"{path} has a non-string object key")
            parts.append(
                f"{_canonical_string(key, path + '.<key>')}:{_canonical_json(value[key], path + '.' + key)}"
            )
        return "{" + ",".join(parts) + "}"
    if isinstance(value, list):
        return "[" + ",".join(_canonical_json(item, f"{path}[{index}]") for index, item in enumerate(value)) + "]"
    if isinstance(value, str):
        return _canonical_string(value, path)
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        if value < -(2**63) or value > 2**63 - 1:
            raise ApmwContractError(f"{path} integer is outside signed 64-bit range")
        return str(value)
    raise ApmwContractError(f"{path} contains unsupported JSON value {type(value).__name__}")


def compute_manifest_sha256(text: str) -> str:
    """Compute the contract hash after blanking the root hash field."""
    root = _decode_json(text)
    if "manifest_sha256" not in root:
        raise ApmwContractError("manifest_sha256 is required for canonical hashing")
    root["manifest_sha256"] = ""
    canonical = _canonical_json(root)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _object(value: Any, path: str, fields: set[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ApmwContractError(f"{path} must be an object")
    actual = set(value)
    if actual != fields:
        missing = sorted(fields - actual)
        unknown = sorted(actual - fields)
        raise ApmwContractError(f"{path} fields differ; missing={missing}, unknown={unknown}")
    return value


def _array(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        raise ApmwContractError(f"{path} must be an array")
    return value


def _string(value: Any, path: str) -> str:
    if not isinstance(value, str):
        raise ApmwContractError(f"{path} must be a string")
    _validate_ascii(value, path)
    if not value:
        raise ApmwContractError(f"{path} must not be empty")
    return value


def _integer(value: Any, path: str, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ApmwContractError(f"{path} must be an integer")
    if value < minimum or value > 2**31 - 1:
        raise ApmwContractError(f"{path} must be between {minimum} and {2**31 - 1}")
    return value


def _boolean(value: Any, path: str) -> bool:
    if not isinstance(value, bool):
        raise ApmwContractError(f"{path} must be a boolean")
    return value


def _string_tuple(value: Any, path: str) -> tuple[str, ...]:
    result = tuple(_string(item, f"{path}[{index}]") for index, item in enumerate(_array(value, path)))
    if len(result) != len(set(result)):
        raise ApmwContractError(f"{path} contains duplicates")
    return result


def _int_tuple(value: Any, path: str) -> tuple[int, ...]:
    return tuple(_integer(item, f"{path}[{index}]", 1) for index, item in enumerate(_array(value, path)))


def _require_exact(actual: Any, expected: Any, path: str) -> None:
    if actual != expected:
        raise ApmwContractError(f"{path} must equal the frozen v2.0 value")


def _parse_int_map(value: Any, path: str) -> dict[str, int]:
    if not isinstance(value, dict):
        raise ApmwContractError(f"{path} must be an object")
    result: dict[str, int] = {}
    for key, item in value.items():
        _validate_ascii(key, f"{path}.<key>")
        result[key] = _integer(item, f"{path}.{key}")
    return result


def parse_contract(text: str) -> ApmwContractV2:
    root = _object(
        _decode_json(text),
        "$",
        {
            "schema",
            "version",
            "manifest_sha256",
            "minimum_client_version",
            "minor_compatibility",
            "itemization_modes",
            "ordering_modes",
            "mode_combinations",
            "geometry",
            "algorithms",
            "expected_material",
            "source_roles",
            "upgrade_dag",
            "castler",
            "semantic_series_ids",
            "presentation_series_ids",
            "overflow_policy",
            "cpu_profiles",
            "effective_item_maxima",
        },
    )
    if _string(root["schema"], "$.schema") != "apmw_contract":
        raise ApmwContractError("$.schema must be apmw_contract")

    version_data = _object(root["version"], "$.version", {"major", "minor"})
    version = ContractVersion(
        _integer(version_data["major"], "$.version.major"),
        _integer(version_data["minor"], "$.version.minor"),
    )
    if version.major != SUPPORTED_MAJOR:
        raise ApmwContractError(f"unsupported contract major version {version.major}")
    if version.minor > SUPPORTED_MINOR:
        raise ApmwContractError(
            f"unsupported contract minor version {version.minor}; parser supports through {SUPPORTED_MINOR}"
        )

    manifest_hash = _string(root["manifest_sha256"], "$.manifest_sha256")
    if not _SHA256_RE.fullmatch(manifest_hash):
        raise ApmwContractError("$.manifest_sha256 must be 64 lowercase hexadecimal characters")
    minimum_client_version = _string(root["minimum_client_version"], "$.minimum_client_version")
    if not _SEMVER_RE.fullmatch(minimum_client_version):
        raise ApmwContractError("$.minimum_client_version must be a three-part semantic version")
    minor_compatibility = _string(root["minor_compatibility"], "$.minor_compatibility")
    _require_exact(minor_compatibility, "same-or-older", "$.minor_compatibility")

    itemization_modes = _string_tuple(root["itemization_modes"], "$.itemization_modes")
    ordering_modes = _string_tuple(root["ordering_modes"], "$.ordering_modes")
    _require_exact(itemization_modes, _ITEMIZATION_MODES, "$.itemization_modes")
    _require_exact(ordering_modes, _ORDERING_MODES, "$.ordering_modes")

    combinations = []
    for index, raw_combination in enumerate(_array(root["mode_combinations"], "$.mode_combinations")):
        path = f"$.mode_combinations[{index}]"
        combination = _object(
            raw_combination,
            path,
            {
                "itemization",
                "ordering",
                "semantic_id",
                "permanent",
                "semantic_snapshot_deterministic",
                "experiential_prefix_stable",
                "planned_series_prefix_stable",
                "semantic_series_isolated",
                "aggregate_semantics_presentation_independent",
            },
        )
        combinations.append(
            ModeCombination(
                _string(combination["itemization"], path + ".itemization"),
                _string(combination["ordering"], path + ".ordering"),
                _string(combination["semantic_id"], path + ".semantic_id"),
                _boolean(combination["permanent"], path + ".permanent"),
                _boolean(
                    combination["semantic_snapshot_deterministic"],
                    path + ".semantic_snapshot_deterministic",
                ),
                _boolean(
                    combination["experiential_prefix_stable"],
                    path + ".experiential_prefix_stable",
                ),
                _boolean(
                    combination["planned_series_prefix_stable"],
                    path + ".planned_series_prefix_stable",
                ),
                _boolean(
                    combination["semantic_series_isolated"],
                    path + ".semantic_series_isolated",
                ),
                _boolean(
                    combination["aggregate_semantics_presentation_independent"],
                    path + ".aggregate_semantics_presentation_independent",
                ),
            )
        )
    combination_values = tuple(
        (
            item.itemization,
            item.ordering,
            item.semantic_id,
            item.permanent,
            item.semantic_snapshot_deterministic,
            item.experiential_prefix_stable,
            item.planned_series_prefix_stable,
            item.semantic_series_isolated,
            item.aggregate_semantics_presentation_independent,
        )
        for item in combinations
    )
    _require_exact(combination_values, _MODE_COMBINATIONS, "$.mode_combinations")

    geometry = _object(
        root["geometry"],
        "$.geometry",
        {
            "base",
            "file_ladder",
            "rank_ladder",
            "stage_order",
            "valid_pairs",
            "unlocks",
            "pawn_capacity_formula",
        },
    )
    base_data = _object(geometry["base"], "$.geometry.base", {"files", "ranks"})
    base = Geometry(
        _integer(base_data["files"], "$.geometry.base.files", 1),
        _integer(base_data["ranks"], "$.geometry.base.ranks", 1),
    )
    file_ladder = _int_tuple(geometry["file_ladder"], "$.geometry.file_ladder")
    rank_ladder = _int_tuple(geometry["rank_ladder"], "$.geometry.rank_ladder")
    for ladder, path in (
        (file_ladder, "$.geometry.file_ladder"),
        (rank_ladder, "$.geometry.rank_ladder"),
    ):
        if not ladder or any(value % 2 for value in ladder) or any(a >= b for a, b in zip(ladder, ladder[1:])):
            raise ApmwContractError(f"{path} must be a strictly increasing ladder of even values")
    if base.files != file_ladder[0] or base.ranks != rank_ladder[0]:
        raise ApmwContractError("$.geometry.base must use the first file and rank ladder values")
    _require_exact(file_ladder, _FILE_LADDER, "$.geometry.file_ladder")
    _require_exact(rank_ladder, _RANK_LADDER, "$.geometry.rank_ladder")

    stage_order = _string_tuple(geometry["stage_order"], "$.geometry.stage_order")
    stages = []
    seen_pairs: set[tuple[int, int]] = set()
    for index, raw_stage in enumerate(_array(geometry["valid_pairs"], "$.geometry.valid_pairs")):
        path = f"$.geometry.valid_pairs[{index}]"
        stage = _object(
            raw_stage,
            path,
            {
                "stage_id",
                "files",
                "ranks",
                "deployment_depth",
                "combined_non_primary_capacity",
                "gross_pawn_capacity",
                "forwardness_capacity",
                "non_pawn_capacity",
                "cpu_pawn_count",
                "cpu_non_king_count",
                "all_tactics_locations",
                "turns_locations",
                "no_tactics_locations",
            },
        )
        parsed = GeometryStage(
            _string(stage["stage_id"], path + ".stage_id"),
            _integer(stage["files"], path + ".files", 1),
            _integer(stage["ranks"], path + ".ranks", 1),
            _integer(stage["deployment_depth"], path + ".deployment_depth", 1),
            _integer(
                stage["combined_non_primary_capacity"],
                path + ".combined_non_primary_capacity",
                1,
            ),
            _integer(stage["gross_pawn_capacity"], path + ".gross_pawn_capacity", 1),
            _integer(stage["forwardness_capacity"], path + ".forwardness_capacity", 1),
            _integer(stage["non_pawn_capacity"], path + ".non_pawn_capacity", 1),
            _integer(stage["cpu_pawn_count"], path + ".cpu_pawn_count", 1),
            _integer(stage["cpu_non_king_count"], path + ".cpu_non_king_count", 1),
            _integer(stage["all_tactics_locations"], path + ".all_tactics_locations", 1),
            _integer(stage["turns_locations"], path + ".turns_locations", 1),
            _integer(stage["no_tactics_locations"], path + ".no_tactics_locations", 1),
        )
        match = _STAGE_RE.fullmatch(parsed.stage_id)
        if not match or (int(match.group(1)), int(match.group(2))) != (parsed.files, parsed.ranks):
            raise ApmwContractError(f"{path}.stage_id must be canonical filesxranks")
        if parsed.files not in file_ladder or parsed.ranks not in rank_ladder:
            raise ApmwContractError(f"{path} geometry is outside the declared ladders")
        pair = (parsed.files, parsed.ranks)
        if pair in seen_pairs:
            raise ApmwContractError("$.geometry.valid_pairs contains duplicate geometries")
        seen_pairs.add(pair)
        deployment_depth = parsed.ranks - 3
        expected_locations = 7 * parsed.files + 15 + index
        expected_values = (
            deployment_depth,
            parsed.files * deployment_depth - 1,
            parsed.files * (deployment_depth - 1),
            parsed.files * (deployment_depth - 2),
            parsed.files * (parsed.ranks - 6) - 1,
            parsed.files,
            parsed.files - 1,
            expected_locations,
            expected_locations - 6,
            expected_locations - 10,
        )
        actual_values = (
            parsed.deployment_depth,
            parsed.combined_non_primary_capacity,
            parsed.gross_pawn_capacity,
            parsed.forwardness_capacity,
            parsed.non_pawn_capacity,
            parsed.cpu_pawn_count,
            parsed.cpu_non_king_count,
            parsed.all_tactics_locations,
            parsed.turns_locations,
            parsed.no_tactics_locations,
        )
        if actual_values != expected_values:
            raise ApmwContractError(f"{path} does not match expanded-formation-v2")
        stages.append(parsed)

    if tuple(stage.stage_id for stage in stages) != stage_order:
        raise ApmwContractError("$.geometry.stage_order must exactly match valid_pairs order")
    _require_exact(stage_order, _STAGE_ORDER, "$.geometry.stage_order")
    if not stages or stages[0].stage_id != base.stage_id:
        raise ApmwContractError("$.geometry.valid_pairs must begin with the base geometry")
    for previous, current in zip(stages, stages[1:]):
        deltas = (current.files - previous.files, current.ranks - previous.ranks)
        if deltas not in ((2, 0), (0, 2)):
            raise ApmwContractError("$.geometry.stage_order must advance one two-unit axis per stage")

    unlocks_data = _object(
        geometry["unlocks"],
        "$.geometry.unlocks",
        {"roles", "selection_policy"},
    )
    unlock_roles = []
    for index, raw_role in enumerate(
        _array(unlocks_data["roles"], "$.geometry.unlocks.roles")
    ):
        path = f"$.geometry.unlocks.roles[{index}]"
        role = _object(raw_role, path, {"role_id", "base", "increment", "maximum"})
        unlock_roles.append(
            GeometryUnlockRole(
                _string(role["role_id"], path + ".role_id"),
                _integer(role["base"], path + ".base", 1),
                _integer(role["increment"], path + ".increment", 1),
                _integer(role["maximum"], path + ".maximum", 1),
            )
        )
    geometry_unlocks = GeometryUnlocks(
        tuple(unlock_roles),
        _string(
            unlocks_data["selection_policy"],
            "$.geometry.unlocks.selection_policy",
        ),
    )
    _require_exact(
        geometry_unlocks,
        GeometryUnlocks(
            (
                GeometryUnlockRole("board-file-unlock", 8, 2, 12),
                GeometryUnlockRole("board-rank-unlock", 8, 2, 12),
            ),
            "largest-componentwise-unlocked-valid-pair",
        ),
        "$.geometry.unlocks",
    )

    formula_data = _object(
        geometry["pawn_capacity_formula"],
        "$.geometry.pawn_capacity_formula",
        {
            "gross_pawn_capacity_algorithm",
            "non_pawns_beyond_back_algorithm",
            "active_pawn_capacity_algorithm",
            "back_rank_primary_royal_slots",
        },
    )
    pawn_capacity_formula = PawnCapacityFormula(
        _string(
            formula_data["gross_pawn_capacity_algorithm"],
            "$.geometry.pawn_capacity_formula.gross_pawn_capacity_algorithm",
        ),
        _string(
            formula_data["non_pawns_beyond_back_algorithm"],
            "$.geometry.pawn_capacity_formula.non_pawns_beyond_back_algorithm",
        ),
        _string(
            formula_data["active_pawn_capacity_algorithm"],
            "$.geometry.pawn_capacity_formula.active_pawn_capacity_algorithm",
        ),
        _integer(
            formula_data["back_rank_primary_royal_slots"],
            "$.geometry.pawn_capacity_formula.back_rank_primary_royal_slots",
            1,
        ),
    )
    _require_exact(
        pawn_capacity_formula,
        PawnCapacityFormula(
            "width-times-ranks-minus-four-v1",
            "max-zero-n-minus-width-minus-one-v1",
            "gross-minus-non-pawns-beyond-back-v1",
            1,
        ),
        "$.geometry.pawn_capacity_formula",
    )

    algorithms_data = _object(root["algorithms"], "$.algorithms", set(_ALGORITHMS))
    algorithms = {key: _string(algorithms_data[key], f"$.algorithms.{key}") for key in _ALGORITHMS}
    _require_exact(algorithms, _ALGORITHMS, "$.algorithms")

    expected_material = _parse_int_map(root["expected_material"], "$.expected_material")
    _require_exact(expected_material, _EXPECTED_MATERIAL, "$.expected_material")
    source_roles = _string_tuple(root["source_roles"], "$.source_roles")
    _require_exact(source_roles, _SOURCE_ROLES, "$.source_roles")

    upgrade_data = _object(
        root["upgrade_dag"],
        "$.upgrade_dag",
        {
            "final_families",
            "pawn_creation_actions",
            "pawn_creation_source_role",
            "transitions",
        },
    )
    final_families = _string_tuple(
        upgrade_data["final_families"], "$.upgrade_dag.final_families"
    )
    pawn_creation_actions = _string_tuple(
        upgrade_data["pawn_creation_actions"], "$.upgrade_dag.pawn_creation_actions"
    )
    pawn_creation_source_role = _string(
        upgrade_data["pawn_creation_source_role"],
        "$.upgrade_dag.pawn_creation_source_role",
    )
    _require_exact(final_families, _FINAL_FAMILIES, "$.upgrade_dag.final_families")
    _require_exact(
        pawn_creation_actions,
        _PAWN_CREATION_ACTIONS,
        "$.upgrade_dag.pawn_creation_actions",
    )
    _require_exact(
        pawn_creation_source_role,
        "pawn-slot",
        "$.upgrade_dag.pawn_creation_source_role",
    )
    transitions = []
    for index, raw_transition in enumerate(
        _array(upgrade_data["transitions"], "$.upgrade_dag.transitions")
    ):
        path = f"$.upgrade_dag.transitions[{index}]"
        transition = _object(
            raw_transition,
            path,
            {
                "action",
                "from_family",
                "to_family",
                "allowed_source_roles",
                "source_role_rule",
            },
        )
        transitions.append(
            UpgradeTransition(
                _string(transition["action"], path + ".action"),
                _string(transition["from_family"], path + ".from_family"),
                _string(transition["to_family"], path + ".to_family"),
                _string_tuple(
                    transition["allowed_source_roles"],
                    path + ".allowed_source_roles",
                ),
                _string(transition["source_role_rule"], path + ".source_role_rule"),
            )
        )
    transition_values = tuple(
        (
            transition.action,
            transition.from_family,
            transition.to_family,
            transition.allowed_source_roles,
            transition.source_role_rule,
        )
        for transition in transitions
    )
    _require_exact(transition_values, _UPGRADE_TRANSITIONS, "$.upgrade_dag.transitions")
    upgrade_dag = UpgradeDag(
        final_families,
        pawn_creation_actions,
        pawn_creation_source_role,
        tuple(transitions),
    )

    castler_data = _object(
        root["castler"],
        "$.castler",
        {
            "source_role",
            "reclassifies_existing_chessman",
            "source_role_immutable",
            "normalized_material",
            "normalized_cost",
            "maximum",
            "adds_chessman",
            "requires_existing_chessman",
            "occupies_board_slot",
            "target_families",
            "upgrade_ceiling",
            "protected_from_higher_upgrades",
            "ordinary_omission_protection",
            "castling_eligibility",
        },
    )
    castler = CastlerSemantics(
        _string(castler_data["source_role"], "$.castler.source_role"),
        _boolean(
            castler_data["reclassifies_existing_chessman"],
            "$.castler.reclassifies_existing_chessman",
        ),
        _boolean(
            castler_data["source_role_immutable"],
            "$.castler.source_role_immutable",
        ),
        _integer(castler_data["normalized_material"], "$.castler.normalized_material"),
        _integer(castler_data["normalized_cost"], "$.castler.normalized_cost"),
        _integer(castler_data["maximum"], "$.castler.maximum"),
        _boolean(castler_data["adds_chessman"], "$.castler.adds_chessman"),
        _boolean(
            castler_data["requires_existing_chessman"],
            "$.castler.requires_existing_chessman",
        ),
        _boolean(castler_data["occupies_board_slot"], "$.castler.occupies_board_slot"),
        _string_tuple(castler_data["target_families"], "$.castler.target_families"),
        _string(castler_data["upgrade_ceiling"], "$.castler.upgrade_ceiling"),
        _boolean(
            castler_data["protected_from_higher_upgrades"],
            "$.castler.protected_from_higher_upgrades",
        ),
        _string(
            castler_data["ordinary_omission_protection"],
            "$.castler.ordinary_omission_protection",
        ),
        _string(
            castler_data["castling_eligibility"],
            "$.castler.castling_eligibility",
        ),
    )
    _require_exact(
        castler,
        CastlerSemantics(
            "locked-castler",
            True,
            True,
            500,
            500,
            2,
            False,
            True,
            True,
            ("major", "jack"),
            "jack",
            True,
            "after-additional-royals-within-back-rank-capacity",
            "any-active-home-rank-major-or-jack",
        ),
        "$.castler",
    )

    semantic_series_ids = _string_tuple(root["semantic_series_ids"], "$.semantic_series_ids")
    presentation_series_ids = _string_tuple(root["presentation_series_ids"], "$.presentation_series_ids")
    _require_exact(semantic_series_ids, _SEMANTIC_SERIES_IDS, "$.semantic_series_ids")
    _require_exact(presentation_series_ids, _PRESENTATION_SERIES_IDS, "$.presentation_series_ids")

    overflow_data = _object(
        root["overflow_policy"],
        "$.overflow_policy",
        {
            "id",
            "role_priority",
            "within_role_activation_order",
            "reserve_entry_order",
            "missing_material_accounting",
            "material_first_activation",
            "larger_geometry_reactivates_reserves",
            "ordinary_omission_protected_roles",
            "aggregate_semantics_ignore_presentation",
            "chaos_nonce_scope",
        },
    )
    overflow = OverflowPolicy(
        _string(overflow_data["id"], "$.overflow_policy.id"),
        _string_tuple(overflow_data["role_priority"], "$.overflow_policy.role_priority"),
        _string_tuple(
            overflow_data["within_role_activation_order"],
            "$.overflow_policy.within_role_activation_order",
        ),
        _string_tuple(
            overflow_data["reserve_entry_order"],
            "$.overflow_policy.reserve_entry_order",
        ),
        _string(
            overflow_data["missing_material_accounting"],
            "$.overflow_policy.missing_material_accounting",
        ),
        _boolean(
            overflow_data["material_first_activation"],
            "$.overflow_policy.material_first_activation",
        ),
        _boolean(
            overflow_data["larger_geometry_reactivates_reserves"],
            "$.overflow_policy.larger_geometry_reactivates_reserves",
        ),
        _string_tuple(
            overflow_data["ordinary_omission_protected_roles"],
            "$.overflow_policy.ordinary_omission_protected_roles",
        ),
        _boolean(
            overflow_data["aggregate_semantics_ignore_presentation"],
            "$.overflow_policy.aggregate_semantics_ignore_presentation",
        ),
        _string(
            overflow_data["chaos_nonce_scope"],
            "$.overflow_policy.chaos_nonce_scope",
        ),
    )
    _require_exact(
        overflow,
        OverflowPolicy(
            "material-first-reserve-v2",
            _SOURCE_ROLES,
            (
                "final-expected-material-descending",
                "ap-granted-material-descending",
                "source-ordinal-ascending",
            ),
            (
                "final-expected-material-ascending",
                "ap-granted-material-ascending",
                "source-ordinal-descending",
            ),
            "normalized-ap-granted-material-per-reserve-slot-exactly-once",
            True,
            True,
            ("primary-royal", "additional-royal", "locked-castler"),
            True,
            "presentation-only",
        ),
        "$.overflow_policy",
    )

    cpu_data = _object(
        root["cpu_profiles"],
        "$.cpu_profiles",
        {"layout_version", "location_profile_version", "army_ids"},
    )
    cpu_profiles = CpuProfiles(
        _string(cpu_data["layout_version"], "$.cpu_profiles.layout_version"),
        _string(cpu_data["location_profile_version"], "$.cpu_profiles.location_profile_version"),
        _string_tuple(cpu_data["army_ids"], "$.cpu_profiles.army_ids"),
    )
    _require_exact(
        cpu_profiles,
        CpuProfiles(
            "apmw-cpu-layout-v1",
            "apmw-location-profile-v1",
            ("standard", "colourbound-clobberers", "remarkable-rookies", "nutty-knights"),
        ),
        "$.cpu_profiles",
    )

    maxima_data = _object(
        root["effective_item_maxima"],
        "$.effective_item_maxima",
        {"common", "legacy", "fundamental"},
    )
    maxima = {
        key: _parse_int_map(maxima_data[key], f"$.effective_item_maxima.{key}")
        for key in ("common", "legacy", "fundamental")
    }
    _require_exact(maxima["common"], _COMMON_MAXIMA, "$.effective_item_maxima.common")
    _require_exact(maxima["legacy"], _LEGACY_MAXIMA, "$.effective_item_maxima.legacy")
    _require_exact(maxima["fundamental"], _FUNDAMENTAL_MAXIMA, "$.effective_item_maxima.fundamental")
    if maxima["fundamental"]["Chessmen"] != max(
        stage.combined_non_primary_capacity for stage in stages
    ):
        raise ApmwContractError("Chessmen maximum must equal the largest geometry capacity")
    if maxima["fundamental"]["Material"] != 3 * maxima["fundamental"]["Chessmen"]:
        raise ApmwContractError("Material maximum must be three times the Chessmen maximum")

    computed_hash = compute_manifest_sha256(text)
    if computed_hash != manifest_hash:
        raise ApmwContractError(
            f"manifest SHA-256 mismatch: embedded {manifest_hash}, computed {computed_hash}"
        )

    frozen_maxima = MappingProxyType(
        {key: MappingProxyType(dict(value)) for key, value in maxima.items()}
    )
    return ApmwContractV2(
        version,
        manifest_hash,
        minimum_client_version,
        minor_compatibility,
        itemization_modes,
        ordering_modes,
        tuple(combinations),
        base,
        file_ladder,
        rank_ladder,
        stage_order,
        tuple(stages),
        geometry_unlocks,
        pawn_capacity_formula,
        MappingProxyType(dict(algorithms)),
        MappingProxyType(dict(expected_material)),
        source_roles,
        upgrade_dag,
        castler,
        semantic_series_ids,
        presentation_series_ids,
        overflow,
        cpu_profiles,
        frozen_maxima,
    )


def load_contract(path: str | Path) -> ApmwContractV2:
    return parse_contract(Path(path).read_text(encoding="utf-8"))
