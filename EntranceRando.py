import itertools
import random
from collections import deque
from typing import Callable, Dict, Iterable, List, Optional, Set, Tuple, Union

from BaseClasses import CollectionState, Entrance, Region
from worlds.AutoWorld import World


class EntranceLookup:
    class GroupLookup:
        _lookup: Dict[str, List[Entrance]]

        def __init__(self):
            self._lookup = {}

        def __bool__(self):
            return bool(self._lookup)

        def __getitem__(self, item: str) -> List[Entrance]:
            return self._lookup.get(item, [])

        def __iter__(self):
            return itertools.chain.from_iterable(self._lookup.values())

        def __str__(self):
            return str(self._lookup)

        def __repr__(self):
            return self.__str__()

        def add(self, entrance: Entrance) -> None:
            self._lookup.setdefault(entrance.er_group, []).append(entrance)

        def remove(self, entrance: Entrance) -> None:
            group = self._lookup.get(entrance.er_group, [])
            group.remove(entrance)
            if not group:
                del self._lookup[entrance.er_group]

    dead_ends: GroupLookup
    others: GroupLookup
    _random: random.Random
    _leads_to_exits_cache: Dict[Entrance, bool]

    def __init__(self, rng: random.Random):
        self.dead_ends = EntranceLookup.GroupLookup()
        self.others = EntranceLookup.GroupLookup()
        self._random = rng
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

            for exit_ in region.exits:
                # randomizable and not the reverse of the start entrance
                if not exit_.connected_region and exit_.name != entrance.name:
                    self._leads_to_exits_cache[entrance] = True
                    return True
                elif exit_.connected_region and exit_.connected_region not in visited:
                    q.append(exit_.connected_region)

        self._leads_to_exits_cache[entrance] = False
        return False

    def add(self, entrance: Entrance) -> None:
        lookup = self.others if self._can_lead_to_randomizable_exits(entrance) else self.dead_ends
        lookup.add(entrance)

    def remove(self, entrance: Entrance) -> None:
        lookup = self.others if self._can_lead_to_randomizable_exits(entrance) else self.dead_ends
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
                self._random.shuffle(lookup[group])
            ret = [entrance for group in groups for entrance in lookup[group]]
        else:
            ret = [entrance for group in groups for entrance in lookup[group]]
            self._random.shuffle(ret)
        return ret


class ERPlacementState:
    placeable_exits: List[Entrance]
    """candidate exits to try and place right now"""
    _pending_exits: List[Entrance]
    """exits that are gated by some unmet requirement"""
    # (either they are not valid source transitions yet or they are static connections with unmet logic restrictions)

    placed_regions: Set[Region]
    placements: List[Entrance]
    pairings: List[Tuple[str, str]]
    world: World
    collection_state: CollectionState
    coupled: bool

    def __init__(self, world: World, coupled: bool):
        self.placeable_exits = []
        self._pending_exits = []

        self.placed_regions = set()
        self.placements = []
        self.pairings = []
        self.world = world
        self.collection_state = world.multiworld.get_all_state(False, True)
        self.coupled = coupled

    @property
    def has_placeable_exits(self) -> bool:
        return bool(self.placeable_exits)

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
            for exit_ in region.exits:
                # if the exit is unconnected, it's a candidate for randomization
                if not exit_.connected_region:
                    # in coupled, the reverse transition will be handled specially;
                    # don't add it as a candidate. in uncoupled it's fair game.
                    if not self.coupled or exit_.name != starting_entrance_name:
                        if exit_.is_valid_source_transition(self):
                            self.placeable_exits.append(exit_)
                        else:
                            self._pending_exits.append(exit_)
                elif exit_.connected_region not in self.placed_regions:
                    # traverse unseen static connections
                    if exit_.can_reach(self.collection_state):
                        q.append(exit_.connected_region)
                    else:
                        self._pending_exits.append(exit_)

    def sweep_pending_exits(self) -> None:
        """
        Checks if any exits which previously had unmet restrictions now have those restrictions met,
        and marks them for placement or places them depending on whether they are randomized or not.
        """
        size = len(self._pending_exits)
        # iterate backwards so that removing items doesn't mess with indices of unprocessed items
        for j, exit_ in enumerate(reversed(self._pending_exits)):
            i = size - j - 1
            if exit_.connected_region and exit_.can_reach(self.collection_state):
                # this is an unrandomized entrance, so place it and propagate
                self.place(exit_.connected_region)
                self._pending_exits.pop(i)
            elif not exit_.connected_region and exit_.is_valid_source_transition(self):
                # this is randomized so mark it eligible for placement
                self.placeable_exits.append(exit_)
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
        if self.coupled and source_exit.er_type == Entrance.EntranceType.TWO_WAY:
            # TODO - better exceptions here
            for reverse_entrance in source_region.entrances:
                if reverse_entrance.name == source_exit.name:
                    if reverse_entrance.parent_region:
                        raise Exception("This is very bad")
                    break
            else:
                raise Exception(f"Two way exit {source_exit.name} had no corresponding entrance in "
                                f"{source_exit.parent_region.name}")
            for reverse_exit in target_region.exits:
                if reverse_exit.name == target_entrance.name:
                    if reverse_exit.connected_region:
                        raise Exception("this is very bad")
                    break
            else:
                raise Exception(f"Two way entrance {target_entrance.name} had no corresponding exit in "
                                f"{target_region.name}")
            self._connect_one_way(reverse_exit, reverse_entrance)
            # the reverse exit might be in the placeable list so clear that to prevent re-randomization
            try:
                self.placeable_exits.remove(reverse_exit)
            except ValueError:
                pass
            return [target_entrance, reverse_entrance]
        return [target_entrance]


