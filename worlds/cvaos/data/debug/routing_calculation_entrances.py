from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import heapq
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Set, Tuple

from .routing_info import AbilityCombo, RoutingInfo
from . import entrance_to_entrance_info_collection

NodeId = str
ReqMask = int


@dataclass(frozen=True, slots=True)
class Edge:
    """
    Directed edge with multiple alternative requirement options.
    """
    to_node: NodeId
    connection_number: int
    req_masks: Tuple[ReqMask, ...]
    variant: Optional[int] = None


@dataclass(frozen=True, slots=True)
class BFSStep:
    from_node: NodeId
    to_node: NodeId
    connection_number: int
    variant: Optional[int]
    usable_req_masks: Tuple[ReqMask, ...]


@dataclass(frozen=True, slots=True)
class BFSResult:
    reachable: bool
    path_nodes: Tuple[NodeId, ...]
    steps: Tuple[BFSStep, ...]


@dataclass(frozen=True, slots=True)
class ParentInfo:
    prev_node: NodeId
    prev_mask: ReqMask
    edge_from: NodeId
    edge_to: NodeId
    connection_number: int
    variant: Optional[int]
    chosen_edge_req_mask: ReqMask


@dataclass(frozen=True, slots=True)
class MinReqResult:
    best: Mapping[NodeId, Set[ReqMask]]
    parent: Mapping[Tuple[NodeId, ReqMask], ParentInfo]


@dataclass(frozen=True, slots=True)
class RouteOption:
    """
    A minimal sufficient requirement set for reaching a goal
        and an example path (edge-by-edge) that achieves it
        using that requirement set.
    """
    required_mask: ReqMask
    steps: Tuple[ParentInfo, ...]


class EntranceId:
    """
    Entrance node IDs are "START_ROOM:END_ROOM", e.g. "000:003".
        (Soma's starting location)
    """

    _SEP = ":"
    _PSEUDO_PREFIX = "__START__@"  # pseudo node for "standing in a room at spawn"

    @staticmethod
    def make(start_room: str, end_room: str) -> NodeId:
        return f"{start_room}{EntranceId._SEP}{end_room}"

    @staticmethod
    def split(entrance_id: NodeId) -> Tuple[str, str]:
        start_room, end_room = entrance_id.split(EntranceId._SEP, 1)
        return start_room, end_room

    @staticmethod
    def start_room(entrance_id: NodeId) -> str:
        start_room, _ = EntranceId.split(entrance_id)
        return start_room

    @staticmethod
    def pseudo_start_node(start_room: str) -> NodeId:
        # Not an actual entrance; just a convenient "spawn state" node
        return f"{EntranceId._PSEUDO_PREFIX}{start_room}"

    @staticmethod
    def is_pseudo(node_id: NodeId) -> bool:
        return node_id.startswith(EntranceId._PSEUDO_PREFIX)


class MaskUtils:
    @staticmethod
    def from_flags(*flags: AbilityCombo) -> ReqMask:
        mask = 0
        for flag in flags:
            mask |= int(flag)
        return mask

    @staticmethod
    def satisfied(have_mask: ReqMask, req_mask: ReqMask) -> bool:
        return (have_mask & req_mask) == req_mask

    @staticmethod
    def usable_options(have_mask: ReqMask, req_masks: Sequence[ReqMask]) -> Tuple[ReqMask, ...]:
        return tuple(req_mask for req_mask in req_masks if MaskUtils.satisfied(have_mask, req_mask))

    @staticmethod
    def edge_traversable(have_mask: ReqMask, req_masks: Sequence[ReqMask]) -> bool:
        return any(MaskUtils.satisfied(have_mask, req_mask) for req_mask in req_masks)

    @staticmethod
    def decode(mask: ReqMask) -> Tuple[str, ...]:
        if mask == 0:
            return ("None",)

        names: List[str] = []
        for flag in AbilityCombo:
            if flag == AbilityCombo.None_:
                continue
            if mask & int(flag):
                names.append(flag.name)

        # Preserve unknown bits for debugging
        known_bits = 0
        for flag in AbilityCombo:
            known_bits |= int(flag)
        extra_bits = mask & ~known_bits
        if extra_bits:
            names.append(hex(extra_bits))

        return tuple(names)

    @staticmethod
    def format(mask: ReqMask) -> str:
        return "|".join(MaskUtils.decode(mask))


Adjacency = Dict[NodeId, List[Edge]]
FromToKey = Tuple[NodeId, NodeId]


