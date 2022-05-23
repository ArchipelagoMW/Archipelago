from typing import cast, List
from BaseClasses import CollectionState
from zilliandomizer.logic_components.locations import Req
from zilliandomizer.randomizer import Randomizer
from zilliandomizer.logic_components.items import Item, items
from .region import ZillionLocation
from .item import ZillionItem

# TODO: unit tests for these


def cs_to_have_req(cs: CollectionState, p: int, zz_r: Randomizer) -> Req:
    return zz_r.make_ability(cs_to_zz_items(cs, p))


def set_randomizer_locs(cs: CollectionState, p: int, zz_r: Randomizer) -> Randomizer:
    for loc in cs.world.get_locations():
        if loc.player == p:
            z_loc = cast(ZillionLocation, loc)
            zz_item = cast(ZillionItem, z_loc.item).zz_item if z_loc.item else None
            zz_r.locations[z_loc.zz_loc.name].item = zz_item
    return zz_r


def cs_to_zz_items(cs: CollectionState, p: int) -> List[Item]:
    items_tr: List[Item] = []
    for item in items:
        name = item.debug_name
        count = cs.item_count(name, p)
        for _ in range(count):
            items_tr.append(item)
    return items_tr
