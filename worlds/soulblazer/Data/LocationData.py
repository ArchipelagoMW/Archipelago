from dataclasses import dataclass
from typing import Any

from Utils import parse_yaml
from .Enums import LocationType, RuleFlag, IDOffset, LairID, ChestID, NPCRewardID
from ..Data import get_data_file_bytes, intFromYaml, listFromYaml, strFromYaml


@dataclass(frozen=True)
class SoulBlazerLocationData:
    id: int
    """Internal location ID and index into ROM chest/lair/NPC reward table"""
    name: str
    """String representation of the location."""
    type: LocationType
    flag: RuleFlag = RuleFlag.NONE
    """Special RuleFlag which applies to this location."""
    description: str = ""
    """Detailed description of the location."""

    @staticmethod
    def from_yaml(yaml: Any) -> "SoulBlazerLocationData":
        return SoulBlazerLocationData(
            id = intFromYaml(yaml["id"]),
            name = strFromYaml(yaml["name"]),
            type = LocationType.from_yaml(yaml["type"]),
            flag = RuleFlag.from_yaml(yaml["flag"]),
            description = strFromYaml(yaml["description"]),
        )

    @property
    def address(self) -> int:
        """The unique ID used by archipelago for this location"""

        if self.type == LocationType.LAIR:
            return IDOffset.BASE_ID + IDOffset.LAIR_ID_OFFSET + self.id
        if self.type == LocationType.NPC_REWARD:
            return IDOffset.BASE_ID + IDOffset.NPC_REWARD_OFFSET + self.id
        return IDOffset.BASE_ID + self.id


@dataclass(frozen=True)
class SoulBlazerLocationsData:
    chests: list[SoulBlazerLocationData]
    lairs: list[SoulBlazerLocationData]
    npc_rewards: list[SoulBlazerLocationData]

    @staticmethod
    def from_yaml(yaml: Any) -> "SoulBlazerLocationsData":
        return SoulBlazerLocationsData(
            chests = listFromYaml(yaml["chests"], SoulBlazerLocationData.from_yaml),
            lairs = listFromYaml(yaml["lairs"], SoulBlazerLocationData.from_yaml),
            npc_rewards = listFromYaml(yaml["npc-rewards"], SoulBlazerLocationData.from_yaml),
        )

    @property
    def all_locations(self) -> list[SoulBlazerLocationData]:
        return [*self.chests, *self.lairs, *self.npc_rewards]


locations_data_bytes = get_data_file_bytes("SoulBlazerLocations.yaml")
locations_data_yaml = parse_yaml(locations_data_bytes)
locations_data: SoulBlazerLocationsData = SoulBlazerLocationsData.from_yaml(locations_data_yaml)

ChestID.full_names = {data.id: data.name for data in locations_data.chests}

LairID.full_names = {data.id: data.name for data in locations_data.lairs}

NPCRewardID.full_names = {data.id: data.name for data in locations_data.npc_rewards}
