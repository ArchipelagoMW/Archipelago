from typing import TYPE_CHECKING, Dict, Callable

from worlds.generic.Rules import set_rule, add_rule
from .Locations import location_table, LocationDict
from .Creatures import all_creatures, aggressive, suffix
from .Options import AggressiveScanLogic
import math

if TYPE_CHECKING:
    from . import SubnauticaWorld
    from BaseClasses import CollectionState, Location


def has_seaglide(state: "CollectionState", player: int):
    return state.has("Seaglide Fragment", player, 2)


def has_modification_station(state: "CollectionState", player: int):
    return state.has("Modification Station Fragment", player, 3)


def has_mobile_vehicle_bay(state: "CollectionState", player: int):
    return state.has("Mobile Vehicle Bay Fragment", player, 3)


def has_moonpool(state: "CollectionState", player: int):
    return state.has("Moonpool Fragment", player, 2)


def has_vehicle_upgrade_console(state: "CollectionState", player: int):
    return state.has("Vehicle Upgrade Console", player) and \
           has_moonpool(state, player)


def has_seamoth(state: "CollectionState", player: int):
    return state.has("Seamoth Fragment", player, 3) and \
           has_mobile_vehicle_bay(state, player)


def has_seamoth_depth_module_mk1(state: "CollectionState", player: int):
    return has_vehicle_upgrade_console(state, player)


def has_seamoth_depth_module_mk2(state: "CollectionState", player: int):
    return has_seamoth_depth_module_mk1(state, player) and \
           has_modification_station(state, player)


def has_seamoth_depth_module_mk3(state: "CollectionState", player: int):
    return has_seamoth_depth_module_mk2(state, player) and \
           has_modification_station(state, player)


def has_cyclops_bridge(state: "CollectionState", player: int):
    return state.has("Cyclops Bridge Fragment", player, 3)


def has_cyclops_engine(state: "CollectionState", player: int):
    return state.has("Cyclops Engine Fragment", player, 3)


def has_cyclops_hull(state: "CollectionState", player: int):
    return state.has("Cyclops Hull Fragment", player, 3)


def has_cyclops(state: "CollectionState", player: int):
    return has_cyclops_bridge(state, player) and \
           has_cyclops_engine(state, player) and \
           has_cyclops_hull(state, player) and \
           has_mobile_vehicle_bay(state, player)


def has_cyclops_depth_module_mk1(state: "CollectionState", player: int):
    return state.has("Cyclops Depth Module MK1", player) and \
           has_modification_station(state, player)


def has_cyclops_depth_module_mk2(state: "CollectionState", player: int):
    return has_cyclops_depth_module_mk1(state, player) and \
           has_modification_station(state, player)


def has_cyclops_depth_module_mk3(state: "CollectionState", player: int):
    return has_cyclops_depth_module_mk2(state, player) and \
           has_modification_station(state, player)


def has_prawn(state: "CollectionState", player: int):
    return state.has("Prawn Suit Fragment", player, 4) and \
           has_mobile_vehicle_bay(state, player)


def has_prawn_propulsion_arm(state: "CollectionState", player: int):
    return state.has("Prawn Suit Propulsion Cannon Fragment", player, 2) and \
           has_vehicle_upgrade_console(state, player)


def has_prawn_depth_module_mk1(state: "CollectionState", player: int):
    return has_vehicle_upgrade_console(state, player)


def has_prawn_depth_module_mk2(state: "CollectionState", player: int):
    return has_prawn_depth_module_mk1(state, player) and \
           has_modification_station(state, player)


def has_laser_cutter(state: "CollectionState", player: int):
    return state.has("Laser Cutter Fragment", player, 3)


def has_stasis_rifle(state: "CollectionState", player: int):
    return state.has("Stasis Rifle Fragment", player, 2)


def has_containment(state: "CollectionState", player: int):
    return state.has("Alien Containment Fragment", player, 2) and state.has("Multipurpose Room", player)


# Either we have propulsion cannon, or prawn + propulsion cannon arm
def has_propulsion_cannon(state: "CollectionState", player: int):
    return state.has("Propulsion Cannon Fragment", player, 2) or \
           (has_prawn(state, player) and has_prawn_propulsion_arm(state, player))


def has_cyclops_shield(state: "CollectionState", player: int):
    return has_cyclops(state, player) and \
           state.has("Cyclops Shield Generator", player)


# Swim depth rules:
# Rebreather, high capacity tank and fins are available from the start.
# All tests for those were done without inventory for light weight.
# Fins and ultra Fins are better than charge fins, so we ignore charge fins.
# We're ignoring lightweight tank in the chart, because the difference is
# negligeable with from high capacity tank. 430m -> 460m
# Fins are not used when using seaglide
#
def get_max_swim_depth(state: "CollectionState", player: int):
    # TODO, Make this a difficulty setting.
    # Only go up to 200m without any submarines for now.
    return 200

    # Rules bellow, are what are technically possible

    # has_ultra_high_capacity_tank = state.has("Ultra High Capacity Tank", player)
    # has_ultra_glide_fins = state.has("Ultra Glide Fins", player)

    # max_depth = 400 # More like 430m. Give some room
    # if has_seaglide(state: "CollectionState", player: int):
    #     if has_ultra_high_capacity_tank:
    #         max_depth = 750 # It's about 50m more. Give some room
    #     else:
    #         max_depth = 600 # It's about 50m more. Give some room
    # elif has_ultra_high_capacity_tank:
    #     if has_ultra_glide_fins:
    #         pass
    #     else:
    #         pass
    # elif has_ultra_glide_fins:
    #     max_depth = 500

    # return max_depth


