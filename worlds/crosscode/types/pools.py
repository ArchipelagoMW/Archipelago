from collections import defaultdict
from random import Random
import itertools

from .metadata import IncludeOptions
from .locations import LocationData
from .items import ItemData, ItemPoolEntry, ProgressiveChainEntry, ProgressiveItemChain, ProgressiveItemChainMulti, ProgressiveItemChainSingle
from .world import WorldData


ItemPool = dict[ItemData, int]


class Pools:
    """A class which stores information about item and location pools.

    A location pool represents the set of locations to include in a world.

    An item pool represents a list of items and their integer weight. This
    weight can be interpreted as a quantity if the pool is meant to be always
    included (such as with the "required" pool in the CrossCode data) or as a
    probability if the pool is to be pulled from repeatedly to fill slots
    (such as with the *Filler pools in the CrossCode data).

    There are expected to be multiple instances of Pools in the Generator.py
    runtime if there are two or more CrossCode worlds therein. Instances of
    Pools are included based on different options. In CrossCode there will be
    a separate instance of Pools when quest rando is included versus when it
    is not.
    """

    options: IncludeOptions

    location_pool: set[LocationData]
    event_pool: set[LocationData]

    item_pools: dict[str, ItemPool]
    _item_pool_lists: dict[str, tuple[list[ItemData], list[int]]]

    progressive_chains: dict[str, list[ItemData]]
    item_progressive_replacements: dict[str, list[tuple[str, int]]]
    """
    Associates item names with the amount of progressive items needed to reach
    that item's entry in the progressive chain.

    Each value can store a number of entries, in case that item shows up in
    multiple progressive chains. Each entry in this list contains the item name
    and the quantity of that item.

    This currently DOES NOT handle items appearing multiple times in the same
    progressive chain.
    """

    def __init__(self, world_data: WorldData, opts: IncludeOptions):
        self.options = opts
        self.location_pool = set()
        self.event_pool = set()
        self.item_pools = {}
        self._item_pool_lists = {}
        self.progressive_chains = {}
        self.item_progressive_replacements = defaultdict(list)

        weights = {}

        for loc in world_data.pool_locations:
            if self.__should_include(loc.metadata):
                self.location_pool.add(loc)

        for ev in world_data.events_dict.values():
            if self.__should_include(ev.metadata):
                self.event_pool.add(ev)

        for name, pool in world_data.item_pools_template.items():
            counter = defaultdict(lambda: 0)
            for entry in pool:
                if self.__should_include(entry.metadata):
                    counter[entry.item] += entry.quantity

            self.item_pools[name] = counter

            weights[name] = list(itertools.accumulate(counter.values()))

        for name, pool in self.item_pools.items():
            self._item_pool_lists[name] = (list(pool.keys()), weights[name])

        for chain_name, chain in world_data.progressive_chains.items():
            item_list: list[ItemData] = []
            self.progressive_chains[chain_name] = item_list
            items = self.locate_chain(chain)
            for idx, entry in enumerate(items):
                if self.__should_include(entry.metadata):
                    item_list.append(entry.item)
                    prog_item = world_data.progressive_items[chain_name].name
                    self.item_progressive_replacements[entry.item.name].append((prog_item, idx + 1))

            self.item_pools[f"pool:{chain_name}"] = { item: 1 for item in item_list }



    def locate_chain(self, chain: ProgressiveItemChain) -> list[ProgressiveChainEntry]:
        if isinstance(chain, ProgressiveItemChainSingle):
            return chain.items

        if isinstance(chain, ProgressiveItemChainMulti):
            for subchain in chain.subchains:
                if subchain.metadata is None:
                    return subchain.chain
                if self.__should_include(subchain.metadata):
                    return subchain.chain

            return []

    def __should_include(self, metadata: IncludeOptions | None) -> bool:
        # Technically the class allows metadata to be None.
        # So we'll assign a local variable and use that instead.
        if metadata is None:
            return True

        # This is where we check the item conditions.
        # These are manually coded for now.
        # The default is to include the item.
        # Return false if at any point it is discovered we shouldn't.

        result = True

        for var in ("trade", "shop", "arena", "chest", "quest"):
            try:
                val = metadata[var]
            except KeyError:
                continue

            if val != self.options[var]:
                result = False
                break

        return result

    def pull_items_from_pool(self, name: str, rand: Random, k=1) -> list[ItemData]:
        population, weights = self._item_pool_lists[name]
        return rand.choices(population, cum_weights=weights, k=k)
