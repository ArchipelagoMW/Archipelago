"""Item definitions for Mystical Ninja Starring Goemon (MN64)."""

from typing import Dict, NamedTuple

from BaseClasses import Item, ItemClassification

from .Logic.mn64_logic_classes import MN64Items


class MN64Item(Item):
    """Item class for MN64."""

    game: str = "Mystical Ninja Starring Goemon"


class ItemData(NamedTuple):
    """Data structure for item information."""

    id: int
    qty: int = 1
    classification: ItemClassification = ItemClassification.progression
    default_location: str = ""
    save_id: int = None
    entity_id: int = None


# Base ID for all MN64 items
BASE_ID = 6464000

# Keys
keys_table: Dict[str, ItemData] = {
    "Silver Key": ItemData(BASE_ID + 0, 18, ItemClassification.progression_skip_balancing, entity_id=0x193),
    "Gold Key": ItemData(BASE_ID + 1, 7, ItemClassification.progression_skip_balancing, entity_id=0x193),
    "Diamond Key": ItemData(BASE_ID + 2, 4, ItemClassification.progression_skip_balancing, entity_id=0x193),
    "Jump Gym Key": ItemData(BASE_ID + 3, 1, ItemClassification.progression_skip_balancing, entity_id=0x193),
}

# Equipment and Tools
equipment_table: Dict[str, ItemData] = {
    "Wind up Camera": ItemData(BASE_ID + 4, 1, ItemClassification.progression, "", 0xC8, entity_id=0x3D3),
    "Chain Pipe": ItemData(BASE_ID + 5, 1, ItemClassification.progression, "", 0xB4, entity_id=0x91),
    "Ice Kunai": ItemData(BASE_ID + 6, 1, ItemClassification.progression, "", 0xCC, entity_id=0x3D4),
    "Medal of Flames": ItemData(BASE_ID + 7, 1, ItemClassification.progression, "", 0xC4, entity_id=0x91),
    "Bazooka": ItemData(BASE_ID + 8, 1, ItemClassification.progression, "", 0xD0, entity_id=0x3D5),
    "Meat Hammer": ItemData(BASE_ID + 9, 1, ItemClassification.progression, "", 0xB8, entity_id=0x3D2),
    "Flute": ItemData(BASE_ID + 10, 1, ItemClassification.progression, "", 0xC0, entity_id=0x91),
}

# Abilities
abilities_table: Dict[str, ItemData] = {
    "Mermaid": ItemData(BASE_ID + 11, 1, ItemClassification.progression, "", 0xF0, entity_id=0x91),
    "Mini Ebisumaru": ItemData(BASE_ID + 12, 1, ItemClassification.progression, "", 0xE8, entity_id=0x91),
    "Sudden Impact": ItemData(BASE_ID + 13, 1, ItemClassification.progression, "", 0xE4, entity_id=0x91),
    "Jetpack": ItemData(BASE_ID + 14, 1, ItemClassification.progression, "", 0xEC, entity_id=0x91),
}

# Characters
characters_table: Dict[str, ItemData] = {
    "Goemon": ItemData(BASE_ID + 15, 1, ItemClassification.progression, "", entity_id=0x91),
    "Yae": ItemData(BASE_ID + 16, 1, ItemClassification.progression, "", 0xA0, entity_id=0x91),
    "Ebisumaru": ItemData(BASE_ID + 17, 1, ItemClassification.progression, entity_id=0x91),
    "Sasuke": ItemData(BASE_ID + 18, 1, ItemClassification.progression, "", 0x9C, entity_id=0x91),
}

# Character Upgrades
character_upgrades_table: Dict[str, ItemData] = {}

# Collectibles
fortune_dolls_table: Dict[str, ItemData] = {
    "Silver Fortune Doll": ItemData(BASE_ID + 22, 40, ItemClassification.useful, entity_id=0x88),
    "Gold Fortune Doll": ItemData(BASE_ID + 23, 5, ItemClassification.useful, entity_id=0x89),
}

