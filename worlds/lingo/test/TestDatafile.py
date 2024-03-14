import os
import unittest

from worlds.lingo.static_logic import HASHES
from worlds.lingo.utils.pickle_static_data import hash_file


class TestDatafile(unittest.TestCase):
    def test_check_hashes(self) -> None:
        ll1_file_hash = hash_file(os.path.join(os.path.dirname(__file__), "..", "data", "LL1.yaml"))
        ids_file_hash = hash_file(os.path.join(os.path.dirname(__file__), "..", "data", "ids.yaml"))

        self.assertEqual(ll1_file_hash, HASHES["LL1.yaml"],
                         "LL1.yaml hash does not match generated.dat. Please regenerate using 'python worlds/lingo/utils/pickle_static_data.py'")
        self.assertEqual(ids_file_hash, HASHES["ids.yaml"],
                         "ids.yaml hash does not match generated.dat. Please regenerate using 'python worlds/lingo/utils/pickle_static_data.py'")
