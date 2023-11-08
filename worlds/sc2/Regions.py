from typing import List, Dict, Tuple, Optional, Callable, NamedTuple
import math

from BaseClasses import MultiWorld, Region, Entrance, Location, CollectionState
from .Locations import LocationData
from .Options import get_option_value, MissionOrder, get_enabled_campaigns, campaign_depending_orders, \
    GridTwoStartPositions
from .MissionTables import MissionInfo, mission_orders, vanilla_mission_req_table, \
    MissionPools, SC2Campaign, get_goal_location, SC2Mission, MissionConnection
from .PoolFilter import filter_missions


class SC2MissionSlot(NamedTuple):
    campaign: SC2Campaign
    slot: MissionPools | SC2Mission | None


def create_regions(
    multiworld: MultiWorld, player: int, locations: Tuple[LocationData, ...], location_cache: List[Location]
) -> Tuple[Dict[SC2Campaign, Dict[str, MissionInfo]], int, str]:
    """
    Creates region connections by calling the multiworld's `connect()` methods
    Returns a 3-tuple containing:
    * dict[SC2Campaign, Dict[str, MissionInfo]] mapping a campaign and mission name to its data
    * int The number of missions in the world
    * str The name of the goal location
    """
    mission_order_type: int = get_option_value(multiworld, player, "mission_order")

    if mission_order_type == MissionOrder.option_vanilla:
        return create_vanilla_regions(multiworld, player, locations, location_cache)
    elif mission_order_type == MissionOrder.option_grid:
        return create_grid_regions(multiworld, player, locations, location_cache)
    else:
        return create_structured_regions(multiworld, player, locations, location_cache, mission_order_type)

