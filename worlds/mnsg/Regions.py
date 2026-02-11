"""Region creation and management utilities for MN64."""

from typing import Any, Dict

from BaseClasses import Entrance, ItemClassification, Location, Region

from .Items import MN64Item, all_item_table, get_event_item_names, get_vanilla_item_names


def import_region_logic() -> Dict:
    """Import all region logic definitions and return combined regions dictionary."""
    from .Logic import (
        mn64_bizen,
        mn64_festival_temple_castle,
        mn64_folypoke_village,
        mn64_ghost_toys_castle,
        mn64_gorgeous_music_castle,
        mn64_gourmet_submarine,
        mn64_iyo,
        mn64_kai,
        mn64_musashi,
        mn64_mutsu,
        mn64_oedo_castle,
        mn64_oedo_town,
        mn64_sanuki,
        mn64_tosa,
        mn64_yamamoto,
        mn64_zazen_town,
    )

    # Collect all region definitions
    all_regions = {}
    all_regions.update(mn64_oedo_town.LogicRegions)
    all_regions.update(mn64_zazen_town.LogicRegions)
    all_regions.update(mn64_musashi.LogicRegions)
    all_regions.update(mn64_mutsu.LogicRegions)
    all_regions.update(mn64_yamamoto.LogicRegions)
    all_regions.update(mn64_sanuki.LogicRegions)
    all_regions.update(mn64_folypoke_village.LogicRegions)
    all_regions.update(mn64_tosa.LogicRegions)
    all_regions.update(mn64_iyo.LogicRegions)
    all_regions.update(mn64_kai.LogicRegions)
    all_regions.update(mn64_bizen.LogicRegions)
    all_regions.update(mn64_oedo_castle.LogicRegions)
    all_regions.update(mn64_ghost_toys_castle.LogicRegions)
    all_regions.update(mn64_festival_temple_castle.LogicRegions)
    all_regions.update(mn64_gorgeous_music_castle.LogicRegions)
    all_regions.update(mn64_gourmet_submarine.LogicRegions)

    return all_regions


def create_game_regions(world, all_regions: Dict, location_name_to_id: Dict) -> None:
    """Create all game regions and their locations."""
    # Import MN64Location here to avoid circular import
    from . import MN64Location
    
    event_item_names = get_event_item_names()
    vanilla_item_names = get_vanilla_item_names(world.options.randomize_health.value)

    for region_name, region_data in all_regions.items():
        region = Region(region_name, world.player, world.multiworld)

        # Add locations to region with unique names
        location_counter = {}  # Track duplicate names within same region
        for location_logic in region_data.locations:
            # Create unique location name using internal region name (without spaces)
            base_name = location_logic.name
            item_name = location_logic.item_type.value

            # Check if this location name was already used in this region
            if base_name in location_counter:
                location_counter[base_name] += 1
                unique_name = f"{region_name} - {base_name} {location_counter[base_name]}"
            else:
                location_counter[base_name] = 1
                unique_name = f"{region_name} - {base_name}"

            # Event locations have address None
            location_id = None if item_name in event_item_names else location_name_to_id.get(unique_name, None)
            location = MN64Location(world.player, unique_name, location_id, region)

            # Store metadata for this location
            store_location_metadata(world, location_logic, region_data, unique_name, item_name, location_id)

            # Place event items on event locations immediately
            if item_name in event_item_names:
                event_item = MN64Item(item_name, ItemClassification.progression, None, world.player)
                location.place_locked_item(event_item)
            # Place vanilla items (miracles and health) at their vanilla locations
            elif item_name in vanilla_item_names:
                vanilla_item = MN64Item(item_name, ItemClassification.progression, all_item_table[item_name].id, world.player)
                location.place_locked_item(vanilla_item)

            region.locations.append(location)

        world.multiworld.regions.append(region)


def store_location_metadata(world, location_logic, region_data, unique_name: str, item_name: str, location_id) -> None:
    """Store metadata for a location."""
    location_meta = {}
    if location_id is not None:
        location_meta["ap_location_id"] = location_id
    if hasattr(location_logic, "flag_id") and location_logic.flag_id is not None:
        location_meta["flag_id"] = location_logic.flag_id
    if hasattr(location_logic, "instance_id") and location_logic.instance_id is not None:
        location_meta["instance_id"] = location_logic.instance_id
    if hasattr(region_data, "room_id") and region_data.room_id is not None:
        location_meta["room_id"] = region_data.room_id

    # Store the original item that was at this location
    location_meta["original_item"] = item_name
    # Store the unique location name for reference
    location_meta["location_name"] = unique_name

    if location_meta and hasattr(region_data, "room_id") and region_data.room_id is not None:
        # Use room_id as key, but handle multiple locations per room
        room_id = region_data.room_id
        if room_id not in world.location_metadata:
            world.location_metadata[room_id] = []
        world.location_metadata[room_id].append(location_meta)


def connect_regions(world, all_regions: Dict, logger) -> None:
    """Create entrances between regions."""
    for region_name, region_data in all_regions.items():
        region = world.multiworld.get_region(region_name, world.player)

        for exit_logic in region_data.exits:
            # Check if destination region exists before creating entrance
            try:
                destination = world.multiworld.get_region(exit_logic.destinationRegion, world.player)
            except KeyError:
                # Destination region doesn't exist, skip this entrance
                logger.warning(f"Region {exit_logic.destinationRegion} not found for entrance from {region_name}")
                continue

            entrance = Entrance(world.player, f"{region_name} -> {exit_logic.destinationRegion}", region)
            region.exits.append(entrance)
            entrance.connect(destination)


def setup_starting_region(world, all_regions: Dict, logger) -> None:
    """Setup starting region connection from menu."""
    # Randomly select a starting region if option is enabled
    if world.options.starting_room_rando.value:
        possible_regions = [
            "GoemonsHouse",
            "ZazenTownEntrance",
            "FestivalVillageEntrance",
            "KaisCoffeeShop",
            "IyoCoffeeShop",
            "IzumoCoffeeShop",
            "KompurasCoffeeShop",
            "KiisCoffeeShop",
        ]
        starting_region_name = world.random.choice(possible_regions)
    else:
        # Default starting region
        starting_region_name = "GoemonsHouse"

    world.starting_region_name = starting_region_name  # Store for slot data

    # Store the room_id for the starting region
    starting_region_data = all_regions.get(starting_region_name)
    world.starting_room_id = getattr(starting_region_data, "room_id", None) if starting_region_data else None

    try:
        menu = world.multiworld.get_region("Menu", world.player)
        starting_region = world.multiworld.get_region(starting_region_name, world.player)
        menu_entrance = Entrance(world.player, "Start Game", menu)
        menu.exits.append(menu_entrance)
        menu_entrance.connect(starting_region)
    except KeyError:
        logger.warning(f"Could not find starting region {starting_region_name}")


def update_location_metadata(world) -> None:
    """Update location metadata with the actual items placed at each location."""
    for location in world.multiworld.get_locations(world.player):
        # Find the location in our room-based metadata structure
        for room_id, location_list in world.location_metadata.items():
            for location_meta in location_list:
                if location_meta["location_name"] == location.name:
                    if location.item:
                        location_meta["new_item"] = location.item.name
                        # Also include the new item's AP ID if it has one
                        if hasattr(location.item, "code") and location.item.code is not None:
                            location_meta["new_item_ap_id"] = location.item.code
                    else:
                        location_meta["new_item"] = None
                    break
