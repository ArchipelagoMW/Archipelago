import random
import unittest
from types import SimpleNamespace

from worlds.alttp.PotShuffle import (
    POT_KEY,
    generate_pot_shuffle,
    get_unique_pot_item_position,
)


class TestPotShuffle(unittest.TestCase):
    def test_reserved_key_rooms_only_place_actual_keys(self) -> None:
        for seed in range(10):
            world = SimpleNamespace(
                random=random.Random(seed),
                options=SimpleNamespace(retro_bow=False),
            )
            shuffled_pots = generate_pot_shuffle(world)
            conveyor_cross_keys = [
                pot for pot in shuffled_pots[0x8B]
                if pot.item == POT_KEY
            ]
            self.assertEqual(len(conveyor_cross_keys), 1)

    def test_get_unique_pot_item_position_returns_single_match(self) -> None:
        world = SimpleNamespace(
            random=random.Random(0),
            options=SimpleNamespace(retro_bow=False),
        )
        shuffled_pots = generate_pot_shuffle(world)

        self.assertEqual(
            get_unique_pot_item_position(shuffled_pots, 0x36, POT_KEY),
            (114, 16),
        )


if __name__ == "__main__":
    unittest.main()
