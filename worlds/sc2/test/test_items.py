import unittest
from typing import List, Set

from worlds.sc2 import items


class TestItems(unittest.TestCase):
    def test_grouped_upgrades_number(self) -> None:
        bundled_items = items.upgrade_bundles.keys()
        bundled_item_data = [items.get_full_item_list()[item_name] for item_name in bundled_items]
        bundled_item_numbers = [item_data.number for item_data in bundled_item_data]

        check_numbers = [number == -1 for number in bundled_item_numbers]

        self.assertNotIn(False, check_numbers)

    def test_non_grouped_upgrades_number(self) -> None:
        check_modulo = 4
        bundled_items = items.upgrade_bundles.keys()
        non_bundled_upgrades = [
            item_name for item_name in items.get_full_item_list().keys()
            if (item_name not in bundled_items
                and items.get_full_item_list()[item_name].type in items.upgrade_item_types)
        ]
        non_bundled_upgrade_data = [items.get_full_item_list()[item_name] for item_name in non_bundled_upgrades]
        non_bundled_upgrade_numbers = [item_data.number for item_data in non_bundled_upgrade_data]

        check_numbers = [number % check_modulo == 0 for number in non_bundled_upgrade_numbers]

        self.assertNotIn(False, check_numbers)

    def test_bundles_contain_only_basic_elements(self) -> None:
        bundled_items = items.upgrade_bundles.keys()
        bundle_elements: List[str] = [item_name for values in items.upgrade_bundles.values() for item_name in values]

        for element in bundle_elements:
            self.assertNotIn(element, bundled_items)

    def test_weapon_armor_level(self) -> None:
        weapon_armor_upgrades = [item for item in items.get_full_item_list() if items.get_item_table()[item].type in items.upgrade_item_types]

        for weapon_armor_upgrade in weapon_armor_upgrades:
            self.assertEqual(items.get_full_item_list()[weapon_armor_upgrade].quantity, items.WEAPON_ARMOR_UPGRADE_MAX_LEVEL)

    def test_item_ids_distinct(self) -> None:
        item_ids: Set[int] = {items.get_full_item_list()[item_name].code for item_name in items.get_full_item_list()}

        self.assertEqual(len(item_ids), len(items.get_full_item_list()))

    def test_number_distinct_in_item_type(self) -> None:
        item_types: List[items.ItemTypeEnum] = [
            *[item.value for item in items.TerranItemType],
            *[item.value for item in items.ZergItemType],
            *[item.value for item in items.ProtossItemType],
            *[item.value for item in items.FactionlessItemType]
        ]

        self.assertGreater(len(item_types), 0)

        for item_type in item_types:
            item_names: List[str] = [
                item_name for item_name in items.get_full_item_list()
                if items.get_full_item_list()[item_name].number >= 0  # Negative numbers have special meaning
                   and items.get_full_item_list()[item_name].type == item_type
            ]
            item_numbers: Set[int] = {items.get_full_item_list()[item_name] for item_name in item_names}

            self.assertEqual(len(item_names), len(item_numbers))
