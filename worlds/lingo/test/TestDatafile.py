import os
import unittest

from ..static_logic import HASHES, PANELS_BY_ROOM
from ..utils.pickle_static_data import hash_file


class TestDatafile(unittest.TestCase):
    def test_check_hashes(self) -> None:
        ll1_file_hash = hash_file(os.path.join(os.path.dirname(__file__), "..", "data", "LL1.yaml"))
        ids_file_hash = hash_file(os.path.join(os.path.dirname(__file__), "..", "data", "ids.yaml"))

        self.assertEqual(ll1_file_hash, HASHES["LL1.yaml"],
                         "LL1.yaml hash does not match generated.dat. Please regenerate using 'python worlds/lingo/utils/pickle_static_data.py'")
        self.assertEqual(ids_file_hash, HASHES["ids.yaml"],
                         "ids.yaml hash does not match generated.dat. Please regenerate using 'python worlds/lingo/utils/pickle_static_data.py'")

    def test_panel_doors_are_set(self) -> None:
        # This panel is defined earlier in the file than the panel door, so we want to check that the panel door is
        # correctly applied.
        self.assertNotEqual(PANELS_BY_ROOM["Outside The Agreeable"]["FIVE (1)"].panel_door, None)
