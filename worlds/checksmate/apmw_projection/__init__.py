"""Canonical, dependency-light APMW v2 semantic projection package."""

from .contract import ApmwContractError, ApmwContractV2, parse_contract
from .protocol import (
    CONTRACT_MISMATCH,
    INVALID_JSON,
    INVALID_PROTOCOL,
    INVALID_REQUEST,
    PROJECTION_ERROR,
    UNKNOWN_GEOMETRY,
    PROTOCOL_VERSION,
    RUNTIME_SEMANTIC_VERSION,
    ProtocolError,
    handle_batch_request,
    handle_json_request,
)
from .resource import FROZEN_CONTRACT_HASH, load_frozen_contract
from .semantic import ProjectionError, project_semantic_roster


__all__ = (
    "ApmwContractError",
    "ApmwContractV2",
    "CONTRACT_MISMATCH",
    "FROZEN_CONTRACT_HASH",
    "INVALID_JSON",
    "INVALID_PROTOCOL",
    "INVALID_REQUEST",
    "PROJECTION_ERROR",
    "PROTOCOL_VERSION",
    "ProtocolError",
    "ProjectionError",
    "RUNTIME_SEMANTIC_VERSION",
    "UNKNOWN_GEOMETRY",
    "handle_batch_request",
    "handle_json_request",
    "load_frozen_contract",
    "parse_contract",
    "project_semantic_roster",
)
