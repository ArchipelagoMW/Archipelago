from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region
# NOTE: Only include when testing!
# from venv import logger

from .logics import possible_regions

if TYPE_CHECKING:
    from .world import EVNWorld

# A region is a container for locations ("checks"), which connects to other regions via "Entrance" objects.
# Every location must be inside a region, and you must have at least one region.
# This is why we create regions first, and then later we create the locations (in locations.py).

def create_and_connect_regions(world: EVNWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: EVNWorld) -> None:
    # Let's put all these regions in a list.
    regions = []

    # As our regions, and which regions we'll be using this run, are defined in logics already
    # We just loop through and create them based on the logic data.
    # AP region doesn't match our region definition - so we just need to know the name and which
    # regions to create an AP counterpart for.
    chosen_route = world.get_chosen_string()
    for regionid in chosen_route["regions"]:
        # Creating a region is as simple as calling the constructor of the Region class.
        regions.append(Region(possible_regions[regionid]["name"], world.player, world.multiworld))
        #logger.info(f"added region {possible_regions[regionid]["name"]}")

    # If we wanted to filter regions based on user options from options.py, do that here

    # We now need to add these regions to multiworld.regions so that AP knows about their existence.
    world.multiworld.regions += regions


def connect_regions(world: EVNWorld) -> None:
    # We have regions now, but still need to connect them to each other.

    chosen_route = world.get_chosen_string()
    #logger.info(f"story routes: {chosen_route["region_connections"]}")
    for fromid, targets in chosen_route["region_connections"].items():
        # We can fetch a region created in create_all_regions() by name via the get_region function
        from_r_name = possible_regions[fromid]["name"]
        from_region = world.get_region(from_r_name)
        # A region can connect to multiple other regions, so we'll loop through its described connections to actually create them
        for toid in targets:
            to_r_name = possible_regions[toid]["name"]
            # We can then connect the fetched region to the next region via the connect function
            from_region.connect(world.get_region(possible_regions[toid]["name"]), f"{from_r_name} to {to_r_name}")
            #logger.info(f"connected {possible_regions[fromid]["name"]} to {possible_regions[toid]["name"]}")
