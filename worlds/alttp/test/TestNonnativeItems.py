import unittest

from worlds.alttp.Rom import get_nonnative_item_sprite


class TestNonnativeItemSprites(unittest.TestCase):
    def test_smz3_lttp_item_uses_its_lttp_sprite(self) -> None:
        self.assertEqual(get_nonnative_item_sprite(84007, "SMZ3"), 7)
        self.assertEqual(get_nonnative_item_sprite(84173, "SMZ3"), 173)

    def test_other_games_use_generic_sprite_for_same_id_range(self) -> None:
        self.assertEqual(get_nonnative_item_sprite(84007, "Other Game"), 0x6B)

    def test_smz3_ids_outside_lttp_range_use_generic_sprite(self) -> None:
        self.assertEqual(get_nonnative_item_sprite(84006, "SMZ3"), 0x6B)
        self.assertEqual(get_nonnative_item_sprite(84174, "SMZ3"), 0x6B)


if __name__ == "__main__":
    unittest.main()
