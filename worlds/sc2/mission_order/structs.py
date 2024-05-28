from __future__ import annotations
from typing import Dict, Set, Callable, Tuple, List, Any, Type, Optional, NamedTuple, Union, TypeVar
from collections.abc import Iterable
from enum import IntEnum

from BaseClasses import Region, Location, CollectionState, Entrance, ItemClassification
from ..mission_tables import SC2Mission, SC2Race, SC2Campaign, lookup_name_to_mission, MissionFlag, lookup_id_to_mission, get_goal_location
from worlds.AutoWorld import World

# TODO band-aid for ..locations circular import
LocationData = Any

class Difficulty(IntEnum):
    RELATIVE = 0
    STARTER = 1
    EASY = 2
    MEDIUM = 3
    HARD = 4
    VERY_HARD = 5

class LayoutType:
    size: int
    limit: int

    def __init__(self, size: int, limit: int):
        self.size = size
        self.limit = limit

    def make_slots(self, mission_factory: Callable[[], SC2MOGenMission]) -> List[SC2MOGenMission]:
        """Use the provided `Callable` to create a one-dimensional list of mission slots and set up initial settings and connections.

        This should include at least one entrance and exit."""
        return []
    
    def get_slot_data(self, slots: List[SC2MOGenMission]) -> List[List[SC2MOGenMission]]:
        """Given the previously created list of mission slots, organize them into a list of columns from left to right and top to bottom.
        
        The resulting 2D list should be rectangular."""
        pass

# TODO figure out an organic way to get these
DEFAULT_DIFFICULTY_THRESHOLDS = {
    Difficulty.STARTER: 0,
    Difficulty.EASY: 5,
    Difficulty.MEDIUM: 35,
    Difficulty.HARD: 65,
    Difficulty.VERY_HARD: 95,
    Difficulty.VERY_HARD + 1: 100
}

def _modified_difficulty_thresholds(min: Difficulty, max: Difficulty) -> Dict[int, Difficulty]:
    if min == Difficulty.RELATIVE:
        min = Difficulty.STARTER
    if max == Difficulty.RELATIVE:
        max = Difficulty.VERY_HARD
    thresholds: Dict[int, Difficulty] = {}
    min_thresh = DEFAULT_DIFFICULTY_THRESHOLDS[min]
    total_thresh = DEFAULT_DIFFICULTY_THRESHOLDS[max + 1] - min_thresh
    for difficulty in range(min, max + 1):
        threshold = DEFAULT_DIFFICULTY_THRESHOLDS[difficulty] - min_thresh
        threshold *= 100 / total_thresh
        thresholds[int(threshold)] = Difficulty(difficulty)
    return thresholds

_T = TypeVar('_T')
def _find_by_name(
        term: str, objects: Iterable[_T], searcher: Union[_T, None] = None,
        error_name: str = "object", full_term: str = "", fail_allowed: bool = False
) -> _T:
    if searcher and searcher.option_name.casefold() == term.casefold():
        raise ValueError(f"{error_name.capitalize()} at address \"{full_term}\" tried to find itself (\"{term}\"). This would create a circular requirement.")
    search = [obj for obj in objects if obj.option_name.casefold() == term.casefold()]
    if len(search) == 0:
        if fail_allowed:
            return None
        raise ValueError(f"Address \"{full_term}\" could not find {error_name} with name \"{term}\". Please check the spelling of {error_name} names.")
    if len(search) > 1:
        raise ValueError(f"Address \"{full_term}\" found multiple {error_name}s with name \"{term}\". Please make sure only one {error_name} with the given name exists.")
    return search[0]

def _find_mission_by_index(term: str, missions: List[SC2MOGenMission], searcher: Union[SC2MOGenMission, None] = None, full_term: str = "") -> SC2MOGenMission:
    index = -1
    try:
        index = int(term)
    except ValueError:
        raise ValueError(f"Address \"{full_term}\" contains index \"{term}\", which is not a number.")
    if index < 0 or index >= len(missions):
        raise ValueError(f"Address \"{full_term}\" contains index \"{term}\", which is out of bounds.")
    mission = missions[index]
    if mission == searcher:
        raise ValueError(f"Mission at address \"{full_term}\" tried to find itself. This would create a circular requirement.")
    if mission.option_empty:
        raise ValueError(f"Mission at address \"{full_term}\" is an empty slot. This is an impossible requirement.")
    return mission

