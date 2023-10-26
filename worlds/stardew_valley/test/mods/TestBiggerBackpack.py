from .. import SVTestBase
from ... import options
from ...mods.mod_data import ModNames


class TestBiggerBackpackVanilla(SVTestBase):
    options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_vanilla,
               options.Mods.internal_name: ModNames.big_backpack}

    def test_no_backpack(self):
        # no items
        item_names = {item.name for item in self.multiworld.get_items()}
        self.assertNotIn("Progressive Backpack", item_names)

        # no locations
        location_names = {location.name for location in self.multiworld.get_locations()}
        self.assertNotIn("Large Pack", location_names)
        self.assertNotIn("Deluxe Pack", location_names)
        self.assertNotIn("Premium Pack", location_names)


class TestBiggerBackpackProgressive(SVTestBase):
    options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_progressive,
               options.Mods.internal_name: ModNames.big_backpack}

    def test_backpack(self):
        # 3 items
        item_names = [item.name for item in self.multiworld.get_items()]
        self.assertEqual(item_names.count("Progressive Backpack"), 3)

        # 3 locations
        location_names = {location.name for location in self.multiworld.get_locations()}
        self.assertIn("Large Pack", location_names)
        self.assertIn("Deluxe Pack", location_names)
        self.assertIn("Premium Pack", location_names)


class TestBiggerBackpackEarlyProgressive(SVTestBase):
    options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_early_progressive,
               options.Mods.internal_name: ModNames.big_backpack}

    def test_backpack(self):
        # 3 items
        item_names = [item.name for item in self.multiworld.get_items()]
        self.assertEqual(item_names.count("Progressive Backpack"), 3)

        # 3 locations
        location_names = {location.name for location in self.multiworld.get_locations()}
        self.assertIn("Large Pack", location_names)
        self.assertIn("Deluxe Pack", location_names)
        self.assertIn("Premium Pack", location_names)

        # is early
        self.assertIn("Progressive Backpack", self.multiworld.early_items[1])
