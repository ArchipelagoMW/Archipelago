from __future__ import annotations

from typing import Dict, List, NamedTuple, TYPE_CHECKING

from BaseClasses import Item, ItemClassification

from .data.pickup_info import rows as pickup_infos
from .data.item_info import item_info_collection
from .item_granting import DISAMBIG_MAX, ID_MAX, TransferCategory, pack

if TYPE_CHECKING:
    from . import CVAOSWorld


class CVAOSItem(Item):
    """Castlevania: Aria of Sorrow item instance."""

    game: str = "Castlevania - Aria of Sorrow"


class ItemData(NamedTuple):
    classification: ItemClassification
    code: int  # packed AP code (see item_granting.pack / its bit layout)


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


_MONEY_SUBTYPE = 1


def _transfer_for(pickup) -> tuple[TransferCategory, int]:
    """
    (category, id/value) for a pickup's AP code: money -> (MONEY, gold value), every other
    pickup -> (PICKUP, item_info.item_number). Raises a ValueError
    if a non-money pickup has no item_info row
    (possibly due to a name mismatch between pickup_info and item_info)
    so the gap fails loudly at load.
    """
    if pickup.subtype_num == _MONEY_SUBTYPE:
        return TransferCategory.MONEY, int(pickup.simple_name)
    info = _item_info_by_name.get(pickup.simple_name)
    if info is None:
        raise ValueError(
            f"pickup {pickup.identifier_key!r} (#{pickup.pickup_number}) has no item_info row for "
            f"name {pickup.simple_name!r}; cannot encode its AP item code")
    return TransferCategory.PICKUP, info.item_number


def _build_item_table() -> Dict[str, ItemData]:
    # TODO(maps): Castle Maps currently encode as plain item transfers (no set_flag). Once the
    # map-reveal EWRAM flag offsets are known, pack them with set_flag=1 so receiving a map
    # reveals it -- item_granting.pack supports it and resolve/grant already apply it.
    copies: Dict[tuple, int] = {}
    table: Dict[str, ItemData] = {}
    for pickup in pickup_infos:
        category, id_or_value = _transfer_for(pickup)
        if id_or_value > ID_MAX:
            raise ValueError(f"{pickup.identifier_key}: id/value {id_or_value} exceeds {ID_MAX} (12 bits)")
        key = (category, id_or_value)
        disambiguation = copies.get(key, 0)
        copies[key] = disambiguation + 1
        if disambiguation > DISAMBIG_MAX:
            raise ValueError(f"more than {DISAMBIG_MAX + 1} copies of {key}; 6-bit disambiguation overflow")
        code = pack(category, id_or_value, disambiguation=disambiguation)
        table[pickup.display_name] = ItemData(_classification_for_pickup(pickup.simple_name), code)
    return table


item_table: Dict[str, ItemData] = _build_item_table()

# Convenience map for the World class.
item_name_to_id: Dict[str, int] = {name: data.code for name, data in item_table.items()}


def create_item(world: "CVAOSWorld", name: str) -> CVAOSItem:
    data = item_table[name]
    return CVAOSItem(name, data.classification, data.code, world.player)


def create_itempool(world: "CVAOSWorld") -> List[CVAOSItem]:
    # One of each defined pickup for now; adjust counts/filters as the world logic matures.
    return [create_item(world, name) for name in item_table]
