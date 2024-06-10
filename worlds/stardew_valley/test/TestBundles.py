import unittest

from ..data.bundle_data import all_bundle_items_except_money, quality_crops_items_thematic
from ..strings.crop_names import Fruit
from ..strings.quality_names import CropQuality


class TestBundles(unittest.TestCase):
    def test_all_bundle_items_have_3_parts(self):
        for bundle_item in all_bundle_items_except_money:
            with self.subTest(bundle_item.item_name):
                self.assertGreater(len(bundle_item.item_name), 0)
                self.assertGreater(bundle_item.amount, 0)
                self.assertTrue(bundle_item.quality)

    def test_quality_crops_have_correct_amounts(self):
        for bundle_item in quality_crops_items_thematic:
            with self.subTest(bundle_item.item_name):
                name = bundle_item.item_name
                if name == Fruit.sweet_gem_berry or name == Fruit.ancient_fruit:
                    self.assertEqual(bundle_item.amount, 1)
                else:
                    self.assertEqual(bundle_item.amount, 5)

    def test_quality_crops_have_correct_quality(self):
        for bundle_item in quality_crops_items_thematic:
            with self.subTest(bundle_item.item_name):
                self.assertEqual(bundle_item.quality, CropQuality.gold)

