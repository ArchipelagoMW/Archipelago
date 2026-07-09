from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

from . import constants

if TYPE_CHECKING:
    from .world import TombaWorld

ITEMS = {
    "Chick": {
        "game_id": 0x00,
        "classification": ItemClassification.progression
    },
    "Frog": {
        "game_id": 0x01,
        "classification": ItemClassification.progression
    },
    "Lost Dwarf": {
        "game_id": 0x02,
        "classification": ItemClassification.progression
    },
    "Bananas": {
        "game_id": 0x03,
        "classification": ItemClassification.progression
    },
    constants.FURIOUS_TORNADO: {
        "game_id": 0x04,
        "classification": ItemClassification.progression
    },
    "100 Year Old Bell": {
        "game_id": 0x05,
        "classification": ItemClassification.useful
    },
    "100 Year Old Key": {
        "game_id": 0x06,
        "classification": ItemClassification.progression
    },
    constants.CHARITY_WINGS: {
        "game_id": 0x07,
        "classification": ItemClassification.filler
    },
    "Blackjack": {
        "game_id": 0x1B,
        "classification": ItemClassification.useful
    },
    "Normal Pants": {
        "game_id": 0x20,
        "classification": ItemClassification.useful
    },
}

ITEM_NAME_TO_ID = {name: id for id, name in enumerate(ITEMS, constants.BASE_ID)}
GAME_ID_TO_ITEM = {
    details["game_id"]: {"name": name, **details}
    for name, details in ITEMS.items()
}

class TombaItem(Item):
    game = constants.GAME


def get_random_filler_item_name(world: TombaWorld) -> str:
    return constants.CHARITY_WINGS


def create_item_with_correct_classification(world: TombaWorld, name: str) -> TombaItem:
    classification = ITEMS[name]["classification"]

    return TombaItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


def create_all_items(world: TombaWorld) -> None:
    itempool: list[Item] = [
        world.create_item(constants.FURIOUS_TORNADO),
        world.create_item(constants.CHARITY_WINGS),
    ]

    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool
