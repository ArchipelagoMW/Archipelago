import abc
import collections
import itertools
import logging
import typing
from collections import Counter, deque

from BaseClasses import CollectionState, Item, Location, LocationProgressType, MultiWorld, PlandoItemBlock
from Options import Accessibility

from worlds.AutoWorld import call_all
from worlds.generic.Rules import add_item_rule


class FillError(RuntimeError):
    def __init__(self, *args: typing.Union[str, typing.Any], **kwargs) -> None:
        if "multiworld" in kwargs and isinstance(args[0], str):
            placements = (args[0] + f"\nAll Placements:\n" +
                          f"{[(loc, loc.item) for loc in kwargs['multiworld'].get_filled_locations()]}")
            args = (placements, *args[1:])
        super().__init__(*args)


def _log_fill_progress(name: str, placed: int, total_items: int) -> None:
    logging.info(f"Current fill step ({name}) at {placed}/{total_items} items placed.")


def sweep_from_pool(base_state: CollectionState, itempool: typing.Sequence[Item] = tuple(),
                    locations: typing.Optional[typing.List[Location]] = None) -> CollectionState:
    new_state = base_state.copy()
    for item in itempool:
        new_state.collect(item, True)
    new_state.sweep_for_advancements(locations=locations)
    return new_state


class _RestrictiveFillBatcher:
    """
    Batcher for item placements in fill_restrictive.

    Breaks up the item_pool into batches of placements at a time.

    The batcher reduces CollectionState sweeping costs by each batch creating two extra CollectionStates:
    - A 'batch base state' that contains only the inventory of items which have yet to be placed and are not being
      placed as part of the current batch, and reachable items that were reachable before fill_restrictive was called.
      This assumes that copying the batch's base state is more performant than copying the `base_state` argument of the
      fill_restrictive call and collecting the items into that copy of `base_state`.
    - A 'partial exploration state' that starts from the 'base state' and explores filled locations, collecting all
      reachable items.

    Creating a maximum exploration state to determine where items can be placed is done by sweeping for advancements
    from the batch's partial exploration state, this saves a lot of work compared to sweeping for advancements from the
    `base_state` argument of the `fill_restrictive` call.

    Creating a partial exploration state is a cost that typically occurs once per batch (may occur multiple times due to
    some swaps). If batches are too small then the extra cost of creating the partial exploration state can outweigh the
    savings of sweeping from the partial exploration state rather than from the `base_state` of the `fill_restrictive`
    call.

    Swap states can also be created from the partial exploration state, but only if the partial exploration state has
    not collected the item from the swap location. If the partial exploration state has collected the item from the swap
    location, then the swap state will have to be swept from the base state instead.

    When a swap displaces an item that the partial exploration state had collected, the partial exploration state must
    be destroyed in some cases. For this reason, the partial exploration state is created lazily and is only re-created
    when needed.

    :param base_state: The base_state passed as an argument to the fill_restrictive call. When there are lots of items
        already placed, this state should have already swept for advancements to collect every reachable advancement
        item.
    :param reachable_items: Items remaining to place, per-player. Because fill uses a reverse-fill algorithm, these
        items are always considered reachable until they are removed and placed.
    :param item_pool: The entire item pool of items to place. Items are removed from it when placed.
    :param one_item_per_player: True to place one item per player simultaneously, False to place one item at a time.
        When True, this significantly increases fill performance at the cost of introducing a small bias towards
        placing items in earlier locations. This bias occurs because items can, usually, only be placed at locations
        that are reachable without themselves, but when multiple items are placed simultaneously the reachable
        locations will be reduced to locations reachable without *any* of the items that are being placed
        simultaneously.
    """

    # Adjust these ClassVars to adjust batch sizes, as needed, when external changes to generation performance are made.

    _MIN_BATCH_ITEMS_PER_PLAYER: typing.ClassVar[int] = 5
    """
    Pick no fewer than this many items per player for each batch, unless that player does not have enough items
    remaining. This is a magic number and will typically be used for most batches.
    """
    _MIN_TOTAL_ITEMS_PER_BATCH: typing.ClassVar[int] = 40
    """
    Try to pick no fewer than this many items total for each batch. If a player does not have enough items remaining to
    fully filly out a batch, then the total number of items in a batch can end up lower than this value.
    With a low number of players, try to keep the total number of items in the batch from being too small, to prevent
    fills with few players from creating lots of very small batches.
    """
    _MAX_PERCENT_OF_LARGEST_STARTING_POOL_TO_PLACE: typing.ClassVar[float] = 0.02  # 2%
    """
    When players have items pools with different sizes, the percentage of remaining items to place gradually approaches
    being 100% the player with the largest item pool. While this happens, gradually increase the number of items in each
    batch until the last player with items remaining places this percentage of their starting item pool in each batch.
    """

    class _RestrictiveFillBatch(abc.ABC):
        """
        Base class for a batch of items to fill in _RestrictiveFillBatcher.

        :param batch_base_state: Base state for the batch. It must have collected all items that will be placed in
            future batches and must not have explored any locations besides those in the base_state at the start of
            fill_restrictive.
        :param batch_empty_spaces: The number of empty spaces for items for each player in the batch. If the size of
            the batch if 5 items per player and one player only had 3 items remaining, they would have 2 empty
            spaces in the batch.
            When swapping items out of already filled locations, the swapped out item can be added into the current
            batch if there is space for it.
        :param batch_item_pool: All items to be placed in this batch. Items are removed from it when picked to be
            placed.
        :param item_pool: All items remaining to be placed. Items are removed from it when picked to be placed. The
            items in this list must also be present in the deques in `reachable_items`.
        :param batched_placements_remaining: The maximum number of placements the batch can make before being
            exhausted.
        :param reachable_items: All items remaining to be placed, by player. The items in the deques in this dict
            must also be present in `item_pool`.
        """
        batch_base_state: CollectionState
        batch_empty_spaces: dict[int, int]
        batch_item_pool: list[Item]
        reachable_items: dict[int, deque[Item]]
        batched_placements_remaining: int
        item_pool: list[Item]

        # An exploration state containing the items reachable starting from `batch_base_state`.
        # Maximum exploration states and some swap states will be swept from `_partial_exploration_state`.
        # Swaps may cause the partial exploration state to become invalid, which the batch accounts for when sweeping
        # new states from it, but the partial exploration state would otherwise be invalid to use in isolation, so it is
        # not exposed as a public attribute.
        _partial_exploration_state: CollectionState | None

        # When an item is swapped from an existing placement, that _partial_exploration_state has already collected
        # from, into the current batch, the _partial_exploration_state must be destroyed and re-created once it is time
        # to place the swapped item.
        # The set tracks the unique object identifiers of swapped items because Item implements __eq__, so a set[Item]
        # would not be usable here.
        # The list tracks the Item instances, whose unique object identifiers must be in the set.
        _deferred_swap_item_ids: set[int]
        _deferred_swap_items: list[Item]

        def __init__(self,
                     batch_base_state: CollectionState,
                     batch_empty_spaces: dict[int, int],
                     batch_item_pool: list[Item],
                     item_pool: list[Item],
                     batched_placements_remaining: int,
                     reachable_items: dict[int, deque[Item]]):
            self.batch_base_state = batch_base_state
            self.batch_empty_spaces = batch_empty_spaces
            self.batch_item_pool = batch_item_pool
            self.item_pool = item_pool
            self.batched_placements_remaining = batched_placements_remaining
            self.reachable_items = reachable_items

            self._partial_exploration_state = None

            self._deferred_swap_item_ids = set()
            self._deferred_swap_items = []

        @abc.abstractmethod
        def _pop_items_to_place(self) -> list[Item]:
            """
            Get and remove items to place from `self.reachable_items`. `self.batched_placements_remaining > 0` must be
            checked before calling this and `self.batched_placements_remaining` must be reduced by 1 afterward.

            :return: A list of items to place, or an empty list if the batch is exhausted and a new batch should be
                created.
            """
            ...

        def _update_pools_for_items_to_place(self, items_to_place: list[Item]) -> None:
            """
            After getting items to place, update the item pools.

            :param items_to_place: Items that have been removed from the batch, and are going to be placed.
            """
            batch_item_pool = self.batch_item_pool
            item_pool = self.item_pool
            for item in items_to_place:
                for p, batch_pool_item in enumerate(batch_item_pool):
                    if batch_pool_item is item:
                        del batch_item_pool[p]
                        break
                # The items added into `reachable_items` are placed starting from the end of each deque in
                # `reachable_items`, so the items being placed are more likely to found towards the end of `item_pool`.
                for p, pool_item in enumerate(reversed(item_pool), start=1):
                    if pool_item is item:
                        del item_pool[-p]
                        break

        def pop_items_to_place(self) -> list[Item]:
            """
            Get and remove items to place from this batch.

            :return: A list of items to place, or an empty list if the batch is exhausted.
            """
            batched_placements_remaining = self.batched_placements_remaining
            if batched_placements_remaining <= 0:
                return []
            self.batched_placements_remaining = batched_placements_remaining - 1
            items_to_place = self._pop_items_to_place()

            deferred_swap_item_ids = self._deferred_swap_item_ids
            if deferred_swap_item_ids and not deferred_swap_item_ids.isdisjoint(map(id, items_to_place)):
                assert self._partial_exploration_state is not None
                # One of the items being placed was swapped into the current batch, but was already collected by the
                # partial exploration state. It is time to place that item now, so the partial exploration state is
                # invalid and will need to be re-created.
                self._partial_exploration_state = None

                # Any deferred swap items that are not being placed will need to be added back into the batch item pool.
                # The deferred swap items that *are* being placed do not need to be added back into the batch item pool,
                # but it is simpler to add all the items and then remove the ones being placed because determining which
                # items do not need to be added needs to be done by comparing by identity.
                for item in self._deferred_swap_items:
                    self.batch_item_pool.append(item)

                # Clear the list of deferred swap items and the set of their item IDs.
                self._deferred_swap_items.clear()
                deferred_swap_item_ids.clear()

            self._update_pools_for_items_to_place(items_to_place)
            return items_to_place

        def get_maximum_exploration_state(self, explore_locations: list[Location] | None, unplaced_items: list[Item]
                                          ) -> CollectionState:
            """
            Get the maximum exploration state for the currently reachable items.

            An item is considered reachable if it matches any one of the following:
            A. It is in `self.item_pool` and is not being placed in this batch. `self.batch_base_state` collected these
               items in advance because they do not change within a batch.
            B. It is in both `self.item_pool` and `self.batch_item_pool` (the items in batch_item_pool should always be
               present in item_pool), so it is an item that is going to be placed as part of this batch, but later on.
            C. It is in `unplaced_items`, so could not be placed at any location. These items must be included because
               fill_restrictive allows for partial fills and retries depending on its arguments.
            D. It is at a location in `explore_locations` that is reachable with all items in A-D.

            Items already placed at reachable locations, items not being placed in this batch, items yet to be removed
            from this batch in order to be placed, and items that could not be placed at any location are all considered
            reachable.

            :param explore_locations: The locations to explore for reachable items. Defaults to all filled locations
                when None.
            :param unplaced_items: All items that could not be placed at any location.
            :return: A CollectionState that has collected all reachable advancement items.
            """
            partial_exploration_state = self._partial_exploration_state

            # Create the initial partial exploration state or recreate it if it was destroyed by a swap.
            if partial_exploration_state is None:
                # `locations=None` defaults to `multiworld.get_filled_locations()`, so only get it once for both the
                # batch's partial exploration state and the maximum exploration state.
                if explore_locations is None:
                    explore_locations = self.batch_base_state.multiworld.get_filled_locations()
                # batch_base_state has already collected all items that still need to be placed, but are not being
                # placed in this batch (A. items).
                # The sweep to create `partial_exploration_state` collects many additional reachable items (some D.
                # items).
                partial_exploration_state = sweep_from_pool(self.batch_base_state, locations=explore_locations)
                self._partial_exploration_state = partial_exploration_state

            # Collect items in this batch that have yet to be removed in order to be placed (B. items), and collect all
            # items that could not be placed at any location (C. items), and then sweep to collect all remaining
            # reachable items (the remaining D. items).
            maximum_exploration_state = sweep_from_pool(
                partial_exploration_state, self.batch_item_pool + unplaced_items, explore_locations)

            return maximum_exploration_state

        def _add_swapped_item_into_batch(self, displaced_item: Item, swap_location: Location) -> None:
            """
            Add an item displaced by a swap into the current batch.
            `self.batch_empty_spaces[displaced_item.player] > 0` must be True.

            :param displaced_item: The previously placed item that the swap displaced.
            :param swap_location: The location at which displaced_item was displaced from, and at which the item being
                placed was placed at.
            """
            assert self.batch_empty_spaces[displaced_item.player] > 0
            self.batch_empty_spaces[displaced_item.player] -= 1
            partial_exploration_state = self._partial_exploration_state
            if partial_exploration_state is not None and swap_location in partial_exploration_state.advancements:
                # The partial exploration state exists and has already collected `displaced_item`.
                # `displaced_item` should be added into `self.batch_item_pool`, but doing so would mean that a maximum
                # exploration state or swap state swept from the partial exploration state would have collected
                # `displaced_item` twice, which would be incorrect.
                # Instead of adding `displaced_item` into `self.batch_item_pool` immediately and re-creating the partial
                # exploration state, adding `displaced_item` into `self.batch_item_pool` is deferred until it is time to
                # place `displaced_item`. Only then does the partial exploration state need to be re-created. This
                # reduces how often the partial exploration state needs to be re-created, increasing performance.
                assert id(displaced_item) not in self._deferred_swap_item_ids, \
                    (f"Displaced item {displaced_item} has already been swapped into the batch. This should never"
                     f" happen because the set of displaced item IDs should be cleared whenever it is time to place one"
                     f" of the displaced items. If this does happen, it is more likely that a world submitted the same"
                     f" Item instance to the item pool multiple times instead of creating multiple Item instances.")
                # Multiple items can be displaced into the current batch, and the items need to be compared by identity,
                # so a set of their unique object IDs is used to track them.
                self._deferred_swap_item_ids.add(id(displaced_item))
                self._deferred_swap_items.append(displaced_item)

                # If a location has already been checked by a state, the state will ignore that location in further
                # sweeps, so `swap_location` needs to be removed so that sweeping will check the location again.
                partial_exploration_state.advancements.remove(swap_location)
                # Also remove it from locations_checked for completeness.
                partial_exploration_state.locations_checked.remove(swap_location)
            else:
                # If the partial exploration state does not currently exist, or has not collected the displaced item,
                # the displaced item can simply be added into the batch's item pool.
                self.batch_item_pool.append(displaced_item)

        def _add_swapped_item_into_future_batch(self, displaced_item: Item, item_to_place: Item,
                                                swap_location: Location) -> None:
            """
            Add an item displaced by a swap into a future batch.

            :param displaced_item: The previously placed item that the swap displaced.
            :param item_to_place: The item that was placed into the swap location.
            :param swap_location: The location at which displaced_item was displaced from and item_to_place was placed
                at.
            """
            # A batch's base state collects all items which are yet to be placed and which are not going to be placed as
            # part of the batch. The displaced item matches these criteria, so collect the item.
            self.batch_base_state.collect(displaced_item, True)
            # A batch's partial exploration state is swept from its batch's base state, so it needs to collect the item
            # too, but only if it had not already collected the item.
            partial_exploration_state = self._partial_exploration_state
            # The batch's partial exploration state may have been destroyed by a previous `_add_swapped_item_into_batch`
            # swap, in which case, it will not exist.
            if partial_exploration_state is not None:
                if swap_location not in partial_exploration_state.advancements:
                    # The partial exploration state had not already collected the un-placed item by sweeping, so collect
                    # the item.
                    partial_exploration_state.collect(displaced_item, True)
                else:
                    # The partial exploration state had already collected the displaced item from `spot_to_fill`.
                    # Rather than destroying the partial exploration state, it can be adjusted.
                    # Collect the item being placed if `spot_to_fill` is still reachable.
                    if swap_location.can_reach(partial_exploration_state):
                        # This is slightly faster than removing `spot_to_fill` from the state's collected advancement
                        # locations and requiring future maximum exploration states sweep to pick up `item_to_place`
                        # from `swap_location`.
                        partial_exploration_state.collect(item_to_place, True)
                    else:
                        # In rare cases, `spot_to_fill` was only reachable because of the item that was placed at it,
                        # which can happen with some self-locking item implementations.
                        # Future sweeps will have to retry `spot_to_fill`, so remove it from the state's set of
                        # collected advancement locations.
                        partial_exploration_state.advancements.remove(swap_location)
                        # Also remove the location from locations_checked for completeness.
                        partial_exploration_state.locations_checked.remove(swap_location)

        def update_for_swap(self, displaced_item: Item, item_to_place: Item, swap_location: Location) -> None:
            """
            Update the batch for the result of a successful swap.

            :param displaced_item: The item that was previously placed at swap_location and has been displaced by the
                swap.
            :param item_to_place: The item that has been placed at swap_location.
            :param swap_location: The location where the two items have been swapped.
            """
            # Determine if the displaced item can be added to the current batch.
            empty_spaces_for_items = self.batch_empty_spaces[displaced_item.player]
            if empty_spaces_for_items > 0:
                # There are some empty spaces for items in this batch for this player, so add the item into this batch.
                self._add_swapped_item_into_batch(displaced_item, swap_location)
            else:
                # There are no empty spaces in this batch for this player, so the item will need to be placed in a
                # different batch.
                self._add_swapped_item_into_future_batch(displaced_item, item_to_place, swap_location)

        def get_swap_state(self, displaced_item: Item, location: Location, explore_locations: list[Location] | None,
                           unsafe: bool) -> CollectionState:
            """
            Get the maximum exploration state for a potential swap.

            :param displaced_item: The item displaced from `location`.
            :param location: The location of the swap attempt.
            :param explore_locations: The locations the swap state should sweep. `None` will sweep all filled locations.
            :param unsafe: Assume it will be possible to collect `displaced_item` before the item that is being placed,
                by continuing to swap.
            :return: A fully swept CollectionState for the swap attempt.
            """
            # Use the batch's partial exploration state as the base state if it has not explored the location of the
            # swap attempt. This reduces sweeping costs.
            partial_exploration_state = self._partial_exploration_state
            if partial_exploration_state is not None and location not in partial_exploration_state.advancements:
                swap_base_state = partial_exploration_state
                deferred_swap_items_to_collect = None
            else:
                # Unfortunately, the partial exploration state has explored the location, so the swap state will have to
                # be swept from the batch's base state instead, which has collected fewer items, so will take longer to
                # sweep from.
                swap_base_state = self.batch_base_state
                # The base state won't have collected any deferred swap items, so those will also need to be collected.
                if self._deferred_swap_items:
                    deferred_swap_items_to_collect = self._deferred_swap_items
                else:
                    deferred_swap_items_to_collect = None

            if unsafe:
                # Assume we can somehow collect `displaced_item` before the item that is being placed, by continuing to
                # swap.
                if deferred_swap_items_to_collect is not None:
                    items_to_collect = self.batch_item_pool + deferred_swap_items_to_collect
                    items_to_collect.append(displaced_item)
                else:
                    items_to_collect = self.batch_item_pool + [displaced_item]
            else:
                if deferred_swap_items_to_collect is not None:
                    items_to_collect = self.batch_item_pool + deferred_swap_items_to_collect
                else:
                    items_to_collect = self.batch_item_pool

            return sweep_from_pool(swap_base_state, items_to_collect, explore_locations)

    class _RestrictiveFillBatchOneItemPerPlayer(_RestrictiveFillBatch):
        """
        Batch that places one item per player at a time.

        This is less accurate because when placing an item for a player, the items belonging to other players that are
        also going to be placed won't be included when determining if a location to place at is reachable. This results
        in a bias towards earlier locations.

        The tradeoff for reduced accuracy is that placing one item per player is significantly faster than placing one
        item at a time when there are multiple players with items remaining to be placed.
        """

        def _pop_items_to_place(self) -> list[Item]:
            # Pop one item per player that has items remaining.
            # The batch is carefully constructed such that `self.batched_placements_remaining` will reach zero before
            # attempting to pop an item from `self.reachable_items` that is not in `self.batch_item_pool`.
            return [items.pop() for items in self.reachable_items.values() if items]

    class _RestrictiveFillBatchOneItemAtATime(_RestrictiveFillBatch):
        """
        A batch that places one item at a time.

        This improves placement accuracy, at the cost of performance.

        :param batch_base_state: See _RestrictiveFillBatch
        :param batch_empty_spaces: See _RestrictiveFillBatch
        :param batch_item_pool: See _RestrictiveFillBatch
        :param item_pool: See _RestrictiveFillBatch
        :param batched_placements_remaining: See _RestrictiveFillBatch
        :param reachable_items: See _RestrictiveFillBatch
        :param items_per_player_in_batch: The number of items, per player, remaining in the batch.
        :param next_player_override: When set, specifies which player the next item to place will belong to, instead of
            picking randomly.
            This should be set when the previous batch attempted to place an item belonging to a player that still has
            items remaining to be placed, but had no items remaining in the batch.
        """

        next_player_override: int | None
        items_per_player_in_batch: dict[int, int]

        def __init__(self,
                     batch_base_state: CollectionState,
                     batch_empty_spaces: dict[int, int],
                     batch_item_pool: list[Item],
                     item_pool: list[Item],
                     batched_placements_remaining: int,
                     reachable_items: dict[int, deque[Item]],
                     items_per_player_in_batch: dict[int, int],
                     next_player_override: int | None):
            super().__init__(batch_base_state, batch_empty_spaces, batch_item_pool, item_pool,
                             batched_placements_remaining, reachable_items)
            self.items_per_player_in_batch = items_per_player_in_batch
            self.next_player_override = next_player_override

        def _pop_items_to_place(self) -> list[Item]:
            if self.next_player_override is None:
                # Randomly pick the next player that will have an item placed.
                multiworld = self.batch_base_state.multiworld
                # Only pick from players with items remaining to be placed, including players with no items remaining in
                # this batch.
                player_choices = [player for player, items in self.reachable_items.items() if items]
                next_player = multiworld.random.choice(player_choices)
                player_remaining_items_in_batch = self.items_per_player_in_batch[next_player]

                # Check that the picked player still has items remaining in this batch.
                if player_remaining_items_in_batch <= 0:
                    assert player_remaining_items_in_batch == 0, ("The count of remaining items should never be"
                                                                  " negative.")
                    # This player still has items to place, but their items in the batch have been exhausted.
                    # A new batch needs to be built. This prevents unfairness in picked items at the boundary between
                    # two batches.
                    self.batched_placements_remaining = 0
                    # The current batch is passed as an argument to create the next batch, where this override will be
                    # read to force the next batch to start by picking an item belonging to this player.
                    self.next_player_override = next_player
                    return []
            else:
                # The override being set means that a new batch was started by trying to pick an item belonging to a
                # player that had run out of items in the previous batch, but still has items remaining to be placed.
                next_player = self.next_player_override
                # Clear the override.
                self.next_player_override = None
                player_remaining_items_in_batch = self.items_per_player_in_batch[next_player]
                assert player_remaining_items_in_batch > 0, "The override player should always have items remaining."
            # Pop an item for the chosen player and reduce the count of their remaining items in this batch.
            items_to_place = [self.reachable_items[next_player].pop()]
            self.items_per_player_in_batch[next_player] = player_remaining_items_in_batch - 1

            return items_to_place

        def _add_swapped_item_into_batch(self, placed_item: Item, swap_location: Location) -> None:
            super()._add_swapped_item_into_batch(placed_item, swap_location)
            # Update the count of items remaining in the batch for this player.
            self.items_per_player_in_batch[placed_item.player] += 1
            # When placing one item at a time, the number of batched placements remaining is equal to the total number
            # of items in the batch to place.
            self.batched_placements_remaining += 1

    # Protected attributes for each of the __init__ parameters.
    _base_state: CollectionState
    _reachable_items: dict[int, deque[Item]]
    _item_pool: list[Item]
    _one_item_per_player: bool

    # The maximum batch size to be reached once only the player with the largest number of items has items remaining to
    # be placed.
    _max_one_item_per_player_batch_size: float

    # The minimum batch size for this batcher, typically equal to MIN_BATCH_SIZE.
    _min_batch_size: int

    # The current batch of the batcher, or `None` when there are no more items to place.
    _current_batch: _RestrictiveFillBatch | None

    def __init__(self,
                 base_state: CollectionState,
                 reachable_items: dict[int, deque[Item]],
                 item_pool: list[Item],
                 one_item_per_player: bool):
        self._base_state = base_state
        self._reachable_items = reachable_items
        self._item_pool = item_pool
        self._one_item_per_player = one_item_per_player
        # With a low number of players, adjust the minimum items to take per player so that there is at least
        # MIN_TOTAL_ITEMS_PER_BATCH total items in the batch. Some players could have fewer items remaining  assuming each player has enough items remaining to fully
        # fill out the batch.
        num_players = len(reachable_items)
        if num_players > 0 and self._MIN_BATCH_ITEMS_PER_PLAYER * num_players < self._MIN_TOTAL_ITEMS_PER_BATCH:
            self._min_batch_size = self._MIN_TOTAL_ITEMS_PER_BATCH // num_players
        else:
            self._min_batch_size = self._MIN_BATCH_ITEMS_PER_PLAYER

        # Gradually increase the number of items placed in each batch until only the player with the largest item pool
        # has items remaining, at which point, place a percentage of their original item pool in each batch. Most fills
        # won't go above `min_batch_size`, so this is mostly to account for progression fill with outlier worlds with
        # very large numbers of advancement items that are likely to individually have minimal effect on progression.
        # 0-274 items: 5  # This will be most fills.
        # 275-324 items: 6
        # 325-374 items: 7  # Few worlds will be higher than this in progression fill.
        # 475-524 items: 10
        # 975-1024 items: 20
        # etc.
        largest_player_pool = max(map(len, reachable_items.values()), default=0)
        self._max_one_item_per_player_batch_size = (
                largest_player_pool * self._MAX_PERCENT_OF_LARGEST_STARTING_POOL_TO_PLACE)

        self._current_batch = self._new_batch(None)

    def _new_batch(self, previous_batch: _RestrictiveFillBatch | None = None) -> _RestrictiveFillBatch | None:
        """
        Create and return a new batch of items to place.

        :param previous_batch: The previous batch, or `None` if there was no previous batch.
        :return: A new batch, or `None` if there are no more items to place.
        """
        # Calculate the number of items, per player, to place in the new batch.
        reachable_items = self._reachable_items

        # Get the count of, and individual lengths of, non-empty remaining per-player item pools.
        nonzero_remaining_per_player = [len(items) for items in reachable_items.values() if items]
        num_players_with_remaining_items = len(nonzero_remaining_per_player)

        if num_players_with_remaining_items == 0:
            # No more items to place, so return None to signal this.
            # Later code in this function does not check for iterables being empty, and would need to be updated if this
            # early return is changed to occur later, or if this early return is removed entirely.
            return None

        # Find the length of the largest remaining item pool.
        largest_remaining = max(nonzero_remaining_per_player)
        if num_players_with_remaining_items > 1:
            # Adjust the batch size by the ratio of the average remaining item pool length to the largest remaining item
            # pool length.
            # Find the average length of the remaining item pools.
            average_remaining = sum(nonzero_remaining_per_player) / num_players_with_remaining_items
            # As the average remaining item pool length approaches the largest remaining item pool length, the batch
            # size approaches `max_one_item_per_player_batch_size`.
            batch_size_float = self._max_one_item_per_player_batch_size * average_remaining / largest_remaining
        else:
            batch_size_float = self._max_one_item_per_player_batch_size

        # Round to the nearest integer.
        batch_size = round(batch_size_float)
        # Limit the minimum number of items per player in the batch.
        batch_size = max(self._min_batch_size, batch_size)
        # Don't make the batch larger than the largest remaining item pool.
        batch_size = min(batch_size, largest_remaining)

        # Make per-batch arguments.

        # If a player has fewer items remaining than the size of the batch, then that player has some empty spaces for
        # items in the batch. This allows for items belonging to that player, that were displaced by a swap, to be added
        # to the current batch until the empty spaces for that player are used up.
        batch_empty_spaces = {player: batch_size - min(len(player_items), batch_size)
                              for player, player_items in reachable_items.items()}

        # Iterate the first `batch_size` items of each player's remaining items into a list of all items that will be
        # placed in the current batch.
        # Items to place are picked from the end of each player's item pool, so, to get the items in the order they will
        # be placed, the item pools must be iterated in reverse.
        item_iters = [reversed(items) for items in reachable_items.values() if items]
        batch_item_pool = [item for item_iter in item_iters
                           for item in itertools.islice(item_iter, batch_size)]

        # Collect the remaining items, which won't be placed in this batch, into a copy of `base_state` and make that
        # the base state for the batch.
        batch_base_state = self._base_state.copy()
        for item_iter in item_iters:
            for item in item_iter:
                batch_base_state.collect(item, True)

        if self._one_item_per_player:
            batched_placements_remaining = batch_size

            return _RestrictiveFillBatcher._RestrictiveFillBatchOneItemPerPlayer(
                batch_base_state,
                batch_empty_spaces,
                batch_item_pool,
                self._item_pool,
                batched_placements_remaining,
                reachable_items)
        else:
            items_per_player_in_batch = {player: batch_size - empty_spaces
                                         for player, empty_spaces in batch_empty_spaces.items()}
            batched_placements_remaining = sum(items_per_player_in_batch.values())

            if isinstance(previous_batch, _RestrictiveFillBatcher._RestrictiveFillBatchOneItemAtATime):
                # If the previous batch ended early by picking a player who had no items remaining in the batch, that
                # player should be picked when getting the first item to place in the new batch. This maintains fairness
                # at the boundary between one almost empty batch and the next batch.
                next_player_override = previous_batch.next_player_override
            else:
                next_player_override = None

            return _RestrictiveFillBatcher._RestrictiveFillBatchOneItemAtATime(
                batch_base_state,
                batch_empty_spaces,
                batch_item_pool,
                self._item_pool,
                batched_placements_remaining,
                reachable_items,
                items_per_player_in_batch,
                next_player_override)

    def pop_items_to_place(self) -> list[Item]:
        """
        Get and remove items to place from the ends of deques in `self.reachable_items`, also removing those items from
        `self.item_pool`.

        Automatically creates new batches internally as needed until all items have been placed.

        :return: A list of items to place, or an empty list when there are no more items to place.
        """
        current_batch = self._current_batch
        if current_batch is None:
            # No more items to place.
            return []
        # Batches are given references to `self.reachable_items` and `self.item_pool` when they are created, so do not
        # need to be given these collections of items again.
        popped_items = current_batch.pop_items_to_place()
        if not popped_items:
            # The current batch is exhausted, so create a new one and retry with the new batch.
            self._current_batch = self._new_batch(current_batch)
            # This recursive call is expected to only recurse at most once.
            # In the recursive call, either there are no more items to place, so `self._current_batch` became `None` and
            # `current_batch` will be `None`, or there are items to place, so `popped_items` will be non-empty. Either
            # way will not result in additional recursion.
            return self.pop_items_to_place()
        else:
            return popped_items

    def get_maximum_exploration_state(self, explore_locations: list[Location] | None, unplaced_items: list[Item]
                                      ) -> CollectionState:
        """
        Get the maximum exploration state for the currently reachable items.

        Must not be called after self.pop_items_to_place() has returned an empty list, indicating that there are no more
        items to place, or after self.finish_fill() has been called.

        An item is reachable if it matches any one of the following:
        A. It is in `self.item_pool`, so has not been placed yet and is not currently being placed.
        B. It is in `unplaced_items`, so could not be placed at any location.
        C. It is at a location in `explore_locations` that is reachable with all items in A-C.

        :param explore_locations: The locations to explore for reachable items. Defaults to all filled locations when
            `None`.
        :param unplaced_items: All items that could not be placed at any location.
        :return: A CollectionState that has collected all reachable advancement items.
        """
        assert self._current_batch is not None, "Cannot call when there are no more items to place."
        return self._current_batch.get_maximum_exploration_state(explore_locations, unplaced_items)

    def get_swap_state(self, displaced_item: Item, location: Location, explore_locations: list[Location] | None,
                       unsafe: bool) -> CollectionState:
        """
        Get the maximum exploration state for a potential swap.

        Must not be called after self.pop_items_to_place() has returned an empty list, indicating that there are no more
        items to place, or after self.finish_fill() has been called.

        :param displaced_item: The item displaced from `location`.
        :param location: The location of the swap attempt.
        :param explore_locations: The locations the swap state should sweep. `None` will sweep all filled locations.
        :param unsafe: Assume it will be possible to collect `displaced_item` before the item that is being placed, by
        continuing to swap.
        :return: A CollectionState that has collected all reachable items, additionally including `displaced_item` when
            `unsafe` is `True`.
        """
        assert self._current_batch is not None, "Cannot call when there are no more items to place."
        return self._current_batch.get_swap_state(displaced_item, location, explore_locations, unsafe)

    def update_for_swap(self, displaced_item: Item, item_to_place: Item, swap_location: Location) -> None:
        """
        Update the current batch for the result of a successful swap.

        Must not be called after self.pop_items_to_place() has returned an empty list, indicating that there are no more
        items to place, or after self.finish_fill() has been called.

        :param displaced_item: The item that was previously placed at swap_location and has been displaced by the swap.
        :param item_to_place: The item that has been placed at swap_location.
        :param swap_location: The location where the two items have been swapped.
        """
        assert self._current_batch is not None, "Cannot call when there are no more items to place."
        # Add the item back into the item_pool and the per-player pools in reachable_items.
        self._item_pool.append(displaced_item)
        self._reachable_items[displaced_item.player].appendleft(displaced_item)
        # Update the batch for the swap.
        return self._current_batch.update_for_swap(displaced_item, item_to_place, swap_location)

    def finish_fill(self, unplaced_items: list[Item]) -> None:
        """
        Add items that could not be placed back into the `item_pool` argument passed in __init__, and mark the batcher
        as having finished filling.

        :param unplaced_items: Items that could not be placed.
        """
        # After this, assertions will fail if an attempt is made to call a function that uses the current batch.
        self._current_batch = None
        self._item_pool.extend(unplaced_items)


