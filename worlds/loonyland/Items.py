from typing import NamedTuple, Dict

from BaseClasses import Item, ItemClassification
from worlds.AutoWorld import World
from enum import Enum

loonyland_base_id: int = 2876900


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


class LoonylandItemData(NamedTuple):
    id: int
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

loony_item_table: Dict[str, LoonylandItemData] = {
    "Heart": LoonylandItemData(loonyland_base_id + 0, ItemCategory.ITEM, ItemClassification.useful),
    "Lightning": LoonylandItemData(loonyland_base_id + 1, ItemCategory.ITEM, ItemClassification.useful),
    "Arrow": LoonylandItemData(loonyland_base_id + 2, ItemCategory.ITEM, ItemClassification.useful),
    "Pants": LoonylandItemData(loonyland_base_id + 3, ItemCategory.ITEM, ItemClassification.useful),
    "Mushroom": LoonylandItemData(loonyland_base_id + 4, ItemCategory.ITEM, ItemClassification.progression),
    "Orb": LoonylandItemData(loonyland_base_id + 5, ItemCategory.ITEM, ItemClassification.progression),
    "Bombs": LoonylandItemData(loonyland_base_id + 6, ItemCategory.ITEM, ItemClassification.progression),
    "Shock Wand": LoonylandItemData(loonyland_base_id + 7, ItemCategory.ITEM, ItemClassification.progression),
    "Ice Spear": LoonylandItemData(loonyland_base_id + 8, ItemCategory.ITEM, ItemClassification.progression),
    "Cactus": LoonylandItemData(loonyland_base_id + 9, ItemCategory.ITEM, ItemClassification.progression),
    "Boomerang": LoonylandItemData(loonyland_base_id + 10, ItemCategory.ITEM, ItemClassification.progression),
    "Whoopee": LoonylandItemData(loonyland_base_id + 11, ItemCategory.ITEM, ItemClassification.progression),
    "Hot Pants": LoonylandItemData(loonyland_base_id + 12, ItemCategory.ITEM, ItemClassification.progression),
    "Skull Key": LoonylandItemData(loonyland_base_id + 13, ItemCategory.ITEM, ItemClassification.progression),
    "Bat Key": LoonylandItemData(loonyland_base_id + 14, ItemCategory.ITEM, ItemClassification.progression),
    "Pumpkin Key": LoonylandItemData(loonyland_base_id + 15, ItemCategory.ITEM, ItemClassification.progression),
    "Boots": LoonylandItemData(loonyland_base_id + 16, ItemCategory.ITEM, ItemClassification.progression),
    "Stick": LoonylandItemData(loonyland_base_id + 17, ItemCategory.ITEM, ItemClassification.progression),
    "Fertilizer": LoonylandItemData(loonyland_base_id + 18, ItemCategory.ITEM, ItemClassification.progression),
    "Silver": LoonylandItemData(loonyland_base_id + 19, ItemCategory.ITEM, ItemClassification.progression),
    "Doom Daisy": LoonylandItemData(loonyland_base_id + 20, ItemCategory.ITEM, ItemClassification.progression),
    "Ghost Potion": LoonylandItemData(loonyland_base_id + 21, ItemCategory.ITEM, ItemClassification.progression),
    "Vamp Statue": LoonylandItemData(loonyland_base_id + 22, ItemCategory.ITEM, ItemClassification.progression),
    "Cat": LoonylandItemData(loonyland_base_id + 23, ItemCategory.ITEM, ItemClassification.progression),
    "Big Gem": LoonylandItemData(loonyland_base_id + 24, ItemCategory.ITEM, ItemClassification.progression),
    "Zombie Reward": LoonylandItemData(loonyland_base_id + 25, ItemCategory.ITEM, ItemClassification.filler),
    "3 way": LoonylandItemData(loonyland_base_id + 26, ItemCategory.ITEM, ItemClassification.useful),
    "Happy Stick": LoonylandItemData(loonyland_base_id + 27, ItemCategory.ITEM, ItemClassification.progression),
    "Bat Statue": LoonylandItemData(loonyland_base_id + 28, ItemCategory.ITEM, ItemClassification.progression),
    "Lantern": LoonylandItemData(loonyland_base_id + 29, ItemCategory.ITEM, ItemClassification.progression),
    "Reflect": LoonylandItemData(loonyland_base_id + 30, ItemCategory.ITEM, ItemClassification.useful),
    "Silver Sling": LoonylandItemData(loonyland_base_id + 31, ItemCategory.ITEM, ItemClassification.progression)
    # TODO add cheats
    # TODO filler
    # TODO traps
    # TODO event
}