class SC2MOGenMissionPools:
    """
    Manages available and used missions for a mission order.
    """
    master_list: Set[int]
    difficulty_pools: Dict[Difficulty, Set[int]]
    _used_flags: Dict[MissionFlag, int]
    _used_missions: Set[SC2Mission]

    def __init__(self):
        self.master_list = {mission.id for mission in SC2Mission}
        self.difficulty_pools = {
            diff: {mission.id for mission in SC2Mission if mission.pool + 1 == diff}
            for diff in Difficulty if diff != Difficulty.RELATIVE
        }
        self._used_flags = {}
        self._used_missions = set()

    def set_exclusions(self, excluded: List[str], unexcluded: List[str]):
        """Prevents all the missions that appear in the `excluded` list, but not in the `unexcluded` list,
        from appearing in the mission order."""
        total_exclusions = [lookup_name_to_mission[name] for name in excluded if name not in unexcluded]
        self.master_list.difference_update(total_exclusions)

    def move_mission(self, mission: SC2Mission, old_diff: Difficulty, new_diff: Difficulty):
        """Changes the difficulty of the given `mission`. Does nothing if the mission is not allowed to appear
        or if it isn't set to the `old_diff` difficulty."""
        if mission.id in self.master_list and mission.id in self.difficulty_pools[old_diff]:
            self.difficulty_pools[old_diff].remove(mission.id)
            self.difficulty_pools[new_diff].add(mission.id)

    def get_pool_size(self, diff: Difficulty) -> int:
        """Returns the amount of missions of the given difficulty that are allowed to appear."""
        return len(self.difficulty_pools[diff])
    
    def get_used_flags(self) -> Dict[MissionFlag, int]:
        """Returns a dictionary of all used flags and their appearance count within the mission order.
        Flags that don't appear in the mission order also don't appear in this dictionary."""
        return self._used_flags

    def get_used_missions(self) -> Set[SC2Mission]:
        """Returns a set of all missions used in the mission order."""
        return self._used_missions

    def pull_specific_mission(self, mission: SC2Mission):
        """Marks the given mission as present in the mission order."""
        # Remove the mission from the master list and whichever difficulty pool it is in
        if mission.id in self.master_list:
            self.master_list.remove(mission.id)
            for diff in self.difficulty_pools:
                if mission.id in self.difficulty_pools[diff]:
                    self.difficulty_pools[diff].remove(mission.id)
                    break
        self._add_mission_stats(mission)
    
    def _add_mission_stats(self, mission: SC2Mission):
        # Update used flag counts & missions
        for flag in mission.flags:
            self._used_flags.setdefault(flag, 0)
            self._used_flags[flag] += 1
        self._used_missions.add(mission)

    def pull_random_mission(self, world: World, slot: SC2MOGenMission, locked_ids: List[int]) -> SC2Mission:
        """Picks a random mission from the mission pool of the given slot, preferring a mission from `locked_ids` if allowed in the slot,
        and marks it as present in the mission order."""
        # Use a locked mission if possible in this slot
        base_pool = slot.option_mission_pool.intersection(self.master_list)
        allowed_locked = base_pool.intersection(locked_ids)
        if len(allowed_locked) > 0:
            pool = allowed_locked
        else:
            pool = base_pool
        
        difficulty_pools = {
            diff: list(pool.intersection(self.difficulty_pools[diff]))
            for diff in Difficulty if diff != Difficulty.RELATIVE
        }

        # Iteratively look down and up around the slot's desired difficulty
        # Either a difficulty with valid missions is found, or an error is raised
        final_pool = []
        final_difficulty = Difficulty.RELATIVE
        desired_diff = slot.option_difficulty
        diff_offset = 0
        while len(final_pool) == 0:
            lower_diff = max(desired_diff - diff_offset, 1)
            higher_diff = min(desired_diff + diff_offset, 5)
            final_pool = difficulty_pools[lower_diff]
            if len(final_pool) > 0:
                final_difficulty = lower_diff
                break
            final_pool = difficulty_pools[higher_diff]
            if len(final_pool) > 0:
                final_difficulty = higher_diff
                break
            if lower_diff == Difficulty.STARTER and higher_diff == Difficulty.VERY_HARD:
                raise Exception(f"Slot in campaign \"{slot.parent_campaign.option_name}\" and layout \"{slot.parent_layout.option_name}\" ran out of possible missions to place.")
            diff_offset += 1
        
        # Remove the mission from the master list
        mission = lookup_id_to_mission[world.random.choice(final_pool)]
        self.master_list.remove(mission.id)
        self.difficulty_pools[final_difficulty].remove(mission.id)
        self._add_mission_stats(mission)
        return mission

