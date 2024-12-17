from typing import Dict

from BaseClasses import ItemClassification as IC
from worlds.loonyland import loonyland_base_id as ll_base_id
from worlds.loonyland.Data.Defines import *
from worlds.loonyland.Items import LL_Item, LL_ItemCat

loony_item_table: Dict[str, LL_Item] = {
    "Heart" : LL_Item(ll_base_id + VAR_HEART, LL_ItemCat.ITEM, IC.useful, 20),
    "Lightning" : LL_Item(ll_base_id + VAR_LIGHTNING, LL_ItemCat.ITEM, IC.useful, 10),
    "Arrow" : LL_Item(ll_base_id + VAR_ARROW, LL_ItemCat.ITEM, IC.useful, 10),
    "Pants" : LL_Item(ll_base_id + VAR_PANTS, LL_ItemCat.ITEM, IC.useful, 10),
    "Mushroom" : LL_Item(ll_base_id + VAR_MUSHROOM, LL_ItemCat.ITEM, IC.progression, 10),
    "Orb" : LL_Item(ll_base_id + VAR_MYSORB, LL_ItemCat.ITEM, IC.progression, 4),
    "Bombs" : LL_Item(ll_base_id + VAR_WBOMBS, LL_ItemCat.ITEM, IC.progression),
    "Shock Wand" : LL_Item(ll_base_id + VAR_WLIGHTNING, LL_ItemCat.ITEM, IC.progression),
    "Ice Spear" : LL_Item(ll_base_id + VAR_WICE, LL_ItemCat.ITEM, IC.progression),
    "Cactus" : LL_Item(ll_base_id + VAR_WCACTUS, LL_ItemCat.ITEM, IC.progression),
    "Boomerang" : LL_Item(ll_base_id + VAR_WBOOMERANG, LL_ItemCat.ITEM, IC.progression),
    "Whoopee" : LL_Item(ll_base_id + VAR_WWHOOPEE, LL_ItemCat.ITEM, IC.progression),
    "Hot Pants" : LL_Item(ll_base_id + VAR_WHOTPANTS, LL_ItemCat.ITEM, IC.progression),
    "Skull Key" : LL_Item(ll_base_id + VAR_SKULLKEY, LL_ItemCat.ITEM, IC.progression),
    "Bat Key" : LL_Item(ll_base_id + VAR_BATKEY, LL_ItemCat.ITEM, IC.progression),
    "Pumpkin Key" : LL_Item(ll_base_id + VAR_PUMPKINKEY, LL_ItemCat.ITEM, IC.progression),
    "Boots" : LL_Item(ll_base_id + VAR_BOOTS, LL_ItemCat.ITEM, IC.progression),
    "Stick" : LL_Item(ll_base_id + VAR_STICK, LL_ItemCat.ITEM, IC.progression),
    "Fertilizer" : LL_Item(ll_base_id + VAR_FERTILIZER, LL_ItemCat.ITEM, IC.progression),
    "Silver" : LL_Item(ll_base_id + VAR_SILVER, LL_ItemCat.ITEM, IC.progression),
    "Doom Daisy" : LL_Item(ll_base_id + VAR_DAISY, LL_ItemCat.ITEM, IC.progression),
    "Ghost Potion" : LL_Item(ll_base_id + VAR_POTION, LL_ItemCat.ITEM, IC.progression),
    "Vampire Bust" : LL_Item(ll_base_id + VAR_VAMPBUST, LL_ItemCat.ITEM, IC.progression, 8),
    "Cat" : LL_Item(ll_base_id + VAR_CAT, LL_ItemCat.ITEM, IC.progression),
    "Big Gem" : LL_Item(ll_base_id + VAR_GEM, LL_ItemCat.ITEM, IC.progression, 6),
    "100 Gems" : LL_Item(ll_base_id + VAR_ZOMBIEGEM, LL_ItemCat.ITEM, IC.filler),
    "Triple Fire Gem" : LL_Item(ll_base_id + VAR_TRIPLEFIRE, LL_ItemCat.ITEM, IC.useful),
    "Happy Stick" : LL_Item(ll_base_id + VAR_TALISMAN, LL_ItemCat.ITEM, IC.progression),
    "Bat Statue" : LL_Item(ll_base_id + VAR_BATSTATUE, LL_ItemCat.ITEM, IC.progression, 4),
    "Lantern" : LL_Item(ll_base_id + VAR_LANTERN, LL_ItemCat.ITEM, IC.progression),
    "Reflect Gem" : LL_Item(ll_base_id + VAR_REFLECT, LL_ItemCat.ITEM, IC.useful),
    "Silver Sling" : LL_Item(ll_base_id + VAR_SILVERSLING, LL_ItemCat.ITEM, IC.progression),
}