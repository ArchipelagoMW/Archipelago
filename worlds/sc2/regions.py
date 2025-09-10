from typing import TYPE_CHECKING, List, Dict, Any, Tuple, Optional

from Options import OptionError
from .locations import LocationData, Location
from .mission_tables import (
    SC2Mission, SC2Campaign, MissionFlag, get_campaign_goal_priority,
    campaign_final_mission_locations, campaign_alt_final_mission_locations
)
from .options import (
    ShuffleNoBuild, RequiredTactics, ShuffleCampaigns,
    kerrigan_unit_available, TakeOverAIAllies, MissionOrder, get_excluded_missions, get_enabled_campaigns,
    static_mission_orders,
    TwoStartPositions, KeyMode, EnableMissionRaceBalancing, EnableRaceSwapVariants, NovaGhostOfAChanceVariant,
    WarCouncilNerfs, GrantStoryTech
)
from .mission_order.options import CustomMissionOrder
from .mission_order import SC2MissionOrder
from .mission_order.nodes import SC2MOGenMissionOrder, Difficulty
from .mission_order.mission_pools import SC2MOGenMissionPools
from .mission_order.generation import resolve_unlocks, fill_depths, resolve_difficulties, fill_missions, make_connections, resolve_generic_keys

if TYPE_CHECKING:
    from . import SC2World


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
    setup_mission_pool_balancing(world, mission_pools)

    mission_order_type = world.options.mission_order
    if mission_order_type == MissionOrder.option_custom:
        mission_order_dict = world.options.custom_mission_order.value
    else:
        mission_order_option = create_regular_mission_order(world, mission_pools)
        if mission_order_type in static_mission_orders:
            # Static orders get converted early to curate preset content, so it can be used as-is
            mission_order_dict = mission_order_option
        else:
            mission_order_dict = CustomMissionOrder(mission_order_option).value
    mission_order = SC2MOGenMissionOrder(world, mission_order_dict)

    # Set up requirements for individual parts of the mission order
    resolve_unlocks(mission_order)
    
    # Ensure total accessibilty and resolve relative difficulties
    fill_depths(mission_order)
    resolve_difficulties(mission_order)
    
    # Build the mission order
    fill_missions(mission_order, mission_pools, world, [], locations, location_cache) # TODO set locked missions
    make_connections(mission_order, world)

    # Fill in Key requirements now that missions are placed
    resolve_generic_keys(mission_order)
    
    return SC2MissionOrder(mission_order, mission_pools)

