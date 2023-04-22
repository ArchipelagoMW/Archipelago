import unittest

from ..data.bundle_data import all_bundle_items, quality_crops_items


class TestBundles(unittest.TestCase):
    def test_all_bundle_items_have_3_parts(self):
        for bundle_item in all_bundle_items:
            with self.subTest(bundle_item.item.name):
                self.assertGreater(len(bundle_item.item.name), 0)
                id = bundle_item.item.item_id
                self.assertGreaterEqual(id, -1)
                self.assertNotEqual(id, 0)
                self.assertGreater(bundle_item.amount, 0)
                self.assertGreaterEqual(bundle_item.quality, 0)

    def test_quality_crops_have_correct_amounts(self):
        for bundle_item in quality_crops_items:
            with self.subTest(bundle_item.item.name):
                name = bundle_item.item.name
                if name == "Sweet Gem Berry" or name == "Ancient Fruit":
                    self.assertEqual(bundle_item.amount, 1)
                else:
                    self.assertEqual(bundle_item.amount, 5)

    def test_quality_crops_have_correct_quality(self):
        for bundle_item in quality_crops_items:
            with self.subTest(bundle_item.item.name):
                self.assertEqual(bundle_item.quality, 2)