def create_vanilla_regions(
    multiworld: MultiWorld,
    player: int,
    locations: Tuple[LocationData, ...],
    location_cache: List[Location],
) -> Tuple[Dict[SC2Campaign, Dict[str, MissionInfo]], int, str]:
    locations_per_region = get_locations_per_region(locations)
    regions = [create_region(multiworld, player, locations_per_region, location_cache, "Menu")]

    mission_pools: Dict[MissionPools, List[SC2Mission]] = filter_missions(multiworld, player)
    final_mission = mission_pools[MissionPools.FINAL][0]

    enabled_campaigns = get_enabled_campaigns(multiworld, player)
    names: Dict[str, int] = {}

    # Generating all regions and locations for each enabled campaign
    for campaign in enabled_campaigns:
        for region_name in vanilla_mission_req_table[campaign].keys():
            regions.append(create_region(multiworld, player, locations_per_region, location_cache, region_name))
    multiworld.regions += regions
    vanilla_mission_reqs = {campaign: missions for campaign, missions in vanilla_mission_req_table.items() if campaign in enabled_campaigns}

    if SC2Campaign.WOL in enabled_campaigns:
        connect(multiworld, player, names, 'Menu', 'Liberation Day')
        connect(multiworld, player, names, 'Liberation Day', 'The Outlaws',
                lambda state: state.has("Beat Liberation Day", player))
        connect(multiworld, player, names, 'The Outlaws', 'Zero Hour',
                lambda state: state.has("Beat The Outlaws", player))
        connect(multiworld, player, names, 'Zero Hour', 'Evacuation',
                lambda state: state.has("Beat Zero Hour", player))
        connect(multiworld, player, names, 'Evacuation', 'Outbreak',
                lambda state: state.has("Beat Evacuation", player))
        connect(multiworld, player, names, "Outbreak", "Safe Haven",
                lambda state: state._sc2wol_cleared_missions(multiworld, player, 7) and
                                state.has("Beat Outbreak", player))
        connect(multiworld, player, names, "Outbreak", "Haven's Fall",
                lambda state: state._sc2wol_cleared_missions(multiworld, player, 7) and
                                state.has("Beat Outbreak", player))
        connect(multiworld, player, names, 'Zero Hour', 'Smash and Grab',
                lambda state: state.has("Beat Zero Hour", player))
        connect(multiworld, player, names, 'Smash and Grab', 'The Dig',
                lambda state: state._sc2wol_cleared_missions(multiworld, player, 8) and
                                state.has("Beat Smash and Grab", player))
        connect(multiworld, player, names, 'The Dig', 'The Moebius Factor',
                lambda state: state._sc2wol_cleared_missions(multiworld, player, 11) and
                                state.has("Beat The Dig", player))
        connect(multiworld, player, names, 'The Moebius Factor', 'Supernova',
                lambda state: state._sc2wol_cleared_missions(multiworld, player, 14) and
                                state.has("Beat The Moebius Factor", player))
        connect(multiworld, player, names, 'Supernova', 'Maw of the Void',
                lambda state: state.has("Beat Supernova", player))
        connect(multiworld, player, names, 'Zero Hour', "Devil's Playground",
                lambda state: state._sc2wol_cleared_missions(multiworld, player, 4) and
                                state.has("Beat Zero Hour", player))
        connect(multiworld, player, names, "Devil's Playground", 'Welcome to the Jungle',
                lambda state: state.has("Beat Devil's Playground", player))
        connect(multiworld, player, names, "Welcome to the Jungle", 'Breakout',
                lambda state: state._sc2wol_cleared_missions(multiworld, player, 8) and
                                state.has("Beat Welcome to the Jungle", player))
        connect(multiworld, player, names, "Welcome to the Jungle", 'Ghost of a Chance',
                lambda state: state._sc2wol_cleared_missions(multiworld, player, 8) and
                                state.has("Beat Welcome to the Jungle", player))
        connect(multiworld, player, names, "Zero Hour", 'The Great Train Robbery',
                lambda state: state._sc2wol_cleared_missions(multiworld, player, 6) and
                                state.has("Beat Zero Hour", player))
        connect(multiworld, player, names, 'The Great Train Robbery', 'Cutthroat',
                lambda state: state.has("Beat The Great Train Robbery", player))
        connect(multiworld, player, names, 'Cutthroat', 'Engine of Destruction',
                lambda state: state.has("Beat Cutthroat", player))
        connect(multiworld, player, names, 'Engine of Destruction', 'Media Blitz',
                lambda state: state.has("Beat Engine of Destruction", player))
        connect(multiworld, player, names, 'Media Blitz', 'Piercing the Shroud',
                lambda state: state.has("Beat Media Blitz", player))
        connect(multiworld, player, names, 'Maw of the Void', 'Gates of Hell',
                lambda state: state.has("Beat Maw of the Void", player))
        connect(multiworld, player, names, 'Gates of Hell', 'Belly of the Beast',
                lambda state: state.has("Beat Gates of Hell", player))
        connect(multiworld, player, names, 'Gates of Hell', 'Shatter the Sky',
                lambda state: state.has("Beat Gates of Hell", player))
        connect(multiworld, player, names, 'Gates of Hell', 'All-In',
                lambda state: state.has('Beat Gates of Hell', player) and (
                        state.has('Beat Shatter the Sky', player) or state.has('Beat Belly of the Beast', player)))

    if SC2Campaign.PROPHECY in enabled_campaigns:
        if SC2Campaign.WOL in enabled_campaigns:
            connect(multiworld, player, names, 'The Dig', 'Whispers of Doom',
                    lambda state: state.has("Beat The Dig", player)),
        else:
            vanilla_mission_reqs[SC2Campaign.PROPHECY] = vanilla_mission_reqs[SC2Campaign.PROPHECY].copy()
            vanilla_mission_reqs[SC2Campaign.PROPHECY][SC2Mission.WHISPERS_OF_DOOM.mission_name] = MissionInfo(
                SC2Mission.WHISPERS_OF_DOOM, [], SC2Mission.WHISPERS_OF_DOOM.area)
            connect(multiworld, player, names, 'Menu', 'Whispers of Doom'),
        connect(multiworld, player, names, 'Whispers of Doom', 'A Sinister Turn',
                lambda state: state.has("Beat Whispers of Doom", player))
        connect(multiworld, player, names, 'A Sinister Turn', 'Echoes of the Future',
                lambda state: state.has("Beat A Sinister Turn", player))
        connect(multiworld, player, names, 'Echoes of the Future', 'In Utter Darkness',
                lambda state: state.has("Beat Echoes of the Future", player))

    if SC2Campaign.HOTS in enabled_campaigns:
        connect(multiworld, player, names, 'Menu', 'Lab Rat'),
        connect(multiworld, player, names, 'Lab Rat', 'Back in the Saddle',
                lambda state: state.has("Beat Lab Rat", player)),
        connect(multiworld, player, names, 'Back in the Saddle', 'Rendezvous',
                lambda state: state.has("Beat Back in the Saddle", player)),
        connect(multiworld, player, names, 'Rendezvous', 'Harvest of Screams',
                lambda state: state.has("Beat Rendezvous", player)),
        connect(multiworld, player, names, 'Harvest of Screams', 'Shoot the Messenger',
                lambda state: state.has("Beat Harvest of Screams", player)),
        connect(multiworld, player, names, 'Shoot the Messenger', 'Enemy Within',
                lambda state: state.has("Beat Shoot the Messenger", player)),
        connect(multiworld, player, names, 'Rendezvous', 'Domination',
                lambda state: state.has("Beat Rendezvous", player)),
        connect(multiworld, player, names, 'Domination', 'Fire in the Sky',
                lambda state: state.has("Beat Domination", player)),
        connect(multiworld, player, names, 'Fire in the Sky', 'Old Soldiers',
                lambda state: state.has("Beat Fire in the Sky", player)),
        connect(multiworld, player, names, 'Old Soldiers', 'Waking the Ancient',
                lambda state: state.has("Beat Old Soldiers", player)),
        connect(multiworld, player, names, 'Enemy Within', 'Waking the Ancient',
                lambda state: state.has("Beat Enemy Within", player)),
        connect(multiworld, player, names, 'Waking the Ancient', 'The Crucible',
                lambda state: state.has("Beat Waking the Ancient", player)),
        connect(multiworld, player, names, 'The Crucible', 'Supreme',
                lambda state: state.has("Beat The Crucible", player)),
        connect(multiworld, player, names, 'Supreme', 'Infested',
                lambda state: state.has("Beat Supreme", player) and
                            state.has("Beat Old Soldiers", player) and
                            state.has("Beat Enemy Within", player)),
        connect(multiworld, player, names, 'Infested', 'Hand of Darkness',
                lambda state: state.has("Beat Infested", player)),
        connect(multiworld, player, names, 'Hand of Darkness', 'Phantoms of the Void',
                lambda state: state.has("Beat Hand of Darkness", player)),
        connect(multiworld, player, names, 'Supreme', 'With Friends Like These',
                lambda state: state.has("Beat Supreme", player) and
                            state.has("Beat Old Soldiers", player) and
                            state.has("Beat Enemy Within", player)),
        connect(multiworld, player, names, 'With Friends Like These', 'Conviction',
                lambda state: state.has("Beat With Friends Like These", player)),
        connect(multiworld, player, names, 'Conviction', 'Planetfall',
                lambda state: state.has("Beat Conviction", player) and
                            state.has("Beat Phantoms of the Void", player)),
        connect(multiworld, player, names, 'Planetfall', 'Death From Above',
                lambda state: state.has("Beat Planetfall", player)),
        connect(multiworld, player, names, 'Death From Above', 'The Reckoning',
                lambda state: state.has("Beat Death From Above", player)),

    if SC2Campaign.PROLOGUE in enabled_campaigns:
        connect(multiworld, player, names, "Menu", "Dark Whispers")
        connect(multiworld, player, names, "Dark Whispers", "Ghosts in the Fog",
                lambda state: state.has("Beat Dark Whispers", player))
        connect(multiworld, player, names, "Dark Whispers", "Evil Awoken",
                lambda state: state.has("Beat Ghosts in the Fog", player))

    goal_location = get_goal_location(final_mission)
    assert goal_location, f"Unable to find a goal location for mission {final_mission}"
    setup_final_location(goal_location, location_cache)

    return (vanilla_mission_reqs, final_mission.id, goal_location)


