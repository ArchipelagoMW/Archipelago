from enum import Enum

from BaseClasses import MultiWorld, Region
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

class Ty1Region(Region):
    subregions: List[Region] = []

def connect_regions(world: MultiWorld, player: int, options: Ty1Options, from_name: str, to_name: str, entrance_name: str, rule_std = None, rule_adv = None) -> Region:
    entrance_region = world.get_region(from_name, player)
    exit_region = world.get_region(to_name, player)
    entrance_region.connect(exit_region, entrance_name, rule = rule_std if options.logic_difficulty == 0 else rule_adv)
    return exit_region

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
    create_region(world, player, options, "Bridge on the River Ty - PF")
    create_region(world, player, options, "Bridge on the River Ty - Beyond Broken Bridge")
    create_region(world, player, options, "Bridge on the River Ty - Beyond Broken Bridge - PF")
    create_region(world, player, options, "Snow Worries")
    create_region(world, player, options, "Snow Worries - PF")
    create_region(world, player, options, "Snow Worries - Underwater")
    create_region(world, player, options, "Outback Safari")
    create_region(world, player, options, "Crikey's Cove")
    create_region(world, player, options, "Lyre, Lyre Pants on Fire")
    create_region(world, player, options, "Lyre, Lyre Pants on Fire - PF")
    create_region(world, player, options, "Lyre, Lyre Pants on Fire - Beyond Gate")
    create_region(world, player, options, "Lyre, Lyre Pants on Fire - Beyond Gate - PF")
    create_region(world, player, options, "Beyond the Black Stump")
    create_region(world, player, options, "Beyond the Black Stump - PF")
    create_region(world, player, options, "Beyond the Black Stump - Upper Area")
    create_region(world, player, options, "Beyond the Black Stump - Upper Area - PF")
    create_region(world, player, options, "Rex Marks the Spot")
    create_region(world, player, options, "Rex Marks the Spot - PF")
    create_region(world, player, options, "Rex Marks the Spot - Underwater")
    create_region(world, player, options, "Fluffy's Fjord")
    create_region(world, player, options, "Cass' Pass")
    create_region(world, player, options, "Cass' Crest")
    create_region(world, player, options, "Final Battle")