def get_seamoth_max_depth(state: "CollectionState", player: int):
    if has_seamoth(state, player):
        if has_seamoth_depth_module_mk3(state, player):
            return 900
        elif has_seamoth_depth_module_mk2(state, player):  # Will never be the case, 3 is craftable
            return 500
        elif has_seamoth_depth_module_mk1(state, player):
            return 300
        else:
            return 200
    else:
        return 0


def get_cyclops_max_depth(state: "CollectionState", player):
    if has_cyclops(state, player):
        if has_cyclops_depth_module_mk3(state, player):
            return 1700
        elif has_cyclops_depth_module_mk2(state, player):  # Will never be the case, 3 is craftable
            return 1300
        elif has_cyclops_depth_module_mk1(state, player):
            return 900
        else:
            return 500
    else:
        return 0


def get_prawn_max_depth(state: "CollectionState", player):
    if has_prawn(state, player):
        if has_prawn_depth_module_mk2(state, player):
            return 1700
        elif has_prawn_depth_module_mk1(state, player):
            return 1300
        else:
            return 900
    else:
        return 0


def get_max_depth(state: "CollectionState", player: int):
    # TODO, Difficulty option, we can add vehicle depth + swim depth
    # But at this point, we have to consider traver distance in caves, not
    # just depth
    return max(get_max_swim_depth(state, player),
               get_seamoth_max_depth(state, player),
               get_cyclops_max_depth(state, player),
               get_prawn_max_depth(state, player))


def can_access_location(state: "CollectionState", player: int, loc: LocationDict) -> bool:
    need_laser_cutter = loc.get("need_laser_cutter", False)
    if need_laser_cutter and not has_laser_cutter(state, player):
        return False

    need_propulsion_cannon = loc.get("need_propulsion_cannon", False)
    if need_propulsion_cannon and not has_propulsion_cannon(state, player):
        return False

    pos = loc["position"]
    pos_x = pos["x"]
    pos_y = pos["y"]
    pos_z = pos["z"]

    aurora_dist = math.sqrt((pos_x - 1038.0) ** 2 + (pos_y - -3.4) ** 2 + (pos_z - -163.1) ** 2)
    need_radiation_suit = aurora_dist < 950
    if need_radiation_suit and not state.has("Radiation Suit", player):
        return False

    # Seaglide doesn't unlock anything specific, but just allows for faster movement. 
    # Otherwise the game is painfully slow.
    map_center_dist = math.sqrt(pos_x ** 2 + pos_z ** 2)
    if (map_center_dist > 800 or pos_y < -200) and not has_seaglide(state, player):
        return False

    depth = -pos_y  # y-up
    return get_max_depth(state, player) >= depth


def set_location_rule(world, player: int, loc: LocationDict):
    set_rule(world.get_location(loc["name"], player), lambda state: can_access_location(state, player, loc))


def can_scan_creature(state: "CollectionState", player: int, creature: str) -> bool:
    if not has_seaglide(state, player):
        return False
    return get_max_depth(state, player) >= all_creatures[creature]


def set_creature_rule(world, player: int, creature_name: str) -> "Location":
    location = world.get_location(creature_name + suffix, player)
    set_rule(location,
             lambda state: can_scan_creature(state, player, creature_name))
    return location


aggression_rules: Dict[int, Callable[["CollectionState", int], bool]] = {
    AggressiveScanLogic.option_stasis: has_stasis_rifle,
    AggressiveScanLogic.option_containment: has_containment,
    AggressiveScanLogic.option_either: lambda state, player:
    has_stasis_rifle(state, player) or has_containment(state, player)
}


def set_rules(subnautica_world: "SubnauticaWorld"):
    player = subnautica_world.player
    world = subnautica_world.world

    for loc in location_table.values():
        set_location_rule(world, player, loc)

    if subnautica_world.creatures_to_scan:
        aggressive_rule = aggression_rules.get(world.creature_scan_logic[player], None)
        for creature_name in subnautica_world.creatures_to_scan:
            location = set_creature_rule(world, player, creature_name)
            if creature_name in aggressive and aggressive_rule:
                add_rule(location, lambda state: aggressive_rule(state, player))

    # Victory locations
    set_rule(world.get_location("Neptune Launch", player), lambda state:
        get_max_depth(state, player) >= 1444 and
        has_mobile_vehicle_bay(state, player) and
        state.has("Neptune Launch Platform", player) and
        state.has("Neptune Gantry", player) and
        state.has("Neptune Boosters", player) and
        state.has("Neptune Fuel Reserve", player) and
        state.has("Neptune Cockpit", player) and
        state.has("Ion Power Cell", player) and
        state.has("Ion Battery", player) and
        has_cyclops_shield(state, player))

    set_rule(world.get_location("Disable Quarantine", player), lambda state:
        get_max_depth(state, player) >= 1444)

    set_rule(world.get_location("Full Infection", player), lambda state:
        get_max_depth(state, player) >= 900)

    room = world.get_location("Aurora Drive Room - Upgrade Console", player)
    set_rule(world.get_location("Repair Aurora Drive", player), lambda state: room.can_reach(state))

    world.completion_condition[player] = lambda state: state.has("Victory", player)