health_table: Dict[str, ItemData] = {
    "Golden Health": ItemData(BASE_ID + 24, 28, ItemClassification.filler, entity_id=0x85),
    "Normal Health": ItemData(BASE_ID + 25, 37, ItemClassification.filler, entity_id=0x8F),
}

# Transportation and Access
transportation_table: Dict[str, ItemData] = {
    "Super Pass": ItemData(BASE_ID + 26, 1, ItemClassification.progression, "", 0xF8, entity_id=0x79),
    "Triton Horn": ItemData(BASE_ID + 27, 1, ItemClassification.progression, "", 0xF4, entity_id=0x91),
}

# Quest Items
quest_items_table: Dict[str, ItemData] = {
    "Cucumber": ItemData(BASE_ID + 28, 1, ItemClassification.progression, "", 0x10C, entity_id=0x91),
}

# # Fish
# fish_table: Dict[str, ItemData] = {
#     "Red Fish": ItemData(BASE_ID + 29, 12, ItemClassification.filler),
#     "Yellow Fish": ItemData(BASE_ID + 30, 8, ItemClassification.filler),
#     "Blue Fish": ItemData(BASE_ID + 31, 8, ItemClassification.filler),
# }

# Upgrades
upgrades_table: Dict[str, ItemData] = {
    "Progressive Strength": ItemData(BASE_ID + 32, 2, ItemClassification.progression, entity_id=0x91),
    "Surprise Pack": ItemData(BASE_ID + 34, 8, ItemClassification.filler, entity_id=0x91),
}

# Collectables (NPCs)
collectables_table: Dict[str, ItemData] = {
    "Mr Elly Fant (Oedo Castle)": ItemData(BASE_ID + 35, 1, ItemClassification.useful, "", 0x26C, entity_id=0x86),
    "Mr Elly Fant (Ghost Toys Castle)": ItemData(BASE_ID + 38, 1, ItemClassification.useful, "", 0x26C, entity_id=0x86),
    "Mr Elly Fant (Festival Temple)": ItemData(BASE_ID + 39, 1, ItemClassification.useful, "", 0x26C, entity_id=0x86),
    "Mr Elly Fant (Gourmet Submarine)": ItemData(BASE_ID + 40, 1, ItemClassification.useful, "", 0x26C, entity_id=0x86),
    "Mr Elly Fant (Gorgeous Music Castle)": ItemData(BASE_ID + 45, 1, ItemClassification.useful, "", 0x26C, entity_id=0x86),
    "Mr Arrow (Oedo Castle)": ItemData(BASE_ID + 36, 1, ItemClassification.useful, "", 0x280, entity_id=0x87),
    "Mr Arrow (Ghost Toys Castle)": ItemData(BASE_ID + 41, 1, ItemClassification.useful, "", 0x280, entity_id=0x87),
    "Mr Arrow (Festival Temple)": ItemData(BASE_ID + 42, 1, ItemClassification.useful, "", 0x280, entity_id=0x87),
    "Mr Arrow (Gorgeous Music Castle)": ItemData(BASE_ID + 43, 1, ItemClassification.useful, "", 0x280, entity_id=0x87),
    "Mr Arrow (Gourmet Submarine)": ItemData(BASE_ID + 44, 1, ItemClassification.useful, "", 0x280, entity_id=0x87),
    "Achilles Heel": ItemData(BASE_ID + 37, 1, ItemClassification.progression, "", 0x104, entity_id=0x91),
}

