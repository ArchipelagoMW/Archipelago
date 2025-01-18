from __future__ import annotations
from typing import Dict, Set, Callable, Tuple, List, Any, Type, Optional, Union, TYPE_CHECKING, NamedTuple
from weakref import ref, ReferenceType
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod
import logging

from BaseClasses import Region, Location, CollectionState, Entrance
from ..mission_tables import SC2Mission, SC2Race, lookup_name_to_mission, MissionFlag, lookup_id_to_mission, get_goal_location
from ..item.item_tables import named_layout_key_item_table, named_campaign_key_item_table
from ..item import item_names
from .layout_types import LayoutType
from .entry_rules import EntryRule, SubRuleEntryRule, CountMissionsEntryRule, BeatMissionsEntryRule, SubRuleRuleData, ItemEntryRule
from .mission_pools import SC2MOGenMissionPools, Difficulty, modified_difficulty_thresholds
from .options import GENERIC_KEY_NAME, GENERIC_PROGRESSIVE_KEY_NAME
from .. import rules

if TYPE_CHECKING:
    from ..locations import LocationData
    from .. import SC2World


class MissionOrderNode(ABC):
    parent: Optional[ReferenceType[MissionOrderNode]]
    important_beat_event: bool

    def get_parent(self, address_so_far: str, full_address: str) -> MissionOrderNode:
        if self.parent is None:
            raise ValueError(
                f"Address \"{address_so_far}\" (from \"{full_address}\") could not find a parent object. " +
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

class SC2MissionOrder(MissionOrderNode):
    """
    The top-level data structure for mission orders. Contains helper functions for getting data about generated missions.
    """
    campaigns: List[SC2MOGenCampaign]
    sorted_missions: Dict[Difficulty, List[SC2MOGenMission]]
    fixed_missions: List[SC2MOGenMission]
    items_to_lock: Dict[str, int]
    keys_to_resolve: Dict[MissionOrderNode, List[ItemEntryRule]]
    mission_pools: SC2MOGenMissionPools
    goal_missions: List[SC2MOGenMission]
    max_depth: int

    def __init__(self, world: 'SC2World', mission_pools: SC2MOGenMissionPools, data: Dict[str, Any]):
        self.campaigns = []
        self.sorted_missions = {diff: [] for diff in Difficulty if diff != Difficulty.RELATIVE}
        self.fixed_missions = []
        self.items_to_lock = {}
        self.keys_to_resolve = {}
        self.mission_pools = mission_pools
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
            for campaign in self.campaigns for layout in campaign.layouts
        )

    def get_starting_missions(self) -> List[SC2Mission]:
        """Returns a list containing all the missions that are accessible without beating any other missions."""
        return [
            mission.mission
            for campaign in self.campaigns if campaign.is_always_unlocked()
            for layout in campaign.layouts if layout.is_always_unlocked()
            for mission in layout.missions if mission.is_always_unlocked() and not mission.option_empty
        ]

    def get_completion_condition(self, player: int) -> Callable[[CollectionState], bool]:
        """Returns a lambda to determine whether a state has beaten the mission order's required campaigns."""
        final_locations = [get_goal_location(mission.mission) for mission in self.get_final_missions()]
        return lambda state, final_locations=final_locations: all(state.can_reach_location(loc, player) for loc in final_locations)

    def get_final_mission_ids(self) -> List[int]:
        """Returns the IDs of all missions that are required to beat the mission order."""
        return [mission.mission.id for mission in self.get_final_missions()]

    def get_final_missions(self) -> List[SC2MOGenMission]:
        """Returns the slots of all missions that are required to beat the mission order."""
        return self.goal_missions

    def get_items_to_lock(self) -> Dict[str, int]:
        """Returns a dict of item names and amounts that are required by Item entry rules."""
        return self.items_to_lock

    def get_slot_data(self) -> List[Dict[str, Any]]:
        """Parses the mission order into a format usable for slot data."""
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

    def make_connections(self, world: 'SC2World'):
        names: Dict[str, int] = {}
        for campaign in self.campaigns:
            for layout in campaign.layouts:
                for mission in layout.missions:
                    if not mission.option_empty:
                        mission.make_connections(world, names)

    def fill_depths(self) -> None:
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

        iterations = 0
        while len(next_missions) > 0:
            # Check for accessible missions
            cur_missions: Set[SC2MOGenMission] = {
                mission for mission in next_missions
                if mission.is_unlocked(beaten_missions)
            }
            if len(cur_missions) == 0:
                raise Exception(f"Mission order ran out of accessible missions during iteration {iterations}")
            next_missions.difference_update(cur_missions)
            # Set the depth counters of all currently accessible missions
            new_beaten_missions: Set[SC2MOGenMission] = set()
            while len(cur_missions) > 0:
                mission = cur_missions.pop()
                new_beaten_missions.add(mission)
                # If the beaten missions at depth X unlock a mission, said mission can be beaten at depth X+1 
                mission.min_depth = mission.entry_rule.get_depth(beaten_missions) + 1
                new_next = [
                    next_mission for next_mission in mission.next if not (
                        next_mission in cur_missions
                        or next_mission in beaten_missions
                        or next_mission in new_beaten_missions
                    )
                ]
                next_missions.update(new_next)
            
            # Any campaigns/layouts/missions added after this point will be seen in the next iteration at the earliest
            iterations += 1
            beaten_missions.update(new_beaten_missions)

            # Check for newly accessible campaigns & layouts
            new_campaigns: Set[SC2MOGenCampaign] = set()
            for campaign in next_campaigns:
                if campaign.is_unlocked(beaten_missions):
                    new_campaigns.add(campaign)
            for campaign in new_campaigns:
                accessible_campaigns.add(campaign)
                next_layouts.update(campaign.layouts)
                next_campaigns.remove(campaign)
                for layout in campaign.layouts:
                    layout.entry_rule.min_depth = campaign.entry_rule.get_depth(beaten_missions)
            new_layouts: Set[SC2MOGenLayout] = set()
            for layout in next_layouts:
                if layout.is_unlocked(beaten_missions):
                    new_layouts.add(layout)
            for layout in new_layouts:
                accessible_layouts.add(layout)
                next_missions.update(layout.entrances)
                next_layouts.remove(layout)
                for mission in layout.entrances:
                    mission.entry_rule.min_depth = layout.entry_rule.get_depth(beaten_missions)
    
        # Make sure we didn't miss anything
        assert len(accessible_campaigns) == len(self.campaigns)
        assert len(accessible_layouts) == sum(len(campaign.layouts) for campaign in self.campaigns)
        total_missions = sum(
            len([mission for mission in layout.missions if not mission.option_empty])
            for campaign in self.campaigns for layout in campaign.layouts
        )
        assert len(beaten_missions) == total_missions, f'Can only access {len(beaten_missions)} missions out of {total_missions}'

        # Fill campaign/layout depth values as min/max of their children
        for campaign in self.campaigns:
            for layout in campaign.layouts:
                depths = [mission.min_depth for mission in layout.missions if not mission.option_empty]
                layout.min_depth = min(depths)
                layout.max_depth = max(depths)
            campaign.min_depth = min(layout.min_depth for layout in campaign.layouts)
            campaign.max_depth = max(layout.max_depth for layout in campaign.layouts)
        self.max_depth = max(campaign.max_depth for campaign in self.campaigns)

    
    def resolve_difficulties(self) -> None:
        for campaign in self.campaigns:
            (campaign_sorted, campaign_fixed) = campaign.resolve_difficulties(self.max_depth)
            self.fixed_missions.extend(campaign_fixed)
            for (diff, missions) in campaign_sorted.items():
                self.sorted_missions[diff].extend(missions)
    
    def resolve_unlocks(self):
        rolling_rule_id = 0
        for campaign in self.campaigns:
            entry_rule = {
                "rules": campaign.option_entry_rules,
                "amount": -1
            }
            campaign.entry_rule = self.dict_to_entry_rule(entry_rule, campaign, rolling_rule_id)
            rolling_rule_id += 1
            for layout in campaign.layouts:
                entry_rule = {
                    "rules": layout.option_entry_rules,
                    "amount": -1
                }
                layout.entry_rule = self.dict_to_entry_rule(entry_rule, layout, rolling_rule_id)
                rolling_rule_id += 1
                for mission in layout.missions:
                    entry_rule = {
                        "rules": mission.option_entry_rules,
                        "amount": -1
                    }
                    mission.entry_rule = self.dict_to_entry_rule(entry_rule, mission, rolling_rule_id)
                    rolling_rule_id += 1
                    # Manually make a rule for prev missions
                    if len(mission.prev) > 0:
                        mission.entry_rule.target_amount += 1
                        mission.entry_rule.rules_to_check.append(CountMissionsEntryRule(mission.prev, 1, mission.prev))

    def dict_to_entry_rule(self, data: Dict[str, Any], start_node: MissionOrderNode, rule_id: int = -1) -> EntryRule:
        if "items" in data:
            items: Dict[str, int] = data["items"]
            has_generic_key = False
            for (item, amount) in items.items():
                if item.casefold() == GENERIC_KEY_NAME or item.casefold().startswith(GENERIC_PROGRESSIVE_KEY_NAME):
                    has_generic_key = True
                    continue # Don't try to lock the generic key
                if item in self.items_to_lock:
                    # Lock the greatest required amount of each item
                    self.items_to_lock[item] = max(self.items_to_lock[item], amount)
                else:
                    self.items_to_lock[item] = amount
            rule = ItemEntryRule(items)
            if has_generic_key:
                self.keys_to_resolve.setdefault(start_node, []).append(rule)
            return rule
        if "rules" in data:
            rules = [self.dict_to_entry_rule(subrule, start_node) for subrule in data["rules"]]
            return SubRuleEntryRule(rules, data["amount"], rule_id)
        if "scope" in data:
            objects: List[Tuple[MissionOrderNode, str]] = []
            for address in data["scope"]:
                resolved = self.resolve_address(address, start_node)
                objects.extend((obj, address) for obj in resolved)
            visual_reqs = [obj.get_visual_requirement(start_node) for (obj, _) in objects]
            missions: List[SC2MOGenMission]
            if "amount" in data:
                missions = [mission for (obj, _) in objects for mission in obj.get_missions() if not mission.option_empty]
                if len(missions) == 0:
                    raise ValueError(f"Count rule did not find any missions at scopes: {data['scope']}")
                return CountMissionsEntryRule(missions, data["amount"], visual_reqs)
            missions = []
            for (obj, address) in objects:
                obj.important_beat_event = True
                exits = obj.get_exits()
                if len(exits) == 0:
                    raise ValueError(
                        f"Address \"{address}\" found an unbeatable object. " +
                        "This should mean the address contains \"..\" too often."
                    )
                missions.extend(exits)
            return BeatMissionsEntryRule(missions, visual_reqs)
        raise ValueError(f"Invalid data for entry rule: {data}")

    def resolve_address(self, address: str, start_node: MissionOrderNode) -> List[MissionOrderNode]:
        if address.startswith("../") or address == "..":
            # Relative address, starts from searching object
            cursor = start_node
        else:
            # Absolute address, starts from the top
            cursor = self
        address_so_far = ""
        for term in address.split("/"):
            if len(address_so_far) > 0:
                address_so_far += "/"
            address_so_far += term
            if term == "..":
                cursor = cursor.get_parent(address_so_far, address)
            else:
                result = cursor.search(term)
                if result is None:
                    raise ValueError(f"Address \"{address_so_far}\" (from \"{address}\") tried to find a child for a mission.")
                if len(result) == 0:
                    raise ValueError(f"Address \"{address_so_far}\" (from \"{address}\") could not find a {cursor.child_type_name()}.")
                if len(result) > 1:
                    # Layouts are allowed to end with multiple missions via an index function
                    if type(result[0]) == SC2MOGenMission and address_so_far == address:
                        return result
                    raise ValueError((f"Address \"{address_so_far}\" (from \"{address}\") found more than one {cursor.child_type_name()}."))
                cursor = result[0]
            if cursor == start_node:
                raise ValueError(
                    f"Address \"{address_so_far}\" (from \"{address}\") returned to original object. " + 
                    "This is not allowed to avoid circular requirements."
                )
        return [cursor]

    def fill_missions(
            self, world: 'SC2World', locked_missions: List[str],
            locations: Tuple['LocationData', ...], location_cache: List[Location]
    ) -> None:
        locations_per_region = get_locations_per_region(locations)
        regions: List[Region] = [create_region(world, locations_per_region, location_cache, "Menu")]
        locked_ids = [lookup_name_to_mission[mission].id for mission in locked_missions]
        prefer_easy_missions = world.options.mission_bias.value == world.options.mission_bias.option_easy

        # Resolve slots with set mission names
        for mission_slot in self.fixed_missions:
            mission_id = mission_slot.option_mission_pool.pop()
            # Remove set mission from locked missions
            locked_ids = [locked for locked in locked_ids if locked != mission_id]
            mission = lookup_id_to_mission[mission_id]
            if mission in self.mission_pools.get_used_missions():
                raise ValueError(f"Mission slot at address \"{mission_slot.get_address_to_node()}\" tried to plando an already plando'd mission.")
            self.mission_pools.pull_specific_mission(mission)
            mission_slot.set_mission(world, mission, locations_per_region, location_cache)
            regions.append(mission_slot.region)

        # Shuffle & sort all slots to pick from smallest to biggest pool with tie-breaks by difficulty (lowest to highest), then randomly
        # Additionally sort goals by difficulty (highest to lowest) with random tie-breaks
        sorted_goals: List[SC2MOGenMission] = []
        for difficulty in sorted(self.sorted_missions.keys()):
            world.random.shuffle(self.sorted_missions[difficulty])
            sorted_goals.extend(mission for mission in self.sorted_missions[difficulty] if mission in self.goal_missions)
        all_slots = [slot for diff in sorted(self.sorted_missions.keys()) for slot in self.sorted_missions[diff]]
        # Sort standard slot difficulties from highest to lowest when using hard bias
        if not prefer_easy_missions:
            all_slots.reverse()
        all_slots.sort(key = lambda slot: len(slot.option_mission_pool.intersection(self.mission_pools.master_list)))
        sorted_goals.reverse()

        # Randomly assign locked missions to appropriate difficulties
        slots_for_locked: Dict[int, List[SC2MOGenMission]] = {locked: [] for locked in locked_ids}
        for mission_slot in all_slots:
            allowed_locked = mission_slot.option_mission_pool.intersection(locked_ids)
            for locked in allowed_locked:
                slots_for_locked[locked].append(mission_slot)
        for (locked, allowed_slots) in slots_for_locked.items():
            locked_mission = lookup_id_to_mission[locked]
            allowed_slots = [slot for slot in allowed_slots if slot in all_slots]
            if len(allowed_slots) == 0:
                logging.warning(f"SC2: Locked mission \"{locked_mission.mission_name}\" is not allowed in any remaining spot and will not be placed.")
                continue
            # This inherits the earlier sorting, but is now sorted again by relative difficulty
            # The result is a sorting in order of nearest difficulty (preferring lower), then by smallest pool, then randomly
            allowed_slots.sort(key = lambda slot: abs(slot.option_difficulty - locked_mission.pool + 1))
            # The first slot should be most appropriate
            mission_slot = allowed_slots[0]
            self.mission_pools.pull_specific_mission(locked_mission)
            mission_slot.set_mission(world, locked_mission, locations_per_region, location_cache)
            regions.append(mission_slot.region)
            all_slots.remove(mission_slot)
            if mission_slot in sorted_goals:
                sorted_goals.remove(mission_slot)

        # Pick goal missions first with stricter difficulty matching, and starting with harder goals
        for goal_slot in sorted_goals:
            try:
                mission = self.mission_pools.pull_random_mission(world, goal_slot, prefer_close_difficulty=True)
                goal_slot.set_mission(world, mission, locations_per_region, location_cache)
                regions.append(goal_slot.region)
                all_slots.remove(goal_slot)
            except IndexError:
                raise IndexError(
                    f"Slot at address \"{goal_slot.get_address_to_node()}\" ran out of possible missions to place "
                    f"with {len(all_slots)} empty slots remaining."
                )

        # Pick random missions
        remaining_count = len(all_slots)
        for mission_slot in all_slots:
            try:
                mission = self.mission_pools.pull_random_mission(world, mission_slot, prefer_close_difficulty=not prefer_easy_missions)
                mission_slot.set_mission(world, mission, locations_per_region, location_cache)
                regions.append(mission_slot.region)
                remaining_count -= 1
            except IndexError:
                raise IndexError(
                    f"Slot at address \"{goal_slot.get_address_to_node()}\" ran out of possible missions to place "
                    f"with {remaining_count} empty slots remaining."
                )

        world.multiworld.regions += regions

    def resolve_generic_keys(self) -> None:
        layout_numbered_keys = 1
        campaign_numbered_keys = 1
        progression_tracks: Dict[int, List[Tuple[MissionOrderNode, ItemEntryRule]]] = {}
        for (node, item_rules) in self.keys_to_resolve.items():
            key_name = node.get_key_name()
            # Generic keys in mission slots should always resolve to an existing key
            # Layouts and campaigns may need to be switched for numbered keys
            if isinstance(node, SC2MOGenLayout) and key_name not in named_layout_key_item_table:
                key_name = item_names._TEMPLATE_NUMBERED_LAYOUT_KEY.format(layout_numbered_keys)
                layout_numbered_keys += 1
            elif isinstance(node, SC2MOGenCampaign) and key_name not in named_campaign_key_item_table:
                key_name = item_names._TEMPLATE_NUMBERED_CAMPAIGN_KEY.format(campaign_numbered_keys)
                campaign_numbered_keys += 1

            for item_rule in item_rules:
                # Swap regular generic key names for the node's proper key name
                item_rule.items_to_check = {
                    key_name if item_name.casefold() == GENERIC_KEY_NAME else item_name: amount
                    for (item_name, amount) in item_rule.items_to_check.items()
                }
                # Only lock the key if it was actually placed in this rule
                if key_name in item_rule.items_to_check:
                    self.items_to_lock[key_name] = max(item_rule.items_to_check[key_name], self.items_to_lock.get(key_name, 0))

                # Sort progressive keys by their given track
                for (item_name, amount) in item_rule.items_to_check.items():
                    if item_name.casefold() == GENERIC_PROGRESSIVE_KEY_NAME:
                        progression_tracks.setdefault(amount, []).append((node, item_rule))
                    elif item_name.casefold().startswith(GENERIC_PROGRESSIVE_KEY_NAME):
                        track_string = item_name.split()[-1]
                        try:
                            track = int(track_string)
                            progression_tracks.setdefault(track, []).append((node, item_rule))
                        except ValueError:
                            raise ValueError(
                                f"Progression track \"{track_string}\" for progressive key \"{item_name}: {amount}\" is not a valid number. "
                                "Valid formats are:\n"
                                f"- {GENERIC_PROGRESSIVE_KEY_NAME.title()}: X\n"
                                f"- {GENERIC_PROGRESSIVE_KEY_NAME.title()} X: 1"
                            )
        
        def find_progressive_keys(item_rule: ItemEntryRule, track_to_find: int) -> List[str]:
            return [
                item_name for (item_name, amount) in item_rule.items_to_check.items()
                if (item_name.casefold() == GENERIC_PROGRESSIVE_KEY_NAME and amount == track_to_find) or (
                    item_name.casefold().startswith(GENERIC_PROGRESSIVE_KEY_NAME) and
                    item_name.split()[-1] == str(track_to_find)
                )
            ]

        def replace_progressive_keys(item_rule: ItemEntryRule, track_to_replace: int, new_key_name: str, new_key_amount: int):
            keys_to_replace = find_progressive_keys(item_rule, track_to_replace)
            new_items_to_check: Dict[str, int] = {}
            for (item_name, amount) in item_rule.items_to_check.items():
                if item_name in keys_to_replace:
                    new_items_to_check[new_key_name] = new_key_amount
                else:
                    new_items_to_check[item_name] = amount
            item_rule.items_to_check = new_items_to_check

        # Change progressive keys to be unique for missions and layouts that request it
        want_unique: Dict[MissionOrderNode, List[Tuple[MissionOrderNode, ItemEntryRule]]] = {}
        empty_tracks: List[int] = []
        for track in progression_tracks:
            # Sort keys to change by layout
            new_unique_tracks: Dict[MissionOrderNode, List[Tuple[MissionOrderNode, ItemEntryRule]]] = {}
            for (node, item_rule) in progression_tracks[track]:
                if isinstance(node, SC2MOGenMission):
                    # Unique tracks for layouts take priority over campaigns
                    if node.parent().option_unique_progression_track == track:
                        new_unique_tracks.setdefault(node.parent(), []).append((node, item_rule))
                    elif node.parent().parent().option_unique_progression_track == track:
                        new_unique_tracks.setdefault(node.parent().parent(), []).append((node, item_rule))
                elif isinstance(node, SC2MOGenLayout) and node.parent().option_unique_progression_track == track:
                    new_unique_tracks.setdefault(node.parent(), []).append((node, item_rule))
            # Remove found keys from their original progression track
            for (container_node, rule_list) in new_unique_tracks.items():
                for node_and_rule in rule_list:
                    progression_tracks[track].remove(node_and_rule)
                want_unique.setdefault(container_node, []).extend(rule_list)
            if len(progression_tracks[track]) == 0:
                empty_tracks.append(track)
        for track in empty_tracks:
            progression_tracks.pop(track)
        
        # Make sure all tracks that can't have keys have been taken care of
        invalid_tracks: List[int] = [track for track in progression_tracks if track < 1 or track > len(SC2Mission)]
        if len(invalid_tracks) > 0:
            affected_key_list: Dict[MissionOrderNode, List[str]] = {}
            for track in invalid_tracks:
                for (node, item_rule) in progression_tracks[track]:
                    affected_key_list.setdefault(node, []).extend(
                        f"{key}: {item_rule.items_to_check[key]}" for key in find_progressive_keys(item_rule, track)
                    )
            affected_key_list_string = "\n- " + "\n- ".join(
                f"{node.get_address_to_node()}: {affected_keys}"
                for (node, affected_keys) in affected_key_list.items()
            )
            raise ValueError(
                "Some item rules contain progressive keys with invalid tracks:" +
                affected_key_list_string +
                f"\nPossible solutions are changing the tracks of affected keys to be in the range from 1 to {len(SC2Mission)}, "
                "or changing the unique_progression_track of containing campaigns/layouts to match the invalid tracks."
            )

        # Assign new free progression tracks to nodes in definition order
        next_free = 1
        nodes_to_assign = list(want_unique.keys())
        while len(want_unique) > 0:
            while next_free in progression_tracks:
                next_free += 1
            container_node = nodes_to_assign.pop(0)
            progression_tracks[next_free] = want_unique.pop(container_node)
            # Replace the affected keys in nodes with their correct counterparts
            key_name = f"{GENERIC_PROGRESSIVE_KEY_NAME} {next_free}"
            for (node, item_rule) in progression_tracks[next_free]:
                # It's guaranteed by the sorting above that the container is either a layout or a campaign
                replace_progressive_keys(item_rule, container_node.option_unique_progression_track, key_name, 1)

        # Give progressive keys a more fitting name if there's only one track and they all apply to the same type of node
        progressive_flavor_name: Union[str, None] = None
        if len(progression_tracks) == 1:
            if all(isinstance(node, SC2MOGenLayout) for rule_list in progression_tracks.values() for (node, _) in rule_list):
                progressive_flavor_name = item_names.PROGRESSIVE_QUESTLINE_KEY
            elif all(isinstance(node, SC2MOGenMission) for rule_list in progression_tracks.values() for (node, _) in rule_list):
                progressive_flavor_name = item_names.PROGRESSIVE_MISSION_KEY
        
        for (track, rule_list) in progression_tracks.items():
            key_name = item_names._TEMPLATE_PROGRESSIVE_KEY.format(track) if progressive_flavor_name is None else progressive_flavor_name
            # Determine order in which the rules should unlock
            ordered_item_rules: List[List[ItemEntryRule]] = []
            if not any(isinstance(node, SC2MOGenMission) for (node, _) in rule_list):
                # No rule on this track belongs to a mission, so the rules can be kept in definition order
                ordered_item_rules = [[item_rule] for (_, item_rule) in rule_list]
            else:
                # At least one rule belongs to a mission
                # Sort rules by the depth of their nodes, ties get the same amount of keys
                depth_to_rules: Dict[int, List[ItemEntryRule]] = {}
                for (node, item_rule) in rule_list:
                    depth_to_rules.setdefault(node.get_min_depth(), []).append(item_rule)
                ordered_item_rules = [depth_to_rules[depth] for depth in sorted(depth_to_rules.keys())]
            
            # Assign correct progressive keys to each rule
            for (position, item_rules) in enumerate(ordered_item_rules):
                for item_rule in item_rules:
                    keys_to_replace = [
                        item_name for (item_name, amount) in item_rule.items_to_check.items()
                        if (item_name.casefold() == GENERIC_PROGRESSIVE_KEY_NAME and amount == track) or (
                            item_name.casefold().startswith(GENERIC_PROGRESSIVE_KEY_NAME) and
                            item_name.split()[-1] == str(track)
                        )
                    ]
                    new_items_to_check: Dict[str, int] = {}
                    for (item_name, amount) in item_rule.items_to_check.items():
                        if item_name in keys_to_replace:
                            new_items_to_check[key_name] = position + 1
                        else:
                            new_items_to_check[item_name] = amount
                    item_rule.items_to_check = new_items_to_check
            self.items_to_lock[key_name] = len(ordered_item_rules)

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

    def __init__(self, world: 'SC2World', parent: ReferenceType[SC2MissionOrder], name: str, data: Dict[str, Any]):
        self.parent = parent
        self.important_beat_event = False
        self.option_name = name
        self.option_display_name = data["display_name"]
        self.option_unique_name = data["unique_name"]
        self.option_goal = data["goal"]
        self.option_entry_rules = data["entry_rules"]
        self.option_unique_progression_track = data["unique_progression_track"]
        self.option_min_difficulty = data["min_difficulty"]
        self.option_max_difficulty = data["max_difficulty"]
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

    def is_always_unlocked(self) -> bool:
        return self.entry_rule.is_always_fulfilled()

    def is_unlocked(self, beaten_missions: Set[SC2MOGenMission]) -> bool:
        return self.entry_rule.is_fulfilled(beaten_missions)

    def resolve_difficulties(self, max_depth: int) -> Tuple[Dict[Difficulty, List[SC2MOGenMission]], List[SC2MOGenMission]]:
        sorted_missions: Dict[Difficulty, List[SC2MOGenMission]] = {diff: [] for diff in Difficulty if diff != Difficulty.RELATIVE}
        fixed_missions: List[SC2MOGenMission] = []
        for layout in self.layouts:
            (layout_sorted, layout_fixed) = layout.resolve_difficulties(
                max_depth, self.min_depth, self.max_depth,
                self.option_min_difficulty, self.option_max_difficulty
            )
            fixed_missions.extend(layout_fixed)
            for (diff, missions) in layout_sorted.items():
                sorted_missions[diff].extend(missions)
        return (sorted_missions, fixed_missions)

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
        self.option_min_difficulty = data.pop("min_difficulty")
        self.option_max_difficulty = data.pop("max_difficulty")
        self.missions = []
        self.entrances = []
        self.exits = []

        # Check for positive size now instead of during YAML validation to actively error with default size
        if self.option_size == 0:
            raise ValueError(f"Layout \"{self.option_name}\" has a size of 0.")

        # Build base layout
        self.layout_type: LayoutType = self.option_type(self.option_size)
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

    def is_always_unlocked(self) -> bool:
        return self.entry_rule.is_always_fulfilled()
    
    def is_unlocked(self, beaten_missions: Set[SC2MOGenMission]) -> bool:
        return self.entry_rule.is_fulfilled(beaten_missions)

    def resolve_difficulties(self,
        order_max_depth: int, parent_min_depth: int, parent_max_depth: int,
        parent_min_diff: Difficulty, parent_max_diff: Difficulty
    ) -> Tuple[Dict[Difficulty, List[SC2MOGenMission]], List[SC2MOGenMission]]:
        if self.option_min_difficulty == Difficulty.RELATIVE:
            min_diff = parent_min_diff
            if min_diff == Difficulty.RELATIVE:
                min_depth = 0
            else:
                min_depth = parent_min_depth
        else:
            min_diff = self.option_min_difficulty
            min_depth = self.min_depth
        if self.option_max_difficulty == Difficulty.RELATIVE:
            max_diff = parent_max_diff
            if max_diff == Difficulty.RELATIVE:
                max_depth = order_max_depth
            else:
                max_depth = parent_max_depth
        else:
            max_diff = self.option_max_difficulty
            max_depth = self.max_depth
        depth_range = max_depth - min_depth
        if depth_range == 0:
            # This can happen if layout size is 1 or layout is all entrances
            # Use minimum difficulty in this case
            depth_range = 1
        # If min/max aren't relative, assume the limits are meant to show up
        layout_thresholds = modified_difficulty_thresholds(min_diff, max_diff)
        thresholds = sorted(layout_thresholds.keys())
        sorted_missions: Dict[Difficulty, List[SC2MOGenMission]] = {diff: [] for diff in Difficulty if diff != Difficulty.RELATIVE}
        fixed_missions: List[SC2MOGenMission] = []
        for mission in self.missions:
            if mission.option_empty:
                continue
            if len(mission.option_mission_pool) == 1:
                fixed_missions.append(mission)
                continue
            if mission.option_difficulty == Difficulty.RELATIVE:
                mission_thresh = int((mission.min_depth - min_depth) * 100 / depth_range)
                for i in range(len(thresholds)):
                    if thresholds[i] > mission_thresh:
                        mission.option_difficulty = layout_thresholds[thresholds[i - 1]]
                        break
                    mission.option_difficulty = layout_thresholds[thresholds[-1]]
            sorted_missions[mission.option_difficulty].append(mission)
        return (sorted_missions, fixed_missions)

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
    
    def set_mission(
            self, world: 'SC2World', mission: SC2Mission,
            locations_per_region: Dict[str, List['LocationData']], location_cache: List[Location]
    ):
        self.mission = mission
        self.region = create_region(world, locations_per_region, location_cache,
                                    mission.mission_name, self)

    def is_always_unlocked(self) -> bool:
        return self.entry_rule.is_always_fulfilled()
    
    def is_unlocked(self, beaten_missions: Set[SC2MOGenMission]) -> bool:
        return self.entry_rule.is_fulfilled(beaten_missions)
    
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

    def make_connections(self, world: 'SC2World', used_names: Dict[str, int]):
        player = world.player
        self_rule = self.entry_rule.to_lambda(player)
        # Only layout entrances need to consider campaign & layout prerequisites
        if self.option_entrance:
            campaign_rule = self.parent().parent().entry_rule.to_lambda(player)
            layout_rule = self.parent().entry_rule.to_lambda(player)
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
            [mission.mission.id for mission in self.prev],
            self.entry_rule.to_slot_data(),
            self.option_victory_cache,
        )


