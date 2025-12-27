from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from BaseClasses import Entrance, Region, CollectionState

if TYPE_CHECKING:
    from .world import PSOWorld

# A region is a container for locations ("checks"), which connects to other regions via "Entrance" objects.
# Many games will model their Regions after physical in-game places, but you can also have more abstract regions.
# For a location to be in logic, its containing region must be reachable.
# The Entrances connecting regions can have rules - more on that in rules.py.
# This makes regions especially useful for traversal logic ("Can the player reach this part of the map?")

# Every location must be inside a region, and you must have at least one region.
# This is why we create regions first, and then later we create the locations (in locations.py).

def playerHas(condition: str) -> Callable[[CollectionState], bool]:
    return lambda state: state.has(condition)

def create_and_connect_regions(world: PSOWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: PSOWorld) -> None:
    # Starting with just a barebones list of the main areas in Episode 1
    region_names = [
        "Pioneer 2",
        "Forest 1",
        "Forest 2",
        "Forest Boss",
        "Caves 1",
        "Caves 2",
        "Caves 3",
        "Caves Boss",
        "Mines 1",
        "Mines 2",
        "Mines Boss",
        "Ruins Entrance",
        "Ruins 1",
        "Ruins 2",
        "Ruins 3",
        "Final Boss"
    ]

    for region_name in region_names:
        region = Region(region_name, world.player, world.multiworld)
        world.multiworld.regions.append(region)

    # Some regions may only exist if the player enables certain options.
    # In our case, the Hammer locks the top middle chest in its own room if the hammer option is enabled.
    # if world.options.hammer:
    #    top_middle_room = Region("Top Middle Room", world.player, world.multiworld)
    #    world.multiworld.regions.append(top_middle_room)

    # We now need to add these regions to multiworld.regions so that AP knows about their existence.
    # world.multiworld.regions += regions


def connect_regions(world: PSOWorld) -> None:
    pioneer_2 = world.get_region("Pioneer 2")
    forest_1 = world.get_region("Forest 1")
    forest_2 = world.get_region("Forest 2")
    forest_boss = world.get_region("Forest Boss")
    caves_1 = world.get_region("Caves 1")
    caves_2 = world.get_region("Caves 2")
    caves_3 = world.get_region("Caves 3")
    caves_boss = world.get_region("Caves Boss")
    mines_1 = world.get_region("Mines 1")
    mines_2 = world.get_region("Mines 2")
    mines_boss = world.get_region("Mines Boss")
    ruins_entrance = world.get_region("Ruins Entrance")
    ruins_1 = world.get_region("Ruins 1")
    ruins_2 = world.get_region("Ruins 2")
    ruins_3 = world.get_region("Ruins 3")
    dark_falz = world.get_region("Dark Falz")

    # Pioneer 2 Entrances
    pioneer_2.connect(forest_1, "Pioneer 2 to Forest 1", playerHas("Unlocked Forest 1"))
    pioneer_2.connect(forest_2, "Pioneer 2 to Forest 2", playerHas("Unlocked Forest 2"))
    pioneer_2.connect(caves_1, "Pioneer 2 to Caves 1", playerHas("Unlocked Caves 1"))
    pioneer_2.connect(caves_2, "Pioneer 2 to Caves 2", playerHas("Unlocked Caves 2"))
    pioneer_2.connect(caves_3, "Pioneer 2 to Caves 3", playerHas("Unlocked Caves 3"))
    pioneer_2.connect(mines_1, "Pioneer 2 to Mines 1", playerHas("Unlocked Mines 1"))
    pioneer_2.connect(mines_2, "Pioneer 2 to Mines 2", playerHas("Unlocked Mines 2"))
    pioneer_2.connect(ruins_1, "Pioneer 2 to Ruins 1", playerHas("Unlocked Ruin 1"))
    pioneer_2.connect(ruins_2, "Pioneer 2 to Ruins 2", playerHas("Unlocked Ruins 2"))
    pioneer_2.connect(ruins_3, "Pioneer 2 to Ruins 3", playerHas("Unlocked Ruins 3"))

    # Level Entrances
    # Technically, there are teleporters to return to Pioneer 2 in some areas, but Archipelago assumes
    # we can always return, so we leave those out.
    # This will also have to be reevaluated if / when we have non-linear progression.
    forest_1.connect(forest_2, "Forest 1 to Forest 2", playerHas("Unlocked Forest 2"))
    forest_2.connect(forest_boss, "Forest 2 to Forest Boss", playerHas("Unlocked Forest Boss"))
    caves_1.connect(caves_2, "Caves 1 to Caves 2", playerHas("Unlocked Caves 2"))
    caves_2.connect(caves_3, "Caves 2 to Caves 3", playerHas("Unlocked Caves 3"))
    caves_3.connect(caves_boss, "Caves 3 to Caves Boss", playerHas("Unlocked Caves Boss"))
    mines_1.connect(mines_2, "Mines 1 to Mines 2", playerHas("Unlocked Mines 2"))
    mines_2.connect(mines_boss, "Mines 2 to Mines Boss", playerHas("Unlocked Mines Boss"))
    mines_boss.connect(ruins_entrance, "Mines Boss to Ruins Entrance", playerHas("Unlocked Ruins Entrance"))
    ruins_entrance.connect(ruins_1, "Ruins Entrance to Ruins 1", playerHas("Activated All Pillars"))
    ruins_1.connect(ruins_2, "Ruins 1 to Ruins 2", playerHas("Unlocked Ruins 2"))
    ruins_2.connect(ruins_3, "Ruins 2 to Ruins 3", playerHas("Unlocked Ruins 3"))
    ruins_3.connect(dark_falz, "Ruins 3 to Final Boss", playerHas("Unlocked Dark Falz"))
