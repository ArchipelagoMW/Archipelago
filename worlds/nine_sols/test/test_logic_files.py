import json
import os
import pytest
import unittest

from ..shared_static_logic.items import items_data
from ..shared_static_logic.locations import locations_data
from ..shared_static_logic.connections import connections_data


IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"

@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="We only want to test this locally before a release. On individual PRs it would force too many conflicts.")
class TestLogicFiles(unittest.TestCase):
    def test_logic_files(self) -> None:
        expected_items_data = json.dumps(items_data)
        expected_locations_data = json.dumps(locations_data)
        expected_connections_data = json.dumps(connections_data)

        items_path = os.path.join(os.path.dirname(__file__), "..", "shared_static_logic", "items.jsonc")
        locations_path = os.path.join(os.path.dirname(__file__), "..", "shared_static_logic", "locations.jsonc")
        connections_path = os.path.join(os.path.dirname(__file__), "..", "shared_static_logic", "connections.jsonc")

        with open(items_path, 'r') as items_file:
            actual_items_data = items_file.read()
        with open(locations_path, 'r') as locations_file:
            actual_locations_data = locations_file.read()
        with open(connections_path, 'r') as connections_file:
            actual_connections_data = connections_file.read()

        self.assertEqual(
            expected_items_data,
            actual_items_data,
            "items.jsonc does not match items.py. Please regenerate these files.")
        self.assertEqual(
            expected_locations_data,
            actual_locations_data,
            "locations.jsonc does not match locations.py. Please regenerate these files.")
        self.assertEqual(
            expected_connections_data,
            actual_connections_data,
            "connections.jsonc does not match connections.py. Please regenerate these files.")
