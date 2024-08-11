from typing import TYPE_CHECKING, List, Dict, Any, Tuple, Optional

from ..locations import LocationData, Location
from ..mission_tables import SC2Mission, SC2Campaign, get_campaign_goal_priority, campaign_final_mission_locations, campaign_alt_final_mission_locations
from ..options import (
    get_option_value, ShuffleNoBuild, RequiredTactics, ExtraLocations, ShuffleCampaigns,
    kerrigan_unit_available, TakeOverAIAllies, MissionOrder, get_excluded_missions, get_enabled_campaigns, static_mission_orders,
    GridTwoStartPositions
)
from .options import CustomMissionOrder
from .structs import SC2MissionOrder, Difficulty
from .mission_pools import SC2MOGenMissionPools

if TYPE_CHECKING:
    from .. import SC2World


def create_mission_order(
    world: 'SC2World', locations: Tuple[LocationData, ...], location_cache: List[Location]
):
    # 'locations' contains both actual game locations and beat event locations for all mission regions
    # When a region (mission) is accessible, all its locations are potentially accessible
    # Accessible in this context always means "its access rule evaluates to True"
    # This includes the beat events, which copy the access rules of the victory locations
    # Beat events being added to logical inventory is auto-magic:
    # Event locations contain an event item of (by default) identical name,
    # which Archipelago's generator will consider part of the logical inventory
    # whenever the event location becomes accessible

    # Set up mission pools
    mission_pools = SC2MOGenMissionPools()
    mission_pools.set_exclusions(get_excluded_missions(world), []) # TODO set unexcluded
    adjust_mission_pools(world, mission_pools)

    mission_order_type = get_option_value(world, "mission_order")
    if mission_order_type == MissionOrder.option_custom:
        mission_order_dict = get_option_value(world, "custom_mission_order")
    else:
        mission_order_option = create_regular_mission_order(world, mission_pools)
        if mission_order_type in static_mission_orders:
            # Static orders get converted early to curate preset content, so it can be used as-is
            mission_order_dict = mission_order_option
        else:
            mission_order_dict = CustomMissionOrder(mission_order_option).value
    mission_order = SC2MissionOrder(world, mission_pools, mission_order_dict)

    # Set up requirements for individual parts of the mission order
    mission_order.resolve_unlocks()
    
    # Ensure total accessibilty and resolve relative difficulties
    mission_order.fill_depths()
    mission_order.resolve_difficulties()
    
    # Build the mission order
    mission_order.fill_missions(world, [], locations, location_cache) # TODO set locked missions
    mission_order.make_connections(world)
    
    return mission_order

