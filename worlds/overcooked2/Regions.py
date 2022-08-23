from .Overcooked2Levels import Overcooked2Level
from .Locations import Overcooked2Location, location_name_to_id

import typing
from BaseClasses import MultiWorld, Region, Entrance, Location, RegionType

overcooked_regions = [
    ("Menu", ["New Game"]),
    ("World Map", [level.level_name() for level in Overcooked2Level()]),
]

for level in Overcooked2Level():
    if (level.level_name() == "6-6"):
        overcooked_regions.append(
            (
                level.level_name(),
                ["Level Exit", "Credits"]
            )
        )
    else:
        overcooked_regions.append(
            (
                level.level_name(),
                ["Level Exit"]
            )
        )

mandatory_connections = [
    ("New Game", "World Map"),
    ("Level Exit", "World Map"),
]

def create_regions(world: MultiWorld, player: int):
    # Main Menu -> Overworld
    region = Region("Menu", RegionType.Generic, "Menu", player, world)
    region.exits = [Entrance(player, "New game", r)]
    world.regions.append(region)

    # Overworld -> All Levels
    region = Region("Overworld", RegionType.Generic, "Overworld", player, world)
    for level_name in location_name_to_id:
        region.locations.append(
            Overcooked2Location(player, level_name, location_name_to_id[level_name], region)
        )
    
    # All Levels -> Overworld
    # ?

    r.exits = [Entrance(player, "Boss Door", r)]
    world.regions.append(r)

    r = Region("Boss Room", RegionType.Generic, "Boss Room", player, world)
    # add event to Boss Room
    r.locations = [MyGameLocation(player, "Final Boss", None, r)]
    world.regions.append(r)

    # If entrances are not randomized, they should be connected here, otherwise
    # they can also be connected at a later stage.
    world.get_entrance("New Game", player)\
        .connect(world.get_region("Main Area", player))
    world.get_entrance("Boss Door", player)\
        .connect(world.get_region("Boss Room", player))

    # If setting location access rules from data is easier here, set_rules can
    # possibly omitted.
