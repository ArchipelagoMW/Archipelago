from typing import NamedTuple, Dict

from BaseClasses import Item, ItemClassification
from worlds.AutoWorld import World
from enum import Enum
from .Defines import *

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
    "Heart": LoonylandItemData(loonyland_base_id + VAR_HEART, ItemCategory.ITEM, ItemClassification.useful),
    "Lightning": LoonylandItemData(loonyland_base_id + VAR_LIGHTNING, ItemCategory.ITEM, ItemClassification.useful),
    "Arrow": LoonylandItemData(loonyland_base_id + VAR_ARROW, ItemCategory.ITEM, ItemClassification.useful),
    "Pants": LoonylandItemData(loonyland_base_id + VAR_PANTS, ItemCategory.ITEM, ItemClassification.useful),
    "Mushroom": LoonylandItemData(loonyland_base_id + VAR_MUSHROOM, ItemCategory.ITEM, ItemClassification.progression),
    "Orb": LoonylandItemData(loonyland_base_id + VAR_MYSORB, ItemCategory.ITEM, ItemClassification.progression),
    "Bombs": LoonylandItemData(loonyland_base_id + VAR_WEAPON, ItemCategory.ITEM, ItemClassification.progression),
    "Shock Wand": LoonylandItemData(loonyland_base_id + VAR_WEAPON + 1, ItemCategory.ITEM, ItemClassification.progression),
    "Ice Spear": LoonylandItemData(loonyland_base_id + VAR_WEAPON + 2, ItemCategory.ITEM, ItemClassification.progression),
    "Cactus": LoonylandItemData(loonyland_base_id + VAR_WEAPON + 3, ItemCategory.ITEM, ItemClassification.progression),
    "Boomerang": LoonylandItemData(loonyland_base_id + VAR_WEAPON + 4, ItemCategory.ITEM, ItemClassification.progression),
    "Whoopee": LoonylandItemData(loonyland_base_id + VAR_WEAPON + 5, ItemCategory.ITEM, ItemClassification.progression),
    "Hot Pants": LoonylandItemData(loonyland_base_id + VAR_WEAPON + 6, ItemCategory.ITEM, ItemClassification.progression),
    "Skull Key": LoonylandItemData(loonyland_base_id + VAR_SKULLKEY, ItemCategory.ITEM, ItemClassification.progression),
    "Bat Key": LoonylandItemData(loonyland_base_id + VAR_BATKEY, ItemCategory.ITEM, ItemClassification.progression),
    "Pumpkin Key": LoonylandItemData(loonyland_base_id + VAR_PUMPKINKEY, ItemCategory.ITEM, ItemClassification.progression),
    "Boots": LoonylandItemData(loonyland_base_id + VAR_BOOTS, ItemCategory.ITEM, ItemClassification.progression),
    "Stick": LoonylandItemData(loonyland_base_id + VAR_STICK, ItemCategory.ITEM, ItemClassification.progression),
    "Fertilizer": LoonylandItemData(loonyland_base_id + VAR_FERTILIZER, ItemCategory.ITEM, ItemClassification.progression),
    "Silver": LoonylandItemData(loonyland_base_id + VAR_SILVER, ItemCategory.ITEM, ItemClassification.progression),
    "Doom Daisy": LoonylandItemData(loonyland_base_id + VAR_DAISY, ItemCategory.ITEM, ItemClassification.progression),
    "Ghost Potion": LoonylandItemData(loonyland_base_id + VAR_POTION, ItemCategory.ITEM, ItemClassification.progression),
    "Vamp Statue": LoonylandItemData(loonyland_base_id + VAR_VAMPBUST, ItemCategory.ITEM, ItemClassification.progression),
    "Cat": LoonylandItemData(loonyland_base_id + VAR_CAT, ItemCategory.ITEM, ItemClassification.progression),
    "Big Gem": LoonylandItemData(loonyland_base_id + VAR_GEM, ItemCategory.ITEM, ItemClassification.progression),
    "Zombie Reward": LoonylandItemData(loonyland_base_id + VAR_ZOMBIEGEM, ItemCategory.ITEM, ItemClassification.filler),
    "3 way": LoonylandItemData(loonyland_base_id + VAR_TRIPLEFIRE, ItemCategory.ITEM, ItemClassification.useful),
    "Happy Stick": LoonylandItemData(loonyland_base_id + VAR_TALISMAN, ItemCategory.ITEM, ItemClassification.progression),
    "Bat Statue": LoonylandItemData(loonyland_base_id + VAR_BATSTATUE, ItemCategory.ITEM, ItemClassification.progression),
    "Lantern": LoonylandItemData(loonyland_base_id + VAR_LANTERN, ItemCategory.ITEM, ItemClassification.progression),
    "Reflect": LoonylandItemData(loonyland_base_id + VAR_REFLECT, ItemCategory.ITEM, ItemClassification.useful),
    "Silver Sling": LoonylandItemData(loonyland_base_id + VAR_SILVERSLING, ItemCategory.ITEM, ItemClassification.progression)
    # TODO add cheats
    # TODO filler
    # TODO traps
    # TODO event
}