def randomize_entrances(
        world: World,
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

    Post-conditions:
    1. All randomizable Entrances will be connected
    2. All placeholder entrances to regions will have been removed.

    :param world: Your World instance
    :param regions: Regions with no connected entrances that you would like to be randomly connected
    :param coupled: Whether connected entrances should be coupled to go in both directions
    :param get_target_groups: Method to call that returns the groups that a specific group type is allowed to connect to
    :param preserve_group_order: Whether the order of groupings should be preserved for the returned target_groups
    """
    er_state = ERPlacementState(world, coupled)
    entrance_lookup = EntranceLookup(world.random)

    def find_pairing(dead_end: bool, require_new_regions: bool) -> Optional[Tuple[Entrance, Entrance]]:
        for source_exit in er_state.placeable_exits:
            target_groups = get_target_groups(source_exit.er_group)
            # anything can connect to the default group - if people don't like it the fix is to
            # assign a non-default group
            if "Default" not in target_groups:
                target_groups.append("Default")
            for target_entrance in entrance_lookup.get_targets(target_groups, dead_end, preserve_group_order):
                # TODO - requiring new regions is a proxy for requiring new entrances to be unlocked, which is
                #        not quite full fidelity so we may need to revisit this in the future
                region_requirement_satisfied = (not require_new_regions
                                                or target_entrance.connected_region not in er_state.placed_regions)
                if region_requirement_satisfied and source_exit.can_connect_to(target_entrance, er_state):
                    return source_exit, target_entrance
        else:
            # no source exits had any valid target so this stage is deadlocked. swap may be implemented if early
            # deadlocking is a frequent issue.
            lookup = entrance_lookup.dead_ends if dead_end else entrance_lookup.others

            # if we're in a stage where we're trying to get to new regions, we could also enter this
            # branch in a success state (when all regions of the preferred type have been placed, but there are still
            # additional unplaced entrances into those regions)
            if require_new_regions:
                if all(e.connected_region in er_state.placed_regions for e in lookup):
                    return None

            raise Exception(f"None of the available entrances had valid targets.\n"
                            f"Available exits: {er_state.placeable_exits}\n"
                            f"Available entrances: {lookup}")

    def do_placement(source_exit: Entrance, target_entrance: Entrance):
        removed_entrances = er_state.connect(source_exit, target_entrance)
        # remove the paired items from consideration
        er_state.placeable_exits.remove(source_exit)
        for entrance in removed_entrances:
            entrance_lookup.remove(entrance)
        # place and propagate
        er_state.place(target_entrance)
        er_state.sweep_pending_exits()

    for region in regions:
        for entrance in region.entrances:
            if not entrance.parent_region:
                entrance_lookup.add(entrance)

    # place the menu region and connected start region(s)
    er_state.place(world.multiworld.get_region("Menu", world.player))

    # stage 1 - try to place all the non-dead-end entrances
    while entrance_lookup.others:
        # TODO - this access to placeable_exits is ugly
        #  this is needed to reduce bias; otherwise newer exits are prioritized
        world.random.shuffle(er_state.placeable_exits)
        pairing = find_pairing(False, True)
        if not pairing:
            break
        do_placement(*pairing)
    # stage 2 - try to place all the dead-end entrances
    while entrance_lookup.dead_ends:
        world.random.shuffle(er_state.placeable_exits)
        pairing = find_pairing(True, True)
        if not pairing:
            break
        do_placement(*pairing)
    # TODO - stages 3 and 4 should ideally run "together"; i.e. without respect to dead-endedness
    #        as we are just trying to tie off loose ends rather than get you somewhere new
    # stage 3 - connect any dangling entrances that remain
    while entrance_lookup.others:
        world.random.shuffle(er_state.placeable_exits)
        pairing = find_pairing(False, False)
        do_placement(*pairing)
    # stage 4 - last chance for dead ends
    while entrance_lookup.dead_ends:
        world.random.shuffle(er_state.placeable_exits)
        pairing = find_pairing(True, False)
        do_placement(*pairing)

    return er_state
