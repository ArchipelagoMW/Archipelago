from typing import Dict, List, Set

from BaseClasses import ItemClassification

from . import static_logic as static_witness_logic
from .item_definition_classes import DoorItemDefinition, ItemCategory, ItemData
from .static_locations import ID_START

ITEM_DATA: Dict[str, ItemData] = {}
ITEM_GROUPS: Dict[str, Set[str]] = {}

# Useful items that are treated specially at generation time and should not be automatically added to the player's
# item list during get_progression_items.
_special_usefuls: List[str] = ["Puzzle Skip"]

ALWAYS_GOOD_SYMBOL_ITEMS: Set[str] = {"Dots", "Black/White Squares", "Symmetry", "Shapers", "Stars"}

MODE_SPECIFIC_GOOD_ITEMS: Dict[str, Set[str]] = {
    "none": set(),
    "sigma_normal": set(),
    "sigma_expert": {"Triangles"},
    "umbra_variety": {"Triangles"}
}

MODE_SPECIFIC_GOOD_DISCARD_ITEMS: Dict[str, Set[str]] = {
    "none": {"Triangles"},
    "sigma_normal": {"Triangles"},
    "sigma_expert": {"Arrows"},
    "umbra_variety": set()  # Variety Discards use both Arrows and Triangles, so neither of them are that useful alone
}

OBELISK_KEYS = [
    "Desert Obelisk Key",
    "Monastery Obelisk Key",
    "Treehouse Obelisk Key",
    "Mountainside Obelisk Key",
    "Quarry Obelisk Key",
    "Town Obelisk Key",
]

SYMBOL_ITEMS = [
    "Arrows",
    "Progressive Dots",
    "Sound Dots",
    "Progressive Symmetry",
    "Triangles",
    "Eraser",
    "Shapers",
    "Rotated Shapers",
    "Negative Shapers",
    "Progressive Stars",
    "Black/White Squares",
    "Colored Squares",
]

LASER_ITEMS = [
    "Symmetry Laser",
    "Desert Laser",
    "Keep Laser",
    "Shadows Laser",
    "Quarry Laser",
    "Town Laser",
    "Swamp Laser",
    "Jungle Laser",
    "Bunker Laser",
    "Monastery Laser",
    "Treehouse Laser",
]

BOAT = [
    "Boat"
]

INDIVIDUAL_DOOR_PANELS = [
    "Glass Factory Entry (Panel)",
    "Outside Tutorial Outpost Entry (Panel)",
    "Outside Tutorial Outpost Exit (Panel)",
    "Symmetry Island Lower (Panel)",
    "Symmetry Island Upper (Panel)",
    "Desert Light Room Entry (Panel)",
    "Desert Flood Room Entry (Panel)",
    "Quarry Entry 1 (Panel)",
    "Quarry Entry 2 (Panel)",
    "Quarry Stoneworks Entry (Panel)",
    "Shadows Door Timer (Panel)",
    "Keep Hedge Maze 1 (Panel)",
    "Keep Hedge Maze 2 (Panel)",
    "Keep Hedge Maze 3 (Panel)",
    "Keep Hedge Maze 4 (Panel)",
    "Monastery Entry Left (Panel)",
    "Monastery Entry Right (Panel)",
    "Town RGB House Entry (Panel)",
    "Town Church Entry (Panel)",
    "Town Maze Stairs (Panel)",
    "Windmill Entry (Panel)",
    "Town Cargo Box Entry (Panel)",
    "Theater Entry (Panel)",
    "Theater Exit (Panel)",
    "Treehouse First & Second Doors (Panel)",
    "Treehouse Third Door (Panel)",
    "Treehouse Laser House Door Timer (Panel)",
    "Treehouse Drawbridge (Panel)",
    "Jungle Popup Wall (Panel)",
    "Bunker Entry (Panel)",
    "Bunker Tinted Glass Door (Panel)",
    "Swamp Entry (Panel)",
    "Swamp Platform Shortcut (Panel)",
    "Caves Entry (Panel)",
    "Challenge Entry (Panel)",
    "Tunnels Entry (Panel)",
    "Tunnels Town Shortcut (Panel)",
]

