from dataclasses import dataclass
from enum import Enum

from BaseClasses import ItemClassification, CollectionRule, LocationProgressType
from rule_builder.rules import Rule, True_
from worlds.potion_craft import PotionCraftBase

class Direction(Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3

class ItemTypeEnum(Enum):
    def __init__(self, value: str, item_id: int, classification: ItemClassification = ItemClassification.useful):
        # self._value_ must be set to the first element to support lookup by value
        self._value_ = value
        self.item_id = item_id
        self.classification = classification

@dataclass
class ItemData:
    type: ItemTypeEnum
    amount: int = 1

@dataclass
class ItemFiller:
    type: ItemTypeEnum
    weight: int = 1

@dataclass
class IngredientData:
    type: ItemTypeEnum
    chapter: int
    direction: list[Direction]



class RegionTypeEnum(Enum):
    def __init__(self,value: str):
        # self._value_ must be set to the first element to support lookup by value
        self._value_ = value

class ConnectionTypeEnum(Enum):
    def __init__(self, value: str, exiting_region: RegionTypeEnum, entering_region: RegionTypeEnum, rule: CollectionRule | Rule[PotionCraftBase] = True_()):
        # self._value_ must be set to the first element to support lookup by value
        self._value_ = value
        self.exiting_region = exiting_region
        self.entering_region = entering_region
        self.rule = rule

class LocationTypeEnum(Enum):
    def __init__(self, value: str, location_id: int, region: RegionTypeEnum,rule: CollectionRule | Rule[PotionCraftBase] = True_(), progress_type: LocationProgressType = LocationProgressType.DEFAULT):
        # self._value_ must be set to the first element to support lookup by value
        self._value_ = value
        self.region = region
        self.location_id = location_id
        self.rule = rule
        self.progress_type = progress_type