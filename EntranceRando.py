import functools
import queue
import random
from dataclasses import dataclass
from enum import IntEnum
from typing import Set, Tuple, List, Dict, Iterable, Callable, Union

from BaseClasses import Region, Entrance, CollectionState
from worlds.AutoWorld import World


class ERType(IntEnum):
    ONE_WAY = 1
    TWO_WAY = 2


class EntranceLookup:
    class GroupLookup:
        _lookup: Dict[str, List[Entrance]]

        def __init__(self):
            self._lookup = {}

        def __bool__(self):
            return bool(self._lookup)

        def add(self, entrance: Entrance) -> None:
            group = self._lookup.setdefault(entrance.er_group, [])
            group.append(entrance)

        def remove(self, entrance: Entrance) -> None:
            group = self._lookup.setdefault(entrance.er_group)
            group.remove(entrance)

        def __getitem__(self, item: str) -> List[Entrance]:
            return self._lookup.get(item, [])

    rng: random.Random
    dead_ends: GroupLookup
    others: GroupLookup

    def __init__(self, rng: random.Random):
        self.rng = rng
        self.dead_ends = EntranceLookup.GroupLookup()
        self.others = EntranceLookup.GroupLookup()

    @staticmethod
    @functools.cache
    def _is_dead_end(entrance: Entrance):
        """
        Checks whether a entrance is an unconditional dead end, that is, no matter what you have,
        it will never lead to new randomizable exits.
        """

        # obviously if this is an unpaired exit, then leads to unpaired exits!
        if not entrance.connected_region:
            return False
        # if the connected region has no exits, it's a dead end. otherwise its exits must all be dead ends.
        return not entrance.connected_region.exits or all(EntranceLookup._is_dead_end(exit)
                                                          for exit in entrance.connected_region.exits
                                                          if exit.name != entrance.name)

    def add(self, entrance: Entrance) -> None:
        lookup = self.dead_ends if self._is_dead_end(entrance) else self.others
        lookup.add(entrance)

    def remove(self, entrance: Entrance) -> None:
        lookup = self.dead_ends if self._is_dead_end(entrance) else self.others
        lookup.remove(entrance)

    def get_targets(
            self,
            groups: Iterable[str],
            dead_end: bool,
            preserve_group_order: bool
        ) -> Iterable[Entrance]:

        lookup = self.dead_ends if dead_end else self.others
        if preserve_group_order:
            for group in groups:
                self.rng.shuffle(lookup[group])
            ret = [entrance for group in groups for entrance in lookup[group]]
        else:
            ret = [entrance for group in groups for entrance in lookup[group]]
            self.rng.shuffle(ret)
        return ret


