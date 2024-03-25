"""
Author: Louis M
Date: Fri, 15 Mar 2024 18:41:40 +0000
Description: Manage items in the Aquaria game multiworld randomizer
"""

from typing import Optional
from enum import Enum
from BaseClasses import Item, ItemClassification

class ItemType(Enum):
    """
    Used to indicate to the multi-world if an item is usefull or not
    """
    NORMAL = 0
    PROGRESSION = 1
    JUNK = 2

class ItemGroup(Enum):
    """
    Used to group items
    """
    COLLECTIBLE = 0
    INGREDIENT = 1
    RECIPE = 2
    HEALTH = 3
    UTILITY = 4
    SONG = 5
    LOGIC = 6

class AquariaItem(Item):
    """
    A single item in the Aquaria game.
    """
    game: str = "Aquaria"
    """The name of the game"""

    def __init__(self, name: str, classification: ItemClassification,
                 code: Optional[int], player: int):
        """
        Initialisation of the Item
        :param name: The name of the item
        :param classification: If the item is usefull or not
        :param code: The ID of the item (if None, it is an event)
        :param player: The ID of the player in the multiworld
        """
        super().__init__(name, classification, code, player)

"""Information data for every (not event) item."""
item_table = {
    #       name:           ID,    Nb,   Item Type,        Item Group
    "Anemone": (698000, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "Arnassi statue": (698001, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "Big seed": (698002, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "Glowing seed": (698003, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "Black pearl": (698004, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "Baby blaster": (698005, 1, ItemType.NORMAL, ItemGroup.UTILITY),
    "Crab armor": (698006, 1, ItemType.NORMAL, ItemGroup.UTILITY),
    "Baby dumbo": (698007, 1, ItemType.NORMAL, ItemGroup.UTILITY),
    "Tooth": (698008, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "Energy statue": (698009, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "Krotite armor": (698010, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "Golden starfish": (698011, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "Golden gear": (698012, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "Jelly beacon": (698013, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "Jelly costume": (698014, 1, ItemType.NORMAL, ItemGroup.UTILITY),
    "Jelly plant": (698015, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "Mithalas doll": (698016, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "Mithalan dress": (698017, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "Mithalas banner": (698018, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "Mithalas pot": (698019, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "Mutant costume": (698020, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "Baby nautilus": (698021, 1, ItemType.NORMAL, ItemGroup.UTILITY),
    "Baby piranha": (698022, 1, ItemType.NORMAL, ItemGroup.UTILITY),
    "Arnassi Armor": (698023, 1, ItemType.NORMAL, ItemGroup.UTILITY),
    "Seed bag": (698024, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "King's Skull": (698025, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "Song plant spore": (698026, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "Stone head": (698027, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "Sun key": (698028, 1, ItemType.NORMAL, ItemGroup.COLLECTIBLE),
    "Girl costume": (698029, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "Odd container": (698030, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "Trident": (698031, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "Turtle egg": (698032, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "Jelly egg": (698033, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "Urchin costume": (698034, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "Baby walker": (698035, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "Vedha's Cure-All-All": (698036, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "Zuuna's perogi": (698037, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "Arcane poultice": (698038, 7, ItemType.NORMAL, ItemGroup.RECIPE),
    "Berry ice cream": (698039, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "Buttery sea loaf": (698040, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "Cold borscht": (698041, 2, ItemType.NORMAL, ItemGroup.RECIPE),
    "Cold soup": (698042, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "Crab cake": (698043, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "Divine soup": (698044, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "Dumbo ice cream": (698045, 3, ItemType.NORMAL, ItemGroup.RECIPE),
    "Eel oil": (698046, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "Fish meat": (698047, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "Fish oil": (698048, 2, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "Glowing egg": (698049, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "Hand roll": (698050, 5, ItemType.NORMAL, ItemGroup.RECIPE),
    "Healing poultice": (698051, 4, ItemType.NORMAL, ItemGroup.RECIPE),
    "Hearty soup": (698052, 5, ItemType.NORMAL, ItemGroup.RECIPE),
    "Hot borscht": (698053, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "Hot soup": (698054, 3, ItemType.PROGRESSION, ItemGroup.RECIPE),
    "Ice cream": (698055, 2, ItemType.NORMAL, ItemGroup.RECIPE),
    "Leadership roll": (698056, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "Leaf poultice": (698057, 1, ItemType.PROGRESSION, ItemGroup.RECIPE),
    "Leeching poultice": (698058, 4, ItemType.NORMAL, ItemGroup.RECIPE),
    "Legendary cake": (698059, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "Loaf of life": (698060, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "Long life soup": (698061, 2, ItemType.NORMAL, ItemGroup.RECIPE),
    "Magic soup": (698062, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "Mushroom x 2": (698063, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "Perogi": (698064, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "Plant leaf": (698065, 3, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "Plump perogi": (698066, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "Poison loaf": (698067, 1, ItemType.JUNK, ItemGroup.RECIPE),
    "Poison soup": (698068, 1, ItemType.JUNK, ItemGroup.RECIPE),
    "Rainbow mushroom": (698069, 4, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "Rainbow soup": (698070, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "Red berry": (698071, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "Red bulb x 2": (698072, 3, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "Rotten cake": (698073, 1, ItemType.JUNK, ItemGroup.RECIPE),
    "Rotten loaf x 8": (698074, 1, ItemType.JUNK, ItemGroup.RECIPE),
    "Rotten meat": (698075, 5, ItemType.JUNK, ItemGroup.INGREDIENT),
    "Royal soup": (698076, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "Sea cake": (698077, 4, ItemType.NORMAL, ItemGroup.RECIPE),
    "Sea loaf": (698078, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "Shark fin soup": (698079, 2, ItemType.NORMAL, ItemGroup.RECIPE),
    "Sight poultice": (698080, 2, ItemType.NORMAL, ItemGroup.RECIPE),
    "Small bone x 2": (698081, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "Small egg": (698082, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "Small tentacle x 2": (698083, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "Special bulb": (698084, 5, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "Special cake": (698085, 2, ItemType.NORMAL, ItemGroup.RECIPE),
    "Spicy meat x 2": (698086, 3, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "Spicy roll": (698087, 11, ItemType.NORMAL, ItemGroup.RECIPE),
    "Spicy soup": (698088, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "Spider roll": (698089, 2, ItemType.NORMAL, ItemGroup.RECIPE),
    "Swamp cake": (698090, 3, ItemType.NORMAL, ItemGroup.RECIPE),
    "Tasty cake": (698091, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "Tasty roll": (698092, 2, ItemType.NORMAL, ItemGroup.RECIPE),
    "Tough cake": (698093, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "Turtle soup": (698094, 2, ItemType.NORMAL, ItemGroup.RECIPE),
    "Vedha sea crisp": (698095, 2, ItemType.NORMAL, ItemGroup.RECIPE),
    "Veggie cake": (698096, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "Veggie ice cream": (698097, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "Veggie soup": (698098, 2, ItemType.NORMAL, ItemGroup.RECIPE),
    "Volcano roll": (698099, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "Health upgrade": (698100, 5, ItemType.NORMAL, ItemGroup.HEALTH),
    "Wok": (698101, 1, ItemType.NORMAL, ItemGroup.UTILITY),
    "Eel oil x 2": (698102, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "Fish meat x 2": (698103, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "Fish oil x 3": (698104, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "Glowing egg x 2": (698105, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "Healing poultice x 2": (698106, 2, ItemType.NORMAL, ItemGroup.RECIPE),
    "Hot soup x 2": (698107, 3, ItemType.PROGRESSION, ItemGroup.RECIPE),
    "Leadership roll x 2": (698108, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "Leaf poultice x 3": (698109, 2, ItemType.PROGRESSION, ItemGroup.RECIPE),
    "Plant leaf x 2": (698110, 2, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "Plant leaf x 3": (698111, 4, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "Rotten meat x 2": (698112, 1, ItemType.JUNK, ItemGroup.INGREDIENT),
    "Rotten meat x 8": (698113, 1, ItemType.JUNK, ItemGroup.INGREDIENT),
    "Sea loaf x 2": (698114, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "Small bone x 3": (698115, 3, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "Small egg x 2": (698116, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "Li and Li song": (698117, 1, ItemType.PROGRESSION, ItemGroup.SONG),
    "Shield song": (698118, 1, ItemType.NORMAL, ItemGroup.SONG),
    "Beast form": (698119, 1, ItemType.PROGRESSION, ItemGroup.SONG),
    "Sun form": (698120, 1, ItemType.PROGRESSION, ItemGroup.SONG),
    "Nature form": (698121, 1, ItemType.PROGRESSION, ItemGroup.SONG),
    "Energy form": (698122, 1, ItemType.PROGRESSION, ItemGroup.SONG),
    "Bind song": (698123, 1, ItemType.PROGRESSION, ItemGroup.SONG),
    "Fish form": (698124, 1, ItemType.PROGRESSION, ItemGroup.SONG),
    "Spirit form": (698125, 1, ItemType.PROGRESSION, ItemGroup.SONG),
}

