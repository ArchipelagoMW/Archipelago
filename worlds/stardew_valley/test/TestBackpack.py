from .bases import SVTestBase
from .. import options


class TestBackpackVanilla(SVTestBase):
    options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_vanilla}

    def test_no_backpack(self):
        with self.subTest("no items"):
            item_names = {item.name for item in self.multiworld.get_items()}
            self.assertNotIn("Progressive Backpack", item_names)

        with self.subTest("no locations"):
            location_names = {location.name for location in self.multiworld.get_locations()}
            self.assertNotIn("Large Pack", location_names)
            self.assertNotIn("Deluxe Pack", location_names)


class TestBackpackProgressive(SVTestBase):
    options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_progressive}

    def test_backpack(self):
        with self.subTest(check="has items"):
            item_names = [item.name for item in self.multiworld.get_items()]
            self.assertEqual(item_names.count("Progressive Backpack"), 2)

        with self.subTest(check="has locations"):
            location_names = {location.name for location in self.multiworld.get_locations()}
            self.assertIn("Large Pack", location_names)
            self.assertIn("Deluxe Pack", location_names)


class TestBackpackEarlyProgressive(TestBackpackProgressive):
    options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_early_progressive}

    @property
    def run_default_tests(self) -> bool:
        # EarlyProgressive is default
        return False

    def test_backpack(self):
        super().test_backpack()

        with self.subTest(check="is early"):
            self.assertIn("Progressive Backpack", self.multiworld.early_items[1])


class TestBackpackSplit1(SVTestBase):
    options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_progressive,
               options.BackpackSize.internal_name: options.BackpackSize.option_1}

    def test_backpack(self):
        with self.subTest(check="has items"):
            item_names = [item.name for item in self.multiworld.get_items()]
            self.assertEqual(item_names.count("Progressive Backpack"), 24)

        with self.subTest(check="has locations"):
            location_names = {location.name for location in self.multiworld.get_locations()}
            self.assertNotIn("Large Pack", location_names)
            self.assertNotIn("Deluxe Pack", location_names)
            for i in range(1, 13):
                self.assertIn(f"Large Pack {i}", location_names)
                self.assertIn(f"Deluxe Pack {i}", location_names)


class TestBackpackSplit2(SVTestBase):
    options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_progressive,
               options.BackpackSize.internal_name: options.BackpackSize.option_2}

    def test_backpack(self):
        with self.subTest(check="has items"):
            item_names = [item.name for item in self.multiworld.get_items()]
            self.assertEqual(item_names.count("Progressive Backpack"), 12)

        with self.subTest(check="has locations"):
            location_names = {location.name for location in self.multiworld.get_locations()}
            self.assertNotIn("Large Pack", location_names)
            self.assertNotIn("Deluxe Pack", location_names)
            for i in range(1, 7):
                self.assertIn(f"Large Pack {i}", location_names)
                self.assertIn(f"Deluxe Pack {i}", location_names)
            for i in range(7, 13):
                self.assertNotIn(f"Large Pack {i}", location_names)
                self.assertNotIn(f"Deluxe Pack {i}", location_names)


class TestBackpackSplit4(SVTestBase):
    options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_progressive,
               options.BackpackSize.internal_name: options.BackpackSize.option_4}

    def test_backpack(self):
        with self.subTest(check="has items"):
            item_names = [item.name for item in self.multiworld.get_items()]
            self.assertEqual(item_names.count("Progressive Backpack"), 6)

        with self.subTest(check="has locations"):
            location_names = {location.name for location in self.multiworld.get_locations()}
            self.assertNotIn("Large Pack", location_names)
            self.assertNotIn("Deluxe Pack", location_names)
            for i in range(1, 4):
                self.assertIn(f"Large Pack {i}", location_names)
                self.assertIn(f"Deluxe Pack {i}", location_names)
            for i in range(4, 13):
                self.assertNotIn(f"Large Pack {i}", location_names)
                self.assertNotIn(f"Deluxe Pack {i}", location_names)


class TestBackpackSplit6(SVTestBase):
    options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_progressive,
               options.BackpackSize.internal_name: options.BackpackSize.option_6}

    def test_backpack(self):
        with self.subTest(check="has items"):
            item_names = [item.name for item in self.multiworld.get_items()]
            self.assertEqual(item_names.count("Progressive Backpack"), 4)

        with self.subTest(check="has locations"):
            location_names = {location.name for location in self.multiworld.get_locations()}
            self.assertNotIn("Large Pack", location_names)
            self.assertNotIn("Deluxe Pack", location_names)
            for i in range(1, 3):
                self.assertIn(f"Large Pack {i}", location_names)
                self.assertIn(f"Deluxe Pack {i}", location_names)
            for i in range(3, 13):
                self.assertNotIn(f"Large Pack {i}", location_names)
                self.assertNotIn(f"Deluxe Pack {i}", location_names)
