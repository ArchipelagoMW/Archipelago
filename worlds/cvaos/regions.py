from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from BaseClasses import Entrance, Region

from .data import (
    entrance_info_collection,
    pickup_info_collection,
    entrance_to_entrance_info_collection,
    entrance_to_pickup_region_info_collection,
    default_transdoor_entrance_connection_collection,
    AbilityCombo,
)
from .locations import CVAOSLocation, location_name_to_id

if TYPE_CHECKING:
    from . import CVAOSWorld
    from BaseClasses import CollectionState

__all__ = [
    "create_regions",
]

def create_regions(world: CVAOSWorld) -> None:
    """
    Create all regions for Castlevania: Aria of Sorrow.

    This creates:
    1. A "Menu" region (required starting point)
    2. An entrance region for each EntranceInfo
    3. A pickup region for each PickupInfo
    4. Connections between regions based on RoutingInfo
    """
    multiworld = world.multiworld
    player = world.player

    # Create the Menu region (required starting point)
    menu = Region("Menu", player, multiworld)
    multiworld.regions.append(menu)

    # Track all regions by their identifier for easy lookup
    entrance_regions: dict[int, Region] = {}
    """e.g. door_number (1, 2, 3...) -> Region object"""  # pylint: disable=W0105
    pickup_regions: dict[str, Region] = {}
    """e.g. pickup_identifier -> Region object"""  # pylint: disable=W0105

    # Build lookups for routing connections
    # door_identifier_unique -> door_number
    door_id_unique_to_number: dict[str, int] = {
        e.door_identifier_unique: e.door_number for e in entrance_info_collection
    }
    # door_number -> door_identifier_unique
    door_number_to_id_unique: dict[int, str] = {
        e.door_number: e.door_identifier_unique for e in entrance_info_collection
    }
    # door_identifier_nonunique -> ordered door_numbers
    door_id_to_numbers: dict[str, list[int]] = {}
    for entrance_info in entrance_info_collection:
        door_id_to_numbers.setdefault(
            entrance_info.door_identifier_nonunique,
            [],
        ).append(entrance_info.door_number)

    # Create entrance regions (one per door/entrance in the game)
    # Use door_number as the unique key, region name uses door_identifier_unique
    for entrance_info in entrance_info_collection:
        region_name = f"Entrance: {entrance_info.door_identifier_unique}"
        region = Region(region_name, player, multiworld)
        entrance_regions[entrance_info.door_number] = region
        multiworld.regions.append(region)

    # Create pickup regions (one per pickup in the game)
    for pickup_info in pickup_info_collection:
        region_name = f"Pickup: {pickup_info.identifier_key}"
        region = Region(region_name, player, multiworld)
        pickup_regions[pickup_info.identifier_key] = region
        multiworld.regions.append(region)

        # Add the pickup as a location in its region
        location_name = pickup_info.identifier_key
        location_id = location_name_to_id[location_name]
        location = CVAOSLocation(player, location_name, location_id, region)
        region.locations.append(location)

    # Connect Menu to the starting entrance (000:003)
    start_entrance_id = "000:003"
    start_door_number = door_id_unique_to_number.get(start_entrance_id)
    if start_door_number is not None and start_door_number in entrance_regions:
        start_region = entrance_regions[start_door_number]
        menu.connect(start_region, "Start Game")
    elif entrance_info_collection:
        # Fallback if the starting entrance isn't found
        first_entrance = entrance_info_collection[0]
        start_region = entrance_regions[first_entrance.door_number]
        menu.connect(start_region, "Start Game")

    # Connect doors between rooms using the explicit transdoor table.
    transdoor_from_occurrence: dict[str, int] = {}
    transdoor_to_occurrence: dict[str, int] = {}
    for transdoor_info in default_transdoor_entrance_connection_collection:
        from_index = transdoor_from_occurrence.get(transdoor_info.from_entrance, 0)
        to_index = transdoor_to_occurrence.get(transdoor_info.to_entrance, 0)
        transdoor_from_occurrence[transdoor_info.from_entrance] = from_index + 1
        transdoor_to_occurrence[transdoor_info.to_entrance] = to_index + 1

        from_numbers = door_id_to_numbers.get(transdoor_info.from_entrance, [])
        to_numbers = door_id_to_numbers.get(transdoor_info.to_entrance, [])
        if from_index >= len(from_numbers) or to_index >= len(to_numbers):
            continue

        from_door_number = from_numbers[from_index]
        to_door_number = to_numbers[to_index]
        from_region = entrance_regions.get(from_door_number)
        to_region = entrance_regions.get(to_door_number)

        if from_region is None or to_region is None:
            continue

        from_door_id_unique = door_number_to_id_unique[from_door_number]
        to_door_id_unique = door_number_to_id_unique[to_door_number]
        connection_name = (
            f"Door: {from_door_id_unique} -> {to_door_id_unique}"
            f" #{transdoor_info.connection_number}"
        )
        from_region.connect(to_region, connection_name)

    # Connect regions based on routing information
    # Routing describes traversal within a room: from entry point to exit point
    # FROM = "{RoomID}:{From}" (entry point - door you came through)
    # TO = "{RoomID}:{To}" (exit point - door you're leaving through)
    for routing_info in entrance_to_entrance_info_collection:
        room_id = routing_info.room_id
        from_door_id = f"{room_id}:{routing_info.from_room}"
        to_door_id = f"{room_id}:{routing_info.to_room}"

        # Look up door_numbers for these door identifiers
        # door_id_unique is a superset of door_id_nonunique, so this works for non-duplicates
        from_door_number = door_id_unique_to_number.get(from_door_id)
        to_door_number = door_id_unique_to_number.get(to_door_id)

        if from_door_number is None or to_door_number is None:
            # Skip if we can't find both doors
            continue

        from_region = entrance_regions.get(from_door_number)
        to_region = entrance_regions.get(to_door_number)

        if from_region is None or to_region is None:
            # Skip connections where we can't find both regions
            continue

        # Create a descriptive name for this connection using unique IDs
        # Include connection_number to handle multiple routing entries between the same doors
        from_door_id_unique = door_number_to_id_unique[from_door_number]
        to_door_id_unique = door_number_to_id_unique[to_door_number]
        connection_name = f"{from_door_id_unique} -> {to_door_id_unique} #{routing_info.connection_number}"

        # Create an access rule based on the routing requirements
        access_rule = _create_access_rule_from_routing(routing_info, world)

        # Connect the regions
        from_region.connect(to_region, connection_name, access_rule)

    # Build pickup_number -> identifier_key lookup
    pickup_number_to_identifier: dict[int, str] = {
        p.pickup_number: p.identifier_key for p in pickup_info_collection
    }

    # Connect entrance regions to pickup regions
    for pickup_routing in entrance_to_pickup_region_info_collection:
        # The entrance_identifier may be unique or nonunique format
        # door_id_unique_to_number handles both since unique is a superset
        entrance_id = pickup_routing.entrance_identifier
        door_number = door_id_unique_to_number.get(entrance_id)

        if door_number is None:
            # Skip if we can't find this entrance
            continue

        entrance_region = entrance_regions.get(door_number)
        if entrance_region is None:
            continue

        # Look up the pickup region by pickup_number
        identifier_key = pickup_number_to_identifier.get(pickup_routing.pickup_number)
        if identifier_key is None:
            continue

        pickup_region = pickup_regions.get(identifier_key)
        if pickup_region is None:
            continue

        # Create connection name using pickup_number to ensure uniqueness
        entrance_id_unique = door_number_to_id_unique[door_number]
        connection_name = f"{entrance_id_unique} -> Pickup:{identifier_key} #{pickup_routing.pickup_number}"

        # Create access rule
        access_rule = _create_access_rule_from_routing(pickup_routing, world)

        # Connect entrance to pickup
        entrance_region.connect(pickup_region, connection_name, access_rule)


