from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, CollectionRule, LocationProgressType, EntranceType
from rule_builder.rules import Rule, True_

from ..world_base import BurnoutParadiseRemasteredBase



class ItemTypeEnum(Enum):
    def __init__(self, value: str, item_id: int, classification: ItemClassification):
        # self._value_ must be set to the first element to support lookup by value
        self._value_ = value
        self.item_id = item_id
        self.classification = classification

@dataclass
class ItemData:
    type: ItemTypeEnum
    amount: int = 1


class RegionTypeEnum(Enum):
    def __init__(self,value: str):
        # self._value_ must be set to the first element to support lookup by value
        self._value_ = value

class EntranceTypeEnum(Enum):
    def __init__(self, value: str, exiting_region: RegionTypeEnum, entering_region: RegionTypeEnum, two_way: EntranceType,rule: CollectionRule | Rule[BurnoutParadiseRemasteredBase] = True_()):
        # self._value_ must be set to the first element to support lookup by value
        self._value_ = value
        self.exiting_region = exiting_region
        self.entering_region = entering_region
        self.two_way = two_way
        self.rule = rule


class LocationTypeEnum(Enum):
    def __init__(self, value: str, location_id: int, region: RegionTypeEnum,rule: CollectionRule | Rule[BurnoutParadiseRemasteredBase] = True_(), progress_type: LocationProgressType = LocationProgressType.DEFAULT):#, item_rule: Callable[[Item], bool] =  lambda item: True_()):
        # self._value_ must be set to the first element to support lookup by value
        self._value_ = value
        self.region = region
        self.location_id = location_id
        self.rule = rule
        self.progress_type = progress_type
        # self.item_rule: Callable[[Item], bool] = item_rule

@dataclass(kw_only=True)
class GeneratedLocationData:
    name: str
    location_id: int
    region: RegionTypeEnum
    rule: CollectionRule | Rule[BurnoutParadiseRemasteredBase] = field(
        default_factory=True_
    )
    progress_type: LocationProgressType = LocationProgressType.DEFAULT