@dataclass
class CampaignSlotData:
    name: str
    entry_rule: SubRuleRuleData
    exits: List[int]
    layouts: List[LayoutSlotData]

    @staticmethod
    def legacy(name: str, layouts: List[LayoutSlotData]) -> CampaignSlotData:
        return CampaignSlotData(name, SubRuleRuleData.empty(), [], layouts)


@dataclass
class LayoutSlotData:
    name: str
    entry_rule: SubRuleRuleData
    exits: List[int]
    missions: List[List[MissionSlotData]]

    @staticmethod
    def legacy(name: str, missions: List[List[MissionSlotData]]) -> LayoutSlotData:
        return LayoutSlotData(name, SubRuleRuleData.empty(), [], missions)


@dataclass
class MissionSlotData:
    mission_id: int
    prev_mission_ids: List[int]
    entry_rule: SubRuleRuleData
    victory_cache_size: int = 0

    @staticmethod
    def empty() -> MissionSlotData:
        return MissionSlotData(-1, [], SubRuleRuleData.empty())

    @staticmethod
    def legacy(mission_id: int, prev_mission_ids: List[int], entry_rule: SubRuleRuleData) -> MissionSlotData:
        return MissionSlotData(mission_id, prev_mission_ids, entry_rule)


class MissionEntryRules(NamedTuple):
    mission_rule: SubRuleRuleData
    layout_rule: SubRuleRuleData
    campaign_rule: SubRuleRuleData


