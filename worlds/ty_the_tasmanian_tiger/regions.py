from enum import Enum

from BaseClasses import MultiWorld, Region, Entrance
from worlds.ty_the_tasmanian_tiger.options import Ty1Options
from worlds.ty_the_tasmanian_tiger.locations import create_locations
from typing import List, Dict


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


ty1_core_levels = [Ty1LevelCode.A1, Ty1LevelCode.A2, Ty1LevelCode.A3,
                   Ty1LevelCode.B1, Ty1LevelCode.B2, Ty1LevelCode.B3,
                   Ty1LevelCode.C1, Ty1LevelCode.C2, Ty1LevelCode.C3]


ty1_levels: Dict[Ty1LevelCode, str] = {
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
    Ty1LevelCode.D1: "Credits",
    Ty1LevelCode.D2: "Cass' Crest",
    Ty1LevelCode.E1: "Cass' Pass",
    Ty1LevelCode.E2: "Final Battle",
    Ty1LevelCode.E3: "Bonus World 1",
    Ty1LevelCode.E4: "Bonus World 2"
}


ty1_levels_short: Dict[Ty1LevelCode, str] = {
    Ty1LevelCode.Z1: "Rainbow Cliffs",
    Ty1LevelCode.A1: "Two Up",
    Ty1LevelCode.A2: "WitP",
    Ty1LevelCode.A3: "Ship Rex",
    Ty1LevelCode.A4: "Bull's Pen",
    Ty1LevelCode.B1: "BotRT",
    Ty1LevelCode.B2: "Snow Worries",
    Ty1LevelCode.B3: "Outback Safari",
    Ty1LevelCode.D4: "Crikey's Cove",
    Ty1LevelCode.C1: "LLPoF",
    Ty1LevelCode.C2: "BtBS",
    Ty1LevelCode.C3: "RMtS",
    Ty1LevelCode.C4: "Fluffy's Fjord",
    Ty1LevelCode.D1: "Credits",
    Ty1LevelCode.D2: "Cass' Crest",
    Ty1LevelCode.E1: "Cass' Pass",
    Ty1LevelCode.E2: "Final Battle",
    Ty1LevelCode.E3: "Bonus World 1",
    Ty1LevelCode.E4: "Bonus World 2"
}


class Ty1Region(Region):
    subregions: List[Region] = []


def connect_regions(world: MultiWorld, player: int, from_name: str, to_name: str, entrance_name: str) -> Entrance:
    entrance_region = world.get_region(from_name, player)
    exit_region = world.get_region(to_name, player)
    return entrance_region.connect(exit_region, entrance_name)


def create_region(world: MultiWorld, player: int, options: Ty1Options, name: str):
    reg = Region(name, player, world)
    create_locations(player, options, reg)
    world.regions.append(reg)


def create_regions(world: MultiWorld, options: Ty1Options, player: int):
    create_region(world, player, options, "Menu")
    create_region(world, player, options, "Rainbow Cliffs")
    create_region(world, player, options, "Rainbow Cliffs - PF")
    create_region(world, player, options, "Bli Bli Station")
    create_region(world, player, options, "Bli Bli Station Gate")
    create_region(world, player, options, "Bli Bli Station Gate - PF")
    create_region(world, player, options, "Pippy Beach")
    create_region(world, player, options, "Pippy Beach - PF")
    create_region(world, player, options, "Lake Burril")
    create_region(world, player, options, "Final Gauntlet")
    create_region(world, player, options, "Final Gauntlet - PF")
    create_region(world, player, options, "Two Up")
    create_region(world, player, options, "Two Up - PF")
    create_region(world, player, options, "Two Up - Upper Area")
    create_region(world, player, options, "Two Up - Upper Area - PF")
    create_region(world, player, options, "Two Up - End Area")
    create_region(world, player, options, "Walk in the Park")
    create_region(world, player, options, "Walk in the Park - PF")
    create_region(world, player, options, "Ship Rex")
    create_region(world, player, options, "Ship Rex - PF")
    create_region(world, player, options, "Ship Rex - Beyond Gate")
    create_region(world, player, options, "Ship Rex - Beyond Gate - PF")
    create_region(world, player, options, "Bull's Pen")
    create_region(world, player, options, "Bridge on the River Ty")
    create_region(world, player, options, "Bridge on the River Ty - Underwater")
    create_region(world, player, options, "Bridge on the River Ty - PF")
    create_region(world, player, options, "Bridge on the River Ty - Beyond Broken Bridge")
    create_region(world, player, options, "Bridge on the River Ty - Beyond Broken Bridge Underwater")
    create_region(world, player, options, "Bridge on the River Ty - Beyond Broken Bridge - PF")
    create_region(world, player, options, "Snow Worries")
    create_region(world, player, options, "Snow Worries - PF")
    create_region(world, player, options, "Snow Worries - Underwater")
    create_region(world, player, options, "Outback Safari")
    create_region(world, player, options, "Crikey's Cove")
    create_region(world, player, options, "Lyre, Lyre Pants on Fire")
    create_region(world, player, options, "Lyre, Lyre Pants on Fire - PF")
    create_region(world, player, options, "Beyond the Black Stump")
    create_region(world, player, options, "Beyond the Black Stump - PF")
    create_region(world, player, options, "Beyond the Black Stump - Upper Area")
    create_region(world, player, options, "Beyond the Black Stump - Glide Behind the Mountain")
    create_region(world, player, options, "Beyond the Black Stump - Upper Area - PF")
    create_region(world, player, options, "Rex Marks the Spot")
    create_region(world, player, options, "Rex Marks the Spot - PF")
    create_region(world, player, options, "Rex Marks the Spot - Underwater")
    create_region(world, player, options, "Fluffy's Fjord")
    create_region(world, player, options, "Cass' Pass")
    create_region(world, player, options, "Cass' Crest")
    create_region(world, player, options, "Final Battle")


