from typing import List, Dict, Tuple, Optional, Callable, NamedTuple, Union, TYPE_CHECKING
import math

from BaseClasses import Region, Entrance, Location, CollectionState
from .options import get_option_value, MissionOrder, get_enabled_campaigns, campaign_depending_orders, \
    GridTwoStartPositions, static_mission_orders, dynamic_mission_orders
from .mission_tables import MissionInfo, vanilla_mission_req_table, \
    MissionPools, SC2Campaign, get_goal_location, SC2Mission, MissionConnection, FillMission
from .mission_orders import make_gauntlet, make_blitz, make_golden_path, make_hopscotch
from .pool_filter import filter_missions


if TYPE_CHECKING:
    from . import SC2World
    from .locations import LocationData


class SC2MissionSlot(NamedTuple):
    campaign: SC2Campaign
    slot: Union[MissionPools, SC2Mission, None]


def create_regions(
    world: 'SC2World', locations: Tuple['LocationData', ...], location_cache: List[Location]
) -> Tuple[Dict[SC2Campaign, Dict[str, MissionInfo]], int, str]:
    """
    Creates region connections by calling the multiworld's `connect()` methods
    Returns a 3-tuple containing:
    * dict[SC2Campaign, Dict[str, MissionInfo]] mapping a campaign and mission name to its data
    * int The number of missions in the world
    * str The name of the goal location
    """
    mission_order_type: MissionOrder = world.options.mission_order

    if mission_order_type == MissionOrder.option_vanilla:
        return create_vanilla_regions(world, locations, location_cache)
    elif mission_order_type == MissionOrder.option_grid:
        return create_grid_regions(world, locations, location_cache)
    else:
        return create_structured_regions(world, locations, location_cache, mission_order_type)

