from typing import TYPE_CHECKING, Dict, Callable, Optional

from worlds.generic.Rules import set_rule, add_rule
from .locations import location_table, LocationDict
from .creatures import all_creatures, aggressive, suffix, hatchable, containment
from .options import AggressiveScanLogic, SubnauticaOptions
import math

if TYPE_CHECKING:
    from . import SubnauticaWorld
    from BaseClasses import CollectionState, Location


def has_seaglide(state: "CollectionState", player: int) -> bool:
    return state.has("Seaglide Fragment", player, 2)


def has_exterior_growbed(state: "CollectionState", player: int) -> bool:
    return state.has("Exterior Growbed", player, 1)


def has_modification_station(state: "CollectionState", player: int) -> bool:
    return state.has("Modification Station Fragment", player, 3)


def has_mobile_vehicle_bay(state: "CollectionState", player: int) -> bool:
    return state.has("Mobile Vehicle Bay Fragment", player, 3)


def has_moonpool(state: "CollectionState", player: int) -> bool:
    return state.has("Moonpool Fragment", player, 2)


def has_vehicle_upgrade_console(state: "CollectionState", player: int) -> bool:
    return state.has("Vehicle Upgrade Console", player) and \
           has_moonpool(state, player)


def has_seamoth(state: "CollectionState", player: int, options: SubnauticaOptions) -> bool:
    if options.include_seamoth > 0:
        return False
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


def has_nuclear_reactor(state: "CollectionState", player: int) -> bool:
    return state.has("Nuclear Reactor Fragment", player, 3) and has_utility_room(state, player)


def has_bioreactor(state: "CollectionState", player: int) -> bool:
    return state.has("Bioreactor Fragment", player, 2) and has_utility_room(state, player)


def has_thermal_plant(state: "CollectionState", player: int) -> bool:
    return state.has("Thermal Plant Fragment", player, 2) and state.has("Power Transmitter Fragment", player, 1)


def has_cyclops(state: "CollectionState", player: int, options: SubnauticaOptions, shield_check: bool = False) -> bool:
    if options.include_cyclops > 0 and not shield_check:
        return False
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


def has_prawn(state: "CollectionState", player: int, options: SubnauticaOptions) -> bool:
    if options.include_prawn > 0:
        return False
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


def has_cyclops_shield(state: "CollectionState", player: int, options: SubnauticaOptions) -> bool:
    # Cyclops in game
    if options.include_cyclops < 2:
        return has_cyclops(state, player, options, True) and \
            state.has("Cyclops Shield Generator", player)

    # Cyclops not in game
    return has_moonpool(state, player) and \
        has_vehicle_upgrade_console(state, player) and \
        state.has("Cyclops Shield Generator", player)


def has_ultra_high_capacity_tank(state: "CollectionState", player: int) -> bool:
    return has_modification_station(state, player) and state.has("Ultra High Capacity Tank", player)


def has_lightweight_high_capacity_tank(state: "CollectionState", player: int) -> bool:
    return has_modification_station(state, player) and state.has("Lightweight High Capacity Tank", player)


def has_ultra_glide_fins(state: "CollectionState", player: int) -> bool:
    return has_modification_station(state, player) and state.has("Ultra Glide Fins", player)


def get_max_swim_depth(state: "CollectionState", player: int, options: SubnauticaOptions, \
        theoretical: bool = False) -> int:
    depth: int = options.swim_rule.base_depth

    additional_depth: int = 0
    if options.swim_rule.consider_items:
        if theoretical:
            additional_depth = 350
        else:
            additional_depth = get_additional_item_depth(state, player, options)

    return depth + additional_depth


# Swim depth rules:
# Rebreather, high capacity tank and fins are available from the start.
# All tests for those were done without inventory for light weight.
# Fins and ultra Fins are better than charge fins, so we ignore charge fins.

# swim speeds: https://subnautica.fandom.com/wiki/Swimming_Speed
def get_additional_item_depth(state: "CollectionState", player: int, options: SubnauticaOptions) -> int:
    depth: int = 0

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


# Basically, if you have neither the prawn or cyclops in logic, then you're stuck
# making bases til you hit depth; max needed depth is ~1444, so anything that gets
# us to 1500 is fine. This is the slow way; better players will use cheats
# such as multiple tanks and bladderfish but logic can't account for that.
def get_hardcore_item_depth(state: "CollectionState", player: int, prev_depth: int) -> int:
    depth: int = 0
    if has_exterior_growbed(state, player):
        depth += 200

    nuclear_depth = bio_depth = thermal_depth = 0

    # have to be able to get to uraninite for nuclear reactor to be useful
    if (prev_depth + depth) >= 250 and has_nuclear_reactor(state, player):
        nuclear_depth = 1500

    if has_bioreactor(state, player):
        bio_depth = 1500

    if has_thermal_plant(state, player):
        thermal_depth = 1500

    return depth + max(nuclear_depth, bio_depth, thermal_depth)


def get_seamoth_max_depth(state: "CollectionState", player: int, options: SubnauticaOptions):
    if not has_seamoth(state, player, options):
        return 0

    if has_seamoth_depth_module_mk3(state, player):
        return 900
    if has_seamoth_depth_module_mk2(state, player):  # Will never be the case, 3 is craftable
        return 500
    if has_seamoth_depth_module_mk1(state, player):
        return 300

    return 200