def adjust_mission_pools(world: 'SC2World', pools: SC2MOGenMissionPools):
    # Mission pool changes
    mission_order_type = get_option_value(world, "mission_order")
    enabled_campaigns = get_enabled_campaigns(world)
    adv_tactics = get_option_value(world, "required_tactics") != RequiredTactics.option_standard
    shuffle_no_build = get_option_value(world, "shuffle_no_build")
    extra_locations = get_option_value(world, "extra_locations")
    grant_story_tech = get_option_value(world, "grant_story_tech")
    grant_story_levels = get_option_value(world, "grant_story_levels")

    # WoL
    if shuffle_no_build == ShuffleNoBuild.option_false or adv_tactics:
        # Replacing No Build missions with Easy missions
        # WoL
        pools.move_mission(SC2Mission.ZERO_HOUR, Difficulty.EASY, Difficulty.STARTER)
        pools.move_mission(SC2Mission.EVACUATION, Difficulty.EASY, Difficulty.STARTER)
        pools.move_mission(SC2Mission.DEVILS_PLAYGROUND, Difficulty.EASY, Difficulty.STARTER)
        # LotV
        pools.move_mission(SC2Mission.THE_GROWING_SHADOW, Difficulty.EASY, Difficulty.STARTER)
        pools.move_mission(SC2Mission.THE_SPEAR_OF_ADUN, Difficulty.EASY, Difficulty.STARTER)
        if extra_locations == ExtraLocations.option_enabled:
            pools.move_mission(SC2Mission.SKY_SHIELD, Difficulty.EASY, Difficulty.STARTER)
        # Pushing this to Easy
        pools.move_mission(SC2Mission.THE_GREAT_TRAIN_ROBBERY, Difficulty.MEDIUM, Difficulty.EASY)
        if shuffle_no_build == ShuffleNoBuild.option_false:
            # Pushing Outbreak to Normal, as it cannot be placed as the second mission on Build-Only
            pools.move_mission(SC2Mission.OUTBREAK, Difficulty.EASY, Difficulty.MEDIUM)
            # Pushing extra Normal missions to Easy
            pools.move_mission(SC2Mission.ECHOES_OF_THE_FUTURE, Difficulty.MEDIUM, Difficulty.EASY)
            pools.move_mission(SC2Mission.CUTTHROAT, Difficulty.MEDIUM, Difficulty.EASY)
        # Additional changes on Advanced Tactics
        if adv_tactics:
            # WoL
            pools.move_mission(SC2Mission.THE_GREAT_TRAIN_ROBBERY, Difficulty.EASY, Difficulty.STARTER)
            pools.move_mission(SC2Mission.SMASH_AND_GRAB, Difficulty.EASY, Difficulty.STARTER)
            pools.move_mission(SC2Mission.THE_MOEBIUS_FACTOR, Difficulty.MEDIUM, Difficulty.EASY)
            pools.move_mission(SC2Mission.WELCOME_TO_THE_JUNGLE, Difficulty.MEDIUM, Difficulty.EASY)
            pools.move_mission(SC2Mission.ENGINE_OF_DESTRUCTION, Difficulty.HARD, Difficulty.MEDIUM)
            # LotV
            pools.move_mission(SC2Mission.AMON_S_REACH, Difficulty.EASY, Difficulty.STARTER)
    # Prophecy needs to be adjusted if by itself
    if enabled_campaigns == {SC2Campaign.PROPHECY}:
        pools.move_mission(SC2Mission.A_SINISTER_TURN, Difficulty.MEDIUM, Difficulty.EASY)
    # Prologue's only valid starter is the goal mission
    if enabled_campaigns == {SC2Campaign.PROLOGUE} \
            or mission_order_type in static_mission_orders \
            and get_option_value(world, "shuffle_campaigns") == ShuffleCampaigns.option_false:
        pools.move_mission(SC2Mission.DARK_WHISPERS, Difficulty.EASY, Difficulty.STARTER)
    # HotS
    kerriganless = get_option_value(world, "kerrigan_presence") not in kerrigan_unit_available \
        or SC2Campaign.HOTS not in enabled_campaigns
    if adv_tactics:
        # Medium -> Easy
        for mission in (SC2Mission.FIRE_IN_THE_SKY, SC2Mission.WAKING_THE_ANCIENT, SC2Mission.CONVICTION):
            pools.move_mission(mission, Difficulty.MEDIUM, Difficulty.EASY)
        # Hard -> Medium
        pools.move_mission(SC2Mission.PHANTOMS_OF_THE_VOID, Difficulty.HARD, Difficulty.MEDIUM)
        if not kerriganless:
            # Additional starter mission assuming player starts with minimal anti-air
            pools.move_mission(SC2Mission.WAKING_THE_ANCIENT, Difficulty.EASY, Difficulty.STARTER)
    if grant_story_tech:
        # Additional starter mission if player is granted story tech
        pools.move_mission(SC2Mission.ENEMY_WITHIN, Difficulty.EASY, Difficulty.STARTER)
        pools.move_mission(SC2Mission.TEMPLAR_S_RETURN, Difficulty.EASY, Difficulty.STARTER)
        pools.move_mission(SC2Mission.THE_ESCAPE, Difficulty.MEDIUM, Difficulty.STARTER)
        pools.move_mission(SC2Mission.IN_THE_ENEMY_S_SHADOW, Difficulty.MEDIUM, Difficulty.STARTER)
    if (grant_story_tech and grant_story_levels) or kerriganless:
        # The player has, all the stuff he needs, provided under these settings
        pools.move_mission(SC2Mission.SUPREME, Difficulty.MEDIUM, Difficulty.STARTER)
        pools.move_mission(SC2Mission.THE_INFINITE_CYCLE, Difficulty.HARD, Difficulty.STARTER)
    if get_option_value(world, "take_over_ai_allies") == TakeOverAIAllies.option_true:
        pools.move_mission(SC2Mission.HARBINGER_OF_OBLIVION, Difficulty.MEDIUM, Difficulty.STARTER)
    if pools.get_pool_size(Difficulty.STARTER) < 2 and not kerriganless or adv_tactics:
        # Conditionally moving Easy missions to Starter
        pools.move_mission(SC2Mission.HARVEST_OF_SCREAMS, Difficulty.EASY, Difficulty.STARTER)
        pools.move_mission(SC2Mission.DOMINATION, Difficulty.EASY, Difficulty.STARTER)
    if pools.get_pool_size(Difficulty.STARTER) < 2:
        pools.move_mission(SC2Mission.TEMPLAR_S_RETURN, Difficulty.EASY, Difficulty.STARTER)
    if pools.get_pool_size(Difficulty.STARTER) + pools.get_pool_size(Difficulty.EASY) < 2:
        # Flashpoint needs just a few items at start but competent comp at the end
        pools.move_mission(SC2Mission.FLASHPOINT, Difficulty.HARD, Difficulty.EASY)


