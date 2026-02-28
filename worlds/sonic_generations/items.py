from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

from BaseClasses import Item, ItemClassification

from . import names

if TYPE_CHECKING:
    from .world import SonicGensWorld

class ItemInfo(NamedTuple):
    id: int
    classification: ItemClassification

ITEM_NAME_TO_INFO = {
    names.Items.EGreen:     ItemInfo(1, ItemClassification.progression),
    names.Items.EPurple:    ItemInfo(2, ItemClassification.progression),
    names.Items.EBlue:      ItemInfo(3, ItemClassification.progression),
    names.Items.EYellow:    ItemInfo(4, ItemClassification.progression),
    names.Items.ERed:       ItemInfo(5, ItemClassification.progression),
    names.Items.ECyan:      ItemInfo(6, ItemClassification.progression),
    names.Items.EWhite:     ItemInfo(7, ItemClassification.progression),

    names.Items.Nothing:    ItemInfo(8, ItemClassification.filler),

    names.Items.BKGHZ:      ItemInfo(50, ItemClassification.progression),
    names.Items.BKCPZ:      ItemInfo(51, ItemClassification.progression),
    names.Items.BKSSZ:      ItemInfo(52, ItemClassification.progression),
    names.Items.BKSPH:      ItemInfo(53, ItemClassification.progression),
    names.Items.BKCTE:      ItemInfo(54, ItemClassification.progression),
    names.Items.BKSSH:      ItemInfo(55, ItemClassification.progression),
    names.Items.BKCSC:      ItemInfo(56, ItemClassification.progression),
    names.Items.BKEUC:      ItemInfo(57, ItemClassification.progression),
    names.Items.BKPLA:      ItemInfo(58, ItemClassification.progression)
}

def get_item_names_to_id() -> dict[str, int]:
    return {name: ITEM_NAME_TO_INFO[name].id for name in ITEM_NAME_TO_INFO.keys()}

class SonicGensItem(Item):
    game = names.GameName

def get_random_filler_item_name(world: SonicGensWorld) -> str:
    return names.Items.Nothing

def create_item_with_correct_classification(world: SonicGensWorld, name: str) -> SonicGensItem:
    info: ItemInfo = ITEM_NAME_TO_INFO[name]
    return SonicGensItem(name, info.classification, info.id, world.player)

def create_all_items(world: SonicGensWorld) -> None:
    itempool: list[Item] = []

    for key, value in ITEM_NAME_TO_INFO.items():
        if value.classification != ItemClassification.filler:
            itempool += [world.create_item(key)]
    
    num: int = len(world.multiworld.get_unfilled_locations(world.player)) - len(itempool)
    itempool += [world.create_filler() for _ in range(num)]

    world.multiworld.itempool += itempool
