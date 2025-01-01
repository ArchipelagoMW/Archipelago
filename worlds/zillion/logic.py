from collections import Counter
from collections.abc import Mapping

from BaseClasses import CollectionState

from zilliandomizer.logic_components.items import Item, items
from zilliandomizer.logic_components.locations import Location
from zilliandomizer.randomizer import Randomizer

from .item import ZillionItem
from .id_maps import item_name_to_id

zz_empty = items[4]

# TODO: unit tests for these


def set_randomizer_locs(cs: CollectionState, p: int, zz_r: Randomizer) -> int:
    """
    sync up zilliandomizer locations with archipelago locations

    returns a hash of the player and of the set locations with their items
    """
    from . import ZillionWorld
    z_world = cs.multiworld.worlds[p]
    assert isinstance(z_world, ZillionWorld)

    _hash = p
    for z_loc in z_world.my_locations:
        zz_name = z_loc.zz_loc.name
        zz_item = z_loc.item.zz_item \
            if isinstance(z_loc.item, ZillionItem) and z_loc.item.player == p \
            else zz_empty
        zz_r.locations[zz_name].item = zz_item
        _hash += (hash(zz_name) * (z_loc.zz_loc.req.gun + 2)) ^ hash(zz_item)
    return _hash


def item_counts(cs: CollectionState, p: int) -> tuple[tuple[str, int], ...]:
    """
    the zilliandomizer items that player p has collected

    ((item_name, count), (item_name, count), ...)
    """
    return tuple((item_name, cs.count(item_name, p)) for item_name in item_name_to_id)


_cache_miss: tuple[None, frozenset[Location]] = (None, frozenset())


class ZillionLogicCache:
    _cache: dict[int, tuple[Counter[str], frozenset[Location]]]
    """ `{ hash: (counter_from_prog_items, accessible_zz_locations) }` """
    _player: int
    _zz_r: Randomizer
    _id_to_zz_item: Mapping[int, Item]

    def __init__(self, player: int, zz_r: Randomizer, id_to_zz_item: Mapping[int, Item]) -> None:
        self._cache = {}
        self._player = player
        self._zz_r = zz_r
        self._id_to_zz_item = id_to_zz_item

    def cs_to_zz_locs(self, cs: CollectionState) -> frozenset[Location]:
        """
        given an Archipelago `CollectionState`,
        returns frozenset of accessible zilliandomizer locations
        """
        # caching this function because it would be slow
        _hash = set_randomizer_locs(cs, self._player, self._zz_r)
        counts = item_counts(cs, self._player)
        _hash += hash(counts)

        cntr, locs = self._cache.get(_hash, _cache_miss)
        if cntr == cs.prog_items[self._player]:
            # print("cache hit")
            return locs

        # print("cache miss")
        have_items: list[Item] = []
        for name, count in counts:
            have_items.extend([self._id_to_zz_item[item_name_to_id[name]]] * count)
        # have_req is the result of converting AP CollectionState to zilliandomizer collection state
        have_req = self._zz_r.make_ability(have_items)
        # print(f"{have_req=}")

        # This `get_locations` is where the core of the logic comes in.
        # It takes a zilliandomizer collection state (a set of the abilities that I have)
        # and returns list of all the zilliandomizer locations I can access with those abilities.
        tr = frozenset(self._zz_r.get_locations(have_req))

        # save result in cache
        self._cache[_hash] = (cs.prog_items[self._player].copy(), tr)

        return tr
