"""Compatibility wrapper for the canonical frozen APMW contract resource."""

from .apmw_projection.resource import (
    CONTRACT_RESOURCE,
    UNLOCK_ITEM_ROLES,
    frozen_contract_document as production_contract_document,
    frozen_contract_text as production_contract_text,
    load_frozen_contract as load_production_contract,
    mode_item_maxima,
)
from .apmw_projection.contract import ApmwContractV2, parse_contract


__all__ = (
    "ApmwContractV2",
    "CONTRACT_RESOURCE",
    "UNLOCK_ITEM_ROLES",
    "load_production_contract",
    "mode_item_maxima",
    "parse_contract",
    "production_contract_document",
    "production_contract_text",
)