def fill_restrictive(multiworld: MultiWorld, base_state: CollectionState, locations: typing.List[Location],
                     item_pool: typing.List[Item], single_player_placement: bool = False, lock: bool = False,
                     swap: bool = True, on_place: typing.Optional[typing.Callable[[Location], None]] = None,
                     allow_partial: bool = False, allow_excluded: bool = False, one_item_per_player: bool = True,
                     name: str = "Unknown") -> None:
    """
    :param multiworld: Multiworld to be filled.
    :param base_state: State assumed before fill.
    :param locations: Locations to be filled with item_pool, gets mutated by removing locations that get filled.
    :param item_pool: Items to fill into the locations, gets mutated by removing items that get placed.
    :param single_player_placement: if true, can speed up placement if everything belongs to a single player
    :param lock: locations are set to locked as they are filled
    :param swap: if true, swaps of already place items are done in the event of a dead end
    :param on_place: callback that is called when a placement happens
    :param allow_partial: only place what is possible. Remaining items will be in the item_pool list.
    :param allow_excluded: if true and placement fails, it is re-attempted while ignoring excluded on Locations
    :param name: name of this fill step for progress logging purposes
    """
    unplaced_items: typing.List[Item] = []
    placements: typing.List[Location] = []
    cleanup_required = False
    swapped_items: typing.Counter[typing.Tuple[int, str, bool]] = Counter()
    reachable_items: typing.Dict[int, typing.Deque[Item]] = {}
    for item in item_pool:
        reachable_items.setdefault(item.player, deque()).append(item)

    # for progress logging
    total = min(len(item_pool), len(locations))
    placed = 0

    # Fill is performed in batches so that sweeping to produce a maximum exploration state can begin from the state at
    # the start of each batch, rather than having to sweep from `base_state`.
    # The batcher manages all the batches internally, creating new batches automatically when the current batch runs out
    # of items to place.
    batcher = _RestrictiveFillBatcher(base_state, reachable_items, item_pool, one_item_per_player)
    # The batcher is responsible for modifying these from this point onwards.
    del item_pool
    del reachable_items

    while locations:
        # Pop items to place from the ends of deques in `reachable_items` and pop those same items from `item_pool`.
        items_to_place = batcher.pop_items_to_place()
        if not items_to_place:
            # There are no more items to place.
            break

        explore_locations = multiworld.get_filled_locations(item.player) if single_player_placement else None

        maximum_exploration_state = batcher.get_maximum_exploration_state(explore_locations, unplaced_items)

        has_beaten_game = multiworld.has_beaten_game(maximum_exploration_state)

        while items_to_place:
            # if we have run out of locations to fill,break out of this loop
            if not locations:
                unplaced_items += items_to_place
                break
            item_to_place = items_to_place.pop(0)

            spot_to_fill: typing.Optional[Location] = None

            # if minimal accessibility, only check whether location is reachable if game not beatable
            if multiworld.worlds[item_to_place.player].options.accessibility == Accessibility.option_minimal:
                perform_access_check = not multiworld.has_beaten_game(maximum_exploration_state,
                                                                      item_to_place.player) \
                    if single_player_placement else not has_beaten_game
            else:
                perform_access_check = True

            for i, location in enumerate(locations):
                if (not single_player_placement or location.player == item_to_place.player) \
                        and location.can_fill(maximum_exploration_state, item_to_place, perform_access_check):
                    # popping by index is faster than removing by content,
                    spot_to_fill = locations.pop(i)
                    # skipping a scan for the element
                    break

            else:
                # we filled all reachable spots.
                if swap:
                    # Keep a cache of previous safe swap states that might be usable to sweep from to produce the next
                    # swap state, instead of sweeping from `base_state` each time.
                    previous_safe_swap_state_cache: typing.Deque[CollectionState] = deque()
                    # Almost never are more than 2 states needed. The rare cases that do are usually highly restrictive
                    # single_player_placement=True pre-fills which can go through more than 10 states in some seeds.
                    max_swap_base_state_cache_length = 3

                    # try swapping this item with previously placed items in a safe way then in an unsafe way
                    swap_attempts = ((i, location, unsafe)
                                     for unsafe in (False, True)
                                     for i, location in enumerate(placements))
                    for (i, location, unsafe) in swap_attempts:
                        placed_item = location.item
                        # Unplaceable items can sometimes be swapped infinitely. Limit the
                        # number of times we will swap an individual item to prevent this
                        swap_count = swapped_items[placed_item.player, placed_item.name, unsafe]
                        if swap_count > 1:
                            continue

                        location.item = None
                        placed_item.location = None

                        for previous_safe_swap_state in previous_safe_swap_state_cache:
                            # If a state has already checked the location of the swap, then it cannot be used.
                            if location not in previous_safe_swap_state.advancements:
                                # Previous swap states will have collected all items in `item_pool`, so the new
                                # `swap_state` can skip having to collect them again.
                                # Previous swap states will also have already checked many locations, making the sweep
                                # faster.
                                swap_state = sweep_from_pool(previous_safe_swap_state, (placed_item,) if unsafe else (),
                                                             multiworld.get_filled_locations(item.player)
                                                             if single_player_placement else None)
                                break
                        else:
                            # No previous swap_state was usable as a base state to sweep from, so create a new one.
                            explore_locations = (multiworld.get_filled_locations(item.player)
                                                 if single_player_placement else None)
                            swap_state = batcher.get_swap_state(placed_item, location, explore_locations, unsafe)
                            # Unsafe states should not be added to the cache because they have collected `placed_item`.
                            if not unsafe:
                                if len(previous_safe_swap_state_cache) >= max_swap_base_state_cache_length:
                                    # Remove the oldest cached state.
                                    previous_safe_swap_state_cache.pop()
                                # Add the new state to the start of the cache.
                                previous_safe_swap_state_cache.appendleft(swap_state)
                        # unsafe means swap_state assumes we can somehow collect placed_item before item_to_place
                        # by continuing to swap, which is not guaranteed. This is unsafe because there is no mechanic
                        # to clean that up later, so there is a chance generation fails.
                        if (not single_player_placement or location.player == item_to_place.player) \
                                and location.can_fill(swap_state, item_to_place, perform_access_check):
                            # Add this item to the existing placement, and
                            # add the old item to the back of the queue
                            spot_to_fill = placements.pop(i)

                            swap_count += 1
                            swapped_items[placed_item.player, placed_item.name, unsafe] = swap_count

                            # cleanup at the end to hopefully get better errors
                            cleanup_required = True

                            batcher.update_for_swap(placed_item, item_to_place, spot_to_fill)
                            break

                        # Item can't be placed here, restore original item
                        location.item = placed_item
                        placed_item.location = location

                    if spot_to_fill is None:
                        # Can't place this item, move on to the next
                        unplaced_items.append(item_to_place)
                        continue
                else:
                    unplaced_items.append(item_to_place)
                    continue
            multiworld.push_item(spot_to_fill, item_to_place, False)
            spot_to_fill.locked = lock
            placements.append(spot_to_fill)
            placed += 1
            if not placed % 1000:
                _log_fill_progress(name, placed, total)
            if on_place:
                on_place(spot_to_fill)

    if total > 1000:
        _log_fill_progress(name, placed, total)

    if cleanup_required:
        # validate all placements and remove invalid ones
        state = sweep_from_pool(
            base_state, [], multiworld.get_filled_locations(item.player)
            if single_player_placement else None)
        for placement in placements:
            if multiworld.worlds[placement.item.player].options.accessibility != "minimal" and not placement.can_reach(state):
                placement.item.location = None
                unplaced_items.append(placement.item)
                placement.item = None
                locations.append(placement)

    if allow_excluded:
        # check if partial fill is the result of excluded locations, in which case retry
        excluded_locations = [
            location for location in locations
            if location.progress_type == location.progress_type.EXCLUDED and not location.item
        ]
        if excluded_locations:
            for location in excluded_locations:
                location.progress_type = location.progress_type.DEFAULT
            fill_restrictive(multiworld, base_state, excluded_locations, unplaced_items, single_player_placement, lock,
                             swap, on_place, allow_partial, False)
            for location in excluded_locations:
                if not location.item:
                    location.progress_type = location.progress_type.EXCLUDED

    if not allow_partial and len(unplaced_items) > 0 and len(locations) > 0:
        # There are leftover unplaceable items and locations that won't accept them
        if multiworld.can_beat_game():
            logging.warning(
                f"Not all items placed. Game beatable anyway.\nCould not place:\n"
                f"{', '.join(str(item) for item in unplaced_items)}")
        else:
            raise FillError(f"No more spots to place {len(unplaced_items)} items. Remaining locations are invalid.\n"
                            f"Unplaced items:\n"
                            f"{', '.join(str(item) for item in unplaced_items)}\n"
                            f"Unfilled locations:\n"
                            f"{', '.join(str(location) for location in locations)}\n"
                            f"Already placed {len(placements)}:\n"
                            f"{', '.join(str(place) for place in placements)}", multiworld=multiworld)

    batcher.finish_fill(unplaced_items)


