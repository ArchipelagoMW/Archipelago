"""
Functions related to AP regions for Pokemon Emerald (see ./data/regions for region definitions)
"""
from typing import TYPE_CHECKING, Callable, Dict, List, Optional, Tuple

from BaseClasses import CollectionState, ItemClassification, Region

from .data import EncounterType, data
from .items import PokemonEmeraldItem
from .locations import PokemonEmeraldLocation

if TYPE_CHECKING:
    from . import PokemonEmeraldWorld


def create_regions(world: "PokemonEmeraldWorld") -> Dict[str, Region]:
    """
    Iterates through regions created from JSON to create regions and adds them to the multiworld.
    Also creates and places events and connects regions via warps and the exits defined in the JSON.
    """
    # Used in connect_to_map_encounters. Splits encounter categories into "subcategories" and gives them names
    # and rules so the rods can only access their specific slots. Rock smash encounters are not considered in logic.
    encounter_categories: Dict[EncounterType, List[Tuple[Optional[str], range, Optional[Callable[[CollectionState], bool]]]]] = {
        EncounterType.LAND: [(None, range(0, 12), None)],
        EncounterType.WATER: [(None, range(0, 5), None)],
        EncounterType.FISHING: [
            ("OLD_ROD", range(0, 2), lambda state: state.has("Old Rod", world.player)),
            ("GOOD_ROD", range(2, 5), lambda state: state.has("Good Rod", world.player)),
            ("SUPER_ROD", range(5, 10), lambda state: state.has("Super Rod", world.player)),
        ],
    }

    def connect_to_map_encounters(region: Region, map_name: str, include_slots: Tuple[bool, bool, bool]):
        """
        Connects the provided region to the corresponding wild encounters for the given parent map.

        Each in-game map may have a non-physical Region for encountering wild pokemon in each of the three categories
        land, water, and fishing. Region data defines whether a given region includes places where those encounters can
        be accessed (i.e. whether the region has tall grass, a river bank, is on water, etc.).

        These regions are created lazily and dynamically so as not to bother with unused maps.
        """
        # For each of land, water, and fishing, connect the region if indicated by include_slots
        for i, (encounter_type, subcategories) in enumerate(encounter_categories.items()):
            if include_slots[i]:
                region_name = f"{map_name}_{encounter_type.value}_ENCOUNTERS"

                # If the region hasn't been created yet, create it now
                try:
                    encounter_region = world.multiworld.get_region(region_name, world.player)
                except KeyError:
                    encounter_region = Region(region_name, world.player, world.multiworld)
                    encounter_slots = data.maps[map_name].encounters[encounter_type].slots

                    # Subcategory is for splitting fishing rods; land and water only have one subcategory
                    for subcategory in subcategories:
                        # Want to create locations per species, not per slot
                        # encounter_categories includes info on which slots belong to which subcategory
                        unique_species = []
                        for j, species_id in enumerate(encounter_slots):
                            if j in subcategory[1] and not species_id in unique_species:
                                unique_species.append(species_id)

                        # Create a location for the species
                        for j, species_id in enumerate(unique_species):
                            encounter_location = PokemonEmeraldLocation(
                                world.player,
                                f"{region_name}{'_' + subcategory[0] if subcategory[0] is not None else ''}_{j + 1}",
                                None,
                                encounter_region
                            )
                            encounter_location.show_in_spoiler = False

                            # Add access rule
                            if subcategory[2] is not None:
                                encounter_location.access_rule = subcategory[2]

                            # Fill the location with an event for catching that species
                            encounter_location.place_locked_item(PokemonEmeraldItem(
                                f"CATCH_{data.species[species_id].name}",
                                ItemClassification.progression_skip_balancing,
                                None,
                                world.player
                            ))
                            encounter_region.locations.append(encounter_location)

                    # Add the new encounter region to the multiworld
                    world.multiworld.regions.append(encounter_region)

                # Encounter region exists, just connect to it
                region.connect(encounter_region, f"{region.name} -> {region_name}")

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

        connect_to_map_encounters(new_region, region_data.parent_map.name,
                                  (region_data.has_grass, region_data.has_water, region_data.has_fishing))

    for name, source, dest in connections:
        regions[source].connect(regions[dest], name)

    regions["Menu"] = Region("Menu", world.player, world.multiworld)
    regions["Menu"].connect(regions["REGION_LITTLEROOT_TOWN/MAIN"], "Start Game")

    return regions
