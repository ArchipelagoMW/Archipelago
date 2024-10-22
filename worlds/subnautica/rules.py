from typing import TYPE_CHECKING, Dict, Callable, Optional

from worlds.generic.Rules import set_rule, add_rule
from .locations import location_table, LocationDict
from .creatures import all_creatures, aggressive, suffix, hatchable, containment
from .options import AggressiveScanLogic, SwimRule
import math

if TYPE_CHECKING:
    from . import SubnauticaWorld
    from BaseClasses import CollectionState, Location


def has_seaglide(state: "CollectionState", player: int) -> bool:
    return state.has("Seaglide Fragment", player, 2)


def has_modification_station(state: "CollectionState", player: int) -> bool:
    return state.has("Modification Station Fragment", player, 3)


def has_mobile_vehicle_bay(state: "CollectionState", player: int) -> bool:
    return state.has("Mobile Vehicle Bay Fragment", player, 3)


def has_moonpool(state: "CollectionState", player: int) -> bool:
    return state.has("Moonpool Fragment", player, 2)


def has_vehicle_upgrade_console(state: "CollectionState", player: int) -> bool:
    return state.has("Vehicle Upgrade Console", player) and \
           has_moonpool(state, player)


def has_seamoth(state: "CollectionState", player: int) -> bool:
    return state.has("Seamoth Fragment", player, 3) and \
           has_mobile_vehicle_bay(state, player)


def has_seamoth_depth_module_mk1(state: "CollectionState", player: int) -> bool:
    return has_vehicle_upgrade_console(state, player)


def has_seamoth_depth_module_mk2(state: "CollectionState", player: int) -> bool:
    return has_seamoth_depth_module_mk1(state, player) and \
           has_modification_station(state, player)


def has_seamoth_depth_module_mk3(state: "CollectionState", player: int) -> bool:
    return has_seamoth_depth_module_mk2(state, player) and \
           has_modification_station(state, player)


def has_cyclops_bridge(state: "CollectionState", player: int) -> bool:
    return state.has("Cyclops Bridge Fragment", player, 3)


def has_cyclops_engine(state: "CollectionState", player: int) -> bool:
    return state.has("Cyclops Engine Fragment", player, 3)


def has_cyclops_hull(state: "CollectionState", player: int) -> bool:
    return state.has("Cyclops Hull Fragment", player, 3)


def has_cyclops(state: "CollectionState", player: int) -> bool:
    return has_cyclops_bridge(state, player) and \
           has_cyclops_engine(state, player) and \
           has_cyclops_hull(state, player) and \
           has_mobile_vehicle_bay(state, player)


def has_cyclops_depth_module_mk1(state: "CollectionState", player: int) -> bool:
    # Crafted in the Cyclops, so we don't need to check for crafting station
    return state.has("Cyclops Depth Module MK1", player)


def has_cyclops_depth_module_mk2(state: "CollectionState", player: int) -> bool:
    return has_cyclops_depth_module_mk1(state, player) and \
           has_modification_station(state, player)


def has_cyclops_depth_module_mk3(state: "CollectionState", player: int) -> bool:
    return has_cyclops_depth_module_mk2(state, player) and \
           has_modification_station(state, player)


def has_prawn(state: "CollectionState", player: int) -> bool:
    return state.has("Prawn Suit Fragment", player, 4) and \
           has_mobile_vehicle_bay(state, player)


def has_prawn_propulsion_arm(state: "CollectionState", player: int) -> bool:
    return state.has("Prawn Suit Propulsion Cannon Fragment", player, 2) and \
           has_vehicle_upgrade_console(state, player)


def has_prawn_depth_module_mk1(state: "CollectionState", player: int) -> bool:
    return has_vehicle_upgrade_console(state, player)


def has_prawn_depth_module_mk2(state: "CollectionState", player: int) -> bool:
    return has_prawn_depth_module_mk1(state, player) and \
           has_modification_station(state, player)


def has_laser_cutter(state: "CollectionState", player: int) -> bool:
    return state.has("Laser Cutter Fragment", player, 3)


def has_stasis_rifle(state: "CollectionState", player: int) -> bool:
    return state.has("Stasis Rifle Fragment", player, 2)


def has_containment(state: "CollectionState", player: int) -> bool:
    return state.has("Alien Containment", player) and has_utility_room(state, player)


def has_utility_room(state: "CollectionState", player: int) -> bool:
    return state.has("Large Room", player) or state.has("Multipurpose Room", player)


# Either we have propulsion cannon, or prawn + propulsion cannon arm
def has_propulsion_cannon(state: "CollectionState", player: int) -> bool:
    return state.has("Propulsion Cannon Fragment", player, 2)


