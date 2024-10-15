from dataclasses import dataclass
import json
import os
import pkgutil
from typing import Dict, List


_cache = {}


def _get_data(key: str):
    global _cache
    if key not in _cache:
        path = os.path.join("data", f"{key}.json")
        _cache[key] = json.loads(
            pkgutil.get_data(__name__, path).decode())
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
    boosts = []
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


def get_existing_civics_data():
    return _get_data("existing_civics")


def get_existing_techs_data():
    return _get_data("existing_tech")


def get_goody_hut_rewards_data():
    return _get_data("goody_hut_rewards")


def get_new_civic_prereqs_data():
    return _get_data("new_civic_prereqs")


def get_new_civics_data():
    return _get_data("new_civics")


def get_new_tech_prereqs_data():
    return _get_data("new_tech_prereqs")


def get_new_techs_data():
    return _get_data("new_tech")


def get_progressive_districts_data():
    return _get_data("progressive_districts")
