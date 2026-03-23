from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import TeardownWorld

# A region is a container for locations ("checks"), which connects to other regions via "Entrance" objects.
# Many games will model their Levels after physical in-game places, but you can also have more abstract regions.
# For a location to be in logic, its containing region must be reachable.
# The Entrances connecting regions can have rules - more on that in rules.py.
# This makes regions especially useful for traversal logic ("Can the player reach this part of the map?")

# Every location must be inside a region, and you must have at least one region.
# This is why we create regions first, and then later we create the locations (in locations.py).


def create_and_connect_regions(world: TeardownWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: TeardownWorld) -> None:
    # Creating a region is as simple as calling the constructor of the Level class.
    level_1 = Region("Level 1", world.player, world.multiworld)
    level_2 = Region("Level 2", world.player, world.multiworld)
    level_3 = Region("Level 3", world.player, world.multiworld)
    #level_4 = Region("Level 4", world.player, world.multiworld)
    #level_5 = Region("Level 5", world.player, world.multiworld)

    # Let's put all these regions in a list.
    regions = [level_1, level_2, level_3]

    # Some regions may only exist if the player enables certain options.
    # In our case, the Hammer locks the top middle chest in its own room if the hammer option is enabled.
    if world.options.Bonus_Level:
        bonus_level_4 = Region("Bonus Level 4", world.player, world.multiworld)
        regions.append(bonus_level_4)

    # We now need to add these regions to multiworld.regions so that AP knows about their existence.
    world.multiworld.regions += regions


def connect_regions(world: TeardownWorld) -> None:
    # We have regions now, but still need to connect them to each other.
    # But wait, we no longer have access to the region variables we created in create_all_regions()!
    # Luckily, once you've submitted your regions to multiworld.regions,
    # you can get them at any time using world.get_region(...).
    level_1 = world.get_region("Level 1")
    level_2 = world.get_region("Level 2")
    level_3 = world.get_region("Level 3")
   # level_4 = world.get_region("Level 4")
   # level_5 = world.get_region("Level 5")


    # An even easier way is to use the region.connect helper.
    level_1.connect(level_2, "Level 1 to Level 2")
    level_2.connect(level_3, "Level 2 to Level 3")
   # level_3.connect(level_4, "Level 3 to Level 4")
   #level_4.connect(level_5, "Level 4 to Level 5")


    # Some Entrances may only exist if the player enables certain options.
    # In our case, the Hammer locks the top middle chest in its own room if the hammer option is enabled.
    # In this case, we previously created an extra "Level Extra 1" region that we now need to connect to Level 1.
    if world.options.Bonus_Level:
        bonus_level_4 = world.get_region("Bonus Level 4")
        level_3.connect(bonus_level_4, "Level 3 to Bonus Level 4")