def create_grid_regions(
    multiworld: MultiWorld,
    player: int,
    locations: Tuple[LocationData, ...],
    location_cache: List[Location],
) -> Tuple[Dict[SC2Campaign, Dict[str, MissionInfo]], int, str]:
    locations_per_region = get_locations_per_region(locations)

    mission_pools = filter_missions(multiworld, player)
    final_mission = mission_pools[MissionPools.FINAL][0]

    mission_pool = [mission for mission_pool in mission_pools.values() for mission in mission_pool]

    num_missions = min(len(mission_pool), get_option_value(multiworld, player, "maximum_campaign_size"))
    remove_top_left: bool = get_option_value(multiworld, player, "grid_two_start_positions") == GridTwoStartPositions.option_true

    regions = [create_region(multiworld, player, locations_per_region, location_cache, "Menu")]
    names: Dict[str, int] = {}
    missions: Dict[Tuple[int, int], SC2Mission] = {}

    grid_size_x, grid_size_y, num_corners_to_remove = get_grid_dimensions(num_missions + remove_top_left)
    # pick missions in order along concentric diagonals
    # each diagonal will have the same difficulty
    # this keeps long sides from possibly stealing lower-difficulty missions from future columns
    num_diagonals = grid_size_x + grid_size_y - 1
    diagonal_difficulty = MissionPools.STARTER
    missions_to_add = mission_pools[MissionPools.STARTER]
    for diagonal in range(num_diagonals):
        if diagonal == num_diagonals - 1:
            diagonal_difficulty = MissionPools.FINAL
            grid_coords = (grid_size_x-1, grid_size_y-1)
            missions[grid_coords] = final_mission
            break
        if diagonal == 0 and remove_top_left:
            continue
        diagonal_length = min(diagonal + 1, num_diagonals - diagonal, grid_size_x, grid_size_y)
        if len(missions_to_add) < diagonal_length:
            raise Exception(f"There are not enough {diagonal_difficulty.name} missions to fill the campaign.  Please exclude fewer missions.")
        for i in range(diagonal_length):
            # (0,0) + (0,1)*diagonal + (1,-1)*i + (1,-1)*max(diagonal - grid_size_y + 1, 0)
            grid_coords = (i + max(diagonal - grid_size_y + 1, 0), diagonal - i - max(diagonal - grid_size_y + 1, 0))
            if grid_coords == (grid_size_x - 1, 0) and num_corners_to_remove >= 2:
                pass
            elif grid_coords == (0, grid_size_y - 1) and num_corners_to_remove >= 1:
                pass
            else:
                mission_index = multiworld.random.randint(0, len(missions_to_add) - 1)
                missions[grid_coords] = missions_to_add.pop(mission_index)

        if diagonal_difficulty < MissionPools.HARD:
            diagonal_difficulty = MissionPools(diagonal_difficulty.value + 1)
            missions_to_add.extend(mission_pools[diagonal_difficulty])

    # Generating regions and locations from selected missions
    for x in range(grid_size_x):
        for y in range(grid_size_y):
            if missions.get((x, y)):
                regions.append(create_region(multiworld, player, locations_per_region, location_cache, missions[(x, y)].mission_name))
    multiworld.regions += regions

    # This pattern is horrifying, why are we using the dict as an ordered dict???
    slot_map: Dict[Tuple[int, int], int] = {}
    for index, coords in enumerate(missions):
        slot_map[coords] = index + 1

    mission_req_table: Dict[str, MissionInfo] = {}
    for coords, mission in missions.items():
        prepend_vertical = 0
        if not mission:
            continue
        connections: List[MissionConnection] = []
        if coords == (0, 0) or (remove_top_left and sum(coords) == 1):
            # Connect to the "Menu" starting region
            connect(multiworld, player, names, "Menu", mission.mission_name)
        else:
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                connected_coords = (coords[0] + dx, coords[1] + dy)
                if connected_coords in missions:
                    # connections.append(missions[connected_coords])
                    connections.append(MissionConnection(slot_map[connected_coords]))
                    connect(multiworld, player, names, missions[connected_coords].mission_name, mission.mission_name,
                            make_grid_connect_rule(missions, connected_coords, player),
                            )
        if coords[1] == 1 and not missions.get((coords[0], 0)):
            prepend_vertical = 1
        mission_req_table[mission.mission_name] = MissionInfo(
            mission,
            connections,
            category=f'_{coords[0] + 1}',
            or_requirements=True,
            ui_vertical_padding=prepend_vertical,
        )

    final_mission_id = final_mission.id
    # Changing the completion condition for alternate final missions into an event
    final_location = get_goal_location(final_mission)
    setup_final_location(final_location, location_cache)

    return {SC2Campaign.GLOBAL: mission_req_table}, final_mission_id, final_location


