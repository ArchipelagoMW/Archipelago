"""
Defines the rules by which locations can be accessed,
depending on the items received
"""

# pylint: disable=E1101

from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule
from .full_logic import ParsedWitnessLogic
from .locations import (
    EVENT_LOCATION_TABLE,
    CHECK_LOCATION_TABLE
)

LOGIC = ParsedWitnessLogic()


class WitnessLogic(LogicMixin):
    """
    Logic macros that get reused
    """
    def _witness_has_lasers(self, player: int, amount: int) -> bool:
        lasers = 0

        lasers += int(self.has("Symmetry Laser Activation", player))
        lasers += int(self.has("Desert Laser Activation", player)
                      and self.has("Desert Laser Redirection", player))
        lasers += int(self.has("Town Laser Activation", player))
        lasers += int(self.has("Monastery Laser Activation", player))
        lasers += int(self.has("Keep Laser Hedges Activation", player)
                      and self.has("Keep Laser Pressure Plates Activation",
                                   player)
                      )
        lasers += int(self.has("Quarry Laser Activation", player))
        lasers += int(self.has("Treehouse Laser Activation", player))
        lasers += int(self.has("Jungle Laser Activation", player))
        lasers += int(self.has("Bunker Laser Activation", player))
        lasers += int(self.has("Swamp Laser Activation", player))
        lasers += int(self.has("Shadows Laser Activation", player))

        return lasers >= amount

    def _can_solve_panel(self, panel, player):
        """
        Determines whether a panel can be solved
        """

        panel_obj = LOGIC.CHECKS_BY_HEX[panel]
        check_name = panel_obj["checkName"]

        if (check_name + " Solved" in EVENT_LOCATION_TABLE
                and not self.has(
                    LOGIC.EVENT_ITEM_PAIRS[check_name + " Solved"],
                    player)):
            return False
        if (panel not in LOGIC.ORIGINAL_EVENT_PANELS
                and not self.can_reach(check_name, "Location", player)):
            return False
        if (panel in LOGIC.ORIGINAL_EVENT_PANELS
                and check_name + " Solved" not in EVENT_LOCATION_TABLE
                and not self._safe_manual_panel_check(panel, player)):

            return False
        return True

    def meets_item_requirements(self, panel, player):
        """
        Checks whether item and panel requirements are met for
        a panel
        """

        panel_obj = LOGIC.CHECKS_BY_HEX[panel]

        for option in panel_obj["requirement"]:
            if len(option) == 0:
                return True

            valid_option = True

            for item in option:
                if item == "7 Lasers":
                    if not self._witness_has_lasers(player, 7):
                        valid_option = False
                        break
                elif item == "11 Lasers":
                    if not self._witness_has_lasers(player, 11):
                        valid_option = False
                        break
                elif item in LOGIC.NECESSARY_EVENT_PANELS:
                    if (LOGIC.CHECKS_BY_HEX[item]["checkName"] + " Solved"
                            in EVENT_LOCATION_TABLE):
                        valid_option = self.has(
                            LOGIC.EVENT_ITEM_NAMES[item], player
                        )
                    else:
                        valid_option = self.can_reach(
                            LOGIC.CHECKS_BY_HEX[item]["checkName"],
                            "Location", player)
                    if not valid_option:
                        break
                elif not self.has(item, player):
                    valid_option = False
                    break

            if valid_option:
                return True

        return False

    def _safe_manual_panel_check(self, panel, player):
        """
        nested can_reach can cause problems, but only if the region being
        checked is neither of the two original regions from the first
        can_reach.
        A nested can_reach is okay here because the only panels this
        function is called on are panels that exist on either side of all
        connections they are required for.
        The spoiler log looks so much nicer this way,
        it gets rid of a bunch of event items, only leaving a couple. :)
        """
        region = LOGIC.CHECKS_BY_HEX[panel]["region"]["name"]

        return (
            self.meets_item_requirements(panel, player)
            and self.can_reach(region, "Region", player)
        )

    def can_solve_panels(self, panel_hex_to_solve_set, player):
        """
        Checks whether a set of panels can be solved.
        """

        for option in panel_hex_to_solve_set:
            if len(option) == 0:
                return True

            valid_option = True

            for panel in option:
                if not self._can_solve_panel(panel, player):
                    valid_option = False
                    break

            if valid_option:
                return True
        return False


def make_lambda(check_hex, player):
    """
    Lambdas are created in a for loop so values need to be captured
    """
    return lambda state: state.meets_item_requirements(check_hex, player)


def set_rules(world: MultiWorld, player: int):
    """
    Sets all rules for all locations
    """

    for location in CHECK_LOCATION_TABLE:
        real_location = location

        if location in EVENT_LOCATION_TABLE:
            real_location = location[:-7]

        panel = LOGIC.CHECKS_BY_NAME[real_location]
        check_hex = panel["checkHex"]

        rule = make_lambda(check_hex, player)

        set_rule(world.get_location(location, player), rule)

    if world.logic[player] != 'nologic':
        world.completion_condition[player] = \
            lambda state: state.has('Victory', player)
