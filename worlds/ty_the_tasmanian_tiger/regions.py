import typing
from enum import Enum

from BaseClasses import MultiWorld, Region
from worlds.ty_the_tasmanian_tiger import Ty1Options


class Ty1Region(Region):
    subregions: typing.List[Region] = []

class Ty1LevelCode(Enum):
    Z1 = 0
    A1 = 4
    A2 = 5
    A3 = 6
    A4 = 7
    B1 = 8
    B2 = 9
    B3 = 10
    D4 = 19
    C1 = 12
    C2 = 13
    C3 = 14
    C4 = 15
    D1 = 16
    D2 = 17
    E1 = 20
    E2 = 21
    E3 = 22
    E4 = 23

ty1_levels: typing.Dict[Ty1LevelCode, str] = {
    Ty1LevelCode.Z1: "Rainbow Cliffs",
    Ty1LevelCode.A1: "Two Up",
    Ty1LevelCode.A2: "Walk in the Park",
    Ty1LevelCode.A3: "Ship Rex",
    Ty1LevelCode.A4: "Bull's Pen",
    Ty1LevelCode.B1: "Bridge on the River Ty",
    Ty1LevelCode.B2: "Snow Worries",
    Ty1LevelCode.B3: "Outback Safari",
    Ty1LevelCode.D4: "Crikey's Cove",
    Ty1LevelCode.C1: "Lyre, Lyre Pants on Fire",
    Ty1LevelCode.C2: "Beyond the Black Stump",
    Ty1LevelCode.C3: "Rex Marks the Spot",
    Ty1LevelCode.C4: "Fluffy's Fjord",
    Ty1LevelCode.D1: "Credits"
    Ty1LevelCode.D2: "Cass' Crest",
    Ty1LevelCode.E1: "Cass' Pass",
    Ty1LevelCode.E2: "Final Battle",
    Ty1LevelCode.E3: "Bonus World 1",
    Ty1LevelCode.E4: "Bonus World 2"
}

region_groups = {
    "Blibli Station": [Ty1LevelCode.A1, Ty1LevelCode.A2, Ty1LevelCode.A3, Ty1LevelCode.A4],
    "Pippy Beach": [Ty1LevelCode.B1, Ty1LevelCode.B2, Ty1LevelCode.B3, Ty1LevelCode.D4],
    "Lake Burril": [Ty1LevelCode.C1, Ty1LevelCode.C2, Ty1LevelCode.C3, Ty1LevelCode.C4],
    "Final Gauntlet": [Ty1LevelCode.E1, Ty1LevelCode.E4],
    "Bonus Worlds": [Ty1LevelCode.E2, Ty1LevelCode.E3]
}

def create_regions(world: MultiWorld, options: Ty1Options, player: int):
    # Create main menu and base regions
    create_region("Menu", player, world, "Main Menu")
    create_region("Rainbow Cliffs", player, world)

    # Create and connect grouped regions
    for group_name, levels in region_groups.items():
        group_region = create_region(group_name, player, world)
        connect_regions(world, player, "Rainbow Cliffs", group_region.name)
        for level_code in levels:
            level_region = create_region(ty1_levels[level_code], player, world)
            connect_regions(world, player, group_region.name, level_region.name)

    # Additional connections
    connect_regions(world, player, ty1_levels[Ty1LevelCode.E1], ty1_levels[Ty1LevelCode.D2]) # Pass -> Crest
    connect_regions(world, player, ty1_levels[Ty1LevelCode.D2], ty1_levels[Ty1LevelCode.E4]) # Crest -> Final
    connect_regions(world, player, ty1_levels[Ty1LevelCode.E4], ty1_levels[Ty1LevelCode.D1]) # Final -> Credits
    connect_regions(world, player, ty1_levels[Ty1LevelCode.D1], ty1_levels[Ty1LevelCode.Z1]) # Credits -> RC
    connect_regions(world, player, ty1_levels[Ty1LevelCode.D2], ty1_levels[Ty1LevelCode.Z1]) # Crest -> RC

def create_region(name: str, player: int, world: MultiWorld, description: str = "") -> Ty1Region:
    region = Ty1Region(name, player, world, description)
    world.regions.append(region)
    return region

def connect_regions(world: MultiWorld, player: int, source: str, target: str, rule=None) -> Entrance:
    source_region = world.get_region(source, player)
    target_region = world.get_region(target, player)
    return source_region.connect(target_region, rule=rule)

def set_subregion_access_rule(world, player, region_name: str, rule):
    world.get_entrance(world, player, region_name).access_rule = rule

def create_default_locs(reg: Region, default_locs: dict):
    create_locs(reg, *default_locs.keys())

def create_locs(reg: Region, *locs: str):
    reg.locations += [Ty1Location(reg.player, loc_name, location_table[loc_name], reg) for loc_name in locs]