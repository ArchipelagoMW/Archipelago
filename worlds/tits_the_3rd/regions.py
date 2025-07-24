"""This module represents region definitions for Trails in the Sky the 3rd"""

from typing import Callable, Optional

from worlds.tits_the_3rd.names.item_name import ItemName
from worlds.tits_the_3rd.names.region_name import RegionName
from BaseClasses import CollectionState, MultiWorld, Region


chapter_1_combat_regions = [
    RegionName.jade_corridor_start,
    RegionName.jade_corridor_expansion_area_1,
    RegionName.jade_corridor_expansion_area_2,
]


def create_region(multiworld: MultiWorld, player: int, name: str):
    """Create a region for Trails in the Sky the 3rd"""
    region = Region(name, player, multiworld)
    multiworld.regions.append(region)


def connect_region(multiworld: MultiWorld, player: int, from_region_name: str, to_region_name: str, rule: Optional[Callable[[CollectionState], bool]] = None):
    """Connect a region to another region for Trails in the Sky the 3rd"""
    from_region = multiworld.get_region(from_region_name, player)
    to_region = multiworld.get_region(to_region_name, player)
    from_region.connect(to_region, rule=rule)


def create_regions(multiworld: MultiWorld, player: int):
    """Define AP regions for Trails in the Sky the 3rd"""
    create_region(multiworld, player, RegionName.menu)
    create_region(multiworld, player, RegionName.warp_menu)
    create_region(multiworld, player, RegionName.lusitania)
    create_region(multiworld, player, RegionName.hermit_garden)
    create_region(multiworld, player, RegionName.jade_corridor_start)
    create_region(multiworld, player, RegionName.jade_corridor_expansion_area_1)
    create_region(multiworld, player, RegionName.jade_corridor_expansion_area_2)
    create_region(multiworld, player, RegionName.jade_corridor_arseille)
    create_region(multiworld, player, RegionName.level_90)
    create_region(multiworld, player, RegionName.level_95)
    create_region(multiworld, player, RegionName.level_103)
    create_region(multiworld, player, RegionName.level_105)
    create_region(multiworld, player, RegionName.level_111)
    create_region(multiworld, player, RegionName.level_116)
    create_region(multiworld, player, RegionName.level_124)
    create_region(multiworld, player, RegionName.level_133)
    create_region(multiworld, player, RegionName.level_136)

    create_region(multiworld, player, RegionName.day_grancel_south)
    create_region(multiworld, player, RegionName.day_grancel_north)
    create_region(multiworld, player, RegionName.day_grancel_west)
    create_region(multiworld, player, RegionName.day_grancel_east)
    create_region(multiworld, player, RegionName.day_grancel_port)
    create_region(multiworld, player, RegionName.night_grancel_south)
    create_region(multiworld, player, RegionName.night_grancel_north)
    create_region(multiworld, player, RegionName.night_grancel_west)
    create_region(multiworld, player, RegionName.night_grancel_east)
    create_region(multiworld, player, RegionName.night_grancel_port)
    create_region(multiworld, player, RegionName.grancel_castle)


