"""Frozen contract resource owned by the standalone semantic package."""

from __future__ import annotations

import json
from importlib import resources
from pathlib import Path
import sys
from typing import Mapping

from .contract import ApmwContractV2, parse_contract


CONTRACT_RESOURCE = "data/apmw_contract_v2.json"
UNLOCK_ITEM_ROLES = {
    "Board Files": "board-file-unlock",
    "Board Ranks": "board-rank-unlock",
}


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


def load_frozen_contract() -> ApmwContractV2:
    return parse_contract(frozen_contract_text())


FROZEN_CONTRACT_HASH = load_frozen_contract().manifest_sha256


def frozen_contract_document() -> dict:
    return json.loads(frozen_contract_text())


def mode_item_maxima(itemization: str) -> Mapping[str, int]:
    contract = load_frozen_contract()
    maxima = dict(contract.effective_item_maxima["common"])
    maxima.update(contract.effective_item_maxima[itemization])
    maxima.update({name: 2 for name in UNLOCK_ITEM_ROLES})
    return maxima
