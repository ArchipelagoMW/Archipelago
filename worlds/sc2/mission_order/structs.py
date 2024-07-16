from __future__ import annotations
from typing import Dict, Set, Callable, Tuple, List, Any, Type, Optional, Union, TypeVar, TYPE_CHECKING
from collections.abc import Iterable
from enum import IntEnum
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict

from BaseClasses import Region, Location, CollectionState, Entrance
from ..mission_tables import SC2Mission, lookup_name_to_mission, MissionFlag, lookup_id_to_mission
from worlds.AutoWorld import World

if TYPE_CHECKING:
    from ..locations import LocationData

class LayoutType(ABC):
    size: int
    limit: int

    def __init__(self, size: int, limit: int):
        self.size = size
        self.limit = limit

    @abstractmethod
    def make_slots(self, mission_factory: Callable[[], SC2MOGenMission]) -> List[SC2MOGenMission]:
        """Use the provided `Callable` to create a one-dimensional list of mission slots and set up initial settings and connections.

        This should include at least one entrance and exit."""
        return []
    
    @abstractmethod
    def parse_index(self, term: str) -> Union[Set[int], None]:
        """From the given term, determine a list of desired target indices. The term is guaranteed to not be "entrances", "exits", or "all".

        If the term cannot be parsed, either raise an exception or return `None`."""
        return None

    @abstractmethod
    def get_visual_layout(self) -> List[List[int]]:
        """Organize the mission slots into a list of columns from left to right and top to bottom.
        The list should contain indices into the list created by `make_slots`. Intentionally empty spots should contain -1.
        
        The resulting 2D list should be rectangular."""
        pass

class EntryRule(ABC):
    def is_always_fulfilled(self) -> bool:
        return self.is_fulfilled(set())

    @abstractmethod
    def is_fulfilled(self, beaten_missions: Set[SC2MOGenMission]) -> bool:
        """Used during region creation to ensure a beatable mission order."""
        return False
    
    @abstractmethod
    def to_lambda(self, player: int) -> Callable[[CollectionState], bool]:
        """Passed to Archipelago for use during item placement."""
        return lambda _: False
    
    @abstractmethod
    def to_slot_data(self) -> RuleData:
        """Used in the client to determine accessibility while playing and to populate tooltips."""
        return {}

@dataclass
class RuleData(ABC):
    @abstractmethod
    def is_fulfilled(self, beaten_missions: Set[int]) -> bool:
        return False
    
    @abstractmethod
    def tooltip(self, indents: int, missions: Dict[int, SC2Mission]) -> str:
        return ""

class BeatMissionsEntryRule(EntryRule):
    missions_to_beat: Set[SC2MOGenMission]
    visual_reqs: List[Union[str, SC2MOGenMission]]

    def __init__(self, missions_to_beat: Set[SC2MOGenMission], visual_reqs: List[Union[str, SC2MOGenMission]]):
        self.missions_to_beat = missions_to_beat
        self.visual_reqs = visual_reqs
    
    def is_fulfilled(self, beaten_missions: Set[SC2MOGenMission]) -> bool:
        return beaten_missions.issuperset(self.missions_to_beat)
    
    def to_lambda(self, player: int) -> Callable[[CollectionState], bool]:
        return lambda state: state.has_all([mission.beat_item() for mission in self.missions_to_beat], player)
    
    def to_slot_data(self) -> RuleData:
        resolved_reqs: List[Union[str, int]] = [req if type(req) == str else req.mission.id for req in self.visual_reqs]
        mission_ids = {mission.mission.id for mission in self.missions_to_beat}
        return BeatMissionsRuleData(
            mission_ids,
            resolved_reqs
        )

@dataclass
class BeatMissionsRuleData(RuleData):
    mission_ids: Set[int]
    visual_reqs: List[Union[str, int]]

    def is_fulfilled(self, beaten_missions: Set[int]) -> bool:
        return beaten_missions.issuperset(self.mission_ids)
    
    def tooltip(self, indents: int, missions: Dict[int, SC2Mission]) -> str:
        indent = " ".join("" for _ in range(indents))
        if len(self.visual_reqs) == 1:
            req = self.visual_reqs[0]
            return f"Beat {missions[req].mission_name if type(req) == int else req}"
        tooltip = f"Beat all of these:\n{indent}- "
        reqs = [missions[req].mission_name if type(req) == int else req for req in self.visual_reqs]
        tooltip += f"\n{indent}- ".join(req for req in reqs)
        return tooltip
    
