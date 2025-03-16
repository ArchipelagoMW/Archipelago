from collections import namedtuple
from dataclasses import dataclass
from BaseClasses import Region, Location
from .Data.LocationData import SoulBlazerLocationData, SoulBlazerLocationsData
from .Rules import get_rule_for_location
from .Data.Enums import IDOffset, LairID, NPCRewardID, LocationType


def address_for_location(type: LocationType, id: int) -> int:
    if type == LocationType.LAIR:
        return IDOffset.BASE_ID + IDOffset.LAIR_ID_OFFSET + id
    if type == LocationType.NPC_REWARD:
        return IDOffset.BASE_ID + IDOffset.NPC_REWARD_OFFSET + id
    return IDOffset.BASE_ID + id


class SoulBlazerLocation(Location):
    game = "Soul Blazer"

    def __init__(
        self, player: int, name: str, data: SoulBlazerLocationData, parent: Region | None = None
    ):
        super().__init__(player, data.name, data.address, parent)
        self.data: SoulBlazerLocationData = data
        self.access_rule = get_rule_for_location(name, player, self.data.flag)


locations_data: SoulBlazerLocationsData = SoulBlazerLocationsData.from_yaml_file("worlds/soulblazer/Data/SoulBlazerLocations.yaml")

chests_by_name = {data.name: data for data in locations_data.chests}

npc_rewards_by_name = {data.name: data for data in locations_data.npc_rewards}

lairs_by_name = {data.name: data for data in locations_data.lairs}

locations_by_name = {
    **chests_by_name,
    **npc_rewards_by_name,
    **lairs_by_name,
}

# IDs are only unique by LocationType. Dont merge these dictionaries.
# (If you want an ID Dictionary, do it by Address)
chests_by_id = {data.id: data for data in locations_data.chests}

npc_rewards_by_id = {data.id: data for data in locations_data.npc_rewards}

lairs_by_id = {data.id: data for data in locations_data.lairs}

locations_by_address = {data.address: data for data in locations_data.all_locations}

boss_lair_names_table = {
    lairs_by_id[LairID.VILLAGE_CHIEF].name,
    lairs_by_id[LairID.GREENWOODS_GUARDIAN].name,
    lairs_by_id[LairID.MERMAID_QUEEN].name,
    lairs_by_id[LairID.MOUNTAIN_KING].name,
    lairs_by_id[LairID.MARIE].name,
    lairs_by_id[LairID.KING_MAGRIDD].name,
}

village_leader_names_table = {
    npc_rewards_by_id[NPCRewardID.VILLAGE_CHIEF].name,
    npc_rewards_by_id[NPCRewardID.GREENWOODS_GUARDIAN].name,
    npc_rewards_by_id[NPCRewardID.MERMAID_QUEEN].name,
    npc_rewards_by_id[NPCRewardID.NOME].name,
    npc_rewards_by_id[NPCRewardID.MARIE].name,
    npc_rewards_by_id[NPCRewardID.KING_MAGRIDD].name,
}

