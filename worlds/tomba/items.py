from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

from . import constants

if TYPE_CHECKING:
    from .world import TombaWorld

ITEMS = [
    {"name": constants.CHICK, "game_id": 0x00, "classification": ItemClassification.progression, "has_quantity": True},
    {"name": "Frog", "game_id": 0x01, "classification": ItemClassification.progression},
    {"name": "Lost Dwarf", "game_id": 0x02, "classification": ItemClassification.progression},
    {
        "name": constants.BANANAS,
        "game_id": 0x03,
        "classification": ItemClassification.progression,
        "has_quantity": True,
    },
    {"name": constants.FURIOUS_TORNADO, "game_id": 0x04, "classification": ItemClassification.progression},
    {"name": "100 Year Old Bell", "game_id": 0x05, "classification": ItemClassification.useful},
    {"name": "100 Year Old Key", "game_id": 0x06, "classification": ItemClassification.progression},
    {
        "name": constants.CHARITY_WINGS,
        "game_id": 0x07,
        "classification": ItemClassification.filler,
        "has_quantity": True,
    },
    {
        "name": "Bitting Plant Flower",
        "game_id": 0x08,
        "classification": ItemClassification.useful,
        "has_quantity": True,
    },
    {"name": "Healing Mushroom", "game_id": 0x09, "classification": ItemClassification.useful, "has_quantity": True},
    {"name": "Bucket", "game_id": 0x0A, "classification": ItemClassification.useful},
    {"name": "Baked Yam", "game_id": 0x0F, "classification": ItemClassification.useful},
    {"name": "Blackjack", "game_id": 0x1B, "classification": ItemClassification.useful},
    {"name": "Normal Pants", "game_id": 0x20, "classification": ItemClassification.useful},
]

ITEM_NAME_TO_ID = {details["name"]: id for id, details in enumerate(ITEMS)}
GAME_ID_TO_ITEM = {details["game_id"]: {**details} for details in ITEMS}


class TombaItem(Item):
    game = constants.GAME


def get_random_filler_item_name(world: TombaWorld) -> str:
    return constants.CHARITY_WINGS


def create_item_with_correct_classification(world: TombaWorld, name: str) -> TombaItem:
    id = ITEM_NAME_TO_ID[name]
    classification = ITEMS[id]["classification"]

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
