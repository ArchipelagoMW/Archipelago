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
