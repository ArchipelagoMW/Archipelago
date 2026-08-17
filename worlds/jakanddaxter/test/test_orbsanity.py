from .bases import JakAndDaxterTestBase
from ..items import orb_item_table


class NoOrbsanityTest(JakAndDaxterTestBase):
    options = {
        "enable_orbsanity": 0,  # Off
        "level_orbsanity_bundle_size": 25,
        "global_orbsanity_bundle_size": 16
    }

    def test_orb_bundles_not_exist_in_pool(self):
        for bundle in orb_item_table:
            self.assertNotIn(orb_item_table[bundle], {item.name for item in self.multiworld.itempool})

    def test_orb_bundle_count(self):
        bundle_name = orb_item_table[self.options["level_orbsanity_bundle_size"]]
        count = len([item.name for item in self.multiworld.itempool if item.name == bundle_name])
        self.assertEqual(0, count)

        bundle_name = orb_item_table[self.options["global_orbsanity_bundle_size"]]
        count = len([item.name for item in self.multiworld.itempool if item.name == bundle_name])
        self.assertEqual(0, count)


class PerLevelOrbsanityTest(JakAndDaxterTestBase):
    options = {
        "enable_orbsanity": 1,  # Per Level
        "level_orbsanity_bundle_size": 25
    }

    def test_orb_bundles_exist_in_pool(self):
        for bundle in orb_item_table:
            if bundle == self.options["level_orbsanity_bundle_size"]:
                self.assertIn(orb_item_table[bundle], {item.name for item in self.multiworld.itempool})
            else:
                self.assertNotIn(orb_item_table[bundle], {item.name for item in self.multiworld.itempool})

    def test_orb_bundle_count(self):
        bundle_name = orb_item_table[self.options["level_orbsanity_bundle_size"]]
        count = len([item.name for item in self.multiworld.itempool if item.name == bundle_name])
        self.assertEqual(80, count)


class GlobalOrbsanityTest(JakAndDaxterTestBase):
    options = {
        "enable_orbsanity": 2,  # Global
        "global_orbsanity_bundle_size": 16
    }

    def test_orb_bundles_exist_in_pool(self):
        for bundle in orb_item_table:
            if bundle == self.options["global_orbsanity_bundle_size"]:
                self.assertIn(orb_item_table[bundle], {item.name for item in self.multiworld.itempool})
            else:
                self.assertNotIn(orb_item_table[bundle], {item.name for item in self.multiworld.itempool})

    def test_orb_bundle_count(self):
        bundle_name = orb_item_table[self.options["global_orbsanity_bundle_size"]]
        count = len([item.name for item in self.multiworld.itempool if item.name == bundle_name])
        self.assertEqual(125, count)
