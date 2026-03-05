import unittest
from typing import Dict, Optional

from .bases import SVTestBase, SVTestCase
from .. import BundleRandomization, location_table
from ..bundles.bundle import Bundle
from ..data.bundles_data.bundle_data import all_bundle_items_except_money, quality_crops_items_thematic, \
    quality_foraging_items, quality_fish_items
from ..data.bundles_data.meme_bundles import all_cc_meme_bundles
from ..locations import LocationTags
from ..options import BundleWhitelist, BundleBlacklist, BundlePrice
from ..strings.bundle_names import BundleName, MemeBundleName, all_meme_bundle_names
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
    whitelist_bundles = {BundleName.money_2500, BundleName.money_5000, BundleName.money_10000, BundleName.gambler, BundleName.ocean_fish,
                         BundleName.lake_fish, BundleName.deep_fishing, BundleName.spring_fish, BundleName.legendary_fish, BundleName.bait}
    blacklist_bundles = {BundleName.spring_foraging, BundleName.quality_crops, BundleName.night_fish, BundleName.carnival, BundleName.dye,
                         BundleName.enchanter}
    options = {
        BundleRandomization: BundleRandomization.option_remixed,
        BundleWhitelist: frozenset(whitelist_bundles),
        BundleBlacklist: frozenset(blacklist_bundles),
    }

    def test_all_plando_bundles_are_there(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for bundle_name in self.whitelist_bundles:
            with self.subTest(f"{bundle_name}"):
                self.assertIn(bundle_name, location_names)
        for bundle_name in self.blacklist_bundles:
            with self.subTest(f"{bundle_name}"):
                self.assertNotIn(bundle_name, location_names)


class TestRemixedAnywhereBundles(SVTestBase):
    fish_bundle_names = {BundleName.spring_fish, BundleName.summer_fish, BundleName.fall_fish, BundleName.winter_fish, BundleName.ocean_fish,
                         BundleName.lake_fish, BundleName.river_fish, BundleName.night_fish, BundleName.legendary_fish, BundleName.specialty_fish,
                         BundleName.bait, BundleName.specific_bait, BundleName.crab_pot, BundleName.tackle, BundleName.quality_fish,
                         BundleName.rain_fish, BundleName.master_fisher}
    blacklist_bundles = {BundleName.spring_foraging, BundleName.quality_crops, BundleName.summer_foraging, BundleName.carnival, BundleName.dye,
                         BundleName.enchanter, BundleName.fall_crops, BundleName.artisan}
    options = {
        BundleRandomization: BundleRandomization.option_remixed_anywhere,
        BundleWhitelist: frozenset(fish_bundle_names),
        BundleBlacklist: frozenset(blacklist_bundles),
    }

    def test_all_plando_bundles_are_there(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for bundle_name in self.fish_bundle_names:
            with self.subTest(f"{bundle_name}"):
                self.assertIn(bundle_name, location_names)
        for bundle_name in self.blacklist_bundles:
            with self.subTest(f"{bundle_name}"):
                self.assertNotIn(bundle_name, location_names)


class TestMemeBundles(SVTestBase):
    options = {
        BundleRandomization.internal_name: BundleRandomization.option_meme,
        BundlePrice.internal_name: BundlePrice.option_maximum,
    }

    def test_can_complete_all_bundles_with_all_state(self):
        self.collect_everything()
        for location_name in self.get_real_location_names():
            if location_name not in location_table or LocationTags.MEME_BUNDLE not in location_table[location_name].tags:
                continue
            with self.subTest(f"{location_name}"):
                self.assert_can_reach_location(location_name)

    def test_specific_bundles_are_not_affected_by_price(self):
        all_bundles = [bundle for bundle_room in self.world.modified_bundles for bundle in bundle_room.bundles]
        bundles_by_name = {bundle.name: bundle for bundle in all_bundles}
        self.check_price(bundles_by_name, MemeBundleName.death, 1, 1, 1)
        self.check_price(bundles_by_name, MemeBundleName.communism, 1, 1, 1)
        self.check_price(bundles_by_name, MemeBundleName.amons_fall, 7, 7, 1)
        self.check_price(bundles_by_name, MemeBundleName.rick, 1, 1, 1)
        self.check_price(bundles_by_name, MemeBundleName.obelisks, 8, 8)
        self.check_price(bundles_by_name, MemeBundleName.eg, 8, 2, 57)
        self.check_price(bundles_by_name, MemeBundleName.chaos_emerald, 7, 7, 1)
        self.check_price(bundles_by_name, MemeBundleName.honorable, 2, 1)
        self.check_price(bundles_by_name, MemeBundleName.snitch, 1, 1, 1)
        self.check_price(bundles_by_name, MemeBundleName.commitment, 4, 4)
        self.check_price(bundles_by_name, MemeBundleName.journalist, 1, 1, 1)
        self.check_price(bundles_by_name, MemeBundleName.off_your_back, 6, 6, 1)
        self.check_price(bundles_by_name, MemeBundleName.sisyphus, 12, 12, 1)

    def check_price(self, bundles: Dict[str, Bundle], bundle_name: str, expected_items: int, expected_required_items: int, stack_amount: Optional[int] = None):
        if bundle_name not in bundles:
            return
        with self.subTest(bundle_name):
            bundle = bundles[bundle_name]
            self.assertEqual(len(bundle.items), expected_items)
            self.assertEqual(bundle.number_required, expected_required_items)
            if stack_amount is not None:
                for item in bundle.items:
                    self.assertEqual(item.amount, stack_amount)


class TestMemeBundleContent(SVTestCase):
    def test_all_meme_bundles_are_included(self):
        all_meme_bundles_in_cc = {bundle.name for bundle in all_cc_meme_bundles}
        for meme_bundle_name in all_meme_bundle_names:
            if meme_bundle_name == MemeBundleName.investment:
                continue
            with self.subTest(meme_bundle_name):
                self.assertIn(meme_bundle_name, all_meme_bundles_in_cc)


class TestScamBundleWhitelist(SVTestBase):
    options = {
        BundleRandomization: BundleRandomization.option_meme,
        BundleWhitelist: frozenset({MemeBundleName.scam})
    }

    def test_scam_bundle_is_there(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        self.assertIn(MemeBundleName.scam, location_names)

    def test_investment_bundle_is_not_there(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        self.assertNotIn(MemeBundleName.investment, location_names)


class TestInvestmentBundleWhitelist(SVTestBase):
    options = {
        BundleRandomization: BundleRandomization.option_meme,
        BundleWhitelist: frozenset({MemeBundleName.investment})
    }

    def test_scam_bundle_is_there(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        self.assertIn(MemeBundleName.scam, location_names)

    def test_investment_bundle_is_not_there(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        self.assertNotIn(MemeBundleName.investment, location_names)


class TestScamBundleBlacklist(SVTestBase):
    options = {
        BundleRandomization: BundleRandomization.option_meme,
        BundleBlacklist: frozenset({MemeBundleName.scam})
    }

    def test_scam_bundle_is_not_there(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        self.assertNotIn(MemeBundleName.scam, location_names)

    def test_investment_bundle_is_not_there(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        self.assertNotIn(MemeBundleName.investment, location_names)


class TestInvestmentBundleBlacklist(SVTestBase):
    options = {
        BundleRandomization: BundleRandomization.option_meme,
        BundleBlacklist: frozenset({MemeBundleName.investment})
    }

    def test_scam_bundle_is_not_there(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        self.assertNotIn(MemeBundleName.scam, location_names)

    def test_investment_bundle_is_not_there(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        self.assertNotIn(MemeBundleName.investment, location_names)