def create_regular_mission_order(world: 'SC2World', mission_pools: SC2MOGenMissionPools) -> Dict[str, Dict[str, Any]]:
    mission_order_type = get_option_value(world, "mission_order")

    if mission_order_type in static_mission_orders:
        return create_static_mission_order(world, mission_order_type, mission_pools)
    else:
        return create_dynamic_mission_order(world, mission_order_type, mission_pools)

def create_static_mission_order(world: 'SC2World', mission_order_type: int, mission_pools: SC2MOGenMissionPools) -> Dict[str, Dict[str, Any]]:
    mission_order: Dict[str, Dict[str, Any]] = {}

    enabled_campaigns = get_enabled_campaigns(world)
    if mission_order_type == MissionOrder.option_vanilla:
        missions = "vanilla"
    elif get_option_value(world, "shuffle_campaigns") == ShuffleCampaigns.option_true:
        missions = "random"
    else:
        missions = "vanilla_shuffled"
    
    if mission_order_type == MissionOrder.option_mini_campaign:
        prefix = "mini "
    else:
        prefix = ""

    def mission_order_preset(name: str) -> Dict[str, str]:
        return {
            "preset": prefix + name,
            "missions": missions
        }

    if SC2Campaign.WOL in enabled_campaigns:
        mission_order[SC2Campaign.WOL.campaign_name] = mission_order_preset("wol")
        
    if SC2Campaign.PROPHECY in enabled_campaigns:
        mission_order[SC2Campaign.PROPHECY.campaign_name] = mission_order_preset("prophecy")
        if SC2Campaign.WOL in enabled_campaigns:
            mission_order[SC2Campaign.PROPHECY.campaign_name]["entry_rules"] = [{ "scope": SC2Campaign.WOL.campaign_name + "/Artifact/1" }]

    if SC2Campaign.HOTS in enabled_campaigns:
        mission_order[SC2Campaign.HOTS.campaign_name] = mission_order_preset("hots")

    if SC2Campaign.PROLOGUE in enabled_campaigns:
        mission_order[SC2Campaign.PROLOGUE.campaign_name] = mission_order_preset("prologue")

    if SC2Campaign.LOTV in enabled_campaigns:
        mission_order[SC2Campaign.LOTV.campaign_name] = mission_order_preset("lotv")

    if SC2Campaign.EPILOGUE in enabled_campaigns:
        mission_order[SC2Campaign.EPILOGUE.campaign_name] = mission_order_preset("epilogue")
        entry_rules = []
        if SC2Campaign.WOL in enabled_campaigns:
            entry_rules.append({ "scope": SC2Campaign.WOL.campaign_name })
        if SC2Campaign.HOTS in enabled_campaigns:
            entry_rules.append({ "scope": SC2Campaign.HOTS.campaign_name })
        if SC2Campaign.LOTV in enabled_campaigns:
            entry_rules.append({ "scope": SC2Campaign.LOTV.campaign_name })
        mission_order[SC2Campaign.EPILOGUE.campaign_name]["entry_rules"] = entry_rules

    if SC2Campaign.NCO in enabled_campaigns:
        mission_order[SC2Campaign.NCO.campaign_name] = mission_order_preset("nco")

    # Resolve immediately so the layout updates are simpler
    mission_order = CustomMissionOrder(mission_order).value

    # Vanilla Shuffled is allowed to drop some slots
    if mission_order_type == MissionOrder.option_vanilla_shuffled:
        remove_missions(world, mission_order, mission_pools)

    # Vanilla Shuffled & Mini Campaign get a curated final mission
    if mission_order_type != MissionOrder.option_vanilla:
        force_final_missions(world, mission_order)

    return mission_order

