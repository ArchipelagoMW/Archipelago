"""
Defines Region for The Witness, assigns locations to them,
and connects them with the proper requirements
"""

from BaseClasses import MultiWorld, Entrance
from .static_logic import StaticWitnessLogic
from .Options import get_option_value
from .locations import WitnessPlayerLocations, StaticWitnessLocations
from .player_logic import WitnessPlayerLogic


class WitnessRegions:
    """Class that defines Witness Regions"""

    locat = None
    logic = None

    def make_lambda(self, panel_hex_to_solve_set, world, player, player_logic):
        """
        Lambdas are made in a for loop, so the values have to be captured
        This function is for that purpose
        """

        return lambda state: state._witness_can_solve_panels(
            panel_hex_to_solve_set, world, player, player_logic, self.locat
        )

    def connect(self, world: MultiWorld, player: int, source: str, target: str, player_logic: WitnessPlayerLogic,
                panel_hex_to_solve_set=frozenset({frozenset()}), backwards: bool = False):
        """
        connect two regions and set the corresponding requirement
        """
        source_region = world.get_region(source, player)
        target_region = world.get_region(target, player)

        backwards = " Backwards" if backwards else ""

        connection = Entrance(
            player,
            source + " to " + target + backwards,
            source_region
        )

        connection.access_rule = self.make_lambda(panel_hex_to_solve_set, world, player, player_logic)

        source_region.exits.append(connection)
        connection.connect(target_region)

    def create_regions(self, world, player: int, player_logic: WitnessPlayerLogic):
        """
        Creates all the regions for The Witness
        """
        from . import create_region

        world.regions += [
            create_region(world, player, 'Menu', self.locat, None, ["The Splashscreen?"]),
        ]

        difficulty = get_option_value(world, player, "puzzle_randomization")

        if difficulty == 1:
            reference_logic = StaticWitnessLogic.sigma_expert
        elif difficulty == 0:
            reference_logic = StaticWitnessLogic.sigma_normal
        else:
            reference_logic = StaticWitnessLogic.vanilla

        all_locations = set()

        for region_name, region in reference_logic.ALL_REGIONS_BY_NAME.items():
            locations_for_this_region = [
                reference_logic.CHECKS_BY_HEX[panel]["checkName"] for panel in region["panels"]
                if reference_logic.CHECKS_BY_HEX[panel]["checkName"] in self.locat.CHECK_LOCATION_TABLE
            ]
            locations_for_this_region += [
                StaticWitnessLocations.get_event_name(panel) for panel in region["panels"]
                if StaticWitnessLocations.get_event_name(panel) in self.locat.EVENT_LOCATION_TABLE
            ]

            all_locations = all_locations | set(locations_for_this_region)

            world.regions += [
                create_region(world, player, region_name, self.locat, locations_for_this_region)
            ]

        for region_name, region in reference_logic.ALL_REGIONS_BY_NAME.items():
            for connection in player_logic.CONNECTIONS_BY_REGION_NAME[region_name]:
                if connection[1] == frozenset({frozenset(["TrueOneWay"])}):
                    self.connect(world, player, region_name, connection[0], player_logic, frozenset({frozenset()}))
                    continue

                backwards_connections = set()

                for subset in connection[1]:
                    if all({panel in player_logic.DOOR_ITEMS_BY_ID for panel in subset}):
                        if all({reference_logic.CHECKS_BY_HEX[panel]["id"] is None for panel in subset}):
                            backwards_connections.add(subset)

                if backwards_connections:
                    self.connect(
                        world, player, connection[0], region_name, player_logic,
                        frozenset(backwards_connections), True
                    )

                self.connect(world, player, region_name, connection[0], player_logic, connection[1])

        world.get_entrance("The Splashscreen?", player).connect(
            world.get_region('First Hallway', player)
        )

    def __init__(self, locat: WitnessPlayerLocations):
        self.locat = locat
