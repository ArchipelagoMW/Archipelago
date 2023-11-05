"""
Defines the rules by which locations can be accessed,
depending on the items received
"""

# pylint: disable=E1101

from BaseClasses import MultiWorld
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

    def _witness_has_lasers(self, world, player: int, amount: int) -> bool:
        regular_lasers = not is_option_enabled(world, player, "shuffle_lasers")

        lasers = 0

        place_names = [
            "Symmetry", "Desert", "Town", "Monastery", "Keep",
            "Quarry", "Treehouse", "Jungle", "Bunker", "Swamp", "Shadows"
        ]

        for place in place_names:
            has_laser = self.has(place + " Laser", player)

            has_laser = has_laser or (regular_lasers and self.has(place + " Laser Activation", player))

            if place == "Desert":
                has_laser = has_laser and self.has("Desert Laser Redirection", player)

            lasers += int(has_laser)

        return lasers >= amount

    def _witness_can_solve_panel(self, panel, world, player, player_logic: WitnessPlayerLogic, locat):
        """
        Determines whether a panel can be solved
        """

        panel_obj = StaticWitnessLogic.CHECKS_BY_HEX[panel]
        check_name = panel_obj["checkName"]

        if (check_name + " Solved" in locat.EVENT_LOCATION_TABLE
                and not self.has(player_logic.EVENT_ITEM_PAIRS[check_name + " Solved"], player)):
            return False
        if (check_name + " Solved" not in locat.EVENT_LOCATION_TABLE
                and not self._witness_meets_item_requirements(panel, world, player, player_logic, locat)):
            return False
        return True

    def _witness_meets_item_requirements(self, panel, world, player, player_logic: WitnessPlayerLogic, locat):
        """
        Checks whether item and panel requirements are met for
        a panel
        """

        panel_req = player_logic.REQUIREMENTS_BY_HEX[panel]

        for option in panel_req:
            if len(option) == 0:
                return True

            valid_option = True

            for item in option:
                if item == "7 Lasers":
                    laser_req = get_option_value(world, player, "mountain_lasers")

                    if not self._witness_has_lasers(world, player, laser_req):
                        valid_option = False
                        break
                elif item == "11 Lasers":
                    laser_req = get_option_value(world, player, "challenge_lasers")

                    if not self._witness_has_lasers(world, player, laser_req):
                        valid_option = False
                        break
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

                    if not (front_access and backwards_access):
                        valid_option = False
                        break
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

                    if not (direct_access or theater_from_town and tunnels_from_town):
                        valid_option = False
                        break
                elif item in player_logic.EVENT_PANELS:
                    if not self._witness_can_solve_panel(item, world, player, player_logic, locat):
                        valid_option = False
                        break
                elif not self.has(item, player):
                    # The player doesn't have the item. Check to see if it's part of a progressive item and, if so, the
                    #   player has enough of that.
                    prog_item = StaticWitnessLogic.get_parent_progressive_item(item)
                    if prog_item is item or not self.has(prog_item, player, player_logic.MULTI_AMOUNTS[item]):
                        valid_option = False
                        break

            if valid_option:
                return True

        return False

    def _witness_can_solve_panels(self, panel_hex_to_solve_set, world, player, player_logic: WitnessPlayerLogic, locat):
        """
        Checks whether a set of panels can be solved.
        """

        for option in panel_hex_to_solve_set:
            if len(option) == 0:
                return True

            valid_option = True

            for panel in option:
                if not self._witness_can_solve_panel(panel, world, player, player_logic, locat):
                    valid_option = False
                    break

            if valid_option:
                return True
        return False


def make_lambda(check_hex, world, player, player_logic, locat):
    """
    Lambdas are created in a for loop so values need to be captured
    """
    return lambda state: state._witness_meets_item_requirements(
        check_hex, world, player, player_logic, locat
    )


def set_rules(world: MultiWorld, player: int, player_logic: WitnessPlayerLogic, locat: WitnessPlayerLocations):
    """
    Sets all rules for all locations
    """

    for location in locat.CHECK_LOCATION_TABLE:
        real_location = location

        if location in locat.EVENT_LOCATION_TABLE:
            real_location = location[:-7]

        panel = StaticWitnessLogic.CHECKS_BY_NAME[real_location]
        check_hex = panel["checkHex"]

        rule = make_lambda(check_hex, world, player, player_logic, locat)

        set_rule(world.get_location(location, player), rule)

    world.completion_condition[player] = \
        lambda state: state.has('Victory', player)
