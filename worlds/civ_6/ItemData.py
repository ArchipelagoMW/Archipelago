from dataclasses import dataclass
from typing import List, TypedDict


class NewItemData(TypedDict):
    Type: str
    Cost: int
    UITreeRow: int
    EraType: str


class ExistingItemData(NewItemData):
    Name: str


@dataclass
class CivVIBoostData:
    Type: str
    EraType: str
    Prereq: List[str]
    PrereqRequiredCount: int
    Classification: str
    EraRequired: bool = False


class GoodyHutRewardData(TypedDict):
    Type: str
    Name: str
    Rarity: str


class CivicPrereqData(TypedDict):
    Civic: str
    PrereqTech: str


class TechPrereqData(TypedDict):
    Technology: str
    PrereqTech: str