def remaining_fill(multiworld: MultiWorld,
                   locations: typing.List[Location],
                   itempool: typing.List[Item],
                   name: str = "Remaining", 
                   move_unplaceable_to_start_inventory: bool = False,
                   check_location_can_fill: bool = False) -> None:
    unplaced_items: typing.List[Item] = []
    placements: typing.List[Location] = []
    swapped_items: typing.Counter[typing.Tuple[int, str]] = Counter()
    total = min(len(itempool), len(locations))
    placed = 0

    # Optimisation: Decide whether to do full location.can_fill check (respect excluded), or only check the item rule
    if check_location_can_fill:
        state = CollectionState(multiworld)

        def location_can_fill_item(location_to_fill: Location, item_to_fill: Item):
            return location_to_fill.can_fill(state, item_to_fill, check_access=False)
    else:
        def location_can_fill_item(location_to_fill: Location, item_to_fill: Item):
            return location_to_fill.item_rule(item_to_fill)

    while locations and itempool:
        item_to_place = itempool.pop()
        spot_to_fill: typing.Optional[Location] = None

        for i, location in enumerate(locations):
            if location_can_fill_item(location, item_to_place):
                # popping by index is faster than removing by content,
                spot_to_fill = locations.pop(i)
                # skipping a scan for the element
                break

        else:
            # we filled all reachable spots.
            # try swapping this item with previously placed items

            for (i, location) in enumerate(placements):
                placed_item = location.item
                # Unplaceable items can sometimes be swapped infinitely. Limit the
                # number of times we will swap an individual item to prevent this

                if swapped_items[placed_item.player,
                                 placed_item.name] > 1:
                    continue

                location.item = None
                placed_item.location = None
                if location_can_fill_item(location, item_to_place):
                    # Add this item to the existing placement, and
                    # add the old item to the back of the queue
                    spot_to_fill = placements.pop(i)

                    swapped_items[placed_item.player,
                                  placed_item.name] += 1

                    itempool.append(placed_item)

                    break

                # Item can't be placed here, restore original item
                location.item = placed_item
                placed_item.location = location

            if spot_to_fill is None:
                # Can't place this item, move on to the next
                unplaced_items.append(item_to_place)
                continue

        multiworld.push_item(spot_to_fill, item_to_place, False)
        placements.append(spot_to_fill)
        placed += 1
        if not placed % 1000:
            _log_fill_progress(name, placed, total)

    if total > 1000:
        _log_fill_progress(name, placed, total)

    if unplaced_items and locations:
        # There are leftover unplaceable items and locations that won't accept them
        if move_unplaceable_to_start_inventory:
            last_batch = []
            for item in unplaced_items:
                logging.debug(f"Moved {item} to start_inventory to prevent fill failure.")
                multiworld.push_precollected(item)
                last_batch.append(multiworld.worlds[item.player].create_filler())
            remaining_fill(multiworld, locations, unplaced_items, name + " Start Inventory Retry")
        else:
            raise FillError(f"No more spots to place {len(unplaced_items)} items. Remaining locations are invalid.\n"
                            f"Unplaced items:\n"
                            f"{', '.join(str(item) for item in unplaced_items)}\n"
                            f"Unfilled locations:\n"
                            f"{', '.join(str(location) for location in locations)}\n"
                            f"Already placed {len(placements)}:\n"
                            f"{', '.join(str(place) for place in placements)}", multiworld=multiworld)

    itempool.extend(unplaced_items)


