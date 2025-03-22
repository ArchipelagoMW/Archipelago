from BaseClasses import Region, Location
from .Data.LocationData import SoulBlazerLocationData, locations_data
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


chests_by_name = {data.name: data for data in locations_data.chests}

npc_rewards_by_name = {data.name: data for data in locations_data.npc_rewards}

lairs_by_name = {data.name: data for data in locations_data.lairs}

locations_by_name = {
    **chests_by_name,
    **npc_rewards_by_name,
    **lairs_by_name,
}

locations_by_address = {data.address: data for data in locations_data.all_locations}

boss_lair_names = {
    LairID.VILLAGE_CHIEF.full_name,
    LairID.GREENWOODS_GUARDIAN.full_name,
    LairID.MERMAID_QUEEN.full_name,
    LairID.MOUNTAIN_KING.full_name,
    LairID.MARIE.full_name,
    LairID.KING_MAGRIDD.full_name,
}

village_leader_names = {
    NPCRewardID.VILLAGE_CHIEF.full_name,
    NPCRewardID.GREENWOODS_GUARDIAN.full_name,
    NPCRewardID.MERMAID_QUEEN.full_name,
    NPCRewardID.NOME.full_name,
    NPCRewardID.MARIE.full_name,
    NPCRewardID.KING_MAGRIDD.full_name,
}