@dataclass(frozen=True, slots=True)
class RoutingGraph:
    """
    Holds the routing adjacency list.
    """
    adj: Adjacency
    by_connection_number: Mapping[int, Tuple[NodeId, Edge]]
    by_from_to: Mapping[FromToKey, Tuple[Edge, ...]]

    def edges_from(self, node: NodeId) -> Sequence[Edge]:
        return self.adj.get(node, ())

    def has_node(self, node: NodeId) -> bool:
        return node in self.adj

    def lookup_by_connection_number(self, connection_number: int) -> Tuple[NodeId, Edge]:
        return self.by_connection_number[connection_number]

    def lookup_edges(self, from_node: NodeId, to_node: NodeId) -> Sequence[Edge]:
        return self.by_from_to.get((from_node, to_node), ())


class RoutingGraphBuilder:
    @staticmethod
    def from_requirements(
        requirements: Iterable[RoutingInfo],
        *,
        include_combos: bool = True,
        minimize: bool = True,
        strict_combo_tokens: bool = True,
    ) -> RoutingGraph:
        adjacency: Adjacency = {}
        by_connection_number: Dict[int, Tuple[NodeId, Edge]] = {}
        by_from_to: Dict[FromToKey, List[Edge]] = {}

        for route_info in requirements:
            req_masks = route_info.get_requirement_bitmasks(
                include_combos=include_combos,
                minimize=minimize,
                strict_combo_tokens=strict_combo_tokens,
            )

            # No options => never traversable, ignore
            if not req_masks:
                continue

            from_entrance = EntranceId.make(route_info.from_room, route_info.room_id)
            to_entrance = EntranceId.make(route_info.room_id, route_info.to_room)

            edge = Edge(
                to_node=to_entrance,
                connection_number=route_info.connection_number,
                req_masks=tuple(int(mask) for mask in req_masks),
                variant=route_info.variant,
            )

            adjacency.setdefault(from_entrance, []).append(edge)
            adjacency.setdefault(to_entrance, adjacency.get(to_entrance, []))  # ensure node exists

            by_connection_number[edge.connection_number] = (from_entrance, edge)
            by_from_to.setdefault((from_entrance, to_entrance), []).append(edge)

        frozen_by_from_to: Dict[FromToKey, Tuple[Edge, ...]] = {
            key: tuple(edges) for key, edges in by_from_to.items()
        }

        return RoutingGraph(
            adj=adjacency,
            by_connection_number=by_connection_number,
            by_from_to=frozen_by_from_to,
        )


