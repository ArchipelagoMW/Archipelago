from enum import IntEnum
from typing import NamedTuple, List, Optional
import random
from BaseClasses import Item, ItemClassification # ItemClassification is used for internal logic, but not directly in MedievilItemData itself.


class MedievilItemCategory(IntEnum):
    FILLER = 0
    PROGRESSION = 1
    WEAPON = 2
    CHALICE = 3
    FUN = 4
    LEVEL_END = 5
    SKIP = 6


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
    # life bottles
    
    "Life Bottle: Dan's Crypt",
    "Life Bottle: The Graveyard",
    "Life Bottle: Hall of Heroes (Canny Tim)",
    "Life Bottle: Dan's Crypt - Behind Wall",
    "Life Bottle: Scarecrow Fields",
    "Life Bottle: Pools of the Ancient Dead",
    "Life Bottle: Hall of Heroes (Ravenhooves The Archer )",
    "Life Bottle: Hall of Heroes (Dirk Steadfast)",
    "Life Bottle: The Time Device",
    
    # skills 
    "Skill: Daring Dash"
    
    # Inventory Key Items
    
    "Key Item: Dragon Gem - Pumpkin Serpent",
    "Key Item: Dragon Gem - Inside the Asylum",
    "Key Item: King Peregrine's Crown",
    "Key Item: Soul Helmet 1",
    "Key Item: Soul Helmet 2",
    "Key Item: Soul Helmet 3",
    "Key Item: Soul Helmet 4",
    "Key Item: Soul Helmet 5",
    "Key Item: Soul Helmet 6",
    "Key Item: Soul Helmet 7",
    "Key Item: Soul Helmet 8",
    "Key Item: Witches Talisman", 
    "Key Item: Safe Key", 
    "Key Item: Shadow Artefact", 
    "Key Item: Shadow Talisman",     
    "Key Item: Crucifix", 
    "Key Item: Landlords Bust", 
    "Key Item: Crucifix Cast", 
    "Key Item: Amber Piece 1", 
    "Key Item: Amber Piece 2", 
    "Key Item: Amber Piece 3", 
    "Key Item: Amber Piece 4", 
    "Key Item: Amber Piece 5", 
    "Key Item: Amber Piece 6", 
    "Key Item: Amber Piece 7", 
    "Key Item: Harvester Parts", 
    "Key Item: Skull Key", 
    "Key Item: Sheet Music", 
    
    # Required Equipment
    
    "Equipment: Club",
    
    # Runes 
    
    "Chaos Rune: The Graveyard", 
    "Chaos Rune: The Hilltop Mausoleum", 
    "Chaos Rune: Scarecrow Fields", 
    "Chaos Rune: The Lake", 
    "Chaos Rune: Pumpkin Gorge", 
    "Chaos Rune: Sleeping Village", 
    "Chaos Rune: Pools of the Ancient Dead",
    "Chaos Rune: Asylum Grounds", 
    "Chaos Rune: The Haunted Ruins", 
    "Chaos Rune: Ghost Ship", 
    "Chaos Rune: The Time Device", 
    "Earth Rune: The Graveyard", 
    "Earth Rune: The Hilltop Mausoleum", 
    "Earth Rune: Scarecrow Fields", 
    "Earth Rune: The Crystal Caves", 
    "Earth Rune: The Lake", 
    "Earth Rune: Pumpkin Gorge", 
    "Earth Rune: Sleeping Village", 
    "Earth Rune: Inside the Asylum",
    "Earth Rune: Enchanted Earth", 
    "Earth Rune: The Haunted Ruins", 
    "Earth Rune: The Entrance Hall", 
    "Earth Rune: The Time Device", 
    "Moon Rune: The Hilltop Mausoleum", 
    "Moon Rune: Scarecrow Fields", 
    "Moon Rune: Pumpkin Gorge", 
    "Moon Rune: Ghost Ship", 
    "Moon Rune: The Time Device", 
    "Star Rune: Return to the Graveyard", 
    "Star Rune: Dan's Crypt", 
    "Star Rune: The Crystal Caves", 
    "Star Rune: The Lake", 
    "Star Rune: Enchanted Earth", 
    "Star Rune: The Gallows Gauntlet",
    "Star Rune: Ghost Ship", 
    "Time Rune: The Lake", 
    "Time Rune: Pumpkin Gorge", 
    "Time Rune: The Time Device",
}