def get_cyclops_max_depth(state: "CollectionState", player, options: SubnauticaOptions):
    if not has_cyclops(state, player, options):
        return 0

    if has_cyclops_depth_module_mk3(state, player):
        return 1700
    if has_cyclops_depth_module_mk2(state, player):  # Will never be the case, 3 is craftable
        return 1300
    if has_cyclops_depth_module_mk1(state, player):
        return 900

    return 500


def get_prawn_max_depth(state: "CollectionState", player, options: SubnauticaOptions):
    if not has_prawn(state, player, options):
        return 0

    if has_prawn_depth_module_mk2(state, player):
        return 1700
    if has_prawn_depth_module_mk1(state, player):
        return 1300

    return 900


def get_max_depth(state: "CollectionState", player: int, options: SubnauticaOptions):
    max_depth: int = get_max_swim_depth(state, player, options)

    # if include_seamoth is 1 or 2, it doesn't count anyway
    # We have to be able to get to the last check between seamoth depth and swimming expertise
    seamoth_can_make_it: bool = False
    if options.include_seamoth == 0 and get_max_swim_depth(state, player, options, "theoretical") + 900 > 1443:
        seamoth_can_make_it = True

    # If we don't have a vehicle that can go to 1444m depth, then we have to use "hardcore" methods
    # PreSeaglide Distance, laser cutter, and radiation will still gate some checks, so it's not completely open
    if seamoth_can_make_it is False \
            and options.include_prawn > 0 \
            and options.include_cyclops > 0:
        return max_depth + get_hardcore_item_depth(state, player, max_depth)

    return max_depth + max(
        get_seamoth_max_depth(state, player, options),
        get_cyclops_max_depth(state, player, options),
        get_prawn_max_depth(state, player, options)
    )


def is_radiated(x: float, y: float, z: float) -> bool:
    aurora_dist = math.sqrt((x - 1038.0) ** 2 + y ** 2 + (z - -163.1) ** 2)
    return aurora_dist < 950


def can_access_location(state: "CollectionState", player: int, options: SubnauticaOptions, loc: LocationDict) -> bool:
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
    return get_max_depth(state, player, options) >= depth


def set_location_rule(world, player: int, options: SubnauticaOptions, loc: LocationDict):
    set_rule(world.get_location(loc["name"], player), lambda state: can_access_location(state, player, options, loc))


def can_scan_creature(state: "CollectionState", player: int, options: SubnauticaOptions, creature: str) -> bool:
    if not has_seaglide(state, player):
        return False
    return get_max_depth(state, player, options) >= all_creatures[creature]


def set_creature_rule(world, options: SubnauticaOptions, player: int, creature_name: str) -> "Location":
    location = world.get_location(creature_name + suffix, player)
    set_rule(location,
             lambda state: can_scan_creature(state, player, options, creature_name))
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
        set_location_rule(multiworld, player, subnautica_world.options, loc)

    if subnautica_world.creatures_to_scan:
        option = subnautica_world.options.creature_scan_logic

        for creature_name in subnautica_world.creatures_to_scan:
            location = set_creature_rule(multiworld, subnautica_world.options, player, creature_name)
            if creature_name in containment:  # there is no other way, hard-required containment
                add_rule(location, lambda state: has_containment(state, player))
            elif creature_name in aggressive:
                rule = get_aggression_rule(option, creature_name)
                if rule:
                    add_rule(location,
                             lambda state, loc_rule=get_aggression_rule(option, creature_name): loc_rule(state, player))

    # Victory locations
    if multiworld.goal[player].get_event_name() == "Neptune Launch":
        set_rule(multiworld.get_location("Neptune Launch", player),
                 lambda state:
                 get_max_depth(state, player, subnautica_world.options) >= 1444 and
                 has_mobile_vehicle_bay(state, player) and
                 state.has("Neptune Launch Platform", player) and
                 state.has("Neptune Gantry", player) and
                 state.has("Neptune Boosters", player) and
                 state.has("Neptune Fuel Reserve", player) and
                 state.has("Neptune Cockpit", player) and
                 state.has("Ion Power Cell", player) and
                 state.has("Ion Battery", player) and
                 has_cyclops_shield(state, player, subnautica_world.options))

    if multiworld.goal[player].get_event_name() == "Disable Quarantine":
        set_rule(multiworld.get_location("Disable Quarantine", player),
                 lambda state: get_max_depth(state, player, subnautica_world.options) >= 1444)

    if multiworld.goal[player].get_event_name() == "Full Infection":
        set_rule(multiworld.get_location("Full Infection", player),
                 lambda state: get_max_depth(state, player, subnautica_world.options) >= 900)

    if multiworld.goal[player].get_event_name() == "Repair Aurora Drive":
        room = multiworld.get_location("Aurora Drive Room - Upgrade Console", player)
        set_rule(multiworld.get_location("Repair Aurora Drive", player),
                 lambda state: room.can_reach(state))

    multiworld.completion_condition[player] = lambda state: state.has("Victory", player)
