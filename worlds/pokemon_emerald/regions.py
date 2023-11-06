"""
Functions related to AP regions for Pokemon Emerald (see ./data/regions for region definitions)
"""
from typing import TYPE_CHECKING, Dict, List, Tuple

from BaseClasses import ItemClassification, Region

from .data import data
from .items import PokemonEmeraldItem
from .locations import PokemonEmeraldLocation

if TYPE_CHECKING:
    from . import PokemonEmeraldWorld


def create_regions(world: "PokemonEmeraldWorld") -> Dict[str, Region]:
    """
    Iterates through regions created from JSON to create regions and adds them to the multiworld.
    Also creates and places events and connects regions via warps and the exits defined in the JSON.
    """
    regions: Dict[str, Region] = {}
    connections: List[Tuple[str, str, str]] = []

    for region_name, region_data in data.regions.items():
        new_region = Region(region_name, world.player, world.multiworld)

        for event_data in region_data.events:
            event = PokemonEmeraldLocation(world.player, event_data.name, None, new_region)
            event.place_locked_item(PokemonEmeraldItem(event_data.name, ItemClassification.progression, None, world.player))
            new_region.locations.append(event)

        for region_exit in region_data.exits:
            connections.append((f"{region_name} -> {region_exit}", region_name, region_exit))

        for warp in region_data.warps:
            dest_warp = data.warps[data.warp_map[warp]]
            if dest_warp.parent_region is None:
                continue
            connections.append((warp, region_name, dest_warp.parent_region))

        regions[region_name] = new_region

    for name, source, dest in connections:
        regions[source].connect(regions[dest], name)

    regions["Menu"] = Region("Menu", world.player, world.multiworld)
    regions["Menu"].connect(regions["REGION_LITTLEROOT_TOWN/MAIN"], "Start Game")

    return regions