# Event Items (these don't get IDs, they use None)
event_items_table: Dict[str, ItemData] = {
    "Crane Game Power On": ItemData(None, 1, ItemClassification.progression),
    "Visited Witch": ItemData(None, 1, ItemClassification.progression),
    "Visited Ghost Toys Entrance": ItemData(None, 1, ItemClassification.progression),
    "Visited Turtle Stone": ItemData(None, 1, ItemClassification.progression),
    "Beat Tsurami": ItemData(None, 1, ItemClassification.progression),
    "Beat Thaisambda": ItemData(None, 1, ItemClassification.progression),
    "Beat Dharumanyo": ItemData(None, 1, ItemClassification.progression),
    "Beat Congo": ItemData(None, 1, ItemClassification.progression),
    "Beat Game Die Hard Fans": ItemData(None, 1, ItemClassification.progression),
    "Cucumber Quest Find Priest": ItemData(None, 1, ItemClassification.progression),
    "Sasuke Battery 1": ItemData(None, 1, ItemClassification.progression),
    "Sasuke Battery 2": ItemData(None, 1, ItemClassification.progression),
}

# Miracle Items
miracle_items_table: Dict[str, ItemData] = {
    "Miracle Star": ItemData(BASE_ID + 48, 1, ItemClassification.progression, "", 0x250, entity_id=0x35F),
    "Miracle Snow": ItemData(BASE_ID + 49, 1, ItemClassification.progression, "", 0x25C, entity_id=0x91),
    "Miracle Moon": ItemData(BASE_ID + 50, 1, ItemClassification.progression, "", 0x254, entity_id=0x91),
    "Miracle Flower": ItemData(BASE_ID + 51, 1, ItemClassification.progression, "", 0x258, entity_id=0x91),
}

# Training/Special Locations (event items, no IDs)
training_table: Dict[str, ItemData] = {
    "Cucumber Quest Start": ItemData(None, 1, ItemClassification.progression),
    "Kyushu Fly": ItemData(None, 1, ItemClassification.progression),
    "Sasuke Dead": ItemData(None, 1, ItemClassification.progression),
    "Sasuke Battery 2 Event": ItemData(None, 1, ItemClassification.progression),
    "Fish Quest Start": ItemData(None, 1, ItemClassification.progression),
    "Moving Boulder in Forest": ItemData(None, 1, ItemClassification.progression),
}

# Filler Items
filler_table: Dict[str, ItemData] = {
    "Nothing": ItemData(BASE_ID + 55, 0, ItemClassification.filler),
    "Pot of Ryo": ItemData(BASE_ID + 59, 0, ItemClassification.filler, entity_id=0x192),
    "Ryo": ItemData(BASE_ID + 58, 83, ItemClassification.filler, entity_id=0x82),
}

# Trap Items (for future use)
trap_table: Dict[str, ItemData] = {
    "Damage Trap": ItemData(BASE_ID + 56, 0, ItemClassification.trap),
    "Confusion Trap": ItemData(BASE_ID + 57, 0, ItemClassification.trap),
}

# Combine all item tables
all_item_table: Dict[str, ItemData] = {
    **keys_table,
    **equipment_table,
    **abilities_table,
    **characters_table,
    **character_upgrades_table,
    **fortune_dolls_table,
    **health_table,
    **transportation_table,
    **quest_items_table,
    # **fish_table,
    **upgrades_table,
    **collectables_table,
    **event_items_table,
    **miracle_items_table,
    **training_table,
    **filler_table,
    **trap_table,
}

# Group items by category for easier filtering
all_group_table: Dict[str, Dict[str, ItemData]] = {
    "keys": keys_table,
    "equipment": equipment_table,
    "abilities": abilities_table,
    "characters": characters_table,
    "character_upgrades": character_upgrades_table,
    "fortune_dolls": fortune_dolls_table,
    "health": health_table,
    "transportation": transportation_table,
    "quest_items": quest_items_table,
    # "fish": fish_table,
    "upgrades": upgrades_table,
    "collectables": collectables_table,
    "event_items": event_items_table,
    "miracle_items": miracle_items_table,
    "training": training_table,
    "filler": filler_table,
    "trap": trap_table,
}


def get_item_name_to_id() -> Dict[str, int]:
    """Get a dictionary mapping item names to their IDs (excludes event items with None IDs)."""
    return {name: data.id for name, data in all_item_table.items() if data.id is not None}


