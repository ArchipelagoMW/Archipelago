from dataclasses import dataclass
import json
import os
import pkgutil
from typing import Any, Dict, List, TypedDict


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


@dataclass
class CivVIBoostData:
    Type: str
    EraType: str
    Prereq: List[str]
    PrereqRequiredCount: int
    Classification: str


def get_boosts_data() -> List[CivVIBoostData]:
    boosts_json = _get_data("boosts")
    boosts: List[CivVIBoostData] = []
    for boost in boosts_json:
        boosts.append(CivVIBoostData(
            Type=boost["Type"],
            EraType=boost["EraType"],
            Prereq=boost["Prereq"],
            PrereqRequiredCount=boost["PrereqRequiredCount"],
            Classification=boost["Classification"]
        ))

    return boosts


def get_era_required_items_data() -> Dict[str, List[str]]:
    return _get_data("era_required_items")


class NewItemData(TypedDict):
    Type: str
    Cost: int
    UITreeRow: int
    EraType: str


class ExistingItemData(NewItemData):
    Name: str


def get_existing_civics_data() -> List[ExistingItemData]:
    return _get_data("existing_civics")


def get_existing_techs_data() -> List[ExistingItemData]:
    return _get_data("existing_tech")


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