def make_grid_connect_rule(
    missions: Dict[Tuple[int, int], SC2Mission],
    connected_coords: Tuple[int, int],
    player: int
) -> Callable[[CollectionState], bool]:
    return lambda state: state.has(f"Beat {missions[connected_coords].mission_name}", player)


def create_structured_regions(
    multiworld: MultiWorld,
    player: int,
    locations: Tuple[LocationData, ...],
    location_cache: List[Location],
    mission_order_type: int,
) -> Tuple[Dict[SC2Campaign, Dict[str, MissionInfo]], int, str]:
    locations_per_region = get_locations_per_region(locations)

    mission_order = mission_orders[mission_order_type]
    enabled_campaigns = get_enabled_campaigns(multiworld, player)
    shuffle_campaigns = get_option_value(multiworld, player, "shuffle_campaigns")

    mission_pools: Dict[MissionPools, List[SC2Mission]] = filter_missions(multiworld, player)
    final_mission = mission_pools[MissionPools.FINAL][0]

    regions = [create_region(multiworld, player, locations_per_region, location_cache, "Menu")]

    names: Dict[str, int] = {}

    mission_slots: List[SC2MissionSlot] = []
    mission_pool = [mission for mission_pool in mission_pools.values() for mission in mission_pool]

    if mission_order_type in campaign_depending_orders:
        # Do slot removal per campaign
        for campaign in enabled_campaigns:
            campaign_mission_pool = [mission for mission in mission_pool if mission.campaign == campaign]
            campaign_mission_pool_size = len(campaign_mission_pool)

            removals = len(mission_order[campaign]) - campaign_mission_pool_size

            for mission in mission_order[campaign]:
                # Removing extra missions if mission pool is too small
                if 0 < mission.removal_priority <= removals:
                    mission_slots.append(SC2MissionSlot(campaign, None))
                elif mission.type == MissionPools.FINAL:
                    if campaign == final_mission.campaign:
                        # Campaign is elected to be goal
                        mission_slots.append(SC2MissionSlot(campaign, final_mission))
                    else:
                        # Not the goal, find the most difficult mission in the pool and set the difficulty
                        campaign_difficulty = max(mission.pool for mission in campaign_mission_pool)
                        mission_slots.append(SC2MissionSlot(campaign, campaign_difficulty))
                else:
                    mission_slots.append(SC2MissionSlot(campaign, mission.type))
    else:
        order = mission_order[SC2Campaign.GLOBAL]
        # Determining if missions must be removed
        mission_pool_size = sum(len(mission_pool) for mission_pool in mission_pools.values())
        removals = len(order) - mission_pool_size

        # Initial fill out of mission list and marking all-in mission
        for mission in order:
            # Removing extra missions if mission pool is too small
            if 0 < mission.removal_priority <= removals:
                mission_slots.append(SC2MissionSlot(SC2Campaign.GLOBAL, None))
            elif mission.type == MissionPools.FINAL:
                mission_slots.append(SC2MissionSlot(SC2Campaign.GLOBAL, final_mission))
            else:
                mission_slots.append(SC2MissionSlot(SC2Campaign.GLOBAL, mission.type))

    no_build_slots = []
    easy_slots = []
    medium_slots = []
    hard_slots = []
    very_hard_slots = []

    # Search through missions to find slots needed to fill
    for i in range(len(mission_slots)):
        mission_slot = mission_slots[i]
        if mission_slot is None:
            continue
        if isinstance(mission_slot, SC2MissionSlot):
            if mission_slot.slot is None:
                continue
            if mission_slot.slot == MissionPools.STARTER:
                no_build_slots.append(i)
            elif mission_slot.slot == MissionPools.EASY:
                easy_slots.append(i)
            elif mission_slot.slot == MissionPools.MEDIUM:
                medium_slots.append(i)
            elif mission_slot.slot == MissionPools.HARD:
                hard_slots.append(i)
            elif mission_slot.slot == MissionPools.VERY_HARD:
                very_hard_slots.append(i)

    def pick_mission(slot):
        if shuffle_campaigns or mission_order_type not in campaign_depending_orders:
            # Pick a mission from any campaign
            filler = multiworld.random.randint(0, len(missions_to_add) - 1)
            mission = missions_to_add.pop(filler)
            slot_campaign = mission_slots[slot].campaign
            mission_slots[slot] = SC2MissionSlot(slot_campaign, mission)
        else:
            # Pick a mission from required campaign
            slot_campaign = mission_slots[slot].campaign
            campaign_mission_candidates = [mission for mission in missions_to_add if mission.campaign == slot_campaign]
            mission = multiworld.random.choice(campaign_mission_candidates)
            missions_to_add.remove(mission)
            mission_slots[slot] = SC2MissionSlot(slot_campaign, mission)

    # Add no_build missions to the pool and fill in no_build slots
    missions_to_add: List[SC2Mission] = mission_pools[MissionPools.STARTER]
    if len(no_build_slots) > len(missions_to_add):
        raise Exception("There are no valid No-Build missions.  Please exclude fewer missions.")
    for slot in no_build_slots:
        pick_mission(slot)

    # Add easy missions into pool and fill in easy slots
    missions_to_add = missions_to_add + mission_pools[MissionPools.EASY]
    if len(easy_slots) > len(missions_to_add):
        raise Exception("There are not enough Easy missions to fill the campaign.  Please exclude fewer missions.")
    for slot in easy_slots:
        pick_mission(slot)

    # Add medium missions into pool and fill in medium slots
    missions_to_add = missions_to_add + mission_pools[MissionPools.MEDIUM]
    if len(medium_slots) > len(missions_to_add):
        raise Exception("There are not enough Easy and Medium missions to fill the campaign.  Please exclude fewer missions.")
    for slot in medium_slots:
        pick_mission(slot)

    # Add hard missions into pool and fill in hard slots
    missions_to_add = missions_to_add + mission_pools[MissionPools.HARD]
    if len(hard_slots) > len(missions_to_add):
        raise Exception("There are not enough missions to fill the campaign.  Please exclude fewer missions.")
    for slot in hard_slots:
        pick_mission(slot)

    # Add very hard missions into pool and fill in very hard slots
    missions_to_add = missions_to_add + mission_pools[MissionPools.VERY_HARD]
    if len(very_hard_slots) > len(missions_to_add):
        raise Exception("There are not enough missions to fill the campaign.  Please exclude fewer missions.")
    for slot in very_hard_slots:
        pick_mission(slot)

    # Generating regions and locations from selected missions
    for mission_slot in mission_slots:
        if isinstance(mission_slot.slot, SC2Mission):
            regions.append(create_region(multiworld, player, locations_per_region, location_cache, mission_slot.slot.mission_name))
    multiworld.regions += regions

    campaigns: List[SC2Campaign]
    if mission_order_type in campaign_depending_orders:
        campaigns = list(enabled_campaigns)
    else:
        campaigns = [SC2Campaign.GLOBAL]

    mission_req_table: Dict[SC2Campaign, Dict[str, MissionInfo]] = {}
    campaign_mission_slots: Dict[SC2Campaign, List[SC2MissionSlot]] = \
        {
            campaign: [mission_slot for mission_slot in mission_slots if campaign == mission_slot.campaign]
            for campaign in campaigns
        }

    slot_map: Dict[SC2Campaign, List[int]] = dict()

    for campaign in campaigns:
        mission_req_table.update({campaign: dict()})

        # Mapping original mission slots to shifted mission slots when missions are removed
        slot_map[campaign] = []
        slot_offset = 0
        for position, mission in enumerate(campaign_mission_slots[campaign]):
            slot_map[campaign].append(position - slot_offset + 1)
            if mission is None or mission.slot is None:
                slot_offset += 1

    def build_connection_rule(mission_names: List[str], missions_req: int) -> Callable:
        if len(mission_names) > 1:
            return lambda state: state.has_all({f"Beat {name}" for name in mission_names}, player) \
                                 and state._sc2_cleared_missions(multiworld, player, missions_req)
        else:
            return lambda state: state.has(f"Beat {mission_names[0]}", player) \
                                 and state._sc2_cleared_missions(multiworld, player, missions_req)

    for campaign in campaigns:
        # Loop through missions to create requirements table and connect regions
        for i, mission in enumerate(campaign_mission_slots[campaign]):
            if mission is None or mission.slot is None:
                continue
            connections: List[MissionConnection] = []
            all_connections: List[SC2MissionSlot] = []
            connection: MissionConnection
            for connection in mission_order[campaign][i].connect_to:
                if connection.connect_to == -1:
                    continue
                # If mission normally connects to an excluded campaign, connect to menu instead
                if connection.campaign not in campaign_mission_slots:
                    connection.connect_to = -1
                    continue
                while campaign_mission_slots[connection.campaign][connection.connect_to].slot is None:
                    connection.connect_to -= 1
                all_connections.append(campaign_mission_slots[connection.campaign][connection.connect_to])
            for connection in mission_order[campaign][i].connect_to:
                if connection.connect_to == -1:
                    connect(multiworld, player, names, "Menu", mission.slot.mission_name)
                else:
                    required_mission = campaign_mission_slots[connection.campaign][connection.connect_to]
                    if ((required_mission is None or required_mission.slot is None)
                            and not mission_order[campaign][i].completion_critical):  # Drop non-critical null slots
                        continue
                    while required_mission is None or required_mission.slot is None:  # Substituting null slot with prior slot
                        connection.connect_to -= 1
                        required_mission = campaign_mission_slots[connection.campaign][connection.connect_to]
                    required_missions = [required_mission] if mission_order[campaign][i].or_requirements else all_connections
                    if isinstance(required_mission.slot, SC2Mission):
                        required_mission_name = required_mission.slot.mission_name
                        required_missions_names = [mission.slot.mission_name for mission in required_missions]
                        connect(multiworld, player, names, required_mission_name, mission.slot.mission_name,
                                build_connection_rule(required_missions_names, mission_order[campaign][i].number))
                        connections.append(MissionConnection(slot_map[connection.campaign][connection.connect_to], connection.campaign))

            mission_req_table[campaign].update({mission.slot.mission_name: MissionInfo(
                mission.slot, connections, mission_order[campaign][i].category,
                number=mission_order[campaign][i].number,
                completion_critical=mission_order[campaign][i].completion_critical,
                or_requirements=mission_order[campaign][i].or_requirements)})

    final_mission_id = final_mission.id
    # Changing the completion condition for alternate final missions into an event
    final_location = get_goal_location(final_mission)
    setup_final_location(final_location, location_cache)

    return mission_req_table, final_mission_id, final_location


