from typing import Dict
from BaseClasses import Item

class NoitaItem(Item):
    game: str = "Noita"

# 110000 - 110013
item_table: Dict[str, int] = {
    "Bad":              110000,
    "Heart":            110001,
    "Refresh":          110002,
    "Potion":           110003,
    "Gold (10)":        110004,
    "Gold (50)":        110005,
    "Gold (200)":       110006,
    "Gold (1000)":      110007,
    "Wand (Tier 1)":    110008,
    "Wand (Tier 2)":    110009,
    "Wand (Tier 3)":    110010,
    "Wand (Tier 4)":    110011,
    "Wand (Tier 5)":    110012,
    "Wand (Tier 6)":    110013,

}

default_weights: Dict[str, int] = {
    "Gold (10)":        40,
    "Wand (Tier 1)":    10,
    "Potion":           35,
    "Gold (50)":        30,
    "Refresh":          25,
    "Heart":            25,
    "Wand (Tier 2)":    9,
    "Wand (Tier 3)":    8,
    "Bad":              15,
    "Gold (200)":       15,
    "Wand (Tier 4)":    7,
    "Wand (Tier 5)":    6,
    "Gold (1000)":      5,
    "Wand (Tier 6)":    4
}

no_bad_weights: Dict[str, int] = {
    "Gold (10)":        40,
    "Wand (Tier 1)":    10,
    "Potion":           35,
    "Gold (50)":        30,
    "Refresh":          25,
    "Heart":            25,
    "Wand (Tier 2)":    9,
    "Wand (Tier 3)":    8,
    "Bad":              0,
    "Gold (200)":       15,
    "Wand (Tier 4)":    7,
    "Wand (Tier 5)":    6,
    "Gold (1000)":      5,
    "Wand (Tier 6)":    4
}

item_pool_weights: Dict[int, Dict[str, int]] = {
    0:      default_weights,
    1:      no_bad_weights
}

lookup_id_to_name: Dict[int, str] = {id: name for name, id in item_table.items()}