from typing import List, Dict, Any, Callable, TYPE_CHECKING

from BaseClasses import CollectionState
from ..mission_tables import SC2Mission, MissionFlag, get_goal_location
from .mission_pools import SC2MOGenMissionPools

if TYPE_CHECKING:
    from .nodes import SC2MOGenMissionOrder, SC2MOGenMission

class SC2MissionOrder:
    """
    Wrapper class for a generated mission order. Contains helper functions for getting data about generated missions.
    """

    def __init__(self, mission_order_node: 'SC2MOGenMissionOrder', mission_pools: SC2MOGenMissionPools):
        self.mission_order_node: 'SC2MOGenMissionOrder' = mission_order_node
        """Root node of the mission order structure."""
        self.mission_pools: SC2MOGenMissionPools = mission_pools
        """Manager for missions in the mission order."""

    def get_used_flags(self) -> Dict[MissionFlag, int]:
        """Returns a dictionary of all used flags and their appearance count within the mission order.
        Flags that don't appear in the mission order also don't appear in this dictionary."""
        return self.mission_pools.get_used_flags()
    
    def get_used_missions(self) -> List[SC2Mission]:
        """Returns a list of all missions used in the mission order."""
        return self.mission_pools.get_used_missions()
    
    def get_mission_count(self) -> int:
        """Returns the amount of missions in the mission order."""
        return sum(
            len([mission for mission in layout.missions if not mission.option_empty])
            for campaign in self.mission_order_node.campaigns for layout in campaign.layouts
        )

    def get_starting_missions(self) -> List[SC2Mission]:
        """Returns a list containing all the missions that are accessible without beating any other missions."""
        return [
            slot.mission
            for campaign in self.mission_order_node.campaigns if campaign.is_always_unlocked()
            for layout in campaign.layouts if layout.is_always_unlocked()
            for slot in layout.missions if slot.is_always_unlocked() and not slot.option_empty
        ]

    def get_completion_condition(self, player: int) -> Callable[[CollectionState], bool]:
        """Returns a lambda to determine whether a state has beaten the mission order's required campaigns."""
        final_locations = [get_goal_location(mission.mission) for mission in self.get_final_missions()]
        return lambda state, final_locations=final_locations: all(state.can_reach_location(loc, player) for loc in final_locations)

    def get_final_mission_ids(self) -> List[int]:
        """Returns the IDs of all missions that are required to beat the mission order."""
        return [mission.mission.id for mission in self.get_final_missions()]

    def get_final_missions(self) -> List['SC2MOGenMission']:
        """Returns the slots of all missions that are required to beat the mission order."""
        return self.mission_order_node.goal_missions

    def get_items_to_lock(self) -> Dict[str, int]:
        """Returns a dict of item names and amounts that are required by Item entry rules."""
        return self.mission_order_node.items_to_lock

    def get_slot_data(self) -> List[Dict[str, Any]]:
        """Parses the mission order into a format usable for slot data."""
        return self.mission_order_node.get_slot_data()