def connect_all_regions(world: MultiWorld, player: int, options: Ty1Options, portal_map: List[int], boss_map: List[int] ):
    if options.level_shuffle:
        world.random.shuffle(portal_map)
    if options.boss_shuffle:
        world.random.shuffle(boss_map)        
    pr_mod = 1 if not options.start_with_boom.value and options.progressive_elementals.value else 0
    pl_mod = 1 if options.level_unlock_style.value == 1 else 0
    connect_regions(world, player, options, "Menu", "Rainbow Cliffs", "Menu -> Z1")
    connect_regions(world, player, options, "Rainbow Cliffs", "Rainbow Cliffs - PF", "Z1 - PF",
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod)),
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod)))
    connect_regions(world, player, options, "Rainbow Cliffs", "Bli Bli Station", "Z1 -> A Zone")
    connect_regions(world, player, options, "Bli Bli Station", "Bli Bli Station Gate", "A Zone Gate",
                    lambda state: (state.has("Progressive Rang", player, 1 + pr_mod) or state.has("Second Rang", player)))
    connect_regions(world, player, options, "Bli Bli Station Gate", "Bli Bli Station Gate - PF", "A Zone Gate - PF",
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod) and (state.has("Infrarang", player) if options.frames_require_infra else True)),
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod) and (state.has("Infrarang", player) if options.frames_require_infra else True)))
    connect_regions(world, player, options, "Rainbow Cliffs", "Pippy Beach", "Z1 -> B Zone",
                    lambda state: (state.has("Progressive Rang", player, 5 + pr_mod) or state.has("Flamerang", player)),
                    lambda state: (state.has("Progressive Rang", player, 4 + pr_mod) or state.has("Flamerang", player) or state.has("Dive", player)))
    connect_regions(world, player, options, "Pippy Beach", "Pippy Beach - PF", "B Zone - PF",
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod) and (state.has("Infrarang", player) if options.frames_require_infra else True)),
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod) and (state.has("Infrarang", player) if options.frames_require_infra else True)))
    connect_regions(world, player, options, "Rainbow Cliffs", "Lake Burril", "Z1 -> C Zone",
                    lambda state: (state.has("Progressive Rang", player, 6 + pr_mod) or state.has("Frostyrang", player)),
                    lambda state: (state.has("Progressive Rang", player, 4 + pr_mod) or state.has("Frostyrang", player) or state.has("Dive", player)))
    connect_regions(world, player, options, "Rainbow Cliffs", "Final Gauntlet", "Z1 -> E Zone",
                    lambda state: (state.has("Progressive Rang", player, 7 + pr_mod) or state.has("Zappyrang", player)),
                    lambda state: (state.has("Progressive Rang", player, 4 + pr_mod) or state.has("Zappyrang", player) or state.has("Dive", player)))
    connect_regions(world, player, options, "Final Gauntlet", "Final Gauntlet - PF", "E Zone - PF",
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod) and (state.has("Infrarang", player) if options.frames_require_infra else True)),
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod) and (state.has("Infrarang", player) if options.frames_require_infra else True)))

    connect_regions(world, player, options, "Bli Bli Station", ty1_levels[Ty1LevelCode(portal_map[0])], "A1 Portal")

    condition = None
    a2_portal_name = "Portal - " + ty1_levels[Ty1LevelCode(portal_map[1])]
    if options.level_unlock_style != 0:
        condition = lambda state: (state.has("Progressive Level", player, 1) or state.has(a2_portal_name, player))
    connect_regions(world, player, options, "Bli Bli Station Gate", ty1_levels[Ty1LevelCode(portal_map[1])],
                    "A2 Portal", condition, condition)

    condition = None
    a3_portal_name = "Portal - " + ty1_levels[Ty1LevelCode(portal_map[2])]
    if options.level_unlock_style != 0:
        condition = lambda state: (state.has("Progressive Level", player, 2) or state.has(a3_portal_name, player))
    connect_regions(world, player, options, "Bli Bli Station Gate", ty1_levels[Ty1LevelCode(portal_map[2])],
                    "A3 Portal", condition, condition)

    condition = None
    a4_portal_name = "Portal - " + ty1_levels[Ty1LevelCode(boss_map[0])]
    if options.level_unlock_style == 1:
        condition = lambda state: (state.has("Progressive Level", player, 3) or state.has(a4_portal_name, player))
    else:
        condition = lambda state: (state.has("Fire Thunder Egg", player, options.hub_te_counts))
    connect_regions(world, player, options, "Bli Bli Station Gate", ty1_levels[Ty1LevelCode(boss_map[0])],
                    "A4 Portal", condition, condition)

    condition = None
    b1_portal_name = "Portal - " + ty1_levels[Ty1LevelCode(portal_map[3])]
    if options.level_unlock_style != 0:
        condition = lambda state: (state.has("Progressive Level", player, 3 + pl_mod) or state.has(b1_portal_name, player))
    connect_regions(world, player, options, "Pippy Beach", ty1_levels[Ty1LevelCode(portal_map[3])],
                    "B1 Portal", condition, condition)

    condition = None
    b2_portal_name = "Portal - " + ty1_levels[Ty1LevelCode(portal_map[4])]
    if options.level_unlock_style != 0:
        condition = lambda state: (state.has("Progressive Level", player, 4 + pl_mod) or state.has(b2_portal_name, player))
    connect_regions(world, player, options, "Pippy Beach", ty1_levels[Ty1LevelCode(portal_map[4])],
                    "B2 Portal", condition, condition)

    condition = None
    b3_portal_name = "Portal - " + ty1_levels[Ty1LevelCode(portal_map[5])]
    if options.level_unlock_style != 0:
        condition = lambda state: (state.has("Progressive Level", player, 5 + pl_mod) or state.has(b3_portal_name, player))
    connect_regions(world, player, options, "Pippy Beach", ty1_levels[Ty1LevelCode(portal_map[5])],
                    "B3 Portal", condition, condition)

    condition = None
    d4_portal_name = "Portal - " + ty1_levels[Ty1LevelCode(boss_map[1])]
    if options.level_unlock_style == 1:
        condition = lambda state: (state.has("Progressive Level", player, 7) or state.has(d4_portal_name, player))
    else:
        condition = lambda state: (state.has("Ice Thunder Egg", player, options.hub_te_counts))
    connect_regions(world, player, options, "Pippy Beach", ty1_levels[Ty1LevelCode(boss_map[1])],
                    "D4 Portal", condition, condition)

    condition = None
    c1_portal_name = "Portal - " + ty1_levels[Ty1LevelCode(portal_map[6])]
    if options.level_unlock_style != 0:
        condition = lambda state: (state.has("Progressive Level", player, 6 + pl_mod * 2) or state.has(c1_portal_name, player))
    connect_regions(world, player, options, "Lake Burril", ty1_levels[Ty1LevelCode(portal_map[6])],
                    "C1 Portal", condition, condition)

    condition = None
    c2_portal_name = "Portal - " + ty1_levels[Ty1LevelCode(portal_map[7])]
    if options.level_unlock_style != 0:
        condition = lambda state: (state.has("Progressive Level", player, 7 + pl_mod * 2) or state.has(c2_portal_name, player))
    connect_regions(world, player, options, "Lake Burril", ty1_levels[Ty1LevelCode(portal_map[7])],
                    "C2 Portal", condition, condition)

    condition = None
    c3_portal_name = "Portal - " + ty1_levels[Ty1LevelCode(portal_map[8])]
    if options.level_unlock_style != 0:
        condition = lambda state: (state.has("Progressive Level", player, 8 + pl_mod * 2) or state.has(c3_portal_name, player))
    connect_regions(world, player, options, "Lake Burril", ty1_levels[Ty1LevelCode(portal_map[8])],
                    "C3 Portal", condition, condition)

    condition = None
    c4_portal_name = "Portal - " + ty1_levels[Ty1LevelCode(boss_map[2])]
    if options.level_unlock_style == 1:
        condition = lambda state: (state.has("Progressive Level", player, 11) or state.has(c4_portal_name, player))
    else:
        condition = lambda state: (state.has("Air Thunder Egg", player, options.hub_te_counts))
    connect_regions(world, player, options, "Lake Burril", ty1_levels[Ty1LevelCode(boss_map[2])],
                    "C4 Portal", condition, condition)

    condition = None
    e1_portal_name = "Portal - Cass' Pass"
    if options.level_unlock_style != 0:
        condition = lambda state: (state.has("Progressive Level", player, 9 + pl_mod * 3) or state.has(e1_portal_name, player))
    connect_regions(world, player, options, "Final Gauntlet", "Cass' Pass",
                    "E1 Portal", condition, condition)

    connect_regions(world, player, options, "Cass' Pass", "Cass' Crest", "E1 -> D2")
    connect_regions(world, player, options, "Cass' Crest", "Final Battle", "D2 -> E4",
                    lambda state: (state.has("Progressive Rang", player, 1 + pr_mod) or state.has("Second Rang", player)),
                    lambda state: (state.has("Progressive Rang", player, 1 + pr_mod) or state.has("Second Rang", player)))

    connect_regions(world, player, options, "Two Up", "Two Up - PF", "Two Up - PF",
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod) and (state.has("Infrarang", player) if options.frames_require_infra else True)),
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod) and (state.has("Infrarang", player) if options.frames_require_infra else True)))
    connect_regions(world, player, options, "Two Up", "Two Up - Upper Area", "Two Up - Upper Area",
                    lambda state: (state.has("Swim", player) or state.has("Dive", player) or state.has("Second Rang", player) or state.has("Progressive Rang", player, 1 + pr_mod)))
    connect_regions(world, player, options, "Two Up - Upper Area", "Two Up - Upper Area - PF", "Two Up - Upper Area - PF",
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod) and (state.has("Infrarang", player) if options.frames_require_infra else True)),
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod) and (state.has("Infrarang", player) if options.frames_require_infra else True)))
    connect_regions(world, player, options, "Two Up", "Two Up - End Area", "Two Up - End Area",
                    lambda state: (state.has("Second Rang", player) or state.has("Progressive Rang", player, 1 + pr_mod)))

    connect_regions(world, player, options, "Walk in the Park", "Walk in the Park - PF", "Walk in the Park - PF",
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod)),
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod)))

    connect_regions(world, player, options, "Ship Rex", "Ship Rex - PF", "Ship Rex - PF",
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod) and (state.has("Infrarang", player) if options.frames_require_infra else True)),
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod) and (state.has("Infrarang", player) if options.frames_require_infra else True)))
    connect_regions(world, player, options, "Ship Rex", "Ship Rex - Beyond Gate", "Ship Rex - Sea Gate",
                    lambda state: (((state.has("Swim", player) or state.has("Dive", player)) and state.has("Aquarang", player)) or state.has("Progressive Rang", player, 3)),
                    lambda state: (state.has("Dive", player) or state.has("Progressive Rang", player, 2)))
    connect_regions(world, player, options, "Ship Rex - Beyond Gate", "Ship Rex - Beyond Gate - PF", "Ship Rex - Gate - PF",
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod) and (state.has("Infrarang", player) if options.frames_require_infra else True)),
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod) and (state.has("Infrarang", player) if options.frames_require_infra else True)))

    connect_regions(world, player, options, "Bridge on the River Ty", "Bridge on the River Ty - PF", "Bridge on the River Ty - PF",
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod) and (state.has("Infrarang", player) if options.frames_require_infra else True)),
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod) and (state.has("Infrarang", player) if options.frames_require_infra else True)))
    connect_regions(world, player, options, "Bridge on the River Ty", "Bridge on the River Ty - Beyond Broken Bridge", "Bridge on the River Ty - Broken Bridge Glide",
                    lambda state: (state.has("Progressive Rang", player, 1 + pr_mod) or state.has("Second Rang", player)))
    connect_regions(world, player, options, "Bridge on the River Ty - Beyond Broken Bridge", "Bridge on the River Ty - Beyond Broken Bridge - PF", "Bridge on the River Ty - Broken Bridge - PF",
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod) and (state.has("Infrarang", player) if options.frames_require_infra else True)),
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod) and (state.has("Infrarang", player) if options.frames_require_infra else True)))

    connect_regions(world, player, options, "Snow Worries", "Snow Worries - PF", "Snow Worries - PF",
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod) and (state.has("Infrarang", player) if options.frames_require_infra else True)),
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod) and (state.has("Infrarang", player) if options.frames_require_infra else True)))
    connect_regions(world, player, options, "Snow Worries", "Snow Worries - Underwater", "Snow Worries - Underwater",
                    lambda state: (state.has("Swim", player) or state.has("Dive", player) or state.has("Progressive Rang", player, 2)),
                    lambda state: (state.has("Swim", player) or state.has("Dive", player) or state.has("Progressive Rang", player, 2)))

    connect_regions(world, player, options, "Lyre, Lyre Pants on Fire", "Lyre, Lyre Pants on Fire - Beyond Gate", "Lyre, Lyre Pants on Fire - Gate",
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod)),
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod)))
    connect_regions(world, player, options, "Lyre, Lyre Pants on Fire", "Lyre, Lyre Pants on Fire - PF", "Lyre, Lyre Pants on Fire - PF",
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod) and (state.has("Infrarang", player) if options.frames_require_infra else True)),
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod) and (state.has("Infrarang", player) if options.frames_require_infra else True)))
    connect_regions(world, player, options, "Lyre, Lyre Pants on Fire - Beyond Gate", "Lyre, Lyre Pants on Fire - Beyond Gate - PF", "Lyre, Lyre Pants on Fire - Gate - PF",
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod) and (state.has("Infrarang", player) if options.frames_require_infra else True)),
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod) and (state.has("Infrarang", player) if options.frames_require_infra else True)))

    connect_regions(world, player, options, "Beyond the Black Stump", "Beyond the Black Stump - PF", "Beyond the Black Stump - PF",
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod) and (state.has("Infrarang", player) if options.frames_require_infra else True)),
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod) and (state.has("Infrarang", player) if options.frames_require_infra else True)))
    connect_regions(world, player, options, "Beyond the Black Stump", "Beyond the Black Stump - Upper Area", "Beyond the Black Stump - Upper Area",
                    lambda state: (state.has("Progressive Rang", player, 1 + pr_mod)) or state.has("Second Rang", player))
    connect_regions(world, player, options, "Beyond the Black Stump - Upper Area", "Beyond the Black Stump - Upper Area - PF", "Beyond the Black Stump - Upper Area - Rang Needed",
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod) and (state.has("Infrarang", player) if options.frames_require_infra else True)),
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod) and (state.has("Infrarang", player) if options.frames_require_infra else True)))

    connect_regions(world, player, options, "Rex Marks the Spot", "Rex Marks the Spot - PF", "Rex Marks the Spot, PF",
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod) and (state.has("Infrarang", player) if options.frames_require_infra else True)),
                    lambda state: (state.has("Progressive Rang", player, 0 + pr_mod) and (state.has("Infrarang", player) if options.frames_require_infra else True)))
    connect_regions(world, player, options, "Rex Marks the Spot", "Rex Marks the Spot - Underwater", "Rex Marks the Spot - Underwater",
                    lambda state: (state.has("Swim", player) or state.has("Dive", player) or state.has("Progressive Rang", player, 2)),
                    lambda state: (state.has("Swim", player) or state.has("Dive", player) or state.has("Progressive Rang", player, 2)))