import typing
from BaseClasses import MultiWorld
from .Options import JakAndDaxterOptions
from .Locations import JakAndDaxterLocation, location_table
from .Regions import JakAndDaxterLevel, JakAndDaxterSubLevel, JakAndDaxterRegion, level_table, subLevel_table
from .Items import item_table

def set_rules(multiworld: MultiWorld, options: JakAndDaxterOptions, player: int):

    menuRegion = multiworld.get_region("Menu", player)
    grRegion = multiworld.get_region(level_table[JakAndDaxterLevel.GEYSER_ROCK], player)
    menuRegion.connect(grRegion)

    connect_regions(multiworld, player,
        JakAndDaxterLevel.GEYSER_ROCK,
        JakAndDaxterLevel.SANDOVER_VILLAGE,
        lambda state: state.has(item_table[0], player, 4))

    connect_regions(multiworld, player,
        JakAndDaxterLevel.SANDOVER_VILLAGE,
        JakAndDaxterLevel.FORBIDDEN_JUNGLE)

    assign_subregion_access_rule(multiworld, player, 
        JakAndDaxterSubLevel.FORBIDDEN_JUNGLE_PLANT_ROOM,
        lambda state: state.has(item_table[2216], player))

    connect_regions(multiworld, player,
        JakAndDaxterLevel.SANDOVER_VILLAGE,
        JakAndDaxterLevel.SENTINEL_BEACH)

    assign_subregion_access_rule(multiworld, player, 
        JakAndDaxterSubLevel.SENTINEL_BEACH_CANNON_TOWER,
        lambda state: state.has(item_table[2216], player))

    connect_regions(multiworld, player,
        JakAndDaxterLevel.SANDOVER_VILLAGE,
        JakAndDaxterLevel.MISTY_ISLAND,
        lambda state: state.has(item_table[2213], player))

    connect_regions(multiworld, player,
        JakAndDaxterLevel.SANDOVER_VILLAGE,
        JakAndDaxterLevel.FIRE_CANYON,
        lambda state: state.has(item_table[0], player, 20))

    connect_regions(multiworld, player,
        JakAndDaxterLevel.FIRE_CANYON,
        JakAndDaxterLevel.ROCK_VILLAGE)

    connect_regions(multiworld, player,
        JakAndDaxterLevel.ROCK_VILLAGE,
        JakAndDaxterLevel.PRECURSOR_BASIN)

    connect_regions(multiworld, player,
        JakAndDaxterLevel.ROCK_VILLAGE,
        JakAndDaxterLevel.LOST_PRECURSOR_CITY)

    connect_regions(multiworld, player,
        JakAndDaxterLevel.ROCK_VILLAGE,
        JakAndDaxterLevel.BOGGY_SWAMP,
        lambda state: state.has(item_table[2217], player))

    assign_subregion_access_rule(multiworld, player, 
        JakAndDaxterSubLevel.BOGGY_SWAMP_FLUT_FLUT,
        lambda state: state.has(item_table[2215], player))

    connect_regions(multiworld, player,
        JakAndDaxterLevel.ROCK_VILLAGE,
        JakAndDaxterLevel.MOUNTAIN_PASS,
        lambda state: state.has(item_table[2217], player) and state.has(item_table[0], player, 45))

    assign_subregion_access_rule(multiworld, player, 
        JakAndDaxterSubLevel.MOUNTAIN_PASS_SHORTCUT,
        lambda state: state.has(item_table[2218], player))

    connect_regions(multiworld, player,
        JakAndDaxterLevel.MOUNTAIN_PASS,
        JakAndDaxterLevel.VOLCANIC_CRATER)

    connect_regions(multiworld, player,
        JakAndDaxterLevel.VOLCANIC_CRATER,
        JakAndDaxterLevel.SPIDER_CAVE)

    connect_regions(multiworld, player,
        JakAndDaxterLevel.VOLCANIC_CRATER,
        JakAndDaxterLevel.SNOWY_MOUNTAIN)

    assign_subregion_access_rule(multiworld, player, 
        JakAndDaxterSubLevel.SNOWY_MOUNTAIN_FLUT_FLUT,
        lambda state: state.has(item_table[2215], player))

    assign_subregion_access_rule(multiworld, player, 
        JakAndDaxterSubLevel.SNOWY_MOUNTAIN_LURKER_FORT,
        lambda state: state.has(item_table[2219], player))

    connect_regions(multiworld, player,
        JakAndDaxterLevel.VOLCANIC_CRATER,
        JakAndDaxterLevel.LAVA_TUBE,
        lambda state: state.has(item_table[0], player, 72))

    connect_regions(multiworld, player,
        JakAndDaxterLevel.LAVA_TUBE,
        JakAndDaxterLevel.GOL_AND_MAIAS_CITADEL)

    assign_subregion_access_rule(multiworld, player, 
        JakAndDaxterSubLevel.GOL_AND_MAIAS_CITADEL_ROTATING_TOWER,
        lambda state: state.has(item_table[96], player) and state.has(item_table[97], player) and state.has(item_table[98], player))

def connect_regions(multiworld: MultiWorld, player: int, source: int, target: int, rule = None):
    sourceRegion = multiworld.get_region(level_table[source], player)
    targetRegion = multiworld.get_region(level_table[target], player)
    sourceRegion.connect(targetRegion, rule = rule)

def assign_subregion_access_rule(multiworld: MultiWorld, player: int, target: int, rule = None):
    targetEntrance = multiworld.get_entrance(subLevel_table[target], player)
    targetEntrance.access_rule = rule
