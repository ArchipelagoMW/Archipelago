from __future__ import annotations

from typing import Dict, List, NamedTuple, TYPE_CHECKING

from BaseClasses import Item, ItemClassification

from .data.pickup_info import rows as pickup_infos
from .data.item_info import item_info_collection

if TYPE_CHECKING:
    from . import CVAOSWorld


class CVAOSItem(Item):
    """Castlevania: Aria of Sorrow item instance."""

    game: str = "Castlevania - Aria of Sorrow"


class ItemData(NamedTuple):
    classification: ItemClassification
    code: int  # using pickup_number currently


# Grab ItemInfos by name for classification flags.
_item_info_by_name: Dict[str, object] = {info.name: info for info in item_info_collection}


def _classification_for_pickup(simple_name: str) -> ItemClassification:
    info = _item_info_by_name.get(simple_name)
    if info:
        if info.progression:
            return ItemClassification.progression
        if info.useful:
            return ItemClassification.useful
        if info.filler:
            return ItemClassification.filler
    return ItemClassification.filler


item_table: Dict[str, ItemData] = {
    pickup.identifier_key: ItemData(_classification_for_pickup(pickup.simple_name), pickup.pickup_number)
    for pickup in pickup_infos
}

# Convenience map for the World class.
item_name_to_id: Dict[str, int] = {name: data.code for name, data in item_table.items()}


def create_item(world: "CVAOSWorld", name: str) -> CVAOSItem:
    data = item_table[name]
    return CVAOSItem(name, data.classification, data.code, world.player)


def create_itempool(world: "CVAOSWorld") -> List[CVAOSItem]:
    # One of each defined pickup for now; adjust counts/filters as the world logic matures.
    return [create_item(world, name) for name in item_table]