def adjust_mission_pools(world: 'SC2World', pools: SC2MOGenMissionPools):
    # Mission pool changes
    mission_order_type = world.options.mission_order.value
    enabled_campaigns = get_enabled_campaigns(world)
    adv_tactics = world.options.required_tactics.value != RequiredTactics.option_standard
    shuffle_no_build = world.options.shuffle_no_build.value
    extra_locations = world.options.extra_locations.value
    grant_story_tech = world.options.grant_story_tech.value
    grant_story_levels = world.options.grant_story_levels.value
    war_council_nerfs = world.options.war_council_nerfs.value == WarCouncilNerfs.option_true

    # WoL
    if shuffle_no_build == ShuffleNoBuild.option_false or adv_tactics:
        # Replacing No Build missions with Easy missions
        # WoL
        pools.move_mission(SC2Mission.ZERO_HOUR, Difficulty.EASY, Difficulty.STARTER)
        pools.move_mission(SC2Mission.EVACUATION, Difficulty.EASY, Difficulty.STARTER)
        pools.move_mission(SC2Mission.EVACUATION_Z, Difficulty.EASY, Difficulty.STARTER)
        pools.move_mission(SC2Mission.EVACUATION_P, Difficulty.EASY, Difficulty.STARTER)
        pools.move_mission(SC2Mission.DEVILS_PLAYGROUND, Difficulty.EASY, Difficulty.STARTER)
        pools.move_mission(SC2Mission.DEVILS_PLAYGROUND_Z, Difficulty.EASY, Difficulty.STARTER)
        pools.move_mission(SC2Mission.DEVILS_PLAYGROUND_P, Difficulty.EASY, Difficulty.STARTER)
        if world.options.required_tactics != RequiredTactics.option_any_units:
            # Per playtester feedback: doing this mission with only one unit is flaky
            # but there are enough viable comps that >= 2 random units is probably workable
            pools.move_mission(SC2Mission.THE_GREAT_TRAIN_ROBBERY, Difficulty.EASY, Difficulty.STARTER)
            pools.move_mission(SC2Mission.THE_GREAT_TRAIN_ROBBERY_Z, Difficulty.EASY, Difficulty.STARTER)
            pools.move_mission(SC2Mission.THE_GREAT_TRAIN_ROBBERY_P, Difficulty.EASY, Difficulty.STARTER)
        # LotV
        pools.move_mission(SC2Mission.THE_GROWING_SHADOW, Difficulty.EASY, Difficulty.STARTER)
        if shuffle_no_build == ShuffleNoBuild.option_false:
            # Pushing Outbreak to Normal, as it cannot be placed as the second mission on Build-Only
            pools.move_mission(SC2Mission.OUTBREAK, Difficulty.EASY, Difficulty.MEDIUM)
            # Pushing extra Normal missions to Easy
            pools.move_mission(SC2Mission.ECHOES_OF_THE_FUTURE, Difficulty.MEDIUM, Difficulty.EASY)
            pools.move_mission(SC2Mission.CUTTHROAT, Difficulty.MEDIUM, Difficulty.EASY)
        # Additional changes on Advanced Tactics
        if adv_tactics:
            # WoL
            pools.move_mission(SC2Mission.SMASH_AND_GRAB, Difficulty.EASY, Difficulty.STARTER)
            pools.move_mission(SC2Mission.THE_MOEBIUS_FACTOR, Difficulty.MEDIUM, Difficulty.EASY)
            pools.move_mission(SC2Mission.THE_MOEBIUS_FACTOR_Z, Difficulty.MEDIUM, Difficulty.EASY)
            pools.move_mission(SC2Mission.THE_MOEBIUS_FACTOR_P, Difficulty.MEDIUM, Difficulty.EASY)
            pools.move_mission(SC2Mission.WELCOME_TO_THE_JUNGLE, Difficulty.MEDIUM, Difficulty.EASY)
            pools.move_mission(SC2Mission.ENGINE_OF_DESTRUCTION, Difficulty.HARD, Difficulty.MEDIUM)
    # Prophecy needs to be adjusted if by itself
    if enabled_campaigns == {SC2Campaign.PROPHECY}:
        pools.move_mission(SC2Mission.A_SINISTER_TURN, Difficulty.MEDIUM, Difficulty.EASY)
    # Prologue's only valid starter is the goal mission
    if enabled_campaigns == {SC2Campaign.PROLOGUE} \
            or mission_order_type in static_mission_orders \
            and world.options.shuffle_campaigns.value == ShuffleCampaigns.option_false:
        pools.move_mission(SC2Mission.DARK_WHISPERS, Difficulty.EASY, Difficulty.STARTER)
    # HotS
    kerriganless = world.options.kerrigan_presence.value not in kerrigan_unit_available \
        or SC2Campaign.HOTS not in enabled_campaigns
    if grant_story_tech == GrantStoryTech.option_grant:
        # Additional starter mission if player is granted story tech
        pools.move_mission(SC2Mission.ENEMY_WITHIN, Difficulty.EASY, Difficulty.STARTER)
        pools.move_mission(SC2Mission.TEMPLAR_S_RETURN, Difficulty.MEDIUM, Difficulty.STARTER)
        pools.move_mission(SC2Mission.THE_ESCAPE, Difficulty.MEDIUM, Difficulty.STARTER)
        pools.move_mission(SC2Mission.IN_THE_ENEMY_S_SHADOW, Difficulty.MEDIUM, Difficulty.STARTER)
    if not war_council_nerfs:
        pools.move_mission(SC2Mission.TEMPLAR_S_RETURN, Difficulty.MEDIUM, Difficulty.STARTER)
    if (grant_story_tech == GrantStoryTech.option_grant and grant_story_levels) or kerriganless:
        # The player has, all the stuff he needs, provided under these settings
        pools.move_mission(SC2Mission.SUPREME, Difficulty.MEDIUM, Difficulty.STARTER)
        pools.move_mission(SC2Mission.THE_INFINITE_CYCLE, Difficulty.HARD, Difficulty.STARTER)
        pools.move_mission(SC2Mission.CONVICTION, Difficulty.MEDIUM, Difficulty.STARTER)
    if (grant_story_tech != GrantStoryTech.option_grant
        and (
            world.options.nova_ghost_of_a_chance_variant == NovaGhostOfAChanceVariant.option_nco
            or (
                SC2Campaign.NCO in enabled_campaigns
                and world.options.nova_ghost_of_a_chance_variant.value == NovaGhostOfAChanceVariant.option_auto
            )
        )
    ):
        # Using NCO tech for this mission that must be acquired
        pools.move_mission(SC2Mission.GHOST_OF_A_CHANCE, Difficulty.STARTER, Difficulty.MEDIUM)
    if world.options.take_over_ai_allies.value == TakeOverAIAllies.option_true:
        pools.move_mission(SC2Mission.HARBINGER_OF_OBLIVION, Difficulty.MEDIUM, Difficulty.STARTER)
    if pools.get_pool_size(Difficulty.STARTER) < 2 and not kerriganless or adv_tactics:
        # Conditionally moving Easy missions to Starter
        pools.move_mission(SC2Mission.HARVEST_OF_SCREAMS, Difficulty.EASY, Difficulty.STARTER)
        pools.move_mission(SC2Mission.DOMINATION, Difficulty.EASY, Difficulty.STARTER)
    if pools.get_pool_size(Difficulty.STARTER) < 2:
        pools.move_mission(SC2Mission.DOMINATION, Difficulty.EASY, Difficulty.STARTER)
        pools.move_mission(SC2Mission.DOMINATION_T, Difficulty.EASY, Difficulty.STARTER)
        pools.move_mission(SC2Mission.DOMINATION_P, Difficulty.EASY, Difficulty.STARTER)
    if pools.get_pool_size(Difficulty.STARTER) + pools.get_pool_size(Difficulty.EASY) < 2:
        # Flashpoint needs just a few items at start but competent comp at the end
        pools.move_mission(SC2Mission.FLASHPOINT, Difficulty.HARD, Difficulty.EASY)