def create_vanilla_regions(
    world: 'SC2World',
    locations: Tuple['LocationData', ...],
    location_cache: List[Location],
) -> Tuple[Dict[SC2Campaign, Dict[str, MissionInfo]], int, str]:
    locations_per_region = get_locations_per_region(locations)
    regions = [create_region(world, locations_per_region, location_cache, "Menu")]

    mission_pools: Dict[MissionPools, List[SC2Mission]] = filter_missions(world)
    final_mission = mission_pools[MissionPools.FINAL][0]

    enabled_campaigns = get_enabled_campaigns(world)
    names: Dict[str, int] = {}

    # Generating all regions and locations for each enabled campaign
    for campaign in enabled_campaigns:
        for region_name in vanilla_mission_req_table[campaign].keys():
            regions.append(create_region(world, locations_per_region, location_cache, region_name))
    world.multiworld.regions += regions
    vanilla_mission_reqs = {campaign: missions for campaign, missions in vanilla_mission_req_table.items() if campaign in enabled_campaigns}

    def wol_cleared_missions(state: CollectionState, mission_count: int) -> bool:
        return state.has_group("WoL Missions", world.player, mission_count)
    
    player: int = world.player
    if SC2Campaign.WOL in enabled_campaigns:
        connect(world, names, 'Menu', SC2Mission.LIBERATION_DAY.mission_name)
        connect(world, names, SC2Mission.LIBERATION_DAY.mission_name, SC2Mission.THE_OUTLAWS.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.LIBERATION_DAY.mission_name}", player))
        connect(world, names, SC2Mission.THE_OUTLAWS.mission_name, SC2Mission.ZERO_HOUR.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.THE_OUTLAWS.mission_name}", player))
        connect(world, names, SC2Mission.ZERO_HOUR.mission_name, SC2Mission.EVACUATION.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.ZERO_HOUR.mission_name}", player))
        connect(world, names, SC2Mission.EVACUATION.mission_name, SC2Mission.OUTBREAK.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.EVACUATION.mission_name}", player))
        connect(world, names, SC2Mission.OUTBREAK.mission_name, SC2Mission.SAFE_HAVEN.mission_name,
                lambda state: wol_cleared_missions(state, 7) and state.has(f"Beat {SC2Mission.OUTBREAK.mission_name}", player))
        connect(world, names, SC2Mission.OUTBREAK.mission_name, SC2Mission.HAVENS_FALL.mission_name,
                lambda state: wol_cleared_missions(state, 7) and state.has(f"Beat {SC2Mission.OUTBREAK.mission_name}", player))
        connect(world, names, SC2Mission.ZERO_HOUR.mission_name, SC2Mission.SMASH_AND_GRAB.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.ZERO_HOUR.mission_name}", player))
        connect(world, names, SC2Mission.SMASH_AND_GRAB.mission_name, SC2Mission.THE_DIG.mission_name,
                lambda state: wol_cleared_missions(state, 8) and state.has(f"Beat {SC2Mission.SMASH_AND_GRAB.mission_name}", player))
        connect(world, names, SC2Mission.THE_DIG.mission_name, SC2Mission.THE_MOEBIUS_FACTOR.mission_name,
                lambda state: wol_cleared_missions(state, 11) and state.has(f"Beat {SC2Mission.THE_DIG.mission_name}", player))
        connect(world, names, SC2Mission.THE_MOEBIUS_FACTOR.mission_name, SC2Mission.SUPERNOVA.mission_name,
                lambda state: wol_cleared_missions(state, 14) and state.has(f"Beat {SC2Mission.THE_MOEBIUS_FACTOR.mission_name}", player))
        connect(world, names, SC2Mission.SUPERNOVA.mission_name, SC2Mission.MAW_OF_THE_VOID.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.SUPERNOVA.mission_name}", player))
        connect(world, names, SC2Mission.ZERO_HOUR.mission_name, SC2Mission.DEVILS_PLAYGROUND.mission_name,
                lambda state: wol_cleared_missions(state, 4) and state.has(f"Beat {SC2Mission.ZERO_HOUR.mission_name}", player))
        connect(world, names, SC2Mission.DEVILS_PLAYGROUND.mission_name, SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.DEVILS_PLAYGROUND.mission_name}", player))
        connect(world, names, SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name, SC2Mission.BREAKOUT.mission_name,
                lambda state: wol_cleared_missions(state, 8) and state.has(f"Beat {SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name}", player))
        connect(world, names, SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name, SC2Mission.GHOST_OF_A_CHANCE.mission_name,
                lambda state: wol_cleared_missions(state, 8) and state.has(f"Beat {SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name}", player))
        connect(world, names, SC2Mission.ZERO_HOUR.mission_name, SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name,
                lambda state: wol_cleared_missions(state, 6) and state.has(f"Beat {SC2Mission.ZERO_HOUR.mission_name}", player))
        connect(world, names, SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name, SC2Mission.CUTTHROAT.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name}", player))
        connect(world, names, SC2Mission.CUTTHROAT.mission_name, SC2Mission.ENGINE_OF_DESTRUCTION.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.CUTTHROAT.mission_name}", player))
        connect(world, names, SC2Mission.ENGINE_OF_DESTRUCTION.mission_name, SC2Mission.MEDIA_BLITZ.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.ENGINE_OF_DESTRUCTION.mission_name}", player))
        connect(world, names, SC2Mission.MEDIA_BLITZ.mission_name, SC2Mission.PIERCING_OF_THE_SHROUD.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.MEDIA_BLITZ.mission_name}", player))
        connect(world, names, SC2Mission.MAW_OF_THE_VOID.mission_name, SC2Mission.GATES_OF_HELL.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.MAW_OF_THE_VOID.mission_name}", player))
        connect(world, names, SC2Mission.GATES_OF_HELL.mission_name, SC2Mission.BELLY_OF_THE_BEAST.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.GATES_OF_HELL.mission_name}", player))
        connect(world, names, SC2Mission.GATES_OF_HELL.mission_name, SC2Mission.SHATTER_THE_SKY.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.GATES_OF_HELL.mission_name}", player))
        connect(world, names, SC2Mission.GATES_OF_HELL.mission_name, SC2Mission.ALL_IN.mission_name,
                lambda state: state.has('Beat Gates of Hell', player) and (
                        state.has('Beat Shatter the Sky', player) or state.has('Beat Belly of the Beast', player)))

    if SC2Campaign.PROPHECY in enabled_campaigns:
        if SC2Campaign.WOL in enabled_campaigns:
            connect(world, names, SC2Mission.THE_DIG.mission_name, SC2Mission.WHISPERS_OF_DOOM.mission_name,
                    lambda state: state.has(f"Beat {SC2Mission.THE_DIG.mission_name}", player)),
        else:
            vanilla_mission_reqs[SC2Campaign.PROPHECY] = vanilla_mission_reqs[SC2Campaign.PROPHECY].copy()
            vanilla_mission_reqs[SC2Campaign.PROPHECY][SC2Mission.WHISPERS_OF_DOOM.mission_name] = MissionInfo(
                SC2Mission.WHISPERS_OF_DOOM, [], SC2Mission.WHISPERS_OF_DOOM.area)
            connect(world, names, 'Menu', SC2Mission.WHISPERS_OF_DOOM.mission_name),
        connect(world, names, SC2Mission.WHISPERS_OF_DOOM.mission_name, SC2Mission.A_SINISTER_TURN.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.WHISPERS_OF_DOOM.mission_name}", player))
        connect(world, names, SC2Mission.A_SINISTER_TURN.mission_name, SC2Mission.ECHOES_OF_THE_FUTURE.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.A_SINISTER_TURN.mission_name}", player))
        connect(world, names, SC2Mission.ECHOES_OF_THE_FUTURE.mission_name, SC2Mission.IN_UTTER_DARKNESS.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.ECHOES_OF_THE_FUTURE.mission_name}", player))

    if SC2Campaign.HOTS in enabled_campaigns:
        connect(world, names, 'Menu', SC2Mission.LAB_RAT.mission_name),
        connect(world, names, SC2Mission.LAB_RAT.mission_name, SC2Mission.BACK_IN_THE_SADDLE.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.LAB_RAT.mission_name}", player)),
        connect(world, names, SC2Mission.BACK_IN_THE_SADDLE.mission_name, SC2Mission.RENDEZVOUS.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.BACK_IN_THE_SADDLE.mission_name}", player)),
        connect(world, names, SC2Mission.RENDEZVOUS.mission_name, SC2Mission.HARVEST_OF_SCREAMS.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.RENDEZVOUS.mission_name}", player)),
        connect(world, names, SC2Mission.HARVEST_OF_SCREAMS.mission_name, SC2Mission.SHOOT_THE_MESSENGER.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.HARVEST_OF_SCREAMS.mission_name}", player)),
        connect(world, names, SC2Mission.SHOOT_THE_MESSENGER.mission_name, SC2Mission.ENEMY_WITHIN.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.SHOOT_THE_MESSENGER.mission_name}", player)),
        connect(world, names, SC2Mission.RENDEZVOUS.mission_name, SC2Mission.DOMINATION.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.RENDEZVOUS.mission_name}", player)),
        connect(world, names, SC2Mission.DOMINATION.mission_name, SC2Mission.FIRE_IN_THE_SKY.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.DOMINATION.mission_name}", player)),
        connect(world, names, SC2Mission.FIRE_IN_THE_SKY.mission_name, SC2Mission.OLD_SOLDIERS.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.FIRE_IN_THE_SKY.mission_name}", player)),
        connect(world, names, SC2Mission.OLD_SOLDIERS.mission_name, SC2Mission.WAKING_THE_ANCIENT.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.OLD_SOLDIERS.mission_name}", player)),
        connect(world, names, SC2Mission.ENEMY_WITHIN.mission_name, SC2Mission.WAKING_THE_ANCIENT.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.ENEMY_WITHIN.mission_name}", player)),
        connect(world, names, SC2Mission.WAKING_THE_ANCIENT.mission_name, SC2Mission.THE_CRUCIBLE.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.WAKING_THE_ANCIENT.mission_name}", player)),
        connect(world, names, SC2Mission.THE_CRUCIBLE.mission_name, SC2Mission.SUPREME.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.THE_CRUCIBLE.mission_name}", player)),
        connect(world, names, SC2Mission.SUPREME.mission_name, SC2Mission.INFESTED.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.SUPREME.mission_name}", player) and
                            state.has(f"Beat {SC2Mission.OLD_SOLDIERS.mission_name}", player) and
                            state.has(f"Beat {SC2Mission.ENEMY_WITHIN.mission_name}", player)),
        connect(world, names, SC2Mission.INFESTED.mission_name, SC2Mission.HAND_OF_DARKNESS.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.INFESTED.mission_name}", player)),
        connect(world, names, SC2Mission.HAND_OF_DARKNESS.mission_name, SC2Mission.PHANTOMS_OF_THE_VOID.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.HAND_OF_DARKNESS.mission_name}", player)),
        connect(world, names, SC2Mission.SUPREME.mission_name, SC2Mission.WITH_FRIENDS_LIKE_THESE.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.SUPREME.mission_name}", player) and
                            state.has(f"Beat {SC2Mission.OLD_SOLDIERS.mission_name}", player) and
                            state.has(f"Beat {SC2Mission.ENEMY_WITHIN.mission_name}", player)),
        connect(world, names, SC2Mission.WITH_FRIENDS_LIKE_THESE.mission_name, SC2Mission.CONVICTION.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.WITH_FRIENDS_LIKE_THESE.mission_name}", player)),
        connect(world, names, SC2Mission.CONVICTION.mission_name, SC2Mission.PLANETFALL.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.CONVICTION.mission_name}", player) and
                            state.has(f"Beat {SC2Mission.PHANTOMS_OF_THE_VOID.mission_name}", player)),
        connect(world, names, SC2Mission.PLANETFALL.mission_name, SC2Mission.DEATH_FROM_ABOVE.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.PLANETFALL.mission_name}", player)),
        connect(world, names, SC2Mission.DEATH_FROM_ABOVE.mission_name, SC2Mission.THE_RECKONING.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.DEATH_FROM_ABOVE.mission_name}", player)),

    if SC2Campaign.PROLOGUE in enabled_campaigns:
        connect(world, names, "Menu", SC2Mission.DARK_WHISPERS.mission_name)
        connect(world, names, SC2Mission.DARK_WHISPERS.mission_name, SC2Mission.GHOSTS_IN_THE_FOG.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.DARK_WHISPERS.mission_name}", player))
        connect(world, names, SC2Mission.GHOSTS_IN_THE_FOG.mission_name, SC2Mission.EVIL_AWOKEN.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.GHOSTS_IN_THE_FOG.mission_name}", player))

    if SC2Campaign.LOTV in enabled_campaigns:
        connect(world, names, "Menu", SC2Mission.FOR_AIUR.mission_name)
        connect(world, names, SC2Mission.FOR_AIUR.mission_name, SC2Mission.THE_GROWING_SHADOW.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.FOR_AIUR.mission_name}", player)),
        connect(world, names, SC2Mission.THE_GROWING_SHADOW.mission_name, SC2Mission.THE_SPEAR_OF_ADUN.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.THE_GROWING_SHADOW.mission_name}", player)),
        connect(world, names, SC2Mission.THE_SPEAR_OF_ADUN.mission_name, SC2Mission.SKY_SHIELD.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.THE_SPEAR_OF_ADUN.mission_name}", player)),
        connect(world, names, SC2Mission.SKY_SHIELD.mission_name, SC2Mission.BROTHERS_IN_ARMS.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.SKY_SHIELD.mission_name}", player)),
        connect(world, names, SC2Mission.BROTHERS_IN_ARMS.mission_name, SC2Mission.FORBIDDEN_WEAPON.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.BROTHERS_IN_ARMS.mission_name}", player)),
        connect(world, names, SC2Mission.THE_SPEAR_OF_ADUN.mission_name, SC2Mission.AMON_S_REACH.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.THE_SPEAR_OF_ADUN.mission_name}", player)),
        connect(world, names, SC2Mission.AMON_S_REACH.mission_name, SC2Mission.LAST_STAND.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.AMON_S_REACH.mission_name}", player)),
        connect(world, names, SC2Mission.LAST_STAND.mission_name, SC2Mission.FORBIDDEN_WEAPON.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.LAST_STAND.mission_name}", player)),
        connect(world, names, SC2Mission.FORBIDDEN_WEAPON.mission_name, SC2Mission.TEMPLE_OF_UNIFICATION.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.BROTHERS_IN_ARMS.mission_name}", player)
                              and state.has(f"Beat {SC2Mission.LAST_STAND.mission_name}", player)
                              and state.has(f"Beat {SC2Mission.FORBIDDEN_WEAPON.mission_name}", player)),
        connect(world, names, SC2Mission.TEMPLE_OF_UNIFICATION.mission_name, SC2Mission.THE_INFINITE_CYCLE.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.TEMPLE_OF_UNIFICATION.mission_name}", player)),
        connect(world, names, SC2Mission.THE_INFINITE_CYCLE.mission_name, SC2Mission.HARBINGER_OF_OBLIVION.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.THE_INFINITE_CYCLE.mission_name}", player)),
        connect(world, names, SC2Mission.HARBINGER_OF_OBLIVION.mission_name, SC2Mission.UNSEALING_THE_PAST.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.HARBINGER_OF_OBLIVION.mission_name}", player)),
        connect(world, names, SC2Mission.UNSEALING_THE_PAST.mission_name, SC2Mission.PURIFICATION.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.UNSEALING_THE_PAST.mission_name}", player)),
        connect(world, names, SC2Mission.PURIFICATION.mission_name, SC2Mission.TEMPLAR_S_CHARGE.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.PURIFICATION.mission_name}", player)),
        connect(world, names, SC2Mission.HARBINGER_OF_OBLIVION.mission_name, SC2Mission.STEPS_OF_THE_RITE.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.HARBINGER_OF_OBLIVION.mission_name}", player)),
        connect(world, names, SC2Mission.STEPS_OF_THE_RITE.mission_name, SC2Mission.RAK_SHIR.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.STEPS_OF_THE_RITE.mission_name}", player)),
        connect(world, names, SC2Mission.RAK_SHIR.mission_name, SC2Mission.TEMPLAR_S_CHARGE.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.RAK_SHIR.mission_name}", player)),
        connect(world, names, SC2Mission.TEMPLAR_S_CHARGE.mission_name, SC2Mission.TEMPLAR_S_RETURN.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.PURIFICATION.mission_name}", player)
                              and state.has(f"Beat {SC2Mission.RAK_SHIR.mission_name}", player)
                              and state.has(f"Beat {SC2Mission.TEMPLAR_S_CHARGE.mission_name}", player)),
        connect(world, names, SC2Mission.TEMPLAR_S_RETURN.mission_name, SC2Mission.THE_HOST.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.TEMPLAR_S_RETURN.mission_name}", player)),
        connect(world, names, SC2Mission.THE_HOST.mission_name, SC2Mission.SALVATION.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.THE_HOST.mission_name}", player)),

    if SC2Campaign.EPILOGUE in enabled_campaigns:
        # TODO: Make this aware about excluded campaigns
        connect(world, names, SC2Mission.SALVATION.mission_name, SC2Mission.INTO_THE_VOID.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.SALVATION.mission_name}", player)
                              and state.has(f"Beat {SC2Mission.THE_RECKONING.mission_name}", player)
                              and state.has(f"Beat {SC2Mission.ALL_IN.mission_name}", player)),
        connect(world, names, SC2Mission.INTO_THE_VOID.mission_name, SC2Mission.THE_ESSENCE_OF_ETERNITY.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.INTO_THE_VOID.mission_name}", player)),
        connect(world, names, SC2Mission.THE_ESSENCE_OF_ETERNITY.mission_name, SC2Mission.AMON_S_FALL.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.THE_ESSENCE_OF_ETERNITY.mission_name}", player)),

    if SC2Campaign.NCO in enabled_campaigns:
        connect(world, names, "Menu", SC2Mission.THE_ESCAPE.mission_name)
        connect(world, names, SC2Mission.THE_ESCAPE.mission_name, SC2Mission.SUDDEN_STRIKE.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.THE_ESCAPE.mission_name}", player))
        connect(world, names, SC2Mission.SUDDEN_STRIKE.mission_name, SC2Mission.ENEMY_INTELLIGENCE.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.SUDDEN_STRIKE.mission_name}", player))
        connect(world, names, SC2Mission.ENEMY_INTELLIGENCE.mission_name, SC2Mission.TROUBLE_IN_PARADISE.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.ENEMY_INTELLIGENCE.mission_name}", player))
        connect(world, names, SC2Mission.TROUBLE_IN_PARADISE.mission_name, SC2Mission.NIGHT_TERRORS.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.TROUBLE_IN_PARADISE.mission_name}", player))
        connect(world, names, SC2Mission.NIGHT_TERRORS.mission_name, SC2Mission.FLASHPOINT.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.NIGHT_TERRORS.mission_name}", player))
        connect(world, names, SC2Mission.FLASHPOINT.mission_name, SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.FLASHPOINT.mission_name}", player))
        connect(world, names, SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name, SC2Mission.DARK_SKIES.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name}", player))
        connect(world, names, SC2Mission.DARK_SKIES.mission_name, SC2Mission.END_GAME.mission_name,
                lambda state: state.has(f"Beat {SC2Mission.DARK_SKIES.mission_name}", player))

    goal_location = get_goal_location(final_mission)
    assert goal_location, f"Unable to find a goal location for mission {final_mission}"
    setup_final_location(goal_location, location_cache)

    return (vanilla_mission_reqs, final_mission.id, goal_location)


