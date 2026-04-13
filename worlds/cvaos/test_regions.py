"""
Test script for validating cvaos regions and locations.

Run from the Archipelago root directory:
    python -m pytest worlds/cvaos/test_regions.py -v
"""
from __future__ import annotations

from .data import (
    entrance_info_collection,
    pickup_info_collection,
    entrance_to_entrance_info_collection,
    transdoor_connection_collection,
)
from .data.routing_calculation_entrances import RoutingGraphBuilder
from .locations import location_name_to_id, location_id_to_name


def test_location_tables_built():
    """Test that location tables are built correctly from pickup data."""
    assert len(location_name_to_id) > 0, "No locations were created"
    assert len(location_name_to_id) == len(location_id_to_name), "Name->ID and ID->Name mappings don't match"
    assert len(location_name_to_id) == len(pickup_info_collection), "Location count doesn't match pickup count"


def test_location_ids_unique():
    """Test that all location IDs are unique."""
    ids = list(location_name_to_id.values())
    assert len(ids) == len(set(ids)), "Duplicate location IDs found"


def test_location_names_unique():
    """Test that all location names are unique."""
    names = list(location_name_to_id.keys())
    assert len(names) == len(set(names)), "Duplicate location names found"


def test_entrance_data_loaded():
    """Test that entrance data was loaded."""
    assert len(entrance_info_collection) > 0, "No entrances were loaded"


def test_routing_data_loaded():
    """Test that routing data was loaded."""
    assert len(entrance_to_entrance_info_collection) > 0, "No routing info was loaded"


def test_transdoor_edges_are_in_routing_graph():
    """Transdoor mappings should become zero-cost edges in the entrance graph."""
    assert len(transdoor_connection_collection) > 0, "No transdoor mappings were loaded"

    graph = RoutingGraphBuilder.from_requirements(entrance_to_entrance_info_collection)
    sample = transdoor_connection_collection[0]
    edges = graph.lookup_edges(sample.from_entrance, sample.to_entrance)

    assert edges, f"Missing transdoor edge {sample.from_entrance} -> {sample.to_entrance}"
    assert any(edge.req_masks == (0,) for edge in edges), "Transdoor edges should have no requirements"


def test_starting_entrance_exists():
    """Test that the starting entrance (000:003) exists."""
    entrance_ids = {e.door_identifier_unique for e in entrance_info_collection}
    assert "000:003" in entrance_ids, "Starting entrance 000:003 not found"


def test_location_id_range():
    """Test that location IDs are within valid range (positive integers)."""
    for name, loc_id in location_name_to_id.items():
        assert loc_id > 0, f"Location {name} has invalid ID {loc_id}"


def test_print_summary():
    """Print a summary of the data (always passes, for info)."""
    print("\n" + "=" * 60)
    print("CVAOS Data Summary")
    print("=" * 60)
    print(f"Entrances: {len(entrance_info_collection)}")
    print(f"Pickups/Locations: {len(pickup_info_collection)}")
    print(f"Routing connections: {len(entrance_to_entrance_info_collection)}")

    if location_name_to_id:
        ids = list(location_name_to_id.values())
        print(f"Location ID range: {min(ids):#x} - {max(ids):#x}")

    print("\nFirst 5 locations:")
    for i, (name, loc_id) in enumerate(list(location_name_to_id.items())[:5]):
        print(f"  {i+1}. {name} (ID: {loc_id:#x})")
    print("=" * 60)
