"""
Functions related to AP regions for Pokemon Emerald (see ./data/regions for region definitions)
"""
from typing import Tuple

from BaseClasses import ItemClassification, Region, MultiWorld

from .data import data
from .items import PokemonEmeraldItem
from .locations import PokemonEmeraldLocation


def _connect_to_map_encounters(multiworld: MultiWorld, player: int, region: Region, map_name: str, include_slots: Tuple[bool, bool, bool]):
        """
        Connects the provided region to the corresponding wild encounters for the given parent map.

        Each in-game map may have a non-physical Region for encountering wild pokemon in each of the three categories
        land, water, and fishing. Region data defines whether a given region includes places where those encounters can
        be accessed (i.e. whether the region has tall grass, a river bank, is on water, etc...).

        These regions are created dynamically so as not to bother with unused maps.
        """
        for i, slot_type in enumerate(["LAND", "WATER", "FISHING"]):
            if include_slots[i]:
                region_name = f"{map_name}_{slot_type}_ENCOUNTERS"

                try:
                    encounter_region = multiworld.get_region(region_name, player)
                except KeyError:
                    encounter_region = Region(region_name, player, multiworld)

                    unique_species = []
                    for species_id in getattr(data.maps[map_name], f"{slot_type.lower()}_encounters").slots:
                        if not species_id in unique_species:
                            unique_species.append(species_id)

                    for i, species_id in enumerate(unique_species):
                        encounter_location = PokemonEmeraldLocation(player, f"{region_name}_{i + 1}", None, encounter_region)
                        encounter_location.show_in_spoiler = False
                        encounter_location.place_locked_item(PokemonEmeraldItem(
                            f"CATCH_SPECIES_{species_id}",
                            ItemClassification.progression_skip_balancing,
                            None,
                            player
                        ))
                        encounter_region.locations.append(encounter_location)

                    multiworld.regions.append(encounter_region)

                region.connect(encounter_region, f"{region.name} -> {region_name}")


def create_regions(multiworld: MultiWorld, player: int) -> None:
    """
    Iterates through regions created from JSON to create regions and adds them to the multiworld.
    Also creates and places events and connects regions via warps and the exits defined in the JSON.
    """
    connections = []
    for region_name, region_data in data.regions.items():
        new_region = Region(region_name, player, multiworld)

        for event_data in region_data.events:
            event = PokemonEmeraldLocation(player, event_data.name, None, new_region)
            event.place_locked_item(PokemonEmeraldItem(event_data.name, ItemClassification.progression_skip_balancing, None, player))
            new_region.locations.append(event)

        for region_exit in region_data.exits:
            connections.append((f"{region_name} -> {region_exit}", region_name, region_exit))

        for warp in region_data.warps:
            dest_warp = data.warps[data.warp_map[warp]]
            if dest_warp.parent_region is None:
                continue
            connections.append((warp, region_name, dest_warp.parent_region))

        multiworld.regions.append(new_region)

        _connect_to_map_encounters(multiworld, player, new_region, region_data.parent_map.name,
                                   (region_data.has_grass, region_data.has_water, region_data.has_fishing))

    for name, source, dest in connections:
        multiworld.get_region(source, player).connect(multiworld.get_region(dest, player), name)

    menu = Region("Menu", player, multiworld)
    menu.connect(multiworld.get_region("REGION_LITTLEROOT_TOWN/MAIN", player), "Start Game")

    multiworld.regions.append(menu)
