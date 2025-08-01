from ..bases import SVTestBase
from ...mods.mod_data import ModNames
from ...options import Mods, BackpackProgression


class TestBiggerBackpackVanilla(SVTestBase):
    options = {
        BackpackProgression.internal_name: BackpackProgression.option_vanilla,
        Mods.internal_name: ModNames.big_backpack
    }

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
    options = {
        BackpackProgression.internal_name: BackpackProgression.option_progressive,
        Mods.internal_name: ModNames.big_backpack
    }

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
    options = {
        BackpackProgression.internal_name: BackpackProgression.option_early_progressive,
        Mods.internal_name: ModNames.big_backpack
    }

    def test_backpack(self):
        super().test_backpack()

        with self.subTest(check="is early"):
            self.assertIn("Progressive Backpack", self.multiworld.early_items[1])
