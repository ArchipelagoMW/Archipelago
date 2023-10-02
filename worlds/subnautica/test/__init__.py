import unittest
from worlds import subnautica


class SubnauticaTest(unittest.TestCase):
    # This is an assumption in the mod side
    scancutoff: int = 33999

    def testIDRange(self):
        for name, id in subnautica.SubnauticaWorld.location_name_to_id.items():
            with self.subTest(location=name):
                if "Scan" in name:
                    self.assertLess(self.scancutoff, id)
                else:
                    self.assertGreater(self.scancutoff, id)

    def testGroupAssociation(self):
        from worlds.subnautica import Items
        for item_id, item_data in Items.item_table.items():
            if item_data.type == Items.ItemType.group:
                with self.subTest(item=item_data.name):
                    self.assertIn(item_id, Items.group_items)
        for item_id in Items.group_items:
            with self.subTest(item_id=item_id):
                self.assertEqual(Items.item_table[item_id].type, Items.ItemType.group)
