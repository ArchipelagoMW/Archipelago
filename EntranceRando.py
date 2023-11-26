import functools
import queue
import random
from collections import deque
from typing import Set, Tuple, List, Dict, Iterable, Callable, Union, Optional

from BaseClasses import Region, Entrance, CollectionState
from worlds.AutoWorld import World


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
            group = self._lookup.get(entrance.er_group, [])
            group.remove(entrance)
            if not group:
                del self._lookup[entrance.er_group]

        def __getitem__(self, item: str) -> List[Entrance]:
            return self._lookup.get(item, [])

    rng: random.Random
    dead_ends: GroupLookup
    others: GroupLookup
    _leads_to_exits_cache: Dict[Entrance, bool]

    def __init__(self, rng: random.Random):
        self.rng = rng
        self.dead_ends = EntranceLookup.GroupLookup()
        self.others = EntranceLookup.GroupLookup()
        self._leads_to_exits_cache = {}

    def _can_lead_to_randomizable_exits(self, entrance: Entrance):
        """
        Checks whether an entrance is able to lead to another randomizable exit
        with some combination of items

        :param entrance: A randomizable (no parent) region entrance
        """
        # we've seen this, return cached result
        if entrance in self._leads_to_exits_cache:
            return self._leads_to_exits_cache[entrance]

        visited = set()
        q = deque()
        q.append(entrance.connected_region)

        while q:
            region = q.popleft()
            visited.add(region)

            for exit in region.exits:
                # randomizable and not the reverse of the start entrance
                if not exit.connected_region and exit.name != entrance.name:
                    self._leads_to_exits_cache[entrance] = True
                    return True
                elif exit.connected_region and exit.connected_region not in visited:
                    q.append(exit.connected_region)

        self._leads_to_exits_cache[entrance] = False
        return False

    def add(self, entrance: Entrance) -> None:
        lookup = self.dead_ends if not self._can_lead_to_randomizable_exits(entrance) else self.others
        lookup.add(entrance)

    def remove(self, entrance: Entrance) -> None:
        lookup = self.dead_ends if not self._can_lead_to_randomizable_exits(entrance) else self.others
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
    _placeable_exits: List[Entrance]
    # exits that are gated by some unmet requirement (either they are not valid source transitions yet
    # or they are static connections with unmet logic restrictions)
    _pending_exits: List[Entrance]

    placed_regions: Set[Region]
    placements: List[Entrance]
    pairings: List[Tuple[str, str]]
    world: World
    collection_state: CollectionState
    coupled: bool

    def __init__(self, world: World, coupled: bool):
        self._placeable_exits = []
        self._pending_exits = []

        self.placed_regions = set()
        self.placements = []
        self.pairings = []
        self.world = world
        self.collection_state = world.multiworld.get_all_state(True, True)
        self.coupled = coupled

    def has_placeable_exits(self) -> bool:
        return bool(self._placeable_exits)

    def place(self, start: Union[Region, Entrance]) -> None:
        """
        Traverses a region's connected exits to find any newly available randomizable
        exits which stem from that region.

        :param start: The starting region or entrance to traverse from.
        """

        q = deque()
        starting_entrance_name = None
        if isinstance(start, Entrance):
            starting_entrance_name = start.name
            q.append(start.connected_region)
        else:
            q.append(start)

        while q:
            region = q.popleft()
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
                            self._placeable_exits.append(exit)
                        else:
                            self._pending_exits.append(exit)
                elif exit.connected_region not in self.placed_regions:
                    # traverse unseen static connections
                    if exit.can_reach(self.collection_state):
                        q.append(exit.connected_region)
                    else:
                        self._pending_exits.append(exit)

    def sweep_pending_exits(self) -> None:
        """
        Checks if any exits which previously had unmet restrictions now have those restrictions met,
        and marks them for placement or places them depending on whether they are randomized or not.
        """
        size = len(self._pending_exits)
        # iterate backwards so that removing items doesn't mess with indices of unprocessed items
        for j, exit in enumerate(reversed(self._pending_exits)):
            i = size - j - 1
            if exit.connected_region and exit.can_reach(self.collection_state):
                # this is an unrandomized entrance, so place it and propagate
                self.place(exit.connected_region)
                self._pending_exits.pop(i)
            elif not exit.connected_region and exit.is_valid_source_transition(self):
                # this is randomized so mark it eligible for placement
                self._placeable_exits.append(exit)
                self._pending_exits.pop(i)

    def _connect_one_way(self, source_exit: Entrance, target_entrance: Entrance) -> None:
        target_region = target_entrance.connected_region

        target_region.entrances.remove(target_entrance)
        source_exit.connect(target_region)

        self.collection_state.stale[self.world.player] = True
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
        if self.coupled and source_exit.er_type == Entrance.Type.TWO_WAY:
            # todo - better exceptions here
            for reverse_entrance in source_region.entrances:
                if reverse_entrance.name == source_exit.name:
                    if reverse_entrance.parent_region:
                        raise Exception("This is very bad")
                    break
            else:
                raise Exception(f'Two way exit {source_exit.name} had no corresponding entrance in '
                                f'{source_exit.parent_region.name}')
            for reverse_exit in target_region.exits:
                if reverse_exit.name == target_entrance.name:
                    if reverse_exit.connected_region:
                        raise Exception("this is very bad")
                    break
            else:
                raise Exception(f'Two way entrance {target_entrance.name} had no corresponding exit in '
                                f'{target_region.name}')
            self._connect_one_way(reverse_exit, reverse_entrance)
            # the reverse exit might be in the placeable list so clear that to prevent re-randomization
            try:
                self._placeable_exits.remove(reverse_exit)
            except ValueError:
                pass
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
    Randomizes Entrances for a single world in the multiworld.

    Depending on how your world is configured, this may be called as early as create_regions or
    need to be called as late as pre_fill. In general, earlier is better, ie the best time to
    randomize entrances is as soon as the preconditions are fulfilled.

    Preconditions:
    1. All of your Regions and all of their exits have been created.
    2. Placeholder entrances have been created as the targets of randomization
       (each exit will be randomly paired to an entrance). <explain methods to do this>
    3. All entrances and exits have been correctly labeled as 1 way or 2 way.
    4. Your Menu region is connected to your starting region.
    5. All the region connections you don't want to randomize are connected; usually this
       is connecting regions within a "scene" but may also include plando'd transitions.
    6. Access rules are set on all relevant region exits.
       * Access rules are used to conservatively prevent cases where, given a switch in region R_s
         and the gate that it opens being the exit E_g to region R_g, the only way to access R_s
         is through a connection R_g --(E_g)-> R_s, thus making R_s inaccessible. If you encode
         this kind of cross-region dependency through events or indirect connections, those must
         be placed/registered before calling this function if you want them to be respected.
       * If you set access rules that contain items other than events, those items must be added to
         the multiworld item pool before randomizing entrances.

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
        if 'Default' not in target_groups:
            target_groups.append('Default')
        for target_entrance in entrance_lookup.get_targets(target_groups, False, preserve_group_order):
            if source_exit.can_connect_to(target_entrance, state):
                # we found a valid, connectable target entrance. We'll connect it in a moment
                break
        else:
            # there were no valid non-dead-end targets for this source, so give up on it for now
            unplaceable_exits.append(source_exit)
            continue

        # place the new pairing. it is important to do connections first so that can_reach will function.
        removed_entrances = state.connect(source_exit, target_entrance)
        state.place(target_entrance)
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
        print("Unable to place all non-dead-end entrances with available source exits")
        return state  # this short circuts the exception for testing purposes in order to see how far ER got.
        raise Exception("Unable to place all non-dead-end entrances with available source exits")

    # anything we couldn't place before might be placeable now
    state._placeable_exits.extend(unplaceable_exits)
    unplaceable_exits.clear()

    # repeat the above but try to place dead ends
    while state.has_placeable_exits() and entrance_lookup.dead_ends:
        rng.shuffle(state._placeable_exits)
        source_exit = state._placeable_exits.pop()

        target_groups = get_target_groups(source_exit.er_group)
        # anything can connect to the default group - if people don't like it the fix is to
        # assign a non-default group
        if 'Default' not in target_groups:
            target_groups.append('Default')
        for target_entrance in entrance_lookup.get_targets(target_groups, True, preserve_group_order):
            if source_exit.can_connect_to(target_entrance, state):
                # we found a valid, connectable target entrance. We'll connect it in a moment
                break
        else:
            # there were no valid dead-end targets for this source, so give up
            # todo - similar to above we should try and prevent this state.
            #        also it can_connect_to may be stateful.
            print("Unable to place all dead-end entrances with available source exits")
            return state  # this short circuts the exception for testing purposes in order to see how far ER got.
            raise Exception("Unable to place all dead-end entrances with available source exits")

        # place the new pairing. it is important to do connections first so that can_reach will function.
        removed_entrances = state.connect(source_exit, target_entrance)
        state.place(target_entrance)
        state.sweep_pending_exits()
        # remove paired entrances from the lookup so they don't get re-randomized
        for entrance in removed_entrances:
            entrance_lookup.remove(entrance)

    if state.has_placeable_exits():
        raise Exception("There are more exits than entrances")

    return state
