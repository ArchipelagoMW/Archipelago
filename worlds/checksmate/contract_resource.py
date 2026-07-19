from __future__ import annotations

import json
from importlib import resources
from typing import Mapping

from .apmw_contract import ApmwContractV2, parse_contract


CONTRACT_RESOURCE = "data/apmw_contract_v2.json"
UNLOCK_ITEM_ROLES = {
    "Board Files": "board-file-unlock",
    "Board Ranks": "board-rank-unlock",
}


def production_contract_text() -> str:
    return (
        resources.files(__package__)
        .joinpath(*CONTRACT_RESOURCE.split("/"))
        .read_text(encoding="utf-8")
    )


def load_production_contract() -> ApmwContractV2:
    return parse_contract(production_contract_text())


def production_contract_document() -> dict:
    return json.loads(production_contract_text())


def mode_item_maxima(itemization: str) -> Mapping[str, int]:
    contract = load_production_contract()
    maxima = dict(contract.effective_item_maxima["common"])
    maxima.update(contract.effective_item_maxima[itemization])
    maxima.update({name: 2 for name in UNLOCK_ITEM_ROLES})
    return maxima
