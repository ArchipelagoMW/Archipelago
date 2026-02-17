"""
Functions related to AP regions for Kirby & The Amazing Mirror
(see ./data/regions for region definitions)
"""
from typing import TYPE_CHECKING, Dict, List, Tuple

from BaseClasses import ItemClassification, Region

from .data import data
from .items import KirbyAmItem
from .locations import KirbyAmLocation

if TYPE_CHECKING:
    from . import KirbyAmWorld


def create_regions(world: "KirbyAmWorld") -> dict[str, Region]:
    """
    Create Regions from JSON, add event Locations, and connect Regions via exits and warps.
    Returns a name -> Region mapping for convenience.
    """
    regions: dict[str, Region] = {}
    connections: list[tuple[str, str, str]] = []

    # 1) Instantiate all regions, populate their real locations and event locations
    for region_name, region_data in data.regions.items():
        region = Region(region_name, world.player, world.multiworld)

        # Add fillable locations from JSON
        for loc_key in region_data.locations:
            loc_meta = data.locations[loc_key]
            region.locations.append(
                KirbyAmLocation(
                    world.player,
                    loc_meta.label,
                    loc_meta.location_id,
                    region,
                    key=loc_key,
                    default_item_code=loc_meta.default_item,
                )
            )

        for event_data in region_data.events:
            loc = KirbyAmLocation(world.player, event_data.name, None, region)
            loc.place_locked_item(
                KirbyAmItem(event_data.name, ItemClassification.progression, None, world.player)
            )
            region.locations.append(loc)

        regions[region_name] = region
        world.multiworld.regions.append(region)

        # Collect region exits
        for region_exit in region_data.exits:
            connections.append((f"{region_name} -> {region_exit}", region_name, region_exit))

        # Collect warp connections (warp name -> destination parent region)
        for warp in region_data.warps:
            dest_key = data.warp_map.get(warp)
            if not dest_key:
                continue

            dest_warp = data.warps.get(dest_key)
            if not dest_warp or dest_warp.parent_region is None:
                continue

            connections.append((warp, region_name, dest_warp.parent_region))

    # 2) Connect regions (after all are created)
    for entrance_name, source_name, dest_name in connections:
        source = regions.get(source_name)
        dest = regions.get(dest_name)
        if source is None or dest is None:
            continue
        source.connect(dest, entrance_name)

    # 3) Add Menu region and start connection
    menu = Region("Menu", world.player, world.multiworld)
    regions["Menu"] = menu
    world.multiworld.regions.append(menu)

    start_region = regions.get("REGION_GAME_START")
    if start_region is not None:
        menu.connect(start_region, "Start Game")

    return regions
