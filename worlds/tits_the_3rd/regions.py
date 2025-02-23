"""This module represents region definitions for Trails in the Sky the 3rd"""
from typing import Callable, Optional

from .names.region_name import RegionName
from BaseClasses import CollectionState, MultiWorld, Region

def create_region(multiworld: MultiWorld, player: int, name: str):
    """Create a region for Trails in the Sky the 3rd"""
    region = Region(name, player, multiworld)
    multiworld.regions.append(region)

def connect_region(
    multiworld: MultiWorld,
    player: int,
    from_region_name: str,
    to_region_name: str,
    rule: Optional[Callable[[CollectionState], bool]] = None
):
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
    create_region(multiworld, player, RegionName.jade_corridor_post_tita_gate)
    create_region(multiworld, player, RegionName.jade_corridor_post_julia_gate)

def connect_regions(multiworld: MultiWorld, player: int):
    """Connect AP regions for Trails in the Sky the 3rd"""
    connect_region(multiworld, player, RegionName.menu, RegionName.lusitania)

    connect_region(multiworld, player, RegionName.lusitania, RegionName.hermit_garden)
    connect_region(multiworld, player, RegionName.hermit_garden, RegionName.lusitania)

    connect_region(multiworld, player, RegionName.hermit_garden, RegionName.jade_corridor_start)
    connect_region(multiworld, player, RegionName.jade_corridor_start, RegionName.hermit_garden)

    connect_region(multiworld, player, RegionName.jade_corridor_start, RegionName.jade_corridor_post_tita_gate)
    connect_region(multiworld, player, RegionName.jade_corridor_post_tita_gate, RegionName.jade_corridor_start)

    connect_region(multiworld, player, RegionName.jade_corridor_post_tita_gate, RegionName.jade_corridor_post_julia_gate)
    connect_region(multiworld, player, RegionName.jade_corridor_post_julia_gate, RegionName.jade_corridor_post_tita_gate)

    # Assume the warp menu is always reachable, but add access rules to specific warps.
    connect_region(multiworld, player, RegionName.menu, RegionName.warp_menu)
    connect_region( # Jade Corridor Moon Door 1
        multiworld, player, RegionName.warp_menu, RegionName.jade_corridor_start,
        lambda state: state.can_reach_region(RegionName.jade_corridor_start, player)
    )
    connect_region( # Jade Corridor first warp + Sun Door One
        multiworld, player, RegionName.warp_menu, RegionName.jade_corridor_post_tita_gate,
        lambda state: state.can_reach_region(RegionName.jade_corridor_post_tita_gate, player)
    )
    connect_region( # Jade Corridor second warp
        multiworld, player, RegionName.warp_menu, RegionName.jade_corridor_post_julia_gate,
        lambda state: state.can_reach_region(RegionName.jade_corridor_post_julia_gate, player)
    )
