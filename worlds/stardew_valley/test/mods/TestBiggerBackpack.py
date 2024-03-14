from .. import SVTestBase
from ... import options
from ...mods.mod_data import ModNames


class TestBiggerBackpackVanilla(SVTestBase):
    options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_vanilla,
               options.Mods.internal_name: ModNames.big_backpack}

    def test_no_backpack(self):
        with self.subTest(check="no items"):
            item_names = {item.name for item in self.multiworld.get_items()}
            self.assertNotIn("Progressive Backpack", item_names)

        with self.subTest(check="no locations"):
            location_names = {location.name for location in self.multiworld.get_locations()}
            self.assertNotIn("Large Pack", location_names)
            self.assertNotIn("Deluxe Pack", location_names)
            self.assertNotIn("Premium Pack", location_names)


class TestBiggerBackpackProgressive(SVTestBase):
    options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_progressive,
               options.Mods.internal_name: ModNames.big_backpack}

    def test_backpack(self):
        with self.subTest(check="has items"):
            item_names = [item.name for item in self.multiworld.get_items()]
            self.assertEqual(item_names.count("Progressive Backpack"), 3)

        with self.subTest(check="has locations"):
            location_names = {location.name for location in self.multiworld.get_locations()}
            self.assertIn("Large Pack", location_names)
            self.assertIn("Deluxe Pack", location_names)
            self.assertIn("Premium Pack", location_names)


class TestBiggerBackpackEarlyProgressive(TestBiggerBackpackProgressive):
    options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_early_progressive,
               options.Mods.internal_name: ModNames.big_backpack}

    def test_backpack(self):
        super().test_backpack()

        with self.subTest(check="is early"):
            self.assertIn("Progressive Backpack", self.multiworld.early_items[1])
