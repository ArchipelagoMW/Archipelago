from BaseClasses import MultiWorld
from .Options import JakAndDaxterOptions
from .Regions import JakAndDaxterLevel, JakAndDaxterSubLevel, level_table, subLevel_table
from .Items import item_table


def set_rules(multiworld: MultiWorld, options: JakAndDaxterOptions, player: int):
    region_menu = multiworld.get_region("Menu", player)
    region_gr = multiworld.get_region(level_table[JakAndDaxterLevel.GEYSER_ROCK], player)
    region_menu.connect(region_gr)

    connect_regions(multiworld, player,
                    JakAndDaxterLevel.GEYSER_ROCK,
                    JakAndDaxterLevel.SANDOVER_VILLAGE,
                    lambda state: state.has(item_table[0], player, 4))

    connect_regions(multiworld, player,
                    JakAndDaxterLevel.SANDOVER_VILLAGE,
                    JakAndDaxterLevel.FORBIDDEN_JUNGLE)

    connect_region_to_sub(multiworld, player,
                          JakAndDaxterLevel.FORBIDDEN_JUNGLE,
                          JakAndDaxterSubLevel.FORBIDDEN_JUNGLE_PLANT_ROOM,
                          lambda state: state.has(item_table[2216], player))

    connect_regions(multiworld, player,
                    JakAndDaxterLevel.SANDOVER_VILLAGE,
                    JakAndDaxterLevel.SENTINEL_BEACH)

    connect_region_to_sub(multiworld, player,
                          JakAndDaxterLevel.SENTINEL_BEACH,
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

    connect_region_to_sub(multiworld, player,
                          JakAndDaxterLevel.BOGGY_SWAMP,
                          JakAndDaxterSubLevel.BOGGY_SWAMP_FLUT_FLUT,
                          lambda state: state.has(item_table[2215], player))

    connect_regions(multiworld, player,
                    JakAndDaxterLevel.ROCK_VILLAGE,
                    JakAndDaxterLevel.MOUNTAIN_PASS,
                    lambda state: state.has(item_table[2217], player) and state.has(item_table[0], player, 45))

    connect_region_to_sub(multiworld, player,
                          JakAndDaxterLevel.MOUNTAIN_PASS,
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

    connect_region_to_sub(multiworld, player,
                          JakAndDaxterLevel.SNOWY_MOUNTAIN,
                          JakAndDaxterSubLevel.SNOWY_MOUNTAIN_FLUT_FLUT,
                          lambda state: state.has(item_table[2215], player))

    connect_region_to_sub(multiworld, player,
                          JakAndDaxterLevel.SNOWY_MOUNTAIN,
                          JakAndDaxterSubLevel.SNOWY_MOUNTAIN_LURKER_FORT,
                          lambda state: state.has(item_table[2219], player))

    connect_regions(multiworld, player,
                    JakAndDaxterLevel.VOLCANIC_CRATER,
                    JakAndDaxterLevel.LAVA_TUBE,
                    lambda state: state.has(item_table[0], player, 72))

    connect_regions(multiworld, player,
                    JakAndDaxterLevel.LAVA_TUBE,
                    JakAndDaxterLevel.GOL_AND_MAIAS_CITADEL)

    connect_region_to_sub(multiworld, player,
                          JakAndDaxterLevel.GOL_AND_MAIAS_CITADEL,
                          JakAndDaxterSubLevel.GOL_AND_MAIAS_CITADEL_ROTATING_TOWER,
                          lambda state: state.has(item_table[2220], player)
                          and state.has(item_table[2221], player)
                          and state.has(item_table[2222], player))

    connect_subregions(multiworld, player,
                       JakAndDaxterSubLevel.GOL_AND_MAIAS_CITADEL_ROTATING_TOWER,
                       JakAndDaxterSubLevel.GOL_AND_MAIAS_CITADEL_FINAL_BOSS,
                       lambda state: state.has(item_table[2223], player))

    multiworld.completion_condition[player] = lambda state: state.can_reach(
        multiworld.get_region(subLevel_table[JakAndDaxterSubLevel.GOL_AND_MAIAS_CITADEL_FINAL_BOSS], player),
        "Region",
        player)


def connect_regions(multiworld: MultiWorld, player: int, source: JakAndDaxterLevel, target: JakAndDaxterLevel,
                    rule=None):
    source_region = multiworld.get_region(level_table[source], player)
    target_region = multiworld.get_region(level_table[target], player)
    source_region.connect(target_region, rule=rule)


def connect_region_to_sub(multiworld: MultiWorld, player: int, source: JakAndDaxterLevel, target: JakAndDaxterSubLevel,
                          rule=None):
    source_region = multiworld.get_region(level_table[source], player)
    target_region = multiworld.get_region(subLevel_table[target], player)
    source_region.connect(target_region, rule=rule)


def connect_subregions(multiworld: MultiWorld, player: int, source: JakAndDaxterSubLevel, target: JakAndDaxterSubLevel,
                       rule=None):
    source_region = multiworld.get_region(subLevel_table[source], player)
    target_region = multiworld.get_region(subLevel_table[target], player)
    source_region.connect(target_region, rule=rule)