def fast_fill(multiworld: MultiWorld,
              item_pool: typing.List[Item],
              fill_locations: typing.List[Location]) -> typing.Tuple[typing.List[Item], typing.List[Location]]:
    placing = min(len(item_pool), len(fill_locations))
    for item, location in zip(item_pool, fill_locations):
        multiworld.push_item(location, item, False)
    return item_pool[placing:], fill_locations[placing:]


def accessibility_corrections(multiworld: MultiWorld, state: CollectionState, locations, pool=[]):
    maximum_exploration_state = sweep_from_pool(state, pool)
    minimal_players = {player for player in multiworld.player_ids if
                       multiworld.worlds[player].options.accessibility == "minimal"}
    unreachable_locations = [location for location in multiworld.get_locations() if
                             location.player in minimal_players and
                             not location.can_reach(maximum_exploration_state)]
    for location in unreachable_locations:
        if (location.item is not None and location.item.advancement and location.address is not None and not
                location.locked and location.item.player not in minimal_players):
            pool.append(location.item)
            location.item = None
            if location in state.advancements:
                state.advancements.remove(location)
                state.remove(location.item)
            locations.append(location)
    if pool and locations:
        locations.sort(key=lambda loc: loc.progress_type != LocationProgressType.PRIORITY)
        fill_restrictive(multiworld, state, locations, pool, name="Accessibility Corrections")


