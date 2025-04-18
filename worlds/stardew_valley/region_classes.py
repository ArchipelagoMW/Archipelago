from copy import deepcopy
from dataclasses import dataclass, field
from enum import IntFlag
from typing import Optional, List, Set

connector_keyword = " to "


class ModificationFlag(IntFlag):
    NOT_MODIFIED = 0
    MODIFIED = 1


class RandomizationFlag(IntFlag):
    NOT_RANDOMIZED = 0b0
    PELICAN_TOWN = 0b00011111
    NON_PROGRESSION = 0b00011110
    BUILDINGS = 0b00011100
    EVERYTHING = 0b00011000
    GINGER_ISLAND = 0b00100000
    LEAD_TO_OPEN_AREA = 0b01000000
    MASTERIES = 0b10000000


@dataclass(frozen=True)
class RegionData:
    name: str
    exits: List[str] = field(default_factory=list)
    flag: ModificationFlag = ModificationFlag.NOT_MODIFIED
    is_ginger_island: bool = False

    def get_merged_with(self, exits: List[str]):
        merged_exits = []
        merged_exits.extend(self.exits)
        if exits is not None:
            merged_exits.extend(exits)
        merged_exits = sorted(set(merged_exits))
        return RegionData(self.name, merged_exits, is_ginger_island=self.is_ginger_island)

    def get_without_exits(self, exits_to_remove: Set[str]):
        exits = [exit_ for exit_ in self.exits if exit_ not in exits_to_remove]
        return RegionData(self.name, exits, is_ginger_island=self.is_ginger_island)

    def get_clone(self):
        return deepcopy(self)


@dataclass(frozen=True)
class ConnectionData:
    name: str
    destination: str
    origin: Optional[str] = None
    reverse: Optional[str] = None
    flag: RandomizationFlag = RandomizationFlag.NOT_RANDOMIZED

    def __post_init__(self):
        if connector_keyword in self.name:
            origin, destination = self.name.split(connector_keyword)
            if self.reverse is None:
                super().__setattr__("reverse", f"{destination}{connector_keyword}{origin}")


@dataclass(frozen=True)
class ModRegionData:
    mod_name: str
    regions: List[RegionData]
    connections: List[ConnectionData]
