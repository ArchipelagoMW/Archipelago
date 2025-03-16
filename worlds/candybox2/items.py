from typing import NamedTuple

from BaseClasses import Item, ItemClassification


# an item is something you receive

candy_box_2_base_id: int = 7665000

class CandyBox2Item(Item):
    game: str = "Candy Box 2"

class CandyBox2ItemData(NamedTuple):
    code: int | None = None
    required_amount: int | None = None
    classification: ItemClassification = ItemClassification.progression
    description: str | None = None

item_descriptions = {
    "HP Bar": ""
}

items: dict[str, CandyBox2ItemData] = {
    "Candy": CandyBox2ItemData(candy_box_2_base_id + 0, 0),
    "Lollipop": CandyBox2ItemData(candy_box_2_base_id + 1, 6, ItemClassification.skip_balancing),
    "Chocolate Bar": CandyBox2ItemData(candy_box_2_base_id + 2, 1),
    "HP Bar": CandyBox2ItemData(candy_box_2_base_id + 3, 1, ItemClassification.useful),
    "Time Ring": CandyBox2ItemData(candy_box_2_base_id + 4, 1),
    "Candy Merchant's Hat": CandyBox2ItemData(candy_box_2_base_id + 5, 1),
    "Leather Gloves": CandyBox2ItemData(candy_box_2_base_id + 6, 1),
    "Leather Boots": CandyBox2ItemData(candy_box_2_base_id + 7, 1),
}

