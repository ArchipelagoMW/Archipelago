from __future__ import annotations

from collections.abc import Container
from dataclasses import dataclass, field
from enum import IntFlag

from ..strings.entrance_names import Entrance, LogicEntrance

connector_keyword = " to "


def reverse_connection_name(name: str) -> str | None:
    if name == Entrance.boat_to_ginger_island:
        return Entrance.boat_from_ginger_island
    if name == Entrance.boat_from_ginger_island:
        return Entrance.boat_to_ginger_island
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

    PELICAN_TOWN = 0b000001
    NON_PROGRESSION = 0b000010
    BUILDINGS = 0b000100
    OVERWORLD = 0b001000
    TRANSITION = 0b010000

    ENDGAME = 0b01000000
    MASTERY_CAVE = 0b10000000

    FARMHOUSE = 0b10000000000

    IS_ONE_WAY = 0b100000000000

    ALWAYS_ACCEPT = IS_ONE_WAY
    SET_PELICAN_TOWN = PELICAN_TOWN | ALWAYS_ACCEPT
    SET_NON_PROGRESSION = SET_PELICAN_TOWN | NON_PROGRESSION
    SET_BUILDINGS = SET_NON_PROGRESSION | BUILDINGS
    SET_OVERWORLD = SET_BUILDINGS | OVERWORLD
    SET_EVERYTHING = SET_OVERWORLD | TRANSITION


class GroupFlag(IntFlag):
    TO_ANY = 0b0

    UP = 0b00001
    DOWN = 0b00010
    LEFT = 0b00100
    RIGHT = 0b01000
    DOOR = 0b10000  # doors/ladders etc.

    FROM_INDOOR = 0b0100000
    FROM_OUTDOOR = 0b1000000

    TO_INDOOR = 0b010000000
    TO_OUTDOOR = 0b100000000

    FROM_FARMHOUSE = 0b01000000000

    IN_TO_OUT = FROM_INDOOR | TO_OUTDOOR
    IN_TO_IN = FROM_INDOOR | TO_INDOOR
    OUT_TO_OUT = FROM_OUTDOOR | TO_OUTDOOR
    OUT_TO_IN = FROM_OUTDOOR | TO_INDOOR

    DIR_MASK = UP | DOWN | LEFT | RIGHT | DOOR
    AREA_MASK = IN_TO_IN | IN_TO_OUT | OUT_TO_IN | OUT_TO_OUT


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
    group: GroupFlag = GroupFlag.TO_ANY

    @property
    def reverse(self) -> str | None:
        if RandomizationFlag.IS_ONE_WAY in self.flag:
            return None
        return reverse_connection_name(self.name)

    def is_eligible_for_randomization(self, chosen_randomization_flag: RandomizationFlag) -> bool:
        return bool(self.flag) and self.flag in chosen_randomization_flag


@dataclass(frozen=True)
class ModRegionsData:
    content_pack: str
    regions: list[RegionData]
    connections: list[ConnectionData]
