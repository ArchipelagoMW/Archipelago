"""
Contains the data structures that make up a mission order.
Data in these structures is validated in .options.py and manipulated by .generation.py.
"""

from __future__ import annotations
from typing import Dict, Set, Callable, List, Any, Type, Optional, Union, TYPE_CHECKING
from weakref import ref, ReferenceType
from dataclasses import asdict
from abc import ABC, abstractmethod
import logging

from BaseClasses import Region, CollectionState
from ..mission_tables import SC2Mission
from ..item import item_names
from .layout_types import LayoutType
from .entry_rules import SubRuleEntryRule, ItemEntryRule
from .mission_pools import Difficulty
from .slot_data import CampaignSlotData, LayoutSlotData, MissionSlotData

if TYPE_CHECKING:
    from .. import SC2World

class MissionOrderNode(ABC):
    parent: Optional[ReferenceType[MissionOrderNode]]
    important_beat_event: bool

    def get_parent(self, address_so_far: str, full_address: str) -> MissionOrderNode:
        if self.parent is None:
            raise ValueError(
                f"Address \"{address_so_far}\" (from \"{full_address}\") could not find a parent object. "
                "This should mean the address contains \"..\" too often."
            )
        return self.parent()

    @abstractmethod
    def search(self, term: str) -> Union[List[MissionOrderNode], None]:
        raise NotImplementedError

    @abstractmethod
    def child_type_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_missions(self) -> List[SC2MOGenMission]:
        raise NotImplementedError
    
    @abstractmethod
    def get_exits(self) -> List[SC2MOGenMission]:
        raise NotImplementedError

    @abstractmethod
    def get_visual_requirement(self, start_node: MissionOrderNode) -> Union[str, SC2MOGenMission]:
        raise NotImplementedError
    
    @abstractmethod
    def get_key_name(self) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def get_min_depth(self) -> int:
        raise NotImplementedError
    
    @abstractmethod
    def get_address_to_node(self) -> str:
        raise NotImplementedError


class SC2MOGenMissionOrder(MissionOrderNode):
    """
    The top-level data structure for mission orders.
    """
    campaigns: List[SC2MOGenCampaign]
    sorted_missions: Dict[Difficulty, List[SC2MOGenMission]]
    """All mission slots in the mission order sorted by their difficulty, but not their depth."""
    fixed_missions: List[SC2MOGenMission]
    """All mission slots that have a plando'd mission."""
    items_to_lock: Dict[str, int]
    keys_to_resolve: Dict[MissionOrderNode, List[ItemEntryRule]]
    goal_missions: List[SC2MOGenMission]
    max_depth: int

    def __init__(self, world: 'SC2World', data: Dict[str, Any]):
        self.campaigns = []
        self.sorted_missions = {diff: [] for diff in Difficulty if diff != Difficulty.RELATIVE}
        self.fixed_missions = []
        self.items_to_lock = {}
        self.keys_to_resolve = {}
        self.goal_missions = []
        self.parent = None

        for (campaign_name, campaign_data) in data.items():
            campaign = SC2MOGenCampaign(world, ref(self), campaign_name, campaign_data)
            self.campaigns.append(campaign)

        # Check that the mission order actually has a goal
        for campaign in self.campaigns:
            if campaign.option_goal:
                self.goal_missions.extend(mission for mission in campaign.exits)
            for layout in campaign.layouts:
                if layout.option_goal:
                    self.goal_missions.extend(layout.exits)
                for mission in layout.missions:
                    if mission.option_goal and not mission.option_empty:
                        self.goal_missions.append(mission)
        # Remove duplicates
        for goal in self.goal_missions:
            while self.goal_missions.count(goal) > 1:
                self.goal_missions.remove(goal)

        # If not, set the last defined campaign as goal
        if len(self.goal_missions) == 0:
            self.campaigns[-1].option_goal = True
            self.goal_missions.extend(mission for mission in self.campaigns[-1].exits)
        
        # Apply victory cache option wherever the value has not yet been defined; must happen after goal missions are decided
        for mission in self.get_missions():
            if mission.option_victory_cache != -1:
                # Already set
                continue
            if mission in self.goal_missions:
                mission.option_victory_cache = 0
            else:
                mission.option_victory_cache = world.options.victory_cache.value

        # Resolve names
        used_names: Set[str] = set()
        for campaign in self.campaigns:
            names = [campaign.option_name] if len(campaign.option_display_name) == 0 else campaign.option_display_name
            if campaign.option_unique_name:
                names = [name for name in names if name not in used_names]
            campaign.display_name = world.random.choice(names)
            used_names.add(campaign.display_name)
            for layout in campaign.layouts:
                names = [layout.option_name] if len(layout.option_display_name) == 0 else layout.option_display_name
                if layout.option_unique_name:
                    names = [name for name in names if name not in used_names]
                layout.display_name = world.random.choice(names)
                used_names.add(layout.display_name)
    
    def get_slot_data(self) -> List[Dict[str, Any]]:
        # [(campaign data, [(layout data, [[(mission data)]] )] )]
        return [asdict(campaign.get_slot_data()) for campaign in self.campaigns]

    def search(self, term: str) -> Union[List[MissionOrderNode], None]:
        return [
            campaign.layouts[0] if campaign.option_single_layout_campaign else campaign
            for campaign in self.campaigns
            if campaign.option_name.casefold() == term.casefold()
        ]
    
    def child_type_name(self) -> str:
        return "Campaign"
    
    def get_missions(self) -> List[SC2MOGenMission]:
        return [mission for campaign in self.campaigns for layout in campaign.layouts for mission in layout.missions]
    
    def get_exits(self) -> List[SC2MOGenMission]:
        return []
    
    def get_visual_requirement(self, _start_node: MissionOrderNode) -> Union[str, SC2MOGenMission]:
        return "All Missions"

    def get_key_name(self) -> str:
        return super().get_key_name()  # type: ignore

    def get_min_depth(self) -> int:
        return super().get_min_depth()  # type: ignore
    
    def get_address_to_node(self):
        return self.campaigns[0].get_address_to_node() + "/.."


