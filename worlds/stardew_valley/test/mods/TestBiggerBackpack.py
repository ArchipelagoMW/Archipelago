from ..bases import SVTestBase
from ...mods.mod_data import ModNames
from ...options import Mods, BackpackProgression, BackpackSize


class TestBiggerBackpackVanilla(SVTestBase):
    options = {
        BackpackProgression.internal_name: BackpackProgression.option_vanilla,
        BackpackSize.internal_name: BackpackSize.option_12,
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
        BackpackSize.internal_name: BackpackSize.option_12,
        Mods.internal_name: ModNames.big_backpack,
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
        BackpackSize.internal_name: BackpackSize.option_12,
        Mods.internal_name: ModNames.big_backpack
    }

    def test_backpack(self):
        super().test_backpack()

        with self.subTest(check="is early"):
            self.assertIn("Progressive Backpack", self.multiworld.early_items[1])


class TestBiggerBackpackSplit1(SVTestBase):
    options = {BackpackProgression.internal_name: BackpackProgression.option_progressive,
               BackpackSize.internal_name: BackpackSize.option_1,
               Mods.internal_name: ModNames.big_backpack}

    def test_backpack(self):
        with self.subTest(check="has items"):
            item_names = [item.name for item in self.multiworld.get_items()]
            self.assertEqual(item_names.count("Progressive Backpack"), 36)

        with self.subTest(check="has locations"):
            location_names = {location.name for location in self.multiworld.get_locations()}
            self.assertNotIn("Large Pack", location_names)
            self.assertNotIn("Deluxe Pack", location_names)
            self.assertNotIn("Premium Pack", location_names)
            for i in range(1, 13):
                self.assertIn(f"Large Pack {i}", location_names)
                self.assertIn(f"Deluxe Pack {i}", location_names)
                self.assertIn(f"Premium Pack {i}", location_names)


class TestBackpackSplit2(SVTestBase):
    options = {BackpackProgression.internal_name: BackpackProgression.option_progressive,
               BackpackSize.internal_name: BackpackSize.option_2,
               Mods.internal_name: ModNames.big_backpack}

    def test_backpack(self):
        with self.subTest(check="has items"):
            item_names = [item.name for item in self.multiworld.get_items()]
            self.assertEqual(item_names.count("Progressive Backpack"), 18)

        with self.subTest(check="has locations"):
            location_names = {location.name for location in self.multiworld.get_locations()}
            self.assertNotIn("Large Pack", location_names)
            self.assertNotIn("Deluxe Pack", location_names)
            self.assertNotIn("Premium Pack", location_names)
            for i in range(1, 7):
                self.assertIn(f"Large Pack {i}", location_names)
                self.assertIn(f"Deluxe Pack {i}", location_names)
                self.assertIn(f"Premium Pack {i}", location_names)
            for i in range(7, 13):
                self.assertNotIn(f"Large Pack {i}", location_names)
                self.assertNotIn(f"Deluxe Pack {i}", location_names)
                self.assertNotIn(f"Premium Pack {i}", location_names)


class TestBackpackSplit4(SVTestBase):
    options = {BackpackProgression.internal_name: BackpackProgression.option_progressive,
               BackpackSize.internal_name: BackpackSize.option_4,
               Mods.internal_name: ModNames.big_backpack}

    def test_backpack(self):
        with self.subTest(check="has items"):
            item_names = [item.name for item in self.multiworld.get_items()]
            self.assertEqual(item_names.count("Progressive Backpack"), 9)

        with self.subTest(check="has locations"):
            location_names = {location.name for location in self.multiworld.get_locations()}
            self.assertNotIn("Large Pack", location_names)
            self.assertNotIn("Deluxe Pack", location_names)
            self.assertNotIn("Premium Pack", location_names)
            for i in range(1, 4):
                self.assertIn(f"Large Pack {i}", location_names)
                self.assertIn(f"Deluxe Pack {i}", location_names)
                self.assertIn(f"Premium Pack {i}", location_names)
            for i in range(4, 13):
                self.assertNotIn(f"Large Pack {i}", location_names)
                self.assertNotIn(f"Deluxe Pack {i}", location_names)
                self.assertNotIn(f"Premium Pack {i}", location_names)


class TestBackpackSplit6(SVTestBase):
    options = {BackpackProgression.internal_name: BackpackProgression.option_progressive,
               BackpackSize.internal_name: BackpackSize.option_6,
               Mods.internal_name: ModNames.big_backpack}

    def test_backpack(self):
        with self.subTest(check="has items"):
            item_names = [item.name for item in self.multiworld.get_items()]
            self.assertEqual(item_names.count("Progressive Backpack"), 6)

        with self.subTest(check="has locations"):
            location_names = {location.name for location in self.multiworld.get_locations()}
            self.assertNotIn("Large Pack", location_names)
            self.assertNotIn("Deluxe Pack", location_names)
            self.assertNotIn("Premium Pack", location_names)
            for i in range(1, 3):
                self.assertIn(f"Large Pack {i}", location_names)
                self.assertIn(f"Deluxe Pack {i}", location_names)
                self.assertIn(f"Premium Pack {i}", location_names)
            for i in range(3, 13):
                self.assertNotIn(f"Large Pack {i}", location_names)
                self.assertNotIn(f"Deluxe Pack {i}", location_names)
                self.assertNotIn(f"Premium Pack {i}", location_names)