def inaccessible_location_rules(multiworld: MultiWorld, state: CollectionState, locations):
    maximum_exploration_state = sweep_from_pool(state)
    unreachable_locations = [location for location in locations if not location.can_reach(maximum_exploration_state)]
    if unreachable_locations:
        def forbid_important_item_rule(item: Item):
            return not ((item.classification & 0b0011) and multiworld.worlds[item.player].options.accessibility != "minimal")

        for location in unreachable_locations:
            add_item_rule(location, forbid_important_item_rule)


def distribute_early_items(multiworld: MultiWorld,
                           fill_locations: typing.List[Location],
                           itempool: typing.List[Item]) -> typing.Tuple[typing.List[Location], typing.List[Item]]:
    """ returns new fill_locations and itempool """
    early_items_count: typing.Dict[typing.Tuple[str, int], typing.List[int]] = {}
    for player in multiworld.player_ids:
        items = itertools.chain(multiworld.early_items[player], multiworld.local_early_items[player])
        for item in items:
            early_items_count[item, player] = [multiworld.early_items[player].get(item, 0),
                                               multiworld.local_early_items[player].get(item, 0)]
    if early_items_count:
        early_locations: typing.List[Location] = []
        early_priority_locations: typing.List[Location] = []
        loc_indexes_to_remove: typing.Set[int] = set()
        base_state = multiworld.state.copy()
        base_state.sweep_for_advancements(locations=(loc for loc in multiworld.get_filled_locations() if loc.address is None))
        for i, loc in enumerate(fill_locations):
            if loc.can_reach(base_state):
                if loc.progress_type == LocationProgressType.PRIORITY:
                    early_priority_locations.append(loc)
                else:
                    early_locations.append(loc)
                loc_indexes_to_remove.add(i)
        fill_locations = [loc for i, loc in enumerate(fill_locations) if i not in loc_indexes_to_remove]

        early_prog_items: typing.List[Item] = []
        early_rest_items: typing.List[Item] = []
        early_local_prog_items: typing.Dict[int, typing.List[Item]] = {player: [] for player in multiworld.player_ids}
        early_local_rest_items: typing.Dict[int, typing.List[Item]] = {player: [] for player in multiworld.player_ids}
        item_indexes_to_remove: typing.Set[int] = set()
        for i, item in enumerate(itempool):
            if (item.name, item.player) in early_items_count:
                if item.advancement:
                    if early_items_count[item.name, item.player][1]:
                        early_local_prog_items[item.player].append(item)
                        early_items_count[item.name, item.player][1] -= 1
                    else:
                        early_prog_items.append(item)
                        early_items_count[item.name, item.player][0] -= 1
                else:
                    if early_items_count[item.name, item.player][1]:
                        early_local_rest_items[item.player].append(item)
                        early_items_count[item.name, item.player][1] -= 1
                    else:
                        early_rest_items.append(item)
                        early_items_count[item.name, item.player][0] -= 1
                item_indexes_to_remove.add(i)
                if early_items_count[item.name, item.player] == [0, 0]:
                    del early_items_count[item.name, item.player]
                    if len(early_items_count) == 0:
                        break
        itempool = [item for i, item in enumerate(itempool) if i not in item_indexes_to_remove]
        for player in multiworld.player_ids:
            player_local = early_local_rest_items[player]
            fill_restrictive(multiworld, base_state,
                             [loc for loc in early_locations if loc.player == player],
                             player_local, lock=True, allow_partial=True, name=f"Local Early Items P{player}")
            if player_local:
                logging.warning(f"Could not fulfill rules of early items: {player_local}")
                early_rest_items.extend(early_local_rest_items[player])
        early_locations = [loc for loc in early_locations if not loc.item]
        fill_restrictive(multiworld, base_state, early_locations, early_rest_items, lock=True, allow_partial=True,
                         name="Early Items")
        early_locations += early_priority_locations
        for player in multiworld.player_ids:
            player_local = early_local_prog_items[player]
            fill_restrictive(multiworld, base_state,
                             [loc for loc in early_locations if loc.player == player],
                             player_local, lock=True, allow_partial=True, name=f"Local Early Progression P{player}")
            if player_local:
                logging.warning(f"Could not fulfill rules of early items: {player_local}")
                early_prog_items.extend(player_local)
        early_locations = [loc for loc in early_locations if not loc.item]
        fill_restrictive(multiworld, base_state, early_locations, early_prog_items, lock=True, allow_partial=True,
                         name="Early Progression")
        unplaced_early_items = early_rest_items + early_prog_items
        if unplaced_early_items:
            logging.warning("Ran out of early locations for early items. Failed to place "
                            f"{unplaced_early_items} early.")
            itempool += unplaced_early_items

        fill_locations.extend(early_locations)
        multiworld.random.shuffle(fill_locations)
    return fill_locations, itempool


