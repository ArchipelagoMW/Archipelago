"""
Defines the rules by which locations can be accessed,
depending on the items received
"""
from typing import TYPE_CHECKING, FrozenSet, Generator

from BaseClasses import CollectionState, Entrance
from .player_logic import WitnessPlayerLogic
from .locations import WitnessPlayerLocations
from . import StaticWitnessLogic, WitnessRegions
from worlds.generic.Rules import set_rule, CollectionRule

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


def _has_laser(laser_hex: str, world: "WitnessWorld", player: int,
               redirect_required: bool) -> CollectionRule:
    if laser_hex == "0x012FB" and redirect_required:
        return lambda state: (
            _can_solve_panel(laser_hex, world, world.player, world.player_logic, world.locat)(state)
            and state.has("Desert Laser Redirection", player)
        )
    else:
        return _can_solve_panel(laser_hex, world, world.player, world.player_logic, world.locat)


def _has_lasers(amount: int, world: "WitnessWorld", redirect_required: bool) -> CollectionRule:
    laser_lambdas = []

    for laser_hex in laser_hexes:
        has_laser_lambda = _has_laser(laser_hex, world, world.player, redirect_required)

        laser_lambdas.append(has_laser_lambda)

    return lambda state: sum(laser_lambda(state) for laser_lambda in laser_lambdas) >= amount


def _can_solve_panel(panel: str, world: "WitnessWorld", player: int, player_logic: WitnessPlayerLogic,
                     locat: WitnessPlayerLocations) -> CollectionRule:
    """
    Determines whether a panel can be solved
    """

    panel_obj = player_logic.REFERENCE_LOGIC.ENTITIES_BY_HEX[panel]
    entity_name = panel_obj["checkName"]

    if entity_name + " Solved" in locat.EVENT_LOCATION_TABLE:
        return lambda state: state.has(player_logic.EVENT_ITEM_PAIRS[entity_name + " Solved"], player)
    else:
        return make_lambda(panel, world)


def _can_do_expert_pp2(state: CollectionState, world: "WitnessWorld") -> bool:
    player = world.player
    regio = world.regio

    front_access = (
        any(e.can_reach(state) for e in world.regio.two_way_entrance_register["Keep 2nd Pressure Plate", "Keep"])
        and state.can_reach("Keep", "Region", player)
    )

    if not front_access:
        return False

    fourth_to_third = any(e.can_reach(state) for e in world.regio.two_way_entrance_register[
        "Keep 3rd Pressure Plate", "Keep 4th Pressure Plate"
    ])

    if not fourth_to_third:
        return False

    hedge_2_access = (
        any(e.can_reach(state) for e in regio.two_way_entrance_register["Keep 2nd Maze", "Keep"])
    )

    hedge_3_access = (
        any(e.can_reach(state) for e in regio.two_way_entrance_register["Keep 3rd Maze", "Keep"])
        or any(e.can_reach(state) for e in regio.two_way_entrance_register["Keep 3rd Maze", "Keep 2nd Maze"])
        and hedge_2_access
    )

    hedge_4_access = (
        any(e.can_reach(state) for e in regio.two_way_entrance_register["Keep 4th Maze", "Keep"])
        or any(e.can_reach(state) for e in regio.two_way_entrance_register["Keep 4th Maze", "Keep 3rd Maze"])
        and hedge_3_access
    )

    hedge_access = (
        any(e.can_reach(state) for e in regio.two_way_entrance_register["Keep 4th Maze", "Keep Tower"])
        # and state.can_reach("Keep", "Region", player)  # Implicit! :)
        and hedge_4_access
    )

    backwards_to_fourth = (
        any(e.can_reach(state) for e in regio.two_way_entrance_register["Keep 4th Pressure Plate", "Keep Tower"])
        and (
            any(e.can_reach(state) for e in regio.two_way_entrance_register["Keep", "Keep Tower"])
            or hedge_access
        )
        # and state.can_reach("Keep", "Region", player)  # Implicit! :)
    )

    shadows_shortcut = (
        any(e.can_reach(state) for e in regio.two_way_entrance_register["Keep 4th Pressure Plate", "Shadows"])
        # and state.can_reach("Main Island", "Region", player)  # Implicit, watch out if there's ever entrance rando
    )

    return backwards_to_fourth or shadows_shortcut  # PP4 -> PP3 is checked further up as guard condition