_all_items: List[MedievilItemData] = [
    # Filler Items
    ("Gold Coins (50)", 0, MedievilItemCategory.FILLER, False),
    ("Gold Coins (100)", 1, MedievilItemCategory.FILLER, False),
    ("Gold Coins (150)", 2, MedievilItemCategory.FILLER, False),
    ("Dagger Ammo (10)", 3, MedievilItemCategory.FILLER, False),
    ("Dagger Ammo (20)", 4, MedievilItemCategory.FILLER, False),
    ("Broadsword Charge (20)", 5, MedievilItemCategory.FILLER, False),
    ("Broadsword Charge (50)", 6, MedievilItemCategory.FILLER, False),
    ("Club Charge (20)", 7, MedievilItemCategory.FILLER, False),
    ("Club Charge (50)", 8, MedievilItemCategory.FILLER, False),
    ("Chicken Drumsticks Ammo (10)", 9, MedievilItemCategory.FILLER, False),
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
    ("Copper Shield Ammo (50)", 22, MedievilItemCategory.FILLER, False),
    ("Copper Shield Ammo (100)", 23, MedievilItemCategory.FILLER, False),
    ("Silver Shield Ammo (50)", 24, MedievilItemCategory.FILLER, False),
    ("Silver Shield Ammo (100)", 25, MedievilItemCategory.FILLER, False),
    ("Gold Shield Ammo (50)", 26, MedievilItemCategory.FILLER, False),
    ("Gold Shield Ammo (100)", 27, MedievilItemCategory.FILLER, False),
    ("Health Vial (50)", 28, MedievilItemCategory.FILLER, False),
    ("Health Vial (150)", 29, MedievilItemCategory.FILLER, False),
    ("Health Vial (300)", 30, MedievilItemCategory.FILLER, False),
    
    # list of weapons
    ("Equipment: Small Sword", 31, MedievilItemCategory.WEAPON, False),
    ("Equipment: Broadsword", 32, MedievilItemCategory.WEAPON, False),
    ("Equipment: Magic Sword", 33, MedievilItemCategory.WEAPON, False),
    ("Equipment: Club", 34, MedievilItemCategory.PROGRESSION, True),
    ("Equipment: Hammer", 35, MedievilItemCategory.WEAPON, False),
    ("Equipment: Daggers", 36, MedievilItemCategory.WEAPON, False),    
    ("Equipment: Axe", 37, MedievilItemCategory.WEAPON, False),
    ("Equipment: Chicken Drumsticks", 38, MedievilItemCategory.WEAPON, False),
    ("Equipment: Crossbow", 39, MedievilItemCategory.WEAPON, False),
    ("Equipment: Longbow", 40, MedievilItemCategory.WEAPON, False),
    ("Equipment: Fire Longbow", 41, MedievilItemCategory.WEAPON, False),
    ("Equipment: Magic Longbow", 42, MedievilItemCategory.WEAPON, False),
    ("Equipment: Spear", 43, MedievilItemCategory.WEAPON, False),
    ("Equipment: Lightning", 44, MedievilItemCategory.WEAPON, False),
    ("Equipment: Good Lightning", 45, MedievilItemCategory.WEAPON, False),
    ("Equipment: Copper Shield", 46, MedievilItemCategory.WEAPON, False),
    ("Equipment: Silver Shield", 47, MedievilItemCategory.WEAPON, False),
    ("Equipment: Gold Shield", 48, MedievilItemCategory.WEAPON, False),
    ("Equipment: Dragon Armour", 49, MedievilItemCategory.WEAPON, False),

    # Progression items    
    ("Life Bottle: Dan's Crypt", 50, MedievilItemCategory.PROGRESSION, True),
    ("Life Bottle: The Graveyard", 51, MedievilItemCategory.PROGRESSION, True),
    ("Life Bottle: Hall of Heroes (Canny Tim)", 52, MedievilItemCategory.PROGRESSION, True),
    ("Life Bottle: Dan's Crypt - Behind Wall", 53, MedievilItemCategory.PROGRESSION, True),
    ("Life Bottle: Scarecrow Fields", 54, MedievilItemCategory.PROGRESSION, True),
    ("Life Bottle: Pools of the Ancient Dead", 55, MedievilItemCategory.PROGRESSION, True),    
    ("Life Bottle: Hall of Heroes (Ravenhooves The Archer)", 56, MedievilItemCategory.PROGRESSION, True),    
    ("Life Bottle: Hall of Heroes (Dirk Steadfast)", 57, MedievilItemCategory.PROGRESSION, True),
    ("Life Bottle: The Time Device", 58, MedievilItemCategory.PROGRESSION, True),
    
    ("Skill: Daring Dash",60,MedievilItemCategory.PROGRESSION, True),    
    
    # Chalice
    ("Chalice of Souls", 88, MedievilItemCategory.CHALICE, False),
    
    # Key Inventory Items
    ("Key Item: Dragon Gem - Pumpkin Serpent", 89, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Dragon Gem - Inside the Asylum", 90, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: King Peregrine's Crown", 91, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Soul Helmet 1", 92, MedievilItemCategory.PROGRESSION, True), # progressive soul helmet?
    ("Key Item: Soul Helmet 2", 93, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Soul Helmet 3", 94, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Soul Helmet 4", 95, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Soul Helmet 5", 96, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Soul Helmet 6", 97, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Soul Helmet 7", 98, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Soul Helmet 8", 99, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Witches Talisman", 100, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Safe Key", 101, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Shadow Artefact", 102, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Shadow Talisman", 103, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Crucifix", 104, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Landlords Bust", 105, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Crucifix Cast", 106, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Amber Piece 1", 107, MedievilItemCategory.PROGRESSION, True), # progressive amber piece later?
    ("Key Item: Amber Piece 2", 108, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Amber Piece 3", 109, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Amber Piece 4", 110, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Amber Piece 5", 111, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Amber Piece 6", 112, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Amber Piece 7", 113, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Harvester Parts", 114, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Skull Key", 115, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Sheet Music", 116, MedievilItemCategory.PROGRESSION, True),

    # Runes
    ("Chaos Rune: The Graveyard", 117, MedievilItemCategory.PROGRESSION, True),
    ("Chaos Rune: The Hilltop Mausoleum", 118, MedievilItemCategory.PROGRESSION, True),
    ("Chaos Rune: Scarecrow Fields", 119, MedievilItemCategory.PROGRESSION, True),
    ("Chaos Rune: The Lake", 120, MedievilItemCategory.PROGRESSION, True),
    ("Chaos Rune: Pumpkin Gorge", 121, MedievilItemCategory.PROGRESSION, True),
    ("Chaos Rune: Sleeping Village", 122, MedievilItemCategory.PROGRESSION, True),
    ("Chaos Rune: Pools of the Ancient Dead", 123, MedievilItemCategory.PROGRESSION, True),
    ("Chaos Rune: Asylum Grounds", 124, MedievilItemCategory.PROGRESSION, True),
    ("Chaos Rune: The Haunted Ruins", 125, MedievilItemCategory.PROGRESSION, True),
    ("Chaos Rune: Ghost Ship", 126, MedievilItemCategory.PROGRESSION, True),
    ("Chaos Rune: The Time Device", 127, MedievilItemCategory.PROGRESSION, True),

    ("Earth Rune: The Graveyard", 128, MedievilItemCategory.PROGRESSION, True),
    ("Earth Rune: The Hilltop Mausoleum", 129, MedievilItemCategory.PROGRESSION, True),
    ("Earth Rune: Scarecrow Fields", 130, MedievilItemCategory.PROGRESSION, True),
    ("Earth Rune: The Crystal Caves", 131, MedievilItemCategory.PROGRESSION, True),
    ("Earth Rune: The Lake", 132, MedievilItemCategory.PROGRESSION, True),
    ("Earth Rune: Pumpkin Gorge", 133, MedievilItemCategory.PROGRESSION, True),
    ("Earth Rune: Sleeping Village", 134, MedievilItemCategory.PROGRESSION, True),
    ("Earth Rune: Inside the Asylum", 135, MedievilItemCategory.PROGRESSION, True),
    ("Earth Rune: Enchanted Earth", 136, MedievilItemCategory.PROGRESSION, True),
    ("Earth Rune: The Haunted Ruins", 137, MedievilItemCategory.PROGRESSION, True),
    ("Earth Rune: The Entrance Hall", 138, MedievilItemCategory.PROGRESSION, True),
    ("Earth Rune: The Time Device", 139, MedievilItemCategory.PROGRESSION, True),

    ("Moon Rune: The Hilltop Mausoleum", 140, MedievilItemCategory.PROGRESSION, True),
    ("Moon Rune: Scarecrow Fields", 141, MedievilItemCategory.PROGRESSION, True),
    ("Moon Rune: Pumpkin Gorge", 142, MedievilItemCategory.PROGRESSION, True),
    ("Moon Rune: Ghost Ship", 143, MedievilItemCategory.PROGRESSION, True),
    ("Moon Rune: The Time Device", 144, MedievilItemCategory.PROGRESSION, True),

    ("Star Rune: Return to the Graveyard", 145, MedievilItemCategory.PROGRESSION, True),
    ("Star Rune: Dan's Crypt", 146, MedievilItemCategory.PROGRESSION, True),
    ("Star Rune: The Crystal Caves", 147, MedievilItemCategory.PROGRESSION, True),
    ("Star Rune: The Lake", 148, MedievilItemCategory.PROGRESSION, True),
    ("Star Rune: Enchanted Earth", 149, MedievilItemCategory.PROGRESSION, True),
    ("Star Rune: The Gallows Gauntlet", 150, MedievilItemCategory.PROGRESSION, True),
    ("Star Rune: Ghost Ship", 151, MedievilItemCategory.PROGRESSION, True),

    ("Time Rune: The Lake", 152, MedievilItemCategory.PROGRESSION, True),
    ("Time Rune: Pumpkin Gorge", 153, MedievilItemCategory.PROGRESSION, True),
    ("Time Rune: The Time Device", 154, MedievilItemCategory.PROGRESSION, True)
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
                
    progression_and_weapon_items = [
        item_data.name for item_data in _all_items
        if item_data.progression or item_data.category == MedievilItemCategory.WEAPON
    ]
    
    for item_name in progression_and_weapon_items:
        if item_name not in item_pool_names and len(item_pool_names) < count:
            item_pool_names.append(item_name)
    
    # Populate the rest of the pool with random filler items
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