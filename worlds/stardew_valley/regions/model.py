from __future__ import annotations

from collections.abc import Container
from dataclasses import dataclass, field
from enum import IntFlag

connector_keyword = " to "


def reverse_connection_name(name: str) -> str | None:
    try:
        origin, destination = name.split(connector_keyword)
    except ValueError:
        return None
    return f"{destination}{connector_keyword}{origin}"


class MergeFlag(IntFlag):
    ADD_EXITS = 0
    REMOVE_EXITS = 1


class RandomizationFlag(IntFlag):
    NOT_RANDOMIZED = 0

    # Randomization options
    # The first 4 bits are used to mark if an entrance is eligible for randomization according to the entrance randomization options.
    BIT_PELICAN_TOWN = 1  # 0b0001
    BIT_NON_PROGRESSION = 1 << 1  # 0b0010
    BIT_BUILDINGS = 1 << 2  # 0b0100
    BIT_EVERYTHING = 1 << 3  # 0b1000

    # Content flag for entrances exclusions
    # The next 2 bits are used to mark if an entrance is to be excluded from randomization according to the content options.
    # Those bits must be removed from an entrance flags when then entrance must be excluded.
    __UNUSED = 1 << 4  # 0b010000
    EXCLUDE_MASTERIES = 1 << 5  # 0b100000

    # Entrance groups
    # The last bit is used to add additional qualifiers on entrances to group them
    # Those bits should be added when an entrance need additional qualifiers.
    LEAD_TO_OPEN_AREA = 1 << 6

    # Tags to apply on connections
    EVERYTHING = EXCLUDE_MASTERIES | BIT_EVERYTHING
    BUILDINGS = EVERYTHING | BIT_BUILDINGS
    NON_PROGRESSION = BUILDINGS | BIT_NON_PROGRESSION
    PELICAN_TOWN = NON_PROGRESSION | BIT_PELICAN_TOWN


@dataclass(frozen=True)
class RegionData:
    name: str
    exits: tuple[str, ...] = field(default_factory=tuple)
    flag: MergeFlag = MergeFlag.ADD_EXITS

    def __post_init__(self):
        assert not isinstance(self.exits, str), "Exits must be a tuple of strings, you probably forgot a trailing comma."

    def merge_with(self, other: RegionData) -> RegionData:
        assert self.name == other.name, "Regions must have the same name to be merged"

        if other.flag == MergeFlag.REMOVE_EXITS:
            return self.get_without_exits(other.exits)

        merged_exits = self.exits + other.exits
        assert len(merged_exits) == len(set(merged_exits)), "Two regions getting merged have duplicated exists..."

        return RegionData(self.name, merged_exits)

    def get_without_exits(self, exits_to_remove: Container[str]) -> RegionData:
        exits = tuple(exit_ for exit_ in self.exits if exit_ not in exits_to_remove)
        return RegionData(self.name, exits)


@dataclass(frozen=True)
class ConnectionData:
    name: str
    destination: str
    flag: RandomizationFlag = RandomizationFlag.NOT_RANDOMIZED

    @property
    def reverse(self) -> str | None:
        return reverse_connection_name(self.name)

    def is_eligible_for_randomization(self, chosen_randomization_flag: RandomizationFlag) -> bool:
        return chosen_randomization_flag and chosen_randomization_flag in self.flag


@dataclass(frozen=True)
class ModRegionsData:
    content_pack: str
    regions: list[RegionData]
    connections: list[ConnectionData]
