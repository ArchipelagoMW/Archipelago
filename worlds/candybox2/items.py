from typing import NamedTuple

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
    "Lollipop": CandyBox2ItemData(candy_box_2_base_id + 1, 7, ItemClassification.skip_balancing),
    "Chocolate Bar": CandyBox2ItemData(candy_box_2_base_id + 2, 2, ItemClassification.useful),
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
}