def distribute_items_restrictive(multiworld: MultiWorld,
                                 panic_method: typing.Literal["swap", "raise", "start_inventory"] = "swap") -> None:
    assert all(item.location is None for item in multiworld.itempool), (
        "At the start of distribute_items_restrictive, "
        "there are items in the multiworld itempool that are already placed on locations:\n"
        f"{[(item.location, item) for item in multiworld.itempool if item.location is not None]}"
    )

    fill_locations = sorted(multiworld.get_unfilled_locations())
    multiworld.random.shuffle(fill_locations)
    # get items to distribute
    itempool = sorted(multiworld.itempool)
    multiworld.random.shuffle(itempool)

    fill_locations, itempool = distribute_early_items(multiworld, fill_locations, itempool)

    progitempool: typing.List[Item] = []
    usefulitempool: typing.List[Item] = []
    filleritempool: typing.List[Item] = []

    for item in itempool:
        if item.advancement:
            progitempool.append(item)
        elif item.useful:
            usefulitempool.append(item)
        else:
            filleritempool.append(item)

    call_all(multiworld, "fill_hook", progitempool, usefulitempool, filleritempool, fill_locations)

    locations: typing.Dict[LocationProgressType, typing.List[Location]] = {
        loc_type: [] for loc_type in LocationProgressType}

    for loc in fill_locations:
        locations[loc.progress_type].append(loc)

    prioritylocations = locations[LocationProgressType.PRIORITY]
    defaultlocations = locations[LocationProgressType.DEFAULT]
    excludedlocations = locations[LocationProgressType.EXCLUDED]

    # can't lock due to accessibility corrections touching things, so we remember which ones got placed and lock later
    lock_later = []

    def mark_for_locking(location: Location):
        nonlocal lock_later
        lock_later.append(location)

    single_player = multiworld.players == 1 and not multiworld.groups

    if prioritylocations:
        regular_progression = []
        deprioritized_progression = []
        for item in progitempool:
            if item.deprioritized:
                deprioritized_progression.append(item)
            else:
                regular_progression.append(item)

        # "priority fill"
        # try without deprioritized items in the mix at all. This means they need to be collected into state first.
        priority_fill_state = sweep_from_pool(multiworld.state, deprioritized_progression)
        fill_restrictive(multiworld, priority_fill_state, prioritylocations, regular_progression,
                         single_player_placement=single_player, swap=False, on_place=mark_for_locking,
                         name="Priority", one_item_per_player=True, allow_partial=True)

        if prioritylocations and regular_progression:
            # retry with one_item_per_player off because some priority fills can fail to fill with that optimization
            # deprioritized items are still not in the mix, so they need to be collected into state first.
            priority_retry_state = sweep_from_pool(multiworld.state, deprioritized_progression)
            fill_restrictive(multiworld, priority_retry_state, prioritylocations, regular_progression,
                             single_player_placement=single_player, swap=False, on_place=mark_for_locking,
                             name="Priority Retry", one_item_per_player=False, allow_partial=True)

        if prioritylocations and deprioritized_progression:
            # There are no more regular progression items that can be placed on any priority locations.
            # We'd still prefer to place deprioritized progression items on priority locations over filler items.
            # Since we're leaving out the remaining regular progression now, we need to collect it into state first.
            priority_retry_2_state = sweep_from_pool(multiworld.state, regular_progression)
            fill_restrictive(multiworld, priority_retry_2_state, prioritylocations, deprioritized_progression,
                             single_player_placement=single_player, swap=False, on_place=mark_for_locking,
                             name="Priority Retry 2", one_item_per_player=True, allow_partial=True)

        if prioritylocations and deprioritized_progression:
            # retry with deprioritized items AND without one_item_per_player optimisation
            # Since we're leaving out the remaining regular progression now, we need to collect it into state first.
            priority_retry_3_state = sweep_from_pool(multiworld.state, regular_progression)
            fill_restrictive(multiworld, priority_retry_3_state, prioritylocations, deprioritized_progression,
                             single_player_placement=single_player, swap=False, on_place=mark_for_locking,
                             name="Priority Retry 3", one_item_per_player=False)

        # restore original order of progitempool
        progitempool[:] = [item for item in progitempool if not item.location]
        accessibility_corrections(multiworld, multiworld.state, prioritylocations, progitempool)
        defaultlocations = prioritylocations + defaultlocations

    if progitempool:
        # "advancement/progression fill"
        maximum_exploration_state = sweep_from_pool(multiworld.state)
        if panic_method == "swap":
            fill_restrictive(multiworld, maximum_exploration_state, defaultlocations, progitempool, swap=True,
                             name="Progression", single_player_placement=single_player)
        elif panic_method == "raise":
            fill_restrictive(multiworld, maximum_exploration_state, defaultlocations, progitempool, swap=False,
                             name="Progression", single_player_placement=single_player)
        elif panic_method == "start_inventory":
            fill_restrictive(multiworld, maximum_exploration_state, defaultlocations, progitempool, swap=False,
                             allow_partial=True, name="Progression", single_player_placement=single_player)
            if progitempool:
                for item in progitempool:
                    logging.debug(f"Moved {item} to start_inventory to prevent fill failure.")
                    multiworld.push_precollected(item)
                    filleritempool.append(multiworld.worlds[item.player].create_filler())
                logging.warning(f"{len(progitempool)} items moved to start inventory,"
                                f" due to failure in Progression fill step.")
                progitempool[:] = []

        else:
            raise ValueError(f"Generator Panic Method {panic_method} not recognized.")
        if progitempool:
            raise FillError(
                f"Not enough locations for progression items. "
                f"There are {len(progitempool)} more progression items than there are available locations.\n"
                f"Unfilled locations:\n{multiworld.get_unfilled_locations()}.",
                multiworld=multiworld,
            )
        accessibility_corrections(multiworld, multiworld.state, defaultlocations)

    for location in lock_later:
        if location.item:
            location.locked = True
    del mark_for_locking, lock_later

    inaccessible_location_rules(multiworld, multiworld.state, defaultlocations)

    remaining_fill(multiworld, excludedlocations, filleritempool, "Remaining Excluded",
                   move_unplaceable_to_start_inventory=panic_method=="start_inventory")

    if excludedlocations:
        raise FillError(
            f"Not enough filler items for excluded locations. "
            f"There are {len(excludedlocations)} more excluded locations than excludable items.",
            multiworld=multiworld,
        )

    restitempool = filleritempool + usefulitempool

    remaining_fill(multiworld, defaultlocations, restitempool,
                   move_unplaceable_to_start_inventory=panic_method=="start_inventory")

    unplaced = restitempool
    unfilled = defaultlocations

    if unplaced or unfilled:
        logging.warning(
            f"Unplaced items({len(unplaced)}): {unplaced} - Unfilled Locations({len(unfilled)}): {unfilled}")
        items_counter = Counter(location.item.player for location in multiworld.get_filled_locations())
        locations_counter = Counter(location.player for location in multiworld.get_locations())
        items_counter.update(item.player for item in unplaced)
        print_data = {"items": items_counter, "locations": locations_counter}
        logging.info(f"Per-Player counts: {print_data})")

        more_locations = locations_counter - items_counter
        more_items = items_counter - locations_counter
        for player in multiworld.player_ids:
            if more_locations[player]:
                logging.error(
                    f"Player {multiworld.get_player_name(player)} had {more_locations[player]} more locations than items.")
            elif more_items[player]:
                logging.warning(
                    f"Player {multiworld.get_player_name(player)} had {more_items[player]} more items than locations.")
        if unfilled:
            raise FillError(
                f"Unable to fill all locations.\n" +
                f"Unfilled locations({len(unfilled)}): {unfilled}"
            )
        else:
            logging.warning(
                f"Unable to place all items.\n" +
                f"Unplaced items({len(unplaced)}): {unplaced}"
            )


