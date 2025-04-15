from collections.abc import Callable
from typing import NamedTuple, Iterable, TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from . import CandyBox2World

# an item is something you receive

candy_box_2_base_id: int = 7665000

class CandyBox2Item(Item):
    game: str = "Candy Box 2"

class CandyBox2ItemData(NamedTuple):
    code: int | None = None
    required_amount: Callable[["CandyBox2World"], int] = lambda: 0
    classification: ItemClassification = ItemClassification.filler
    description: str | None = None

item_descriptions = {
    "HP Bar": ""
}

items: dict[str, CandyBox2ItemData] = {
    "Candy": CandyBox2ItemData(candy_box_2_base_id + 0, lambda _: 0),
    "Lollipop": CandyBox2ItemData(candy_box_2_base_id + 1, lambda _: 8, ItemClassification.progression),
    "Chocolate Bar": CandyBox2ItemData(candy_box_2_base_id + 2, lambda _: 3, ItemClassification.progression),
    "HP Bar": CandyBox2ItemData(candy_box_2_base_id + 3, lambda world: hp_bar_count(world), ItemClassification.useful),
    "Time Ring": CandyBox2ItemData(candy_box_2_base_id + 4, lambda _: 1, ItemClassification.useful),
    "Candy Merchant's Hat": CandyBox2ItemData(candy_box_2_base_id + 5, lambda _: 1, ItemClassification.useful),
    "Leather Gloves": CandyBox2ItemData(candy_box_2_base_id + 6, lambda _: 1, ItemClassification.progression),
    "Leather Boots": CandyBox2ItemData(candy_box_2_base_id + 7, lambda _: 1, ItemClassification.progression),
    "Progressive World Map": CandyBox2ItemData(candy_box_2_base_id + 8, lambda _: 7, ItemClassification.progression),
    "Troll's Bludgeon": CandyBox2ItemData(candy_box_2_base_id + 9, lambda world: weapon_item_count(world, 9), ItemClassification.progression),
    "Desert bird feather": CandyBox2ItemData(candy_box_2_base_id + 10, lambda _: 1, ItemClassification.progression),
    "Beginners' Grimoire": CandyBox2ItemData(candy_box_2_base_id + 11, lambda _: 1, ItemClassification.progression),
    "Advanced Grimoire": CandyBox2ItemData(candy_box_2_base_id + 12, lambda _: 1, ItemClassification.progression),
    "Sorceress' Cauldron": CandyBox2ItemData(candy_box_2_base_id + 13, lambda _: 1, ItemClassification.progression),
    "Sorceress' Hat": CandyBox2ItemData(candy_box_2_base_id + 14, lambda _: 1, ItemClassification.useful),
    "Octopus King Crown": CandyBox2ItemData(candy_box_2_base_id + 15, lambda _: 1, ItemClassification.progression),
    "Monkey Wizard Staff": CandyBox2ItemData(candy_box_2_base_id + 16, lambda world: weapon_item_count(world, 16), ItemClassification.progression),
    "Heart Plug": CandyBox2ItemData(candy_box_2_base_id + 17, lambda _: 1, ItemClassification.progression),
    "Pogo Stick": CandyBox2ItemData(candy_box_2_base_id + 18, lambda _: 1, ItemClassification.progression),
    "P Stone": CandyBox2ItemData(candy_box_2_base_id + 19, lambda _: 1, ItemClassification.progression | ItemClassification.useful),
    "L Stone": CandyBox2ItemData(candy_box_2_base_id + 20, lambda _: 1, ItemClassification.progression | ItemClassification.useful),
    "A Stone": CandyBox2ItemData(candy_box_2_base_id + 21, lambda _: 1, ItemClassification.progression | ItemClassification.useful),
    "Y Stone": CandyBox2ItemData(candy_box_2_base_id + 22, lambda _: 1, ItemClassification.progression | ItemClassification.useful),
    "Wooden Sword": CandyBox2ItemData(candy_box_2_base_id + 23, lambda world: weapon_item_count(world, 23), ItemClassification.progression),
    "Iron Axe": CandyBox2ItemData(candy_box_2_base_id + 24, lambda world: weapon_item_count(world, 24), ItemClassification.progression),
    "Polished Silver Sword": CandyBox2ItemData(candy_box_2_base_id + 25, lambda world: weapon_item_count(world, 25), ItemClassification.progression),
    "Lightweight Body Armour": CandyBox2ItemData(candy_box_2_base_id + 26, lambda _: 1, ItemClassification.progression),
    "Scythe": CandyBox2ItemData(candy_box_2_base_id + 27, lambda world: weapon_item_count(world, 27), ItemClassification.progression),
    "Red Enchanted Gloves": CandyBox2ItemData(candy_box_2_base_id + 28, lambda _: 1, ItemClassification.progression),
    "Pink Enchanted Gloves": CandyBox2ItemData(candy_box_2_base_id + 29, lambda _: 1, ItemClassification.progression),
    "Summoning Tribal Spear": CandyBox2ItemData(candy_box_2_base_id + 30, lambda world: weapon_item_count(world, 30), ItemClassification.progression),
    "Enchanted Monkey Wizard Staff": CandyBox2ItemData(candy_box_2_base_id + 31, lambda world: weapon_item_count(world, 31), ItemClassification.progression),
    "Enchanted Knight Body Armour": CandyBox2ItemData(candy_box_2_base_id + 32, lambda _: 1, ItemClassification.progression),
    "Octopus King Crown with Jaspers": CandyBox2ItemData(candy_box_2_base_id + 33, lambda _: 1, ItemClassification.progression),
    "Octopus King Crown with Obsidian": CandyBox2ItemData(candy_box_2_base_id + 34, lambda _: 1, ItemClassification.progression),
    "Giant Spoon of Doom": CandyBox2ItemData(candy_box_2_base_id + 35, lambda world: weapon_item_count(world, 35), ItemClassification.progression),
    "Tribal Spear": CandyBox2ItemData(candy_box_2_base_id + 36, lambda world: weapon_item_count(world, 36), ItemClassification.progression),
    "Giant Spoon": CandyBox2ItemData(candy_box_2_base_id + 37, lambda world: weapon_item_count(world, 37), ItemClassification.progression),
    "Desert Fortress Key": CandyBox2ItemData(candy_box_2_base_id + 38, lambda _: 1, ItemClassification.progression),
    "Knight Body Armour": CandyBox2ItemData(candy_box_2_base_id + 39, lambda _: 1, ItemClassification.progression),
    "Xinopherydon Claw": CandyBox2ItemData(candy_box_2_base_id + 40, lambda _: 1, ItemClassification.progression),
    "Unicorn Horn": CandyBox2ItemData(candy_box_2_base_id + 41, lambda _: 1, ItemClassification.progression),
    "Rocket Boots": CandyBox2ItemData(candy_box_2_base_id + 42, lambda _: 1, ItemClassification.progression),
    "Heart Pendant": CandyBox2ItemData(candy_box_2_base_id + 43, lambda _: 1, ItemClassification.progression),
    "Black Magic Grimoire": CandyBox2ItemData(candy_box_2_base_id + 44, lambda _: 1, ItemClassification.progression),
    "4 Chocolate Bars": CandyBox2ItemData(candy_box_2_base_id + 45, lambda _: 1, ItemClassification.progression),
    "Pitchfork": CandyBox2ItemData(candy_box_2_base_id + 46, lambda _: 1, ItemClassification.progression),
    "20 Candies": CandyBox2ItemData(candy_box_2_base_id + 47, lambda _: 1),
    "100 Candies": CandyBox2ItemData(candy_box_2_base_id + 48, lambda _: 1),
    "500 Candies": CandyBox2ItemData(candy_box_2_base_id + 49, lambda _: 1),
    "3 Lollipops": CandyBox2ItemData(candy_box_2_base_id + 50, lambda _: 1, ItemClassification.progression),
    "3 Chocolate Bars": CandyBox2ItemData(candy_box_2_base_id + 51, lambda _: 2, ItemClassification.progression),
    "Third House Key": CandyBox2ItemData(candy_box_2_base_id + 52, lambda _: 1),
    "Sponge": CandyBox2ItemData(candy_box_2_base_id + 53, lambda _: 1, ItemClassification.progression),
    "Shell Powder": CandyBox2ItemData(candy_box_2_base_id + 54, lambda _: 1, ItemClassification.progression),
    "Red Fin": CandyBox2ItemData(candy_box_2_base_id + 55, lambda _: 1, ItemClassification.useful),
    "Green Fin": CandyBox2ItemData(candy_box_2_base_id + 56, lambda _: 1, ItemClassification.progression),
    "Purple Fin": CandyBox2ItemData(candy_box_2_base_id + 57, lambda _: 1, ItemClassification.progression),
    "Locked Candy Box": CandyBox2ItemData(candy_box_2_base_id + 58, lambda _: 1, ItemClassification.progression | ItemClassification.useful),
    "Boots of Introspection": CandyBox2ItemData(candy_box_2_base_id + 59, lambda _: 1, ItemClassification.progression),
    "Pain au Chocolat": CandyBox2ItemData(candy_box_2_base_id + 60, lambda _: 5, ItemClassification.useful),
    "Nothing (Weapon)": CandyBox2ItemData(candy_box_2_base_id + 61, lambda world: weapon_item_count(world, 61), ItemClassification.progression),
    "Progressive Weapon": CandyBox2ItemData(candy_box_2_base_id + 62, lambda world: progressive_weapon_count(world), ItemClassification.progression),
}

def weapon_item_count(world: "CandyBox2World", weapon: int):
    if world.starting_weapon == weapon:
        # We start with this weapon, so none of these are required
        return 0

    if world.starting_weapon == -1:
        # We are using Progressive Weapons, so no weapons will be added to the pool
        return 0

    return 1

def progressive_weapon_count(world: "CandyBox2World"):
    if world.starting_weapon == -1:
        return 11

    # Progressive Weapons are disabled
    return 0

def hp_bar_count(world: "CandyBox2World"):
    if world.options.randomise_hp_bar:
        return 1

    return 0