def _can_do_theater_to_tunnels(state: CollectionState, world: "WitnessWorld") -> bool:
    direct_access = (
        any(e.can_reach(state) for e in world.regio.two_way_entrance_register["Tunnels", "Windmill Interior"])
        and any(e.can_reach(state) for e in world.regio.two_way_entrance_register["Theater", "Windmill Interior"])
    )

    if direct_access:
        return True

    theater_from_town = (
        any(e.can_reach(state) for e in world.regio.two_way_entrance_register["Town", "Windmill Interior"])
        and any(e.can_reach(state) for e in world.regio.two_way_entrance_register["Theater", "Windmill Interior"])
        or any(e.can_reach(state) for e in world.regio.two_way_entrance_register["Town", "Theater"])
    )

    if not theater_from_town:
        return False

    tunnels_from_town = (
        any(e.can_reach(state) for e in world.regio.two_way_entrance_register["Tunnels", "Windmill Interior"])
        and any(e.can_reach(state) for e in world.regio.two_way_entrance_register["Town", "Windmill Interior"])
        or any(e.can_reach(state) for e in world.regio.two_way_entrance_register["Tunnels", "Town"])
    )

    return tunnels_from_town


def _has_item(item: str, world: "WitnessWorld", player: int,
              player_logic: WitnessPlayerLogic, locat: WitnessPlayerLocations) -> CollectionRule:
    if item in player_logic.REFERENCE_LOGIC.ALL_REGIONS_BY_NAME:
        region = world.get_region(item)
        return region.can_reach
    if item == "7 Lasers":
        laser_req = world.options.mountain_lasers.value
        return _has_lasers(laser_req, world, False)
    if item == "7 Lasers + Redirect":
        laser_req = world.options.mountain_lasers.value
        return _has_lasers(laser_req, world, True)
    if item == "11 Lasers":
        laser_req = world.options.challenge_lasers.value
        return _has_lasers(laser_req, world, False)
    if item == "11 Lasers + Redirect":
        laser_req = world.options.challenge_lasers.value
        return _has_lasers(laser_req, world, True)
    elif item == "PP2 Weirdness":
        return lambda state: _can_do_expert_pp2(state, world)
    elif item == "Theater to Tunnels":
        return lambda state: _can_do_theater_to_tunnels(state, world)
    if item in player_logic.USED_EVENT_NAMES_BY_HEX:
        return _can_solve_panel(item, world, player, player_logic, locat)

    prog_item = StaticWitnessLogic.get_parent_progressive_item(item)
    return lambda state: state.has(prog_item, player, player_logic.MULTI_AMOUNTS[item])


def _meets_item_requirements(requirements: FrozenSet[FrozenSet[str]],
                             world: "WitnessWorld") -> CollectionRule:
    """
    Checks whether item and panel requirements are met for
    a panel
    """

    lambda_conversion = [
        [_has_item(item, world, world.player, world.player_logic, world.locat) for item in subset]
        for subset in requirements
    ]

    return lambda state: any(
        all(condition(state) for condition in sub_requirement)
        for sub_requirement in lambda_conversion
    )


def make_lambda(entity_hex: str, world: "WitnessWorld") -> CollectionRule:
    """
    Lambdas are created in a for loop so values need to be captured
    """
    entity_req = world.player_logic.REQUIREMENTS_BY_HEX[entity_hex]

    return _meets_item_requirements(entity_req, world)


def set_rules(world: "WitnessWorld"):
    """
    Sets all rules for all locations
    """

    for location in world.locat.CHECK_LOCATION_TABLE:
        real_location = location

        if location in world.locat.EVENT_LOCATION_TABLE:
            real_location = location[:-7]

        associated_entity = world.player_logic.REFERENCE_LOGIC.ENTITIES_BY_NAME[real_location]
        entity_hex = associated_entity["entity_hex"]

        rule = make_lambda(entity_hex, world)

        location = world.multiworld.get_location(location, world.player)

        set_rule(location, rule)

    world.multiworld.completion_condition[world.player] = lambda state: state.has('Victory', world.player)