def setup_final_location(final_location, location_cache):
    # Final location should be near the end of the cache
    for i in range(len(location_cache) - 1, -1, -1):
        if location_cache[i].name == final_location:
            location_cache[i].locked = True
            location_cache[i].event = True
            location_cache[i].address = None
            break


def create_location(player: int, location_data: LocationData, region: Region,
                    location_cache: List[Location]) -> Location:
    location = Location(player, location_data.name, location_data.code, region)
    location.access_rule = location_data.rule

    if id is None:
        location.event = True
        location.locked = True

    location_cache.append(location)

    return location


def create_region(multiworld: MultiWorld, player: int, locations_per_region: Dict[str, List[LocationData]],
                  location_cache: List[Location], name: str) -> Region:
    region = Region(name, player, multiworld)

    if name in locations_per_region:
        for location_data in locations_per_region[name]:
            location = create_location(player, location_data, region, location_cache)
            region.locations.append(location)

    return region


def connect(world: MultiWorld, player: int, used_names: Dict[str, int], source: str, target: str,
            rule: Optional[Callable] = None):
    source_region = world.get_region(source, player)
    target_region = world.get_region(target, player)

    if target not in used_names:
        used_names[target] = 1
        name = target
    else:
        used_names[target] += 1
        name = target + (' ' * used_names[target])

    connection = Entrance(player, name, source_region)

    if rule:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)


