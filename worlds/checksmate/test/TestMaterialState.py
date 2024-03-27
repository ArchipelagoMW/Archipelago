from . import CMTestBase


class MaterialStateTestBase(CMTestBase):
    def setUp(self):
        self.options["early_material"] = 0
        super().setUp()
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
    def test_no_options(self):
        past_material = self.multiworld.state.prog_items[self.player]["Material"]
        self.assertLessEqual(4050, past_material)
        self.assertGreaterEqual(4650, past_material)


class TestCyclicMaterial(MaterialStateTestBase):
    """Removes all material, then adds it back again. This tests remove() via sledgehammer method"""
    def test_no_options(self):
        past_material = self.multiworld.state.prog_items[self.player]["Material"]
        self.assertEqual(past_material, self.multiworld.state.prog_items[self.player]["Material"])
        self.assertLessEqual(4050, past_material)
        self.assertGreaterEqual(4650, past_material)

        for item in list(self.multiworld.state.prog_items[self.player].keys()):
            self.remove_by_name(item)
        # self.assertEqual(0, self.multiworld.state.prog_items[self.player])
        self.assertEqual(0, self.multiworld.state.prog_items[self.player]["Progressive Pawn"])
        self.assertEqual(0, self.multiworld.state.prog_items[self.player]["Material"])
        self.collect_all_but("Progressive Pocket Gems", self.multiworld.state)

        self.assertEqual(past_material, self.multiworld.state.prog_items[self.player]["Material"])

    """Same as before, but backward, to test "children" logic"""
    def test_backward(self):
        past_material = self.multiworld.state.prog_items[self.player]["Material"]
        self.assertEqual(past_material, self.multiworld.state.prog_items[self.player]["Material"])
        self.assertLessEqual(4050, past_material)
        self.assertGreaterEqual(4650, past_material)

        items = list(self.multiworld.state.prog_items[self.player].keys())
        items.reverse()
        for item in items:
            self.remove_by_name(item)
        # self.assertEqual(0, self.multiworld.state.prog_items[self.player])
        self.assertEqual(0, self.multiworld.state.prog_items[self.player]["Progressive Pawn"])
        self.assertEqual(0, self.multiworld.state.prog_items[self.player]["Material"])
        self.collect_all_but("Progressive Pocket Gems", self.multiworld.state)

        self.assertEqual(past_material, self.multiworld.state.prog_items[self.player]["Material"])

