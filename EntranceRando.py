import itertools
import logging
import random
import time
from collections import deque
from typing import Callable, Dict, Iterable, List, Tuple, Union, Set, Optional

from BaseClasses import CollectionState, Entrance, Region, EntranceType
from Options import Accessibility
from worlds.AutoWorld import World


class EntranceRandomizationError(RuntimeError):
    pass


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
    placements: List[Entrance]
    pairings: List[Tuple[str, str]]
    world: World
    collection_state: CollectionState
    coupled: bool

    def __init__(self, world: World, coupled: bool):
        self.placements = []
        self.pairings = []
        self.world = world
        self.collection_state = world.multiworld.get_all_state(False, True)
        self.coupled = coupled

    @property
    def placed_regions(self) -> Set[Region]:
        return self.collection_state.reachable_regions[self.world.player]

    def find_placeable_exits(self, check_validity: bool) -> List[Entrance]:
        blocked_connections = self.collection_state.blocked_connections[self.world.player]
        blocked_connections = sorted(blocked_connections, key=lambda x: x.name)
        placeable_randomized_exits = [connection for connection in blocked_connections
                                      if not connection.connected_region
                                      and (not check_validity or connection.is_valid_source_transition(self))]
        self.world.random.shuffle(placeable_randomized_exits)
        return placeable_randomized_exits

    def _connect_one_way(self, source_exit: Entrance, target_entrance: Entrance) -> None:
        target_region = target_entrance.connected_region

        target_region.entrances.remove(target_entrance)
        source_exit.connect(target_region)

        self.collection_state.stale[self.world.player] = True
        self.placements.append(source_exit)
        self.pairings.append((source_exit.name, target_entrance.name))

    def connect(
            self,
            source_exit: Entrance,
            target_entrance: Entrance
    ) -> Tuple[Iterable[Entrance], Iterable[Entrance]]:
        """
        Connects a source exit to a target entrance in the graph, accounting for coupling

        :returns: The newly placed exits and the dummy entrance(s) which were removed from the graph
        """
        source_region = source_exit.parent_region
        target_region = target_entrance.connected_region

        self._connect_one_way(source_exit, target_entrance)
        # if we're doing coupled randomization place the reverse transition as well.
        if self.coupled and source_exit.er_type == EntranceType.TWO_WAY:
            for reverse_entrance in source_region.entrances:
                if reverse_entrance.name == source_exit.name:
                    if reverse_entrance.parent_region:
                        raise EntranceRandomizationError(
                            f"Could not perform coupling on {source_exit.name} -> {target_entrance.name} "
                            f"because the reverse entrance is already parented to "
                            f"{reverse_entrance.parent_region.name}.")
                    break
            else:
                raise EntranceRandomizationError(f"Two way exit {source_exit.name} had no corresponding entrance in "
                                                 f"{source_exit.parent_region.name}")
            for reverse_exit in target_region.exits:
                if reverse_exit.name == target_entrance.name:
                    if reverse_exit.connected_region:
                        raise EntranceRandomizationError(
                            f"Could not perform coupling on {source_exit.name} -> {target_entrance.name} "
                            f"because the reverse exit is already connected to "
                            f"{reverse_exit.connected_region.name}.")
                    break
            else:
                raise EntranceRandomizationError(f"Two way entrance {target_entrance.name} had no corresponding exit "
                                                 f"in {target_region.name}.")
            self._connect_one_way(reverse_exit, reverse_entrance)
            return (source_exit, reverse_exit), (target_entrance, reverse_entrance)
        return (source_exit,), (target_entrance,)


def disconnect_entrance_for_randomization(entrance: Entrance, target_group: Optional[str] = None) -> None:
    """
    Given an entrance in a "vanilla" region graph, splits that entrance to prepare it for randomization
    in randomize_entrances. Specifically that means the entrance will be disconnected from its
    connected region and a corresponding ER target will be created in a way that can respect coupled randomization
    requirements for 2 way transitions (assuming that this is called on both sides of the vanilla 2 way).
    
    Preconditions:
    1. The entrance has both a parent and child region (ie, it is fully connected)
    2. The entrance has already been labeled with the appropriate entrance type

    :param entrance: The entrance which will be disconnected in preparation for randomization.
    :param target_group: The group to assign to the created ER target. If not specified, the group from
                         the original entrance will be copied.
    """
    child_region = entrance.connected_region
    parent_region = entrance.parent_region

    # disconnect the edge
    child_region.entrances.remove(entrance)
    entrance.connected_region = None

    # create the needed ER target
    if entrance.er_type == EntranceType.TWO_WAY:
        # for 2-ways, create a target in the parent region with a matching name to support coupling.
        # targets in the child region will be created when the other direction edge is disconnected
        target = parent_region.create_er_target(entrance.name)
    else:
        # for 1-ways, the child region needs a target and coupling/naming is not a concern
        target = child_region.create_er_target(child_region.name)
    target.er_type = entrance.er_type
    target.er_group = target_group or entrance.er_group


