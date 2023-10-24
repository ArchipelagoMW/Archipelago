"""
Defines Region for The Witness, assigns locations to them,
and connects them with the proper requirements
"""
from typing import FrozenSet, Dict

from BaseClasses import Entrance, Region, Location
from worlds.AutoWorld import World
from .static_logic import StaticWitnessLogic
from .Options import get_option_value
from .locations import WitnessPlayerLocations, StaticWitnessLocations
from .player_logic import WitnessPlayerLogic


class WitnessRegions:
    """Class that defines Witness Regions"""

    locat = None
    logic = None

    def make_lambda(self, panel_hex_to_solve_set: FrozenSet[FrozenSet[str]], world: World, player: int,
                    player_logic: WitnessPlayerLogic):
        """
        Lambdas are made in a for loop, so the values have to be captured
        This function is for that purpose
        """

        return lambda state: state._witness_can_solve_panels(
            panel_hex_to_solve_set, world, player, player_logic, self.locat
        )

    def connect(self, world: World, source: str, target: str, player_logic: WitnessPlayerLogic,
                panel_hex_to_solve_set: FrozenSet[FrozenSet[str]] = frozenset({frozenset()}), backwards: bool = False):
        """
        connect two regions and set the corresponding requirement
        """
        source_region = self.region_cache[source]
        target_region = self.region_cache[target]

        backwards = " Backwards" if backwards else ""

        connection = Entrance(
            world.player,
            source + " to " + target + backwards,
            source_region
        )

        connection.access_rule = self.make_lambda(panel_hex_to_solve_set, world, world.player, player_logic)

        source_region.exits.append(connection)
        connection.connect(target_region)

    def create_regions(self, world: World, player_logic: WitnessPlayerLogic):
        """
        Creates all the regions for The Witness
        """
        from . import create_region

        difficulty = get_option_value(world, "puzzle_randomization")

        if difficulty == 1:
            reference_logic = StaticWitnessLogic.sigma_expert
        elif difficulty == 0:
            reference_logic = StaticWitnessLogic.sigma_normal
        else:
            reference_logic = StaticWitnessLogic.vanilla

        all_locations = set()

        for region_name, region in reference_logic.ALL_REGIONS_BY_NAME.items():
            locations_for_this_region = [
                reference_logic.ENTITIES_BY_HEX[panel]["checkName"] for panel in region["panels"]
                if reference_logic.ENTITIES_BY_HEX[panel]["checkName"] in self.locat.CHECK_LOCATION_TABLE
            ]
            locations_for_this_region += [
                StaticWitnessLocations.get_event_name(panel) for panel in region["panels"]
                if StaticWitnessLocations.get_event_name(panel) in self.locat.EVENT_LOCATION_TABLE
            ]

            all_locations = all_locations | set(locations_for_this_region)

            new_region = create_region(world, region_name, self.locat, locations_for_this_region)
            self.region_cache[region_name] = new_region
            self.location_cache.update({location.name: location for location in new_region.locations})

            world.multiworld.regions.append(new_region)

        for region_name, region in reference_logic.ALL_REGIONS_BY_NAME.items():
            for connection in player_logic.CONNECTIONS_BY_REGION_NAME[region_name]:
                if connection[1] == frozenset({frozenset(["TrueOneWay"])}):
                    self.connect(world, region_name, connection[0], player_logic, frozenset({frozenset()}))
                    continue

                backwards_connections = set()

                for subset in connection[1]:
                    if all({panel in player_logic.DOOR_ITEMS_BY_ID for panel in subset}):
                        if all({reference_logic.ENTITIES_BY_HEX[panel]["id"] is None for panel in subset}):
                            backwards_connections.add(subset)

                if backwards_connections:
                    self.connect(
                        world, connection[0], region_name, player_logic,
                        frozenset(backwards_connections), True
                    )

                self.connect(world, region_name, connection[0], player_logic, connection[1])

        return self.location_cache

    def __init__(self, locat: WitnessPlayerLocations):
        self.locat = locat
        self.region_cache: Dict[str, Region] = dict()
        self.location_cache: Dict[str, Location] = dict()
