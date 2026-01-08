from collections import defaultdict
from typing import Dict, Iterator
from BaseClasses import Item, ItemClassification as IC
from .config import base_id

from subversion_rando.area_rando_types import DoorPairs
from subversion_rando.item_data import Item as SvItem, Items
from subversion_rando.fillAssumed import FillAssumed


classifications: Dict[str, IC] = defaultdict(lambda: IC.progression)
classifications.update({
    Items.Refuel.name: IC.filler,
    Items.SmallAmmo.name: IC.filler,

    Items.DamageAmp.name: IC.useful,
    Items.AccelCharge.name: IC.useful,
    Items.SpaceJumpBoost.name: IC.useful,  # 1 progression set by create_items
    Items.LargeAmmo.name: IC.useful  # 10 progression set by create_items
})


class SubversionItem(Item):
    game = "Subversion"
    __slots__ = ("sv_item",)
    sv_item: SvItem

    def __init__(self, name: str, player: int) -> None:
        classification = classifications[name]
        code = name_to_id[name]
        super().__init__(name, classification, code, player)
        self.sv_item = id_to_sv_item[code]


# The order of this list must match itemnames.asm
local_id_to_sv_item: Dict[int, SvItem] = {
    0x00: Items.Energy,
    0x01: Items.Missile,
    0x02: Items.Super,
    0x03: Items.PowerBomb,
    0x04: Items.Bombs,
    0x05: Items.Charge,
    0x06: Items.Ice,
    0x07: Items.HiJump,
    0x08: Items.SpeedBooster,
    0x09: Items.Wave,
    0x0a: Items.Spazer,
    0x0b: Items.Speedball,
    0x0c: Items.Varia,
    0x0d: Items.Aqua,
    0x0e: Items.Xray,
    0x0f: Items.Plasma,
    0x10: Items.Grapple,
    0x11: Items.SpaceJump,
    0x12: Items.Screw,
    0x13: Items.Morph,
    0x14: Items.Refuel,
    0x15: Items.DamageAmp,
    0x16: Items.SmallAmmo,
    0x17: Items.LargeAmmo,
    0x18: Items.AccelCharge,
    0x19: Items.SpaceJumpBoost,
    0x1a: Items.GravityBoots,
    0x1b: Items.DarkVisor,
    0x1c: Items.MetroidSuit,
    0x1d: Items.Hypercharge
}
""" starting from 0 """

sv_item_name_to_sm_item_id = {
    Items.Refuel.name: len(local_id_to_sv_item) + 0,
    Items.Aqua.name: len(local_id_to_sv_item) + 1,
    Items.Speedball.name: len(local_id_to_sv_item) + 2,
}
"""
in `itemnames.asm` after all of the subversion items,
there are these items with subversion icons, but different (sm) names
"""

id_to_sv_item = {
    id_ + base_id: item
    for id_, item in local_id_to_sv_item.items()
}

name_to_id = {
    item.name: id_
    for id_, item in id_to_sv_item.items()
}

# This is an item that should never be in the item pool or placed in any locations.
# It's used only to hide the name of items in hints.
IMPORTANT_ITEM_NAME = "Important Item"
name_to_id[IMPORTANT_ITEM_NAME] = max(name_to_id.values()) + 1
IMPORTANT_ITEM_ID = name_to_id[IMPORTANT_ITEM_NAME]
id_to_sv_item[IMPORTANT_ITEM_ID] = Items.Refuel  # This is so unit tests don't crash when they try to create this item.
# TODO: add API in AP to hide item name in hint


def names_for_item_pool() -> Iterator[str]:
    sv_fill = FillAssumed(DoorPairs([]))
    for sv_item in sv_fill.prog_items:
        yield sv_item.name
    for sv_item in sv_fill.extra_items:
        yield sv_item.name
