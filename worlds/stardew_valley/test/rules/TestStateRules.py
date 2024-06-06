import unittest

from BaseClasses import ItemClassification
from ...test import solo_multiworld


class TestHasProgressionPercent(unittest.TestCase):
    def test_max_item_amount_is_full_collection(self):
        # Not caching because it fails too often for some reason
        with solo_multiworld(world_caching=False) as (multiworld, world):
            progression_item_count = sum(1 for i in multiworld.get_items() if ItemClassification.progression in i.classification)
            self.assertEqual(world.total_progression_items, progression_item_count - 1)  # -1 to skip Victory