class SC2MissionOrder:
    """
    The top-level data structure for mission orders. Contains helper functions for getting data about generated missions.
    """
    campaigns: List[SC2MOGenCampaign]
    ordered_campaigns: Dict[int, List[SC2MOGenCampaign]]
    sorted_missions: Dict[Difficulty, List[SC2MOGenMission]]
    fixed_missions: Set[SC2MOGenMission]
    mission_pools: SC2MOGenMissionPools
    max_steps: int

    entrances: Set[SC2MOGenCampaign]

    def __init__(self, world: World, data: Dict[str, Any]):
        self.campaigns = []
        self.ordered_campaigns = dict()
        self.sorted_missions = {diff: [] for diff in Difficulty if diff != Difficulty.RELATIVE}
        self.fixed_missions = set()
        self.entrances = set()
        self.mission_pools = SC2MOGenMissionPools()

        for (campaign_name, campaign_data) in data.items():
            campaign = SC2MOGenCampaign(world, campaign_name, campaign_data)
            self.ordered_campaigns.setdefault(campaign.option_order, []).append(campaign)
        orders = sorted(self.ordered_campaigns.keys())
        for order in orders:
            world.random.shuffle(self.ordered_campaigns[order])
            self.campaigns.extend(self.ordered_campaigns[order])
        
        # Check that any campaigns are actually set to required
        any_required = False
        for campaign in self.campaigns:
            if campaign.required:
                any_required = True
                break
        # If not, set the highest-order campaigns as required
        if not any_required:
            for campaign in self.ordered_campaigns[orders[-1]]:
                campaign.option_required = True
        
        self.entrances = {campaign for campaign in self.ordered_campaigns[orders[0]]}
    
    def get_used_flags(self) -> Dict[MissionFlag, int]:
        """Returns a dictionary of all used flags and their appearance count within the mission order.
        Flags that don't appear in the mission order also don't appear in this dictionary."""
        return self.mission_pools.get_used_flags()
    
    def get_used_missions(self) -> Set[SC2Mission]:
        """Returns a set of all missions used in the mission order."""
        return self.mission_pools.get_used_missions()
    
    def get_starting_missions(self) -> Set[SC2Mission]:
        """Returns a set containing all the missions that are accessible without beating any other missions."""
        # Entrance missions of entrance layouts of entrance campaigns that have no requirements
        return {
            mission.mission
            for campaign in self.entrances for layout in campaign.entrances for mission in layout.entrances
            if campaign.is_always_unlocked() and layout.is_always_unlocked() and mission.is_always_unlocked()
        }

    def get_completion_condition(self, player: int) -> Callable[[CollectionState], bool]:
        """Returns a lambda to determine whether a state has beaten the mission order's required campaigns."""
        final_items = [mission.beat_item() for mission in self.get_final_missions()]
        return lambda state, final_items=final_items: state.has_all(final_items, player)

    def get_final_mission_ids(self) -> List[int]:
        """Returns the IDs of all missions that are required to beat the mission order."""
        return [mission.mission.id for mission in self.get_final_missions()]

    def get_final_missions(self) -> List[SC2MOGenMission]:
        """Returns the slots of all missions that are required to beat the mission order."""
        return [mission for campaign in self.campaigns for mission in campaign.required if campaign.option_required]

    def get_slot_data(self) -> Dict[str, Dict[str, List[List[Tuple[int, Dict[str, Any]]]]]]:
        """Parses the mission order into a format usable for slot data."""
        # {"campaign": {"layout": [[(mission id, requirement), ...], ...]}}
        return {
            campaign.option_name: {
                layout.option_name: layout.get_slot_data()
                for layout in campaign.layouts
            }
            for campaign in self.campaigns
        }

    def make_connections(self, world: World):
        cur_campaigns = {campaign for campaign in self.entrances}
        names: Dict[str, int] = {}
        while len(cur_campaigns) > 0:
            campaign = cur_campaigns.pop()
            cur_campaigns.update(campaign.next)
            cur_layouts = {layout for layout in campaign.entrances}
            while len(cur_layouts) > 0:
                layout = cur_layouts.pop()
                cur_layouts.update(layout.next)
                seen_missions: Set[SC2MOGenMission] = set()
                cur_missions = {mission for mission in layout.entrances}
                while len(cur_missions) > 0:
                    mission = cur_missions.pop()
                    seen_missions.add(mission)
                    cur_missions.update(mission.next.difference(seen_missions))
                    mission.make_connections(world, names)
        
    def fill_min_steps(self):
        steps = 0

        cur_campaigns: Set[SC2MOGenCampaign] = set()
        beaten_campaigns: Set[SC2MOGenCampaign] = set()
        next_campaigns: Set[SC2MOGenCampaign] = {campaign for campaign in self.entrances}

        cur_layouts: Dict[str, Set[SC2MOGenLayout]] = {}
        beaten_layouts: Dict[str, Set[SC2MOGenLayout]] = {campaign.option_name: set() for campaign in self.campaigns}
        next_layouts: Dict[str, Set[SC2MOGenLayout]] = {}

        beaten_missions: Set[SC2MOGenMission] = set()
        beaten_campaign_missions: Dict[str, Set[SC2MOGenMission]] = {campaign.option_name: set() for campaign in self.campaigns}
        next_missions: Set[SC2MOGenMission] = set()

        # Immediately accessible are the always-unlocked missions of the always-unlocked layouts of the always-unlocked campaigns
        new_campaigns: Set[SC2MOGenCampaign] = set()
        for campaign in next_campaigns:
            if campaign.is_unlocked(beaten_campaigns, beaten_missions):
                cur_campaigns.add(campaign)
                new_campaigns.update(campaign.next)
                next_layouts[campaign.option_name] = {layout for layout in campaign.entrances}
                cur_layouts[campaign.option_name] = set()
        next_campaigns.difference_update(cur_campaigns)
        next_campaigns.update(new_campaigns)
        for campaign in next_layouts:
            new_layouts: Set[SC2MOGenLayout] = set()
            for layout in next_layouts[campaign]:
                if layout.is_unlocked(beaten_layouts[campaign], beaten_missions):
                    cur_layouts[campaign].add(layout)
                    new_layouts.update(layout.next)
                    next_missions.update(layout.entrances)
            next_layouts[campaign].difference_update(cur_layouts[campaign])
            next_layouts[campaign].update(new_layouts)
        
        # Sanity check: Can any missions be accessed?
        if len(next_missions) == 0:
            raise Exception("Mission order has no possibly accessible missions")

        while len(next_missions) > 0:
            # Check for accessible missions
            cur_missions: Set[SC2MOGenMission] = {
                mission for mission in next_missions
                if mission.is_unlocked(beaten_missions, beaten_campaign_missions[mission.parent_campaign.option_name])
            }
            if len(cur_missions) == 0:
                raise Exception(f"Mission order ran out of accessible missions at depth {steps}")
            next_missions.difference_update(cur_missions)
            # Set the step counters of all currently accessible missions
            while len(cur_missions) > 0:
                mission = cur_missions.pop()
                beaten_missions.add(mission)
                beaten_campaign_missions[mission.parent_campaign.option_name].add(mission)
                mission.min_steps = steps
                next_missions.update(mission.next.difference(cur_missions, beaten_missions))
            
            # Any campaigns/layouts/missions added after this point will be seen in the next iteration at the earliest
            steps += 1

            # Check for newly beaten campaigns & layout
            for campaign in cur_campaigns:
                # Campaigns are beaten when all required missions have been seen
                if campaign.is_beaten(beaten_missions):
                    beaten_campaigns.add(campaign)
                # Layouts are beaten when all exit missions have been seen
                for layout in cur_layouts[campaign.option_name]:
                    if layout.is_beaten(beaten_missions):
                        beaten_layouts[campaign.option_name].add(layout)

            # Check whether upcoming campaigns & layouts are now accessible
            new_campaigns: Set[SC2MOGenCampaign] = set()
            for campaign in next_campaigns:
                if campaign.is_unlocked(beaten_campaigns, beaten_missions):
                    cur_campaigns.add(campaign)
                    new_campaigns.update(campaign.next)
                    next_layouts[campaign.option_name] = {layout for layout in campaign.entrances}
                    cur_layouts[campaign.option_name] = set()
            next_campaigns.difference_update(cur_campaigns)
            next_campaigns.update(new_campaigns)
            for campaign in next_layouts:
                new_layouts: Set[SC2MOGenLayout] = set()
                for layout in next_layouts[campaign]:
                    if layout.is_unlocked(beaten_layouts[campaign], beaten_missions):
                        cur_layouts[campaign].add(layout)
                        new_layouts.update(layout.next)
                        next_missions.update(layout.entrances)
                next_layouts[campaign].difference_update(cur_layouts[campaign])
                next_layouts[campaign].update(new_layouts)
        
            # Remove fully beaten campaigns & layouts
            done_campaigns: Set[SC2MOGenCampaign] = set()
            for campaign in cur_campaigns:
                # Layouts are fully beaten when all their missions are beaten
                done_layouts: Set[SC2MOGenLayout] = set()
                for layout in cur_layouts[campaign.option_name]:
                    if beaten_missions.issuperset([mission for mission in layout.missions if not mission.option_empty]):
                        step_counts = [mission.min_steps for mission in layout.missions if not mission.option_empty]
                        layout.min_steps = min(step_counts)
                        layout.max_steps = max(step_counts)
                        done_layouts.add(layout)
                cur_layouts[campaign.option_name].difference_update(done_layouts)
                # Campaigns are fully beaten when all their layouts are fully beaten
                if len(cur_layouts[campaign.option_name]) == 0:
                    campaign.min_steps = min(layout.min_steps for layout in campaign.layouts)
                    campaign.max_steps = max(layout.max_steps for layout in campaign.layouts)
                    done_campaigns.add(campaign)
            cur_campaigns.difference_update(done_campaigns)
        self.max_steps = steps - 1
    
    def resolve_difficulties(self):
        for campaign in self.campaigns:
            (campaign_sorted, campaign_fixed) = campaign.resolve_difficulties(self.max_steps)
            self.fixed_missions.update(campaign_fixed)
            for (diff, missions) in campaign_sorted.items():
                self.sorted_missions[diff].extend(missions)
    
    def resolve_unlocks(self):
        orders = sorted(self.ordered_campaigns.keys())
        # campaign/layout.next should hold campaigns/layouts that may be unlocked via the order/count mechanism by beating this layout
        #   mission.next is handled by layout type
        #   a campaign/layout is either:
        #     a lowest-order object: then it is an entrance
        #     a non-lowest-order object: then there exists an object whose .next contains this object
        #   so when starting at entrances, this setup iteratively covers every object
        #   always-unlocked objects are additionally made entrances and removed from .nexts
        # campaign/layout.prev should hold campaigns/layouts that may be required via the order/count mechanism
        #   mission.prev is handled by layout init
        # campaign/layout/mission.unlock_specific_* should hold campaigns/layouts/missions required by the campaign/layout
        #   this needs to be rolled down to only missions somewhere
        #   unlock_specific_missions holds missions that are required
        #   unlock_specific_layouts holds layouts whose exit missions (layout.exits) are required
        #   unlock_specific_campaigns holds campaigns whose required missions (campaign.required) are required
        #   => campaign/layout/mission.unlock_missions is a set of hard required remote missions
        for idx in range(len(orders) - 1):
            low_order = orders[idx]
            high_order = orders[idx + 1]
            for campaign in self.ordered_campaigns[low_order]:
                campaign.next.update(self.ordered_campaigns[high_order])
            for campaign in self.ordered_campaigns[high_order]:
                campaign.prev.update(self.ordered_campaigns[low_order])
        for campaign in self.campaigns:
            orders = sorted(campaign.ordered_layouts.keys())
            for idx in range(len(orders) - 1):
                low_order = orders[idx]
                high_order = orders[idx + 1]
                for layout in campaign.ordered_layouts[low_order]:
                    layout.next.update(campaign.ordered_layouts[high_order])
                for layout in campaign.ordered_layouts[high_order]:
                    layout.prev.update(campaign.ordered_layouts[low_order])
            
            # Address parsing
            # campaign-level addresses: "campaign", "campaign/layout", "campaign/layout/index"
            # layout-level addresses: ^ + "layout", "layout/index"
            # mission-level addresses: ^ + "index"
            # parent campaign/layout can be implicit
            for address in campaign.option_unlock_specific:
                parts = address.split('/')
                other_campaign = _find_by_name(parts[0], self.campaigns, campaign, "campaign", address)
                if len(parts) == 1: # "campaign"
                    campaign.unlock_specific_campaigns.add(other_campaign)
                    campaign.unlock_missions.update(other_campaign.required)
                elif len(parts) == 2: # "campaign/layout"
                    layout = _find_by_name(parts[1], other_campaign.layouts, None, "layout", address)
                    campaign.unlock_specific_layouts.add(layout)
                    campaign.unlock_missions.update(layout.exits)
                elif len(parts) == 3: # "campaign/layout/index"
                    layout = _find_by_name(parts[1], other_campaign.layouts, None, "layout", address)
                    mission = _find_mission_by_index(parts[2], layout.missions, None, address)
                    campaign.unlock_specific_missions.add(mission)
                    campaign.unlock_missions.add(mission)
                else:
                    raise ValueError(f"Address {address} contains too many '/'s.")
            for layout in campaign.layouts:
                for address in layout.option_unlock_specific:
                    parts = address.split('/')
                    other_campaign = _find_by_name(parts[0], self.campaigns, None, "campaign", address, True)
                    other_layout = None
                    if not other_campaign: # If the first part is not a campaign, assume it wants the local campaign
                        other_campaign = campaign
                        other_layout = _find_by_name(parts[0], campaign.layouts, layout, "layout", address)
                    if len(parts) == 1:
                        if other_layout: # [parent campaign]/"layout"
                            layout.unlock_specific_layouts.add(other_layout)
                            layout.unlock_missions.update(other_layout.exits)
                        else: # "campaign"
                            layout.unlock_specific_campaigns.add(other_campaign)
                            layout.unlock_missions.update(other_campaign.required)
                    elif len(parts) == 2:
                        if other_layout: # [parent campaign]/"layout/index"
                            mission = _find_mission_by_index(parts[1], other_layout.missions, None, address)
                            layout.unlock_specific_missions.add(mission)
                            layout.unlock_missions.add(mission)
                        else: # "campaign/layout"
                            other_layout = _find_by_name(parts[1], other_campaign.layouts, layout, "layout", address)
                            layout.unlock_specific_layouts.add(other_layout)
                            layout.unlock_missions.update(other_layout.exits)
                    elif len(parts) == 3: # "campaign/layout/index"
                        if other_layout:
                            raise ValueError(f"Address {address} could not find campaign with name \"{parts[0]}\". Please check the spelling of campaign names.")
                        other_layout = _find_by_name(parts[1], other_campaign.layouts, layout, "layout", address)
                        mission = _find_mission_by_index(parts[2], other_layout.missions, None, address)
                        layout.unlock_specific_missions.add(mission)
                        layout.unlock_missions.update(mission)
                    else:
                        raise ValueError(f"Address {address} contains too many '/'s.")
                for mission in layout.missions:
                    for address in mission.option_unlock_specific:
                        parts = address.split('/')
                        other_campaign = _find_by_name(parts[0], self.campaigns, None, "campaign", address, True)
                        other_layout = None
                        other_mission = None
                        if not other_campaign: # If the first part is not a campaign, assume it wants the local campaign
                            other_campaign = campaign
                            other_layout = _find_by_name(parts[0], campaign.layouts, None, "layout", address, True)
                            if not other_layout: # If the first part is not a layout either, assume it wants the local layout
                                other_layout = layout
                                other_mission = _find_mission_by_index(parts[0], layout.missions, mission, address)
                        if len(parts) == 1:
                            if other_mission: # [parent campaign]/[parent layout]/"index"
                                mission.unlock_specific_missions.add(other_mission)
                                mission.unlock_missions.add(other_mission)
                            elif other_layout: # [parent campaign]/"layout"
                                mission.unlock_specific_layouts.add(other_layout)
                                mission.unlock_missions.update(other_layout.exits)
                            elif other_campaign: # "campaign"
                                mission.unlock_specific_campaigns.add(other_campaign)
                                mission.unlock_missions.update(other_campaign.required)
                            else:
                                raise ValueError(f"Address {address} could not find campaign or layout with name \"{parts[0]}\". Please check the spelling of campaign and layout names.")
                        elif len(parts) == 2:
                            if other_mission: # Error: "index/???"
                                raise ValueError(f"Address {address} could not find campaign or layout with name \"{parts[0]}\". Please check the spelling of campaign and layout names.")
                            elif other_layout: # [parent campaign]/"layout/index"
                                other_mission = _find_mission_by_index(parts[1], other_layout.missions, mission, address)
                                mission.unlock_specific_missions.add(other_mission)
                                mission.unlock_missions.add(other_mission)
                            else: # "campaign/layout"
                                other_layout = _find_by_name(parts[1], other_campaign.layouts, None, "layout", address)
                                mission.unlock_specific_layouts.add(other_layout)
                                mission.unlock_missions.update(other_layout.exits)
                        elif len(parts) == 3:
                            if other_mission: # Error: "index/???/???"
                                raise ValueError(f"Address {address} could not find campaign with name \"{parts[0]}\". Please check the spelling of campaign names.")
                            elif other_layout: # Error: "layout/???/???"
                                raise ValueError(f"Address {address} could not find campaign with name \"{parts[0]}\". Please check the spelling of campaign names.")
                            else: # "campaign/layout/index"
                                other_layout = _find_by_name(parts[1], other_campaign.layouts, None, "layout", address)
                                other_mission = _find_mission_by_index(parts[2], other_layout.missions, mission, address)
                                mission.unlock_specific_missions.add(other_mission)
                                mission.unlock_missions.add(other_mission)
                        else:
                            raise ValueError(f"Address {address} contains too many '/'s.")
    
        # Set up entrance campaigns/layouts
        for campaign in self.campaigns:
            if campaign.is_always_unlocked():
                self.entrances.add(campaign)
                for prev_campaign in campaign.prev:
                    prev_campaign.next.remove(campaign)
                campaign.prev.clear()
            for layout in campaign.layouts:
                if layout.is_always_unlocked():
                    campaign.entrances.add(layout)
                    for prev_layout in layout.prev:
                        prev_layout.next.remove(layout)
                    layout.prev.clear()


    def fill_missions(
            self, world: World, locked_missions: List[str],
            locations: Tuple[LocationData], location_cache: List[Location]
    ):
        locations_per_region = get_locations_per_region(locations)
        regions: List[Region] = [create_region(world, locations_per_region, location_cache, "Menu")]
        locked_ids = [lookup_name_to_mission[mission].id for mission in locked_missions]

        # Resolve slots with set mission names
        for mission_slot in self.fixed_missions:
            mission = lookup_name_to_mission[mission_slot.option_mission]
            self.mission_pools.pull_specific_mission(mission)
            mission_slot.set_mission(world, mission, locations_per_region, location_cache)
            regions.append(mission_slot.region)

        # Shuffle & sort all slots to pick from smallest to biggest pool with tie-breaks by difficulty (lowest to highest), then randomly
        for diff in sorted(self.sorted_missions.keys()):
            world.random.shuffle(self.sorted_missions[diff])
        all_slots = [slot for diff in sorted(self.sorted_missions.keys()) for slot in self.sorted_missions[diff]]
        all_slots.sort(key = lambda slot: len(slot.option_mission_pool.intersection(self.mission_pools.master_list)))

        # Pick random missions
        for mission_slot in all_slots:
            mission = self.mission_pools.pull_random_mission(world, mission_slot, locked_ids)
            if mission.id in locked_ids:
                locked_ids.remove(mission.id)
            mission_slot.set_mission(world, mission, locations_per_region, location_cache)
            regions.append(mission_slot.region)

        world.multiworld.regions += regions

