"""
Defines Region for The Witness, assigns locations to them,
and connects them with the proper requirements
"""
from logging import warning
from typing import FrozenSet, Dict, Tuple, List, TYPE_CHECKING

from BaseClasses import Entrance, Region, Location
from .static_logic import StaticWitnessLogic
from Utils import KeyedDefaultDict
from .locations import WitnessPlayerLocations, StaticWitnessLocations
from .player_logic import WitnessPlayerLogic

if TYPE_CHECKING:
    from . import WitnessWorld


class WitnessRegions:
    """Class that defines Witness Regions"""

    locat = None
    logic = None

    def make_lambda(self, item_requirement: FrozenSet[FrozenSet[str]], world: "WitnessWorld"):
        from .rules import _meets_item_requirements

        """
        Lambdas are made in a for loop, so the values have to be captured
        This function is for that purpose
        """

        return _meets_item_requirements(item_requirement, world)

    def connect_if_possible(self, world: "WitnessWorld", source: str, target: str,
                            requirement: FrozenSet[FrozenSet[str]], backwards: bool = False):
        """
        connect two regions and set the corresponding requirement
        """

        # Remove any possibilities where being in the target region would be required anyway.
        real_requirement = frozenset({option for option in requirement if target not in option})

        # There are some connections that should only be done one way. If this is a backwards connection, check for that
        if backwards:
            real_requirement = frozenset({option for option in real_requirement if "TrueOneWay" not in option})

        # Dissolve any "True" or "TrueOneWay"
        real_requirement = frozenset({option - {"True", "TrueOneWay"} for option in real_requirement})

        # If there is no way to actually use this connection, don't even bother making it.
        if not real_requirement:
            return

        # We don't need to check for the accessibility of the source region.
        final_requirement = frozenset({option - frozenset({source}) for option in real_requirement})

        source_region = self.region_cache[source]
        target_region = self.region_cache[target]

        backwards = " Backwards" if backwards else ""
        connection_name = source + " to " + target + backwards

        connection = Entrance(
            world.player,
            connection_name,
            source_region
        )

        connection.access_rule = self.make_lambda(final_requirement, world)

        source_region.exits.append(connection)
        connection.connect(target_region)

        self.created_entrances[(source, target)].append(connection)

        if connection_name in self.entrance_cache:
            warning(f"{connection_name} already present in entrance cache!")
        self.entrance_cache[connection_name] = connection

        # Register any necessary indirect connections
        mentioned_regions = {
            single_unlock for option in final_requirement for single_unlock in option
            if single_unlock in self.reference_logic.ALL_REGIONS_BY_NAME
        }

        for dependent_region in mentioned_regions:
            world.multiworld.register_indirect_condition(self.region_cache[dependent_region], connection)

    def create_regions(self, world: "WitnessWorld", player_logic: WitnessPlayerLogic):
        """
        Creates all the regions for The Witness
        """
        from . import create_region

        all_locations = set()

        for region_name, region in self.reference_logic.ALL_REGIONS_BY_NAME.items():
            locations_for_this_region = [
                self.reference_logic.ENTITIES_BY_HEX[panel]["checkName"] for panel in region["panels"]
                if self.reference_logic.ENTITIES_BY_HEX[panel]["checkName"] in self.locat.CHECK_LOCATION_TABLE
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

        for region_name, region in self.reference_logic.ALL_REGIONS_BY_NAME.items():
            for connection in player_logic.CONNECTIONS_BY_REGION_NAME[region_name]:
                self.connect_if_possible(world, region_name, connection[0], connection[1])
                self.connect_if_possible(world, connection[0], region_name, connection[1], backwards=True)

        return self.location_cache

    def __init__(self, locat: WitnessPlayerLocations, world: "WitnessWorld"):
        difficulty = world.options.puzzle_randomization.value

        if difficulty == 0:
            self.reference_logic = StaticWitnessLogic.sigma_normal
        elif difficulty == 1:
            self.reference_logic = StaticWitnessLogic.sigma_expert
        elif difficulty == 2:
            self.reference_logic = StaticWitnessLogic.vanilla

        self.locat = locat
        player_name = world.multiworld.get_player_name(world.player)

        self.created_entrances: Dict[Tuple[str, str], List[Entrance]] = KeyedDefaultDict(lambda _: [])

        def get_uncached_entrance(key: str) -> Entrance:
            warning(f"Entrance \"{key}\" was not cached in {player_name}'s Witness world. Violet pls fix this.")
            return world.multiworld.get_entrance(key, world.player)

        def get_uncached_region(key: str) -> Region:
            warning(f"Region \"{key}\" was not cached in {player_name}'s Witness world. Violet pls fix this.")
            return world.multiworld.get_region(key, world.player)

        def get_uncached_location(key: str) -> Location:
            warning(f"Location \"{key}\" was not cached in {player_name}'s Witness world. Violet pls fix this.")
            return world.multiworld.get_location(key, world.player)

        self.region_cache: Dict[str, Region] = KeyedDefaultDict(get_uncached_region)
        self.location_cache: Dict[str, Location] = KeyedDefaultDict(get_uncached_location)
        self.entrance_cache: Dict[str, Entrance] = KeyedDefaultDict(get_uncached_entrance)
