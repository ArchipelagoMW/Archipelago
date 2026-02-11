"""Hints for MNSG Archipelago."""

from BaseClasses import ItemClassification
from .Items import get_vanilla_item_names


def CompileMNSGHints(world):
    """Generate and compile hints for MNSG."""
    # Initialize dynamic hints storage
    world.dynamic_hints = {}
    
    # Get hint counts from options
    major_hint_count = world.options.major_hint_count.value
    location_hint_count = world.options.location_hint_count.value
    
    # If no hints requested, return early
    if major_hint_count == 0 and location_hint_count == 0:
        return
    
    # Get vanilla item names to exclude from hints
    vanilla_item_names = get_vanilla_item_names(world.options.randomize_health.value)
    
    # Get all filled locations for this player (includes items from all players)
    all_locations = [
        loc for loc in world.multiworld.get_filled_locations(world.player)
        if loc.item
    ]
    
    # Filter out event locations and vanilla items
    all_locations = [
        loc for loc in all_locations 
        if loc.address is not None and loc.item.name not in vanilla_item_names
    ]
    
    # Separate progression items for major hints
    progression_locations = [
        loc for loc in all_locations
        if loc.item.classification in [ItemClassification.progression, ItemClassification.progression_skip_balancing]
    ]
    
    # Sample major hints from progression items
    major_hint_locations = []
    if major_hint_count > 0 and progression_locations:
        sample_count = min(major_hint_count, len(progression_locations))
        major_hint_locations = world.random.sample(progression_locations, sample_count)
    
    # Define tedious locations to hint
    # TODO: Fill more locations here
    tedious_location_names = [
        "MtFujiSalesmanRoom - Chain Pipe",
        "MtFujiSalesmanRoom - Strength Upgrade 1",
        "GorgeousMusicCastleGarden - Strength Upgrade 2",
        "GorgeousMusicCastleScaffoldingClimbUpper - Silver Key",
        "LakewithaLargetree - Sasuke",
        "PipeMakersHouse - Sudden Impact",
    ]
    
    # Filter for tedious locations that exist
    tedious_locations = [loc for loc in all_locations if loc.name in tedious_location_names]
    
    # Sample location hints from tedious locations
    location_hint_locations = []
    if location_hint_count > 0 and tedious_locations:
        sample_count = min(location_hint_count, len(tedious_locations))
        location_hint_locations = world.random.sample(tedious_locations, sample_count)
    
    # Generate major hints
    for location in major_hint_locations:
        hint_text = format_major_hint(world, location)
        region_name = get_region_name_from_world(world, location)
        world.dynamic_hints[location.address] = {
            "type": "major",
            "text": hint_text,
            "location_id": location.address,
            "item_name": location.item.name,
            "location_name": location.name,
            "region": region_name,
            "player_id": location.item.player
        }
    
    # Generate location hints
    for location in location_hint_locations:
        hint_text = format_location_hint(world, location)
        region_name = get_region_name_from_world(world, location)
        world.dynamic_hints[location.address] = {
            "type": "location",
            "text": hint_text,
            "location_id": location.address,
            "item_name": location.item.name,
            "location_name": location.name,
            "region": region_name,
            "player_id": location.item.player
        }


def get_region_name_from_world(world, location):
    """Extract the region name from the world's all_regions data."""
    # Try to find the region in world.all_regions
    if hasattr(world, "all_regions") and world.all_regions:
        # Extract base location name (AP locations are "RegionName - LocationName")
        location_parts = location.name.split(" - ", 1)
        if len(location_parts) == 2:
            region_part, base_name_part = location_parts
            # Remove any numbering suffix (e.g., "Normal Health 2" -> "Normal Health")
            base_name = base_name_part.rsplit(" ", 1)[0] if base_name_part[-1].isdigit() else base_name_part
            
            # Look through regions to find one that matches the region part
            for region_name, mn64_region in world.all_regions.items():
                if region_name == region_part:
                    # Found the region, return its hint_name
                    if hasattr(mn64_region, "hint_name"):
                        if hasattr(mn64_region.hint_name, "value"):
                            return mn64_region.hint_name.value
                        return str(mn64_region.hint_name)
    
    # Fallback to parent_region name
    if hasattr(location, "parent_region") and location.parent_region:
        if hasattr(location.parent_region, "name"):
            return location.parent_region.name
    
    return "Unknown Region"


