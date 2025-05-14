from io import BytesIO
import os
import pickle
import pkgutil
import unittest

from ..shared_static_logic.hash_file import hash_file


class TestPickleFile(unittest.TestCase):
    def test_pickle_file_hashes(self) -> None:
        pickled_data = pkgutil.get_data(__name__, "../shared_static_logic/static_logic.pickle")
        pickled_hashes = pickle.load(BytesIO(pickled_data))["HASHES"]

        items_hash = hash_file(os.path.join(os.path.dirname(__file__), "..", "shared_static_logic",
                                            "items.jsonc"))
        locations_hash = hash_file(os.path.join(os.path.dirname(__file__), "..", "shared_static_logic",
                                                "locations.jsonc"))
        connections_hash = hash_file(os.path.join(os.path.dirname(__file__), "..", "shared_static_logic",
                                                  "connections.jsonc"))

        self.assertEqual(
            items_hash,
            pickled_hashes["ITEMS"],
            "items.jsonc hash does not match static_logic.pickle. "
            "Please regenerate using 'python worlds/outer_wilds/shared_static_logic/pickle_static_logic.py'")
        self.assertEqual(
            locations_hash,
            pickled_hashes["LOCATIONS"],
            "locations.jsonc hash does not match static_logic.pickle. "
            "Please regenerate using 'python worlds/outer_wilds/shared_static_logic/pickle_static_logic.py'")
        self.assertEqual(
            connections_hash,
            pickled_hashes["CONNECTIONS"],
            "connections.jsonc hash does not match static_logic.pickle. "
            "Please regenerate using 'python worlds/outer_wilds/shared_static_logic/pickle_static_logic.py'")