def connect_regions(multiworld: MultiWorld, player: int):
    """Connect AP regions for Trails in the Sky the 3rd"""
    connect_region(
        multiworld,
        player,
        RegionName.menu,
        RegionName.hermit_garden
    )

    connect_region(
        multiworld,
        player,
        RegionName.hermit_garden,
        RegionName.lusitania
    )
    connect_region(
        multiworld,
        player,
        RegionName.lusitania,
        RegionName.hermit_garden
    )

    connect_region(
        multiworld,
        player,
        RegionName.hermit_garden,
        RegionName.jade_corridor_start
    )
    connect_region(
        multiworld,
        player,
        RegionName.jade_corridor_start,
        RegionName.hermit_garden
    )

    connect_region(
        multiworld,
        player,
        RegionName.jade_corridor_start,
        RegionName.jade_corridor_expansion_area_1,
        lambda state: state.has(ItemName.jade_corridor_unlock_1, player, 1)
    )
    connect_region(
        multiworld,
        player,
        RegionName.jade_corridor_expansion_area_1,
        RegionName.jade_corridor_start,
        lambda state: state.has(ItemName.jade_corridor_unlock_1, player, 1)
    )

    connect_region(
        multiworld,
        player,
        RegionName.jade_corridor_expansion_area_1,
        RegionName.jade_corridor_expansion_area_2,
        lambda state: state.has(ItemName.jade_corridor_unlock_2, player, 1),
    )
    connect_region(
        multiworld,
        player,
        RegionName.jade_corridor_expansion_area_2,
        RegionName.jade_corridor_expansion_area_1,
        lambda state: state.has(ItemName.jade_corridor_unlock_2, player, 1),
    )

    connect_region(
        multiworld,
        player,
        RegionName.jade_corridor_expansion_area_1,
        RegionName.jade_corridor_arseille,
        lambda state: state.has(ItemName.jade_corridor_arseille_unlock, player, 1)
    )
    connect_region(
        multiworld,
        player,
        RegionName.jade_corridor_arseille,
        RegionName.jade_corridor_expansion_area_1,
        lambda state: state.has(ItemName.jade_corridor_arseille_unlock, player, 1)
    )

    connect_region(
        multiworld,
        player,
        RegionName.jade_corridor_expansion_area_2,
        RegionName.night_grancel_south,
    )
    connect_region(
        multiworld,
        player,
        RegionName.night_grancel_south,
        RegionName.jade_corridor_expansion_area_2,
    )

    connect_region(
        multiworld,
        player,
        RegionName.night_grancel_south,
        RegionName.night_grancel_north,
    )
    connect_region(
        multiworld,
        player,
        RegionName.night_grancel_north,
        RegionName.night_grancel_south,
    )

    connect_region(
        multiworld,
        player,
        RegionName.night_grancel_south,
        RegionName.night_grancel_east,
    )
    connect_region(
        multiworld,
        player,
        RegionName.night_grancel_east,
        RegionName.night_grancel_south,
    )

    connect_region(
        multiworld,
        player,
        RegionName.night_grancel_south,
        RegionName.night_grancel_west,
    )
    connect_region(
        multiworld,
        player,
        RegionName.night_grancel_west,
        RegionName.night_grancel_south,
    )

    connect_region(
        multiworld,
        player,
        RegionName.night_grancel_west,
        RegionName.night_grancel_north,
    )
    connect_region(
        multiworld,
        player,
        RegionName.night_grancel_north,
        RegionName.night_grancel_west,
    )

    connect_region(
        multiworld,
        player,
        RegionName.night_grancel_east,
        RegionName.night_grancel_north,
    )
    connect_region(
        multiworld,
        player,
        RegionName.night_grancel_north,
        RegionName.night_grancel_east,
    )

    connect_region(
        multiworld,
        player,
        RegionName.night_grancel_west,
        RegionName.night_grancel_port,
    )
    connect_region(
        multiworld,
        player,
        RegionName.night_grancel_port,
        RegionName.night_grancel_west,
    )

    connect_region(
        multiworld,
        player,
        RegionName.night_grancel_north,
        RegionName.grancel_castle,
    )
    connect_region(
        multiworld,
        player,
        RegionName.grancel_castle,
        RegionName.night_grancel_north,
    )

    # Assume the warp menu is always reachable, but add access rules to specific warps.
    connect_region(
        multiworld,
        player,
        RegionName.menu,
        RegionName.warp_menu
    )
    connect_region(
        multiworld,
        player,
        RegionName.warp_menu,
        RegionName.hermit_garden,
        lambda state: state.can_reach_region(RegionName.hermit_garden, player)
    )
    connect_region(
        multiworld,
        player,
        RegionName.warp_menu,
        RegionName.jade_corridor_start,
        lambda state: state.can_reach_region(RegionName.jade_corridor_start, player)
    )  # Jade Corridor Moon Door 1
    connect_region(  # Jade Corridor first warp + Sun Door One
        multiworld,
        player,
        RegionName.warp_menu,
        RegionName.jade_corridor_expansion_area_1,
        lambda state: state.can_reach_region(RegionName.jade_corridor_expansion_area_1, player)
    )
    connect_region(  # Jade Corridor second warp
        multiworld,
        player,
        RegionName.warp_menu,
        RegionName.jade_corridor_expansion_area_2,
        lambda state: state.can_reach_region(RegionName.jade_corridor_expansion_area_2, player)
    )

    # Assuming no progression balancing for now:
    connect_region(multiworld, player, RegionName.hermit_garden, RegionName.level_90)

    for region in chapter_1_combat_regions:
        connect_region(multiworld, player, region, RegionName.level_90)
        connect_region(multiworld, player, region, RegionName.level_95)
