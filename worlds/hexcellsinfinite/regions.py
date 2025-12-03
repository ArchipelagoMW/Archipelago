from BaseClasses import Region
from .types import HexcellsInfiniteLocation
from .locations import location_table
from typing import TYPE_CHECKING
from .options import LevelUnlockType

if TYPE_CHECKING:
    from . import HexcellsInfiniteWorld

def create_regions(world: "HexcellsInfiniteWorld"):
    menu = create_region(world, "Menu")
    
    if world.options.LevelUnlockType == LevelUnlockType.option_vanilla:

        lvlgroup1 = create_region_and_connect(world, "Level Group 1", "Menu -> Level Group 1", menu)
        lvlgroup2 = create_region_and_connect(world, "Level Group 2", "Level Group 1 -> Level Group 2", lvlgroup1)
        lvlgroup3 = create_region_and_connect(world, "Level Group 3", "Level Group 2 -> Level Group 3", lvlgroup2)
        lvlgroup4 = create_region_and_connect(world, "Level Group 4", "Level Group 3 -> Level Group 4", lvlgroup3)
        lvlgroup5 = create_region_and_connect(world, "Level Group 5", "Level Group 4 -> Level Group 5", lvlgroup4)
        create_region_and_connect(world, "Level Group 6", "Level Group 5 -> Level Group 6", lvlgroup5)

    elif world.options.LevelUnlockType == LevelUnlockType.option_individual:

        levels = [f"{i}-{j}" for j in range(1, 7) for i in range(1, 7)]
        for level in levels:
            create_region_and_connect(world, f"Hexcells Level {level}", f"Menu -> {level}", menu)

def create_region(world: "HexcellsInfiniteWorld", name: str) -> Region:
    reg = Region(name, world.player, world.multiworld)

    for (key, data) in location_table.items():
        if data.region == name:
            location = HexcellsInfiniteLocation(world.player, key, data.ap_code, reg)
            reg.locations.append(location)
    
    world.multiworld.regions.append(reg)
    return reg

def create_region_and_connect(world: "HexcellsInfiniteWorld",
                               name: str, entrancename: str, connected_region: Region) -> Region:
    reg: Region = create_region(world, name)
    connected_region.connect(reg, entrancename)
    return reg
