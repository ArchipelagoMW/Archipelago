import unittest
from typing import List, Set

from worlds.sc2 import items


class TestItems(unittest.TestCase):
    def test_grouped_upgrades_number(self) -> None:
        """
        Tests if grouped upgrades have set number correctly
        :return:
        """
        bundled_items = items.upgrade_bundles.keys()
        bundled_item_data = [items.get_full_item_list()[item_name] for item_name in bundled_items]
        bundled_item_numbers = [item_data.number for item_data in bundled_item_data]

        check_numbers = [number == -1 for number in bundled_item_numbers]

        self.assertNotIn(False, check_numbers)

    def test_non_grouped_upgrades_number(self) -> None:
        """
        Checks if non-grouped upgrades number is set correctly thus can be sent into the game.
        :return:
        """
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
        """
        Checks if there are no bundles within bundles.
        :return:
        """
        bundled_items = items.upgrade_bundles.keys()
        bundle_elements: List[str] = [item_name for values in items.upgrade_bundles.values() for item_name in values]

        for element in bundle_elements:
            self.assertNotIn(element, bundled_items)

    def test_weapon_armor_level(self) -> None:
        """
        Checks if Weapon/Armor upgrade level is correctly set to all Weapon/Armor upgrade items.
        :return:
        """
        weapon_armor_upgrades = [item for item in items.get_full_item_list() if items.get_item_table()[item].type in items.upgrade_item_types]

        for weapon_armor_upgrade in weapon_armor_upgrades:
            self.assertEqual(items.get_full_item_list()[weapon_armor_upgrade].quantity, items.WEAPON_ARMOR_UPGRADE_MAX_LEVEL)

    def test_item_ids_distinct(self) -> None:
        """
        Verifies if there are no duplicates of item ID.
        :return:
        """
        item_ids: Set[int] = {items.get_full_item_list()[item_name].code for item_name in items.get_full_item_list()}

        self.assertEqual(len(item_ids), len(items.get_full_item_list()))

    def test_number_distinct_in_item_type(self) -> None:
        """
        Tests if each item is distinct for sending into the mod.
        :return:
        """
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

    def test_progressive_has_quantity(self) -> None:
        """
        Checks if the quantity attribute has been set for progressive items.
        :return:
        """
        progressive_groups: List[items.ItemTypeEnum] = [
            items.TerranItemType.Progressive,
            items.TerranItemType.Progressive_2,
            items.ProtossItemType.Progressive,
            items.ZergItemType.Progressive
        ]

        quantities: List[int] = [
            items.get_full_item_list()[item].quantity for item in items.get_full_item_list()
            if items.get_full_item_list()[item].type in progressive_groups
        ]

        self.assertNotIn(1, quantities)

    def test_non_progressive_quantity(self) -> None:
        """
        Check if non-progressive items have quantity at most 1.
        :return:
        """
        non_progressive_single_entity_groups: List[items.ItemTypeEnum] = [
            # Terran
            items.TerranItemType.Unit,
            items.TerranItemType.Mercenary,
            items.TerranItemType.Armory_1,
            items.TerranItemType.Armory_2,
            items.TerranItemType.Armory_3,
            items.TerranItemType.Armory_4,
            items.TerranItemType.Armory_5,
            items.TerranItemType.Armory_6,
            items.TerranItemType.Armory_7,
            items.TerranItemType.Building,
            items.TerranItemType.Laboratory,
            items.TerranItemType.Nova_Gear,
            # Zerg
            items.ZergItemType.Unit,
            items.ZergItemType.Mercenary,
            items.ZergItemType.Morph,
            items.ZergItemType.Strain,
            items.ZergItemType.Mutation_1,
            items.ZergItemType.Mutation_2,
            items.ZergItemType.Mutation_3,
            items.ZergItemType.Evolution_Pit,
            items.ZergItemType.Ability,
            # Protoss
            items.ProtossItemType.Unit,
            items.ProtossItemType.Unit_2,
            items.ProtossItemType.Building,
            items.ProtossItemType.Forge_1,
            items.ProtossItemType.Forge_2,
            items.ProtossItemType.Forge_3,
            items.ProtossItemType.Solarite_Core,
            items.ProtossItemType.Spear_Of_Adun
        ]

        quantities: List[int] = [
            items.get_full_item_list()[item].quantity for item in items.get_full_item_list()
            if items.get_full_item_list()[item].type in non_progressive_single_entity_groups
        ]

        for quantity in quantities:
            self.assertLessEqual(quantity, 1)

    def test_item_number_less_than_30(self) -> None:
        """
        Checks if all item numbers are within bounds supported by game mod.
        :return:
        """
        not_checked_item_types: List[items.ItemTypeEnum] = [
            items.ZergItemType.Level
        ]
        items_to_check: List[str] = [
            item for item in items.get_full_item_list()
            if items.get_full_item_list()[item].type not in not_checked_item_types
        ]

        for item in items_to_check:
            item_number = items.get_full_item_list()[item].number
            self.assertLess(item_number, 30)
