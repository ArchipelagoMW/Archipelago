"""
Defines the rules by which locations can be accessed,
depending on the items received
"""

from typing import FrozenSet, Dict, TYPE_CHECKING

from BaseClasses import Location, CollectionState
from .player_logic import WitnessPlayerLogic
from .Options import get_option_value
from .locations import WitnessPlayerLocations
from . import StaticWitnessLogic, WitnessRegions
from worlds.generic.Rules import set_rule

if TYPE_CHECKING:
    from . import WitnessWorld

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


def _has_lasers(state: CollectionState, amount: int, world: "WitnessWorld", player: int,
                player_logic: WitnessPlayerLogic, locat: WitnessPlayerLocations) -> bool:
    lasers = 0

    for laser_hex in laser_hexes:
        has_laser = _can_solve_panel(state, laser_hex, world, player, player_logic, locat)

        if laser_hex == "0x012FB":
            has_laser = has_laser and state.has("Desert Laser Redirection", player)

        lasers += int(has_laser)

    return lasers >= amount


def _can_solve_panel(state: CollectionState, panel: str, world: "WitnessWorld", player: int,
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


def _can_move_either_direction(state: CollectionState, source: str, target: str, regio: WitnessRegions):
    return (
        any(entrance.can_reach(state) for entrance in regio.created_entrances[(source, target)])
        or
        any(entrance.can_reach(state) for entrance in regio.created_entrances[(target, source)])
    )


def _has_item(state: CollectionState, item: str, world: "WitnessWorld", player: int,
              player_logic: WitnessPlayerLogic, locat: WitnessPlayerLocations):
    if item in StaticWitnessLogic.ALL_REGIONS_BY_NAME:
        return world.regio.region_cache[item].can_reach(state)
    if item == "7 Lasers":
        laser_req = get_option_value(world, "mountain_lasers")
        return _has_lasers(state, laser_req, world, player, player_logic, locat)
    if item == "11 Lasers":
        laser_req = get_option_value(world, "challenge_lasers")
        return _has_lasers(state, laser_req, world, player, player_logic, locat)
    elif item == "PP2 Weirdness":
        hedge_2_access = (
            _can_move_either_direction(state, "Keep 2nd Maze", "Keep", world.regio)
        )

        hedge_3_access = (
            _can_move_either_direction(state, "Keep 3rd Maze", "Keep", world.regio)
            or _can_move_either_direction(state, "Keep 3rd Maze", "Keep 2nd Maze", world.regio)
            and hedge_2_access
        )

        hedge_4_access = (
            _can_move_either_direction(state, "Keep 4th Maze", "Keep", world.regio)
            or _can_move_either_direction(state, "Keep 4th Maze", "Keep 3rd Maze", world.regio)
            and hedge_3_access
        )

        hedge_access = (
            _can_move_either_direction(state, "Keep 4th Maze", "Keep Tower", world.regio)
            and world.regio.region_cache["Keep"].can_reach(state)
            and hedge_4_access
        )

        backwards_to_fourth = (
            world.regio.region_cache["Keep"].can_reach(state)
            and _can_move_either_direction(state, "Keep 4th Pressure Plate", "Keep Tower", world.regio)
            and (
                _can_move_either_direction(state, "Keep", "Keep Tower", world.regio)
                or hedge_access
            )
        )

        shadows_shortcut = (
            world.regio.region_cache["Main Island"].can_reach(state)
            and _can_move_either_direction(state, "Keep 4th Pressure Plate", "Shadows", world.regio)
        )

        backwards_access = (
            _can_move_either_direction(state, "Keep 3rd Pressure Plate", "Keep 4th Pressure Plate", world.regio)
            and (backwards_to_fourth or shadows_shortcut)
        )

        front_access = (
            _can_move_either_direction(state, "Keep 2nd Pressure Plate", "Keep", world.regio)
            and world.regio.region_cache["Keep"].can_reach(state)
        )

        return front_access and backwards_access
    elif item == "Theater to Tunnels":
        direct_access = (
            _can_move_either_direction(state, "Tunnels", "Windmill Interior", world.regio)
            and _can_move_either_direction(state, "Theater", "Windmill Interior", world.regio)
        )

        theater_from_town = (
                _can_move_either_direction(state, "Town", "Windmill Interior", world.regio)
                and _can_move_either_direction(state, "Theater", "Windmill Interior", world.regio)
                or _can_move_either_direction(state, "Town", "Theater", world.regio)
        )

        tunnels_from_town = (
                _can_move_either_direction(state, "Tunnels", "Windmill Interior", world.regio)
                and _can_move_either_direction(state, "Town", "Windmill Interior", world.regio)
                or _can_move_either_direction(state, "Tunnels", "Town", world.regio)
        )

        return direct_access or theater_from_town and tunnels_from_town
    if item in player_logic.EVENT_PANELS:
        return _can_solve_panel(state, item, world, player, player_logic, locat)

    prog_item = StaticWitnessLogic.get_parent_progressive_item(item)
    return state.has(prog_item, player)


def _meets_item_requirements(state: CollectionState, panel: str, world: "WitnessWorld", player: int,
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


def _can_solve_panels(state: CollectionState, panel_hex_to_solve_set: FrozenSet[FrozenSet[str]], world: "WitnessWorld",
                      player: int, player_logic: WitnessPlayerLogic, locat: WitnessPlayerLocations):
    """
    Checks whether a set of panels can be solved.
    """

    return any(
        all(_can_solve_panel(state, panel, world, player, player_logic, locat) for panel in subset)
        for subset in panel_hex_to_solve_set
    )


def make_lambda(check_hex: str, world: "WitnessWorld", player: int,
                player_logic: WitnessPlayerLogic, locat: WitnessPlayerLocations):
    """
    Lambdas are created in a for loop so values need to be captured
    """
    return lambda state: _meets_item_requirements(state, check_hex, world, player, player_logic, locat)


def set_rules(world: "WitnessWorld", player_logic: WitnessPlayerLogic,
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
