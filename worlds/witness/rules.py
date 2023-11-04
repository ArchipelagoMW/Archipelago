"""
Defines the rules by which locations can be accessed,
depending on the items received
"""

from typing import FrozenSet, Dict

from BaseClasses import Location, CollectionState
from worlds.AutoWorld import World
from .player_logic import WitnessPlayerLogic
from .Options import get_option_value
from .locations import WitnessPlayerLocations
from . import StaticWitnessLogic
from worlds.generic.Rules import set_rule

laser_hexes = [
    "0x028A4",
    "0x00274",
    "0x032F9",
    "0x01539",
    "0x181B3",
    "0x0C2B2",
    "0x00509",
    "0x00BF6",
    "0x014BB",
    "0x012FB",
    "0x17C65",
]


def _has_lasers(state: CollectionState, amount: int, world: World, player: int,
                player_logic: WitnessPlayerLogic, locat: WitnessPlayerLocations) -> bool:
    lasers = 0

    for laser_hex in laser_hexes:
        has_laser = _can_solve_panel(state, laser_hex, world, player, player_logic, locat)

        if laser_hex == "0x012FB":
            has_laser = has_laser and state.has("Desert Laser Redirection", player)

        lasers += int(has_laser)

    return lasers >= amount


def _can_solve_panel(state: CollectionState, panel: str, world: World, player: int,
                     player_logic: WitnessPlayerLogic, locat: WitnessPlayerLocations):
    """
    Determines whether a panel can be solved
    """

    panel_obj = StaticWitnessLogic.ENTITIES_BY_HEX[panel]
    entity_name = panel_obj["checkName"]

    if entity_name + " Solved" in locat.EVENT_LOCATION_TABLE:
        return state.has(player_logic.EVENT_ITEM_PAIRS[entity_name + " Solved"], player)
    else:
        return _meets_item_requirements(state, panel, world, player, player_logic, locat)


def _has_item(state: CollectionState, item: str, world: World, player: int,
              player_logic: WitnessPlayerLogic, locat: WitnessPlayerLocations):
    if item in StaticWitnessLogic.ALL_REGIONS_BY_NAME:
        return state.can_reach(item, "Region", player)
    if item == "7 Lasers":
        laser_req = get_option_value(world, "mountain_lasers")
        return _has_lasers(state, laser_req, world, player, player_logic, locat)
    if item == "11 Lasers":
        laser_req = get_option_value(world, "challenge_lasers")
        return _has_lasers(state, laser_req, world, player, player_logic, locat)
    elif item == "PP2 Weirdness":
        hedge_2_access = (
                state.can_reach("Keep 2nd Maze to Keep", "Entrance", player)
                or state.can_reach("Keep to Keep 2nd Maze", "Entrance", player)
        )

        hedge_3_access = (
                state.can_reach("Keep 3rd Maze to Keep", "Entrance", player)
                or state.can_reach("Keep 2nd Maze to Keep 3rd Maze", "Entrance", player)
                and hedge_2_access
        )

        hedge_4_access = (
                state.can_reach("Keep 4th Maze to Keep", "Entrance", player)
                or state.can_reach("Keep 3rd Maze to Keep 4th Maze", "Entrance", player)
                and hedge_3_access
        )

        hedge_access = (
                state.can_reach("Keep 4th Maze to Keep Tower", "Entrance", player)
                and state.can_reach("Keep", "Region", player)
                and hedge_4_access
        )

        backwards_to_fourth = (
                state.can_reach("Keep", "Region", player)
                and state.can_reach("Keep 4th Pressure Plate to Keep Tower", "Entrance", player)
                and (
                        state.can_reach("Keep Tower to Keep", "Entrance", player)
                        or hedge_access
                )
        )

        shadows_shortcut = (
                state.can_reach("Main Island", "Region", player)
                and state.can_reach("Keep 4th Pressure Plate to Shadows", "Entrance", player)
        )

        backwards_access = (
                state.can_reach("Keep 3rd Pressure Plate to Keep 4th Pressure Plate", "Entrance", player)
                and (backwards_to_fourth or shadows_shortcut)
        )

        front_access = (
                state.can_reach("Keep to Keep 2nd Pressure Plate", 'Entrance', player)
                and state.can_reach("Keep", "Region", player)
        )

        return front_access and backwards_access
    elif item == "Theater to Tunnels":
        direct_access = (
                state.can_reach("Tunnels to Windmill Interior", "Entrance", player)
                and state.can_reach("Windmill Interior to Theater", "Entrance", player)
        )

        theater_from_town = (
                state.can_reach("Town to Windmill Interior", "Entrance", player)
                and state.can_reach("Windmill Interior to Theater", "Entrance", player)
                or state.can_reach("Theater to Town", "Entrance", player)
        )

        tunnels_from_town = (
                state.can_reach("Tunnels to Windmill Interior", "Entrance", player)
                and state.can_reach("Town to Windmill Interior", "Entrance", player)
                or state.can_reach("Tunnels to Town", "Entrance", player)
        )

        return direct_access or theater_from_town and tunnels_from_town
    if item in player_logic.EVENT_PANELS:
        return _can_solve_panel(state, item, world, player, player_logic, locat)

    prog_item = StaticWitnessLogic.get_parent_progressive_item(item)
    return state.has(prog_item, player)


def _meets_item_requirements(state: CollectionState, panel: str, world: World, player: int,
                             player_logic: WitnessPlayerLogic, locat: WitnessPlayerLocations):
    """
    Checks whether item and panel requirements are met for
    a panel
    """

    entity_req = player_logic.REQUIREMENTS_BY_HEX[panel]

    return any(
        all(_has_item(state, item, world, player, player_logic, locat) for item in sub_requirement)
        for sub_requirement in entity_req
    )


def _can_solve_panels(state: CollectionState, panel_hex_to_solve_set: FrozenSet[FrozenSet[str]], world: World,
                      player: int, player_logic: WitnessPlayerLogic, locat: WitnessPlayerLocations):
    """
    Checks whether a set of panels can be solved.
    """

    return any(
        all(_can_solve_panel(state, panel, world, player, player_logic, locat) for panel in subset)
        for subset in panel_hex_to_solve_set
    )


def make_lambda(check_hex: str, world: World, player: int,
                player_logic: WitnessPlayerLogic, locat: WitnessPlayerLocations):
    """
    Lambdas are created in a for loop so values need to be captured
    """
    return lambda state: _meets_item_requirements(state, check_hex, world, player, player_logic, locat)


def set_rules(world: World, player_logic: WitnessPlayerLogic,
              locat: WitnessPlayerLocations, location_cache: Dict[str, Location]):
    """
    Sets all rules for all locations
    """

    for location in locat.CHECK_LOCATION_TABLE:
        real_location = location

        if location in locat.EVENT_LOCATION_TABLE:
            real_location = location[:-7]

        panel = StaticWitnessLogic.ENTITIES_BY_NAME[real_location]
        check_hex = panel["checkHex"]

        rule = make_lambda(check_hex, world, world.player, player_logic, locat)

        location = location_cache[location] if location in location_cache\
            else world.multiworld.get_location(location, world.player)

        set_rule(location, rule)

    world.multiworld.completion_condition[world.player] = \
        lambda state: state.has('Victory', world.player)
