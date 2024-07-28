import argparse
import json
import subprocess
import sys
import unittest

from Fill import distribute_items_restrictive
from test.general import setup_solo_multiworld
from worlds import AutoWorldRegister


class TestDeterminism(unittest.TestCase):
    def test_world_determinism(self):
        """Tests that the state of a generated multiworld is the same per world."""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest(game=game_name):
    
                multi_one = json.loads(
                    subprocess.check_output(
                        [sys.executable, "-m", "test.general.test_determinism", "--seed", "0", "--game", game_name]
                    )[:-4]  # strip some garbage at the end
                )
                multi_two = json.loads(
                    subprocess.check_output(
                        [sys.executable, "-m", "test.general.test_determinism", "--seed", "0", "--game", game_name]
                    )[:-4]
                )
                self.assertEqual(len(multi_one), len(multi_two))
                
                for i in range(len(multi_one)):
                    with self.subTest(f"filled location {i}"):
                        self.assertEqual(multi_one[i], multi_two[i])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", help="Seed number to generate multiworld with", type=int, required=True)
    parser.add_argument("--game", help="Game to generate multiworld with", type=str, required=True)

    args = parser.parse_args()

    multiworld = setup_solo_multiworld(AutoWorldRegister.world_types[args.game], seed=args.seed)
    distribute_items_restrictive(multiworld)

    # location and item objects aren't serializable
    output = [{loc.name: loc.item.name} for loc in multiworld.get_locations()]
    print(json.dumps(output))
