from enum import IntEnum
from typing import NamedTuple, List, Optional
import random
from BaseClasses import Item, ItemClassification # ItemClassification is used for internal logic, but not directly in MedievilItemData itself.


class MedievilItemCategory(IntEnum):
    FILLER = 0
    PROGRESSION = 1
    FUN = 2
    LEVEL_END = 4
    SKIP = 5


class MedievilItemData(NamedTuple):
    name: str
    m_code: Optional[int] # Changed to Optional[int] for flexibility with None
    category: MedievilItemCategory
    progression: bool # Added 'progression' field to the raw data


class MedievilItem(Item):
    game: str = "Medievil"
    category: MedievilItemCategory
    m_code: Optional[int] # Make m_code an instance attribute for MedievilItem

    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int):
        super().__init__(name, classification, code, player)
        # The 'advancement' attribute is automatically handled by the parent Item class
        # if ItemClassification.progression is passed to its constructor.
        # You can explicitly set it here for clarity if you prefer, but BaseClasses.Item does this.
        # self.advancement = classification == ItemClassification.progression

        # Store game-specific data directly on the item instance
        item_data = item_dictionary.get(name)
        if item_data:
            self.m_code = item_data.m_code
            self.category = item_data.category
        else:
            self.m_code = None
            self.category = MedievilItemCategory.FILLER # Fallback for unknown items


    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 9901000 
        # Create a dictionary mapping item names to their unique Archipelago IDs.
        return {item_data.name: (base_id + item_data.m_code) 
                for item_data in _all_items if item_data.m_code is not None}


key_item_names = {
    # Add names of items here that should always be considered progression,
    # even if their category isn't MedievilItemCategory.PROGRESSION.
    # E.g., "Chalice", "Dragon Gem"
}


_all_items: List[MedievilItemData] = [
    # (name, m_code, category, is_progression)
    ("Gold (50)", 0, MedievilItemCategory.FILLER, False), # m_codes should be unique and ideally sequential for offsets
    ("Gold (100)", 1, MedievilItemCategory.FILLER, False),
    ("Gold (150)", 2, MedievilItemCategory.FILLER, False),
    ("Daggers (10)", 3, MedievilItemCategory.FILLER, False),
    ("Daggers (20)", 4, MedievilItemCategory.FILLER, False),
    ("Broadsword Energy (20)", 5, MedievilItemCategory.FILLER, False),
    ("Broadsword Energy (50)", 6, MedievilItemCategory.FILLER, False),
    ("Club Energy (20)", 7, MedievilItemCategory.FILLER, False),
    ("Club Energy (50)", 8, MedievilItemCategory.FILLER, False),
    ("Chicken Drumsticks (10)", 9, MedievilItemCategory.FILLER, False),
    ("Crossbow Ammo (20)", 10, MedievilItemCategory.FILLER, False),
    ("Crossbow Ammo (50)", 11, MedievilItemCategory.FILLER, False),
    ("Longbow Ammo (20)", 12, MedievilItemCategory.FILLER, False),
    ("Longbow Ammo (50)", 13, MedievilItemCategory.FILLER, False),
    ("Fire Longbow Ammo (20)", 14, MedievilItemCategory.FILLER, False),
    ("Fire Longbow Ammo (50)", 15, MedievilItemCategory.FILLER, False),
    ("Magic Longbow Ammo (20)", 16, MedievilItemCategory.FILLER, False),
    ("Magic Longbow Ammo (50)", 17, MedievilItemCategory.FILLER, False),
    ("Spear Ammo (20)", 18, MedievilItemCategory.FILLER, False),
    ("Spear Ammo (50)", 19, MedievilItemCategory.FILLER, False),
    ("Lightning Charge (30)", 20, MedievilItemCategory.FILLER, False),
    ("Lightning Charge (50)", 21, MedievilItemCategory.FILLER, False),
    ("Copper Shield Charge (50)", 22, MedievilItemCategory.FILLER, False),
    ("Copper Shield Charge (100)", 23, MedievilItemCategory.FILLER, False),
    ("Silver Shield Charge (50)", 24, MedievilItemCategory.FILLER, False),
    ("Silver Shield Charge (100)", 25, MedievilItemCategory.FILLER, False),
    ("Gold Shield Charge (50)", 26, MedievilItemCategory.FILLER, False),
    ("Gold Shield Charge (100)", 27, MedievilItemCategory.FILLER, False),
    
    # Level_End is typically a progression item as it signifies advancing a stage
    ("Level_End", 28, MedievilItemCategory.LEVEL_END, True) 
]
# Convert raw list of tuples into MedievilItemData NamedTuple instances
_all_items = [MedievilItemData(row[0], row[1], row[2], row[3]) for row in _all_items]


item_descriptions = {
    # Optional: Add detailed descriptions for items here
    # "Gold (50)": "A small pouch of gold coins."
}

# Create a dictionary for quick lookup of item data by name
item_dictionary: dict[str, MedievilItemData] = {item_data.name: item_data for item_data in _all_items}


def BuildItemPool(count: int, options) -> List[str]:
    """
    Generates a list of item names to be used for the item pool.
    This function does NOT create Archipelago Item objects; it only provides their names.
    The actual Item objects are created in MedievilWorld.create_items.

    Args:
        count (int): The total number of item names to generate.
        options: The options object from the Archipelago multiworld, used for guaranteed items.

    Returns:
        List[str]: A shuffled list of item names.
    """
    item_pool_names: List[str] = []
    
    # Add any guaranteed items specified in the options first
    if hasattr(options, "guaranteed_items") and options.guaranteed_items.value:
        for item_name in options.guaranteed_items.value:
            if item_name in item_dictionary:
                item_pool_names.append(item_name)
            else:
                print(f"Warning: Guaranteed item '{item_name}' not found in item_dictionary. Skipping.")
    
    # Populate the rest of the pool with random filler items
    # Prioritize items marked as FILLER.
    filler_item_names = [item_data.name for item_data in _all_items 
                         if item_data.category == MedievilItemCategory.FILLER]

    for _ in range(count - len(item_pool_names)):
        if filler_item_names:
            item_name_to_add = random.choice(filler_item_names)
            item_pool_names.append(item_name_to_add)
        else:
            print("Warning: Ran out of filler items for Medievil. Duplicating from all available items.")
            # Fallback: if no specific filler items left, pick from any available item
            item_pool_names.append(random.choice(list(item_dictionary.keys())))

    random.shuffle(item_pool_names) # Shuffle the final list of item names
    return item_pool_names