class ERPlacementState:
    # candidate exits to try and place right now!
    _placeable_exits: Set[Entrance]
    # exits that are gated by some unmet requirement (either they are not valid source transitions yet
    # or they are static connections with unmet logic restrictions)
    _pending_exits: Set[Entrance]

    placed_regions: Set[Region]
    placements: List[Entrance]
    pairings: List[Tuple[str, str]]
    world: World
    collection_state: CollectionState
    coupled: bool

    def __init__(self, world: World, coupled: bool):
        self._placeable_exits = set()
        self._pending_exits = set()

        self.placed_regions = set()
        self.placements = []
        self.pairings = []
        self.world = world
        self.collection_state = world.multiworld.get_all_state(True)
        self.coupled = coupled

    def has_placeable_exits(self) -> bool:
        return bool(self._placeable_exits)

    def place(self, start: Union[Region, Entrance]) -> None:
        """
        Traverses a region's connected exits to find any newly available randomizable
        exits which stem from that region.

        :param start: The starting region or entrance to traverse from.
        """

        q = queue.Queue[Region]()
        starting_entrance_name = None
        if isinstance(start, Entrance):
            starting_entrance_name = start.name
            q.put(start.parent_region)
        else:
            q.put(start)

        while q:
            region = q.get()
            if region in self.placed_regions:
                continue
            self.placed_regions.add(region)
            # collect events
            local_locations = self.world.multiworld.get_locations(self.world.player)
            self.collection_state.sweep_for_events(locations=local_locations)
            # traverse exits
            for exit in region.exits:
                # if the exit is unconnected, it's a candidate for randomization
                if not exit.connected_region:
                    # in coupled, the reverse transition will be handled specially;
                    # don't add it as a candidate. in uncoupled it's fair game.
                    if not self.coupled or exit.name != starting_entrance_name:
                        if exit.is_valid_source_transition(self):
                            self._placeable_exits.add(exit)
                        else:
                            self._pending_exits.add(exit)
                elif exit.connected_region not in self.placed_regions:
                    # traverse unseen static connections
                    if exit.can_reach(self.collection_state):
                        q.put(exit)
                    else:
                        self._pending_exits.add(exit)

    def sweep_pending_exits(self) -> None:
        """
        Checks if any exits which previously had unmet restrictions now have those restrictions met,
        and marks them for placement or places them depending on whether they are randomized or not.
        """
        no_longer_pending_exits = []
        for exit in self._pending_exits:
            if exit.connected_region and exit.can_reach(self.collection_state):
                # this is an unrandomized entrance, so place it and propagate
                self.place(exit.connected_region)
                no_longer_pending_exits.append(exit)
            elif not exit.connected_region and exit.is_valid_source_transition(self):
                # this is randomized so mark it eligible for placement
                self._placeable_exits.add(exit)
                no_longer_pending_exits.append(exit)
        self._pending_exits.difference_update(no_longer_pending_exits)

    def _connect_one_way(self, source_exit: Entrance, target_entrance: Entrance) -> None:
        target_region = target_entrance.connected_region

        target_region.entrances.remove(target_entrance)
        source_exit.connect(target_region)
        self.placements.append(source_exit)
        self.pairings.append((source_exit.name, target_entrance.name))

    def connect(self, source_exit: Entrance, target_entrance: Entrance) -> Iterable[Entrance]:
        """
        Connects a source exit to a target entrance in the graph, accounting for coupling

        :returns: The dummy entrance(s) which were removed from the graph
        """
        source_region = source_exit.parent_region
        target_region = target_entrance.connected_region

        self._connect_one_way(source_exit, target_entrance)
        # if we're doing coupled randomization place the reverse transition as well.
        if self.coupled and source_exit.er_type == ERType.TWO_WAY:
            # todo - better exceptions here
            for reverse_entrance in source_region.entrances:
                if reverse_entrance.name == source_exit.name:
                    break
            else:
                raise Exception(f'Two way exit {source_exit.name} had no corresponding entrance in '
                                f'{source_exit.parent_region.name}')
            for reverse_exit in target_region.exits:
                if reverse_exit.name == target_entrance.name:
                    break
            else:
                raise Exception(f'Two way entrance {target_entrance.name} had no corresponding exit in '
                                f'{target_region.name}')
            self._connect_one_way(reverse_exit, reverse_entrance)
            return [target_entrance, reverse_entrance]
        return [target_entrance]


