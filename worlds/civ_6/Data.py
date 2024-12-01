from dataclasses import dataclass
import json
import os
import pkgutil
from typing import Any, Dict, List, TypedDict

from worlds.civ_6.ItemData import CivVIBoostData, ExistingItemData, NewItemData


_cache: Dict[Any, Any] = {}


def _get_data(key: str) -> Any:
    global _cache
    if key not in _cache:
        path = os.path.join("data", f"{key}.json")
        data = pkgutil.get_data(__name__, path)
        if data is None:
            raise FileNotFoundError(f"Data file not found: {path}")
        _cache[key] = json.loads(data.decode())
    return _cache[key]


def get_boosts_data() -> List[CivVIBoostData]:
    from .data.boosts import boosts

    return boosts


def get_era_required_items_data() -> Dict[str, List[str]]:
    from .data.era_required_items import era_required_items

    return era_required_items


def get_existing_civics_data() -> List[ExistingItemData]:
    from .data.existing_civics import existing_civics

    return existing_civics


def get_existing_techs_data() -> List[ExistingItemData]:
    from .data.existing_tech import existing_tech

    return existing_tech


class GoodyHutRewardData(TypedDict):
    Type: str
    Name: str
    Rarity: str


def get_goody_hut_rewards_data() -> List[GoodyHutRewardData]:
    return _get_data("goody_hut_rewards")


class CivicPrereqData(TypedDict):
    Civic: str
    PrereqTech: str


def get_new_civic_prereqs_data() -> List[CivicPrereqData]:
    return _get_data("new_civic_prereqs")


def get_new_civics_data() -> List[NewItemData]:
    return _get_data("new_civics")


class TechPrereqData(TypedDict):
    Technology: str
    PrereqTech: str


def get_new_tech_prereqs_data() -> List[TechPrereqData]:
    return _get_data("new_tech_prereqs")


def get_new_techs_data() -> List[NewItemData]:
    return _get_data("new_tech")


def get_progressive_districts_data() -> Dict[str, List[str]]:
    return _get_data("progressive_districts")
