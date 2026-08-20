"""Frozen contract resource owned by the standalone semantic package."""

from __future__ import annotations

from collections.abc import Mapping
from functools import cache
import json
from importlib import resources
from pathlib import Path
import sys
from types import MappingProxyType
from typing import Any

from .contract import ApmwContractV2, parse_contract


CONTRACT_RESOURCE = "data/apmw_contract_v2.json"
UNLOCK_ITEM_ROLES = MappingProxyType(
    {
        "Board Files": "board-file-unlock",
        "Board Ranks": "board-rank-unlock",
    }
)


@cache
def frozen_contract_text() -> str:
    if getattr(sys, "frozen", False):
        frozen_resource = Path(sys.executable).resolve().parent / CONTRACT_RESOURCE
        if frozen_resource.is_file():
            return frozen_resource.read_text(encoding="utf-8")
    return (
        resources.files(__package__)
        .joinpath(*CONTRACT_RESOURCE.split("/"))
        .read_text(encoding="utf-8")
    )


@cache
def load_frozen_contract() -> ApmwContractV2:
    return parse_contract(frozen_contract_text())


FROZEN_CONTRACT_HASH = load_frozen_contract().manifest_sha256


def frozen_contract_document() -> dict[str, Any]:
    document = _thaw_json(_frozen_contract_document())
    if not isinstance(document, dict):
        raise RuntimeError("frozen contract document root is not an object")
    return document


def mode_item_maxima(itemization: str) -> Mapping[str, int]:
    contract = load_frozen_contract()
    maxima = dict(contract.effective_item_maxima["common"])
    maxima.update(contract.effective_item_maxima[itemization])
    maxima.update({name: 2 for name in UNLOCK_ITEM_ROLES})
    return maxima


@cache
def _frozen_contract_document() -> Mapping[str, Any]:
    document = json.loads(frozen_contract_text())
    if not isinstance(document, dict):
        raise RuntimeError("frozen contract document root is not an object")
    return _freeze_json(document)


def _freeze_json(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType(
            {key: _freeze_json(item) for key, item in value.items()}
        )
    if isinstance(value, list):
        return tuple(_freeze_json(item) for item in value)
    return value


def _thaw_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _thaw_json(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw_json(item) for item in value]
    return value