def randomize_entrances(
        world: World,
        rng: random.Random,
        regions: Iterable[Region],
        coupled: bool,
        get_target_groups: Callable[[str], List[str]],
        preserve_group_order: bool = False
    ) -> ERPlacementState:
    """
    Randomizes Entrances for a single world in the multiworld. This should usually be
    called in pre_fill or possibly set_rules if you know what you're doing.

    Preconditions:
    1. All of your Regions and all of their exits have been created.
    2. Placeholder entrances have been created as the targets of randomization
       (each exit will be randomly paired to an entrance). <explain methods to do this>
    3. Your Menu region is connected to your starting region
    4. All the region connections you don't want to randomize are connected; usually this
       is connecting regions within a "scene" but may also include plando'd transitions.
    5. Access rules are set on all relevant region exits
    6. All event items and locations have been placed with access rules applied.
    7. All non-event items have been added to the item pool.

    Postconditions:
    1. All randomizable Entrances will be connected
    2. All placeholder entrances to regions will have been removed.
    """
    state = ERPlacementState(world, coupled)
    # exits which had no candidate exits found in the non-dead-end stage.
    # they will never be placeable until we start placing dead ends so
    # hold them here and stop trying.
    unplaceable_exits: List[Entrance] = []

    entrance_lookup = EntranceLookup(rng)

    for region in regions:
        for entrance in region.entrances:
            if not entrance.parent_region:
                entrance_lookup.add(entrance)

    # place the menu region and connected start region(s)
    state.place(world.multiworld.get_region('Menu', world.player))

    while state.has_placeable_exits() and entrance_lookup.others:
        # todo - this access to placeable_exits is ugly
        # todo - this should iterate placeable exits instead of immediately
        #        giving up; can_connect_to may be stateful
        # todo - this doesn't prioritize placing new rooms like the original did;
        #        that's problematic because early loops would lead to failures
        # this is needed to reduce bias; otherwise newer exits are prioritized
        rng.shuffle(state._placeable_exits)
        source_exit = state._placeable_exits.pop()

        target_groups = get_target_groups(source_exit.er_group)
        # anything can connect to the default group - if people don't like it the fix is to
        # assign a non-default group
        target_groups.append('Default')
        for target_entrance in entrance_lookup.get_targets(target_groups, False, preserve_group_order):
            if source_exit.can_connect_to(target_entrance, state):
                # we found a valid, connectable target entrance. We'll connect it in a moment
                break
        else:
            # there were no valid non-dead-end targets for this source, so give up on it for now
            unplaceable_exits.append(source_exit)
            continue

        # place the new pairing
        state.place(target_entrance)
        removed_entrances = state.connect(source_exit, target_entrance)
        state.sweep_pending_exits()
        # remove paired entrances from the lookup so they don't get re-randomized
        for entrance in removed_entrances:
            entrance_lookup.remove(entrance)

    if entrance_lookup.others:
        # this is generally an unsalvagable failure, we would need to implement swap earlier in the process
        # to prevent it. A stateful can_connect_to implementation may make this recoverable in some worlds as well.
        # why? there are no placeable exits, which means none of them have valid targets, and conversely
        # none of the existing targets can pair to the existing sources. Since dead ends will never add new sources
        # this means the current targets can never be paired (in most cases)
        # todo - investigate ways to prevent this case
        raise Exception("Unable to place all non-dead-end entrances with available source exits")

    # anything we couldn't place before might be placeable now
    state._placeable_exits.union(unplaceable_exits)
    unplaceable_exits.clear()

    # repeat the above but try to place dead ends
    while state.has_placeable_exits() and entrance_lookup.others:
        rng.shuffle(state._placeable_exits)
        source_exit = state._placeable_exits.pop()

        target_groups = get_target_groups(source_exit.er_group)
        target_groups.append('Default')
        for target_entrance in entrance_lookup.get_targets(target_groups, True, preserve_group_order):
            if source_exit.can_connect_to(target_entrance, state):
                # we found a valid, connectable target entrance. We'll connect it in a moment
                break
        else:
            # there were no valid dead-end targets for this source, so give up
            # todo - similar to above we should try and prevent this state.
            #        also it can_connect_to may be stateful.
            raise Exception("Unable to place all dead-end entrances with available source exits")

        # place the new pairing
        state.place(target_entrance)
        removed_entrances = state.connect(source_exit, target_entrance)
        state.sweep_pending_exits()
        # remove paired entrances from the lookup so they don't get re-randomized
        for entrance in removed_entrances:
            entrance_lookup.remove(entrance)

    if state.has_placeable_exits():
        raise Exception("There are more exits than entrances")

    return state
