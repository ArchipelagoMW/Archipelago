from .bases import SVTestBase
from .. import options, StartWithoutOptionName


class TestBackpackBase(SVTestBase):
    expected_starting_backpacks: int = 0
    expected_total_backpacks: int = 2

    def test_has_correct_number_of_backpacks(self):
        backpack_item_name = "Progressive Backpack"
        item_names = [item.name for item in self.multiworld.get_items()]
        precollected_items = [item.name for item in self.multiworld.precollected_items[self.player]]
        if self.expected_total_backpacks <= 0:
            self.assertNotIn(backpack_item_name, item_names)
        else:
            self.assertEqual(item_names.count(backpack_item_name), self.expected_total_backpacks - self.expected_starting_backpacks)
        if self.expected_starting_backpacks <= 0:
            self.assertNotIn(backpack_item_name, precollected_items)
        else:
            self.assertEqual(precollected_items.count(backpack_item_name), self.expected_starting_backpacks)


class TestBackpackVanilla(TestBackpackBase):
    options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_vanilla}
    expected_total_backpacks = 0

    def test_no_backpacks(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        self.assertNotIn("Small Pack", location_names)
        self.assertNotIn("Large Pack", location_names)
        self.assertNotIn("Deluxe Pack", location_names)


class TestBackpackProgressive(TestBackpackBase):
    options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_progressive}
    expected_total_backpacks = 2

    def test_has_correct_backpack_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        self.assertNotIn("Small Pack", location_names)
        self.assertIn("Large Pack", location_names)
        self.assertIn("Deluxe Pack", location_names)


class TestBackpackEarlyProgressive(TestBackpackProgressive):
    options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_early_progressive}

    @property
    def run_default_tests(self) -> bool:
        # EarlyProgressive is default
        return False

    def test_has_correct_backpack_locations(self):
        super().test_has_correct_backpack_locations()

        with self.subTest(check="is early"):
            self.assertIn("Progressive Backpack", self.multiworld.early_items[1])


class TestBackpackSplit1(TestBackpackBase):
    options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_progressive,
               options.BackpackSize.internal_name: options.BackpackSize.option_1}
    expected_total_backpacks = 24

    def test_has_correct_backpack_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        self.assertNotIn("Small Pack", location_names)
        self.assertNotIn("Large Pack", location_names)
        self.assertNotIn("Deluxe Pack", location_names)
        for i in range(1, 13):
            self.assertNotIn(f"Small Pack {i}", location_names)
            self.assertIn(f"Large Pack {i}", location_names)
            self.assertIn(f"Deluxe Pack {i}", location_names)


class TestBackpackSplit2(TestBackpackBase):
    options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_progressive,
               options.BackpackSize.internal_name: options.BackpackSize.option_2}
    expected_total_backpacks = 12

    def test_has_correct_backpack_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        self.assertNotIn("Small Pack", location_names)
        self.assertNotIn("Large Pack", location_names)
        self.assertNotIn("Deluxe Pack", location_names)
        for i in range(1, 7):
            self.assertNotIn(f"Small Pack {i}", location_names)
            self.assertIn(f"Large Pack {i}", location_names)
            self.assertIn(f"Deluxe Pack {i}", location_names)
        for i in range(7, 13):
            self.assertNotIn(f"Small Pack {i}", location_names)
            self.assertNotIn(f"Large Pack {i}", location_names)
            self.assertNotIn(f"Deluxe Pack {i}", location_names)


class TestBackpackSplit4(TestBackpackBase):
    options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_progressive,
               options.BackpackSize.internal_name: options.BackpackSize.option_4}
    expected_total_backpacks = 6

    def test_has_correct_backpack_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        self.assertNotIn("Small Pack", location_names)
        self.assertNotIn("Large Pack", location_names)
        self.assertNotIn("Deluxe Pack", location_names)
        for i in range(1, 4):
            self.assertNotIn(f"Small Pack {i}", location_names)
            self.assertIn(f"Large Pack {i}", location_names)
            self.assertIn(f"Deluxe Pack {i}", location_names)
        for i in range(4, 13):
            self.assertNotIn(f"Small Pack {i}", location_names)
            self.assertNotIn(f"Large Pack {i}", location_names)
            self.assertNotIn(f"Deluxe Pack {i}", location_names)


