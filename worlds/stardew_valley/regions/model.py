from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntFlag
from functools import cached_property

connector_keyword = " to "


class MergeFlag(IntFlag):
    ADD_EXITS = 0
    REMOVE_EXITS = 1


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
    exits: tuple[str, ...] = field(default_factory=tuple)
    flag: MergeFlag = MergeFlag.ADD_EXITS
    is_ginger_island: bool = False

    def __post_init__(self):
        assert not isinstance(self.exits, str), "Exits must be a tuple of strings, you probably forgot a trailing comma."

    def merge_with(self, other: RegionData) -> RegionData:
        assert self.name == other.name, "Regions must have the same name to be merged"

        if other.flag == MergeFlag.REMOVE_EXITS:
            return self.get_without_exits(set(other.exits))

        merged_exits = tuple(set(self.exits + other.exits))
        return RegionData(self.name, merged_exits, is_ginger_island=self.is_ginger_island)

    def get_without_exits(self, exits_to_remove: set[str]) -> RegionData:
        exits = tuple(exit_ for exit_ in self.exits if exit_ not in exits_to_remove)
        return RegionData(self.name, exits, is_ginger_island=self.is_ginger_island)


@dataclass(frozen=True)
class ConnectionData:
    name: str
    destination: str
    flag: RandomizationFlag = RandomizationFlag.NOT_RANDOMIZED

    @cached_property
    def reverse(self) -> str | None:
        try:
            origin, destination = self.name.split(connector_keyword)
        except ValueError:
            return None
        return f"{destination}{connector_keyword}{origin}"


@dataclass(frozen=True)
class ModRegionsData:
    mod_name: str
    regions: list[RegionData]
    connections: list[ConnectionData]
