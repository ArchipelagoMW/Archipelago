from dataclasses import dataclass, field
import typing

from .condition import Condition

@dataclass
class RegionConnection:
    region_from: str
    region_to: str
    cond: typing.Optional[list[Condition]]

@dataclass
class RegionsData:
    starting_region: str
    goal_region: str
    excluded_regions: typing.List[str]
    region_list: typing.List[str]
    region_connections: typing.List[RegionConnection]