def get_locations_per_region(locations: Tuple[LocationData, ...]) -> Dict[str, List[LocationData]]:
    per_region: Dict[str, List[LocationData]] = {}

    for location in locations:
        per_region.setdefault(location.region, []).append(location)

    return per_region


def get_factors(number: int) -> Tuple[int, int]:
    """
    Simple factorization into pairs of numbers (x, y) using a sieve method.
    Returns the factorization that is most square, i.e. where x + y is minimized.
    Factor order is such that x <= y.
    """
    assert number > 0
    for divisor in range(math.floor(math.sqrt(number)), 1, -1):
        quotient = number // divisor
        if quotient * divisor == number:
            return divisor, quotient
    return 1, number


def get_grid_dimensions(size: int) -> Tuple[int, int, int]:
    """
    Get the dimensions of a grid mission order from the number of missions, int the format (x, y, error).
    * Error will always be 0, 1, or 2, so the missions can be removed from the corners that aren't the start or end.
    * Dimensions are chosen such that x <= y, as buttons in the UI are wider than they are tall.
    * Dimensions are chosen to be maximally square. That is, x + y + error is minimized.
    * If multiple options of the same rating are possible, the one with the larger error is chosen,
    as it will appear more square. Compare 3x11 to 5x7-2 for an example of this.
    """
    dimension_candidates: List[Tuple[int, int, int]] = [(*get_factors(size + x), x) for x in (2, 1, 0)]
    best_dimension = min(dimension_candidates, key=sum)
    return best_dimension

