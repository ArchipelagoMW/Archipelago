from BaseClasses import Item, ItemClassification
from worlds.AutoWorld import World


loonyland_base_id: int 2876900

class LoonylandItem(Item):
    """
    Item from the game Loonyland
    """
    game: str = "Loonyland"
    
    
class ItemCategory(Enum):
    ITEM = 0
    CHEAT = 1
    FILLER = 2
    TRAP = 3
    EVENT = 4
    
    
class ItemData(NamedTuple):
    category: ItemCategory
    classification: ItemClassification

item_frequencies = {
    "Heart": 20,
    "Lightning": 10,
    "Arrow": 10,
    "Pants": 10,
    "Mushroom": 10,
    "Orb": 4,
    "Vamp Statue": 8,
    "Big Gem": 6,
    "Bat Statue": 4
}    
    
item_table: Dict[str, ItemData] = {
    "Heart": ItemData(ItemCategory.ITEM, ItemClassification.useful
    "Lightning": ItemCategory.ITEM, ItemClassification.useful
    "Arrow": ItemCategory.ITEM, ItemClassification.useful
    "Pants": ItemCategory.ITEM, ItemClassification.useful
    "Mushroom": ItemCategory.ITEM, ItemClassification.progression
    "Orb": ItemCategory.ITEM, ItemClassification.progression
    "Bombs": ItemCategory.ITEM, ItemClassification.progression
    "Shock Wand": ItemCategory.ITEM, ItemClassification.progression
    "Ice spear": ItemCategory.ITEM,  ItemClassification.progression
    "Cactus": ItemCategory.ITEM, ItemClassification.progression
    "Boomerang": ItemCategory.ITEM, ItemClassification.progression
    "Whoopee": ItemCategory.ITEM, ItemClassification.progression
    "Hot Pants": ItemCategory.ITEM, ItemClassification.progression
    "Skull Key": ItemCategory.ITEM, ItemClassification.progression
    "Bat Key": ItemCategory.ITEM, ItemClassification.progression
    "Pumpkin Key": ItemCategory.ITEM, ItemClassification.progression
    "Boots": ItemCategory.ITEM, ItemClassification.progression
    "Stick": ItemCategory.ITEM, ItemClassification.progression
    "Fertilizer": ItemCategory.ITEM, ItemClassification.progression
    "Silver": ItemCategory.ITEM, ItemClassification.progression
    "Doom Daisy": ItemCategory.ITEM, ItemClassification.progression
    "Ghost Potion": ItemCategory.ITEM, ItemClassification.progression
    "Vamp Statue": ItemCategory.ITEM,  ItemClassification.progression
    "Cat": ItemCategory.ITEM, ItemClassification.progression
    "Big Gem": ItemCategory.ITEM, ItemClassification.progression
    "Zombie Reward": ItemCategory.ITEM, ItemClassification.filler
    "3 way": ItemCategory.ITEM, ItemClassification.useful
    "Happy Stick": ItemCategory.ITEM, ItemClassification.progression
    "Bat Statue": ItemCategory.ITEM, ItemClassification.progression
    "Lantern": ItemCategory.ITEM, ItemClassification.progression
    "Reflect": ItemCategory.ITEM, ItemClassification.useful
    "Silver Sling": ItemCategory.ITEM, ItemClassification.progression