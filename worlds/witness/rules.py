"""
Defines the rules by which locations can be accessed,
depending on the items received
"""

# pylint: disable=E1101
from typing import FrozenSet, Dict

from BaseClasses import Location
from worlds.AutoWorld import World
from .player_logic import WitnessPlayerLogic
from .Options import is_option_enabled, get_option_value
from .locations import WitnessPlayerLocations
from . import StaticWitnessLogic
from worlds.AutoWorld import LogicMixin
from worlds.generic.Rules import set_rule


class WitnessLogic(LogicMixin):
    """
    Logic macros that get reused
    """

    def _witness_has_lasers(self, amount: int, world: World, player: int,
                            player_logic: WitnessPlayerLogic, locat: WitnessPlayerLocations) -> bool:
        lasers = 0

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

        for laser_hex in laser_hexes:
            has_laser = self._witness_can_solve_panel(laser_hex, world, player, player_logic, locat)

            if laser_hex == "0x012FB":
                has_laser = has_laser and self.has("Desert Laser Redirection", player)

            lasers += int(has_laser)

        return lasers >= amount

    def _witness_can_solve_panel(self, panel: str, world: World, player: int,
                                 player_logic: WitnessPlayerLogic, locat: WitnessPlayerLocations):
        """
        Determines whether a panel can be solved
        """

        panel_obj = StaticWitnessLogic.ENTITIES_BY_HEX[panel]
        entity_name = panel_obj["checkName"]

        if entity_name + " Solved" in locat.EVENT_LOCATION_TABLE:
            return self.has(player_logic.EVENT_ITEM_PAIRS[entity_name + " Solved"], player)
        else:
            return self._witness_meets_item_requirements(panel, world, player, player_logic, locat)

    def _witness_has_item(self, item: str, world: World, player: int,
                          player_logic: WitnessPlayerLogic, locat: WitnessPlayerLocations):

            if item in StaticWitnessLogic.ALL_REGIONS_BY_NAME:
                return self.can_reach(item, "Region", player)
            if item == "7 Lasers":
                laser_req = get_option_value(world, "mountain_lasers")
                return self._witness_has_lasers(laser_req, world, player, player_logic, locat)
            if item == "11 Lasers":
                laser_req = get_option_value(world, "challenge_lasers")
                return self._witness_has_lasers(laser_req, world, player, player_logic, locat)
            elif item == "PP2 Weirdness":
                hedge_2_access = (
                        self.can_reach("Keep 2nd Maze to Keep", "Entrance", player)
                        or self.can_reach("Keep to Keep 2nd Maze", "Entrance", player)
                )

                hedge_3_access = (
                        self.can_reach("Keep 3rd Maze to Keep", "Entrance", player)
                        or self.can_reach("Keep 2nd Maze to Keep 3rd Maze", "Entrance", player)
                        and hedge_2_access
                )

                hedge_4_access = (
                        self.can_reach("Keep 4th Maze to Keep", "Entrance", player)
                        or self.can_reach("Keep 3rd Maze to Keep 4th Maze", "Entrance", player)
                        and hedge_3_access
                )

                hedge_access = (
                        self.can_reach("Keep 4th Maze to Keep Tower", "Entrance", player)
                        and self.can_reach("Keep", "Region", player)
                        and hedge_4_access
                )

                backwards_to_fourth = (
                        self.can_reach("Keep", "Region", player)
                        and self.can_reach("Keep 4th Pressure Plate to Keep Tower", "Entrance", player)
                        and (
                                self.can_reach("Keep Tower to Keep", "Entrance", player)
                                or hedge_access
                        )
                )

                shadows_shortcut = (
                        self.can_reach("Main Island", "Region", player)
                        and self.can_reach("Keep 4th Pressure Plate to Shadows", "Entrance", player)
                )

                backwards_access = (
                        self.can_reach("Keep 3rd Pressure Plate to Keep 4th Pressure Plate", "Entrance", player)
                        and (backwards_to_fourth or shadows_shortcut)
                )

                front_access = (
                        self.can_reach("Keep to Keep 2nd Pressure Plate", 'Entrance', player)
                        and self.can_reach("Keep", "Region", player)
                )

                return front_access and backwards_access
            elif item == "Theater to Tunnels":
                direct_access = (
                        self.can_reach("Tunnels to Windmill Interior", "Entrance", player)
                        and self.can_reach("Windmill Interior to Theater", "Entrance", player)
                )

                theater_from_town = (
                        self.can_reach("Town to Windmill Interior", "Entrance", player)
                        and self.can_reach("Windmill Interior to Theater", "Entrance", player)
                        or self.can_reach("Theater to Town", "Entrance", player)
                )

                tunnels_from_town = (
                        self.can_reach("Tunnels to Windmill Interior", "Entrance", player)
                        and self.can_reach("Town to Windmill Interior", "Entrance", player)
                        or self.can_reach("Tunnels to Town", "Entrance", player)
                )

                return direct_access or theater_from_town and tunnels_from_town
            if item in player_logic.EVENT_PANELS:
                return self._witness_can_solve_panel(item, world, player, player_logic, locat)

            prog_item = StaticWitnessLogic.get_parent_progressive_item(item)
            return self.has(prog_item, player)

    def _witness_meets_item_requirements(self, panel: str, world: World, player: int,
                                         player_logic: WitnessPlayerLogic, locat: WitnessPlayerLocations):
        """
        Checks whether item and panel requirements are met for
        a panel
        """

        entity_req = player_logic.REQUIREMENTS_BY_HEX[panel]

        return any(
            all(self._witness_has_item(item, world, player, player_logic, locat)
            for item in sub_requirement) for sub_requirement in entity_req
        )

    def _witness_can_solve_panels(self, panel_hex_to_solve_set: FrozenSet[FrozenSet[str]], world: World, player: int,
                                  player_logic: WitnessPlayerLogic, locat: WitnessPlayerLocations):
        """
        Checks whether a set of panels can be solved.
        """

        return any(
            all(self._witness_can_solve_panel(panel, world, player, player_logic, locat) for panel in subset)
            for subset in panel_hex_to_solve_set
        )


def make_lambda(check_hex: str, world: World, player: int,
                player_logic: WitnessPlayerLogic, locat: WitnessPlayerLocations):
    """
    Lambdas are created in a for loop so values need to be captured
    """
    return lambda state: state._witness_meets_item_requirements(
        check_hex, world, player, player_logic, locat
    )


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