def get_region_name(location):
    """Extract the region name from a location."""
    if hasattr(location, "parent_region") and location.parent_region:
        # Try to get hint_name attribute
        if hasattr(location.parent_region, "hint_name"):
            hint_name = location.parent_region.hint_name
            # Handle enum value
            if hasattr(hint_name, "value"):
                return hint_name.value
            # Handle string directly
            return str(hint_name)
        # Fallback to region name
        if hasattr(location.parent_region, "name"):
            return location.parent_region.name
    return "Unknown Region"


def format_major_hint(world, location):
    """Format a major item hint with line breaks for 32 char/line textboxes."""
    item_name = sanitize_text(location.item.name)
    location_name = sanitize_text(location.name)
    # Extract just the location part (after region name and dash)
    location_parts = location.name.split(" - ", 1)
    if len(location_parts) == 2:
        loc_only = sanitize_text(location_parts[1])
    else:
        loc_only = sanitize_text(location.name)    
    # Check if item belongs to another player
    if location.item.player != world.player:
        player_name = sanitize_text(world.multiworld.get_player_name(location.item.player)[:20])
        lines = [f"{player_name} HAS", item_name, f"AT {loc_only}"]
    else:
        lines = [f"{item_name} IS AT", location_name]
    
    return wrap_lines_for_textbox(lines)


def format_location_hint(world, location):
    """Format a location hint with line breaks for 32 char/line textboxes."""
    item_name = sanitize_text(location.item.name)
    location_name = sanitize_text(location.name)
    # Extract just the location part (after region name and dash)    
    # Check if item belongs to another player
    if location.item.player != world.player:
        player_name = sanitize_text(world.multiworld.get_player_name(location.item.player)[:20])
        lines = [f"{location_name} CONTAINS {player_name}'S {item_name}"]
    else:
        lines = [f"{item_name} IS AT", location_name]
    
    return wrap_lines_for_textbox(lines)


def wrap_lines_for_textbox(lines):
    """Wrap lines to fit 32 characters per line with max 4 lines."""
    wrapped_lines = []
    
    for line in lines:
        if len(line) <= 32:
            wrapped_lines.append(line)
        else:
            # Break line into multiple lines at word boundaries
            words = line.split()
            current_line = ""
            for word in words:
                test_line = f"{current_line} {word}".strip()
                if len(test_line) <= 32:
                    current_line = test_line
                else:
                    if current_line:
                        wrapped_lines.append(current_line)
                    current_line = word
            if current_line:
                wrapped_lines.append(current_line)
        
        # Stop if we've reached 4 lines
        if len(wrapped_lines) >= 4:
            break
    
    return "\n".join(wrapped_lines[:4])


def add_spaces_to_camelcase(text):
    """Add spaces between words in PascalCase/camelCase text."""
    import re
    # Add space before uppercase letters that follow lowercase letters or numbers
    spaced = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', text)
    # Add space before uppercase letters that are followed by lowercase letters
    spaced = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', spaced)
    return spaced


def sanitize_text(text):
    """Sanitize text to uppercase with only allowed characters."""
    # First add spaces to camelCase/PascalCase
    text = add_spaces_to_camelcase(text)
    
    # Convert to uppercase
    text = text.upper()
    
    # Keep only alphanumeric, spaces, and basic punctuation
    allowed_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,!?:;'-()%"
    sanitized = "".join(c if c in allowed_chars else " " for c in text)
    
    # Clean up multiple spaces
    sanitized = " ".join(sanitized.split())
    
    return sanitized