def has_cyclops_shield(state: "CollectionState", player: int) -> bool:
    return has_cyclops(state, player) and \
           state.has("Cyclops Shield Generator", player)


def has_ultra_high_capacity_tank(state: "CollectionState", player: int) -> bool:
    return has_modification_station(state, player) and state.has("Ultra High Capacity Tank", player)


def has_lightweight_high_capacity_tank(state: "CollectionState", player: int) -> bool:
    return has_modification_station(state, player) and state.has("Lightweight High Capacity Tank", player)


def has_ultra_glide_fins(state: "CollectionState", player: int) -> bool:
    return has_modification_station(state, player) and state.has("Ultra Glide Fins", player)

# Swim depth rules:
# Rebreather, high capacity tank and fins are available from the start.
# All tests for those were done without inventory for light weight.
# Fins and ultra Fins are better than charge fins, so we ignore charge fins.

# swim speeds: https://subnautica.fandom.com/wiki/Swimming_Speed


def get_max_swim_depth(state: "CollectionState", player: int) -> int:
    swim_rule: SwimRule = state.multiworld.worlds[player].options.swim_rule
    depth: int = swim_rule.base_depth
    if swim_rule.consider_items:
        if has_seaglide(state, player):
            if has_ultra_high_capacity_tank(state, player):
                depth += 350  # It's about 800m. Give some room
            else:
                depth += 200  # It's about 650m. Give some room
        # seaglide and fins cannot be used together
        elif has_ultra_glide_fins(state, player):
            if has_ultra_high_capacity_tank(state, player):
                depth += 150
            elif has_lightweight_high_capacity_tank(state, player):
                depth += 75
            else:
                depth += 50
        elif has_ultra_high_capacity_tank(state, player):
            depth += 100
        elif has_lightweight_high_capacity_tank(state, player):
            depth += 25
    return depth


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
    return get_max_swim_depth(state, player) + max(
        get_seamoth_max_depth(state, player),
        get_cyclops_max_depth(state, player),
        get_prawn_max_depth(state, player)
    )


def is_radiated(x: float, y: float, z: float) -> bool:
    aurora_dist = math.sqrt((x - 1038.0) ** 2 + y ** 2 + (z - -163.1) ** 2)
    return aurora_dist < 950


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

    need_radiation_suit = is_radiated(pos_x, pos_y, pos_z)
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


def get_aggression_rule(option: AggressiveScanLogic, creature_name: str) -> \
        Optional[Callable[["CollectionState", int], bool]]:
    """Get logic rule for a creature scan location."""
    if creature_name not in hatchable and option != option.option_none:  # can only be done via stasis
        return has_stasis_rifle
    # otherwise allow option preference
    return aggression_rules.get(option.value, None)


aggression_rules: Dict[int, Callable[["CollectionState", int], bool]] = {
    AggressiveScanLogic.option_stasis: has_stasis_rifle,
    AggressiveScanLogic.option_containment: has_containment,
    AggressiveScanLogic.option_either: lambda state, player:
    has_stasis_rifle(state, player) or has_containment(state, player)
}


def set_rules(subnautica_world: "SubnauticaWorld"):
    player = subnautica_world.player
    multiworld = subnautica_world.multiworld

    for loc in location_table.values():
        set_location_rule(multiworld, player, loc)

    if subnautica_world.creatures_to_scan:
        option = multiworld.worlds[player].options.creature_scan_logic

        for creature_name in subnautica_world.creatures_to_scan:
            location = set_creature_rule(multiworld, player, creature_name)
            if creature_name in containment:  # there is no other way, hard-required containment
                add_rule(location, lambda state: has_containment(state, player))
            elif creature_name in aggressive:
                rule = get_aggression_rule(option, creature_name)
                if rule:
                    add_rule(location,
                             lambda state, loc_rule=get_aggression_rule(option, creature_name): loc_rule(state, player))

    # Victory locations
    set_rule(multiworld.get_location("Neptune Launch", player),
             lambda state:
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

    set_rule(multiworld.get_location("Disable Quarantine", player),
             lambda state: get_max_depth(state, player) >= 1444)

    set_rule(multiworld.get_location("Full Infection", player),
             lambda state: get_max_depth(state, player) >= 900)

    room = multiworld.get_location("Aurora Drive Room - Upgrade Console", player)
    set_rule(multiworld.get_location("Repair Aurora Drive", player),
             lambda state: room.can_reach(state))

    multiworld.completion_condition[player] = lambda state: state.has("Victory", player)
