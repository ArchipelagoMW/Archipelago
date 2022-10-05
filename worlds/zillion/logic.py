from typing import Dict, FrozenSet, Tuple, cast, List, Counter as _Counter
from BaseClasses import CollectionState
from zilliandomizer.logic_components.locations import Location
from zilliandomizer.randomizer import Randomizer
from zilliandomizer.logic_components.items import Item, items
from .region import ZillionLocation
from .item import ZillionItem
from .id_maps import item_name_to_id

zz_empty = items[4]

# TODO: unit tests for these


def set_randomizer_locs(cs: CollectionState, p: int, zz_r: Randomizer) -> int:
    """
    sync up zilliandomizer locations with archipelago locations

    returns a hash of the player and of the set locations
    """
    # print("in logic set locs")
    _hash = p
    for loc in cs.world.get_locations():
        if loc.player == p:
            z_loc = cast(ZillionLocation, loc)
            zz_name = z_loc.zz_loc.name
            zz_item = z_loc.item.zz_item \
                if isinstance(z_loc.item, ZillionItem) and z_loc.item.player == p \
                else zz_empty
            zz_r.locations[zz_name].item = zz_item
            _hash += hash(zz_name) ^ hash(zz_item)
    return _hash


def item_counts(cs: CollectionState, p: int) -> Tuple[Tuple[str, int], ...]:
    """
    the zilliandomizer items that player p has collected

    ((item_name, count), (item_name, count), ...)
    """
    return tuple((item_name, cs.item_count(item_name, p)) for item_name in item_name_to_id)


_logic_cache: Dict[int, Tuple[_Counter[Tuple[str, int]], FrozenSet[Location]]] = {}


def cs_to_zz_locs(cs: CollectionState, p: int, zz_r: Randomizer, id_to_zz_item: Dict[int, Item]) -> FrozenSet[Location]:
    """ accessible locations from this collection state """
    # caching this function because it would be slow
    _hash = set_randomizer_locs(cs, p, zz_r)
    counts = item_counts(cs, p)
    _hash += hash(counts)

    if _hash in _logic_cache and _logic_cache[_hash][0] == cs.prog_items:
        # print("cache hit")
        return _logic_cache[_hash][1]

    # print("cache miss")
    have_items: List[Item] = []
    for name, count in counts:
        have_items.extend([id_to_zz_item[item_name_to_id[name]]] * count)
    have_req = zz_r.make_ability(have_items)
    tr = frozenset(zz_r.get_locations(have_req))

    # save result in cache
    _logic_cache[_hash] = (cs.prog_items.copy(), tr)

    return tr


def clear_cache() -> None:
    _logic_cache.clear()
