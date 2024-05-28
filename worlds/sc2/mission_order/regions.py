import typing

from worlds.AutoWorld import World
from ..locations import LocationData, Location
from ..mission_tables import SC2Mission
from ..options import get_option_value, ShuffleNoBuild, RequiredTactics, ExtraLocations, kerrigan_unit_available, TakeOverAIAllies
from .structs import SC2MissionOrder, Difficulty

def mission_order_regions(
    world: World, locations: typing.Tuple[LocationData, ...], location_cache: typing.List[Location]
):
    # 'locations' contains both actual game locations and beat event locations for all mission regions
    # When a region (mission) is accessible, all its locations are potentially accessible
    # Accessible in this context always means "its access rule evaluates to True"
    # This includes the beat events, which copy the access rules of the victory locations
    # Beat events being added to logical inventory is auto-magic:
    # Event locations contain an event item of (by default) identical name,
    # which Archipelago's generator will consider part of the logical inventory
    # whenever the event location becomes accessible
    mission_order = SC2MissionOrder(world, get_option_value(world, "custom_mission_order"))

    # Set up mission pools
    mission_order.mission_pools.set_exclusions([], []) # TODO set excluded + unexcluded
    adjust_mission_pools(world, mission_order)
    
    # Set up requirements for individual parts of the mission order
    mission_order.resolve_unlocks()
    
    # Ensure total accessibilty and resolve relative difficulties
    mission_order.fill_min_steps()
    mission_order.resolve_difficulties()
    
    # Build the mission order
    mission_order.fill_missions(world, [], locations, location_cache) # TODO set locked missions
    mission_order.make_connections(world)
    
    return mission_order

def adjust_mission_pools(world: World, mission_order: SC2MissionOrder):
    pools = mission_order.mission_pools
    # Mission pool changes
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
    # TODO
    # # Prophecy needs to be adjusted on tiny grid
    # if enabled_campaigns == {SC2Campaign.PROPHECY} and mission_order_type == MissionOrder.option_tiny_grid:
    #     pools.move_mission(SC2Mission.A_SINISTER_TURN, Difficulty.MEDIUM, Difficulty.EASY)
    # # Prologue's only valid starter is the goal mission
    # if enabled_campaigns == {SC2Campaign.PROLOGUE} \
    #         or mission_order_type in campaign_depending_orders \
    #         and get_option_value(world, "shuffle_campaigns") == ShuffleCampaigns.option_false:
    #     pools.move_mission(SC2Mission.DARK_WHISPERS, Difficulty.EASY, Difficulty.STARTER)
    # HotS
    kerriganless = get_option_value(world, "kerrigan_presence") not in kerrigan_unit_available \
        # or SC2Campaign.HOTS not in enabled_campaigns
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
