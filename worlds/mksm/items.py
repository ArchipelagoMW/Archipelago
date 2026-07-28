from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification
from .consts import CHARACTER_PURCHASE_AMOUNTS, HEALTH_UPGRADE_AMOUNT, BLOOD_BAR_AMOUNT, FILLER_EXP

if TYPE_CHECKING:
    from .world import MKSMWorld

ITEM_NAME_TO_ID = {
    "Long Jump": 1,
    "Fist of Ruin": 2,
    "Wall Climb": 3,
    "Wall Run": 4,
    "Wall Jump": 5,
    "Swing": 6,
    "Double Jump": 7,
    "Combo 1": 8,
    "Combo 2": 9,
    "Combo 3": 10,
    "Combo 4": 11,
    "Combo 5": 12,
    "Square special upgrade": 13,
    "Triangle special upgrade": 14,
    "Circle special upgrade": 15,
    "R2 special upgrade": 16,
    "Red Koin": 17,
    "Health upgrade": 18,
    "Blood bar": 19,
    f"{FILLER_EXP} XP": 20,
}

DEFAULT_ITEM_CLASSIFICATIONS = {
    "Long Jump": ItemClassification.progression,
    "Fist of Ruin": ItemClassification.progression,
    "Wall Climb": ItemClassification.progression,
    "Wall Run": ItemClassification.progression,
    "Wall Jump": ItemClassification.progression,
    "Swing": ItemClassification.progression,
    "Double Jump": ItemClassification.progression,
    "Red Koin": ItemClassification.progression_deprioritized_skip_balancing,
    "Blood bar": ItemClassification.progression_deprioritized_skip_balancing,
    "Combo 1": ItemClassification.filler,
    "Combo 2": ItemClassification.filler,
    "Combo 3": ItemClassification.filler,
    "Combo 4": ItemClassification.filler,
    "Combo 5": ItemClassification.filler,
    "Square special upgrade": ItemClassification.filler,
    "Triangle special upgrade": ItemClassification.filler,
    "Circle special upgrade": ItemClassification.filler,
    "R2 special upgrade": ItemClassification.filler,
    "Health upgrade": ItemClassification.filler,
    f"{FILLER_EXP} XP": ItemClassification.filler,
}


class MKSMItem(Item):
    game = "Mortal Kombat: Shaolin Monks"


def create_item_with_correct_classification(world: MKSMWorld, name: str) -> MKSMItem:
    return MKSMItem(name, DEFAULT_ITEM_CLASSIFICATIONS[name], ITEM_NAME_TO_ID[name], world.player)


def create_all_items(world: MKSMWorld) -> None:
    itempool: list[Item] = [
        world.create_item("Long Jump"),
        world.create_item("Fist of Ruin"),
        world.create_item("Wall Climb"),
        world.create_item("Wall Run"),
        world.create_item("Wall Jump"),
        world.create_item("Swing"),
        world.create_item("Double Jump"),
    ]

    amounts = CHARACTER_PURCHASE_AMOUNTS[world.options.character.value]

    itempool += [world.create_item(f"Combo {i + 1}") for i in range(amounts.combo)]
    itempool += [world.create_item("Square special upgrade") for _ in range(amounts.square)]
    itempool += [world.create_item("Triangle special upgrade") for _ in range(amounts.triangle)]
    itempool += [world.create_item("Circle special upgrade") for _ in range(amounts.circle)]
    itempool += [world.create_item("R2 special upgrade") for _ in range(amounts.r2)]

    itempool += [world.create_item("Health upgrade") for _ in range(HEALTH_UPGRADE_AMOUNT)]
    itempool += [world.create_item("Blood bar") for _ in range(BLOOD_BAR_AMOUNT)]

    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    current_count = len(itempool)

    diff = number_of_unfilled_locations - current_count
    diff = 0 if diff < 0 else diff

    red_koin_count = min(diff, 60)
    world.red_koin_amount = red_koin_count
    itempool += [world.create_item("Red Koin") for _ in range(red_koin_count)]

    new_diff = diff - red_koin_count
    new_diff = 0 if new_diff < 0 else new_diff

    itempool += [world.create_filler() for _ in range(new_diff)]

    world.multiworld.itempool += itempool