def flood_items(multiworld: MultiWorld) -> None:
    # get items to distribute
    multiworld.random.shuffle(multiworld.itempool)
    itempool = multiworld.itempool
    progress_done = False

    # sweep once to pick up preplaced items
    multiworld.state.sweep_for_advancements()

    # fill multiworld from top of itempool while we can
    while not progress_done:
        location_list = multiworld.get_unfilled_locations()
        multiworld.random.shuffle(location_list)
        spot_to_fill = None
        for location in location_list:
            if location.can_fill(multiworld.state, itempool[0]):
                spot_to_fill = location
                break

        if spot_to_fill:
            item = itempool.pop(0)
            multiworld.push_item(spot_to_fill, item, True)
            continue

        # ran out of spots, check if we need to step in and correct things
        if len(multiworld.get_reachable_locations()) == len(multiworld.get_locations()):
            progress_done = True
            continue

        # need to place a progress item instead of an already placed item, find candidate
        item_to_place = None
        candidate_item_to_place = None
        for item in itempool:
            if item.advancement:
                candidate_item_to_place = item
                if multiworld.unlocks_new_location(item):
                    item_to_place = item
                    break

        # we might be in a situation where all new locations require multiple items to reach.
        # If that is the case, just place any advancement item we've found and continue trying
        if item_to_place is None:
            if candidate_item_to_place is not None:
                item_to_place = candidate_item_to_place
            else:
                raise FillError('No more progress items left to place.', multiworld=multiworld)

        # find item to replace with progress item
        location_list = multiworld.get_reachable_locations()
        multiworld.random.shuffle(location_list)
        for location in location_list:
            if location.item is not None and not location.item.advancement:
                # safe to replace
                replace_item = location.item
                replace_item.location = None
                itempool.append(replace_item)
                multiworld.push_item(location, item_to_place, True)
                itempool.remove(item_to_place)
                break


def balance_multiworld_progression(multiworld: MultiWorld) -> None:
    # A system to reduce situations where players have no checks remaining, popularly known as "BK mode."
    # Overall progression balancing algorithm:
    # Gather up all locations in a sphere.
    # Define a threshold value based on the player with the most available locations.
    # If other players are below the threshold value, swap progression in this sphere into earlier spheres,
    #   which gives more locations available by this sphere.
    balanceable_players: typing.Dict[int, float] = {
        player: multiworld.worlds[player].options.progression_balancing / 100
        for player in multiworld.player_ids
        if multiworld.worlds[player].options.progression_balancing > 0
    }
    if not balanceable_players:
        logging.info("Skipping multiworld progression balancing.")
    else:
        logging.info(f"Balancing multiworld progression for {len(balanceable_players)} Players.")
        logging.debug(balanceable_players)
        state: CollectionState = CollectionState(multiworld)
        checked_locations: typing.Set[Location] = set()
        unchecked_locations: typing.Set[Location] = set(multiworld.get_locations())

        total_locations_count: typing.Counter[int] = Counter(
            location.player
            for location in multiworld.get_locations()
            if not location.locked
        )
        reachable_locations_count: typing.Dict[int, int] = {
            player: 0
            for player in multiworld.player_ids
            if total_locations_count[player] and len(multiworld.get_filled_locations(player)) != 0
        }
        balanceable_players = {
            player: balanceable_players[player]
            for player in balanceable_players
            if total_locations_count[player]
        }
        sphere_num: int = 1
        moved_item_count: int = 0

        def get_sphere_locations(sphere_state: CollectionState,
                                 locations: typing.Set[Location]) -> typing.Set[Location]:
            return {loc for loc in locations if sphere_state.can_reach(loc)}

        def item_percentage(player: int, num: int) -> float:
            return num / total_locations_count[player]

        # If there are no locations that aren't locked, there's no point in attempting to balance progression.
        if len(total_locations_count) == 0:
            return

        while True:
            # Gather non-locked locations.
            # This ensures that only shuffled locations get counted for progression balancing,
            #   i.e. the items the players will be checking.
            sphere_locations = get_sphere_locations(state, unchecked_locations)
            for location in sphere_locations:
                unchecked_locations.remove(location)
                if not location.locked:
                    reachable_locations_count[location.player] += 1

            logging.debug(f"Sphere {sphere_num}")
            logging.debug(f"Reachable locations: {reachable_locations_count}")
            debug_percentages = {
                player: round(item_percentage(player, num), 2)
                for player, num in reachable_locations_count.items()
            }
            logging.debug(f"Reachable percentages: {debug_percentages}\n")
            sphere_num += 1

            if checked_locations:
                max_percentage = max(map(lambda p: item_percentage(p, reachable_locations_count[p]),
                                         reachable_locations_count))
                threshold_percentages = {
                    player: max_percentage * balanceable_players[player]
                    for player in balanceable_players
                }
                logging.debug(f"Thresholds: {threshold_percentages}")
                balancing_players = {
                    player
                    for player, reachables in reachable_locations_count.items()
                    if (player in threshold_percentages
                        and item_percentage(player, reachables) < threshold_percentages[player])
                }
                if balancing_players:
                    balancing_state = state.copy()
                    balancing_unchecked_locations = unchecked_locations.copy()
                    balancing_reachables = reachable_locations_count.copy()
                    balancing_sphere = sphere_locations.copy()
                    candidate_items: typing.Dict[int, typing.Set[Location]] = collections.defaultdict(set)
                    while True:
                        # Check locations in the current sphere and gather progression items to swap earlier
                        for location in balancing_sphere:
                            if location.advancement:
                                balancing_state.collect(location.item, True, location)
                                player = location.item.player
                                # only replace items that end up in another player's world
                                if (not location.locked and not location.item.skip_in_prog_balancing and
                                        player in balancing_players and
                                        location.player != player and
                                        location.progress_type != LocationProgressType.PRIORITY):
                                    candidate_items[player].add(location)
                                    logging.debug(f"Candidate item: {location.name}, {location.item.name}")
                        balancing_sphere = get_sphere_locations(balancing_state, balancing_unchecked_locations)
                        for location in balancing_sphere:
                            balancing_unchecked_locations.remove(location)
                            if not location.locked:
                                balancing_reachables[location.player] += 1
                        if multiworld.has_beaten_game(balancing_state) or all(
                                item_percentage(player, reachables) >= threshold_percentages[player]
                                for player, reachables in balancing_reachables.items()
                                if player in threshold_percentages):
                            break
                        elif not balancing_sphere:
                            raise RuntimeError("Not all required items reachable. Something went terribly wrong here.")
                    # Gather a set of locations which we can swap items into
                    unlocked_locations: typing.Dict[int, typing.Set[Location]] = collections.defaultdict(set)
                    for l in unchecked_locations:
                        if l not in balancing_unchecked_locations:
                            unlocked_locations[l.player].add(l)
                    items_to_replace: typing.List[Location] = []
                    for player in balancing_players:
                        locations_to_test = unlocked_locations[player]
                        items_to_test = list(candidate_items[player])
                        items_to_test.sort()
                        multiworld.random.shuffle(items_to_test)
                        while items_to_test:
                            testing = items_to_test.pop()
                            reducing_state = state.copy()
                            for location in itertools.chain((
                                    l for l in items_to_replace
                                    if l.item.player == player
                            ), items_to_test):
                                reducing_state.collect(location.item, True, location)

                            reducing_state.sweep_for_advancements(locations=locations_to_test)

                            if multiworld.has_beaten_game(balancing_state):
                                if not multiworld.has_beaten_game(reducing_state):
                                    items_to_replace.append(testing)
                            else:
                                reduced_sphere = get_sphere_locations(reducing_state, locations_to_test)
                                p = item_percentage(player, reachable_locations_count[player] + len(reduced_sphere))
                                if p < threshold_percentages[player]:
                                    items_to_replace.append(testing)

                    old_moved_item_count = moved_item_count

                    # sort then shuffle to maintain deterministic behaviour,
                    # while allowing use of set for better algorithm growth behaviour elsewhere
                    replacement_locations = sorted(l for l in checked_locations if not l.advancement and not l.locked)
                    multiworld.random.shuffle(replacement_locations)
                    items_to_replace.sort()
                    multiworld.random.shuffle(items_to_replace)

                    # Start swapping items. Since we swap into earlier spheres, no need for accessibility checks. 
                    while replacement_locations and items_to_replace:
                        old_location = items_to_replace.pop()
                        for i, new_location in enumerate(replacement_locations):
                            if new_location.can_fill(state, old_location.item, False) and \
                                    old_location.can_fill(state, new_location.item, False):
                                replacement_locations.pop(i)
                                swap_location_item(old_location, new_location)
                                logging.debug(f"Progression balancing moved {new_location.item} to {new_location}, "
                                              f"displacing {old_location.item} into {old_location}")
                                moved_item_count += 1
                                state.collect(new_location.item, True, new_location)
                                break
                        else:
                            logging.warning(f"Could not Progression Balance {old_location.item}")

                    if old_moved_item_count < moved_item_count:
                        logging.debug(f"Moved {moved_item_count} items so far\n")
                        unlocked = {fresh for player in balancing_players for fresh in unlocked_locations[player]}
                        for location in get_sphere_locations(state, unlocked):
                            unchecked_locations.remove(location)
                            if not location.locked:
                                reachable_locations_count[location.player] += 1
                            sphere_locations.add(location)

            for location in sphere_locations:
                if location.advancement:
                    state.collect(location.item, True, location)
            checked_locations |= sphere_locations

            if multiworld.has_beaten_game(state):
                break
            elif not sphere_locations:
                logging.warning("Progression Balancing ran out of paths.")
                break