class SC2MOGenCampaign(MissionOrderNode):
    option_name: str # name of this campaign
    option_display_name: List[str]
    option_unique_name: bool
    option_entry_rules: List[Dict[str, Any]]
    option_unique_progression_track: int # progressive keys under this campaign and on this track will be changed to a unique track
    option_goal: bool # whether this campaign is required to beat the game
    # minimum difficulty of this campaign
    # 'relative': based on the median distance of the first mission
    option_min_difficulty: Difficulty
    # maximum difficulty of this campaign
    # 'relative': based on the median distance of the last mission
    option_max_difficulty: Difficulty
    option_single_layout_campaign: bool

    # layouts of this campaign in correct order
    layouts: List[SC2MOGenLayout]
    exits: List[SC2MOGenMission] # missions required to beat this campaign (missions marked "exit" in layouts marked "exit")
    entry_rule: SubRuleEntryRule
    display_name: str

    min_depth: int
    max_depth: int

    def __init__(self, world: 'SC2World', parent: ReferenceType[SC2MOGenMissionOrder], name: str, data: Dict[str, Any]):
        self.parent = parent
        self.important_beat_event = False
        self.option_name = name
        self.option_display_name = data["display_name"]
        self.option_unique_name = data["unique_name"]
        self.option_goal = data["goal"]
        self.option_entry_rules = data["entry_rules"]
        self.option_unique_progression_track = data["unique_progression_track"]
        self.option_min_difficulty = Difficulty(data["min_difficulty"])
        self.option_max_difficulty = Difficulty(data["max_difficulty"])
        self.option_single_layout_campaign = data["single_layout_campaign"]
        self.layouts = []
        self.exits = []

        for (layout_name, layout_data) in data.items():
            if type(layout_data) == dict:
                layout = SC2MOGenLayout(world, ref(self), layout_name, layout_data)
                self.layouts.append(layout)

                # Collect required missions (marked layouts' exits)
                if layout.option_exit:
                    self.exits.extend(layout.exits)
                
        # If no exits are set, use the last defined layout
        if len(self.exits) == 0:
            self.layouts[-1].option_exit = True
            self.exits.extend(self.layouts[-1].exits)
        
    def is_beaten(self, beaten_missions: Set[SC2MOGenMission]) -> bool:
        return beaten_missions.issuperset(self.exits)

    def is_always_unlocked(self, in_region_creation = False) -> bool:
        return self.entry_rule.is_always_fulfilled(in_region_creation)

    def is_unlocked(self, beaten_missions: Set[SC2MOGenMission], in_region_creation = False) -> bool:
        return self.entry_rule.is_fulfilled(beaten_missions, in_region_creation)

    def search(self, term: str) -> Union[List[MissionOrderNode], None]:
        return [
            layout
            for layout in self.layouts
            if layout.option_name.casefold() == term.casefold()
        ]
    
    def child_type_name(self) -> str:
        return "Layout"

    def get_missions(self) -> List[SC2MOGenMission]:
        return [mission for layout in self.layouts for mission in layout.missions]

    def get_exits(self) -> List[SC2MOGenMission]:
        return self.exits
    
    def get_visual_requirement(self, start_node: MissionOrderNode) -> Union[str, SC2MOGenMission]:
        visual_name = self.get_visual_name()
        # Needs special handling for double-parent, which is valid for missions but errors for campaigns
        first_parent = start_node.get_parent("", "")
        if (
            first_parent is self or (
                first_parent.parent is not None and first_parent.get_parent("", "") is self
            )
        ) and visual_name == "":
            return "this campaign"
        return visual_name
    
    def get_visual_name(self) -> str:
        return self.display_name
    
    def get_key_name(self) -> str:
        return item_names._TEMPLATE_NAMED_CAMPAIGN_KEY.format(self.get_visual_name())
    
    def get_min_depth(self) -> int:
        return self.min_depth
    
    def get_address_to_node(self) -> str:
        return f"{self.option_name}"

    def get_slot_data(self) -> CampaignSlotData:
        if self.important_beat_event:
            exits = [slot.mission.id for slot in self.exits]
        else:
            exits = []

        return CampaignSlotData(
            self.get_visual_name(),
            asdict(self.entry_rule.to_slot_data()),
            exits,
            [asdict(layout.get_slot_data()) for layout in self.layouts]
        )


