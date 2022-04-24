"""
Defines Region for The Witness, assigns locations to them,
and connects them with the proper requirements
"""

from BaseClasses import MultiWorld, Entrance
from worlds.witness import ParsedWitnessLogic
from worlds.witness.locations import WitnessLocations


class WitnessRegions:
    """Class that defines Witness Regions"""

    locat = None
    logic = None

    def make_lambda(self, panel_hex_to_solve_set, world, player):
        """
        Lambdas are made in a for loop, so the values have to be captured
        This function is for that purpose
        """

        return lambda state: state.can_solve_panels(
            panel_hex_to_solve_set, world, player, self.logic, self.locat
        )

    def connect(self, world: MultiWorld, player: int, source: str, target: str, panel_hex_to_solve_set=None):
        """
        connect two regions and set the corresponding requirement
        """
        source_region = world.get_region(source, player)
        target_region = world.get_region(target, player)

        connection = Entrance(
            player,
            source + " to " + target + " via " + str(panel_hex_to_solve_set),
            source_region
        )

        connection.access_rule = self.make_lambda(panel_hex_to_solve_set, world,
                                                  player)

        source_region.exits.append(connection)
        connection.connect(target_region)

    def create_regions(self, world, player: int):
        """
        Creates all the regions for The Witness
        """
        from . import create_region

        world.regions += [
            create_region(
                world, player, 'Menu', self.logic,
                self.locat, None, ["The Splashscreen?"]
            ),
        ]

        all_locations = set()

        for region_name, region in self.logic.ALL_REGIONS_BY_NAME.items():
            locations_for_this_region = [
                self.logic.CHECKS_BY_HEX[panel]["checkName"] for panel in region["panels"]
                if self.logic.CHECKS_BY_HEX[panel]["checkName"] in self.locat.CHECK_LOCATION_TABLE
            ]
            locations_for_this_region += [
                self.logic.CHECKS_BY_HEX[panel]["checkName"] + " Solved" for panel in region["panels"]
                if self.logic.CHECKS_BY_HEX[panel]["checkName"] + " Solved" in self.locat.EVENT_LOCATION_TABLE
            ]

            all_locations = all_locations | set(locations_for_this_region)

            world.regions += [create_region(
                world, player, region_name, self.logic, self.locat,
                locations_for_this_region
            )]

        for region_name, region in self.logic.ALL_REGIONS_BY_NAME.items():
            for connection in region["connections"]:
                if connection[0] == "Entry":
                    continue
                self.connect(world, player, region_name,
                             connection[0], connection[1])
                self.connect(world, player, connection[0],
                             region_name, connection[1])

        world.get_entrance("The Splashscreen?", player).connect(
            world.get_region('First Hallway', player)
        )

    def __init__(self, logic: ParsedWitnessLogic, locat: WitnessLocations):
        self.logic = logic
        self.locat = locat
