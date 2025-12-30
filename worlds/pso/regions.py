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
        RegionName.pioneer_2,
        RegionName.forest_1,
        RegionName.forest_2,
        RegionName.forest_boss,
        RegionName.caves_1,
        RegionName.caves_2,
        RegionName.caves_3,
        RegionName.caves_boss,
        RegionName.mines_1,
        RegionName.mines_2,
        RegionName.mines_boss,
        RegionName.ruins_entrance,
        RegionName.ruins_1,
        RegionName.ruins_2,
        RegionName.ruins_3,
        RegionName.dark_falz
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

    pioneer_2 = world.get_region(RegionName.pioneer_2)
    forest_1 = world.get_region(RegionName.forest_1)
    forest_2 = world.get_region(RegionName.forest_2)
    forest_boss = world.get_region(RegionName.forest_boss)
    caves_1 = world.get_region(RegionName.caves_1)
    caves_2 = world.get_region(RegionName.caves_2)
    caves_3 = world.get_region(RegionName.caves_3)
    caves_boss = world.get_region(RegionName.caves_boss)
    mines_1 = world.get_region(RegionName.mines_1)
    mines_2 = world.get_region(RegionName.mines_2)
    mines_boss = world.get_region(RegionName.mines_boss)
    ruins_entrance = world.get_region(RegionName.ruins_entrance)
    ruins_1 = world.get_region(RegionName.ruins_1)
    ruins_2 = world.get_region(RegionName.ruins_2)
    ruins_3 = world.get_region(RegionName.ruins_3)
    dark_falz = world.get_region(RegionName.dark_falz)

    # Pioneer 2 Entrances
    pioneer_2.connect(forest_1, EntranceName.pioneer_2_to_forest_1, player_has(Item.unlock_forest_1))
    pioneer_2.connect(forest_2, EntranceName.pioneer_2_to_forest_2, player_has(Item.unlock_forest_2))
    pioneer_2.connect(caves_1, EntranceName.pioneer_2_to_caves_1, player_has(Item.unlock_caves_1))
    pioneer_2.connect(caves_2, EntranceName.pioneer_2_to_caves_2, player_has(Item.unlock_caves_2))
    pioneer_2.connect(caves_3, EntranceName.pioneer_2_to_caves_3, player_has(Item.unlock_caves_3))
    pioneer_2.connect(mines_1, EntranceName.pioneer_2_to_mines_1, player_has(Item.unlock_mines_1))
    pioneer_2.connect(mines_2, EntranceName.pioneer_2_to_mines_2, player_has(Item.unlock_mines_2))
    pioneer_2.connect(ruins_1, EntranceName.pioneer_2_to_ruins_1, player_has(Item.unlock_ruins_1))
    pioneer_2.connect(ruins_2, EntranceName.pioneer_2_to_ruins_2, player_has(Item.unlock_ruins_2))
    pioneer_2.connect(ruins_3, EntranceName.pioneer_2_to_ruins_3, player_has(Item.unlock_ruins_3))

    # Level Entrances
    # Technically, there are teleporters to return to Pioneer 2 in some areas, but Archipelago assumes
    # we can always return, so we leave those out.
    # This will also have to be reevaluated if / when we have non-linear progression.
    forest_1.connect(forest_2, EntranceName.forest_1_to_forest_2, player_has(Item.unlock_forest_2))
    forest_2.connect(forest_boss, EntranceName.forest_2_to_forest_boss, player_has(Item.unlock_dragon))
    caves_1.connect(caves_2, EntranceName.caves_1_to_caves_2, player_has(Item.unlock_caves_2))
    caves_2.connect(caves_3, EntranceName.caves_2_to_caves_3, player_has(Item.unlock_caves_3))
    caves_3.connect(caves_boss, EntranceName.caves_3_to_caves_boss, player_has(Item.unlock_de_rol_le))
    mines_1.connect(mines_2, EntranceName.mines_1_to_mines_2, player_has(Item.unlock_mines_2))
    mines_2.connect(mines_boss, EntranceName.mines_2_to_mines_boss, player_has(Item.unlock_vol_opt))
    # I feel like it makes sense that this connection will always be open, similar to vanilla, even without an unlock
    mines_boss.connect(ruins_entrance, EntranceName.mines_boss_to_ruins_entrance) #, player_has("Unlocked Ruins Entrance"))
    ruins_entrance.connect(ruins_1, EntranceName.ruins_entrance_to_ruins_1,
                           player_has_all([Item.forest_pillar, Item.caves_pillar, Item.mines_pillar]))
    ruins_1.connect(ruins_2, EntranceName.ruins_1_to_ruins_2, player_has(Item.unlock_ruins_2))
    ruins_2.connect(ruins_3, EntranceName.ruins_2_to_ruins_3, player_has(Item.unlock_ruins_3))
    ruins_3.connect(dark_falz, EntranceName.ruins_3_to_dark_falz, player_has(Item.unlock_dark_falz))