class SC2MOGenLayout(MissionOrderNode):
    option_name: str # name of this layout
    option_display_name: List[str] # visual name of this layout
    option_unique_name: bool
    option_type: Type[LayoutType] # type of this layout
    option_size: int # amount of missions in this layout
    option_goal: bool # whether this layout is required to beat the game
    option_exit: bool # whether this layout is required to beat its parent campaign
    option_mission_pool: List[int] # IDs of valid missions for this layout
    option_missions: List[Dict[str, Any]]

    option_entry_rules: List[Dict[str, Any]]
    option_unique_progression_track: int # progressive keys under this layout and on this track will be changed to a unique track

    # minimum difficulty of this layout
    # 'relative': based on the median distance of the first mission
    option_min_difficulty: Difficulty
    # maximum difficulty of this layout
    # 'relative': based on the median distance of the last mission
    option_max_difficulty: Difficulty

    missions: List[SC2MOGenMission]
    layout_type: LayoutType
    entrances: List[SC2MOGenMission]
    exits: List[SC2MOGenMission]
    entry_rule: SubRuleEntryRule
    display_name: str

    min_depth: int
    max_depth: int

    def __init__(self, world: 'SC2World', parent: ReferenceType[SC2MOGenCampaign], name: str, data: Dict):
        self.parent: ReferenceType[SC2MOGenCampaign] = parent
        self.important_beat_event = False
        self.option_name = name
        self.option_display_name = data.pop("display_name")
        self.option_unique_name = data.pop("unique_name")
        self.option_type = data.pop("type")
        self.option_size = data.pop("size")
        self.option_goal = data.pop("goal")
        self.option_exit = data.pop("exit")
        self.option_mission_pool = data.pop("mission_pool")
        self.option_missions = data.pop("missions")
        self.option_entry_rules = data.pop("entry_rules")
        self.option_unique_progression_track = data.pop("unique_progression_track")
        self.option_min_difficulty = Difficulty(data.pop("min_difficulty"))
        self.option_max_difficulty = Difficulty(data.pop("max_difficulty"))
        self.missions = []
        self.entrances = []
        self.exits = []

        # Check for positive size now instead of during YAML validation to actively error with default size
        if self.option_size == 0:
            raise ValueError(f"Layout \"{self.option_name}\" has a size of 0.")

        # Build base layout
        from . import layout_types
        self.layout_type: LayoutType = getattr(layout_types, self.option_type)(self.option_size)
        unused = self.layout_type.set_options(data)
        if len(unused) > 0:
            logging.warning(f"SC2 ({world.player_name}): Layout \"{self.option_name}\" has unknown options: {list(unused.keys())}")
        mission_factory = lambda: SC2MOGenMission(ref(self), set(self.option_mission_pool))
        self.missions = self.layout_type.make_slots(mission_factory)

        # Update missions with user data
        for mission_data in self.option_missions:
            indices: Set[int] = set()
            index_terms: List[Union[int, str]] = mission_data["index"]
            for term in index_terms:
                result = self.resolve_index_term(term)
                indices.update(result)
            for idx in indices:
                self.missions[idx].update_with_data(mission_data)

        # Let layout respond to user changes
        self.layout_type.final_setup(self.missions)

        for mission in self.missions:
            if mission.option_entrance:
                self.entrances.append(mission)
            if mission.option_exit:
                self.exits.append(mission)
            if mission.option_next is not None:
                mission.next = [self.missions[idx] for term in mission.option_next for idx in sorted(self.resolve_index_term(term))]

        # Set up missions' prev data
        for mission in self.missions:
            for next_mission in mission.next:
                next_mission.prev.append(mission)
        
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
                mission.option_goal = False
                # Empty missions are also not allowed to cause secondary effects via entry rules (eg. create key items)
                mission.option_entry_rules = []
            else:
                all_empty = False
                # Establish the following invariant:
                # A non-empty mission has no prev missions <=> A non-empty mission is an entrance
                # This is mandatory to guarantee the entire layout is accessible via consecutive .nexts
                # Note that the opposite is not enforced for exits to allow fully optional layouts
                if len(mission.prev) == 0:
                    mission.option_entrance = True
                    self.entrances.append(mission)
                elif mission.option_entrance:
                    for prev_mission in mission.prev:
                        prev_mission.next.remove(mission)
                    mission.prev.clear()
        if all_empty:
            raise Exception(f"Layout \"{self.option_name}\" only contains empty mission slots.")

    def is_beaten(self, beaten_missions: Set[SC2MOGenMission]) -> bool:
        return beaten_missions.issuperset(self.exits)

    def is_always_unlocked(self, in_region_creation = False) -> bool:
        return self.entry_rule.is_always_fulfilled(in_region_creation)
    
    def is_unlocked(self, beaten_missions: Set[SC2MOGenMission], in_region_creation = False) -> bool:
        return self.entry_rule.is_fulfilled(beaten_missions, in_region_creation)

    def resolve_index_term(self, term: Union[str, int], *, ignore_out_of_bounds: bool = True, reject_none: bool = True) -> Union[Set[int], None]:
        try:
            result = {int(term)}
        except ValueError:
            if term == "entrances":
                result = {idx for idx in range(len(self.missions)) if self.missions[idx].option_entrance}
            elif term == "exits":
                result = {idx for idx in range(len(self.missions)) if self.missions[idx].option_exit}
            elif term == "all":
                result = {idx for idx in range(len(self.missions))}
            else:
                result = self.layout_type.parse_index(term)
                if result is None and reject_none:
                    raise ValueError(f"Layout \"{self.option_name}\" could not resolve mission index term \"{term}\".")
        if ignore_out_of_bounds:
            result = [index for index in result if index >= 0 and index < len(self.missions)]
        return result

    def get_parent(self, _address_so_far: str, _full_address: str) -> MissionOrderNode:
        if self.parent().option_single_layout_campaign:
            parent = self.parent().parent
        else:
            parent = self.parent
        return parent()

    def search(self, term: str) -> Union[List[MissionOrderNode], None]:
        indices = self.resolve_index_term(term, reject_none=False)
        if indices is None:
            # Let the address parser handle the fail case
            return []
        missions = [self.missions[index] for index in sorted(indices)]
        return missions
    
    def child_type_name(self) -> str:
        return "Mission"

    def get_missions(self) -> List[SC2MOGenMission]:
        return [mission for mission in self.missions]

    def get_exits(self) -> List[SC2MOGenMission]:
        return self.exits
    
    def get_visual_requirement(self, start_node: MissionOrderNode) -> Union[str, SC2MOGenMission]:
        visual_name = self.get_visual_name()
        if start_node.get_parent("", "") is self and visual_name == "":
            return "this questline"
        return visual_name
    
    def get_visual_name(self) -> str:
        return self.display_name
    
    def get_key_name(self) -> str:
        return item_names._TEMPLATE_NAMED_LAYOUT_KEY.format(self.get_visual_name(), self.parent().get_visual_name())
    
    def get_min_depth(self) -> int:
        return self.min_depth
    
    def get_address_to_node(self) -> str:
        campaign = self.parent()
        if campaign.option_single_layout_campaign:
            return f"{self.option_name}"
        return self.parent().get_address_to_node() + f"/{self.option_name}"

    def get_slot_data(self) -> LayoutSlotData:
        mission_slots = [
            [
                asdict(self.missions[idx].get_slot_data() if (idx >= 0 and not self.missions[idx].option_empty) else MissionSlotData.empty())
                for idx in column
            ]
            for column in self.layout_type.get_visual_layout()
        ]
        if self.important_beat_event:
            exits = [slot.mission.id for slot in self.exits]
        else:
            exits = []

        return LayoutSlotData(
            self.get_visual_name(),
            asdict(self.entry_rule.to_slot_data()),
            exits,
            mission_slots
        )