def setup_mission_pool_balancing(world: 'SC2World', pools: SC2MOGenMissionPools):
    race_mission_balance = world.options.mission_race_balancing.value
    flag_ratios: Dict[MissionFlag, int] = {}
    flag_weights: Dict[MissionFlag, int] = {}
    if race_mission_balance == EnableMissionRaceBalancing.option_semi_balanced:
        flag_weights = { MissionFlag.Terran: 1, MissionFlag.Zerg: 1, MissionFlag.Protoss: 1 }
    elif race_mission_balance == EnableMissionRaceBalancing.option_fully_balanced:
        flag_ratios = { MissionFlag.Terran: 1, MissionFlag.Zerg: 1, MissionFlag.Protoss: 1 }
    pools.set_flag_balances(flag_ratios, flag_weights)

def create_regular_mission_order(world: 'SC2World', mission_pools: SC2MOGenMissionPools) -> Dict[str, Dict[str, Any]]:
    mission_order_type = world.options.mission_order.value

    if mission_order_type in static_mission_orders:
        return create_static_mission_order(world, mission_order_type, mission_pools)
    else:
        return create_dynamic_mission_order(world, mission_order_type, mission_pools)

def create_static_mission_order(world: 'SC2World', mission_order_type: int, mission_pools: SC2MOGenMissionPools) -> Dict[str, Dict[str, Any]]:
    mission_order: Dict[str, Dict[str, Any]] = {}

    enabled_campaigns = get_enabled_campaigns(world)
    if mission_order_type == MissionOrder.option_vanilla:
        missions = "vanilla"
    elif world.options.shuffle_campaigns.value == ShuffleCampaigns.option_true:
        missions = "random"
    else:
        missions = "vanilla_shuffled"
    
    if world.options.enable_race_swap.value == EnableRaceSwapVariants.option_disabled:
        shuffle_raceswaps = False
    else:
        # Picking specific raceswap variants is handled by mission exclusion
        shuffle_raceswaps = True

    key_mode_option = world.options.key_mode.value
    if key_mode_option == KeyMode.option_missions:
        keys = "missions"
    elif key_mode_option == KeyMode.option_questlines:
        keys = "layouts"
    elif key_mode_option == KeyMode.option_progressive_missions:
        keys = "progressive_missions"
    elif key_mode_option == KeyMode.option_progressive_questlines:
        keys = "progressive_layouts"
    elif key_mode_option == KeyMode.option_progressive_per_questline:
        keys = "progressive_per_layout"
    else:
        keys = "none"
    
    if mission_order_type == MissionOrder.option_mini_campaign:
        prefix = "mini "
    else:
        prefix = ""

    def mission_order_preset(name: str) -> Dict[str, str]:
        return {
            "preset": prefix + name,
            "missions": missions,
            "shuffle_raceswaps": shuffle_raceswaps,
            "keys": keys
        }

    prophecy_enabled = SC2Campaign.PROPHECY in enabled_campaigns
    wol_enabled = SC2Campaign.WOL in enabled_campaigns
    if wol_enabled:
        mission_order[SC2Campaign.WOL.campaign_name] = mission_order_preset("wol") 

    if prophecy_enabled:
        mission_order[SC2Campaign.PROPHECY.campaign_name] = mission_order_preset("prophecy")

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

    # WoL requirements should count missions from Prophecy if both are enabled, and Prophecy should require a WoL mission
    # There is a preset that already does this, but special-casing this way is easier to work with for other code
    if wol_enabled and prophecy_enabled:
        fix_wol_prophecy_entry_rules(mission_order)
    
    # Vanilla Shuffled is allowed to drop some slots
    if mission_order_type == MissionOrder.option_vanilla_shuffled:
        remove_missions(world, mission_order, mission_pools)

    # Curate final missions and goal campaigns
    force_final_missions(world, mission_order, mission_order_type)

    return mission_order


