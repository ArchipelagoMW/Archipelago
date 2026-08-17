import unittest

from ..item import item_descriptions, item_tables


class TestItemDescriptions(unittest.TestCase):
    def test_all_items_have_description(self) -> None:
        for item_name in item_tables.item_table:
            self.assertIn(item_name, item_descriptions.item_descriptions)
    
    def test_all_descriptions_refer_to_item_and_end_in_dot(self) -> None:
        for item_name, item_desc in item_descriptions.item_descriptions.items():
            self.assertIn(item_name, item_tables.item_table)
            self.assertEqual(item_desc.strip()[-1], '.', msg=f"{item_name}'s item description does not end in a '.': '{item_desc}'")
    
    def test_item_descriptions_follow_single_space_after_period_style(self) -> None:
        for item_name, item_desc in item_descriptions.item_descriptions.items():
            self.assertNotIn('.  ', item_desc, f"Double-space after period in description for {item_name}")