class CountMissionsEntryRule(EntryRule):
    missions_to_count: Set[SC2MOGenMission]
    target_amount: int
    visual_reqs: List[Union[str, SC2MOGenMission]]

    def __init__(self, missions_to_count: Set[SC2MOGenMission], target_amount: int, visual_reqs: List[Union[str, SC2MOGenMission]]):
        self.missions_to_count = missions_to_count
        if target_amount == -1 or target_amount > len(missions_to_count):
            self.target_amount = len(missions_to_count)
        else:
            self.target_amount = target_amount
        self.visual_reqs = visual_reqs

    def is_fulfilled(self, beaten_missions: Set[SC2MOGenMission]) -> bool:
        return self.target_amount <= len(beaten_missions.intersection(self.missions_to_count))
    
    def to_lambda(self, player: int) -> Callable[[CollectionState], bool]:
        return lambda state: self.target_amount <= sum(state.has(mission.beat_item(), player) for mission in self.missions_to_count)
    
    def to_slot_data(self) -> RuleData:
        resolved_reqs: List[Union[str, int]] = [req if type(req) == str else req.mission.id for req in self.visual_reqs]
        mission_ids = {mission.mission.id for mission in self.missions_to_count}
        return CountMissionsRuleData(
            mission_ids,
            self.target_amount,
            resolved_reqs
        )

@dataclass
class CountMissionsRuleData(RuleData):
    mission_ids: Set[int]
    amount: int
    visual_reqs: List[Union[str, int]]

    def is_fulfilled(self, beaten_missions: Set[int]) -> bool:
        return self.amount <= len(beaten_missions.intersection(self.mission_ids))
    
    def tooltip(self, indents: int, missions: Dict[int, SC2Mission]) -> str:
        indent = " ".join("" for _ in range(indents))
        if self.amount == len(self.mission_ids):
            amount = "all"
        else:
            amount = str(self.amount)
        if len(self.visual_reqs) == 1:
            req = self.visual_reqs[0]
            req_str = missions[req].mission_name if type(req) == int else req
            if self.amount == 1:
                return f"Beat {req_str}"
            return f"Beat {amount} missions from {req_str}"
        if self.amount == 1:
            tooltip = f"Beat {amount} mission from:\n{indent}- "
        else:
            tooltip = f"Beat {amount} missions from:\n{indent}- "
        reqs = [missions[req].mission_name if type(req) == int else req for req in self.visual_reqs]
        tooltip += f"\n{indent}- ".join(req for req in reqs)
        return tooltip
    
class SubRuleEntryRule(EntryRule):
    rules_to_check: List[EntryRule]
    target_amount: int

    def __init__(self, rules_to_check: List[EntryRule], target_amount: int):
        self.rules_to_check = rules_to_check
        if target_amount == -1 or target_amount > len(rules_to_check):
            self.target_amount = len(rules_to_check)
        else:
            self.target_amount = target_amount

    def is_fulfilled(self, beaten_missions: Set[SC2MOGenMission]) -> bool:
        return self.target_amount <= sum(rule.is_fulfilled(beaten_missions) for rule in self.rules_to_check)
    
    def to_lambda(self, player: int) -> Callable[[CollectionState], bool]:
        sub_lambdas = [rule.to_lambda(player) for rule in self.rules_to_check]
        return lambda state, sub_lambdas=sub_lambdas: self.target_amount <= sum(sub_lambda(state) for sub_lambda in sub_lambdas)
    
    def to_slot_data(self) -> RuleData:
        sub_rules = [rule.to_slot_data() for rule in self.rules_to_check]
        return SubRuleRuleData(
            sub_rules,
            self.target_amount
        )

@dataclass
class SubRuleRuleData(RuleData):
    sub_rules: List[RuleData]
    amount: int

    def is_fulfilled(self, beaten_missions: Set[int]) -> bool:
        return self.amount <= sum(rule.is_fulfilled(beaten_missions) for rule in self.sub_rules)
    
    @staticmethod
    def parse_from_dict(data: Dict[str, Any]) -> SubRuleRuleData:
        amount = data["amount"]
        sub_rules: List[RuleData] = []
        for rule_data in data["sub_rules"]:
            if "sub_rules" in rule_data:
                rule = SubRuleRuleData.parse_from_dict(rule_data)
            elif "amount" in rule_data:
                rule = CountMissionsRuleData(
                    **{field: value for field, value in rule_data.items()}
                )
            else:
                rule = BeatMissionsRuleData(
                    **{field: value for field, value in rule_data.items()}
                )
            sub_rules.append(rule)
        return SubRuleRuleData(
            sub_rules,
            amount
        )
    
    @staticmethod
    def empty() -> SubRuleRuleData:
        return SubRuleRuleData([], 0)
    
    def tooltip(self, indents: int, missions: Dict[int, SC2Mission]) -> str:
        indent = " ".join("" for _ in range(indents))
        if self.amount == len(self.sub_rules):
            if self.amount == 1:
                return self.sub_rules[0].tooltip(indents, missions)
            amount = "all"
        else:
            amount = str(self.amount)
        tooltip = f"Fulfill {amount} of these conditions:\n{indent}- "
        tooltip += f"\n{indent}- ".join(rule.tooltip(indents + 2, missions) for rule in self.sub_rules)
        return tooltip