class SC2MOGenCampaign:
    option_name: str # name of this campaign
    option_order: int # order of this campaign
    option_unlock_count: int # how many previous-order campaigns are required to enter this campaign
    option_unlock_specific: List[str] # which specific campaigns are required to enter this campaign
    option_required: bool # whether this campaign is required to beat the game
    # minimum difficulty of this campaign
    # 'relative': based on the median distance of the first mission
    option_min_difficulty: Difficulty
    # maximum difficulty of this campaign
    # 'relative': based on the median distance of the last mission
    option_max_difficulty: Difficulty

    # layouts of this campaign in correct order
    layouts: List[SC2MOGenLayout]
    # layouts of this campaign, sorted by order, in unknown order
    ordered_layouts: Dict[int, List[SC2MOGenLayout]]
    entrances: Set[SC2MOGenLayout]
    exits: Set[SC2MOGenLayout]
    required: Set[SC2MOGenMission] # missions required to beat this campaign (layouts & missions marked "required")
    region: Region

    next: Set[SC2MOGenCampaign]
    prev: Set[SC2MOGenCampaign]
    # TODO these three are currently unused
    unlock_specific_campaigns: Set[SC2MOGenCampaign]
    unlock_specific_layouts: Set[SC2MOGenLayout]
    unlock_specific_missions: Set[SC2MOGenMission]

    unlock_missions: Set[SC2MOGenMission] # remote missions required to access this campaign
    # TODO these two are currently unused
    min_steps: int
    max_steps: int

    def __init__(self, world: World, name: str, data: Dict[str, Any]):
        self.option_name = name
        self.option_order = data["order"]
        self.option_unlock_count = data["unlock_count"]
        self.option_unlock_specific = data["unlock_specific"]
        self.option_required = data["required"]
        self.option_min_difficulty = data["min_difficulty"]
        self.option_max_difficulty = data["max_difficulty"]
        self.layouts = []
        self.ordered_layouts = dict()
        self.entrances = set()
        self.exits = set()
        self.next = set()
        self.prev = set()
        self.unlock_specific_campaigns = set()
        self.unlock_specific_layouts = set()
        self.unlock_specific_missions = set()
        self.unlock_missions = set()
        self.required = set()
        self.min_steps = 0
        self.max_steps = 0

        for (layout_name, layout_data) in data.items():
            if type(layout_data) == dict:
                layout = SC2MOGenLayout(self, layout_name, layout_data)
                self.ordered_layouts.setdefault(layout_data["order"], []).append(layout)
                # Collect required missions (marked layouts' exits and marked missions)
                if layout.option_required:
                    self.exits.add(layout)
                    self.required.update(layout.exits)
                for mission in layout.missions:
                    if mission.option_required:
                        self.required.update(layout.exits)
                
        orders = sorted(self.ordered_layouts.keys())
        for order in orders:
            world.random.shuffle(self.ordered_layouts[order])
            self.layouts.extend(self.ordered_layouts[order])
        self.entrances.update(self.ordered_layouts[orders[0]])
        # Only use default exits if no exits are manually set
        if len(self.exits) == 0 and len(self.required) == 0:
            self.exits.update(self.ordered_layouts[orders[-1]])
            for req_layout in self.exits:
                req_layout.option_required = True
        # If there are no missions or layouts marked as required, pick the exit missions of the highest-order layouts
        if len(self.required) == 0:
            self.required.update(exit_mission for layout in self.ordered_layouts[orders[-1]] for exit_mission in layout.exits)
            for req_mission in self.required:
                req_mission.option_required = True
    
    def is_beaten(self, beaten_missions: Set[SC2MOGenMission]) -> bool:
        return beaten_missions.issuperset(self.required)

    def is_always_unlocked(self) -> bool:
        return self.is_unlocked(set(), set())

    def is_unlocked(self, beaten_campaigns: Set[SC2MOGenCampaign], beaten_missions: Set[SC2MOGenMission]) -> bool:
        # Count/Order requirement: Amount of beaten previous-order campaigns must be >= count option
        count_required = self.option_unlock_count
        # If count is -1, all previous-order campaigns are required
        if count_required == -1:
            count_required = len(self.prev)
        beaten_prev_campaigns = beaten_campaigns.intersection(self.prev)
        count_requirement: bool = len(beaten_prev_campaigns) >= self.option_unlock_count
            
        # Specific requirement: All required remote missions are required
        specific_requirement: bool = beaten_missions.issuperset(self.unlock_missions)
        
        return count_requirement and specific_requirement

    def resolve_difficulties(self, total_steps: int) -> Tuple[Dict[Difficulty, Set[SC2MOGenMission]], Set[SC2MOGenMission]]:
        sorted_missions: Dict[Difficulty, Set[SC2MOGenMission]] = {diff: set() for diff in Difficulty if diff != Difficulty.RELATIVE}
        fixed_missions: Set[SC2MOGenMission] = set()
        for layout in self.layouts:
            (layout_sorted, layout_fixed) = layout.resolve_difficulties(total_steps, self.option_min_difficulty, self.option_max_difficulty)
            fixed_missions.update(layout_fixed)
            for (diff, missions) in layout_sorted.items():
                sorted_missions[diff].update(missions)
        return (sorted_missions, fixed_missions)

    def get_prev_id_sets(self) -> List[Set[int]]:
        return [{mission.mission.id for mission in campaign.required} for campaign in self.prev]

