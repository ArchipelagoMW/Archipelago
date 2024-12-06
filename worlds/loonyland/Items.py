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
    "Heart": ItemData(ItemCategory.ITEM, ItemClassification.useful),
    "Lightning": ItemData(ItemCategory.ITEM, ItemClassification.useful),
    "Arrow": ItemData(ItemCategory.ITEM, ItemClassification.useful),
    "Pants": ItemData(ItemCategory.ITEM, ItemClassification.useful),
    "Mushroom": ItemData(ItemCategory.ITEM, ItemClassification.progression),
    "Orb": ItemData(ItemCategory.ITEM, ItemClassification.progression),
    "Bombs": ItemData(ItemCategory.ITEM, ItemClassification.progression),
    "Shock Wand": ItemData(ItemCategory.ITEM, ItemClassification.progression),
    "Ice spear": ItemData(ItemCategory.ITEM,  ItemClassification.progression),
    "Cactus": ItemData(ItemCategory.ITEM, ItemClassification.progression),
    "Boomerang": ItemData(ItemCategory.ITEM, ItemClassification.progression),
    "Whoopee": ItemData(ItemCategory.ITEM, ItemClassification.progression),
    "Hot Pants": ItemData(ItemCategory.ITEM, ItemClassification.progression),
    "Skull Key": ItemData(ItemCategory.ITEM, ItemClassification.progression),
    "Bat Key": ItemData(ItemCategory.ITEM, ItemClassification.progression),
    "Pumpkin Key": ItemData(ItemCategory.ITEM, ItemClassification.progression),
    "Boots": ItemData(ItemCategory.ITEM, ItemClassification.progression),
    "Stick": ItemData(ItemCategory.ITEM, ItemClassification.progression),
    "Fertilizer": ItemData(ItemCategory.ITEM, ItemClassification.progression),
    "Silver": ItemData(ItemCategory.ITEM, ItemClassification.progression),
    "Doom Daisy": ItemData(ItemCategory.ITEM, ItemClassification.progression),
    "Ghost Potion": ItemData(ItemCategory.ITEM, ItemClassification.progression),
    "Vamp Statue": ItemData(ItemCategory.ITEM,  ItemClassification.progression),
    "Cat": ItemData(ItemCategory.ITEM, ItemClassification.progression),
    "Big Gem": ItemData(ItemCategory.ITEM, ItemClassification.progression),
    "Zombie Reward": ItemData(ItemCategory.ITEM, ItemClassification.filler),
    "3 way": ItemData(ItemCategory.ITEM, ItemClassification.useful),
    "Happy Stick": ItemData(ItemCategory.ITEM, ItemClassification.progression),
    "Bat Statue": ItemData(ItemCategory.ITEM, ItemClassification.progression),
    "Lantern": ItemData(ItemCategory.ITEM, ItemClassification.progression),
    "Reflect": ItemData(ItemCategory.ITEM, ItemClassification.useful),
    "Silver Sling": ItemData(ItemCategory.ITEM, ItemClassification.progression)
    }