def _create_access_rule_from_routing(
    routing_info,
    world: CVAOSWorld,
) -> Callable[[CollectionState], bool] | None:
    """
    Create an access rule function from RoutingInfo.

    The RoutingInfo contains requirement bitmasks where each mask represents
    a different way to satisfy the requirement (disjunctive options).
    Each bit in a mask represents a required ability (conjunctive).

    Returns a lambda that checks if the player has any of the requirement combinations.
    """
    requirement_masks = routing_info.get_requirement_bitmasks()

    if not requirement_masks:
        # No requirements means always accessible
        return None

    # Ability flags to item names
    ability_to_item: dict[AbilityCombo, str] = {
        AbilityCombo.Glide: "Flying Armor",
        AbilityCombo.Slide: "Skeleton Blaze",
        AbilityCombo.DJump: "Malphas",
        AbilityCombo.HJump: "Hippogryph",
        AbilityCombo.WWalk: "Undine",
        AbilityCombo.Dive: "Skula",
        AbilityCombo.Panth: "Black Panther",
        AbilityCombo.Bat: "Giant Bat",
        AbilityCombo.BDash: "Grave Keeper",
        AbilityCombo.Kick: "Kicker Skeleton",
    }

    def access_rule(state: CollectionState) -> bool:
        """
        Check if any of the requirement combinations are satisfied.
        """
        player = world.player

        for mask in requirement_masks:
            # Check if this particular combination of abilities is satisfied
            requirements_met = True

            # Special case: mask == 0 means no requirements (always accessible)
            if mask == 0:
                return True

            # Check for Impossible flag
            if mask & AbilityCombo.Impossible:
                continue  # This path is impossible, try next mask

            # Check each ability bit
            for ability_flag, item_name in ability_to_item.items():
                if mask & ability_flag:
                    # This ability is required for this combination
                    if not state.has(item_name, player):
                        requirements_met = False
                        break

            # Special handling for technical requirements
            # These might need different logic based on your game's rules
            if mask & AbilityCombo.Enemy:
                # TODO: Implement enemy presence logic if needed
                pass
            if mask & AbilityCombo.PixPer:
                # TODO: Implement pixel-perfect platforming logic if needed
                # This might be controlled by an option
                pass
            if mask & AbilityCombo.Clip:
                # TODO: Implement platform clip logic if needed
                pass

            if requirements_met:
                return True

        # None of the requirement combinations were satisfied
        return False

    return access_rule