class RoutingQueries:
    """
    Graph-searching methods over entrance-node graphs.

    Nodes are entrance identifiers like "000:003".
    Each DEdge can have multiple requirement options (conjunction masks),
        encoded as bitmaks.
    """

    @staticmethod
    def start_entrances_for_room(graph: RoutingGraph, start_room: str) -> Tuple[NodeId, ...]:
        prefix = f"{start_room}:"
        candidates = [node_id for node_id in graph.adj.keys() if node_id.startswith(prefix)]
        candidates.sort()
        return tuple(candidates)

    @staticmethod
    def reachable_entrance_nodes(graph: RoutingGraph, start: NodeId, have_mask: ReqMask) -> Set[NodeId]:
        """
        Computes the set of all entrances reachable from the given node with the given bitmask.

        Performs BFS over a filtered graph:
        an edge u->v is considered traversable if any of its option masks is
        satisfied by have_mask.

        Args:
            graph: The routing graph (in adjacency-list format) to traverse.
            start: Starting entranc identifier.
            have_mask: Bitmask of abilities/conditions currently available.

        Returns:
            A set of node IDs: start and every node reachable from it
                under the provided mask.
        """
        visited_nodes: Set[NodeId] = {start}
        frontier: deque[NodeId] = deque([start])

        while frontier:
            current_node = frontier.popleft()

            # Explore outgoing edges from current_node
            for edge in graph.edges_from(current_node):
                # Edge is usable if any option-mask is satisfied by have_mask
                if not MaskUtils.edge_traversable(have_mask, edge.req_masks):
                    continue

                next_node = edge.to_node
                if next_node in visited_nodes:
                    continue

                visited_nodes.add(next_node)
                frontier.append(next_node)

        return visited_nodes

    @staticmethod
    def reachable_entrance_nodes_from_room(
        graph: RoutingGraph,
        start_room: str,
        have_mask: ReqMask
    ) -> Set[NodeId]:
        """
        Multi-source bfs
        """
        starting_entrances = RoutingQueries.start_entrances_for_room(graph, start_room)
        if not starting_entrances:
            return set()

        visited_nodes: Set[NodeId] = set(starting_entrances)
        frontier: deque[NodeId] = deque(starting_entrances)

        while frontier:
            current_node = frontier.popleft()

            for edge in graph.edges_from(current_node):
                if not MaskUtils.edge_traversable(have_mask, edge.req_masks):
                    continue

                next_node = edge.to_node
                if next_node in visited_nodes:
                    continue

                visited_nodes.add(next_node)
                frontier.append(next_node)

        return visited_nodes

    @staticmethod
    def reachable_with_options_bfs(
        graph: RoutingGraph,
        start: NodeId,
        goal: NodeId,
        have_mask: ReqMask,
    ) -> BFSResult:
        """
        Returns a path from start to goal if reachable under the conditions of the have_mask.

        Args:
            graph: The routing graph (in adjacency-list format) to traverse.
            start: Starting room identifier.
            goal: Destination room identifier.
            have_mask: Bitmask of currently available abilities/conditions.

        Returns:
            BFSResult where:
              - reachable indicates whether the goal was found,
              - path_nodes is the (inclusive) sequence from start to goal
              - steps is the per-edge metadata for that path, including the usable
                option masks on each traversed edge.
        """
        if start == goal:
            return BFSResult(True, (start,), ())

        frontier: deque[NodeId] = deque([start])
        visited_nodes: Set[NodeId] = {start}

        # How we got to a node: prev[node] = (previous_node, edge_used, usable_masks_on_edge)
        previous_step: Dict[NodeId, Tuple[NodeId, Edge, Tuple[ReqMask, ...]]] = {}

        while frontier:
            current_node = frontier.popleft()

            for edge in graph.edges_from(current_node):
                # Filter the edge's options down to the ones we can actually use right now
                usable_masks = MaskUtils.usable_options(have_mask, edge.req_masks)
                if not usable_masks:
                    continue

                next_node = edge.to_node
                if next_node in visited_nodes:
                    continue

                visited_nodes.add(next_node)
                previous_step[next_node] = (current_node, edge, usable_masks)

                # Early exit
                if next_node == goal:
                    frontier.clear()
                    break

                frontier.append(next_node)

        if goal not in previous_step:
            return BFSResult(False, (), ())

        # Walk backwards from goal to start
        reconstructed_nodes_reversed: List[NodeId] = [goal]
        reconstructed_steps_reversed: List[BFSStep] = []

        current_node = goal
        while current_node != start:
            previous_node, edge_used, usable_masks_on_edge = previous_step[current_node]

            reconstructed_steps_reversed.append(
                BFSStep(
                    from_node=previous_node,
                    to_node=current_node,
                    connection_number=edge_used.connection_number,
                    variant=edge_used.variant,
                    usable_req_masks=usable_masks_on_edge,
                )
            )

            reconstructed_nodes_reversed.append(previous_node)
            current_node = previous_node

        reconstructed_nodes_reversed.reverse()
        reconstructed_steps_reversed.reverse()

        return BFSResult(
            reachable=True,
            path_nodes=tuple(reconstructed_nodes_reversed),
            steps=tuple(reconstructed_steps_reversed),
        )


    @staticmethod
    def _dominates(subset_mask: ReqMask, superset_mask: ReqMask) -> bool:
        """
        Returns True iff requirement mask a \\subseteq b.
        """
        return (subset_mask | superset_mask) == superset_mask

    @staticmethod
    def _is_dominated(candidate_mask: ReqMask, frontier_masks: Set[ReqMask]) -> bool:
        """
        Returns True iff candidate_mask \\subseteq mask_i for some mask_i in frontier_masks.
        """
        return any(
            RoutingQueries._dominates(existing_mask, candidate_mask)
            for existing_mask in frontier_masks
        )

    @staticmethod
    def _prune_and_add(candidate_mask: ReqMask, frontier_masks: Set[ReqMask]) -> None:
        """
        Inserts candidate_mask into frontier_masks and prunes any masks that candidate_mask dominates.
        """
        masks_to_remove = [
            existing_mask
            for existing_mask in frontier_masks
            if RoutingQueries._dominates(candidate_mask, existing_mask)  # candidate ⊆ existing
        ]
        for removable_mask in masks_to_remove:
            frontier_masks.remove(removable_mask)

        frontier_masks.add(candidate_mask)

    @staticmethod
    def compute_min_requirements(graph: RoutingGraph, start: NodeId) -> MinReqResult:
        """
        Computes subset-minimal requirement masks sufficient to reach every node from start.

        Args:
            graph: The routing graph.
            start: Starting room identifier.

        Returns:
            MinReqResult with:
              - best: dict mapping each node to a set of subset-minimal requirement masks to reach it
              - parent: dict mapping each (node, mask) to ParentInfo for reconstructing a path that
                    achieves that (node, mask)
        """
        best_masks_by_node: Dict[NodeId, Set[ReqMask]] = {start: {0}}
        parent_by_state: Dict[Tuple[NodeId, ReqMask], ParentInfo] = {}

        # Priority is number of bits set
        heap: List[Tuple[int, NodeId, ReqMask]] = [(0, start, 0)]

        while heap:
            _, current_node, current_requirement_mask = heapq.heappop(heap)

            node_frontier = best_masks_by_node.get(current_node)
            # Skip stale heap entries (we may have pruned this state already)
            if node_frontier is None or current_requirement_mask not in node_frontier:
                continue

            for edge in graph.edges_from(current_node):
                next_node = edge.to_node
                frontier_at_next_node = best_masks_by_node.setdefault(next_node, set())

                for edge_option_requirement in edge.req_masks:
                    # accumulate path reqs
                    new_requirement_mask = current_requirement_mask | int(edge_option_requirement)

                    # avoid adding a dominated mask
                    if RoutingQueries._is_dominated(new_requirement_mask, frontier_at_next_node):
                        continue

                    # otherwise, add and prune masks dominated
                    RoutingQueries._prune_and_add(new_requirement_mask, frontier_at_next_node)

                    # store a concrete way to realize this (node,mask) so we can get a path later
                    parent_by_state[(next_node, new_requirement_mask)] = ParentInfo(
                        prev_node=current_node,
                        prev_mask=current_requirement_mask,
                        edge_from=current_node,
                        edge_to=next_node,
                        connection_number=edge.connection_number,
                        variant=edge.variant,
                        chosen_edge_req_mask=int(edge_option_requirement),
                    )

                    heapq.heappush(
                        heap,
                        (new_requirement_mask.bit_count(), next_node, new_requirement_mask),
                    )

        return MinReqResult(best=best_masks_by_node, parent=parent_by_state)

    @staticmethod
    def masks_that_work_for_have(
        best_masks: Iterable[ReqMask],
        have_mask: ReqMask
    ) -> Tuple[ReqMask, ...]:
        """
        Given a bunch of requirement masks, return only the ones we can satisfy right now.
        """
        viable_masks = [
            int(mask)
            for mask in best_masks
            if MaskUtils.satisfied(have_mask, int(mask))
        ]
        viable_masks.sort(key=lambda mask: (mask.bit_count(), mask))
        return tuple(viable_masks)

    @staticmethod
    def reconstruct_path_for_mask(
        parent: Mapping[Tuple[NodeId, ReqMask], ParentInfo],
        start: NodeId,
        goal: NodeId,
        req_mask: ReqMask,
    ) -> Tuple[ParentInfo, ...]:
        """
        Reconstruct one example path that achieves (goal, req_mask).

            This uses the parent mapping returned by `compute_min_requirements`.
            Each returned ParentInfo describes one traversed edge and which specific
                edge option mask was chosen.

        Args:
            parent: Mapping of (node, mask) to ParentInfo (from compute_min_requirements).
            start: Starting room identifier.
            goal: Destination room identifier.
            req_mask: A mask that should be present in best[goal].

        Returns:
            A tuple of ParentInfo steps in forward order from start to goal.

        """
        if start == goal:
            return ()

        reversed_steps: List[ParentInfo] = []
        current_state = (goal, int(req_mask))

        while True:
            info = parent.get(current_state)
            if info is None:
                raise KeyError(
                    f"No parent info for (node={current_state[0]!r}, mask={MaskUtils.format(current_state[1])}); "
                    f"mask may not be in best[{goal!r}]"
                )

            reversed_steps.append(info)

            # Stop when we hit the start with empty requirement
            if info.prev_node == start and info.prev_mask == 0:
                break

            current_state = (info.prev_node, info.prev_mask)

        reversed_steps.reverse()
        return tuple(reversed_steps)

    @staticmethod
    def route_options(
        graph: RoutingGraph,
        start: NodeId,
        goal: NodeId,
        *,
        have_mask: Optional[ReqMask] = None,
        limit: Optional[int] = None,
    ) -> Tuple[RouteOption, ...]:
        """
        Return minimal ways to reach goal as (required_mask, example_path) pairs.

        This is a wrapper around:
          1) compute_min_requirements(graph, start)
          2) select masks in best[goal] (optionally filter by have_mask)
          3) reconstruct one example path for each selected mask

        Args:
            graph: The routing graph.
            start: Starting room identifier.
            goal: Destination room identifier.
            have_mask: If provided, only include options whose required_mask is
                       satisfied by have_mask.
            limit: If provided, return at most this many options (after sorting).

        Returns:
            A tuple of RouteOptions, each containing:
              - required_mask: a subset-minimal mask sufficient to reach goal
              - steps: one example path that achieves that required_mask
        """
        minreq_result = RoutingQueries.compute_min_requirements(graph, start)
        masks_at_goal = minreq_result.best.get(goal, set())

        if have_mask is not None:
            selected_masks = list(RoutingQueries.masks_that_work_for_have(masks_at_goal, have_mask))
        else:
            selected_masks = sorted(
                (int(mask) for mask in masks_at_goal),
                key=lambda mask: (mask.bit_count(), mask)
            )

        if limit is not None:
            selected_masks = selected_masks[: max(0, int(limit))]

        options: List[RouteOption] = []
        for required_mask in selected_masks:
            steps = RoutingQueries.reconstruct_path_for_mask(
                minreq_result.parent, start, goal, required_mask)
            options.append(RouteOption(required_mask=required_mask, steps=steps))

        return tuple(options)