def fix_wol_prophecy_entry_rules(mission_order: Dict[str, Dict[str, Any]]):
    prophecy_name = SC2Campaign.PROPHECY.campaign_name

    # Make the mission count entry rules in WoL also count Prophecy
    def fix_entry_rule(entry_rule: Dict[str, Any], local_campaign_scope: str):
        # This appends Prophecy to any scope that points at the local campaign (WoL)
        if "scope" in entry_rule:
            if entry_rule["scope"] == local_campaign_scope:
                entry_rule["scope"] = [local_campaign_scope, prophecy_name]
            elif isinstance(entry_rule["scope"], list) and local_campaign_scope in entry_rule["scope"]:
                entry_rule["scope"] = entry_rule["scope"] + [prophecy_name]
    
    for layout_dict in mission_order[SC2Campaign.WOL.campaign_name].values():
        if not isinstance(layout_dict, dict):
            continue
        if "entry_rules" in layout_dict:
            for entry_rule in layout_dict["entry_rules"]:
                fix_entry_rule(entry_rule, "..")
        if "missions" in layout_dict:
            for mission_dict in layout_dict["missions"]:
                if "entry_rules" in mission_dict:
                    for entry_rule in mission_dict["entry_rules"]:
                        fix_entry_rule(entry_rule, "../..")
    
    # Make Prophecy require Artifact's second mission
    mission_order[prophecy_name][prophecy_name]["entry_rules"] = [{ "scope": [f"{SC2Campaign.WOL.campaign_name}/Artifact/1"]}]


