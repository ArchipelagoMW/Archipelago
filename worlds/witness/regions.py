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


def entity_requires_region(entity: str, region: str, player_logic: WitnessPlayerLogic):
    if all(region in requirement for requirement in player_logic.REQUIREMENTS_BY_HEX[entity]):
        return True
    if entity in StaticWitnessLogic.ENTITIES_BY_HEX and StaticWitnessLogic.ENTITIES_BY_HEX[entity]["region"]:
        return StaticWitnessLogic.ENTITIES_BY_HEX[entity]["region"]["name"] == region
    return False


class WitnessRegions:
    """Class that defines Witness Regions"""

    locat = None
    logic = None

    def make_lambda(self, item_requirement: FrozenSet[FrozenSet[str]], world: "WitnessWorld", player: int,
                    player_logic: WitnessPlayerLogic, locat: WitnessPlayerLocations):
        from .rules import _has_item

        """
        Lambdas are made in a for loop, so the values have to be captured
        This function is for that purpose
        """

        return lambda state: any(
            all(_has_item(state, item, world, player, player_logic, locat) for item in sub_requirement)
            for sub_requirement in item_requirement
        )

    def connect_if_possible(self, world: "WitnessWorld", source: str, target: str, player_logic: WitnessPlayerLogic,
                            requirement: FrozenSet[FrozenSet[str]], backwards: bool = False):
        """
        connect two regions and set the corresponding requirement
        """

        # Remove any possibilities where being in the target region would be required anyway.
        real_requirement = frozenset({option for option in requirement if target not in option})

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

        connection.access_rule = self.make_lambda(final_requirement, world, world.player, player_logic, self.locat)

        source_region.exits.append(connection)
        connection.connect(target_region)

        self.created_entrances[(source, target)].append(connection)

        # Register any necessary indirect connections
        mentioned_regions = {
            single_unlock for option in final_requirement for single_unlock in option
            if single_unlock in StaticWitnessLogic.ALL_REGIONS_BY_NAME
        }

        for dependent_region in mentioned_regions:
            world.multiworld.register_indirect_condition(self.region_cache[dependent_region], connection)

    def create_regions(self, world: "WitnessWorld", player_logic: WitnessPlayerLogic):
        """
        Creates all the regions for The Witness
        """
        from . import create_region

        difficulty = world.options.puzzle_randomization

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
                if connection[1] == frozenset({frozenset({"TrueOneWay"})}):
                    self.connect_if_possible(world, region_name, connection[0], player_logic, frozenset({frozenset()}))
                    continue

                self.connect_if_possible(world, region_name, connection[0], player_logic, connection[1])
                self.connect_if_possible(world, connection[0], region_name, player_logic, connection[1])

        return self.location_cache

    def __init__(self, locat: WitnessPlayerLocations, world: "WitnessWorld"):
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