class SC2MOGenLayout:
    option_name: str # name of this layout
    option_order: int # order of this layout
    option_type: Type[LayoutType] # type of this layout
    option_size: int # amount of missions in this layout
    option_limit: int # secondary size limit of this layout
    option_required: bool # whether this layout is required to beat the campaign
    option_mission_pool: List[int] # IDs of valid missions for this layout

    option_unlock_count: int # how many previous-order layouts are required to enter this layout
    option_unlock_specific: List[str] # which specific layouts are required to enter this layout

    # minimum difficulty of this layout
    # 'relative': based on the median distance of the first mission
    option_min_difficulty: Difficulty
    # maximum difficulty of this layout
    # 'relative': based on the median distance of the last mission
    option_max_difficulty: Difficulty

    missions: List[SC2MOGenMission]
    layout_type: LayoutType
    entrances: Set[SC2MOGenMission]
    exits: Set[SC2MOGenMission]
    region: Region

    next: Set[SC2MOGenLayout]
    prev: Set[SC2MOGenLayout]
    # TODO these three are currently unused
    unlock_specific_campaigns: Set[SC2MOGenCampaign]
    unlock_specific_layouts: Set[SC2MOGenLayout]
    unlock_specific_missions: Set[SC2MOGenMission]

    unlock_missions: Set[SC2MOGenMission] # missions required to access this layout
    min_steps: int
    max_steps: int

    def __init__(self, parent_campaign: SC2MOGenCampaign, name: str, data: Dict):
        self.option_name = name
        self.option_order = data["order"]
        self.option_type = data["type"]
        self.option_size = data["size"]
        self.option_limit = data["limit"]
        self.option_required = data["required"]
        self.option_mission_pool = data["mission_pool"]
        self.option_unlock_count = data["unlock_count"]
        self.option_unlock_specific = data["unlock_specific"]
        self.option_min_difficulty = data["min_difficulty"]
        self.option_max_difficulty = data["max_difficulty"]
        self.missions = []
        self.entrances = set()
        self.exits = set()
        self.next = set()
        self.prev = set()
        self.unlock_specific_campaigns = set()
        self.unlock_specific_layouts = set()
        self.unlock_specific_missions = set()
        self.unlock_missions = set()
        self.min_steps = 0
        self.max_steps = 0

        # Check for positive size now instead of during YAML validation to actively error with default size
        if self.option_size == 0:
            raise ValueError(f"Layout \"{self.option_name}\" has a size of 0.")

        # Build base layout
        self.layout_type: LayoutType = self.option_type(self.option_size, self.option_limit)
        mission_factory = lambda: SC2MOGenMission(parent_campaign, self, self.option_mission_pool)
        self.missions = self.layout_type.make_slots(mission_factory)
        for (slot, mission_data) in data.items():
            if type(slot) == int:
                self.missions[slot].update_with_data(mission_data)
        for mission in self.missions:
            if mission.option_entrance:
                self.entrances.add(mission)
            if mission.option_exit:
                self.exits.add(mission)
            if len(mission.option_next) > 0:
                mission.next = {self.missions[idx] for idx in mission.option_next}
        
        # Set up missions' prev data
        seen_missions: Set[SC2MOGenMission] = set()
        cur_missions: Set[SC2MOGenMission] = {mission for mission in self.entrances}
        while len(cur_missions) > 0:
            mission = cur_missions.pop()
            seen_missions.add(mission)
            for next_mission in mission.next:
                next_mission.prev.add(mission)
                if next_mission not in seen_missions and \
                   next_mission not in cur_missions:
                    cur_missions.add(next_mission)
        
        # Remove empty missions from access data
        for mission in self.missions:
            if mission.option_empty:
                for next_mission in mission.next:
                    next_mission.prev.remove(mission)
                mission.next.clear()
                for prev_mission in mission.prev:
                    prev_mission.next.remove(mission)
                mission.prev.clear()
        
        # Clean up data and options
        all_empty = True
        for mission in self.missions:
            if mission.option_empty:
                # Empty missions cannot be entrances, exits, or required
                # This is done now instead of earlier to make "set all default entrances to empty" not fail
                if mission in self.entrances:
                    self.entrances.remove(mission)
                mission.option_entrance = False
                if mission in self.exits:
                    self.exits.remove(mission)
                mission.option_exit = False
                mission.option_required = False
            else:
                all_empty = False
                # Establish the following invariant:
                # A non-empty mission has no prev missions <=> A non-empty mission is an entrance
                # This is mandatory to guarantee the entire layout is accessible via consecutive .nexts
                # Note that the opposite is not enforced for exits to allow fully optional layouts
                if len(mission.prev) == 0:
                    mission.option_entrance = True
                    self.entrances.add(mission)
                elif mission.option_entrance:
                    for prev_mission in mission.prev:
                        prev_mission.next.remove(mission)
                    mission.prev.clear()
        if all_empty:
            raise Exception(f"Layout \"{self.option_name}\" contains no missions.")
    
    def is_beaten(self, beaten_missions: Set[SC2MOGenMission]) -> bool:
        return beaten_missions.issuperset(self.exits)

    def is_always_unlocked(self) -> bool:
        return self.is_unlocked(set(), set())
    
    def is_unlocked(self, beaten_layouts: Set[SC2MOGenLayout], beaten_missions: Set[SC2MOGenMission]) -> bool:
        # Count/Order requirement: Amount of beaten previous-order layouts must be >= count option
        count_required = self.option_unlock_count
        # If count is -1, all previous-order layouts are required
        if count_required == -1:
            count_required = len(self.prev)
        beaten_prev_layouts = beaten_layouts.intersection(self.prev)
        count_requirement: bool = len(beaten_prev_layouts) >= count_required
        
        # Specific requirement: All required remote missions are required
        specific_requirement: bool = beaten_missions.issuperset(self.unlock_missions)
        
        return count_requirement and specific_requirement

    def resolve_difficulties(self, total_steps: int, parent_min: Difficulty, parent_max: Difficulty) \
        -> Tuple[Dict[Difficulty, Set[SC2MOGenMission]], Set[SC2MOGenMission]]:
        if self.option_min_difficulty == Difficulty.RELATIVE:
            min_diff = parent_min
            min_steps = 0
        else:
            min_diff = self.option_min_difficulty
            min_steps = self.min_steps
        if self.option_max_difficulty == Difficulty.RELATIVE:
            max_diff = parent_max
            max_steps = total_steps
        else:
            max_diff = self.option_max_difficulty
            max_steps = self.max_steps
        step_range = max_steps - min_steps
        if step_range == 0:
            # This can happen if layout size is 1 or layout is all entrances
            # Use minimum difficulty in this case
            step_range = 1
        # If min/max aren't relative, assume the limits are meant to show up
        layout_thresholds = _modified_difficulty_thresholds(min_diff, max_diff)
        thresholds = sorted(layout_thresholds.keys())
        sorted_missions: Dict[Difficulty, Set[SC2MOGenMission]] = {diff: set() for diff in Difficulty if diff != Difficulty.RELATIVE}
        fixed_missions: Set[SC2MOGenMission] = set()
        for mission in self.missions:
            if mission.option_empty:
                continue
            if len(mission.option_mission) > 0:
                fixed_missions.add(mission)
                continue
            if mission.option_difficulty == Difficulty.RELATIVE:
                mission_thresh = int((mission.min_steps - min_steps) * 100 / step_range)
                for i in range(len(thresholds)):
                    if thresholds[i] > mission_thresh:
                        mission.option_difficulty = layout_thresholds[thresholds[i - 1]]
                        break
                    mission.option_difficulty = layout_thresholds[thresholds[-1]]
            sorted_missions[mission.option_difficulty].add(mission)
        return (sorted_missions, fixed_missions)

    def get_slot_data(self) -> List[List[int, Dict[str, Any]]]:
        mission_slots = self.layout_type.get_slot_data(self.missions)
        return [[(-1 if row.option_empty else row.mission.id, row.get_slot_requirements()._asdict()) for row in column] for column in mission_slots]
    
    def get_prev_id_sets(self) -> List[Set[int]]:
        return [{mission.mission.id for mission in layout.exits} for layout in self.prev]