def force_final_missions(world: 'SC2World', mission_order: Dict[str, Dict[str, Any]], mission_order_type: int):
    goal_mission: Optional[SC2Mission] = None
    excluded_missions = get_excluded_missions(world)
    enabled_campaigns = get_enabled_campaigns(world)
    raceswap_variants = [mission for mission in SC2Mission if mission.flags & MissionFlag.RaceSwap]
    # Prefer long campaigns over shorter ones and harder missions over easier ones
    goal_priorities = {campaign: get_campaign_goal_priority(campaign, excluded_missions) for campaign in enabled_campaigns}
    goal_level = max(goal_priorities.values())
    candidate_campaigns: List[SC2Campaign] = [campaign for campaign, goal_priority in goal_priorities.items() if goal_priority == goal_level]
    candidate_campaigns.sort(key=lambda it: it.id)

    # Vanilla Shuffled & Mini Campaign get a curated final mission
    if mission_order_type != MissionOrder.option_vanilla:
        for goal_campaign in candidate_campaigns:
            primary_goal = campaign_final_mission_locations[goal_campaign]
            if primary_goal is None or primary_goal.mission in excluded_missions:
                # No primary goal or its mission is excluded
                candidate_missions = list(campaign_alt_final_mission_locations[goal_campaign].keys())
                # Also allow raceswaps of curated final missions, provided they're not excluded
                for candidate_with_raceswaps in [mission for mission in candidate_missions if mission.flags & MissionFlag.HasRaceSwap]:
                    raceswap_candidates = [mission for mission in raceswap_variants if mission.map_file == candidate_with_raceswaps.map_file]
                    candidate_missions.extend(raceswap_candidates)
                candidate_missions = [mission for mission in candidate_missions if mission not in excluded_missions]
                if len(candidate_missions) == 0:
                    raise OptionError(f"There are no valid goal missions for campaign {goal_campaign.campaign_name}. Please exclude fewer missions.")
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
        if campaign not in candidate_campaigns:
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
            raise OptionError(f"Too many missions of campaign {campaign.campaign_name} excluded, cannot fill vanilla shuffled mission order.")
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
            "two_start_positions": world.options.two_start_positions.value == TwoStartPositions.option_true
        }
    }
    return mission_order

def make_golden_path(world: 'SC2World', size: int) -> Dict[str, Dict[str, Any]]:
    key_mode = world.options.key_mode.value
    if key_mode == KeyMode.option_missions:
        keys = "missions"
    elif key_mode == KeyMode.option_questlines:
        keys = "layouts"
    elif key_mode == KeyMode.option_progressive_missions:
        keys = "progressive_missions"
    elif key_mode == KeyMode.option_progressive_questlines:
        keys = "progressive_layouts"
    elif key_mode == KeyMode.option_progressive_per_questline:
        keys = "progressive_per_layout"
    else:
        keys = "none"
    
    mission_order = {
        "golden path": {
            "display_name": "",
            "preset": "golden path",
            "size": size,
            "keys": keys,
            "two_start_positions": world.options.two_start_positions.value == TwoStartPositions.option_true
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
            "two_start_positions": world.options.two_start_positions.value == TwoStartPositions.option_true
        }
    }
    return mission_order

def create_dynamic_mission_order(world: 'SC2World', mission_order_type: int, mission_pools: SC2MOGenMissionPools) -> Dict[str, Dict[str, Any]]:
    num_missions = min(mission_pools.get_allowed_mission_count(), world.options.maximum_campaign_size.value)
    num_missions = max(1, num_missions)
    if mission_order_type == MissionOrder.option_golden_path:
        return make_golden_path(world, num_missions)
    
    if mission_order_type == MissionOrder.option_grid:
        mission_order = make_grid(world, num_missions)
    elif mission_order_type == MissionOrder.option_gauntlet:
        mission_order = make_gauntlet(num_missions)
    elif mission_order_type == MissionOrder.option_blitz:
        mission_order = make_blitz(num_missions)
    elif mission_order_type == MissionOrder.option_hopscotch:
        mission_order = make_hopscotch(world, num_missions)
    else:
        raise ValueError("Received unknown Mission Order type")
    
    # Optionally add key requirements
    # This only works for layout types that don't define their own entry rules (which is currently all of them)
    # Golden Path handles Key Mode on its own
    key_mode = world.options.key_mode.value
    if key_mode == KeyMode.option_missions:
        mission_order[list(mission_order.keys())[0]]["missions"] = [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] },
            { "index": "entrances", "entry_rules": [] }
        ]
    elif key_mode == KeyMode.option_progressive_missions:
        mission_order[list(mission_order.keys())[0]]["missions"] = [
            { "index": "all", "entry_rules": [{ "items": { "Progressive Key": 1 }}] },
            { "index": "entrances", "entry_rules": [] }
        ]
    
    return mission_order
