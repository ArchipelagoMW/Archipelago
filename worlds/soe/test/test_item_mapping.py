from unittest import TestCase
from .. import SoEWorld


class TestMapping(TestCase):
    def test_atlas_medallion_name_group(self) -> None:
        """
        Test that we used the pyevermizer name for Atlas Medallion (not Amulet) in item groups.
        """
        self.assertIn("Any Atlas Medallion", SoEWorld.item_name_groups)

    def test_atlas_medallion_name_items(self) -> None:
        """
        Test that we used the pyevermizer name for Atlas Medallion (not Amulet) in items.
        """
        found_medallion = False
        for name in SoEWorld.item_name_to_id:
            self.assertNotIn("Atlas Amulet", name, "Expected Atlas Medallion, not Amulet")
            if "Atlas Medallion" in name:
                found_medallion = True
        self.assertTrue(found_medallion, "Did not find Atlas Medallion in items")
