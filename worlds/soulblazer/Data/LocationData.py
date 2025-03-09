from dataclasses import dataclass
from dataclass_wizard import YAMLWizard
from .Enums import LocationType, RuleFlag, IDOffset


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

    @property
    def address(self) -> int:
        """The unique ID used by archipelago for this location"""

        if self.type == LocationType.LAIR:
            return IDOffset.BASE_ID + IDOffset.LAIR_ID_OFFSET + self.id
        if self.type == LocationType.NPC_REWARD:
            return IDOffset.BASE_ID + IDOffset.NPC_REWARD_OFFSET + self.id
        return IDOffset.BASE_ID + self.id


@dataclass(frozen=True)
class SoulBlazerLocationsData(YAMLWizard):
    chests: list[SoulBlazerLocationData]
    lairs: list[SoulBlazerLocationData]
    npc_rewards: list[SoulBlazerLocationData]

    @property
    def all_locations(self) -> list[SoulBlazerLocationData]:
        return [*self.chests, *self.lairs, *self.npc_rewards]