class SC2MOGenMission:
    option_required: bool # whether this mission is required to beat the campaign
    option_entrance: bool # whether this mission is unlocked when the layout is unlocked
    option_exit: bool # whether this mission is required to beat the layout
    option_empty: bool # whether this slot contains a mission at all
    option_mission: str # name of the specific mission for this mission
    option_next: List[int] # indices of internally connected missions
    option_unlock_count: int # amount of missions from this campaign required to unlock this mission
    option_unlock_specific: List[str] # which specific layouts are required to unlock this mission
    option_difficulty: Difficulty # difficulty pool this mission pulls from
    option_mission_pool: Set[int] # Allowed mission IDs for this slot

    parent_campaign: SC2MOGenCampaign # Parent campaign of this slot
    parent_layout: SC2MOGenLayout # Parent layout of this slot
    min_steps: int # Smallest amount of missions to beat before this slot is accessible

    mission: SC2Mission
    region: Region

    next: Set[SC2MOGenMission]
    prev: Set[SC2MOGenMission]
    unlock_specific_campaigns: Set[SC2MOGenCampaign]
    unlock_specific_layouts: Set[SC2MOGenLayout]
    unlock_specific_missions: Set[SC2MOGenMission]
    unlock_missions: Set[SC2MOGenMission]

    def __init__(self, parent_campaign: SC2MOGenCampaign, parent_layout: SC2MOGenLayout, parent_mission_pool: Set[int]):
        self.option_mission_pool = parent_mission_pool
        self.option_required = False
        self.option_entrance = False
        self.option_exit = False
        self.option_empty = False
        self.option_mission = ""
        self.option_next = []
        self.option_unlock_count = 0
        self.option_unlock_specific = []
        self.option_difficulty = Difficulty.RELATIVE
        self.parent_campaign = parent_campaign
        self.parent_layout = parent_layout
        self.next = set()
        self.unlock_specific_campaigns = set()
        self.unlock_specific_layouts = set()
        self.unlock_specific_missions = set()
        self.unlock_missions = set()
        self.prev = set()

    def update_with_data(self, data: Dict):
        self.option_required = data.get("required", self.option_required)
        self.option_entrance = data.get("entrance", self.option_entrance)
        self.option_exit = data.get("exit", self.option_exit)
        self.option_empty = data.get("empty", self.option_empty)
        self.option_mission = data.get("mission", self.option_mission)
        self.option_next = data.get("next", self.option_next)
        self.option_unlock_count = data.get("unlock_count", self.option_unlock_count)
        self.option_unlock_specific = data.get("unlock_specific", self.option_unlock_specific)
        self.option_difficulty = data.get("difficulty", self.option_difficulty)
        self.option_mission_pool = data.get("mission_pool", self.option_mission_pool)
    
    def set_mission(
            self, world: World, mission: SC2Mission,
            locations_per_region: Dict[str, List[LocationData]], location_cache: List[Location]
    ):
        self.mission = mission
        self.region = create_region(world, locations_per_region, location_cache,
                                    mission.mission_name)

    def is_always_unlocked(self) -> bool:
        return self.is_unlocked(set(), set())
    
    def is_unlocked(self, beaten_missions: Set[SC2MOGenMission], beaten_campaign_missions: Set[SC2MOGenMission]) -> bool:
        # Count/Order requirement: Amount of beaten missions from this slot's campaign must be >= count option
        count_requirement: bool = len(beaten_campaign_missions) >= self.option_unlock_count
        
        # Specific requirement: All required remote missions are required
        specific_requirement: bool = beaten_missions.issuperset(self.unlock_missions)
        
        return count_requirement and specific_requirement
    
    def beat_item(self) -> str:
        return f"Beat {self.mission.mission_name}"
    
    def beat_rule(self, player) -> Callable[[CollectionState], bool]:
        return lambda state: state.has(self.beat_item(), player)

    def is_campaign_entrance(self) -> bool:
        return self.parent_layout in self.parent_campaign.entrances and self.option_entrance

    def connect_rule(self, player: int) -> Callable[[CollectionState], bool]:
        # has_all is true for empty lists
        # This intentionally leaves out prev_missions because those are handled by the region connection

        required_missions = {mission for mission in self.unlock_missions}
        if self.is_campaign_entrance():
            required_missions.update(mission for mission in self.parent_campaign.unlock_missions)
        if self.option_entrance:
            required_missions.update(mission for mission in self.parent_layout.unlock_missions)

        if self.parent_campaign.option_unlock_count == -1:
            campaign_unlock_count = len(self.parent_campaign.prev)
        else:
            campaign_unlock_count = self.parent_campaign.option_unlock_count

        if self.parent_layout.option_unlock_count == -1:
            layout_unlock_count = len(self.parent_layout.prev)
        else:
            layout_unlock_count = self.parent_layout.option_unlock_count

        return lambda state: (
            # Specific requirement (beat all remote missions, including possible campaign/layout requirements)
            state.has_all([mission.beat_item() for mission in required_missions], player) and
            # Count requirement (beat X missions of the parent campaign)
            self.option_unlock_count <= sum(state.has(mission.beat_item(), player) for layout in self.parent_campaign.layouts for mission in layout.missions if not mission.option_empty) and
            # Campaign count requirement (beat X sets of required missions of previous-order campaigns)
            campaign_unlock_count <= sum(state.has_all([mission.beat_item() for mission in campaign.required], player) for campaign in self.parent_campaign.prev) and
            # Layout count requirement (beat X sets of exit missions of previous-order layouts)
            layout_unlock_count <= sum(state.has_all([mission.beat_item() for mission in layout.exits], player) for layout in self.parent_layout.prev)
        )

    def make_connections(self, world: World, used_names: Dict[str, int]):
        unlocking_rule = self.connect_rule(world.player)
        # Individually connect to previous missions
        for mission in self.prev:
            connect(world, used_names, mission.mission.mission_name, self.mission.mission_name,
                    lambda state, beat_rule=mission.beat_rule(world.player): beat_rule(state) and unlocking_rule(state))
        # If there are no previous missions, connect to Menu instead
        # TODO this means every layout entrance connects to menu, is that good enough?
        # An alternative would be picking any guaranteed required mission, if any exist
        if len(self.prev) == 0:
            connect(world, used_names, "Menu", self.mission.mission_name, unlocking_rule)
    
    def get_slot_requirements(self) -> MissionRequirements:
        if self.option_empty:
            return MissionRequirements.empty()
        remote_missions = {mission.mission.id for mission in self.unlock_missions}
        campaign_sets = []
        campaign_count = 0
        if self.is_campaign_entrance():
            # This mission is its parent campaign's entrance and should copy the campaign's entrance requirements
            campaign_sets = self.parent_campaign.get_prev_id_sets()
            campaign_count = self.parent_campaign.option_unlock_count
            remote_missions.update(mission.mission.id for mission in self.parent_campaign.unlock_missions)
        layout_sets = []
        layout_count = 0
        if self.option_entrance:
            # This mission is its parent layout's entrance and should copy the layout's entrance requirements
            layout_sets = self.parent_layout.get_prev_id_sets()
            layout_count = self.parent_layout.option_unlock_count
            remote_missions.update(mission.mission.id for mission in self.parent_layout.unlock_missions)
        return MissionRequirements(
            {mission.mission.id for mission in self.prev}, # Beat any of these
            remote_missions, # Beat all of these
            self.parent_campaign.option_name, # Parent campaign for lookup for the following
            self.option_unlock_count, # Beat this many in the campaign
            campaign_sets, # Parent campaign's previous campaigns' required missions
            campaign_count, # Beat this many sets from the above list
            layout_sets, # Parent layout's previous layouts' exit missions
            layout_count # Beat this many sets from the above list
        )

