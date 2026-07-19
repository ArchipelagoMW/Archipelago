"""Strict batched JSON protocol for the standalone APMW semantic projector."""

from __future__ import annotations

import json
from typing import Any, TextIO

from .resource import load_frozen_contract
from .semantic import ProjectionError, projection_input_from_dict, projection_to_dict, project_semantic_roster


PROTOCOL_VERSION = 1
RUNTIME_SEMANTIC_VERSION = "0.1.0"

INVALID_JSON = "invalid_json"
INVALID_PROTOCOL = "invalid_protocol"
CONTRACT_MISMATCH = "contract_mismatch"
INVALID_REQUEST = "invalid_request"
UNKNOWN_GEOMETRY = "unknown_geometry"
PROJECTION_ERROR = "projection_error"

_REQUEST_FIELDS = {
    "protocol_version",
    "request_id",
    "contract_hash",
    "input",
    "geometries",
}
_INPUT_REQUIRED_FIELDS = {"itemization", "ordering", "seeds", "item_counts"}
_INPUT_OPTIONAL_FIELDS = {"upgrade_preferences"}
_SEED_FIELDS = {
    "pocket_seed",
    "pawn_seed",
    "minor_seed",
    "major_seed",
    "queen_seed",
}
_PREFERENCE_REQUIRED_FIELDS = {"action", "priority"}
_PREFERENCE_OPTIONAL_FIELDS = {
    "proportion_numerator",
    "proportion_denominator",
}


