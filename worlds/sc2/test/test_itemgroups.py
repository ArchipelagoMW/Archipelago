"""
Unit tests for ItemGroups.py
"""

import unittest
from .. import ItemGroups, Items

class ItemGroupsUnitTests(unittest.TestCase):
    def test_all_production_structure_groups_capture_all_units(self) -> None:
        self.assertCountEqual(
            ItemGroups.terran_units,
            ItemGroups.barracks_units + ItemGroups.factory_units + ItemGroups.starport_units + ItemGroups.terran_mercenaries
        )
        self.assertCountEqual(
            ItemGroups.protoss_units,
            ItemGroups.gateway_units + ItemGroups.robo_units + ItemGroups.stargate_units
        )
    
    def test_terran_original_progressive_group_fully_contained_in_wol_upgrades(self) -> None:
        for item_name in ItemGroups.terran_original_progressive_upgrades:
            self.assertIn(Items.item_table[item_name].type, (Items.TerranItemType.Progressive, Items.TerranItemType.Progressive_2), f"{item_name} is not progressive")
            self.assertIn(item_name, ItemGroups.wol_upgrades)
    
    def test_all_items_in_stimpack_group_are_stimpacks(self) -> None:
        for item_name in ItemGroups.terran_stimpacks:
            self.assertIn("Stimpack", item_name)

    def test_all_item_group_names_have_a_group_defined(self) -> None:
        for var_name, display_name in ItemGroups.ItemGroupNames.__dict__.items():
            if var_name.startswith("_"):
                continue
            assert display_name in ItemGroups.item_name_groups
