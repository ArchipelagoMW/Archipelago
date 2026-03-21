import unittest
from collections import Counter
from typing import List

from .. import Group
from ..content.content_packs import all_content_pack_names
from ..items import load_item_csv
from ..locations import load_location_csv, LocationTags
from ..strings.trap_names import all_traps


def print_lists_difference(list1: List[str], list2: List[str], list1_name: str = "List 1", list2_name: str = "List 2"):
    for item in list1:
        if item not in list2:
            print(f"{item} is in {list1_name} but not in {list2_name}")
    for item in list2:
        if item not in list1:
            print(f"{item} is in {list2_name} but not in {list1_name}")


def print_duplicates(items: List[str]):
    for item in items:
        if items.count(item) > 1:
            print(f"{item} is in the list {items.count(item)} times")


class TestCsvIntegrity(unittest.TestCase):
    def test_items_integrity(self):
        items = load_item_csv()

        with self.subTest("Test all items have an id"):
            for item in items:
                self.assertIsNotNone(item.code_without_offset, "Some item do not have an id."
                                                               " Run the script `update_data.py` to generate them.")
        with self.subTest("Test all ids are unique"):
            all_ids = [item.code_without_offset for item in items]
            unique_ids = set(all_ids)
            self.assertEqual(len(all_ids), len(unique_ids), f"Some ids are duplicated: {[item for item, count in Counter(all_ids).items() if count > 1]}")

        with self.subTest("Test all names are unique"):
            all_names = [item.name for item in items]
            unique_names = set(all_names)
            self.assertEqual(len(all_names), len(unique_names))

        with self.subTest("Test all content packs are valid"):
            content_packs = {content_pack for item in items for content_pack in item.content_packs}
            for content_pack in content_packs:
                self.assertIn(content_pack, all_content_pack_names)

        with self.subTest("Test all traps are in string"):
            traps = [item.name for item in items if Group.TRAP in item.groups and Group.DEPRECATED not in item.groups]
            for trap in traps:
                self.assertIn(trap, all_traps)

    def test_locations_integrity(self):
        locations = load_location_csv()

        with self.subTest("Test all locations have an id"):
            for location in locations:
                self.assertIsNotNone(location.code_without_offset, "Some location do not have an id."
                                                                   " Run the script `update_data.py` to generate them.")
        with self.subTest("Test all ids are unique"):
            all_ids = [location.code_without_offset for location in locations]
            unique_ids = set(all_ids)
            self.assertEqual(len(all_ids), len(unique_ids))

        with self.subTest("Test all names are unique"):
            all_names = [location.name for location in locations]
            unique_names = set(all_names)
            self.assertEqual(len(all_names), len(unique_names))

        with self.subTest("Test all mod names are valid"):
            content_packs = {content_pack for location in locations for content_pack in location.content_packs}
            for content_pack in content_packs:
                self.assertIn(content_pack, all_content_pack_names)

        with self.subTest("Test all craftsanity locations are either craft or recipe"):
            for location in locations:
                if LocationTags.CRAFTSANITY not in location.tags:
                    continue
                self.assertTrue(LocationTags.CRAFTSANITY_CRAFT in location.tags or LocationTags.CRAFTSANITY_RECIPE in location.tags)