class ProtocolError(ValueError):
    """A stable protocol failure suitable for sidecar consumers."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message

    def to_dict(self) -> dict[str, dict[str, str]]:
        return {"error": {"code": self.code, "message": self.message}}


def canonical_json(value: Any) -> str:
    """Encode ASCII-only compact JSON with deterministic object key ordering."""
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True)


def handle_json_request(text: str) -> dict[str, Any]:
    """Decode and process one sidecar request without starting a subprocess."""
    try:
        request = json.loads(text)
    except (TypeError, ValueError, json.JSONDecodeError) as error:
        raise ProtocolError(INVALID_JSON, "request is not valid JSON") from error
    return handle_batch_request(request)


def handle_batch_request(request: Any) -> dict[str, Any]:
    """Process a parsed protocol-v1 request using the frozen local contract."""
    _validate_request_envelope(request)
    assert isinstance(request, dict)
    if request["protocol_version"] != PROTOCOL_VERSION:
        raise ProtocolError(INVALID_PROTOCOL, "unsupported protocol version")

    contract = load_frozen_contract()
    if request["contract_hash"] != contract.manifest_sha256:
        raise ProtocolError(CONTRACT_MISMATCH, "contract hash does not match frozen v2 contract")

    semantic_input = _validate_input(request["input"])
    geometries = _validate_geometries(request["geometries"], contract.stage_order)
    stages = {stage.stage_id: stage for stage in contract.stages}
    results = []
    for stage_id in geometries:
        projection_input = dict(semantic_input)
        projection_input["unlock_counts"] = _unlock_counts_for_stage(contract, stages[stage_id])
        try:
            result = project_semantic_roster(
                contract, projection_input_from_dict(projection_input)
            )
        except ProjectionError as error:
            raise ProtocolError(PROJECTION_ERROR, "semantic projection failed") from error
        results.append(
            {
                "geometry_stage": stage_id,
                "projection": projection_to_dict(result),
            }
        )

    return {
        "protocol_version": PROTOCOL_VERSION,
        "request_id": request["request_id"],
        "contract_hash": contract.manifest_sha256,
        "runtime_semantic_version": RUNTIME_SEMANTIC_VERSION,
        "results": results,
    }


def run_cli(stdin: TextIO, stdout: TextIO, stderr: TextIO) -> int:
    """Run one JSON request, reserving stdout for its single JSON response."""
    try:
        response = handle_json_request(stdin.read())
    except ProtocolError as error:
        stdout.write(canonical_json(error.to_dict()) + "\n")
        stderr.write(f"{error.code}: {error.message}\n")
        return 1
    stdout.write(canonical_json(response) + "\n")
    return 0


def _validate_request_envelope(request: Any) -> None:
    if not isinstance(request, dict) or set(request) != _REQUEST_FIELDS:
        raise ProtocolError(INVALID_REQUEST, "request fields are invalid")
    if not isinstance(request["protocol_version"], int) or isinstance(
        request["protocol_version"], bool
    ):
        raise ProtocolError(INVALID_REQUEST, "protocol_version must be an integer")
    for field in ("request_id", "contract_hash"):
        if not isinstance(request[field], str) or not request[field]:
            raise ProtocolError(INVALID_REQUEST, f"{field} must be a non-empty string")


def _validate_input(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ProtocolError(INVALID_REQUEST, "input must be an object")
    if not _INPUT_REQUIRED_FIELDS.issubset(value) or set(value) - (
        _INPUT_REQUIRED_FIELDS | _INPUT_OPTIONAL_FIELDS
    ):
        raise ProtocolError(INVALID_REQUEST, "input fields are invalid")
    if not isinstance(value["itemization"], str) or not isinstance(
        value["ordering"], str
    ):
        raise ProtocolError(INVALID_REQUEST, "itemization and ordering must be strings")

    seeds = value["seeds"]
    if not isinstance(seeds, dict) or set(seeds) != _SEED_FIELDS or not all(
        isinstance(seed, str) for seed in seeds.values()
    ):
        raise ProtocolError(INVALID_REQUEST, "seeds fields are invalid")

    item_counts = value["item_counts"]
    if not isinstance(item_counts, dict) or not all(
        isinstance(name, str)
        and isinstance(count, int)
        and not isinstance(count, bool)
        for name, count in item_counts.items()
    ):
        raise ProtocolError(INVALID_REQUEST, "item_counts fields are invalid")

    preferences = value.get("upgrade_preferences", [])
    if not isinstance(preferences, list):
        raise ProtocolError(INVALID_REQUEST, "upgrade_preferences must be an array")
    for preference in preferences:
        if not isinstance(preference, dict) or not _PREFERENCE_REQUIRED_FIELDS.issubset(
            preference
        ) or set(preference) - (
            _PREFERENCE_REQUIRED_FIELDS | _PREFERENCE_OPTIONAL_FIELDS
        ):
            raise ProtocolError(INVALID_REQUEST, "upgrade_preferences fields are invalid")
        if not isinstance(preference["action"], str) or any(
            not isinstance(preference[field], int)
            or isinstance(preference[field], bool)
            for field in preference
            if field != "action"
        ):
            raise ProtocolError(INVALID_REQUEST, "upgrade_preferences values are invalid")
    return dict(value)


def _validate_geometries(value: Any, stage_order: tuple[str, ...]) -> list[str]:
    if not isinstance(value, list) or not value or any(
        not isinstance(stage_id, str) for stage_id in value
    ):
        raise ProtocolError(INVALID_REQUEST, "geometries must be a non-empty string array")
    if len(set(value)) != len(value):
        raise ProtocolError(INVALID_REQUEST, "geometries must not contain duplicates")
    unknown = next((stage_id for stage_id in value if stage_id not in stage_order), None)
    if unknown is not None:
        raise ProtocolError(UNKNOWN_GEOMETRY, "geometry is not defined by frozen v2 contract")
    return value


def _unlock_counts_for_stage(contract: Any, stage: Any) -> dict[str, int]:
    roles = {role.role_id: role for role in contract.geometry_unlocks.roles}
    file_role = roles["board-file-unlock"]
    rank_role = roles["board-rank-unlock"]
    return {
        file_role.role_id: (stage.files - file_role.base) // file_role.increment,
        rank_role.role_id: (stage.ranks - rank_role.base) // rank_role.increment,
    }