def create_location(player: int, location_data: 'LocationData', region: Region,
                    location_cache: List[Location]) -> Location:
    location = Location(player, location_data.name, location_data.code, region)
    location.access_rule = location_data.rule

    location_cache.append(location)
    return location


def create_minimal_logic_location(
    player: int, location_data: 'LocationData', region: Region, location_cache: List[Location], unit_count: int = 0,
) -> Location:
    location = Location(player, location_data.name, location_data.code, region)
    mission = lookup_name_to_mission.get(region.name)
    if mission is None:
        pass
    elif location_data.hard_rule:
        unit_rule = rules.has_race_units(player, unit_count, mission.race)
        location.access_rule = lambda state: unit_rule(state) and location_data.hard_rule(state)
    else:
        location.access_rule = rules.has_race_units(player, unit_count, mission.race)
    location_cache.append(location)
    return location


def create_region(
    world: 'SC2World',
    locations_per_region: Dict[str, List['LocationData']],
    location_cache: List[Location],
    name: str,
    slot: Optional[SC2MOGenMission] = None,
) -> Region:
    region = Region(name, world.player, world.multiworld)

    from ..locations import LocationType
    if slot is None:
        target_victory_cache_locations = 0
    else:
        target_victory_cache_locations = slot.option_victory_cache
    victory_cache_locations = 0

    # If the first mission is a build mission,
    # require a unit everywhere except one location in the easiest category
    mission_needs_unit = False
    unit_given = False
    easiest_category = LocationType.MASTERY
    if slot is not None and slot.min_depth == 0:
        mission = lookup_name_to_mission.get(region.name)
        if mission is not None and MissionFlag.NoBuild not in mission.flags:
            mission_needs_unit = True
            for location_data in locations_per_region.get(name, ()):
                if location_data.type == LocationType.VICTORY:
                    pass
                elif location_data.type < easiest_category:
                    easiest_category = location_data.type
            if easiest_category >= LocationType.CHALLENGE:
                easiest_category = LocationType.VICTORY

    for location_data in locations_per_region.get(name, ()):
        if location_data.type == LocationType.VICTORY_CACHE:
            if victory_cache_locations >= target_victory_cache_locations:
                continue
            victory_cache_locations += 1
        if world.options.required_tactics.value == world.options.required_tactics.option_any_units:
            if mission_needs_unit and not unit_given and location_data.type == easiest_category:

                location = create_minimal_logic_location(world.player, location_data, region, location_cache, 0)
                unit_given = True
            else:
                location = create_minimal_logic_location(world.player, location_data, region, location_cache, min(slot.min_depth, 5) + mission_needs_unit)
        else:
            location = create_location(world.player, location_data, region, location_cache)
        region.locations.append(location)

    return region


def connect(world: 'SC2World', used_names: Dict[str, int], source: str, target: str,
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