class MissionRequirements(NamedTuple):
    prev_missions: Set[int] # Beat any of these
    unlocking_missions: Set[int] # Beat all of these
    parent_campaign: str # Parent campaign for lookup for the following
    unlocking_count: int # Beat this many in the campaign
    campaign_required: List[Set[int]] # Parent campaign's previous campaigns' required missions
    campaign_count: int # Beat this many sets from the above list
    layout_required: List[Set[int]] # Parent layout's previous layouts' exit missions
    layout_count: int # Beat this many sets from the above list

    def empty() -> MissionRequirements:
        return MissionRequirements(set(), set(), "", 0, [], 0, [], 0)

# TODO band-aid for ..regions circular import
def create_location(player: int, location_data: LocationData, region: Region,
                    location_cache: List[Location]) -> Location:
    location = Location(player, location_data.name, location_data.code, region)
    location.access_rule = location_data.rule

    if id is None:
        location.event = True
        location.locked = True

    location_cache.append(location)

    return location


def create_region(world: World, locations_per_region: Dict[str, List[LocationData]],
                  location_cache: List[Location], name: str) -> Region:
    region = Region(name, world.player, world.multiworld)

    if name in locations_per_region:
        for location_data in locations_per_region[name]:
            location = create_location(world.player, location_data, region, location_cache)
            region.locations.append(location)

    return region


def connect(world: World, used_names: Dict[str, int], source: str, target: str,
            rule: Optional[Callable] = None):
    source_region = world.get_region(source)
    target_region = world.get_region(target)

    if target not in used_names:
        used_names[target] = 1
        name = target
    else:
        used_names[target] += 1
        name = target + (' ' * used_names[target])

    connection = Entrance(world.player, name, source_region)

    if rule:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)


def get_locations_per_region(locations: Tuple[LocationData, ...]) -> Dict[str, List[LocationData]]:
    per_region: Dict[str, List[LocationData]] = {}

    for location in locations:
        per_region.setdefault(location.region, []).append(location)

    return per_region
