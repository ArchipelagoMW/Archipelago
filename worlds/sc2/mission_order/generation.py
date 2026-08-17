"""
Contains the complex data manipulation functions for mission order generation and Archipelago region creation.
Incoming data is validated to match specifications in .options.py.
The functions here are called from ..regions.py.
"""

from typing import Set, Dict, Any, List, Tuple, Union, Optional, Callable, TYPE_CHECKING
import logging

from BaseClasses import Location, Region, Entrance
from ..mission_tables import SC2Mission, MissionFlag, lookup_name_to_mission, lookup_id_to_mission
from ..item.item_tables import named_layout_key_item_table, named_campaign_key_item_table
from ..item import item_names
from .nodes import MissionOrderNode, SC2MOGenMissionOrder, SC2MOGenCampaign, SC2MOGenLayout, SC2MOGenMission
from .entry_rules import EntryRule, SubRuleEntryRule, ItemEntryRule, CountMissionsEntryRule, BeatMissionsEntryRule
from .mission_pools import (
    SC2MOGenMissionPools, Difficulty, modified_difficulty_thresholds, STANDARD_DIFFICULTY_FILL_ORDER
)
from .options import GENERIC_KEY_NAME, GENERIC_PROGRESSIVE_KEY_NAME

if TYPE_CHECKING:
    from ..locations import LocationData
    from .. import SC2World

def resolve_unlocks(mission_order: SC2MOGenMissionOrder):
    """Parses a mission order's entry rule dicts into entry rule objects."""
    rolling_rule_id = 0
    for campaign in mission_order.campaigns:
        entry_rule = {
            "rules": campaign.option_entry_rules,
            "amount": -1
        }
        campaign.entry_rule = dict_to_entry_rule(mission_order, entry_rule, campaign, rolling_rule_id)
        rolling_rule_id += 1
        for layout in campaign.layouts:
            entry_rule = {
                "rules": layout.option_entry_rules,
                "amount": -1
            }
            layout.entry_rule = dict_to_entry_rule(mission_order, entry_rule, layout, rolling_rule_id)
            rolling_rule_id += 1
            for mission in layout.missions:
                entry_rule = {
                    "rules": mission.option_entry_rules,
                    "amount": -1
                }
                mission.entry_rule = dict_to_entry_rule(mission_order, entry_rule, mission, rolling_rule_id)
                rolling_rule_id += 1
                # Manually make a rule for prev missions
                if len(mission.prev) > 0:
                    mission.entry_rule.target_amount += 1
                    mission.entry_rule.rules_to_check.append(CountMissionsEntryRule(mission.prev, 1, mission.prev))


def dict_to_entry_rule(mission_order: SC2MOGenMissionOrder, data: Dict[str, Any], start_node: MissionOrderNode, rule_id: int = -1) -> EntryRule:
    """Tries to create an entry rule object from an entry rule dict. The structure of these dicts is validated in .options.py."""
    if "items" in data:
        items: Dict[str, int] = data["items"]
        has_generic_key = False
        for (item, amount) in items.items():
            if item.casefold() == GENERIC_KEY_NAME or item.casefold().startswith(GENERIC_PROGRESSIVE_KEY_NAME):
                has_generic_key = True
                continue # Don't try to lock the generic key
            if item in mission_order.items_to_lock:
                # Lock the greatest required amount of each item
                mission_order.items_to_lock[item] = max(mission_order.items_to_lock[item], amount)
            else:
                mission_order.items_to_lock[item] = amount
        rule = ItemEntryRule(items)
        if has_generic_key:
            mission_order.keys_to_resolve.setdefault(start_node, []).append(rule)
        return rule
    if "rules" in data:
        rules = [dict_to_entry_rule(mission_order, subrule, start_node) for subrule in data["rules"]]
        return SubRuleEntryRule(rules, data["amount"], rule_id)
    if "scope" in data:
        objects: List[Tuple[MissionOrderNode, str]] = []
        for address in data["scope"]:
            resolved = resolve_address(mission_order, address, start_node)
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
                    f"Address \"{address}\" found an unbeatable object. "
                    "This should mean the address contains \"..\" too often."
                )
            missions.extend(exits)
        return BeatMissionsEntryRule(missions, visual_reqs)
    raise ValueError(f"Invalid data for entry rule: {data}")


