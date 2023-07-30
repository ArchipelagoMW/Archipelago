"""
Functions related to AP regions for Pokemon Emerald (see ./data/regions for region definitions)
"""
from typing import Dict

from BaseClasses import Entrance, ItemClassification, Region, MultiWorld

from .data import data
from .items import PokemonEmeraldItem
from .locations import PokemonEmeraldLocation


def create_regions(multiworld: MultiWorld, player: int) -> None:
    """
    Iterates through regions created from JSON to create regions and adds them to the multiworld.
    Also creates and places events and connects regions via warps and the exits defined in the JSON.
    """
    regions: Dict[str, Region] = {}

    connections = []
    for region_name, region_data in data.regions.items():
        new_region = Region(region_name, player, multiworld)

        for event_data in region_data.events:
            event = PokemonEmeraldLocation(player, event_data.name, None, new_region)
            event.place_locked_item(PokemonEmeraldItem(event_data.name, ItemClassification.progression, None, player))
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
        connection = Entrance(player, name, regions[source])
        regions[source].exits.append(connection)
        connection.connect(regions[dest])

    menu = Region("Menu", player, multiworld)
    connection = Entrance(player, "Start Game", menu)
    menu.exits.append(connection)
    connection.connect(regions["REGION_LITTLEROOT_TOWN/MAIN"])
    regions["Menu"] = menu

    multiworld.regions += regions.values()
