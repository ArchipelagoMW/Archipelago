from BaseClasses import Item, ItemClassification
from .Types import ItemData, Sly1Item
from .Locations import get_total_locations
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from . import Sly1World

def create_itempool(world: "Sly1World") -> List[Item]:
    itempool: List[Item] = []

    for name in item_table.keys():
        item_type: ItemClassification = item_table.get(name).classification
        item_amount: int = item_table.get(name).count
    
        itempool += create_multiple_items(world, name, item_amount, item_type)

    itempool += create_junk_items(world, get_total_locations() - len(itempool))
    return itempool

def create_item(world: "Sly1World", name: str) -> Item:
    data = item_table[name]
    return Sly1Item(name, data.classification, data.ap_code, world.player)

def create_multiple_items(world: "Sly1World", name: str, count: int = 1,
                          item_type: ItemClassification = ItemClassification.progression) -> List[Item]:
    data = item_table[name]
    itemlist: List[Item] = []

    for i in range(count):
        itemlist += [Sly1Item(name, item_type, data.ap_code, world.player)]

    return itemlist

# Fix this, it sucks ass
def create_junk_items(world: "Sly1World", count: int) -> List[Item]:
    junk_pool: List[Item] = []
    # For now, all junk has equal weights
    for i in range(count):
        junk_pool.append(world.create_item(world.random.choices(list(junk_items.keys()), k=1)[0]))
    return junk_pool

sly_items = {
    # Progressive Moves
    "Progressive Dive Attack": ItemData(100020001, ItemClassification.useful, 2),
    "Progressive Roll": ItemData(100020002, ItemClassification.useful, 2),
    "Progressive Slow Motion": ItemData(100020003, ItemClassification.useful, 3),
    "Progressive Safety": ItemData(100020007, ItemClassification.useful, 2),
    "Progressive Invisibility": ItemData(100020010, ItemClassification.progression_skip_balancing, 2),
    
    # Non-progressive Moves
    "Coin Magnet": ItemData(100020004, ItemClassification.useful),
    "Mine": ItemData(100020005, ItemClassification.useful),
    "Fast": ItemData(100020006, ItemClassification.useful),
    "Decoy": ItemData(100020008, ItemClassification.useful),
    "Hacking": ItemData(100020009, ItemClassification.useful),

    # Blueprints
    "ToT Blueprints": ItemData(100020011, ItemClassification.useful),
    "SSE Blueprints": ItemData(100020012, ItemClassification.useful),
    "VV Blueprints": ItemData(100020013, ItemClassification.useful),
    "FitS Blueprints": ItemData(100020014, ItemClassification.useful),

    # Keys
    "ToT Key": ItemData(100020015, ItemClassification.progression, 7),
    "SSE Key": ItemData(100020016, ItemClassification.progression, 7),
    "VV Key": ItemData(100020017, ItemClassification.progression, 7),
    "FitS Key": ItemData(100020018, ItemClassification.progression, 7),

    # Levels/Worlds - TBI
}

junk_items = {
    # Junk
    "Charm": ItemData(100020019, ItemClassification.filler),
    "1-Up": ItemData(100020020, ItemClassification.filler)

    # Traps - TBI
}

item_table = {
    **sly_items
}