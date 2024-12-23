from copy import copy

from . import CMTestBase
from ..Rules import determine_difficulty
from ..Items import item_table


class MaterialStateTestBase(CMTestBase):

    def world_setup(self, *args, **kwargs) -> None:
        self.options = copy(self.options)
        self.options["goal"] = "single"
        self.options["difficulty"] = "grandmaster"
        super().world_setup(*args, **kwargs)

        # this class ultimately isn't trying to test this relatively simple function
        self.difficulty = determine_difficulty(self.world.options)

    def test_basic_fill(self) -> None:
        # this is mostly to demonstrate that collect fundamentally acquires the items and to show that setUp sets up
        self.assertEqual(0, self.multiworld.state.prog_items[self.player]["Progressive Pawn"])
        self.assertEqual(0, self.multiworld.state.prog_items[self.player]["Material"])
        self.collect_all_but("Progressive Pocket Gems", self.multiworld.state)
        self.assertEqual(
            len([item for item in self.multiworld.itempool if item.name == "Progressive Pawn"]),
            self.multiworld.state.prog_items[self.player]["Progressive Pawn"])


class TestSimpleMaterial(MaterialStateTestBase):
    """
    Checks that goal can be reached based on the math performed by collect()

    If this fails, it's not necessarily the fault of collect(), it might be that the generator isn't adding enough items
    """
    def test_no_options(self) -> None:
        self.collect_all_but("Progressive Pocket Gems", self.multiworld.state)
        past_material = self.multiworld.state.prog_items[self.player]["Material"]
        self.assertLessEqual(4150 * self.difficulty, past_material)
        self.assertGreaterEqual(4650 * self.difficulty, past_material)

    def test_exact_material(self) -> None:
        """Test that the material value matches exactly what we expect from summing all items."""
        # First collect everything
        self.collect_all_but("Progressive Pocket Gems", self.multiworld.state)
        actual_material = self.multiworld.state.prog_items[self.player]["Material"]
        
        # Calculate expected material by summing up each item's material value
        expected_material = 0
        for item_name, count in self.multiworld.state.prog_items[self.player].items():
            if item_name == "Material":  # Skip the material counter itself
                continue
            if item_name in item_table and item_table[item_name].material > 0:
                expected_material += item_table[item_name].material * count
        
        # Assert exact equality and print values if they don't match
        self.assertEqual(expected_material, actual_material, 
            f"Material mismatch: expected {expected_material}, got {actual_material}. "
            f"Difference: {actual_material - expected_material}")


class TestCyclicMaterial(MaterialStateTestBase):
    """Removes all material, then adds it back again. This tests remove() via sledgehammer method"""
    def test_no_options(self) -> None:
        self.collect_all_but("Progressive Pocket Gems", self.multiworld.state)
        past_material = self.multiworld.state.prog_items[self.player]["Material"]
        self.assertEqual(past_material, self.multiworld.state.prog_items[self.player]["Material"])
        self.assertLessEqual(4150 * self.difficulty, past_material)
        self.assertGreaterEqual(4650 * self.difficulty, past_material)

        for item in list(self.multiworld.state.prog_items[self.player].keys()):
            self.remove_by_name(item)
        # self.assertEqual(0, self.multiworld.state.prog_items[self.player])
        self.assertEqual(0, self.multiworld.state.prog_items[self.player]["Progressive Pawn"])
        self.assertEqual(0, self.multiworld.state.prog_items[self.player]["Material"])
        self.collect_all_but("Progressive Pocket Gems", self.multiworld.state)

        self.assertEqual(past_material, self.multiworld.state.prog_items[self.player]["Material"])

    """Same as before, but backward, to test "children" logic"""
    def test_backward(self) -> None:
        self.collect_all_but("Progressive Pocket Gems", self.multiworld.state)
        past_material = self.multiworld.state.prog_items[self.player]["Material"]
        self.assertEqual(past_material, self.multiworld.state.prog_items[self.player]["Material"])
        self.assertLessEqual(4150 * self.difficulty, past_material)
        self.assertGreaterEqual(4650 * self.difficulty, past_material)

        items = list(self.multiworld.state.prog_items[self.player].keys())
        items.reverse()
        for item in items:
            self.remove_by_name(item)
        # self.assertEqual(0, self.multiworld.state.prog_items[self.player])
        self.assertEqual(0, self.multiworld.state.prog_items[self.player]["Progressive Pawn"])
        self.assertEqual(0, self.multiworld.state.prog_items[self.player]["Material"])
        self.collect_all_but("Progressive Pocket Gems", self.multiworld.state)

        self.assertEqual(past_material, self.multiworld.state.prog_items[self.player]["Material"])

