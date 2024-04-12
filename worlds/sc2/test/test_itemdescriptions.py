import unittest

from .. import Items
from .. import ItemDescriptions

class TestItemDescriptions(unittest.TestCase):
    def test_all_items_have_description(self):
        for item_name in Items.item_table:
            self.assertIn(item_name, ItemDescriptions.item_descriptions)
    
    def test_all_descriptions_refer_to_item_and_end_in_dot(self):
        for item_name, item_desc in ItemDescriptions.item_descriptions.items():
            self.assertIn(item_name, Items.item_table)
            self.assertEqual(item_desc.strip()[-1], '.', msg=f"{item_name}'s item description does not end in a '.': '{item_desc}'")
