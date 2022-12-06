import itertools
from typing import Dict
from BaseClasses import Item, ItemClassification

class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    group: str
    required_num: int = 0
    classification: ItemClassification = item_group_classification[group]

class NoitaItem(Item):
    game: str = "Noita"


def create_item(player: int, name: str) -> Item:
    item_data = item_table[name]
    return NoitaItem(name, item_data.classification, item_data.code, player)


def create_all_items(world, player: int) -> None:
    pool_option = world.bad_effects[player].value
    total_locations = world.total_locations[player].value

    # Generate item pool
    itempool: List = []
    for item_name, count in required_items.items():
        itempool += [item_name] * count

    # Add other junk to the pool
    junk_pool = item_pool_weights[pool_option]
    for i in range(1, total_locations + 1):
        itempool += world.random.choices(list(junk_pool.keys()), weights=list(junk_pool.values()))

    # Convert itempool into real items
    world.itempool += [create_item(name) for name in itempool]


item_group_classification: Dict[str, ItemClassification] = {
    "Traps": ItemClassification.trap,
    "Pickups": ItemClassification.useful,
    "Gold": ItemClassification.filler,
    "Items": ItemClassification.filler,
    "Wands": ItemClassification.useful,
    "Perks": ItemClassification.progression,
    "Repeatable Perks": ItemClassification.useful,
}

# 110000 - 110021
item_table: Dict[str, ItemData] = {
    "Bad":              ItemData(110000, "Traps"),
    "Heart":            ItemData(110001, "Pickups"),
    "Refresh":          ItemData(110002, "Pickups"),
    "Potion":           ItemData(110003, "Items"),
    "Gold (10)":        ItemData(110004, "Gold"),
    "Gold (50)":        ItemData(110005, "Gold"),
    "Gold (200)":       ItemData(110006, "Gold"),
    "Gold (1000)":      ItemData(110007, "Gold"),
    "Wand (Tier 1)":    ItemData(110008, "Wands"),
    "Wand (Tier 2)":    ItemData(110009, "Wands"),
    "Wand (Tier 3)":    ItemData(110010, "Wands"),
    "Wand (Tier 4)":    ItemData(110011, "Wands"),
    "Wand (Tier 5)":    ItemData(110012, "Wands"),
    "Wand (Tier 6)":    ItemData(110013, "Wands"),
    "Perk (Fire Immunity)":                 ItemData(110014, "Perks", 1),
    "Perk (Toxic Immunity)":                ItemData(110015, "Perks", 1),
    "Perk (Explosion Immunity)":            ItemData(110016, "Perks", 1),
    "Perk (Melee Immunity)":                ItemData(110017, "Perks", 1),
    "Perk (Electricity Immunity)":          ItemData(110018, "Perks", 1),
    "Perk (Tinker With Wands Everywhere)":  ItemData(110019, "Perks", 1),
    "Perk (All-Seeing Eye)":                ItemData(110020, "Perks", 1),
    "Perk (Extra Life)":                    ItemData(110021, "Repeatable Perks"),
}

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


filler_items = [name for name, data in item_table.items() if data.classification == ItemClassification.filler]
item_name_to_id = { name: data.code for name, data in item_table.items() }
item_name_groups = { group: set(item_names) for group, item_names in itertools.groupby(item_data, key = lambda v: v.classification) }

required_items = { name: data.required_num for name, data in item_table.items() }
