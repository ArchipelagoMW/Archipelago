"""
Defines Region for The Witness, assigns locations to them,
and connects them with the proper requirements
"""
from collections import defaultdict
from typing import TYPE_CHECKING, Dict, List, Set, Tuple

from BaseClasses import Entrance, Region

from worlds.generic.Rules import CollectionRule

from .data import static_logic as static_witness_logic
from .data.utils import WitnessRule, optimize_witness_rule
from .locations import WitnessPlayerLocations, static_witness_locations
from .player_logic import WitnessPlayerLogic

if TYPE_CHECKING:
    from . import WitnessWorld


class WitnessPlayerRegions:
    """Class that defines Witness Regions"""

    player_locations = None
    logic = None

    @staticmethod
    def make_lambda(item_requirement: WitnessRule, world: "WitnessWorld") -> CollectionRule:
        from .rules import _meets_item_requirements

        """
        Lambdas are made in a for loop, so the values have to be captured
        This function is for that purpose
        """

        return _meets_item_requirements(item_requirement, world)

    def connect_if_possible(self, world: "WitnessWorld", source: str, target: str, req: WitnessRule,
                            regions_by_name: Dict[str, Region]):
        """
        connect two regions and set the corresponding requirement
        """

        # Remove any possibilities where being in the target region would be required anyway.
        real_requirement = frozenset({option for option in req if target not in option})

        # Dissolve any "True" or "TrueOneWay"
        real_requirement = frozenset({option - {"True", "TrueOneWay"} for option in real_requirement})

        # If there is no way to actually use this connection, don't even bother making it.
        if not real_requirement:
            return

        # We don't need to check for the accessibility of the source region.
        final_requirement = frozenset({option - frozenset({source}) for option in real_requirement})
        final_requirement = optimize_witness_rule(final_requirement)

        source_region = regions_by_name[source]
        target_region = regions_by_name[target]

        connection_name = source + " to " + target

        connection = Entrance(
            world.player,
            connection_name,
            source_region
        )

        connection.access_rule = self.make_lambda(final_requirement, world)

        source_region.exits.append(connection)
        connection.connect(target_region)

        self.two_way_entrance_register[source, target].append(connection)
        self.two_way_entrance_register[target, source].append(connection)

        # Register any necessary indirect connections
        mentioned_regions = {
            single_unlock for option in final_requirement for single_unlock in option
            if single_unlock in self.reference_logic.ALL_REGIONS_BY_NAME
        }

        for dependent_region in mentioned_regions:
            world.multiworld.register_indirect_condition(regions_by_name[dependent_region], connection)

    def create_regions(self, world: "WitnessWorld", player_logic: WitnessPlayerLogic) -> None:
        """
        Creates all the regions for The Witness
        """
        from . import create_region

        all_locations = set()
        regions_by_name = dict()

        regions_to_create = {
            k: v for k, v in self.reference_logic.ALL_REGIONS_BY_NAME.items()
            if k not in player_logic.UNREACHABLE_REGIONS
        }

        for region_name, region in regions_to_create.items():
            locations_for_this_region = [
                self.reference_logic.ENTITIES_BY_HEX[panel]["checkName"] for panel in region["entities"]
                if self.reference_logic.ENTITIES_BY_HEX[panel]["checkName"]
                in self.player_locations.CHECK_LOCATION_TABLE
            ]
            locations_for_this_region += [
                static_witness_locations.get_event_name(panel) for panel in region["entities"]
                if static_witness_locations.get_event_name(panel) in self.player_locations.EVENT_LOCATION_TABLE
            ]

            all_locations = all_locations | set(locations_for_this_region)

            new_region = create_region(world, region_name, self.player_locations, locations_for_this_region)

            regions_by_name[region_name] = new_region

        self.created_region_names = set(regions_by_name)

        world.multiworld.regions += regions_by_name.values()

        for region_name, region in regions_to_create.items():
            for connection in player_logic.CONNECTIONS_BY_REGION_NAME[region_name]:
                self.connect_if_possible(world, region_name, connection[0], connection[1], regions_by_name)

    def __init__(self, player_locations: WitnessPlayerLocations, world: "WitnessWorld") -> None:
        difficulty = world.options.puzzle_randomization

        if difficulty == "sigma_normal":
            self.reference_logic = static_witness_logic.sigma_normal
        elif difficulty == "sigma_expert":
            self.reference_logic = static_witness_logic.sigma_expert
        elif difficulty == "none":
            self.reference_logic = static_witness_logic.vanilla

        self.player_locations = player_locations
        self.two_way_entrance_register: Dict[Tuple[str, str], List[Entrance]] = defaultdict(lambda: [])
        self.created_region_names: Set[str] = set()