def randomize_entrances(
        world: World,
        coupled: bool,
        get_target_groups: Callable[[str], List[str]],
        preserve_group_order: bool = False,
        on_connect: Optional[Callable[[ERPlacementState, Iterable[Entrance]], None]] = None
) -> ERPlacementState:
    """
    Randomizes Entrances for a single world in the multiworld.

    Depending on how your world is configured, this may be called as early as create_regions or
    need to be called as late as pre_fill. In general, earlier is better; the best time to
    randomize entrances is as soon as the preconditions are fulfilled.

    Preconditions:
    1. All of your Regions and all of their exits have been created.
    2. Placeholder entrances have been created as the targets of randomization
       (each exit will be randomly paired to an entrance). There are 2 primary ways to do this:
       * Pre-place your unrandomized region graph, then use disconnect_entrances_for_randomization
         to prepare them, or
       * Manually prepare your entrances for randomization. Exits to be randomized should be created
         and left without a connected region. There should be an equal number of matching dummy
         entrances of each entrance type in the region graph which do not have a parent; these can
         easily be created with region.create_er_target(). If you plan to use coupled randomization, the names
         of these placeholder entrances matter and should exactly match the name of the corresponding exit in
         that region. For example, given regions R1 and R2 connected R1 --[E1]-> R2 and R2 --[E2]-> R1 when
         unrandomized, then the expected inputs to coupled ER would be the following (the names of the ER targets
         for one-way transitions do not matter):
            * R1 --[E1]-> None
            * None --[E1]-> R1
            * R2 --[E2]-> None
            * None --[E2]-> R2
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
    :param coupled: Whether connected entrances should be coupled to go in both directions
    :param get_target_groups: Method to call that returns the groups that a specific group type is allowed to connect to
    :param preserve_group_order: Whether the order of groupings should be preserved for the returned target_groups
    :param on_connect: A callback function which allows specifying side effects after a placement is completed
                       successfully and the underlying collection state has been updated.
    """
    start_time = time.perf_counter()
    er_state = ERPlacementState(world, coupled)
    entrance_lookup = EntranceLookup(world.random)
    # similar to fill, skip validity checks on entrances if the game is beatable on minimal accessibility
    perform_validity_check = True

    def do_placement(source_exit: Entrance, target_entrance: Entrance):
        placed_exits, removed_entrances = er_state.connect(source_exit, target_entrance)
        # remove the placed targets from consideration
        for entrance in removed_entrances:
            entrance_lookup.remove(entrance)
        # propagate new connections
        er_state.collection_state.update_reachable_regions(world.player)
        if on_connect:
            on_connect(er_state, placed_exits)

    def find_pairing(dead_end: bool, require_new_regions: bool) -> bool:
        nonlocal perform_validity_check
        placeable_exits = er_state.find_placeable_exits(perform_validity_check)
        for source_exit in placeable_exits:
            target_groups = get_target_groups(source_exit.er_group)
            # anything can connect to the default group - if people don't like it the fix is to
            # assign a non-default group
            if "Default" not in target_groups:
                target_groups.append("Default")
            for target_entrance in entrance_lookup.get_targets(target_groups, dead_end, preserve_group_order):
                # requiring a new region is a proxy for enforcing new entrances are added, thus growing the search
                # space. this is not quite a full fidelity conversion, but doesn't seem to cause issues enough
                # to do more complex checks
                region_requirement_satisfied = (not require_new_regions
                                                or target_entrance.connected_region not in er_state.placed_regions)
                if region_requirement_satisfied and source_exit.can_connect_to(target_entrance, er_state):
                    do_placement(source_exit, target_entrance)
                    return True
        else:
            # no source exits had any valid target so this stage is deadlocked. swap may be implemented if early
            # deadlocking is a frequent issue.
            lookup = entrance_lookup.dead_ends if dead_end else entrance_lookup.others

            # if we're in a stage where we're trying to get to new regions, we could also enter this
            # branch in a success state (when all regions of the preferred type have been placed, but there are still
            # additional unplaced entrances into those regions)
            if require_new_regions:
                if all(e.connected_region in er_state.placed_regions for e in lookup):
                    return False

            # if we're on minimal accessibility and can guarantee the game is beatable,
            # we can prevent a failure by bypassing future validity checks. this check may be
            # expensive; fortunately we only have to do it once
            if perform_validity_check and world.options.accessibility == Accessibility.option_minimal \
                    and world.multiworld.has_beaten_game(er_state.collection_state, world.player):
                # ensure that we have enough locations to place our progression
                accessible_location_count = 0
                prog_item_count = len(er_state.collection_state.prog_items[world.player])
                for region in er_state.placed_regions:
                    for loc in region.locations:
                        if loc.can_reach(er_state.collection_state):
                            accessible_location_count += 1
                            if accessible_location_count >= prog_item_count:
                                perform_validity_check = False
                                # pretend that this was successful to retry the current stage
                                return True

            raise EntranceRandomizationError(
                f"None of the available entrances are valid targets for the available exits.\n"
                f"Available entrances: {lookup}\n"
                f"Available exits: {placeable_exits}")

    er_targets = (entrance for region in world.multiworld.get_regions(world.player)
                  for entrance in region.entrances if not entrance.parent_region)
    for entrance in er_targets:
        entrance_lookup.add(entrance)

    # place the menu region and connected start region(s)
    er_state.collection_state.update_reachable_regions(world.player)

    # stage 1 - try to place all the non-dead-end entrances
    while entrance_lookup.others:
        if not find_pairing(False, True):
            break
    # stage 2 - try to place all the dead-end entrances
    while entrance_lookup.dead_ends:
        if not find_pairing(True, True):
            break
    # stage 3 - connect any dangling entrances that remain
    while entrance_lookup.others:
        find_pairing(False, False)
    # stage 4 - last chance for dead ends
    while entrance_lookup.dead_ends:
        find_pairing(True, False)

    running_time = time.perf_counter() - start_time
    if running_time > 1.0:
        logging.info(f"Took {running_time:.4f} seconds during entrance randomization for player {world.player},"
                     f"named {world.multiworld.player_name[world.player]}")

    return er_state