class RoutingDisplay:
    @staticmethod
    def print_reachable_entrance_nodes(
        entrance_nodes: Iterable[NodeId],
        *,
        start_label: str,
        have_mask: ReqMask,
    ) -> None:
        nodes_sorted = sorted(set(entrance_nodes))
        print(f"Start: {start_label}")
        print(f"Have:  {MaskUtils.format(have_mask)}")
        print(f"Reachable entrance-nodes ({len(nodes_sorted)}):")
        for node_id in nodes_sorted:
            print(node_id)

    @staticmethod
    def print_bfs_result(result: BFSResult, *, have_mask: ReqMask) -> None:
        if not result.reachable:
            print(f"Unreachable with have={MaskUtils.format(have_mask)}")
            return

        print(f"Path nodes ({len(result.path_nodes)}): {' -> '.join(result.path_nodes)}")
        print("Steps:")
        for step in result.steps:
            options_text = ", ".join(MaskUtils.format(mask) for mask in step.usable_req_masks)
            print(
                f"  {step.from_node} -> {step.to_node} "
                f"(conn={step.connection_number}, variant={step.variant}) "
                f"usable: [{options_text}]"
            )


def reachable_entrance_nodes_from_000_003_with_none(graph: RoutingGraph) -> Set[NodeId]:
    start_entrance = "000:003"
    have_mask = int(AbilityCombo.None_)
    return RoutingQueries.reachable_entrance_nodes(graph, start_entrance, have_mask)