class TestBackpackSplit6(TestBackpackBase):
    options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_progressive,
               options.BackpackSize.internal_name: options.BackpackSize.option_6}
    expected_total_backpacks = 4

    def test_has_correct_backpack_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        self.assertNotIn("Small Pack", location_names)
        self.assertNotIn("Large Pack", location_names)
        self.assertNotIn("Deluxe Pack", location_names)
        for i in range(1, 3):
            self.assertNotIn(f"Small Pack {i}", location_names)
            self.assertIn(f"Large Pack {i}", location_names)
            self.assertIn(f"Deluxe Pack {i}", location_names)
        for i in range(3, 13):
            self.assertNotIn(f"Small Pack {i}", location_names)
            self.assertNotIn(f"Large Pack {i}", location_names)
            self.assertNotIn(f"Deluxe Pack {i}", location_names)


class TestStartWithoutBackpackSize1(TestBackpackBase):
    options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_progressive,
               options.BackpackSize.internal_name: options.BackpackSize.option_1,
               options.StartWithout.internal_name: frozenset({StartWithoutOptionName.backpack})}
    expected_starting_backpacks = 6
    expected_total_backpacks = 36

    def test_has_correct_backpack_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        self.assertNotIn("Small Pack", location_names)
        self.assertNotIn("Large Pack", location_names)
        self.assertNotIn("Deluxe Pack", location_names)
        for i in range(1, 13):
            self.assertIn(f"Small Pack {i}", location_names)
            self.assertIn(f"Large Pack {i}", location_names)
            self.assertIn(f"Deluxe Pack {i}", location_names)


class TestStartWithoutBackpackSize3(TestBackpackBase):
    options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_progressive,
               options.BackpackSize.internal_name: options.BackpackSize.option_3,
               options.StartWithout.internal_name: frozenset({StartWithoutOptionName.backpack})}
    expected_starting_backpacks = 2
    expected_total_backpacks = 12

    def test_has_correct_backpack_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        self.assertNotIn("Small Pack", location_names)
        self.assertNotIn("Large Pack", location_names)
        self.assertNotIn("Deluxe Pack", location_names)
        for i in range(1, 5):
            self.assertIn(f"Small Pack {i}", location_names)
            self.assertIn(f"Large Pack {i}", location_names)
            self.assertIn(f"Deluxe Pack {i}", location_names)
        for i in range(5, 13):
            self.assertNotIn(f"Small Pack {i}", location_names)
            self.assertNotIn(f"Large Pack {i}", location_names)
            self.assertNotIn(f"Deluxe Pack {i}", location_names)


class TestStartWithoutBackpackSize4(TestBackpackBase):
    options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_progressive,
               options.BackpackSize.internal_name: options.BackpackSize.option_4,
               options.StartWithout.internal_name: frozenset({StartWithoutOptionName.backpack})}
    expected_starting_backpacks = 2
    expected_total_backpacks = 9

    def test_has_correct_backpack_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        self.assertNotIn("Small Pack", location_names)
        self.assertNotIn("Large Pack", location_names)
        self.assertNotIn("Deluxe Pack", location_names)
        for i in range(1, 4):
            self.assertIn(f"Small Pack {i}", location_names)
            self.assertIn(f"Large Pack {i}", location_names)
            self.assertIn(f"Deluxe Pack {i}", location_names)
        for i in range(4, 13):
            self.assertNotIn(f"Small Pack {i}", location_names)
            self.assertNotIn(f"Large Pack {i}", location_names)
            self.assertNotIn(f"Deluxe Pack {i}", location_names)


class TestStartWithoutBackpackSize12(TestBackpackBase):
    options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_progressive,
               options.BackpackSize.internal_name: options.BackpackSize.option_12,
               options.StartWithout.internal_name: frozenset({StartWithoutOptionName.backpack})}
    expected_starting_backpacks = 1
    expected_total_backpacks = 3

    def test_has_correct_backpack_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        self.assertIn("Small Pack", location_names)
        self.assertIn("Large Pack", location_names)
        self.assertIn("Deluxe Pack", location_names)
        for i in range(1, 13):
            self.assertNotIn(f"Small Pack {i}", location_names)
            self.assertNotIn(f"Large Pack {i}", location_names)
            self.assertNotIn(f"Deluxe Pack {i}", location_names)