def force_final_missions(world: 'SC2World', mission_order: Dict[str, Dict[str, Any]]):
    goal_mission: Optional[SC2Mission] = None
    excluded_missions = get_excluded_missions(world)
    enabled_campaigns = get_enabled_campaigns(world)
    # Prefer long campaigns over shorter ones and harder missions over easier ones
    goal_priorities = {campaign: get_campaign_goal_priority(campaign, excluded_missions) for campaign in enabled_campaigns}
    goal_level = max(goal_priorities.values())
    candidate_campaigns: List[SC2Campaign] = [campaign for campaign, goal_priority in goal_priorities.items() if goal_priority == goal_level]
    candidate_campaigns.sort(key=lambda it: it.id)

    for goal_campaign in candidate_campaigns:
        primary_goal = campaign_final_mission_locations[goal_campaign]
        if primary_goal is None or primary_goal.mission in excluded_missions:
            # No primary goal or its mission is excluded
            candidate_missions = list(campaign_alt_final_mission_locations[goal_campaign].keys())
            candidate_missions = [mission for mission in candidate_missions if mission not in excluded_missions]
            if len(candidate_missions) == 0:
                raise Exception(f"There are no valid goal missions for campaign {goal_campaign.campaign_name}. Please exclude fewer missions.")
            goal_mission = world.random.choice(candidate_missions)
        else:
            goal_mission = primary_goal.mission
        
        # The goal layout for static presets is the layout corresponding to the last key
        goal_layout = list(mission_order[goal_campaign.campaign_name].keys())[-1]
        goal_index = mission_order[goal_campaign.campaign_name][goal_layout]["size"] - 1
        mission_order[goal_campaign.campaign_name][goal_layout]["missions"].append({
            "index": [goal_index],
            "mission_pool": [goal_mission.id]
        })

    # Remove goal status from lower priority campaigns
    for campaign in enabled_campaigns:
        if not campaign in candidate_campaigns:
            mission_order[campaign.campaign_name]["goal"] = False

def remove_missions(world: 'SC2World', mission_order: Dict[str, Dict[str, Any]], mission_pools: SC2MOGenMissionPools):
    enabled_campaigns = get_enabled_campaigns(world)
    removed_counts: Dict[SC2Campaign, Dict[str, int]] = {}
    for campaign in enabled_campaigns:
        # Count missing missions for each campaign individually
        campaign_size = sum(layout["size"] for layout in mission_order[campaign.campaign_name].values() if type(layout) == dict)
        allowed_missions = mission_pools.count_allowed_missions(campaign)
        removal_count = campaign_size - allowed_missions
        if removal_count > len(removal_priorities[campaign]):
            raise Exception(f"Too many missions of campaign {campaign.campaign_name} excluded, cannot fill vanilla shuffled mission order.")
        for layout in removal_priorities[campaign][:removal_count]:
            removed_counts.setdefault(campaign, {}).setdefault(layout, 0)
            removed_counts[campaign][layout] += 1
            mission_order[campaign.campaign_name][layout]["size"] -= 1

    # Fix mission indices & nexts
    for (campaign, layouts) in removed_counts.items():
        for (layout, amount) in layouts.items():
            new_size = mission_order[campaign.campaign_name][layout]["size"]
            original_size = new_size + amount
            for removed_idx in range(new_size, original_size):
                for mission in mission_order[campaign.campaign_name][layout]["missions"]:
                    if "index" in mission and removed_idx in mission["index"]:
                        mission["index"].remove(removed_idx)
                    if "next" in mission and removed_idx in mission["next"]:
                        mission["next"].remove(removed_idx)

    # Special cases
    if SC2Campaign.WOL in removed_counts:
        if "Char" in removed_counts[SC2Campaign.WOL]:
            # Remove the first two mission changes that create the branching path
            mission_order[SC2Campaign.WOL.campaign_name]["Char"]["missions"] = mission_order[SC2Campaign.WOL.campaign_name]["Char"]["missions"][2:]
    if SC2Campaign.NCO in removed_counts:
        # Update entry rules for Mission Pack 2 & 3
        for idx in range(2):
            this_layout = f"Mission Pack {idx + 2}"
            prev_layout = f"Mission Pack {idx + 1}"
            prev_last_index = mission_order[SC2Campaign.NCO.campaign_name][prev_layout]["size"] - 1
            mission_order[SC2Campaign.NCO.campaign_name][this_layout]["entry_rules"] = [{
                "scope": [f"../{prev_layout}/{prev_last_index}"]
            }]
        # Remove the whole last layout if its size is 0
        if "Mission Pack 3" in removed_counts[SC2Campaign.NCO] and removed_counts[SC2Campaign.NCO]["Mission Pack 3"] == 3:
            mission_order[SC2Campaign.NCO.campaign_name].pop("Mission Pack 3")

