"""Enemy randomization and memory management utilities for MN64."""

from typing import Dict

from .Items import all_item_table


def get_enemy_pool(enemy_rando_enabled: bool):
    """Return the list of all enemies available for randomization."""
    all_enemies = [
        0x0FB,
        0x0FC,
        0x0FD,
        0x100,
        0x103,
        0x12C,
        0x12D,
        0x130,
        0x0FF,
        0x10F,
        0x106,
        0x132,
        0x133,
        0x145,
        0x148,
        0x105,
        0x10C,
        0x13C,
        0x13D,
        0x13F,
        0x147,
        0x13E,
        0x140,
        0x141,
        0x190,
        0x108,
        0x109,
        0x10A,
        0x10B,
        0x12E,
        0x12F,
        0x144,
    ]

    # If enemy randomization is disabled, clear the enemy pool to skip randomization
    # while still performing memory management
    if not enemy_rando_enabled:
        return []

    return all_enemies


def randomize_all_enemies(world, all_regions: Dict, all_enemies, RESTRICTED_ENEMIES, RESTRICTED_ENEMY_ROOMS) -> None:
    """Randomize enemies in each room with memory constraints."""
    for region_name, region_data in all_regions.items():
        # Check if this region has a room with enemies
        if hasattr(region_data, "enemies") and region_data.enemies and hasattr(region_data, "room_id"):
            room_id = region_data.room_id

            # Initialize storage for this room's enemy data
            if room_id not in world.randomized_enemy_data:
                world.randomized_enemy_data[room_id] = {}

            # Try normal enemy randomization first
            success = try_enemy_randomization(world, region_data, room_id, all_enemies, RESTRICTED_ENEMIES, RESTRICTED_ENEMY_ROOMS)

            # If normal randomization failed, apply extreme memory reduction
            if not success:
                success = apply_extreme_memory_reduction(world, region_name, region_data, room_id, all_enemies, RESTRICTED_ENEMIES)

            # If still failing, raise error
            if not success:
                raise_memory_error(region_name, room_id)


def try_enemy_randomization(world, region_data, room_id: int, all_enemies, RESTRICTED_ENEMIES, RESTRICTED_ENEMY_ROOMS) -> bool:
    """Try normal enemy randomization with memory constraints. Returns success status."""
    max_attempts = 5
    attempt = 0
    current_enemy_pool = all_enemies.copy()

    # If this room is in RESTRICTED_ENEMY_ROOMS, exclude restricted enemies
    if room_id in RESTRICTED_ENEMY_ROOMS:
        current_enemy_pool = [e for e in current_enemy_pool if e not in RESTRICTED_ENEMIES]

    while attempt < max_attempts:
        attempt += 1
        temp_enemy_config = select_enemy_configuration(world, region_data, current_enemy_pool, all_enemies)

        # Test memory with this enemy configuration
        current_files, total_size, under_budget = calculate_room_memory(world, region_data, temp_enemy_config)

        if under_budget:
            # Success! Apply this configuration
            for instance_id, enemy_id in temp_enemy_config.items():
                region_data.enemies[instance_id] = enemy_id
                world.randomized_enemy_data[room_id][instance_id] = enemy_id

            # Update room default definitions
            region_data.room_default_definitions = current_files
            return True

    return False


def select_enemy_configuration(world, region_data, current_enemy_pool, all_enemies) -> Dict:
    """Select enemy configuration for a room, optimizing for memory usage."""
    from .file_memory_sizes import ENEMY_FILES, entities_dict

    temp_enemy_config = {}
    max_enemy_types = 3
    num_types_to_select = min(max_enemy_types, len(current_enemy_pool))

    # First, select random enemy types
    selected_enemy_types = world.random.sample(current_enemy_pool, num_types_to_select)

    # Check how many enemy files this would require
    required_enemy_files = set()
    for enemy_id in selected_enemy_types:
        if enemy_id in entities_dict:
            file_id = entities_dict[enemy_id][0]
            if file_id in ENEMY_FILES:
                required_enemy_files.add(file_id)

    # If we have more than 3 enemy files, optimize to use fewer files
    if len(required_enemy_files) > 3:
        selected_enemy_types = optimize_enemy_files(world, current_enemy_pool, max_enemy_types)

    # Assign selected enemy types to randomizable slots
    for instance_id, enemy_id in list(region_data.enemies.items()):
        if enemy_id in all_enemies:
            # Use one of the selected types (random choice from the limited set)
            new_enemy_id = world.random.choice(selected_enemy_types)
            temp_enemy_config[instance_id] = new_enemy_id
        else:
            temp_enemy_config[instance_id] = enemy_id

    return temp_enemy_config


def optimize_enemy_files(world, current_enemy_pool, max_enemy_types: int):
    """Optimize enemy selection to use fewer files."""
    from .file_memory_sizes import ENEMY_FILES, entities_dict

    # Group enemies by their file
    enemies_by_file = {}
    for enemy_id in current_enemy_pool:
        if enemy_id in entities_dict:
            file_id = entities_dict[enemy_id][0]
            if file_id in ENEMY_FILES:
                if file_id not in enemies_by_file:
                    enemies_by_file[file_id] = []
                enemies_by_file[file_id].append(enemy_id)

    # Select up to 3 enemy files and pick enemies from those files
    selected_files = world.random.sample(list(enemies_by_file.keys()), min(3, len(enemies_by_file)))
    selected_enemy_types = []

    for file_id in selected_files:
        available_enemies = enemies_by_file[file_id]
        # Pick 1-2 enemies from each file to reach our target count
        enemies_from_this_file = min(2, len(available_enemies), max_enemy_types - len(selected_enemy_types))
        if enemies_from_this_file > 0:
            selected_enemy_types.extend(world.random.sample(available_enemies, enemies_from_this_file))

    # If we still need more types and have room, add from any file
    if len(selected_enemy_types) < max_enemy_types:
        remaining_enemies = [e for e in current_enemy_pool if e not in selected_enemy_types]
        additional_needed = min(max_enemy_types - len(selected_enemy_types), len(remaining_enemies))
        if additional_needed > 0:
            selected_enemy_types.extend(world.random.sample(remaining_enemies, additional_needed))

    return selected_enemy_types


