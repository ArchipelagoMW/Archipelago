from BaseClasses import ItemClassification
from ...test import SVTestBase


class TestHasProgressionPercent(SVTestBase):
    def test_max_item_amount_is_full_collection(self):
        progression_item_count = sum(1 for i in self.multiworld.get_items() if ItemClassification.progression in i.classification)
        self.assertEqual(self.world.total_progression_items, progression_item_count - 1)  # -1 to skip Victory
