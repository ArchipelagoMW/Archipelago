from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from BaseClasses import Entrance, Region, CollectionState
from .strings.region_names import Region as RegionName
from .strings.entrance_names import Entrance as EntranceName
from .strings.item_names import Item

if TYPE_CHECKING:
    from .world import PSOWorld

# A region is a container for locations ("checks"), which connects to other regions via "Entrance" objects.
# Many games will model their Regions after physical in-game places, but you can also have more abstract regions.
# For a location to be in logic, its containing region must be reachable.
# The Entrances connecting regions can have rules - more on that in rules.py.
# This makes regions especially useful for traversal logic ("Can the player reach this part of the map?")

# Every location must be inside a region, and you must have at least one region.
# This is why we create regions first, and then later we create the locations (in locations.py).

def create_and_connect_regions(world: PSOWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: PSOWorld) -> None:
    # Starting with just a barebones list of the main areas in Episode 1
    region_names = [
        RegionName.PIONEER_2,
        RegionName.FOREST_1,
        RegionName.FOREST_2,
        RegionName.DRAGON,
        RegionName.CAVES_1,
        RegionName.CAVES_2,
        RegionName.CAVES_3,
        RegionName.DE_ROL_LE,
        RegionName.MINES_1,
        RegionName.MINES_2,
        RegionName.VOL_OPT,
        RegionName.RUINS_ENTRANCE,
        RegionName.RUINS_1,
        RegionName.RUINS_2,
        RegionName.RUINS_3,
        RegionName.DARK_FALZ
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
    def player_has(condition: str) -> Callable[[CollectionState], bool]:
        return lambda state: state.has(condition, world.player)

    def player_has_all(conditions: list[str]) -> Callable[[CollectionState], bool]:
        return lambda state: state.has_all(conditions, world.player)

    pioneer_2 = world.get_region(RegionName.PIONEER_2)
    forest_1 = world.get_region(RegionName.FOREST_1)
    forest_2 = world.get_region(RegionName.FOREST_2)
    forest_boss = world.get_region(RegionName.DRAGON)
    caves_1 = world.get_region(RegionName.CAVES_1)
    caves_2 = world.get_region(RegionName.CAVES_2)
    caves_3 = world.get_region(RegionName.CAVES_3)
    caves_boss = world.get_region(RegionName.DE_ROL_LE)
    mines_1 = world.get_region(RegionName.MINES_1)
    mines_2 = world.get_region(RegionName.MINES_2)
    mines_boss = world.get_region(RegionName.VOL_OPT)
    ruins_entrance = world.get_region(RegionName.RUINS_ENTRANCE)
    ruins_1 = world.get_region(RegionName.RUINS_1)
    ruins_2 = world.get_region(RegionName.RUINS_2)
    ruins_3 = world.get_region(RegionName.RUINS_3)
    dark_falz = world.get_region(RegionName.DARK_FALZ)

    # Pioneer 2 Entrances
    pioneer_2.connect(forest_1, EntranceName.PIONEER_2_TO_FOREST_1, player_has(Item.UNLOCK_FOREST_1))
    pioneer_2.connect(forest_2, EntranceName.PIONEER_2_TO_FOREST_2, player_has(Item.UNLOCK_FOREST_2))
    pioneer_2.connect(caves_1, EntranceName.PIONEER_2_TO_CAVES_1, player_has(Item.UNLOCK_CAVES_1))
    pioneer_2.connect(caves_2, EntranceName.PIONEER_2_TO_CAVES_2, player_has(Item.UNLOCK_CAVES_2))
    pioneer_2.connect(caves_3, EntranceName.PIONEER_2_TO_CAVES_3, player_has(Item.UNLOCK_CAVES_3))
    pioneer_2.connect(mines_1, EntranceName.PIONEER_2_TO_MINES_1, player_has(Item.UNLOCK_MINES_1))
    pioneer_2.connect(mines_2, EntranceName.PIONEER_2_TO_MINES_2, player_has(Item.UNLOCK_MINES_2))
    pioneer_2.connect(ruins_1, EntranceName.PIONEER_2_TO_RUINS_1, player_has(Item.UNLOCK_RUINS_1))
    pioneer_2.connect(ruins_2, EntranceName.PIONEER_2_TO_RUINS_2, player_has(Item.UNLOCK_RUINS_2))
    pioneer_2.connect(ruins_3, EntranceName.PIONEER_2_TO_RUINS_3, player_has(Item.UNLOCK_RUINS_3))

    # Level Entrances
    # Technically, there are teleporters to return to Pioneer 2 in some areas, but Archipelago assumes
    # we can always return, so we leave those out.
    # This will also have to be reevaluated if / when we have non-linear progression.
    forest_1.connect(forest_2, EntranceName.FOREST_1_TO_FOREST_2, player_has(Item.UNLOCK_FOREST_2))
    forest_2.connect(forest_boss, EntranceName.FOREST_2_TO_DRAGON, player_has(Item.UNLOCK_DRAGON))
    caves_1.connect(caves_2, EntranceName.CAVES_1_TO_CAVES_2, player_has(Item.UNLOCK_CAVES_2))
    caves_2.connect(caves_3, EntranceName.CAVES_2_TO_CAVES_3, player_has(Item.UNLOCK_CAVES_3))
    caves_3.connect(caves_boss, EntranceName.CAVES_3_TO_DE_ROL_LE, player_has(Item.UNLOCK_DE_ROL_LE))
    mines_1.connect(mines_2, EntranceName.MINES_1_TO_MINES_2, player_has(Item.UNLOCK_MINES_2))
    mines_2.connect(mines_boss, EntranceName.MINES_2_TO_VOL_OPT, player_has(Item.UNLOCK_VOL_OPT))
    # I feel like it makes sense that this connection will always be open, similar to vanilla, even without an unlock
    mines_boss.connect(ruins_entrance, EntranceName.VOL_OPT_TO_RUINS_ENTRANCE) #, player_has("Unlocked Ruins Entrance"))
    ruins_entrance.connect(ruins_1, EntranceName.RUINS_ENTRANCE_TO_RUINS_1,
                           player_has_all([Item.FOREST_PILLAR, Item.CAVES_PILLAR, Item.MINES_PILLAR]))
    ruins_1.connect(ruins_2, EntranceName.RUINS_1_TO_RUINS_2, player_has(Item.UNLOCK_RUINS_2))
    ruins_2.connect(ruins_3, EntranceName.RUINS_2_TO_RUINS_3, player_has(Item.UNLOCK_RUINS_3))
    ruins_3.connect(dark_falz, EntranceName.RUINS_3_TO_DARK_FALZ, player_has(Item.UNLOCK_DARK_FALZ))