def print_reachable_entrance_nodes_from_000_003_with_none(graph: RoutingGraph) -> Set[NodeId]:
    start_entrance = "000:003"
    have_mask = int(AbilityCombo.None_)

    reachable_nodes = RoutingQueries.reachable_entrance_nodes(graph, start_entrance, have_mask)
    RoutingDisplay.print_reachable_entrance_nodes(
        reachable_nodes,
        start_label=f"start entrance {start_entrance}",
        have_mask=have_mask,
    )
    return reachable_nodes

def test_print_reachable_entrance_nodes_from_000_003_with_none() -> None:
    graph = RoutingGraphBuilder.from_requirements(entrance_to_entrance_info_collection)

    reachable_nodes = print_reachable_entrance_nodes_from_000_003_with_none(graph)

    assert isinstance(reachable_nodes, set)
    assert "000:003" in reachable_nodes


def reachable_entrance_nodes_from_000_003_with_djump(graph: RoutingGraph) -> Set[NodeId]:
    start_entrance = "000:003"
    have_mask = int(AbilityCombo.DJump)
    return RoutingQueries.reachable_entrance_nodes(graph, start_entrance, have_mask)

def print_reachable_entrance_nodes_from_000_003_with_djump(graph: RoutingGraph) -> Set[NodeId]:
    start_entrance = "000:003"
    have_mask = int(AbilityCombo.DJump)

    reachable_nodes = RoutingQueries.reachable_entrance_nodes(graph, start_entrance, have_mask)
    RoutingDisplay.print_reachable_entrance_nodes(
        reachable_nodes,
        start_label=f"start entrance {start_entrance}",
        have_mask=have_mask,
    )
    return reachable_nodes

def test_print_reachable_entrance_nodes_from_000_003_with_djump() -> None:
    graph = RoutingGraphBuilder.from_requirements(entrance_to_entrance_info_collection)

    reachable_nodes = print_reachable_entrance_nodes_from_000_003_with_djump(graph)

    assert isinstance(reachable_nodes, set)
    assert "000:003" in reachable_nodes

