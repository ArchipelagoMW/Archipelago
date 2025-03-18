from typing import NamedTuple, Iterable

from BaseClasses import Item, ItemClassification


# an item is something you receive

candy_box_2_base_id: int = 7665000

class CandyBox2Item(Item):
    game: str = "Candy Box 2"

class CandyBox2ItemData(NamedTuple):
    code: int | None = None
    required_amount: int | None = None
    classification: ItemClassification = ItemClassification.filler
    description: str | None = None

item_descriptions = {
    "HP Bar": ""
}

items: dict[str, CandyBox2ItemData] = {
    "Candy": CandyBox2ItemData(candy_box_2_base_id + 0, 0),
    "Lollipop": CandyBox2ItemData(candy_box_2_base_id + 1, 8, ItemClassification.skip_balancing),
    "Chocolate Bar": CandyBox2ItemData(candy_box_2_base_id + 2, 3, ItemClassification.useful),
    "HP Bar": CandyBox2ItemData(candy_box_2_base_id + 3, 1, ItemClassification.useful),
    "Time Ring": CandyBox2ItemData(candy_box_2_base_id + 4, 1, ItemClassification.useful),
    "Candy Merchant's Hat": CandyBox2ItemData(candy_box_2_base_id + 5, 1, ItemClassification.useful),
    "Leather Gloves": CandyBox2ItemData(candy_box_2_base_id + 6, 1, ItemClassification.filler),
    "Leather Boots": CandyBox2ItemData(candy_box_2_base_id + 7, 1, ItemClassification.filler),
    "Progressive World Map": CandyBox2ItemData(candy_box_2_base_id + 8, 7, ItemClassification.progression),
    "The Troll's Bludgeon": CandyBox2ItemData(candy_box_2_base_id + 9, 1, ItemClassification.useful),
    "A desert bird feather": CandyBox2ItemData(candy_box_2_base_id + 10, 1, ItemClassification.useful),
    "The Beginners' Grimoire": CandyBox2ItemData(candy_box_2_base_id + 11, 1, ItemClassification.useful),
    "The Advanced Grimoire": CandyBox2ItemData(candy_box_2_base_id + 12, 1, ItemClassification.useful),
    "The Sorceress' Cauldron": CandyBox2ItemData(candy_box_2_base_id + 13, 1, ItemClassification.useful),
    "The Sorceress' Hat": CandyBox2ItemData(candy_box_2_base_id + 14, 1, ItemClassification.useful),
    "The Octopus King Crown": CandyBox2ItemData(candy_box_2_base_id + 15, 1, ItemClassification.useful),
    "The Monkey Wizard Staff": CandyBox2ItemData(candy_box_2_base_id + 16, 1, ItemClassification.useful),
    "The Heart Plug": CandyBox2ItemData(candy_box_2_base_id + 17, 1, ItemClassification.useful),
    "The Pogo Stick": CandyBox2ItemData(candy_box_2_base_id + 18, 1, ItemClassification.useful),
    "The P Stone": CandyBox2ItemData(candy_box_2_base_id + 19, 1, ItemClassification.progression),
    "The L Stone": CandyBox2ItemData(candy_box_2_base_id + 20, 1, ItemClassification.progression),
    "The A Stone": CandyBox2ItemData(candy_box_2_base_id + 21, 1, ItemClassification.progression),
    "The Y Stone": CandyBox2ItemData(candy_box_2_base_id + 22, 1, ItemClassification.progression),
    "Wooden Sword": CandyBox2ItemData(candy_box_2_base_id + 23, 1, ItemClassification.useful),
    "Iron Axe": CandyBox2ItemData(candy_box_2_base_id + 24, 1, ItemClassification.useful),
    "Polished Silver Sword": CandyBox2ItemData(candy_box_2_base_id + 25, 1, ItemClassification.useful),
    "Lightweight Body Armour": CandyBox2ItemData(candy_box_2_base_id + 26, 1, ItemClassification.useful),
    "Scythe": CandyBox2ItemData(candy_box_2_base_id + 27, 1, ItemClassification.useful),
    "Red Enchanted Gloves": CandyBox2ItemData(candy_box_2_base_id + 28, 1, ItemClassification.useful),
    "Pink Enchanted Gloves": CandyBox2ItemData(candy_box_2_base_id + 29, 1, ItemClassification.useful),
    "Summoning Tribal Spear": CandyBox2ItemData(candy_box_2_base_id + 30, 1, ItemClassification.useful),
    "Enchanted Monkey Wizard Staff": CandyBox2ItemData(candy_box_2_base_id + 31, 1, ItemClassification.useful),
    "Enchanted Knight Body Armour": CandyBox2ItemData(candy_box_2_base_id + 32, 1, ItemClassification.useful),
    "Octopus King Crown with Jaspers": CandyBox2ItemData(candy_box_2_base_id + 33, 1, ItemClassification.useful),
    "Octopus King Crown with Obsidian": CandyBox2ItemData(candy_box_2_base_id + 34, 1, ItemClassification.useful),
    "Giant Spoon of Doom": CandyBox2ItemData(candy_box_2_base_id + 35, 1, ItemClassification.useful),
    "Tribal Spear": CandyBox2ItemData(candy_box_2_base_id + 36, 1, ItemClassification.useful),
    "Giant Spoon": CandyBox2ItemData(candy_box_2_base_id + 37, 1, ItemClassification.useful),
    "Desert Fortress Key": CandyBox2ItemData(candy_box_2_base_id + 38, 1, ItemClassification.progression),
    "Knight Body Armour": CandyBox2ItemData(candy_box_2_base_id + 39, 1, ItemClassification.useful),
    "Xinopherydon Claw": CandyBox2ItemData(candy_box_2_base_id + 40, 1, ItemClassification.useful),
    "Unicorn Horn": CandyBox2ItemData(candy_box_2_base_id + 41, 1, ItemClassification.useful),
    "Rocket Boots": CandyBox2ItemData(candy_box_2_base_id + 42, 1, ItemClassification.useful),
    "Heart Pendant": CandyBox2ItemData(candy_box_2_base_id + 43, 1, ItemClassification.useful),
    "Black Magic Grimoire": CandyBox2ItemData(candy_box_2_base_id + 44, 1, ItemClassification.useful),
    "4 Chocolate Bars": CandyBox2ItemData(candy_box_2_base_id + 45, 1, ItemClassification.skip_balancing),
    "Pitchfork": CandyBox2ItemData(candy_box_2_base_id + 46, 1, ItemClassification.useful),
    "20 Candies": CandyBox2ItemData(candy_box_2_base_id + 47, 1, ItemClassification.skip_balancing),
    "100 Candies": CandyBox2ItemData(candy_box_2_base_id + 48, 1, ItemClassification.skip_balancing),
    "500 Candies": CandyBox2ItemData(candy_box_2_base_id + 49, 1, ItemClassification.skip_balancing),
    "3 Lollipops": CandyBox2ItemData(candy_box_2_base_id + 50, 1, ItemClassification.skip_balancing),
    "3 Chocolate Bars": CandyBox2ItemData(candy_box_2_base_id + 51, 2, ItemClassification.skip_balancing),
    "Third House Key": CandyBox2ItemData(candy_box_2_base_id + 52, 1, ItemClassification.skip_balancing),
    "The Sponge": CandyBox2ItemData(candy_box_2_base_id + 53, 1, ItemClassification.useful),
    "The Shell Powder": CandyBox2ItemData(candy_box_2_base_id + 54, 1, ItemClassification.useful),
    "The Red Fin": CandyBox2ItemData(candy_box_2_base_id + 55, 1, ItemClassification.useful),
    "The Green Fin": CandyBox2ItemData(candy_box_2_base_id + 56, 1, ItemClassification.useful),
    "The Purple Fin": CandyBox2ItemData(candy_box_2_base_id + 57, 1, ItemClassification.useful),
    "Locked Candy Box": CandyBox2ItemData(candy_box_2_base_id + 58, 1, ItemClassification.progression),
}

weapons: Iterable[str] = [
    "Wooden Sword",
    "Iron Axe",
    "Polished Silver Sword",
    "The Troll's Bludgeon",
    "The Monkey Wizard Staff",
    "Scythe",
    "Summoning Tribal Spear",
    "Enchanted Monkey Wizard Staff",
    "Enchanted Knight Body Armour",
    "Giant Spoon of Doom"
]