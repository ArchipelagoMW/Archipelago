from typing import Container, Dict, FrozenSet, Tuple, cast, List, Counter as _Counter
from BaseClasses import CollectionState
from zilliandomizer.logic_components.locations import Req, Location
from zilliandomizer.randomizer import Randomizer
from zilliandomizer.logic_components.items import Item, items, item_name_to_item
from .region import ZillionLocation
from .item import ZillionItem

# TODO: unit tests for these
# TODO: investigate: CaitSith2 reported unbeatable generation with 2 Zillion yamls


def cs_to_have_req(cs: CollectionState, p: int, zz_r: Randomizer) -> Req:
    """ returns what abilities I have based on collected items and options """
    return zz_r.make_ability(cs_to_zz_items(cs, p))


def set_randomizer_locs(cs: CollectionState, p: int, zz_r: Randomizer) -> int:
    """
    sync up zilliandomizer locations with archipelago locations

    returns a hash of the player and of the set locations
    """
    _hash = p
    for loc in cs.world.get_locations():
        if loc.player == p:
            z_loc = cast(ZillionLocation, loc)
            zz_name = z_loc.zz_loc.name
            zz_item = z_loc.item.zz_item \
                if isinstance(z_loc.item, ZillionItem) and z_loc.item.player == p \
                else None
            zz_r.locations[zz_name].item = zz_item
            _hash += hash(zz_name) ^ hash(zz_item)
    return _hash


def cs_to_zz_items(cs: CollectionState, p: int) -> List[Item]:
    """ return the zilliandomizer options that I've collected """
    items_tr: List[Item] = []
    for item in items:
        name = item.debug_name
        count = cs.item_count(name, p)
        for _ in range(count):
            items_tr.append(item)
    return items_tr


def item_counts(cs: CollectionState, p: int) -> Tuple[Tuple[str, int], ...]:
    return tuple((item.debug_name, cs.item_count(item.debug_name, p)) for item in items)


_logic_cache: Dict[int, Tuple[_Counter[Tuple[str, int]], FrozenSet[Location]]] = {}


def cs_to_zz_locs(cs: CollectionState, p: int, zz_r: Randomizer) -> Container[Location]:
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
        have_items.extend([item_name_to_item[name]] * count)
    have_req = zz_r.make_ability(have_items)
    tr = frozenset(zz_r.get_locations(have_req))

    # save result in cache
    _logic_cache[_hash] = (cs.prog_items.copy(), tr)

    return tr