def swap_location_item(location_1: Location, location_2: Location, check_locked: bool = True) -> None:
    """Swaps Items of locations. Does NOT swap flags like shop_slot or locked, but does swap event"""
    if check_locked:
        if location_1.locked:
            logging.warning(f"Swapping {location_1}, which is marked as locked.")
        if location_2.locked:
            logging.warning(f"Swapping {location_2}, which is marked as locked.")
    location_2.item, location_1.item = location_1.item, location_2.item
    location_1.item.location = location_1
    location_2.item.location = location_2


def parse_planned_blocks(multiworld: MultiWorld) -> dict[int, list[PlandoItemBlock]]:
    def warn(warning: str, force: bool | str) -> None:
        if isinstance(force, bool):
            logging.warning(f"{warning}")
        else:
            logging.debug(f"{warning}")

    def failed(warning: str, force: bool | str) -> None:
        if force is True:
            raise Exception(warning)
        else:
            warn(warning, force)

    world_name_lookup = multiworld.world_name_lookup

    plando_blocks: dict[int, list[PlandoItemBlock]] = dict()
    player_ids: set[int] = set(multiworld.player_ids)
    for player in player_ids:
        plando_blocks[player] = []
        for block in multiworld.worlds[player].options.plando_items:
            new_block: PlandoItemBlock = PlandoItemBlock(player, block.from_pool, block.force)
            target_world = block.world
            if target_world is False or multiworld.players == 1:  # target own world
                worlds: set[int] = {player}
            elif target_world is True:  # target any worlds besides own
                worlds = set(multiworld.player_ids) - {player}
            elif target_world is None:  # target all worlds
                worlds = set(multiworld.player_ids)
            elif type(target_world) == list:  # list of target worlds
                worlds = set()
                for listed_world in target_world:
                    if listed_world not in world_name_lookup:
                        failed(f"Cannot place item to {listed_world}'s world as that world does not exist.",
                               block.force)
                        continue
                    worlds.add(world_name_lookup[listed_world])
            elif type(target_world) == int:  # target world by slot number
                if target_world not in range(1, multiworld.players + 1):
                    failed(
                        f"Cannot place item in world {target_world} as it is not in range of (1, {multiworld.players})",
                        block.force)
                    continue
                worlds = {target_world}
            else:  # target world by slot name
                if target_world not in world_name_lookup:
                    failed(f"Cannot place item to {target_world}'s world as that world does not exist.",
                           block.force)
                    continue
                worlds = {world_name_lookup[target_world]}
            new_block.worlds = worlds

            items: list[str] | dict[str, typing.Any] = block.items
            if isinstance(items, dict):
                item_list: list[str] = []
                for key, value in items.items():
                    if value is True:
                        value = multiworld.itempool.count(multiworld.worlds[player].create_item(key))
                    item_list += [key] * value
                items = item_list
            new_block.items = items

            locations: list[str] = block.locations
            if isinstance(locations, str):
                locations = [locations]

            resolved_locations: list[Location] = []
            for target_player in worlds:
                locations_from_groups: list[str] = []
                world_locations = multiworld.get_unfilled_locations(target_player)
                for group in multiworld.worlds[target_player].location_name_groups:
                    if group in locations:
                        locations_from_groups.extend(multiworld.worlds[target_player].location_name_groups[group])
                resolved_locations.extend(location for location in world_locations
                                          if location.name in [*locations, *locations_from_groups])
            new_block.locations = sorted(dict.fromkeys(locations))
            new_block.resolved_locations = sorted(set(resolved_locations))

            count = block.count
            if not count:
                count = (min(len(new_block.items), len(new_block.resolved_locations))
                         if new_block.resolved_locations else len(new_block.items))
            if isinstance(count, int):
                count = {"min": count, "max": count}
            if "min" not in count:
                count["min"] = 0
            if "max" not in count:
                count["max"] = (min(len(new_block.items), len(new_block.resolved_locations))
                                if new_block.resolved_locations else len(new_block.items))


            new_block.count = count
            plando_blocks[player].append(new_block)

    return plando_blocks


def resolve_early_locations_for_planned(multiworld: MultiWorld):
    def warn(warning: str, force: bool | str) -> None:
        if isinstance(force, bool):
            logging.warning(f"{warning}")
        else:
            logging.debug(f"{warning}")

    def failed(warning: str, force: bool | str) -> None:
        if force is True:
            raise Exception(warning)
        else:
            warn(warning, force)

    swept_state = multiworld.state.copy()
    swept_state.sweep_for_advancements()
    reachable = frozenset(multiworld.get_reachable_locations(swept_state))
    early_locations: dict[int, list[Location]] = collections.defaultdict(list)
    non_early_locations: dict[int, list[Location]] = collections.defaultdict(list)
    for loc in multiworld.get_unfilled_locations():
        if loc in reachable:
            early_locations[loc.player].append(loc)
        else:  # not reachable with swept state
            non_early_locations[loc.player].append(loc)

    for player in multiworld.plando_item_blocks:
        removed = []
        for block in multiworld.plando_item_blocks[player]:
            locations = block.locations
            resolved_locations = block.resolved_locations
            worlds = block.worlds
            if "early_locations" in locations:
                for target_player in worlds:
                    resolved_locations += early_locations[target_player]
            if "non_early_locations" in locations:
                for target_player in worlds:
                    resolved_locations += non_early_locations[target_player]

            if block.count["max"] > len(block.items):
                count = block.count["max"]
                failed(f"Plando count {count} greater than items specified", block.force)
                block.count["max"] = len(block.items)
                if block.count["min"] > len(block.items):
                    block.count["min"] = len(block.items)
            if block.count["max"] > len(block.resolved_locations) > 0:
                count = block.count["max"]
                failed(f"Plando count {count} greater than locations specified", block.force)
                block.count["max"] = len(block.resolved_locations)
                if block.count["min"] > len(block.resolved_locations):
                    block.count["min"] = len(block.resolved_locations)
            block.count["target"] = multiworld.random.randint(block.count["min"],
                                                                     block.count["max"])

            if not block.count["target"]:
                removed.append(block)

        for block in removed:
            multiworld.plando_item_blocks[player].remove(block)


def distribute_planned_blocks(multiworld: MultiWorld, plando_blocks: list[PlandoItemBlock]):
    def warn(warning: str, force: bool | str) -> None:
        if isinstance(force, bool):
            logging.warning(f"{warning}")
        else:
            logging.debug(f"{warning}")

    def failed(warning: str, force: bool | str) -> None:
        if force is True:
            raise Exception(warning)
        else:
            warn(warning, force)

    # shuffle, but then sort blocks by number of locations minus number of items,
    # so less-flexible blocks get priority
    multiworld.random.shuffle(plando_blocks)
    plando_blocks.sort(key=lambda block: (len(block.resolved_locations) - block.count["target"]
                                          if len(block.resolved_locations) > 0
                                          else len(multiworld.get_unfilled_locations(block.player)) -
                                          block.count["target"]))
    for placement in plando_blocks:
        player = placement.player
        try:
            worlds = placement.worlds
            locations = placement.resolved_locations
            items = placement.items
            maxcount = placement.count["target"]
            from_pool = placement.from_pool

            item_candidates = []
            if from_pool:
                instances = [item for item in multiworld.itempool if item.player == player and item.name in items]
                for item in multiworld.random.sample(items, maxcount):
                    candidate = next((i for i in instances if i.name == item), None)
                    if candidate is None:
                        warn(f"Could not remove {item} from pool for {multiworld.player_name[player]} as "
                             f"it's already missing from it", placement.force)
                        candidate = multiworld.worlds[player].create_item(item)
                    else:
                        multiworld.itempool.remove(candidate)
                        instances.remove(candidate)
                    item_candidates.append(candidate)
            else:
                item_candidates = [multiworld.worlds[player].create_item(item)
                                   for item in multiworld.random.sample(items, maxcount)]
            if any(item.code is None for item in item_candidates) \
               and not all(item.code is None for item in item_candidates):
                failed(f"Plando block for player {player} ({multiworld.player_name[player]}) contains both "
                       f"event items and non-event items. "
                       f"Event items: {[item for item in item_candidates if item.code is None]}, "
                       f"Non-event items: {[item for item in item_candidates if item.code is not None]}",
                       placement.force)
                continue
            else:
                is_real = item_candidates[0].code is not None
            candidates = [candidate for candidate in locations if candidate.item is None
                          and bool(candidate.address) == is_real]
            multiworld.random.shuffle(candidates)
            allstate = multiworld.get_all_state(False)
            mincount = placement.count["min"]
            allowed_margin = len(item_candidates) - mincount
            fill_restrictive(multiworld, allstate, candidates, item_candidates, lock=True,
                             allow_partial=True, name="Plando Main Fill")

            if len(item_candidates) > allowed_margin:
                failed(f"Could not place {len(item_candidates)} "
                       f"of {mincount + allowed_margin} item(s) "
                       f"for {multiworld.player_name[player]}, "
                       f"remaining items: {item_candidates}",
                       placement.force)
            if from_pool:
                multiworld.itempool.extend([item for item in item_candidates if item.code is not None])
        except Exception as e:
            raise Exception(
                f"Error running plando for player {player} ({multiworld.player_name[player]})") from e