def create_grid_regions(
    world: 'SC2World',
    locations: Tuple['LocationData', ...],
    location_cache: List[Location],
) -> Tuple[Dict[SC2Campaign, Dict[str, MissionInfo]], int, str]:
    locations_per_region = get_locations_per_region(locations)

    mission_pools = filter_missions(world)
    final_mission = mission_pools[MissionPools.FINAL][0]

    mission_pool = [mission for mission_pool in mission_pools.values() for mission in mission_pool]

    num_missions = min(len(mission_pool), get_option_value(world, "maximum_campaign_size"))
    remove_top_left: bool = get_option_value(world, "grid_two_start_positions") == GridTwoStartPositions.option_true

    regions = [create_region(world, locations_per_region, location_cache, "Menu")]
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
                mission_index = world.random.randint(0, len(missions_to_add) - 1)
                missions[grid_coords] = missions_to_add.pop(mission_index)

        if diagonal_difficulty < MissionPools.VERY_HARD:
            diagonal_difficulty = MissionPools(diagonal_difficulty.value + 1)
            missions_to_add.extend(mission_pools[diagonal_difficulty])

    # Generating regions and locations from selected missions
    for x in range(grid_size_x):
        for y in range(grid_size_y):
            if missions.get((x, y)):
                regions.append(create_region(world, locations_per_region, location_cache, missions[(x, y)].mission_name))
    world.multiworld.regions += regions

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
            connect(world, names, "Menu", mission.mission_name)
        else:
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                connected_coords = (coords[0] + dx, coords[1] + dy)
                if connected_coords in missions:
                    # connections.append(missions[connected_coords])
                    connections.append(MissionConnection(slot_map[connected_coords]))
                    connect(world, names, missions[connected_coords].mission_name, mission.mission_name,
                            make_grid_connect_rule(missions, connected_coords, world.player),
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
    assert final_location, f"Unable to find a goal location for mission {final_mission}"
    setup_final_location(final_location, location_cache)

    return {SC2Campaign.GLOBAL: mission_req_table}, final_mission_id, final_location


def make_grid_connect_rule(
    missions: Dict[Tuple[int, int], SC2Mission],
    connected_coords: Tuple[int, int],
    player: int
) -> Callable[[CollectionState], bool]:
    return lambda state: state.has(f"Beat {missions[connected_coords].mission_name}", player)


def make_dynamic_mission_order(
    world: 'SC2World',
    mission_order_type: int
) -> Dict[SC2Campaign, List[FillMission]]:
    mission_pools = filter_missions(world)

    mission_pool = [mission for mission_pool in mission_pools.values() for mission in mission_pool]

    num_missions = min(len(mission_pool), get_option_value(world, "maximum_campaign_size"))
    num_missions = max(2, num_missions)
    if mission_order_type == MissionOrder.option_golden_path:
        return make_golden_path(world, num_missions)
    # Grid handled by dedicated region generator
    elif mission_order_type == MissionOrder.option_gauntlet:
        return make_gauntlet(num_missions)
    elif mission_order_type == MissionOrder.option_blitz:
        return make_blitz(num_missions)
    elif mission_order_type == MissionOrder.option_hopscotch:
        return make_hopscotch(world.options.grid_two_start_positions, num_missions)


def create_structured_regions(
    world: 'SC2World',
    locations: Tuple['LocationData', ...],
    location_cache: List[Location],
    mission_order_type: MissionOrder,
) -> Tuple[Dict[SC2Campaign, Dict[str, MissionInfo]], int, str]:
    locations_per_region = get_locations_per_region(locations)

    if mission_order_type in static_mission_orders:
        mission_order = static_mission_orders[mission_order_type]()
    else:
        mission_order = make_dynamic_mission_order(world, mission_order_type)
    enabled_campaigns = get_enabled_campaigns(world)
    shuffle_campaigns = get_option_value(world, "shuffle_campaigns")

    mission_pools: Dict[MissionPools, List[SC2Mission]] = filter_missions(world)
    final_mission = mission_pools[MissionPools.FINAL][0]

    regions = [create_region(world, locations_per_region, location_cache, "Menu")]

    names: Dict[str, int] = {}

    mission_slots: List[SC2MissionSlot] = []
    mission_pool = [mission for mission_pool in mission_pools.values() for mission in mission_pool]

    if mission_order_type in campaign_depending_orders:
        # Do slot removal per campaign
        for campaign in enabled_campaigns:
            campaign_mission_pool = [mission for mission in mission_pool if mission.campaign == campaign]
            campaign_mission_pool_size = len(campaign_mission_pool)

            removals = len(mission_order[campaign]) - campaign_mission_pool_size

            for fill_mission in mission_order[campaign]:
                # Removing extra missions if mission pool is too small
                if 0 < fill_mission.removal_priority <= removals:
                    mission_slots.append(SC2MissionSlot(campaign, None))
                elif fill_mission.type == MissionPools.FINAL:
                    if campaign == final_mission.campaign:
                        # Campaign is elected to be goal
                        mission_slots.append(SC2MissionSlot(campaign, final_mission))
                    else:
                        # Not the goal, find the most difficult mission in the pool and set the difficulty
                        campaign_difficulty = max(fill_mission.pool for fill_mission in campaign_mission_pool)
                        mission_slots.append(SC2MissionSlot(campaign, campaign_difficulty))
                else:
                    mission_slots.append(SC2MissionSlot(campaign, fill_mission.type))
    else:
        order = mission_order[SC2Campaign.GLOBAL]
        # Determining if missions must be removed
        mission_pool_size = sum(len(mission_pool) for mission_pool in mission_pools.values())
        removals = len(order) - mission_pool_size

        # Initial fill out of mission list and marking All-In mission
        for fill_mission in order:
            # Removing extra missions if mission pool is too small
            if 0 < fill_mission.removal_priority <= removals:
                mission_slots.append(SC2MissionSlot(SC2Campaign.GLOBAL, None))
            elif fill_mission.type == MissionPools.FINAL:
                mission_slots.append(SC2MissionSlot(SC2Campaign.GLOBAL, final_mission))
            else:
                mission_slots.append(SC2MissionSlot(SC2Campaign.GLOBAL, fill_mission.type))

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
            filler = world.random.randint(0, len(missions_to_add) - 1)
            mission = missions_to_add.pop(filler)
            slot_campaign = mission_slots[slot].campaign
            mission_slots[slot] = SC2MissionSlot(slot_campaign, mission)
        else:
            # Pick a mission from required campaign
            slot_campaign = mission_slots[slot].campaign
            campaign_mission_candidates = [mission for mission in missions_to_add if mission.campaign == slot_campaign]
            mission = world.random.choice(campaign_mission_candidates)
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
            regions.append(create_region(world, locations_per_region, location_cache, mission_slot.slot.mission_name))
    world.multiworld.regions += regions

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
        player = world.player
        if len(mission_names) > 1:
            return lambda state: state.has_all({f"Beat {name}" for name in mission_names}, player) \
                                 and state.has_group("Missions", player, missions_req)
        else:
            return lambda state: state.has(f"Beat {mission_names[0]}", player) \
                                 and state.has_group("Missions", player, missions_req)

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
                    connect(world, names, "Menu", mission.slot.mission_name)
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
                        connect(world, names, required_mission_name, mission.slot.mission_name,
                                build_connection_rule(required_missions_names, mission_order[campaign][i].number))
                        connections.append(MissionConnection(slot_map[connection.campaign][connection.connect_to], connection.campaign))

            mission_req_table[campaign].update({mission.slot.mission_name: MissionInfo(
                mission.slot, connections, mission_order[campaign][i].category,
                number=mission_order[campaign][i].number,
                completion_critical=mission_order[campaign][i].completion_critical,
                or_requirements=mission_order[campaign][i].or_requirements,
                ui_vertical_padding=mission_order[campaign][i].ui_vertical_padding),
            })

    final_mission_id = final_mission.id
    # Changing the completion condition for alternate final missions into an event
    final_location = get_goal_location(final_mission)
    assert final_location, f"Unable to find a goal location for mission {final_mission}"
    setup_final_location(final_location, location_cache)

    return mission_req_table, final_mission_id, final_location


def setup_final_location(final_location, location_cache):
    # Final location should be near the end of the cache
    for i in range(len(location_cache) - 1, -1, -1):
        if location_cache[i].name == final_location:
            location_cache[i].address = None
            break


def create_location(player: int, location_data: 'LocationData', region: Region,
                    location_cache: List[Location]) -> Location:
    location = Location(player, location_data.name, location_data.code, region)
    location.access_rule = location_data.rule

    location_cache.append(location)

    return location


def create_region(world: 'SC2World', locations_per_region: Dict[str, List['LocationData']],
                  location_cache: List[Location], name: str) -> Region:
    region = Region(name, world.player, world.multiworld)

    if name in locations_per_region:
        for location_data in locations_per_region[name]:
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