INDIVIDUAL_DOORS = [
    "Outside Tutorial Outpost Path (Door)",
    "Outside Tutorial Outpost Entry (Door)",
    "Outside Tutorial Outpost Exit (Door)",
    "Glass Factory Entry (Door)",
    "Glass Factory Back Wall (Door)",
    "Symmetry Island Lower (Door)",
    "Symmetry Island Upper (Door)",
    "Orchard First Gate (Door)",
    "Orchard Second Gate (Door)",
    "Desert Light Room Entry (Door)",
    "Desert Pond Room Entry (Door)",
    "Desert Flood Room Entry (Door)",
    "Desert Elevator Room Entry (Door)",
    "Desert Elevator (Door)",
    "Quarry Entry 1 (Door)",
    "Quarry Entry 2 (Door)",
    "Quarry Stoneworks Entry (Door)",
    "Quarry Stoneworks Side Exit (Door)",
    "Quarry Stoneworks Roof Exit (Door)",
    "Quarry Stoneworks Stairs (Door)",
    "Quarry Boathouse Dock (Door)",
    "Quarry Boathouse First Barrier (Door)",
    "Quarry Boathouse Second Barrier (Door)",
    "Shadows Timed Door",
    "Shadows Laser Entry Right (Door)",
    "Shadows Laser Entry Left (Door)",
    "Shadows Quarry Barrier (Door)",
    "Shadows Ledge Barrier (Door)",
    "Keep Hedge Maze 1 Exit (Door)",
    "Keep Pressure Plates 1 Exit (Door)",
    "Keep Hedge Maze 2 Shortcut (Door)",
    "Keep Hedge Maze 2 Exit (Door)",
    "Keep Hedge Maze 3 Shortcut (Door)",
    "Keep Hedge Maze 3 Exit (Door)",
    "Keep Hedge Maze 4 Shortcut (Door)",
    "Keep Hedge Maze 4 Exit (Door)",
    "Keep Pressure Plates 2 Exit (Door)",
    "Keep Pressure Plates 3 Exit (Door)",
    "Keep Pressure Plates 4 Exit (Door)",
    "Keep Shadows Shortcut (Door)",
    "Keep Tower Shortcut (Door)",
    "Monastery Laser Shortcut (Door)",
    "Monastery Entry Inner (Door)",
    "Monastery Entry Outer (Door)",
    "Monastery Garden Entry (Door)",
    "Town Cargo Box Entry (Door)",
    "Town Wooden Roof Stairs (Door)",
    "Town RGB House Entry (Door)",
    "Town Church Entry (Door)",
    "Town Maze Stairs (Door)",
    "Windmill Entry (Door)",
    "Town RGB House Stairs (Door)",
    "Town Tower Second (Door)",
    "Town Tower First (Door)",
    "Town Tower Fourth (Door)",
    "Town Tower Third (Door)",
    "Theater Entry (Door)",
    "Theater Exit Left (Door)",
    "Theater Exit Right (Door)",
    "Jungle Laser Shortcut (Door)",
    "Jungle Popup Wall (Door)",
    "Jungle Monastery Garden Shortcut (Door)",
    "Bunker Entry (Door)",
    "Bunker Tinted Glass Door",
    "Bunker UV Room Entry (Door)",
    "Bunker Elevator Room Entry (Door)",
    "Swamp Entry (Door)",
    "Swamp Between Bridges First Door",
    "Swamp Platform Shortcut (Door)",
    "Swamp Cyan Water Pump (Door)",
    "Swamp Between Bridges Second Door",
    "Swamp Red Water Pump (Door)",
    "Swamp Red Underwater Exit (Door)",
    "Swamp Blue Water Pump (Door)",
    "Swamp Purple Water Pump (Door)",
    "Swamp Laser Shortcut (Door)",
    "Treehouse First (Door)",
    "Treehouse Second (Door)",
    "Treehouse Third (Door)",
    "Treehouse Drawbridge (Door)",
    "Treehouse Laser House Entry (Door)",
    "Mountain Floor 1 Exit (Door)",
    "Mountain Floor 2 Staircase Near (Door)",
    "Mountain Floor 2 Exit (Door)",
    "Mountain Floor 2 Staircase Far (Door)",
    "Mountain Bottom Floor Giant Puzzle Exit (Door)",
    "Mountain Bottom Floor Pillars Room Entry (Door)",
    "Mountain Bottom Floor Rock (Door)",
    "Caves Entry (Door)",
    "Caves Pillar Door",
    "Caves Mountain Shortcut (Door)",
    "Caves Swamp Shortcut (Door)",
    "Challenge Entry (Door)",
    "Tunnels Entry (Door)",
    "Tunnels Theater Shortcut (Door)",
    "Tunnels Desert Shortcut (Door)",
    "Tunnels Town Shortcut (Door)",
]

