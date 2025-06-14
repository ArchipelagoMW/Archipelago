import unittest

from .bases import SVTestBase
from .. import BundleRandomization
from ..data.bundle_data import all_bundle_items_except_money, quality_crops_items_thematic, quality_foraging_items, quality_fish_items
from ..options import BundlePlando
from ..strings.bundle_names import BundleName
from ..strings.crop_names import Fruit
from ..strings.quality_names import CropQuality, ForageQuality, FishQuality


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

    def test_quality_foraging_have_correct_amounts(self):
        for bundle_item in quality_foraging_items:
            with self.subTest(bundle_item.item_name):
                self.assertEqual(bundle_item.amount, 3)

    def test_quality_foraging_have_correct_quality(self):
        for bundle_item in quality_foraging_items:
            with self.subTest(bundle_item.item_name):
                self.assertEqual(bundle_item.quality, ForageQuality.gold)

    def test_quality_fish_have_correct_amounts(self):
        for bundle_item in quality_fish_items:
            with self.subTest(bundle_item.item_name):
                self.assertEqual(bundle_item.amount, 2)

    def test_quality_fish_have_correct_quality(self):
        for bundle_item in quality_fish_items:
            with self.subTest(bundle_item.item_name):
                self.assertEqual(bundle_item.quality, FishQuality.gold)


class TestRemixedPlandoBundles(SVTestBase):
    plando_bundles = {BundleName.money_2500, BundleName.money_5000, BundleName.money_10000, BundleName.gambler, BundleName.ocean_fish,
                      BundleName.lake_fish, BundleName.deep_fishing, BundleName.spring_fish, BundleName.legendary_fish, BundleName.bait}
    options = {
        BundleRandomization: BundleRandomization.option_remixed,
        BundlePlando: frozenset(plando_bundles)
    }

    def test_all_plando_bundles_are_there(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for bundle_name in self.plando_bundles:
            with self.subTest(f"{bundle_name}"):
                self.assertIn(bundle_name, location_names)
        self.assertNotIn(BundleName.money_25000, location_names)
        self.assertNotIn(BundleName.carnival, location_names)
        self.assertNotIn(BundleName.night_fish, location_names)
        self.assertNotIn(BundleName.specialty_fish, location_names)
        self.assertNotIn(BundleName.specific_bait, location_names)


class TestRemixedAnywhereBundles(SVTestBase):
    fish_bundle_names = {BundleName.spring_fish, BundleName.summer_fish, BundleName.fall_fish, BundleName.winter_fish, BundleName.ocean_fish,
                         BundleName.lake_fish, BundleName.river_fish, BundleName.night_fish, BundleName.legendary_fish, BundleName.specialty_fish,
                         BundleName.bait, BundleName.specific_bait, BundleName.crab_pot, BundleName.tackle, BundleName.quality_fish,
                         BundleName.rain_fish, BundleName.master_fisher}
    options = {
        BundleRandomization: BundleRandomization.option_remixed_anywhere,
        BundlePlando: frozenset(fish_bundle_names)
    }

    def test_all_plando_bundles_are_there(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for bundle_name in self.fish_bundle_names:
            with self.subTest(f"{bundle_name}"):
                self.assertIn(bundle_name, location_names)
