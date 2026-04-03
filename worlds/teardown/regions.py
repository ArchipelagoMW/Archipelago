from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import TeardownWorld




def create_and_connect_regions(world: TeardownWorld) -> None:
    create_all_regions(world)
    connect_regions(world)

# Creates all regions
def create_all_regions(world: TeardownWorld) -> None:
    level_1 = Region("Level 1", world.player, world.multiworld)
    level_2 = Region("Level 2", world.player, world.multiworld)
    level_3 = Region("Level 3", world.player, world.multiworld)

# Lists all regions
    regions = [level_1, level_2, level_3]

# Creates region if option is enabled
    if world.options.Bonus_Level:
        bonus_level_4 = Region("Bonus Level 4", world.player, world.multiworld)
        regions.append(bonus_level_4)

# Adds all regions to list
    world.multiworld.regions += regions

# Renames the objects we lost creating them
def connect_regions(world: TeardownWorld) -> None:
    level_1 = world.get_region("Level 1")
    level_2 = world.get_region("Level 2")
    level_3 = world.get_region("Level 3")

# Connects the regions
    level_1.connect(level_2, "Level 1 to Level 2")
    level_2.connect(level_3, "Level 2 to Level 3")


# Connects the region if option is enabled
    if world.options.Bonus_Level:
        bonus_level_4 = world.get_region("Bonus Level 4")
        level_3.connect(bonus_level_4, "Level 3 to Bonus Level 4")
