import unittest
from typing import List, Set

from ..item import item_tables


class TestItems(unittest.TestCase):
    def test_grouped_upgrades_number(self) -> None:
        """
        Tests if grouped upgrades have set number correctly
        """
        bundled_items = item_tables.upgrade_bundles.keys()
        bundled_item_data = [item_tables.get_full_item_list()[item_name] for item_name in bundled_items]
        bundled_item_numbers = [item_data.number for item_data in bundled_item_data]

        check_numbers = [number == -1 for number in bundled_item_numbers]

        self.assertNotIn(False, check_numbers)

    def test_non_grouped_upgrades_number(self) -> None:
        """
        Checks if non-grouped upgrades number is set correctly thus can be sent into the game.
        """
        check_modulo = 4
        bundled_items = item_tables.upgrade_bundles.keys()
        non_bundled_upgrades = [
            item_name for item_name in item_tables.get_full_item_list().keys()
            if (item_name not in bundled_items
                and item_tables.get_full_item_list()[item_name].type in item_tables.upgrade_item_types)
        ]
        non_bundled_upgrade_data = [item_tables.get_full_item_list()[item_name] for item_name in non_bundled_upgrades]
        non_bundled_upgrade_numbers = [item_data.number for item_data in non_bundled_upgrade_data]

        check_numbers = [number % check_modulo == 0 for number in non_bundled_upgrade_numbers]

        self.assertNotIn(False, check_numbers)

    def test_bundles_contain_only_basic_elements(self) -> None:
        """
        Checks if there are no bundles within bundles.
        """
        bundled_items = item_tables.upgrade_bundles.keys()
        bundle_elements: List[str] = [item_name for values in item_tables.upgrade_bundles.values() for item_name in values]

        for element in bundle_elements:
            self.assertNotIn(element, bundled_items)

    def test_weapon_armor_level(self) -> None:
        """
        Checks if Weapon/Armor upgrade level is correctly set to all Weapon/Armor upgrade items.
        """
        weapon_armor_upgrades = [item for item in item_tables.get_full_item_list() if item_tables.get_item_table()[item].type in item_tables.upgrade_item_types]

        for weapon_armor_upgrade in weapon_armor_upgrades:
            self.assertEqual(item_tables.get_full_item_list()[weapon_armor_upgrade].quantity, item_tables.WEAPON_ARMOR_UPGRADE_MAX_LEVEL)

    def test_item_ids_distinct(self) -> None:
        """
        Verifies if there are no duplicates of item ID.
        """
        item_ids: Set[int] = {item_tables.get_full_item_list()[item_name].code for item_name in item_tables.get_full_item_list()}

        self.assertEqual(len(item_ids), len(item_tables.get_full_item_list()))

    def test_number_distinct_in_item_type(self) -> None:
        """
        Tests if each item is distinct for sending into the mod.
        """
        item_types: List[item_tables.ItemTypeEnum] = [
            *[item.value for item in item_tables.TerranItemType],
            *[item.value for item in item_tables.ZergItemType],
            *[item.value for item in item_tables.ProtossItemType],
            *[item.value for item in item_tables.FactionlessItemType]
        ]

        self.assertGreater(len(item_types), 0)

        for item_type in item_types:
            item_names: List[str] = [
                item_name for item_name in item_tables.get_full_item_list()
                if item_tables.get_full_item_list()[item_name].number >= 0  # Negative numbers have special meaning
                   and item_tables.get_full_item_list()[item_name].type == item_type
            ]
            item_numbers: Set[int] = {item_tables.get_full_item_list()[item_name] for item_name in item_names}

            self.assertEqual(len(item_names), len(item_numbers))

    def test_progressive_has_quantity(self) -> None:
        """
        :return:
        """
        progressive_groups: List[item_tables.ItemTypeEnum] = [
            item_tables.TerranItemType.Progressive,
            item_tables.TerranItemType.Progressive_2,
            item_tables.ProtossItemType.Progressive,
            item_tables.ZergItemType.Progressive
        ]

        quantities: List[int] = [
            item_tables.get_full_item_list()[item].quantity for item in item_tables.get_full_item_list()
            if item_tables.get_full_item_list()[item].type in progressive_groups
        ]

        self.assertNotIn(1, quantities)

    def test_non_progressive_quantity(self) -> None:
        """
        Check if non-progressive items have quantity at most 1.
        """
        non_progressive_single_entity_groups: List[item_tables.ItemTypeEnum] = [
            # Terran
            item_tables.TerranItemType.Unit,
            item_tables.TerranItemType.Unit_2,
            item_tables.TerranItemType.Mercenary,
            item_tables.TerranItemType.Armory_1,
            item_tables.TerranItemType.Armory_2,
            item_tables.TerranItemType.Armory_3,
            item_tables.TerranItemType.Armory_4,
            item_tables.TerranItemType.Armory_5,
            item_tables.TerranItemType.Armory_6,
            item_tables.TerranItemType.Armory_7,
            item_tables.TerranItemType.Building,
            item_tables.TerranItemType.Laboratory,
            item_tables.TerranItemType.Nova_Gear,
            # Zerg
            item_tables.ZergItemType.Unit,
            item_tables.ZergItemType.Mercenary,
            item_tables.ZergItemType.Morph,
            item_tables.ZergItemType.Strain,
            item_tables.ZergItemType.Mutation_1,
            item_tables.ZergItemType.Mutation_2,
            item_tables.ZergItemType.Mutation_3,
            item_tables.ZergItemType.Evolution_Pit,
            item_tables.ZergItemType.Ability,
            # Protoss
            item_tables.ProtossItemType.Unit,
            item_tables.ProtossItemType.Unit_2,
            item_tables.ProtossItemType.Building,
            item_tables.ProtossItemType.Forge_1,
            item_tables.ProtossItemType.Forge_2,
            item_tables.ProtossItemType.Forge_3,
            item_tables.ProtossItemType.Forge_4,
            item_tables.ProtossItemType.Solarite_Core,
            item_tables.ProtossItemType.Spear_Of_Adun
        ]

        quantities: List[int] = [
            item_tables.get_full_item_list()[item].quantity for item in item_tables.get_full_item_list()
            if item_tables.get_full_item_list()[item].type in non_progressive_single_entity_groups
        ]

        for quantity in quantities:
            self.assertLessEqual(quantity, 1)

    def test_item_number_less_than_30(self) -> None:
        """
        Checks if all item numbers are within bounds supported by game mod.
        """
        not_checked_item_types: List[item_tables.ItemTypeEnum] = [
            item_tables.ZergItemType.Level
        ]
        items_to_check: List[str] = [
            item for item in item_tables.get_full_item_list()
            if item_tables.get_full_item_list()[item].type not in not_checked_item_types
        ]

        for item in items_to_check:
            item_number = item_tables.get_full_item_list()[item].number
            self.assertLess(item_number, 30)

