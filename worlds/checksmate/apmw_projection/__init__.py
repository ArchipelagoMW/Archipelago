"""Canonical, dependency-light APMW v2 semantic projection package."""

from .contract import ApmwContractError, ApmwContractV2, parse_contract
from .protocol import (
    CONTRACT_MISMATCH,
    INVALID_JSON,
    INVALID_PROTOCOL,
    INVALID_REQUEST,
    PROJECTION_ERROR,
    UNKNOWN_GEOMETRY,
    ProtocolError,
    handle_batch_request,
    handle_json_request,
)
from .resource import load_frozen_contract
from .semantic import ProjectionError, project_semantic_roster


RUNTIME_SEMANTIC_VERSION = "0.1.0"
PROTOCOL_VERSION = 1


__all__ = (
    "ApmwContractError",
    "ApmwContractV2",
    "CONTRACT_MISMATCH",
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