class SC2MOGenMission(MissionOrderNode):
    option_goal: bool  # whether this mission is required to beat the game
    option_entrance: bool  # whether this mission is unlocked when the layout is unlocked
    option_exit: bool  # whether this mission is required to beat its parent layout
    option_empty: bool  # whether this slot contains a mission at all
    option_next: Union[None, List[Union[int, str]]]  # indices of internally connected missions
    option_entry_rules: List[Dict[str, Any]]
    option_difficulty: Difficulty  # difficulty pool this mission pulls from
    option_mission_pool: Set[int]  # Allowed mission IDs for this slot
    option_victory_cache: int  # Number of victory cache locations tied to the mission name

    entry_rule: SubRuleEntryRule
    min_depth: int # Smallest amount of missions to beat before this slot is accessible

    mission: SC2Mission
    region: Region

    next: List[SC2MOGenMission]
    prev: List[SC2MOGenMission]

    def __init__(self, parent: ReferenceType[SC2MOGenLayout], parent_mission_pool: Set[int]):
        self.parent: ReferenceType[SC2MOGenLayout] = parent
        self.important_beat_event = False
        self.option_mission_pool = parent_mission_pool
        self.option_goal = False
        self.option_entrance = False
        self.option_exit = False
        self.option_empty = False
        self.option_next = None
        self.option_entry_rules = []
        self.option_difficulty = Difficulty.RELATIVE
        self.next = []
        self.prev = []
        self.min_depth = -1
        self.option_victory_cache = -1

    def update_with_data(self, data: Dict):
        self.option_goal = data.get("goal", self.option_goal)
        self.option_entrance = data.get("entrance", self.option_entrance)
        self.option_exit = data.get("exit", self.option_exit)
        self.option_empty = data.get("empty", self.option_empty)
        self.option_next = data.get("next", self.option_next)
        self.option_entry_rules = data.get("entry_rules", self.option_entry_rules)
        self.option_difficulty = data.get("difficulty", self.option_difficulty)
        self.option_mission_pool = data.get("mission_pool", self.option_mission_pool)
        self.option_victory_cache = data.get("victory_cache", -1)
    
    def is_always_unlocked(self, in_region_creation = False) -> bool:
        return self.entry_rule.is_always_fulfilled(in_region_creation)
    
    def is_unlocked(self, beaten_missions: Set[SC2MOGenMission], in_region_creation = False) -> bool:
        return self.entry_rule.is_fulfilled(beaten_missions, in_region_creation)
    
    def beat_item(self) -> str:
        return f"Beat {self.mission.mission_name}"
    
    def beat_rule(self, player) -> Callable[[CollectionState], bool]:
        return lambda state: state.has(self.beat_item(), player)

    def search(self, term: str) -> Union[List[MissionOrderNode], None]:
        return None
    
    def child_type_name(self) -> str:
        return ""

    def get_missions(self) -> List[SC2MOGenMission]:
        return [self]

    def get_exits(self) -> List[SC2MOGenMission]:
        return [self]
    
    def get_visual_requirement(self, _start_node: MissionOrderNode) -> Union[str, SC2MOGenMission]:
        return self
    
    def get_key_name(self) -> str:
        return item_names._TEMPLATE_MISSION_KEY.format(self.mission.mission_name)
    
    def get_min_depth(self) -> int:
        return self.min_depth
    
    def get_address_to_node(self) -> str:
        layout = self.parent()
        assert layout is not None
        index = layout.missions.index(self)
        return layout.get_address_to_node() + f"/{index}"

    def get_slot_data(self) -> MissionSlotData:
        return MissionSlotData(
            self.mission.id,
            [mission.mission.id for mission in self.prev],
            self.entry_rule.to_slot_data(),
            self.option_victory_cache,
        )