def resolve_address(mission_order: SC2MOGenMissionOrder, address: str, start_node: MissionOrderNode) -> List[MissionOrderNode]:
    """Tries to find a node in the mission order by following the given address."""
    if address.startswith("../") or address == "..":
        # Relative address, starts from searching object
        cursor = start_node
    else:
        # Absolute address, starts from the top
        cursor = mission_order
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
                f"Address \"{address_so_far}\" (from \"{address}\") returned to original object. "
                "This is not allowed to avoid circular requirements."
            )
    return [cursor]


########################


def fill_depths(mission_order: SC2MOGenMissionOrder) -> None:
    """
    Flood-fills the mission order by following its entry rules to determine the depth of all nodes.
    This also ensures theoretical total accessibility of all nodes, but this is allowed to be violated by item placement and the accessibility setting.
    """
    accessible_campaigns: Set[SC2MOGenCampaign] = {campaign for campaign in mission_order.campaigns if campaign.is_always_unlocked(in_region_creation=True)}
    next_campaigns: Set[SC2MOGenCampaign] = set(mission_order.campaigns).difference(accessible_campaigns)

    accessible_layouts: Set[SC2MOGenLayout] = {
        layout
        for campaign in accessible_campaigns for layout in campaign.layouts
        if layout.is_always_unlocked(in_region_creation=True)
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
            if mission.is_unlocked(beaten_missions, in_region_creation=True)
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
            if campaign.is_unlocked(beaten_missions, in_region_creation=True):
                new_campaigns.add(campaign)
        for campaign in new_campaigns:
            accessible_campaigns.add(campaign)
            next_layouts.update(campaign.layouts)
            next_campaigns.remove(campaign)
            for layout in campaign.layouts:
                layout.entry_rule.min_depth = campaign.entry_rule.get_depth(beaten_missions)
        new_layouts: Set[SC2MOGenLayout] = set()
        for layout in next_layouts:
            if layout.is_unlocked(beaten_missions, in_region_creation=True):
                new_layouts.add(layout)
        for layout in new_layouts:
            accessible_layouts.add(layout)
            next_missions.update(layout.entrances)
            next_layouts.remove(layout)
            for mission in layout.entrances:
                mission.entry_rule.min_depth = layout.entry_rule.get_depth(beaten_missions)

    # Make sure we didn't miss anything
    assert len(accessible_campaigns) == len(mission_order.campaigns)
    assert len(accessible_layouts) == sum(len(campaign.layouts) for campaign in mission_order.campaigns)
    total_missions = sum(
        len([mission for mission in layout.missions if not mission.option_empty])
        for campaign in mission_order.campaigns for layout in campaign.layouts
    )
    assert len(beaten_missions) == total_missions, f'Can only access {len(beaten_missions)} missions out of {total_missions}'

    # Fill campaign/layout depth values as min/max of their children
    for campaign in mission_order.campaigns:
        for layout in campaign.layouts:
            depths = [mission.min_depth for mission in layout.missions if not mission.option_empty]
            layout.min_depth = min(depths)
            layout.max_depth = max(depths)
        campaign.min_depth = min(layout.min_depth for layout in campaign.layouts)
        campaign.max_depth = max(layout.max_depth for layout in campaign.layouts)
    mission_order.max_depth = max(campaign.max_depth for campaign in mission_order.campaigns)


########################


def resolve_difficulties(mission_order: SC2MOGenMissionOrder) -> None:
    """Determines the concrete difficulty of all mission slots."""
    for campaign in mission_order.campaigns:
        for layout in campaign.layouts:
            if layout.option_min_difficulty == Difficulty.RELATIVE:
                min_diff = campaign.option_min_difficulty
                if min_diff == Difficulty.RELATIVE:
                    min_depth = 0
                else:
                    min_depth = campaign.min_depth
            else:
                min_diff = layout.option_min_difficulty
                min_depth = layout.min_depth
            
            if layout.option_max_difficulty == Difficulty.RELATIVE:
                max_diff = campaign.option_max_difficulty
                if max_diff == Difficulty.RELATIVE:
                    max_depth = mission_order.max_depth
                else:
                    max_depth = campaign.max_depth
            else:
                max_diff = layout.option_max_difficulty
                max_depth = layout.max_depth
            
            depth_range = max_depth - min_depth
            if depth_range == 0:
                # This can happen if layout size is 1 or layout is all entrances
                # Use minimum difficulty in this case
                depth_range = 1
            # If min/max aren't relative, assume the limits are meant to show up
            layout_thresholds = modified_difficulty_thresholds(min_diff, max_diff)
            thresholds = sorted(layout_thresholds.keys())
            
            for mission in layout.missions:
                if mission.option_empty:
                    continue
                if len(mission.option_mission_pool) == 1:
                    mission_order.fixed_missions.append(mission)
                    continue
                if mission.option_difficulty == Difficulty.RELATIVE:
                    mission_thresh = int((mission.min_depth - min_depth) * 100 / depth_range)
                    for i in range(len(thresholds)):
                        if thresholds[i] > mission_thresh:
                            mission.option_difficulty = layout_thresholds[thresholds[i - 1]]
                            break
                        mission.option_difficulty = layout_thresholds[thresholds[-1]]
                mission_order.sorted_missions[mission.option_difficulty].append(mission)


########################


def fill_missions(
        mission_order: SC2MOGenMissionOrder, mission_pools: SC2MOGenMissionPools,
        world: 'SC2World', locked_missions: List[str], locations: Tuple['LocationData', ...], location_cache: List[Location]
) -> None:
    """Places missions in all non-empty mission slots. Also responsible for creating Archipelago regions & locations for placed missions."""
    locations_per_region = get_locations_per_region(locations)
    regions: List[Region] = [create_region(world, locations_per_region, location_cache, "Menu")]
    locked_ids = [lookup_name_to_mission[mission].id for mission in locked_missions]
    prefer_close_difficulty = world.options.difficulty_curve.value == world.options.difficulty_curve.option_standard

    def set_mission_in_slot(slot: SC2MOGenMission, mission: SC2Mission):
        slot.mission = mission
        slot.region = create_region(world, locations_per_region, location_cache,
                                    mission.mission_name, slot)

    # Resolve slots with set mission names
    for mission_slot in mission_order.fixed_missions:
        mission_id = mission_slot.option_mission_pool.pop()
        # Remove set mission from locked missions
        locked_ids = [locked for locked in locked_ids if locked != mission_id]
        mission = lookup_id_to_mission[mission_id]
        if mission in mission_pools.get_used_missions():
            raise ValueError(f"Mission slot at address \"{mission_slot.get_address_to_node()}\" tried to plando an already plando'd mission.")
        mission_pools.pull_specific_mission(mission)
        set_mission_in_slot(mission_slot, mission)
        regions.append(mission_slot.region)

    # Shuffle & sort all slots to pick from smallest to biggest pool with tie-breaks by difficulty (lowest to highest), then randomly
    # Additionally sort goals by difficulty (highest to lowest) with random tie-breaks
    sorted_goals: List[SC2MOGenMission] = []
    for difficulty in sorted(mission_order.sorted_missions.keys()):
        world.random.shuffle(mission_order.sorted_missions[difficulty])
        sorted_goals.extend(mission for mission in mission_order.sorted_missions[difficulty] if mission in mission_order.goal_missions)
    # Sort slots by difficulty, with difficulties sorted by fill order
    # standard curve/close difficulty fills difficulties out->in, uneven fills easy->hard
    if prefer_close_difficulty:
        all_slots = [slot for diff in STANDARD_DIFFICULTY_FILL_ORDER for slot in mission_order.sorted_missions[diff]]
    else:
        all_slots = [slot for diff in sorted(mission_order.sorted_missions.keys()) for slot in mission_order.sorted_missions[diff]]
    # Pick slots with a constrained mission pool first
    all_slots.sort(key = lambda slot: len(slot.option_mission_pool.intersection(mission_pools.master_list)))
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
        mission_pools.pull_specific_mission(locked_mission)
        set_mission_in_slot(mission_slot, locked_mission)
        regions.append(mission_slot.region)
        all_slots.remove(mission_slot)
        if mission_slot in sorted_goals:
            sorted_goals.remove(mission_slot)

    # Pick goal missions first with stricter difficulty matching, and starting with harder goals
    for goal_slot in sorted_goals:
        try:
            mission = mission_pools.pull_random_mission(world, goal_slot, prefer_close_difficulty=True)
            set_mission_in_slot(goal_slot, mission)
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
            mission = mission_pools.pull_random_mission(world, mission_slot, prefer_close_difficulty=prefer_close_difficulty)
            set_mission_in_slot(mission_slot, mission)
            regions.append(mission_slot.region)
            remaining_count -= 1
        except IndexError:
            raise IndexError(
                f"Slot at address \"{mission_slot.get_address_to_node()}\" ran out of possible missions to place "
                f"with {remaining_count} empty slots remaining."
            )

    world.multiworld.regions += regions


def get_locations_per_region(locations: Tuple['LocationData', ...]) -> Dict[str, List['LocationData']]:
    per_region: Dict[str, List['LocationData']] = {}

    for location in locations:
        per_region.setdefault(location.region, []).append(location)

    return per_region


def create_location(player: int, location_data: 'LocationData', region: Region,
                    location_cache: List[Location]) -> Location:
    location = Location(player, location_data.name, location_data.code, region)
    location.access_rule = location_data.rule

    location_cache.append(location)
    return location


def create_minimal_logic_location(
    world: 'SC2World', location_data: 'LocationData', region: Region, location_cache: List[Location], unit_count: int = 0,
) -> Location:
    location = Location(world.player, location_data.name, location_data.code, region)
    mission = lookup_name_to_mission.get(region.name)
    if mission is None:
        pass
    elif location_data.hard_rule:
        assert world.logic
        unit_rule = world.logic.has_race_units(unit_count, mission.race)
        location.access_rule = lambda state: unit_rule(state) and location_data.hard_rule(state)
    else:
        assert world.logic
        location.access_rule = world.logic.has_race_units(unit_count, mission.race)
    location_cache.append(location)
    return location


def create_region(
    world: 'SC2World',
    locations_per_region: Dict[str, List['LocationData']],
    location_cache: List[Location],
    name: str,
    slot: Optional[SC2MOGenMission] = None,
) -> Region:
    MAX_UNIT_REQUIREMENT = 5
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
        assert slot is not None
        if location_data.type == LocationType.VICTORY_CACHE:
            if victory_cache_locations >= target_victory_cache_locations:
                continue
            victory_cache_locations += 1
        if world.options.required_tactics.value == world.options.required_tactics.option_any_units:
            if mission_needs_unit and not unit_given and location_data.type == easiest_category:
                # Ensure there is at least one no-logic location if the first mission is a build mission
                location = create_minimal_logic_location(world, location_data, region, location_cache, 0)
                unit_given = True
            elif location_data.type == LocationType.MASTERY:
                # Mastery locations always require max units regardless of position in the ramp
                location = create_minimal_logic_location(world, location_data, region, location_cache, MAX_UNIT_REQUIREMENT)
            else:
                # Required number of units = mission depth; +1 if it's a starting build mission; +1 if it's a challenge location
                location = create_minimal_logic_location(world, location_data, region, location_cache, min(
                    slot.min_depth + mission_needs_unit + (location_data.type == LocationType.CHALLENGE),
                    MAX_UNIT_REQUIREMENT
                ))
        else:
            location = create_location(world.player, location_data, region, location_cache)
        region.locations.append(location)

    return region


########################


def make_connections(mission_order: SC2MOGenMissionOrder, world: 'SC2World'):
    """Creates Archipelago entrances between missions and creates access rules for the generator from entry rule objects."""
    names: Dict[str, int] = {}
    player = world.player
    for campaign in mission_order.campaigns:
        for layout in campaign.layouts:
            for mission in layout.missions:
                if not mission.option_empty:
                    mission_uses_rule = mission.entry_rule.target_amount > 0
                    mission_rule = mission.entry_rule.to_lambda(player)
                    mandatory_prereq = mission.entry_rule.find_mandatory_mission()
                    # Only layout entrances need to consider campaign & layout prerequisites
                    if mission.option_entrance:
                        campaign_uses_rule = campaign.entry_rule.target_amount > 0
                        campaign_rule = campaign.entry_rule.to_lambda(player)
                        layout_uses_rule = layout.entry_rule.target_amount > 0
                        layout_rule = layout.entry_rule.to_lambda(player)

                        # Any mandatory prerequisite mission is good enough
                        mandatory_prereq = campaign.entry_rule.find_mandatory_mission() if mandatory_prereq is None else mandatory_prereq
                        mandatory_prereq = layout.entry_rule.find_mandatory_mission() if mandatory_prereq is None else mandatory_prereq

                        # Avoid calling obviously unused lambdas
                        if campaign_uses_rule:
                            if layout_uses_rule:
                                if mission_uses_rule:
                                    unlock_rule = lambda state, campaign_rule=campaign_rule, layout_rule=layout_rule, mission_rule=mission_rule: \
                                                         campaign_rule(state) and layout_rule(state) and mission_rule(state)
                                else:
                                    unlock_rule = lambda state, campaign_rule=campaign_rule, layout_rule=layout_rule: \
                                                         campaign_rule(state) and layout_rule(state)
                            else:
                                if mission_uses_rule:
                                    unlock_rule = lambda state, campaign_rule=campaign_rule, mission_rule=mission_rule: \
                                                         campaign_rule(state) and mission_rule(state)
                                else:
                                    unlock_rule = campaign_rule
                        elif layout_uses_rule:
                            if mission_uses_rule:
                                unlock_rule = lambda state, layout_rule=layout_rule, mission_rule=mission_rule: \
                                                     layout_rule(state) and mission_rule(state)
                            else:
                                unlock_rule = layout_rule
                        elif mission_uses_rule:
                            unlock_rule = mission_rule
                        else:
                            unlock_rule = None
                    elif mission_uses_rule:
                        unlock_rule = mission_rule
                    else:
                        unlock_rule = None
                    
                    # Connect to a discovered mandatory mission if possible
                    if mandatory_prereq is not None:
                        connect(world, names, mandatory_prereq.mission.mission_name, mission.mission.mission_name, unlock_rule)
                    else:
                        # If no mission is known to be mandatory, connect to all previous missions instead
                        for prev_mission in mission.prev:
                            connect(world, names, prev_mission.mission.mission_name, mission.mission.mission_name, unlock_rule)
                        # As a last resort connect to Menu
                        if len(mission.prev) == 0:
                            connect(world, names, "Menu", mission.mission.mission_name, unlock_rule)


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


########################


def resolve_generic_keys(mission_order: SC2MOGenMissionOrder) -> None:
    """
    Replaces placeholder keys in Item entry rules with their concrete counterparts.
    Specifically this handles placing named keys into missions and vanilla campaigns/layouts,
    and assigning correct progression tracks to progressive keys.
    """
    layout_numbered_keys = 1
    campaign_numbered_keys = 1
    progression_tracks: Dict[int, List[Tuple[MissionOrderNode, ItemEntryRule]]] = {}
    for (node, item_rules) in mission_order.keys_to_resolve.items():
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
                mission_order.items_to_lock[key_name] = max(item_rule.items_to_check[key_name], mission_order.items_to_lock.get(key_name, 0))

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
        mission_order.items_to_lock[key_name] = len(ordered_item_rules)