def connect_all_regions(world: MultiWorld, player: int, options: Ty1Options, portal_map: List[int]):
    if options.level_shuffle:
        world.random.shuffle(portal_map)
    connect_regions(world, player, "Menu",
                    "Rainbow Cliffs", "Menu -> Z1")
    connect_regions(world, player, "Rainbow Cliffs",
                    "Rainbow Cliffs - PF", "Z1 - PF")
    connect_regions(world, player, "Rainbow Cliffs",
                    "Bli Bli Station", "Z1 -> A Zone")
    connect_regions(world, player, "Bli Bli Station",
                    "Bli Bli Station Gate", "A Zone Gate")
    connect_regions(world, player, "Bli Bli Station Gate",
                    "Bli Bli Station Gate - PF", "A Zone Gate - PF")
    connect_regions(world, player, "Rainbow Cliffs",
                    "Pippy Beach", "Z1 -> B Zone")
    connect_regions(world, player, "Pippy Beach",
                    "Pippy Beach - PF", "B Zone - PF")
    connect_regions(world, player, "Rainbow Cliffs",
                    "Lake Burril", "Z1 -> C Zone")
    connect_regions(world, player, "Rainbow Cliffs",
                    "Final Gauntlet", "Z1 -> E Zone")
    connect_regions(world, player, "Final Gauntlet",
                    "Final Gauntlet - PF", "E Zone - PF")
    ent_a1 = connect_regions(world, player, "Bli Bli Station",
                             ty1_levels[Ty1LevelCode(portal_map[0])], "A1 Portal")
    ent_a2 = connect_regions(world, player, "Bli Bli Station Gate",
                             ty1_levels[Ty1LevelCode(portal_map[1])], "A2 Portal")
    ent_a3 = connect_regions(world, player, "Bli Bli Station Gate",
                             ty1_levels[Ty1LevelCode(portal_map[2])], "A3 Portal")
    connect_regions(world, player, "Bli Bli Station Gate",
                    ty1_levels[Ty1LevelCode.A4], "A4 Portal")
    ent_b1 = connect_regions(world, player, "Pippy Beach",
                             ty1_levels[Ty1LevelCode(portal_map[3])], "B1 Portal")
    ent_b2 = connect_regions(world, player, "Pippy Beach",
                             ty1_levels[Ty1LevelCode(portal_map[4])], "B2 Portal")
    ent_b3 = connect_regions(world, player, "Pippy Beach",
                             ty1_levels[Ty1LevelCode(portal_map[5])], "B3 Portal")
    connect_regions(world, player, "Pippy Beach",
                    ty1_levels[Ty1LevelCode.D4], "D4 Portal")
    ent_c1 = connect_regions(world, player, "Lake Burril",
                             ty1_levels[Ty1LevelCode(portal_map[6])], "C1 Portal")
    ent_c2 = connect_regions(world, player, "Lake Burril",
                             ty1_levels[Ty1LevelCode(portal_map[7])], "C2 Portal")
    ent_c3 = connect_regions(world, player, "Lake Burril",
                             ty1_levels[Ty1LevelCode(portal_map[8])], "C3 Portal")
    connect_regions(world, player, "Lake Burril",
                    ty1_levels[Ty1LevelCode.C4], "C4 Portal")
    connect_regions(world, player, "Final Gauntlet",
                    "Cass' Pass", "E1 Portal")
    connect_regions(world, player, "Cass' Pass",
                    "Cass' Crest", "E1 -> D2")
    connect_regions(world, player, "Cass' Crest",
                    "Final Battle", "D2 -> E4")
    connect_regions(world, player, "Two Up",
                    "Two Up - PF", "Two Up - PF")
    connect_regions(world, player, "Two Up",
                    "Two Up - Upper Area", "Two Up - Upper Area")
    connect_regions(world, player, "Two Up - Upper Area",
                    "Two Up - Upper Area - PF", "Two Up - Upper Area - PF")
    connect_regions(world, player, "Two Up",
                    "Two Up - End Area", "Two Up - End Area")
    connect_regions(world, player, "Walk in the Park",
                    "Walk in the Park - PF", "Walk in the Park - PF")
    connect_regions(world, player, "Ship Rex",
                    "Ship Rex - PF", "Ship Rex - PF")
    connect_regions(world, player, "Ship Rex",
                    "Ship Rex - Beyond Gate", "Ship Rex - Sea Gate")
    connect_regions(world, player, "Ship Rex - Beyond Gate",
                    "Ship Rex - Beyond Gate - PF", "Ship Rex - Gate - PF")
    connect_regions(world, player, "Bridge on the River Ty",
                    "Bridge on the River Ty - Underwater", "Bridge on the River Ty - Underwater")
    connect_regions(world, player, "Bridge on the River Ty",
                    "Bridge on the River Ty - PF", "Bridge on the River Ty - PF")
    connect_regions(world, player, "Bridge on the River Ty",
                    "Bridge on the River Ty - Beyond Broken Bridge", 
                    "Bridge on the River Ty - Broken Bridge Glide")
    connect_regions(world, player, "Bridge on the River Ty - Beyond Broken Bridge",
                    "Bridge on the River Ty - Beyond Broken Bridge Underwater",
                    "Bridge on the River Ty - Beyond Broken Bridge Underwater")
    connect_regions(world, player, "Bridge on the River Ty - Beyond Broken Bridge",
                    "Bridge on the River Ty - Beyond Broken Bridge - PF", 
                    "Bridge on the River Ty - Broken Bridge - PF")
    connect_regions(world, player, "Snow Worries",
                    "Snow Worries - PF", "Snow Worries - PF")
    connect_regions(world, player, "Snow Worries",
                    "Snow Worries - Underwater", "Snow Worries - Underwater")
    connect_regions(world, player, "Lyre, Lyre Pants on Fire",
                    "Lyre, Lyre Pants on Fire - PF", "Lyre, Lyre Pants on Fire - PF")
    connect_regions(world, player, "Beyond the Black Stump",
                    "Beyond the Black Stump - PF", "Beyond the Black Stump - PF")
    connect_regions(world, player, "Beyond the Black Stump",
                    "Beyond the Black Stump - Upper Area", "Beyond the Black Stump - Upper Area")
    connect_regions(world, player, "Beyond the Black Stump - Upper Area",
                    "Beyond the Black Stump - Glide Behind the Mountain",
                    "Beyond the Black Stump - Glide")
    connect_regions(world, player, "Beyond the Black Stump - Upper Area",
                    "Beyond the Black Stump - Upper Area - PF", 
                    "Beyond the Black Stump - Upper Area - PF")
    connect_regions(world, player, "Rex Marks the Spot",
                    "Rex Marks the Spot - PF", "Rex Marks the Spot, PF")
    connect_regions(world, player, "Rex Marks the Spot",
                    "Rex Marks the Spot - Underwater", "Rex Marks the Spot - Underwater")
    # 0.6.0 ENTRANCE RANDO SUPPORT
    # if options.level_shuffle:
        # disconnect_entrance_for_randomization(ent_a1, 0)
        # disconnect_entrance_for_randomization(ent_a2, 0)
        # disconnect_entrance_for_randomization(ent_a3, 0)
        # disconnect_entrance_for_randomization(ent_b1, 0)
        # disconnect_entrance_for_randomization(ent_b2, 0)
        # disconnect_entrance_for_randomization(ent_b3, 0)
        # disconnect_entrance_for_randomization(ent_c1, 0)
        # disconnect_entrance_for_randomization(ent_c2, 0)
        # disconnect_entrance_for_randomization(ent_c3, 0)
        # target_group_lookup: Dict[int, List[int]] = {0: [0]}
        # return randomize_entrances(world.worlds[player], True, target_group_lookup)
