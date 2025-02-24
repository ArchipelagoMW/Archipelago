import itertools
import logging
import random
import time
from collections import deque
from collections.abc import Callable, Iterable

from BaseClasses import CollectionState, Entrance, Region, EntranceType
from Options import Accessibility
from worlds.AutoWorld import World


class EntranceRandomizationError(RuntimeError):
    pass


class EntranceLookup:
    class GroupLookup:
        _lookup: dict[int, list[Entrance]]

        def __init__(self):
            self._lookup = {}

        def __len__(self):
            return sum(map(len, self._lookup.values()))

        def __bool__(self):
            return bool(self._lookup)

        def __getitem__(self, item: int) -> list[Entrance]:
            return self._lookup.get(item, [])

        def __iter__(self):
            return itertools.chain.from_iterable(self._lookup.values())

        def __repr__(self):
            return str(self._lookup)

        def add(self, entrance: Entrance) -> None:
            self._lookup.setdefault(entrance.randomization_group, []).append(entrance)

        def remove(self, entrance: Entrance) -> None:
            group = self._lookup[entrance.randomization_group]
            group.remove(entrance)
            if not group:
                del self._lookup[entrance.randomization_group]

    dead_ends: GroupLookup
    others: GroupLookup
    _random: random.Random
    _expands_graph_cache: dict[Entrance, bool]
    _coupled: bool

    def __init__(self, rng: random.Random, coupled: bool):
        self.dead_ends = EntranceLookup.GroupLookup()
        self.others = EntranceLookup.GroupLookup()
        self._random = rng
        self._expands_graph_cache = {}
        self._coupled = coupled

    def _can_expand_graph(self, entrance: Entrance) -> bool:
        """
        Checks whether an entrance is able to expand the region graph, either by
        providing access to randomizable exits or by granting access to items or
        regions used in logic conditions.

        :param entrance: A randomizable (no parent) region entrance
        """
        # we've seen this, return cached result
        if entrance in self._expands_graph_cache:
            return self._expands_graph_cache[entrance]

        visited = set()
        q: deque[Region] = deque()
        q.append(entrance.connected_region)

        while q:
            region = q.popleft()
            visited.add(region)

            # check if the region itself is progression
            if region in region.multiworld.indirect_connections:
                self._expands_graph_cache[entrance] = True
                return True

            # check if any placed locations are progression
            for loc in region.locations:
                if loc.advancement:
                    self._expands_graph_cache[entrance] = True
                    return True

            # check if there is a randomized exit out (expands the graph directly) or else search any connected
            # regions to see if they are/have progression
            for exit_ in region.exits:
                # randomizable exits which are not reverse of the incoming entrance.
                # uncoupled mode is an exception because in this case going back in the door you just came in could
                # actually lead somewhere new
                if not exit_.connected_region and (not self._coupled or exit_.name != entrance.name):
                    self._expands_graph_cache[entrance] = True
                    return True
                elif exit_.connected_region and exit_.connected_region not in visited:
                    q.append(exit_.connected_region)

        self._expands_graph_cache[entrance] = False
        return False

    def add(self, entrance: Entrance) -> None:
        lookup = self.others if self._can_expand_graph(entrance) else self.dead_ends
        lookup.add(entrance)

    def remove(self, entrance: Entrance) -> None:
        lookup = self.others if self._can_expand_graph(entrance) else self.dead_ends
        lookup.remove(entrance)

    def get_targets(
            self,
            groups: Iterable[int],
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

    def __len__(self):
        return len(self.dead_ends) + len(self.others)


class ERPlacementState:
    """The state of an ongoing or completed entrance randomization"""
    placements: list[Entrance]
    """The list of randomized Entrance objects which have been connected successfully"""
    pairings: list[tuple[str, str]]
    """A list of pairings of connected entrance names, of the form (source_exit, target_entrance)"""
    world: World
    """The world which is having its entrances randomized"""
    collection_state: CollectionState
    """The CollectionState backing the entrance randomization logic"""
    coupled: bool
    """Whether entrance randomization is operating in coupled mode"""

    def __init__(self, world: World, coupled: bool):
        self.placements = []
        self.pairings = []
        self.world = world
        self.coupled = coupled
        self.collection_state = world.multiworld.get_all_state(False, True)

    @property
    def placed_regions(self) -> set[Region]:
        return self.collection_state.reachable_regions[self.world.player]

    def find_placeable_exits(self, check_validity: bool) -> list[Entrance]:
        if check_validity:
            blocked_connections = self.collection_state.blocked_connections[self.world.player]
            blocked_connections = sorted(blocked_connections, key=lambda x: x.name)
            placeable_randomized_exits = [connection for connection in blocked_connections
                                          if not connection.connected_region
                                          and connection.is_valid_source_transition(self)]
        else:
            # this is on a beaten minimal attempt, so any exit anywhere is fair game
            placeable_randomized_exits = [ex for region in self.world.multiworld.get_regions(self.world.player)
                                          for ex in region.exits if not ex.connected_region]
        self.world.random.shuffle(placeable_randomized_exits)
        return placeable_randomized_exits

    def _connect_one_way(self, source_exit: Entrance, target_entrance: Entrance) -> None:
        target_region = target_entrance.connected_region

        target_region.entrances.remove(target_entrance)
        source_exit.connect(target_region)

        self.collection_state.stale[self.world.player] = True
        self.placements.append(source_exit)
        self.pairings.append((source_exit.name, target_entrance.name))

    def test_speculative_connection(self, source_exit: Entrance, target_entrance: Entrance) -> bool:
        copied_state = self.collection_state.copy()
        # simulated connection. A real connection is unsafe because the region graph is shallow-copied and would
        # propagate back to the real multiworld.
        copied_state.reachable_regions[self.world.player].add(target_entrance.connected_region)
        copied_state.blocked_connections[self.world.player].remove(source_exit)
        copied_state.blocked_connections[self.world.player].update(target_entrance.connected_region.exits)
        copied_state.update_reachable_regions(self.world.player)
        copied_state.sweep_for_advancements()
        # test that at there are newly reachable randomized exits that are ACTUALLY reachable
        available_randomized_exits = copied_state.blocked_connections[self.world.player]
        for _exit in available_randomized_exits:
            if _exit.connected_region:
                continue
            # ignore the source exit, and, if coupled, the reverse exit. They're not actually new
            if _exit.name == source_exit.name or (self.coupled and _exit.name == target_entrance.name):
                continue
            # technically this should be is_valid_source_transition, but that may rely on side effects from
            # on_connect, which have not happened here (because we didn't do a real connection, and if we did, we would
            # not want them to persist). can_reach is a close enough approximation most of the time.
            if _exit.can_reach(copied_state):
                return True
        return False

    def connect(
            self,
            source_exit: Entrance,
            target_entrance: Entrance
    ) -> tuple[list[Entrance], list[Entrance]]:
        """
        Connects a source exit to a target entrance in the graph, accounting for coupling

        :returns: The newly placed exits and the dummy entrance(s) which were removed from the graph
        """
        source_region = source_exit.parent_region
        target_region = target_entrance.connected_region

        self._connect_one_way(source_exit, target_entrance)
        # if we're doing coupled randomization place the reverse transition as well.
        if self.coupled and source_exit.randomization_type == EntranceType.TWO_WAY:
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
            return [source_exit, reverse_exit], [target_entrance, reverse_entrance]
        return [source_exit], [target_entrance]


def bake_target_group_lookup(world: World, get_target_groups: Callable[[int], list[int]]) \
        -> dict[int, list[int]]:
    """
    Applies a transformation to all known entrance groups on randomizable exists to build a group lookup table.

    :param world: Your World instance
    :param get_target_groups: Function to call that returns the groups that a specific group type is allowed to
                              connect to
    """
    unique_groups = { entrance.randomization_group for entrance in world.multiworld.get_entrances(world.player)
                      if entrance.parent_region and not entrance.connected_region }
    return { group: get_target_groups(group) for group in unique_groups }


def disconnect_entrance_for_randomization(entrance: Entrance, target_group: int | None = None) -> None:
    """
    Given an entrance in a "vanilla" region graph, splits that entrance to prepare it for randomization
    in randomize_entrances. This should be done after setting the type and group of the entrance.

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
    if entrance.randomization_type == EntranceType.TWO_WAY:
        # for 2-ways, create a target in the parent region with a matching name to support coupling.
        # targets in the child region will be created when the other direction edge is disconnected
        target = parent_region.create_er_target(entrance.name)
    else:
        # for 1-ways, the child region needs a target and coupling/naming is not a concern
        target = child_region.create_er_target(child_region.name)
    target.randomization_type = entrance.randomization_type
    target.randomization_group = target_group or entrance.randomization_group


def randomize_entrances(
        world: World,
        coupled: bool,
        target_group_lookup: dict[int, list[int]],
        preserve_group_order: bool = False,
        er_targets: list[Entrance] | None = None,
        exits: list[Entrance] | None = None,
        on_connect: Callable[[ERPlacementState, list[Entrance]], None] | None = None
) -> ERPlacementState:
    """
    Randomizes Entrances for a single world in the multiworld.

    :param world: Your World instance
    :param coupled: Whether connected entrances should be coupled to go in both directions
    :param target_group_lookup: Map from each group to a list of the groups that it can be connect to. Every group
                                used on an exit must be provided and must map to at least one other group. The default
                                group is 0.
    :param preserve_group_order: Whether the order of groupings should be preserved for the returned target_groups
    :param er_targets: The list of ER targets (Entrance objects with no parent region) to use for randomization.
                       Remember to be deterministic! If not provided, automatically discovers all valid targets
                       in your world.
    :param exits: The list of exits (Entrance objects with no target region) to use for randomization.
                  Remember to be deterministic! If not provided, automatically discovers all valid exits in your world.
    :param on_connect: A callback function which allows specifying side effects after a placement is completed
                       successfully and the underlying collection state has been updated.
    """
    if not world.explicit_indirect_conditions:
        raise EntranceRandomizationError("Entrance randomization requires explicit indirect conditions in order "
                                         + "to correctly analyze whether dead end regions can be required in logic.")

    start_time = time.perf_counter()
    er_state = ERPlacementState(world, coupled)
    entrance_lookup = EntranceLookup(world.random, coupled)
    # similar to fill, skip validity checks on entrances if the game is beatable on minimal accessibility
    perform_validity_check = True

    def do_placement(source_exit: Entrance, target_entrance: Entrance) -> None:
        placed_exits, removed_entrances = er_state.connect(source_exit, target_entrance)
        # remove the placed targets from consideration
        for entrance in removed_entrances:
            entrance_lookup.remove(entrance)
        # propagate new connections
        er_state.collection_state.update_reachable_regions(world.player)
        er_state.collection_state.sweep_for_advancements()
        if on_connect:
            on_connect(er_state, placed_exits)

    def find_pairing(dead_end: bool, require_new_exits: bool) -> bool:
        nonlocal perform_validity_check
        placeable_exits = er_state.find_placeable_exits(perform_validity_check)
        for source_exit in placeable_exits:
            target_groups = target_group_lookup[source_exit.randomization_group]
            for target_entrance in entrance_lookup.get_targets(target_groups, dead_end, preserve_group_order):
                # when requiring new exits, ideally we would like to make it so that every placement increases
                # (or keeps the same number of) reachable exits. The goal is to continue to expand the search space
                # so that we do not crash. In the interest of performance and bias reduction, generally, just checking
                # that we are going to a new region is a good approximation. however, we should take extra care on the
                # very last exit and check whatever exits we open up are functionally accessible.
                # this requirement can be ignored on a beaten minimal, islands are no issue there.
                exit_requirement_satisfied = (not perform_validity_check or not require_new_exits
                                                or target_entrance.connected_region not in er_state.placed_regions)
                needs_speculative_sweep = (not dead_end and require_new_exits and perform_validity_check
                                           and len(placeable_exits) == 1)
                if exit_requirement_satisfied and source_exit.can_connect_to(target_entrance, dead_end, er_state):
                    if (needs_speculative_sweep
                            and not er_state.test_speculative_connection(source_exit, target_entrance)):
                        continue
                    do_placement(source_exit, target_entrance)
                    return True
        else:
            # no source exits had any valid target so this stage is deadlocked. retries may be implemented if early
            # deadlocking is a frequent issue.
            lookup = entrance_lookup.dead_ends if dead_end else entrance_lookup.others

            # if we're in a stage where we're trying to get to new regions, we could also enter this
            # branch in a success state (when all regions of the preferred type have been placed, but there are still
            # additional unplaced entrances into those regions)
            if require_new_exits:
                if all(e.connected_region in er_state.placed_regions for e in lookup):
                    return False

            # if we're on minimal accessibility and can guarantee the game is beatable,
            # we can prevent a failure by bypassing future validity checks. this check may be
            # expensive; fortunately we only have to do it once
            if perform_validity_check and world.options.accessibility == Accessibility.option_minimal \
                    and world.multiworld.has_beaten_game(er_state.collection_state, world.player):
                # ensure that we have enough locations to place our progression
                accessible_location_count = 0
                prog_item_count = sum(er_state.collection_state.prog_items[world.player].values())
                # short-circuit location checking in this case
                if prog_item_count == 0:
                    return True
                for region in er_state.placed_regions:
                    for loc in region.locations:
                        if loc.can_reach(er_state.collection_state):
                            accessible_location_count += 1
                            if accessible_location_count >= prog_item_count:
                                perform_validity_check = False
                                # pretend that this was successful to retry the current stage
                                return True

            unplaced_entrances = [entrance for region in world.multiworld.get_regions(world.player)
                                  for entrance in region.entrances if not entrance.parent_region]
            unplaced_exits = [exit_ for region in world.multiworld.get_regions(world.player)
                              for exit_ in region.exits if not exit_.connected_region]
            entrance_kind = "dead ends" if dead_end else "non-dead ends"
            region_access_requirement = "requires" if require_new_exits else "does not require"
            raise EntranceRandomizationError(
                f"None of the available entrances are valid targets for the available exits.\n"
                f"Randomization stage is placing {entrance_kind} and {region_access_requirement} "
                f"new region/exit access by default\n"
                f"Placeable entrances: {lookup}\n"
                f"Placeable exits: {placeable_exits}\n"
                f"All unplaced entrances: {unplaced_entrances}\n"
                f"All unplaced exits: {unplaced_exits}")

    if not er_targets:
        er_targets = sorted([entrance for region in world.multiworld.get_regions(world.player)
                             for entrance in region.entrances if not entrance.parent_region], key=lambda x: x.name)
    if not exits:
        exits = sorted([ex for region in world.multiworld.get_regions(world.player)
                        for ex in region.exits if not ex.connected_region], key=lambda x: x.name)
    if len(er_targets) != len(exits):
        raise EntranceRandomizationError(f"Unable to randomize entrances due to a mismatched count of "
                                         f"entrances ({len(er_targets)}) and exits ({len(exits)}.")
    for entrance in er_targets:
        entrance_lookup.add(entrance)

    # place the menu region and connected start region(s)
    er_state.collection_state.update_reachable_regions(world.player)

    # stage 1 - try to place all the non-dead-end entrances
    while entrance_lookup.others:
        if not find_pairing(dead_end=False, require_new_exits=True):
            break
    # stage 2 - try to place all the dead-end entrances
    while entrance_lookup.dead_ends:
        if not find_pairing(dead_end=True, require_new_exits=True):
            break
    # stage 3 - all the regions should be placed at this point. We now need to connect dangling edges
    # stage 3a - get the rest of the dead ends (e.g. second entrances into already-visited regions)
    #            doing this before the non-dead-ends is important to ensure there are enough connections to
    #            go around
    while entrance_lookup.dead_ends:
        find_pairing(dead_end=True, require_new_exits=False)
    # stage 3b - tie all the other loose ends connecting visited regions to each other
    while entrance_lookup.others:
        find_pairing(dead_end=False, require_new_exits=False)

    running_time = time.perf_counter() - start_time
    if running_time > 1.0:
        logging.info(f"Took {running_time:.4f} seconds during entrance randomization for player {world.player},"
                     f"named {world.multiworld.player_name[world.player]}")

    return er_state