removal_priorities: Dict[SC2Campaign, List[str]] = {
    SC2Campaign.WOL: [
        "Colonist",
        "Covert",
        "Covert",
        "Char",
        "Rebellion",
        "Artifact",
        "Artifact",
        "Rebellion"
    ],
    SC2Campaign.PROPHECY: [
        "Prophecy",
        "Prophecy"
    ],
    SC2Campaign.HOTS: [
        "Umoja",
        "Kaldir",
        "Char",
        "Zerus",
        "Skygeirr Station"
    ],
    SC2Campaign.PROLOGUE: [
        "Prologue",
    ],
    SC2Campaign.LOTV: [
        "Ulnar",
        "Return to Aiur",
        "Aiur",
        "Tal'darim",
        "Purifier",
        "Shakuras",
        "Korhal"
    ],
    SC2Campaign.EPILOGUE: [
        "Epilogue",
    ],
    SC2Campaign.NCO: [
        "Mission Pack 3",
        "Mission Pack 3",
        "Mission Pack 2",
        "Mission Pack 2",
        "Mission Pack 1",
        "Mission Pack 1",
        "Mission Pack 3"
    ]
}

def make_grid(world: 'SC2World', size: int) -> Dict[str, Dict[str, Any]]:
    mission_order = {
        "grid": {
            "display_name": "",
            "type": "grid",
            "size": size,
            "two_start_positions": get_option_value(world, "grid_two_start_positions") == GridTwoStartPositions.option_true
        }
    }
    return mission_order

def make_golden_path(size: int) -> Dict[str, Dict[str, Any]]:
    mission_order = {
        "golden path": {
            "display_name": "",
            "preset": "golden path",
            "size": size,
        }
    }
    return mission_order

def make_gauntlet(size: int) -> Dict[str, Dict[str, Any]]:
    mission_order = {
        "gauntlet": {
            "display_name": "",
            "type": "gauntlet",
            "size": size,
        }
    }
    return mission_order

def make_blitz(size: int) -> Dict[str, Dict[str, Any]]:
    mission_order = {
        "blitz": {
            "display_name": "",
            "type": "blitz",
            "size": size,
        }
    }
    return mission_order

def make_hopscotch(world: 'SC2World', size: int) -> Dict[str, Dict[str, Any]]:
    mission_order = {
        "hopscotch": {
            "display_name": "",
            "type": "hopscotch",
            "size": size,
            "two_start_positions": get_option_value(world, "grid_two_start_positions") == GridTwoStartPositions.option_true
        }
    }
    return mission_order

def create_dynamic_mission_order(world: 'SC2World', mission_order_type: int, mission_pools: SC2MOGenMissionPools) -> Dict[str, Dict[str, Any]]:
    num_missions = min(mission_pools.get_allowed_mission_count(), get_option_value(world, "maximum_campaign_size"))
    num_missions = max(2, num_missions)
    if mission_order_type == MissionOrder.option_grid:
        return make_grid(world, num_missions)
    if mission_order_type == MissionOrder.option_golden_path:
        return make_golden_path(num_missions)
    elif mission_order_type == MissionOrder.option_gauntlet:
        return make_gauntlet(num_missions)
    elif mission_order_type == MissionOrder.option_blitz:
        return make_blitz(num_missions)
    elif mission_order_type == MissionOrder.option_hopscotch:
        return make_hopscotch(world, num_missions)