def calculate_room_memory(world, region_data, enemy_config):
    """Calculate room memory with current enemy setup. Returns (files, total_size, under_budget)."""
    from .file_memory_sizes import MINIMUM_SAFE_BUDGET, entities_dict, file_sizes

    # Use a list to preserve order, but track what's been added to avoid duplicates
    current_files_list = list(region_data.room_default_definitions)
    current_files_set = set(current_files_list)

    # Add files for randomized items in this room
    if hasattr(region_data, "locations"):
        for location_logic in region_data.locations:
            # Find the multiworld location that matches this logic location
            for multiworld_location in world.multiworld.get_locations(world.player):
                if hasattr(multiworld_location, "name") and multiworld_location.name.endswith(f" - {location_logic.name}") and multiworld_location.item:
                    item_name = multiworld_location.item.name
                    item_data = all_item_table.get(item_name)
                    if item_data and hasattr(item_data, "entity_id") and item_data.entity_id is not None:
                        entity_id = item_data.entity_id
                        if entity_id in entities_dict:
                            file_id = entities_dict[entity_id][0]
                            if file_id not in current_files_set:
                                current_files_list.append(file_id)
                                current_files_set.add(file_id)
                    break

    # Add files for enemies
    for enemy_id in enemy_config.values():
        if enemy_id in entities_dict:
            file_id = entities_dict[enemy_id][0]
            if file_id not in current_files_set:
                current_files_list.append(file_id)
                current_files_set.add(file_id)

    # Calculate total size
    total_size = 0
    for file_id in current_files_list:
        if file_id in file_sizes:
            total_size += file_sizes[file_id]

    return current_files_list, total_size, total_size <= MINIMUM_SAFE_BUDGET


def apply_extreme_memory_reduction(world, region_name: str, region_data, room_id: int, all_enemies, RESTRICTED_ENEMIES) -> bool:
    """Apply extreme memory reduction for rooms that fail memory limits. Returns success status."""
    from .file_memory_sizes import ENEMY_FILES, entities_dict, file_sizes

    # Save original for reference
    original_definitions = list(region_data.room_default_definitions)

    # Identify essential non-enemy files under 50KB
    essential_files = []
    for file_id in original_definitions:
        if file_id not in ENEMY_FILES:
            file_size = file_sizes.get(file_id, 0)
            if file_size < 50000:  # Only files under 50KB
                essential_files.append(file_id)

    # Remove duplicates
    essential_files = list(set(essential_files))

    # Find the smallest enemy available
    smallest_enemy = find_smallest_enemy(all_enemies, RESTRICTED_ENEMIES)

    if smallest_enemy:
        # Use the smallest enemy for all slots
        minimal_config = {}
        for instance_id, enemy_id in list(region_data.enemies.items()):
            minimal_config[instance_id] = smallest_enemy

        # Test with minimal files + smallest enemy
        region_data.room_default_definitions = essential_files
        current_files, total_size, under_budget = calculate_room_memory(world, region_data, minimal_config)

        if under_budget:
            for instance_id, enemy_id in minimal_config.items():
                region_data.enemies[instance_id] = enemy_id
                world.randomized_enemy_data[room_id][instance_id] = enemy_id

            region_data.room_default_definitions = current_files
            return True
        else:
            # Even more extreme - use only smallest files
            file_sizes_sorted = [(f, file_sizes.get(f, 0)) for f in essential_files]
            file_sizes_sorted.sort(key=lambda x: x[1])

            # Take only smallest 50% of files
            minimal_files = [f[0] for f in file_sizes_sorted[: max(1, len(file_sizes_sorted) // 2)]]

            region_data.room_default_definitions = minimal_files
            current_files, total_size, under_budget = calculate_room_memory(world, region_data, minimal_config)

            if under_budget:
                for instance_id, enemy_id in minimal_config.items():
                    region_data.enemies[instance_id] = enemy_id
                    world.randomized_enemy_data[room_id][instance_id] = enemy_id

                region_data.room_default_definitions = current_files
                return True

    # If still failing, restore original
    region_data.room_default_definitions = original_definitions
    return False


def find_smallest_enemy(all_enemies, RESTRICTED_ENEMIES):
    """Find the smallest enemy available."""
    from .file_memory_sizes import entities_dict, file_sizes

    smallest_enemy = None
    smallest_size = float("inf")

    for enemy_id in all_enemies:
        if enemy_id not in RESTRICTED_ENEMIES and enemy_id in entities_dict:
            file_id = entities_dict[enemy_id][0]
            size = file_sizes.get(file_id, 0)
            if size < smallest_size:
                smallest_size = size
                smallest_enemy = enemy_id

    return smallest_enemy


def raise_memory_error(region_name: str, room_id: int) -> None:
    """Raise a runtime error for memory budget failures."""
    from .file_memory_sizes import MINIMUM_SAFE_BUDGET

    raise RuntimeError(f"Room {hex(room_id)} in region '{region_name}' exceeds memory budget even with extreme reduction! " f"Budget limit: {MINIMUM_SAFE_BUDGET} bytes. " f"Room ID: {hex(room_id)}")
