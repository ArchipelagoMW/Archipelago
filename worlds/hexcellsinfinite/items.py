from BaseClasses import Item, ItemClassification
from .types import ItemData, HexcellsInfiniteItem
from .options import LevelUnlockType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import HexcellsInfiniteWorld

def create_itempool(world: "HexcellsInfiniteWorld") -> list[Item]:
    itempool: list[Item] = []

    if world.options.LevelUnlockType == LevelUnlockType.option_vanilla:
        itempool.extend(create_multiple_items(world, "Gem", 36))
    elif world.options.LevelUnlockType == LevelUnlockType.option_individual:
        for item in item_table.keys():
            if item != "Gem":
                itempool.append(create_item(world, item))

    return itempool

def create_item(world: "HexcellsInfiniteWorld", name: str) -> Item:
    data = item_table[name]
    return HexcellsInfiniteItem(name, data.classification, data.ap_code, world.player)

def create_multiple_items(world: "HexcellsInfiniteWorld", name: str, count: int,
                          item_type: ItemClassification = ItemClassification.progression) -> list[Item]:
    
    return [HexcellsInfiniteItem(name, item_type, item_table[name].ap_code, world.player) for _ in range(count)]

item_table: dict[str, ItemData] = {}

HEXCELLS_LEVEL_ITEMS = []

for world in range(1, 7):
    for level in range(1, 7):
        name = f"Hexcells {world}-{level}"
        item_table[name] = ItemData(len(item_table)+1, ItemClassification.progression)
        HEXCELLS_LEVEL_ITEMS.append(name)
item_table["Gem"] = ItemData(len(item_table)+1, ItemClassification.progression)