INDIVIDUAL_CONTROL_PANELS = [
    "Desert Surface 3 Control (Panel)",
    "Desert Surface 8 Control (Panel)",
    "Desert Elevator Room Hexagonal Control (Panel)",
    "Desert Flood Controls (Panel)",
    "Desert Light Control (Panel)",
    "Quarry Elevator Control (Panel)",
    "Quarry Stoneworks Ramp Controls (Panel)",
    "Quarry Stoneworks Lift Controls (Panel)",
    "Quarry Boathouse Ramp Height Control (Panel)",
    "Quarry Boathouse Ramp Horizontal Control (Panel)",
    "Quarry Boathouse Hook Control (Panel)",
    "Monastery Shutters Control (Panel)",
    "Town Maze Rooftop Bridge (Panel)",
    "Town RGB Control (Panel)",
    "Town Desert Laser Redirect Control (Panel)",
    "Windmill Turn Control (Panel)",
    "Theater Video Input (Panel)",
    "Bunker Drop-Down Door Controls (Panel)",
    "Bunker Elevator Control (Panel)",
    "Swamp Sliding Bridge (Panel)",
    "Swamp Rotating Bridge (Panel)",
    "Swamp Long Bridge (Panel)",
    "Swamp Maze Controls (Panel)",
    "Mountain Floor 1 Light Bridge (Panel)",
    "Mountain Floor 2 Light Bridge Near (Panel)",
    "Mountain Floor 2 Light Bridge Far (Panel)",
    "Mountain Floor 2 Elevator Control (Panel)",
    "Caves Elevator Controls (Panel)",
]

REGIONAL_PANELS = [
    "Symmetry Island Panels",
    "Outside Tutorial Outpost Panels",
    "Desert Panels",
    "Quarry Outside Panels",
    "Quarry Stoneworks Panels",
    "Quarry Boathouse Panels",
    "Keep Hedge Maze Panels",
    "Monastery Panels",
    "Town Church & RGB House Panels",
    "Town Maze Panels",
    "Windmill & Theater Panels",
    "Town Dockside House Panels",
    "Treehouse Panels",
    "Bunker Panels",
    "Swamp Panels",
    "Mountain Panels",
    "Caves Panels",
    "Tunnels Panels",
    "Glass Factory Entry (Panel)",
    "Shadows Door Timer (Panel)",
    "Jungle Popup Wall (Panel)",
]

REGIONAL_DOORS = [
    "Outside Tutorial Outpost Doors",
    "Glass Factory Doors",
    "Symmetry Island Doors",
    "Orchard Gates",
    "Desert Doors & Elevator",
    "Quarry Entry Doors",
    "Quarry Stoneworks Doors",
    "Quarry Boathouse Doors",
    "Shadows Laser Room Doors",
    "Shadows Lower Doors",
    "Keep Hedge Maze Doors",
    "Keep Pressure Plates Doors",
    "Keep Shortcuts",
    "Monastery Entry Doors",
    "Monastery Shortcuts",
    "Town Doors",
    "Town Tower Doors",
    "Windmill & Theater Doors",
    "Jungle Doors",
    "Bunker Doors",
    "Swamp Doors",
    "Swamp Shortcuts",
    "Swamp Water Pumps",
    "Treehouse Entry Doors",
    "Treehouse Upper Doors",
    "Mountain Floor 1 & 2 Doors",
    "Mountain Bottom Floor Doors",
    "Caves Doors",
    "Caves Shortcuts",
    "Tunnels Doors",
]

REGIONAL_CONTROL_PANELS = [
    "Desert Control Panels",
    "Quarry Elevator Control (Panel)",
    "Quarry Stoneworks Control Panels",
    "Quarry Boathouse Control Panels",
    "Monastery Shutters Control (Panel)",
    "Town Control Panels",
    "Windmill & Theater Control Panels",
    "Bunker Control Panels",
    "Swamp Control Panels",
    "Mountain & Caves Control Panels",
]


def populate_items() -> None:
    for item_name, definition in static_witness_logic.ALL_ITEMS.items():
        ap_item_code = definition.local_code + ID_START
        classification: ItemClassification = ItemClassification.filler
        local_only: bool = False

        if definition.category is ItemCategory.SYMBOL:
            classification = ItemClassification.progression
            ITEM_GROUPS.setdefault("Symbols", set()).add(item_name)
        elif definition.category is ItemCategory.DOOR:
            classification = ItemClassification.progression
            ITEM_GROUPS.setdefault("Doors", set()).add(item_name)
        elif definition.category is ItemCategory.LASER:
            classification = ItemClassification.progression_skip_balancing
            ITEM_GROUPS.setdefault("Lasers", set()).add(item_name)
        elif definition.category is ItemCategory.USEFUL:
            classification = ItemClassification.useful
        elif definition.category is ItemCategory.FILLER:
            if item_name in ["Energy Fill (Small)"]:
                local_only = True
            classification = ItemClassification.filler
        elif definition.category is ItemCategory.TRAP:
            classification = ItemClassification.trap
        elif definition.category is ItemCategory.JOKE:
            classification = ItemClassification.filler

        ITEM_DATA[item_name] = ItemData(ap_item_code, definition,
                                        classification, local_only)


def get_item_to_door_mappings() -> Dict[int, List[int]]:
    output: Dict[int, List[int]] = {}
    for item_name, item_data in ITEM_DATA.items():
        if not isinstance(item_data.definition, DoorItemDefinition) or item_data.ap_code is None:
            continue
        output[item_data.ap_code] = [int(hex_string, 16) for hex_string in item_data.definition.panel_id_hexes]
    return output


populate_items()