class Difficulty(IntEnum):
    RELATIVE = 0
    STARTER = 1
    EASY = 2
    MEDIUM = 3
    HARD = 4
    VERY_HARD = 5

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

    def __init__(self) -> None:
        self.master_list = {mission.id for mission in SC2Mission}
        self.difficulty_pools = {
            diff: {mission.id for mission in SC2Mission if mission.pool + 1 == diff}
            for diff in Difficulty if diff != Difficulty.RELATIVE
        }
        self._used_flags = {}
        self._used_missions = set()

    def set_exclusions(self, excluded: List[str], unexcluded: List[str]) -> None:
        """Prevents all the missions that appear in the `excluded` list, but not in the `unexcluded` list,
        from appearing in the mission order."""
        total_exclusions = [lookup_name_to_mission[name] for name in excluded if name not in unexcluded]
        self.master_list.difference_update(total_exclusions)

    def move_mission(self, mission: SC2Mission, old_diff: Difficulty, new_diff: Difficulty) -> None:
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

    def pull_specific_mission(self, mission: SC2Mission) -> None:
        """Marks the given mission as present in the mission order."""
        # Remove the mission from the master list and whichever difficulty pool it is in
        if mission.id in self.master_list:
            self.master_list.remove(mission.id)
            for diff in self.difficulty_pools:
                if mission.id in self.difficulty_pools[diff]:
                    self.difficulty_pools[diff].remove(mission.id)
                    break
        self._add_mission_stats(mission)
    
    def _add_mission_stats(self, mission: SC2Mission) -> None:
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
        
        difficulty_pools: Dict[int, List[int]] = {
            diff: list(pool.intersection(self.difficulty_pools[diff]))
            for diff in Difficulty if diff != Difficulty.RELATIVE
        }

        # Iteratively look down and up around the slot's desired difficulty
        # Either a difficulty with valid missions is found, or an error is raised
        final_pool: List[int] = []
        final_difficulty = Difficulty.RELATIVE
        desired_diff = slot.option_difficulty
        diff_offset = 0
        while len(final_pool) == 0:
            lower_diff = max(desired_diff - diff_offset, 1)
            higher_diff = min(desired_diff + diff_offset, 5)
            final_pool = difficulty_pools[lower_diff]
            if len(final_pool) > 0:
                final_difficulty = Difficulty(lower_diff)
                break
            final_pool = difficulty_pools[higher_diff]
            if len(final_pool) > 0:
                final_difficulty = Difficulty(higher_diff)
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
    sorted_missions: Dict[Difficulty, List[SC2MOGenMission]]
    fixed_missions: Set[SC2MOGenMission]
    mission_pools: SC2MOGenMissionPools
    goal_missions: Set[SC2MOGenMission]
    max_steps: int

    def __init__(self, world: World, data: Dict[str, Any]):
        self.campaigns = []
        self.sorted_missions = {diff: [] for diff in Difficulty if diff != Difficulty.RELATIVE}
        self.fixed_missions = set()
        self.mission_pools = SC2MOGenMissionPools()
        self.goal_missions = set()

        for (campaign_name, campaign_data) in data.items():
            campaign = SC2MOGenCampaign(world, campaign_name, campaign_data)
            self.campaigns.append(campaign)

        # Check that the mission order actually has a goal
        for campaign in self.campaigns:
            if campaign.option_goal:
                self.goal_missions.update(mission for mission in campaign.exits)
            for layout in campaign.layouts:
                if layout.option_goal:
                    self.goal_missions.update(layout.exits)
                for mission in layout.missions:
                    if mission.option_goal:
                        self.goal_missions.add(mission)

        # If not, set the last defined campaign as goal
        if len(self.goal_missions) == 0:
            self.campaigns[-1].option_goal = True
            self.goal_missions.update(mission for mission in self.campaigns[-1].exits)
    
    def get_used_flags(self) -> Dict[MissionFlag, int]:
        """Returns a dictionary of all used flags and their appearance count within the mission order.
        Flags that don't appear in the mission order also don't appear in this dictionary."""
        return self.mission_pools.get_used_flags()
    
    def get_used_missions(self) -> Set[SC2Mission]:
        """Returns a set of all missions used in the mission order."""
        return self.mission_pools.get_used_missions()
    
    def get_starting_missions(self) -> Set[SC2Mission]:
        """Returns a set containing all the missions that are accessible without beating any other missions."""
        return {
            mission.mission
            for campaign in self.campaigns if campaign.is_always_unlocked()
            for layout in campaign.layouts if layout.is_always_unlocked()
            for mission in layout.missions if mission.is_always_unlocked()
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
        return list(self.goal_missions)

    def get_slot_data(self) -> List[Dict[str, Any]]:
        """Parses the mission order into a format usable for slot data."""
        # [(campaign data, [(layout data, [[(mission data)]] )] )]
        return [asdict(campaign.get_slot_data()) for campaign in self.campaigns]

    def make_connections(self, world: World):
        names: Dict[str, int] = {}
        for campaign in self.campaigns:
            for layout in campaign.layouts:
                for mission in layout.missions:
                    mission.make_connections(world, names)

    def fill_min_steps(self) -> None:
        steps = 0

        accessible_campaigns: Set[SC2MOGenCampaign] = {campaign for campaign in self.campaigns if campaign.is_always_unlocked()}
        next_campaigns: Set[SC2MOGenCampaign] = set(self.campaigns).difference(accessible_campaigns)

        accessible_layouts: Set[SC2MOGenLayout] = {
            layout
            for campaign in accessible_campaigns for layout in campaign.layouts
            if layout.is_always_unlocked()
        }
        next_layouts: Set[SC2MOGenLayout] = {layout for campaign in accessible_campaigns for layout in campaign.layouts}.difference(accessible_layouts)

        next_missions: Set[SC2MOGenMission] = {mission for layout in accessible_layouts for mission in layout.entrances}
        beaten_missions: Set[SC2MOGenMission] = set()

        # Sanity check: Can any missions be accessed?
        if len(next_missions) == 0:
            raise Exception("Mission order has no possibly accessible missions")

        while len(next_missions) > 0:
            # Check for accessible missions
            cur_missions: Set[SC2MOGenMission] = {
                mission for mission in next_missions
                if mission.is_unlocked(beaten_missions)
            }
            if len(cur_missions) == 0:
                raise Exception(f"Mission order ran out of accessible missions at depth {steps}")
            next_missions.difference_update(cur_missions)
            # Set the step counters of all currently accessible missions
            while len(cur_missions) > 0:
                mission = cur_missions.pop()
                beaten_missions.add(mission)
                mission.min_steps = steps
                next_missions.update(mission.next.difference(cur_missions, beaten_missions))
            
            # Any campaigns/layouts/missions added after this point will be seen in the next iteration at the earliest
            steps += 1

            # Check for newly accessible campaigns & layouts
            new_campaigns: Set[SC2MOGenCampaign] = set()
            for campaign in next_campaigns:
                if campaign.is_unlocked(beaten_missions):
                    new_campaigns.add(campaign)
            for campaign in new_campaigns:
                accessible_campaigns.add(campaign)
                next_layouts.update(campaign.layouts)
                next_campaigns.remove(campaign)
            new_layouts: Set[SC2MOGenLayout] = set()
            for layout in next_layouts:
                if layout.is_unlocked(beaten_missions):
                    new_layouts.add(layout)
            for layout in new_layouts:
                accessible_layouts.add(layout)
                next_missions.update(layout.entrances)
                next_layouts.remove(layout)
    
        # Make sure we didn't miss anything
        assert len(accessible_campaigns) == len(self.campaigns)
        assert len(accessible_layouts) == sum(len(campaign.layouts) for campaign in self.campaigns)
        assert len(beaten_missions) == sum(len(layout.missions) for campaign in self.campaigns for layout in campaign.layouts)

        self.max_steps = steps - 1

    
    def resolve_difficulties(self) -> None:
        for campaign in self.campaigns:
            (campaign_sorted, campaign_fixed) = campaign.resolve_difficulties(self.max_steps)
            self.fixed_missions.update(campaign_fixed)
            for (diff, missions) in campaign_sorted.items():
                self.sorted_missions[diff].extend(missions)
    
    def resolve_unlocks(self):
        for campaign in self.campaigns:
            entry_rule = {
                "rules": campaign.option_entry_rules,
                "amount": -1
            }
            campaign.entry_rule = self.dict_to_entry_rule(entry_rule, [campaign])
            for layout in campaign.layouts:
                entry_rule = {
                    "rules": layout.option_entry_rules,
                    "amount": -1
                }
                layout.entry_rule = self.dict_to_entry_rule(entry_rule, [campaign, layout])
                for mission in layout.missions:
                    entry_rule = {
                        "rules": mission.option_entry_rules,
                        "amount": -1
                    }
                    mission.entry_rule = self.dict_to_entry_rule(entry_rule, [campaign, layout, mission])
                    # Manually make a rule for prev missions
                    mission.entry_rule.target_amount += 1
                    mission.entry_rule.rules_to_check.append(CountMissionsEntryRule(mission.prev, 1, list(mission.prev)))

    def dict_to_entry_rule(self, data: Dict[str, Any], searchers: Any) -> EntryRule:
        if "rules" in data:
            rules = [self.dict_to_entry_rule(subrule, searchers) for subrule in data["rules"]]
            return SubRuleEntryRule(rules, data["amount"])
        if "scope" in data:
            objects: List[Union[SC2MOGenCampaign, SC2MOGenLayout, SC2MOGenMission]] = []
            for address in data["scope"]:
                resolved = self.resolve_address(address, searchers)
                objects.append(resolved)
            visual_reqs = [obj if type(obj) == SC2MOGenMission else obj.get_visual_name() for obj in objects]
            if "amount" in data:
                missions = {mission for obj in objects for mission in obj.get_missions()}
                return CountMissionsEntryRule(missions, data["amount"], visual_reqs)
            missions = {mission for obj in objects for mission in obj.get_exits()}
            return BeatMissionsEntryRule(missions, visual_reqs)

    def resolve_address(self, address: str, searchers: List[Any]) -> Union[SC2MOGenCampaign, SC2MOGenLayout, SC2MOGenMission]:
        match len(searchers):
            case 1:
                return self.resolve_address_from_campaign(address, searchers[0])
            case 2:
                return self.resolve_address_from_layout(address, searchers[1], searchers[0])
            case 3:
                return self.resolve_address_from_mission(address, searchers[2], searchers[0], searchers[1])
            case _:
                return self.resolve_address_from_campaign(address, None)

    def resolve_address_from_campaign(
        self, address: str, searcher: Union[SC2MOGenCampaign, None]
    ) -> Union[SC2MOGenCampaign, SC2MOGenLayout, SC2MOGenMission]:
        # campaign-level addresses: "campaign", "campaign/layout", "campaign/layout/index", "top layout", "top layout/index"
        parts = address.split('/')
        other_campaign = _find_by_name(parts[0], self.campaigns, searcher, "campaign", address)
        if len(parts) == 1: # "campaign", "top layout" (= same-name campaign)
            return other_campaign
        elif len(parts) == 2:
            if other_campaign.option_single_layout_campaign: # "top layout/index"
                mission = _find_mission_by_index(parts[1], other_campaign.layouts[0].missions, None, address)
                return mission
            else: # "campaign/layout"
                layout = _find_by_name(parts[1], other_campaign.layouts, None, "layout", address)
                return layout
        elif len(parts) == 3: # "campaign/layout/index"
            layout = _find_by_name(parts[1], other_campaign.layouts, None, "layout", address)
            mission = _find_mission_by_index(parts[2], layout.missions, None, address)
            return mission
        else:
            raise ValueError(f"Address {address} contains too many '/'s.")

    def resolve_address_from_layout(
        self, address: str, searcher: SC2MOGenLayout, parent: SC2MOGenCampaign
    ) -> Union[SC2MOGenCampaign, SC2MOGenLayout, SC2MOGenMission]:
        # layout-level addresses: campaign-level addresses + "layout", "layout/index"
        parts = address.split('/')
        other_campaign = _find_by_name(parts[0], self.campaigns, None, "campaign", address, True)
        other_layout = None
        if not other_campaign: # If the first part is not a campaign, assume it wants the local campaign
            other_campaign = parent
            other_layout = _find_by_name(parts[0], parent.layouts, searcher, "layout", address)
        if len(parts) == 1:
            if other_layout: # [parent campaign]/"layout"
                return other_layout
            else: # "campaign", "top layout"
                return other_campaign
        elif len(parts) == 2:
            if other_layout: # [parent campaign]/"layout/index"
                mission = _find_mission_by_index(parts[1], other_layout.missions, None, address)
                return mission
            else:
                if other_campaign.option_single_layout_campaign: # "top layout/index"
                    mission = _find_mission_by_index(parts[1], other_campaign.layouts[0].missions, None, address)
                    return mission
                else: # "campaign/layout"
                    other_layout = _find_by_name(parts[1], other_campaign.layouts, searcher, "layout", address)
                    return other_layout
        elif len(parts) == 3: # "campaign/layout/index"
            if other_layout:
                raise ValueError(f"Address {address} could not find campaign with name \"{parts[0]}\". Please check the spelling of campaign names.")
            other_layout = _find_by_name(parts[1], other_campaign.layouts, searcher, "layout", address)
            mission = _find_mission_by_index(parts[2], other_layout.missions, None, address)
            return mission
        else:
            raise ValueError(f"Address {address} contains too many '/'s.")

    def resolve_address_from_mission(
        self, address: str, searcher: SC2MOGenMission,
        parent_campaign: SC2MOGenCampaign, parent_layout: SC2MOGenLayout
    ) -> Union[SC2MOGenCampaign, SC2MOGenLayout, SC2MOGenMission]:
        # mission-level addresses: layout-level addresses + "index"
        parts = address.split('/')
        other_campaign = _find_by_name(parts[0], self.campaigns, None, "campaign", address, True)
        other_layout = None
        other_mission = None
        if not other_campaign: # If the first part is not a campaign, assume it wants the local campaign
            other_campaign = parent_campaign
            other_layout = _find_by_name(parts[0], parent_campaign.layouts, None, "layout", address, True)
            if not other_layout: # If the first part is not a layout either, assume it wants the local layout
                other_layout = parent_layout
                other_mission = _find_mission_by_index(parts[0], parent_layout.missions, searcher, address)
        if len(parts) == 1:
            if other_mission: # [parent campaign]/[parent layout]/"index"
                return other_mission
            elif other_layout: # [parent campaign]/"layout"
                return other_layout
            elif other_campaign: # "campaign"
                return other_campaign
            else:
                raise ValueError(f"Address {address} could not find campaign or layout with name \"{parts[0]}\". Please check the spelling of campaign and layout names.")
        elif len(parts) == 2:
            if other_mission: # Error: "index/???"
                raise ValueError(f"Address {address} could not find campaign or layout with name \"{parts[0]}\". Please check the spelling of campaign and layout names.")
            elif other_layout: # [parent campaign]/"layout/index"
                other_mission = _find_mission_by_index(parts[1], other_layout.missions, searcher, address)
                return other_mission
            else:
                if other_campaign.option_single_layout_campaign: # "top layout/index"
                    other_mission = _find_mission_by_index(parts[1], other_campaign.layouts[0].missions, None, address)
                    return other_mission
                else: # "campaign/layout"
                    other_layout = _find_by_name(parts[1], other_campaign.layouts, None, "layout", address)
                    return other_layout
        elif len(parts) == 3:
            if other_mission: # Error: "index/???/???"
                raise ValueError(f"Address {address} could not find campaign with name \"{parts[0]}\". Please check the spelling of campaign names.")
            elif other_layout: # Error: "layout/???/???"
                raise ValueError(f"Address {address} could not find campaign with name \"{parts[0]}\". Please check the spelling of campaign names.")
            else: # "campaign/layout/index"
                other_layout = _find_by_name(parts[1], other_campaign.layouts, None, "layout", address)
                other_mission = _find_mission_by_index(parts[2], other_layout.missions, searcher, address)
                return other_mission
        else:
            raise ValueError(f"Address {address} contains too many '/'s.")


    def fill_missions(
            self, world: World, locked_missions: List[str],
            locations: Tuple['LocationData', ...], location_cache: List[Location]
    ):
        locations_per_region = get_locations_per_region(locations)
        regions: List[Region] = [create_region(world, locations_per_region, location_cache, "Menu")]
        locked_ids = [lookup_name_to_mission[mission].id for mission in locked_missions]

        # Resolve slots with set mission names
        for mission_slot in self.fixed_missions:
            mission = lookup_id_to_mission[mission_slot.option_mission_pool.pop()]
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
    option_display_name: List[str]
    option_entry_rules: List[Dict[str, Any]]
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
    exits: Set[SC2MOGenMission] # missions required to beat this campaign (missions marked "exit" in layouts marked "exit")
    entry_rule: SubRuleEntryRule
    display_name: str

    # TODO these two are currently unused
    min_steps: int
    max_steps: int

    def __init__(self, world: World, name: str, data: Dict[str, Any]):
        self.option_name = name
        self.option_display_name = data["display_name"]
        self.option_goal = data["goal"]
        self.option_entry_rules = data["entry_rules"]
        self.option_min_difficulty = data["min_difficulty"]
        self.option_max_difficulty = data["max_difficulty"]
        self.option_single_layout_campaign = data["single_layout_campaign"]
        self.layouts = []
        self.exits = set()
        self.min_steps = 0
        self.max_steps = 0

        for (layout_name, layout_data) in data.items():
            if type(layout_data) == dict:
                layout = SC2MOGenLayout(world, self, layout_name, layout_data)
                self.layouts.append(layout)

                # Collect required missions (marked layouts' exits)
                if layout.option_exit:
                    self.exits.update(layout.exits)
                
        # If no exits are set, use the last defined layout
        if len(self.exits) == 0:
            self.layouts[-1].option_exit = True
            self.exits.update(self.layouts[-1].exits)
        
        # Pick a random display name
        if len(self.option_display_name) == 0:
            self.display_name = self.option_name
        else:
            self.display_name = world.random.choice(self.option_display_name)
    
    def is_beaten(self, beaten_missions: Set[SC2MOGenMission]) -> bool:
        return beaten_missions.issuperset(self.exits)

    def is_always_unlocked(self) -> bool:
        return self.entry_rule.is_always_fulfilled()

    def is_unlocked(self, beaten_missions: Set[SC2MOGenMission]) -> bool:
        return self.entry_rule.is_fulfilled(beaten_missions)

    def resolve_difficulties(self, total_steps: int) -> Tuple[Dict[Difficulty, Set[SC2MOGenMission]], Set[SC2MOGenMission]]:
        sorted_missions: Dict[Difficulty, Set[SC2MOGenMission]] = {diff: set() for diff in Difficulty if diff != Difficulty.RELATIVE}
        fixed_missions: Set[SC2MOGenMission] = set()
        for layout in self.layouts:
            (layout_sorted, layout_fixed) = layout.resolve_difficulties(total_steps, self.option_min_difficulty, self.option_max_difficulty)
            fixed_missions.update(layout_fixed)
            for (diff, missions) in layout_sorted.items():
                sorted_missions[diff].update(missions)
        return (sorted_missions, fixed_missions)

    def get_missions(self) -> Set[SC2MOGenMission]:
        return {mission for layout in self.layouts for mission in layout.missions}    

    def get_exits(self) -> Set[SC2MOGenMission]:
        return self.exits
    
    def get_visual_name(self) -> str:
        return self.display_name

    def get_slot_data(self) -> CampaignSlotData:
        return CampaignSlotData(
            self.get_visual_name(),
            asdict(self.entry_rule.to_slot_data()),
            [asdict(layout.get_slot_data()) for layout in self.layouts]
        )

class SC2MOGenLayout:
    option_name: str # name of this layout
    option_display_name: str # visual name of this layout
    option_type: Type[LayoutType] # type of this layout
    option_size: int # amount of missions in this layout
    option_limit: int # secondary size limit of this layout
    option_goal: bool # whether this layout is required to beat the game
    option_exit: bool # whether this layout is required to beat its parent campaign
    option_mission_pool: List[int] # IDs of valid missions for this layout
    option_missions: List[Dict[str, Any]]

    option_entry_rules: List[Dict[str, Any]]

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
    entry_rule: SubRuleEntryRule

    min_steps: int
    max_steps: int

    def __init__(self, world: World, parent_campaign: SC2MOGenCampaign, name: str, data: Dict):
        self.option_name = name
        self.option_display_name = data["display_name"]
        self.option_type = data["type"]
        self.option_size = data["size"]
        self.option_limit = data["limit"]
        self.option_goal = data["goal"]
        self.option_exit = data["exit"]
        self.option_mission_pool = data["mission_pool"]
        self.option_missions = data["missions"]
        self.option_entry_rules = data["entry_rules"]
        self.option_min_difficulty = data["min_difficulty"]
        self.option_max_difficulty = data["max_difficulty"]
        self.missions = []
        self.entrances = set()
        self.exits = set()
        self.min_steps = 0
        self.max_steps = 0

        # Check for positive size now instead of during YAML validation to actively error with default size
        if self.option_size == 0:
            raise ValueError(f"Layout \"{self.option_name}\" has a size of 0.")

        # Build base layout
        self.layout_type: LayoutType = self.option_type(self.option_size, self.option_limit)
        mission_factory = lambda: SC2MOGenMission(parent_campaign, self, set(self.option_mission_pool))
        self.missions = self.layout_type.make_slots(mission_factory)

        # Update missions with user data
        for mission_data in self.option_missions:
            indices: Set[int] = set()
            index_terms: List[Union[int, str]] = mission_data["index"]
            for term in index_terms:
                if type(term) == int:
                    indices.add(term)
                elif term == "entrances":
                    indices.update(idx for idx in range(len(self.missions)) if self.missions[idx].option_entrance)
                elif term == "exits":
                    indices.update(idx for idx in range(len(self.missions)) if self.missions[idx].option_exit)
                elif term == "all":
                    indices.update(idx for idx in range(len(self.missions)))
                else:
                    result = self.layout_type.parse_index(term)
                    if result is None:
                        raise ValueError(f"Mission index term \"{term}\" did not resolve to any indices.")
                    indices.update(result)
            for idx in indices:
                self.missions[idx].update_with_data(mission_data)

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
                mission.option_goal = False
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
            raise Exception(f"Layout \"{self.option_name}\" only contains empty mission slots.")

        # Pick a random display name
        if len(self.option_display_name) == 0:
            self.display_name = self.option_name
        else:
            self.display_name = world.random.choice(self.option_display_name)
    
    def is_beaten(self, beaten_missions: Set[SC2MOGenMission]) -> bool:
        return beaten_missions.issuperset(self.exits)

    def is_always_unlocked(self) -> bool:
        return self.entry_rule.is_always_fulfilled()
    
    def is_unlocked(self, beaten_missions: Set[SC2MOGenMission]) -> bool:
        return self.entry_rule.is_fulfilled(beaten_missions)

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
            if len(mission.option_mission_pool) == 1:
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

    def get_missions(self) -> Set[SC2MOGenMission]:
        return {mission for mission in self.missions}    

    def get_exits(self) -> Set[SC2MOGenMission]:
        return self.exits
    
    def get_visual_name(self) -> str:
        return self.display_name

    def get_slot_data(self) -> LayoutSlotData:
        mission_slots = [
            [
                asdict(self.missions[idx].get_slot_data()) if idx >= 0 else asdict(MissionSlotData.empty())
                for idx in column
            ]
            for column in self.layout_type.get_visual_layout()
        ]

        return LayoutSlotData(
            self.get_visual_name(),
            asdict(self.entry_rule.to_slot_data()),
            mission_slots
        )
    
class SC2MOGenMission:
    option_goal: bool # whether this mission is required to beat the game
    option_entrance: bool # whether this mission is unlocked when the layout is unlocked
    option_exit: bool # whether this mission is required to beat its parent layout
    option_empty: bool # whether this slot contains a mission at all
    option_next: List[int] # indices of internally connected missions
    option_entry_rules: List[Dict[str, Any]]
    option_difficulty: Difficulty # difficulty pool this mission pulls from
    option_mission_pool: Set[int] # Allowed mission IDs for this slot

    parent_campaign: SC2MOGenCampaign # Parent campaign of this slot
    parent_layout: SC2MOGenLayout # Parent layout of this slot
    entry_rule: SubRuleEntryRule
    min_steps: int # Smallest amount of missions to beat before this slot is accessible

    mission: SC2Mission
    region: Region

    next: Set[SC2MOGenMission]
    prev: Set[SC2MOGenMission]

    def __init__(self, parent_campaign: SC2MOGenCampaign, parent_layout: SC2MOGenLayout, parent_mission_pool: Set[int]):
        self.option_mission_pool = parent_mission_pool
        self.option_goal = False
        self.option_entrance = False
        self.option_exit = False
        self.option_empty = False
        self.option_next = []
        self.option_entry_rules = []
        self.option_difficulty = Difficulty.RELATIVE
        self.parent_campaign = parent_campaign
        self.parent_layout = parent_layout
        self.next = set()
        self.prev = set()

    def update_with_data(self, data: Dict):
        self.option_goal = data.get("goal", self.option_goal)
        self.option_entrance = data.get("entrance", self.option_entrance)
        self.option_exit = data.get("exit", self.option_exit)
        self.option_empty = data.get("empty", self.option_empty)
        self.option_next = data.get("next", self.option_next)
        self.option_entry_rules = data.get("entry_rules", self.option_entry_rules)
        self.option_difficulty = data.get("difficulty", self.option_difficulty)
        self.option_mission_pool = data.get("mission_pool", self.option_mission_pool)
    
    def set_mission(
            self, world: World, mission: SC2Mission,
            locations_per_region: Dict[str, List['LocationData']], location_cache: List[Location]
    ):
        self.mission = mission
        self.region = create_region(world, locations_per_region, location_cache,
                                    mission.mission_name)

    def is_always_unlocked(self) -> bool:
        return self.entry_rule.is_always_fulfilled()
    
    def is_unlocked(self, beaten_missions: Set[SC2MOGenMission]) -> bool:
        return self.entry_rule.is_fulfilled(beaten_missions)
    
    def beat_item(self) -> str:
        return f"Beat {self.mission.mission_name}"
    
    def beat_rule(self, player) -> Callable[[CollectionState], bool]:
        return lambda state: state.has(self.beat_item(), player)

    def get_missions(self) -> Set[SC2MOGenMission]:
        return {self}

    def get_exits(self) -> Set[SC2MOGenMission]:
        return {self}
    
    def make_connections(self, world: World, used_names: Dict[str, int]):
        player = world.player
        self_rule = self.entry_rule.to_lambda(player)
        # Only layout entrances need to consider campaign & layout prerequisites
        if self.option_entrance:
            campaign_rule = self.parent_campaign.entry_rule.to_lambda(player)
            layout_rule = self.parent_layout.entry_rule.to_lambda(player)
            unlock_rule = lambda state: campaign_rule(state) and layout_rule(state) and self_rule(state)
        else:
            unlock_rule = self_rule
        # Individually connect to previous missions
        for mission in self.prev:
            connect(world, used_names, mission.mission.mission_name, self.mission.mission_name,
                    lambda state, unlock_rule=unlock_rule: unlock_rule(state))
        # If there are no previous missions, connect to Menu instead
        if len(self.prev) == 0:
            connect(world, used_names, "Menu", self.mission.mission_name,
                    lambda state, unlock_rule=unlock_rule: unlock_rule(state))
    
    def get_slot_data(self) -> MissionSlotData:
        return MissionSlotData(
            self.mission.id,
            {mission.mission.id for mission in self.prev},
            self.entry_rule.to_slot_data()
        )

@dataclass
class CampaignSlotData:
    name: str
    entry_rule: SubRuleRuleData
    layouts: List[LayoutSlotData]

@dataclass
class LayoutSlotData:
    name: str
    entry_rule: SubRuleRuleData
    missions: List[List[MissionSlotData]]

@dataclass
class MissionSlotData:
    mission_id: int
    prev_mission_ids: Set[int]
    entry_rule: SubRuleRuleData

    @staticmethod
    def empty() -> MissionSlotData:
        return MissionSlotData(-1, set(), SubRuleRuleData.empty())
    
# TODO band-aid for ..regions circular import
def create_location(player: int, location_data: 'LocationData', region: Region,
                    location_cache: List[Location]) -> Location:
    location = Location(player, location_data.name, location_data.code, region)
    location.access_rule = location_data.rule

    if id is None:
        location.event = True
        location.locked = True

    location_cache.append(location)

    return location


def create_region(world: World, locations_per_region: Dict[str, List['LocationData']],
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


def get_locations_per_region(locations: Tuple['LocationData', ...]) -> Dict[str, List['LocationData']]:
    per_region: Dict[str, List['LocationData']] = {}

    for location in locations:
        per_region.setdefault(location.region, []).append(location)

    return per_region
