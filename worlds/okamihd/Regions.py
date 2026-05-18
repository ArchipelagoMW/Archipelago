from BaseClasses import Region, LocationProgressType
from rule_builder.rules import Rule, Has, HasAll, And, False_, True_
from .Enums.BrushTechniques import BrushTechniques
from .Enums.WarpType import WarpType
from .Locations import create_region_locations, create_region_events
from typing import TYPE_CHECKING, List
from .Rules import apply_exit_rules
from .Enums.RegionNames import RegionNames
from .RegionsData import okami_exits, okami_warps

if TYPE_CHECKING:
    from . import OkamiWorld


def get_region_name(key: str):
    if key in RegionNames:
        return RegionNames[key]


def create_regions(world: "OkamiWorld"):
    for r in RegionNames:
        reg = create_region(world, r.value)
        world.multiworld.regions.append(reg)
    # Second loop to create exits
    for r in RegionNames:
        reg = world.multiworld.get_region(r.value, world.player)
        create_region_exits(reg, world)
        # Only create warps entrances if we're using warp logic.
        if world.options.AccountForWarpsLogic.value == world.options.AccountForWarpsLogic.option_true:
            create_region_warps(reg, world)


def create_region(world: "OkamiWorld", region_name: str):
    reg = Region(region_name, world.player, world.multiworld)
    create_region_locations(reg, world)
    create_region_events(reg, world)
    return reg


def create_region_exits(reg: Region, world: "OkamiWorld"):
    if reg.name in okami_exits:
        for exit_data in okami_exits[reg.name]:
            exiting_region = world.multiworld.get_region(exit_data.destination, world.player)
            exit_name = reg.name + ' -> ' + exiting_region.name
            ext = reg.connect(exiting_region, exit_name)
            apply_exit_rules(ext, ext.name, exit_data, world)
            if not exit_data.one_way:
                reverse_exit_name = exiting_region.name + ' -> ' + reg.name
                rev_ext = exiting_region.connect(reg, reverse_exit_name)
                apply_exit_rules(rev_ext, rev_ext.name, exit_data, world)


def create_region_warps(reg: Region, world: "OkamiWorld"):
    if reg.name in okami_warps:
        for warp_data in okami_warps[reg.name]:
            # Partial support for Mermaid Springs
            if warp_data.type == WarpType.MIST_WARP:
                hub = world.multiworld.get_region(RegionNames.MIST_WARP_HUB.value, world.player)
                # Requirements for Mist Warp
                hub_access_rule = Has(BrushTechniques.MIST_WARP)
            else:
                hub = world.multiworld.get_region(RegionNames.MERMAID_SPRING_HUB.value, world.player)
                # Requirements to use Mermaid Spring - Figure out a way to account for mermaid coins
                hub_access_rule = Has(BrushTechniques.FOUNTAIN)

            # If False we don't even create a way to warp from this place
            if warp_data.trigger_warp_from != False_:
                from_name = reg.name + ' (' + warp_data.type.value + ') -> ' + hub.name
                warp_from = reg.connect(hub, from_name)
                if warp_data.trigger_warp_from != True_:
                    world.set_rule(warp_from, And(hub_access_rule, warp_data.trigger_warp_from))
                else:
                    world.set_rule(warp_from, hub_access_rule)

            # IF False we don't even create a way to warp to this place
            if warp_data.trigger_warp_to != False_:
                to_name = hub.name + ' -> ' + reg.name + ' (' + warp_data.type.value + ')'
                warp_to = hub.connect(reg, to_name)
                if warp_data.trigger_warp_from != True_:
                    world.set_rule(warp_to, warp_data.trigger_warp_from)
                # No need to check if we have the power/coin to get out of the hub.


def get_region_location_count(world: "OkamiWorld", region_name: str, included_only: bool = True) -> int:
    count = 0
    region = world.multiworld.get_region(region_name, world.player)
    for loc in region.locations:
        if loc.address is not None and (not included_only or loc.progress_type is not LocationProgressType.EXCLUDED):
            count += 1

    return count
