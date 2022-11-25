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
    "Perk (Fire Immunity)": 110014,
    "Perk (Toxic Immunity)":    110015,
    "Perk (Explosion Immunity)":    110016,
    "Perk (Melee Immunity)":    110017,
    "Perk (Electricity Immunity)":  110018,
    "Perk (Tinker With Wands Everywhere)":  110019,
    "Perk (All-Seeing Eye)":    110020,
    "Perk (Extra Life)":    110021
}

required_items: Dict[str, int] = {
    "Perk (Fire Immunity)":                 1,
    "Perk (Toxic Immunity)":                1,
    "Perk (Explosion Immunity)":            1,
    "Perk (Melee Immunity)":                1,
    "Perk (Electricity Immunity)":          1,
    "Perk (Tinker With Wands Everywhere)":  1,
    "Perk (All-Seeing Eye)":                1
}

#optional_pool_items: Dict[str, int] ={
#    "Heart": 1,
#the 1 is a placeholder until I figure out how to make it controlled by the yaml
#probably going to have a specific number of hearts in the pool? idk yet, might leave it as random
#}

default_weights: Dict[str, int] = {
    "Wand (Tier 1)":    10,
    "Potion":           35,
    "Refresh":          25,
    "Heart":            25,
    "Wand (Tier 2)":    9,
    "Wand (Tier 3)":    8,
    "Bad":              15,
    "Gold (200)":       15,
    "Wand (Tier 4)":    7,
    "Wand (Tier 5)":    6,
    "Gold (1000)":      5,
    "Wand (Tier 6)":    4,
    "Perk (Extra Life)": 4
}

no_bad_weights: Dict[str, int] = {
    "Wand (Tier 1)":    10,
    "Potion":           35,
    "Refresh":          25,
    "Heart":            25,
    "Wand (Tier 2)":    9,
    "Wand (Tier 3)":    8,
    "Bad":              0,
    "Gold (200)":       15,
    "Wand (Tier 4)":    7,
    "Wand (Tier 5)":    6,
    "Gold (1000)":      5,
    "Wand (Tier 6)":    4,
    "Perk (Extra Life)": 4
}

item_pool_weights: Dict[int, Dict[str, int]] = {
    0:      no_bad_weights,
    1:      default_weights
}