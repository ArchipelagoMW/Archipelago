from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

from . import constants

if TYPE_CHECKING:
    from .world import TombaWorld

ITEMS = {
    constants.FURIOUS_TORNADO: {"classification": ItemClassification.progression},
    constants.CHARITY_WINGS: {"classification": ItemClassification.filler},
}

ITEM_NAME_TO_ID = {name: id for id, name in enumerate(ITEMS, constants.BASE_ID)}


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