def get_items_by_classification(
    classification: ItemClassification,
) -> Dict[str, ItemData]:
    """Get all items of a specific classification."""
    return {name: data for name, data in all_item_table.items() if data.classification == classification}


def get_items_by_group(group: str) -> Dict[str, ItemData]:
    """Get all items in a specific group."""
    return all_group_table.get(group, {})


def get_progression_items() -> Dict[str, ItemData]:
    """Get all progression items."""
    return {
        name: data
        for name, data in all_item_table.items()
        if data.classification
        in [
            ItemClassification.progression,
            ItemClassification.progression_skip_balancing,
        ]
    }


def get_filler_items() -> Dict[str, ItemData]:
    """Get all filler items."""
    return {name: data for name, data in all_item_table.items() if data.classification == ItemClassification.filler}


def get_event_item_names():
    """Return set of event item names."""
    return {
        MN64Items.CRANE_GAME_POWER_ON.value,
        MN64Items.VISITED_WITCH.value,
        MN64Items.VISITED_GHOST_TOYS_ENTRANCE.value,
        MN64Items.beat_tsurami.value,
        MN64Items.BEAT_THAISAMBDA.value,
        MN64Items.BEAT_DHARUMANYO.value,
        MN64Items.BEAT_CONGO.value,
        MN64Items.BEAT_GAME_DIE_HARD_FANS.value,
        MN64Items.CUCUMBER_QUEST_PRIEST.value,
        MN64Items.CUCUMBER_QUEST_START.value,
        MN64Items.KUYSHU_FLY.value,
        MN64Items.SASUKE_DEAD.value,
        MN64Items.MOVING_BOULDER_IN_FOREST.value,
        MN64Items.MOKUBEI_BROTHER.value,
        MN64Items.SASUKE_BATTERY_1.value,
        MN64Items.SASUKE_BATTERY_2.value,
        "Sasuke Battery 2 Event",
    }


def get_vanilla_item_names(randomize_health: bool, randomize_ryo: bool, randomize_pots: bool):
    """Return set of vanilla item names (items that stay at their original locations)."""
    vanilla_item_names = {
        MN64Items.MIRACLE_STAR.value,
        MN64Items.MIRACLE_SNOW.value,
        MN64Items.MIRACLE_MOON.value,
        MN64Items.MIRACLE_FLOWER.value,
    }

    # If health randomization is disabled, keep health items at vanilla locations
    if not randomize_health:
        vanilla_item_names.add(MN64Items.GOLDEN_HEALTH.value)
        vanilla_item_names.add(MN64Items.NORMAL_HEALTH.value)

    # If ryo randomization is disabled, keep ryo items at vanilla locations
    if not randomize_ryo:
        vanilla_item_names.add(MN64Items.RYO.value)

    # If pot randomization is disabled, keep pot items at vanilla locations
    if not randomize_pots:
        vanilla_item_names.add(MN64Items.POT.value)

    return vanilla_item_names


def populate_item_metadata(world) -> None:
    """Populate item_metadata with all items from the item table."""
    for item_name, item_data in all_item_table.items():
        # Skip event items that don't have AP IDs
        if item_data.id is None:
            continue

        # Use AP ID as the key
        ap_id = item_data.id
        world.item_metadata[ap_id] = {}

        # Add item name as description
        world.item_metadata[ap_id]["name"] = item_name

        # Add save ID if it exists
        if item_data.save_id is not None:
            world.item_metadata[ap_id]["save_id"] = item_data.save_id

        # Add entity ID if it exists
        if item_data.entity_id is not None:
            world.item_metadata[ap_id]["entity_id"] = item_data.entity_id

        # Add classification
        world.item_metadata[ap_id]["classification"] = item_data.classification.name

        # Add quantity
        world.item_metadata[ap_id]["qty"] = item_data.qty
