from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Set, Tuple

from .routing_info import (
    EntranceToPickupRegionInfo,
    entrance_to_entrance_info_collection,
    entrance_to_pickup_region_info_collection,
)
from .routing_calculation_entrances import (
    Edge,
    MaskUtils,
    RouteOption,
    RoutingQueries,
    RoutingGraph as EntranceRoutingGraph,
    RoutingGraphBuilder as EntranceRoutingGraphBuilder,
)

NodeId = str
ReqMask = int


class PickupNodeId:
    """
    Helpers for representing pickup regions as graph nodes.
    """

    _PREFIX = "PICKUP:"

    @staticmethod
    def make(pickup_number: int) -> NodeId:
        return f"{PickupNodeId._PREFIX}{int(pickup_number)}"

    @staticmethod
    def is_pickup(node_id: NodeId) -> bool:
        return node_id.startswith(PickupNodeId._PREFIX)

    @staticmethod
    def number(node_id: NodeId) -> int:
        return int(node_id[len(PickupNodeId._PREFIX) :])


Adjacency = Dict[NodeId, List[Edge]]
FromToKey = Tuple[NodeId, NodeId]


@dataclass(frozen=True, slots=True)
class RoutingGraph:
    """
    Minimal graph container compatible with RoutingQueries.
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
        requirements: Iterable[EntranceToPickupRegionInfo],
        *,
        include_combos: bool = True,
        minimize: bool = True,
        strict_combo_tokens: bool = True,
        include_entrance_network: bool = True,
    ) -> RoutingGraph:
        if include_entrance_network:
            base_graph: EntranceRoutingGraph = EntranceRoutingGraphBuilder.from_requirements(
                entrance_to_entrance_info_collection,
                include_combos=include_combos,
                minimize=minimize,
                strict_combo_tokens=strict_combo_tokens,
            )
            adjacency: Adjacency = {node: list(edges) for node, edges in base_graph.adj.items()}
            by_connection_number: Dict[int, Tuple[NodeId, Edge]] = dict(base_graph.by_connection_number)
            by_from_to: Dict[FromToKey, List[Edge]] = {
                key: list(edges) for key, edges in base_graph.by_from_to.items()
            }
            connection_counter = (max(by_connection_number.keys()) + 1) if by_connection_number else 1
        else:
            adjacency = {}
            by_connection_number = {}
            by_from_to = {}
            connection_counter = 1

        for req in requirements:
            masks = req.get_requirement_bitmasks(
                include_combos=include_combos,
                minimize=minimize,
                strict_combo_tokens=strict_combo_tokens,
            )

            if not masks:
                continue

            entrance_node = req.entrance_identifier
            pickup_node = PickupNodeId.make(req.pickup_number)

            for from_node, to_node in (
                (entrance_node, pickup_node),
                (pickup_node, entrance_node),  # symmetric: to and from the pickup region
            ):
                edge = Edge(
                    to_node=to_node,
                    connection_number=connection_counter,
                    req_masks=tuple(int(m) for m in masks),
                    variant=req.variant,
                )

                adjacency.setdefault(from_node, []).append(edge)
                adjacency.setdefault(to_node, adjacency.get(to_node, []))
                by_connection_number[connection_counter] = (from_node, edge)
                by_from_to.setdefault((from_node, to_node), []).append(edge)
                connection_counter += 1

        frozen_by_from_to: Dict[FromToKey, Tuple[Edge, ...]] = {
            key: tuple(edges) for key, edges in by_from_to.items()
        }

        return RoutingGraph(
            adj=adjacency,
            by_connection_number=by_connection_number,
            by_from_to=frozen_by_from_to,
        )


def reachable_pickup_numbers_from_entrance(
    graph: RoutingGraph, start_entrance: NodeId, have_mask: ReqMask
) -> Set[int]:
    """
    Return pickup numbers reachable from the given entrance under have_mask.
    """
    reachable_nodes = RoutingQueries.reachable_entrance_nodes(graph, start_entrance, have_mask)
    return {
        PickupNodeId.number(node_id)
        for node_id in reachable_nodes
        if PickupNodeId.is_pickup(node_id)
    }


def pickup_route_options(
    graph: RoutingGraph,
    start_entrance: NodeId,
    pickup_number: int,
    *,
    have_mask: Optional[ReqMask] = None,
    limit: Optional[int] = None,
) -> Tuple[RouteOption, ...]:
    """
    Wrapper around RoutingQueries.route_options with a pickup target.
    """
    pickup_node = PickupNodeId.make(pickup_number)
    return RoutingQueries.route_options(
        graph,
        start_entrance,
        pickup_node,
        have_mask=have_mask,
        limit=limit,
    )


# Convenience: build a graph from the bundled symmetric entrance->pickup data.
def default_graph(
    *,
    include_combos: bool = True,
    minimize: bool = True,
    strict_combo_tokens: bool = True,
) -> RoutingGraph:
    return RoutingGraphBuilder.from_requirements(
        entrance_to_pickup_region_info_collection,
        include_combos=include_combos,
        minimize=minimize,
        strict_combo_tokens=strict_combo_tokens,
    )


# ------------------------------------------------------------
# Convenience test/demo
# ------------------------------------------------------------

def test_print_route_from_000_003_to_pickup_42() -> None:
    """
    Finds one minimal requirement set to reach pickup 42 from entrance 000:003
    and prints the route with its required abilities.
    """
    graph = default_graph()
    start = "000:003"
    pickup_number = 42

    options = pickup_route_options(graph, start, pickup_number, limit=1)
    assert options, "No route options found from 000:003 to pickup 42"

    option = options[0]
    print(f"Required abilities: {MaskUtils.format(option.required_mask)}")
    for step in option.steps:
        print(
            f"{step.edge_from} -> {step.edge_to} "
            f"(conn={step.connection_number}, variant={step.variant}) "
            f"requires {MaskUtils.format(step.chosen_edge_req_mask)}"
        )
